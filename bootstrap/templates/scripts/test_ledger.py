#!/usr/bin/env python3
"""Tests for the traceability tool.

Every fatal condition gets a test that makes it fire, and every non-fatal one gets a test that
makes it *not* fire. A check nobody has seen fail is a check nobody knows is wired up.

    python3 scripts/test_ledger.py
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location("ledger", os.path.join(HERE, "ledger.py"))
ledger = importlib.util.module_from_spec(SPEC)
sys.modules["ledger"] = ledger
SPEC.loader.exec_module(ledger)


REGISTRY = """# Identifier registry

## Families

| Family | Pattern | Owner (relative to `docs/`) | Declared in | Kind | Traceable |
|---|---|---|---|---|:--:|
| `FR` | `FR-AREA-NN` | `spec/BRD.md` | 3 Functional requirements | requirement | yes |
| `INV` | `INV-N` | `spec/BRD.md` | 2 Invariants | invariant | yes |
| `SL` | `SL-PHASE-N` | `process/SLICE-QUEUE.md` | * | slice | no |
| `ADR` | `ADR-NNNN` | `decisions/` | * | decision | no |
"""

BRD = """# BRD

## 1. Summary

Prose that declares nothing.

## 2. Invariants

| ID | Invariant |
|---|---|
| **INV-1** | Every row carries a tenant. |

## 3. Functional requirements

### 3.1 Accounts

| ID | Requirement | Phase |
|---|---|---|
| FR-ACC-01 | Sign up. | V1 |
| FR-ACC-02 | Sign in. | V1 |
| FR-ACC-03 | Sign out. | V1 |
"""

QUEUE = """# Slice queue

Prose the human writes, above the generated block.

<!-- generated:queue -->
<!-- /generated -->

Prose the human writes, below it.
"""

BASE_CONFIG = {
    "tests": {"globs": ["**/*.test.ts"], "exclude": []},
    "placeholder_scan": {
        "include": ["docs/**/*.md"],
        "exclude": ["docs/process/COVERAGE.md", "docs/process/SLICE-QUEUE.md"],
    },
    "phases": [{"letter": "F", "name": "Foundation"}],
}


def work_order(slice_id, body=None, **kw):
    front = {
        "id": slice_id,
        "title": "does a thing",
        "phase": "F",
        "size": "S",
        "status": "queued",
        "demo": "script",
    }
    front.update(kw)
    lines = ["---"]
    for key, value in front.items():
        if isinstance(value, list):
            lines.append(key + ": [" + ", ".join(value) + "]")
        else:
            lines.append(key + ": " + str(value))
    lines.append("---")
    lines.append("")
    lines.append("# Slice " + slice_id)
    lines.append("")
    lines.append(body if body is not None else "## Demo\n\n```bash\nmake test\n```\n")
    return "\n".join(lines)


class Fixture:
    """A minimal project tree. Every test starts from a green one and breaks exactly one thing."""

    def __init__(self):
        self.root = tempfile.mkdtemp()
        self.write("docs/spec/ID-REGISTRY.md", REGISTRY)
        self.write("docs/spec/BRD.md", BRD)
        self.write("docs/process/SLICE-QUEUE.md", QUEUE)
        self.write("docs/decisions/0001-a-thing.md", "# ADR-0001\n")
        self.write("docs/process/work-orders/F1.md", work_order("SL-F1", satisfies=["FR-ACC-01"]))
        self.write(
            "docs/process/work-orders/F2.md",
            work_order("SL-F2", satisfies=["FR-ACC-02"], depends_on=["SL-F1"]),
        )
        self.write("src/accounts.test.ts", "it('[FR-ACC-01] signs a person up', () => {});\n")
        self.config(BASE_CONFIG)

    def config(self, data):
        self.write("scripts/ledger.config.json", json.dumps(data))

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)

    def read(self, rel):
        with open(os.path.join(self.root, rel), encoding="utf-8") as handle:
            return handle.read()

    def run(self, *argv):
        err, out = io.StringIO(), io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
            code = ledger.main(list(argv) + ["--root", self.root])
        return code, err.getvalue()

    def close(self):
        shutil.rmtree(self.root, ignore_errors=True)


class LedgerTest(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.close)

    def green(self):
        code, err = self.fx.run("all")
        self.assertEqual(code, 0, err)
        code, err = self.fx.run("check")
        self.assertEqual(code, 0, err)

    # -- the happy path -----------------------------------------------------------------------

    def test_a_green_tree_passes_and_writes_both_artefacts(self):
        self.green()
        coverage = self.fx.read("docs/process/COVERAGE.md")
        self.assertIn("# Requirement coverage", coverage)
        self.assertIn("| FR-ACC-01 | ● | SL-F1 |", coverage)
        self.assertIn(ledger.QUEUE_BEGIN, self.fx.read("docs/process/SLICE-QUEUE.md"))

    def test_status_is_derived_from_claim_and_proof_together(self):
        self.green()
        coverage = self.fx.read("docs/process/COVERAGE.md")
        self.assertIn("| FR-ACC-01 | ● |", coverage)
        self.assertIn("| FR-ACC-02 | ◐ |", coverage)
        self.assertIn("## Claimed without proof", coverage)
        self.assertIn("| FR-ACC-02 | SL-F2 |", coverage)
        self.assertIn("| FR-ACC-03 | ○ |", coverage)
        self.assertIn("| INV-1 | ○ |", coverage)

    def test_the_proof_column_carries_the_test_name_not_the_line(self):
        self.green()
        self.assertIn("`[FR-ACC-01] signs a person up`", self.fx.read("docs/process/COVERAGE.md"))

    def test_output_is_byte_identical_across_runs(self):
        self.fx.run("all")
        first = self.fx.read("docs/process/COVERAGE.md")
        self.fx.run("all")
        self.assertEqual(first, self.fx.read("docs/process/COVERAGE.md"))

    def test_the_queue_is_ordered_by_dependency(self):
        self.fx.write("docs/process/work-orders/F0.md", work_order("SL-F0", satisfies=["FR-ACC-03"]))
        self.fx.write(
            "docs/process/work-orders/F1.md",
            work_order("SL-F1", satisfies=["FR-ACC-01"], depends_on=["SL-F0"]),
        )
        self.green()
        queue = self.fx.read("docs/process/SLICE-QUEUE.md")
        self.assertLess(queue.index("**SL-F0**"), queue.index("**SL-F1**"))
        self.assertLess(queue.index("**SL-F1**"), queue.index("**SL-F2**"))

    def test_the_prose_around_the_generated_block_survives(self):
        self.green()
        queue = self.fx.read("docs/process/SLICE-QUEUE.md")
        self.assertIn("Prose the human writes, above the generated block.", queue)
        self.assertIn("Prose the human writes, below it.", queue)

    # -- fatal conditions ---------------------------------------------------------------------

    def test_an_annotation_naming_an_undeclared_number_is_fatal(self):
        self.fx.run("all")
        self.fx.write("src/typo.test.ts", "it('[FR-ACC-99] a typo', () => {});\n")
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("[FR-ACC-99] is not declared in FR's section", err)
        self.assertIn("src/typo.test.ts", err)

    def test_a_claim_on_an_undeclared_number_is_fatal(self):
        self.fx.write("docs/process/work-orders/F2.md", work_order("SL-F2", satisfies=["FR-ACC-77"]))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("FR-ACC-77", err)

    def test_a_traceable_family_with_no_identifiers_is_fatal(self):
        self.fx.write("docs/spec/BRD.md", BRD.replace("## 2. Invariants", "## 2. Invariance"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("registry declares family INV, which yields no identifiers", err)

    def test_a_family_declared_twice_in_the_registry_is_fatal(self):
        self.fx.write(
            "docs/spec/ID-REGISTRY.md",
            REGISTRY + "| `FR` | `FR-AREA-NN` | `spec/OTHER.md` | * | requirement | yes |\n",
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("registry declares family FR twice", err)

    def test_an_identifier_declared_twice_in_one_section_is_fatal(self):
        self.fx.write("docs/spec/BRD.md", BRD.replace("| FR-ACC-03 |", "| FR-ACC-01 |"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("FR-ACC-01 is declared twice", err)

    def test_a_traceable_family_owning_a_directory_is_fatal(self):
        self.fx.write(
            "docs/spec/ID-REGISTRY.md",
            REGISTRY.replace("| `ADR` | `ADR-NNNN` | `decisions/` | * | decision | no |",
                             "| `ADR` | `ADR-NNNN` | `decisions/` | * | decision | yes |"),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("owns the directory", err)

    def test_a_named_adr_that_does_not_exist_is_fatal(self):
        self.fx.write(
            "docs/process/work-orders/F2.md",
            work_order("SL-F2", satisfies=["FR-ACC-02"], adr=["ADR-0009"]),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("names ADR-0009", err)

    def test_a_named_adr_that_exists_is_accepted(self):
        self.fx.write(
            "docs/process/work-orders/F2.md",
            work_order("SL-F2", satisfies=["FR-ACC-02"], adr=["ADR-0001"]),
        )
        self.green()

    def test_a_missing_demo_section_is_fatal(self):
        self.fx.write(
            "docs/process/work-orders/F2.md",
            work_order("SL-F2", "## Notes\n\nNothing.\n", satisfies=["FR-ACC-02"]),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("has no Demo section", err)

    def test_a_script_demo_with_no_code_block_is_fatal(self):
        self.fx.write(
            "docs/process/work-orders/F2.md",
            work_order("SL-F2", "## Demo\n\nRun it and look.\n", satisfies=["FR-ACC-02"]),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("carries no runnable code block", err)

    def test_a_demo_carrying_a_placeholder_identifier_is_fatal(self):
        self.fx.write(
            "docs/process/work-orders/F2.md",
            work_order(
                "SL-F2",
                "## Demo\n\n```bash\ncurl /v1/accounts/<ACCOUNT ID>\n```\n",
                satisfies=["FR-ACC-02"],
            ),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("nobody types an identifier", err)

    def test_a_ui_demo_needs_numbered_steps_and_an_expectation(self):
        self.fx.write(
            "docs/process/work-orders/F2.md",
            work_order("SL-F2", "## Demo\n\nClick around.\n", satisfies=["FR-ACC-02"], demo="ui"),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("numbered steps and an Expected line", err)

    def test_a_ui_demo_that_is_specific_is_accepted(self):
        self.fx.write(
            "docs/process/work-orders/F2.md",
            work_order(
                "SL-F2",
                "## Demo\n\n1. Open the sign-up page.\n2. Submit a used address.\n\n"
                "**Expected:** the field reports the address is taken, and no account is created.\n",
                satisfies=["FR-ACC-02"],
                demo="ui",
            ),
        )
        self.green()

    def test_a_dependency_on_an_unknown_slice_is_fatal(self):
        self.fx.write(
            "docs/process/work-orders/F2.md",
            work_order("SL-F2", satisfies=["FR-ACC-02"], depends_on=["SL-F9"]),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("depends_on names SL-F9", err)

    def test_a_dependency_cycle_is_fatal(self):
        self.fx.write(
            "docs/process/work-orders/F1.md",
            work_order("SL-F1", satisfies=["FR-ACC-01"], depends_on=["SL-F2"]),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("cycle", err)

    def test_a_done_slice_with_no_summary_is_fatal(self):
        self.fx.write(
            "docs/process/work-orders/F1.md",
            work_order("SL-F1", satisfies=["FR-ACC-01"], status="done"),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("status is done", err)

    def test_a_done_slice_with_a_summary_is_accepted(self):
        self.fx.write(
            "docs/process/work-orders/F1.md",
            work_order("SL-F1", satisfies=["FR-ACC-01"], status="done"),
        )
        self.fx.write("docs/process/slices/SL-F1.md", "# Slice SL-F1 - summary\n")
        self.green()

    def test_an_unresolved_placeholder_in_a_document_is_fatal(self):
        self.fx.write("docs/spec/NOTES.md", "# Notes\n\nOwned by <THE TEAM>.\n")
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("unresolved placeholder <THE TEAM>", err)

    def test_a_placeholder_inside_template_guidance_is_ignored(self):
        self.fx.write("docs/spec/NOTES.md", "# Notes\n\n> Replace <THE TEAM> with a name.\n")
        self.green()

    def test_a_placeholder_is_caught_whatever_its_first_character(self):
        """The templates spell placeholders every way — `<N>`, `<the gate commands>`, `<150>`,
        `<test:all>` — and a scan that only knew the capitalised shape let most of them through."""
        for token in ("<the gate commands>", "<150>", "<test:all>", "<dev cli>", "<suffix>"):
            self.fx.write("docs/spec/NOTES.md", "# Notes\n\nRun " + token + " first.\n")
            code, err = self.fx.run("check")
            self.assertEqual(code, 1, token)
            self.assertIn("unresolved placeholder " + token, err)

    def test_markup_in_angle_brackets_is_not_a_placeholder(self):
        self.fx.write(
            "docs/spec/NOTES.md",
            "# Notes\n\nSee <https://example.com/x> or <ops@example.com>.<br>\n"
            "<!-- a comment --> and <details><summary>more</summary></details>\n"
            "where a < b and c > d.\n",
        )
        self.green()

    def test_notation_inside_code_is_not_a_placeholder(self):
        """A finished document still says `/slice-open <id>` and `slice/<ID>-<slug>`. Those are
        shapes, not gaps, and a scan that failed on them would fail every project for ever."""
        self.fx.write(
            "docs/spec/NOTES.md",
            "# Notes\n\nRun `/slice-open <id>` on `slice/<ID>-<slug>`.\n\n"
            "```text\n### MR-NN — <short title>\n```\n",
        )
        self.green()
        self.fx.write("docs/spec/NOTES.md", "# Notes\n\nRun `/slice-open <id>` before <The gate>.\n")
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("unresolved placeholder <The gate>", err)
        self.assertNotIn("<id>", err)

    def test_a_registry_section_the_document_does_not_carry_is_named(self):
        """An empty table and a missing heading are different mistakes with different fixes."""
        self.fx.write("docs/spec/BRD.md", BRD.replace("## 2. Invariants", "## 2. Invariance"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("INV is declared in spec/BRD.md", err)
        self.assertIn("has no such heading", err)

    def test_a_stale_artefact_fails_the_check(self):
        self.fx.run("all")
        self.fx.write("docs/process/COVERAGE.md", "# hand-edited\n")
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("is stale", err)

    def test_a_duplicate_slice_id_is_fatal(self):
        self.fx.write("docs/process/work-orders/F3.md", work_order("SL-F1", satisfies=["FR-ACC-03"]))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("is already used by", err)

    # -- parallel work ------------------------------------------------------------------------

    def test_two_active_slices_touching_one_surface_are_fatal_when_a_limit_is_set(self):
        config = dict(BASE_CONFIG, mode="team", wip_limit=4)
        self.fx.config(config)
        for name, sid, req in (("F1", "SL-F1", "FR-ACC-01"), ("F2", "SL-F2", "FR-ACC-02")):
            self.fx.write(
                "docs/process/work-orders/" + name + ".md",
                work_order(sid, satisfies=[req], status="in-progress", touches=["schema/accounts"]),
            )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("both touch schema/accounts", err)

    def test_the_wip_limit_is_enforced(self):
        self.fx.config(dict(BASE_CONFIG, mode="team", wip_limit=1))
        for name, sid, req in (("F1", "SL-F1", "FR-ACC-01"), ("F2", "SL-F2", "FR-ACC-02")):
            self.fx.write(
                "docs/process/work-orders/" + name + ".md",
                work_order(sid, satisfies=[req], status="in-progress"),
            )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("over the limit of 1", err)

    def test_the_queue_names_an_owner_in_team_mode(self):
        self.fx.config(dict(BASE_CONFIG, mode="team"))
        self.fx.write(
            "docs/process/work-orders/F1.md",
            work_order("SL-F1", satisfies=["FR-ACC-01"], owner="ada"),
        )
        self.green()
        self.assertIn("| Owner |", self.fx.read("docs/process/SLICE-QUEUE.md"))
        self.assertIn("| ada |", self.fx.read("docs/process/SLICE-QUEUE.md"))

    # -- deliberately not fatal ---------------------------------------------------------------

    def test_an_annotation_from_an_unregistered_family_is_reported_not_fatal(self):
        self.fx.write("src/other.test.ts", "it('[Process-4] holds', () => {});\n")
        self.green()
        coverage = self.fx.read("docs/process/COVERAGE.md")
        self.assertIn("## Annotations outside the registry", coverage)
        self.assertIn("| Process-4 |", coverage)

    def test_a_claim_from_an_unregistered_family_is_reported_not_fatal(self):
        self.fx.write(
            "docs/process/work-orders/F2.md",
            work_order("SL-F2", satisfies=["FR-ACC-02", "Process-4"]),
        )
        self.green()
        coverage = self.fx.read("docs/process/COVERAGE.md")
        self.assertIn("## Claims outside the registry", coverage)
        self.assertIn("| Process-4 | SL-F2 |", coverage)

    # -- the parsers --------------------------------------------------------------------------

    def test_a_section_stops_at_a_sibling_and_includes_subsections(self):
        self.assertEqual(
            ledger.declared_ids(BRD, "3 Functional requirements"),
            ["FR-ACC-01", "FR-ACC-02", "FR-ACC-03"],
        )
        self.assertEqual(ledger.declared_ids(BRD, "2 Invariants"), ["INV-1"])

    def test_a_comment_inside_a_fenced_block_is_not_a_heading(self):
        """A demo script full of `#` comments must not truncate its own section."""
        self.fx.write(
            "docs/process/work-orders/F2.md",
            work_order(
                "SL-F2",
                "## Demo\n\n### Script\n\n```bash\n# 1 - the first step\nmake test\n```\n\n"
                "## Out of scope\n\nNothing.\n",
                satisfies=["FR-ACC-02"],
            ),
        )
        self.green()

    # -- the requirement detail track -----------------------------------------------------------

    def detail_on(self, **over):
        """Turn the track on. Off by default, so every existing test stays a test of the loop."""
        spec = {"dir": "docs/process/requirements", "families": ["FR", "INV"], "phase_pattern": "V1|V2|R"}
        spec.update(over)
        config = dict(BASE_CONFIG)
        config["requirements"] = spec
        self.fx.config(config)

    def detail(self, ident="FR-ACC-01", quote="Sign up.", area="FR-ACC", phase="V1", sections=None, **front):
        data = {
            "id": ident,
            "area": area,
            "phase": phase,
            "status": "draft",
            "drafted_by": "sam",
            "approved_by": '""',
            "reviewed_against": "1.0",
            "surface": "[cli]",
        }
        data.update(front)
        out = ["---"] + [k + ": " + str(v) for k, v in data.items()] + ["---", "", "# " + ident, ""]
        for title in ledger.DETAIL_SECTIONS if sections is None else sections:
            out += ["## " + title, ""]
            if title == "The requirement":
                out += ["> " + quote, ""]
        return "\n".join(out) + "\n"

    def file_detail(self, rel, text):
        self.fx.write("docs/process/requirements/" + rel, text)

    def test_a_detail_file_that_quotes_the_requirement_verbatim_passes(self):
        self.detail_on()
        self.file_detail("FR-ACC/FR-ACC-01.md", self.detail())
        self.green()
        coverage = self.fx.read("docs/process/COVERAGE.md")
        self.assertIn("## Requirement detail", coverage)
        self.assertIn("| draft | 1 |", coverage)

    def test_a_paraphrased_requirement_fails(self):
        """The one rule of the track, and the only thing standing between it and a second spec."""
        self.detail_on()
        self.file_detail("FR-ACC/FR-ACC-01.md", self.detail(quote="A person can sign up."))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("quotes FR-ACC-01 differently from the specification", err)

    def test_a_quote_wrapped_over_several_lines_is_accepted(self):
        self.detail_on()
        text = self.detail().replace("> Sign up.", "> Sign\n> up.")
        self.file_detail("FR-ACC/FR-ACC-01.md", text)
        self.green()

    def test_a_file_in_the_wrong_area_directory_fails(self):
        self.detail_on()
        self.file_detail("FR/FR-ACC-01.md", self.detail())
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("sits under FR and its identifier files under FR-ACC", err)

    def test_a_file_naming_an_undeclared_identifier_fails(self):
        """How a withdrawn requirement's file gets found rather than quietly outliving it."""
        self.detail_on()
        self.file_detail("FR-ACC/FR-ACC-99.md", self.detail(ident="FR-ACC-99", quote="Gone."))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("FR-ACC-99 is not declared in the specification", err)

    def test_a_family_outside_the_covered_set_is_refused(self):
        self.detail_on(families=["FR"])
        self.file_detail("INV/INV-1.md", self.detail(ident="INV-1", area="INV", phase="", quote="Every row carries a tenant."))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("belongs to no family the detail track covers", err)

    def test_an_invariant_whose_table_has_no_phase_column_is_not_phase_checked(self):
        self.detail_on()
        self.file_detail("INV/INV-1.md", self.detail(ident="INV-1", area="INV", phase="V1", quote="Every row carries a tenant."))
        self.green()

    def test_a_phase_that_disagrees_with_the_specification_fails(self):
        self.detail_on()
        self.file_detail("FR-ACC/FR-ACC-01.md", self.detail(phase="V2"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("says V2 and the specification says V1", err)

    def test_a_reviewed_file_naming_no_approver_fails(self):
        self.detail_on()
        self.file_detail("FR-ACC/FR-ACC-01.md", self.detail(status="reviewed"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("names no approver", err)

    def test_a_reviewed_file_with_an_approver_passes_and_counts_as_reviewed(self):
        self.detail_on()
        self.file_detail("FR-ACC/FR-ACC-01.md", self.detail(status="reviewed", approved_by="dana"))
        self.green()
        self.assertIn("| reviewed | 1 |", self.fx.read("docs/process/COVERAGE.md"))

    def test_a_status_outside_the_vocabulary_fails(self):
        self.detail_on()
        self.file_detail("FR-ACC/FR-ACC-01.md", self.detail(status="nearly"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("status is nearly", err)

    def test_a_missing_front_matter_field_fails(self):
        self.detail_on()
        text = self.detail().replace("drafted_by: sam\n", "")
        self.file_detail("FR-ACC/FR-ACC-01.md", text)
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("front matter has no drafted_by", err)

    def test_a_missing_template_section_fails(self):
        self.detail_on()
        keep = [t for t in ledger.DETAIL_SECTIONS if t != "Observable behaviour"]
        self.file_detail("FR-ACC/FR-ACC-01.md", self.detail(sections=keep))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("has no Observable behaviour section", err)

    def test_a_verdict_outside_the_four_fails(self):
        """`mostly works` is the verdict the vocabulary exists to refuse."""
        self.detail_on()
        text = self.detail().replace(
            "## Verification\n",
            "## Verification\n\n| Date | Verdict | By | Evidence |\n|---|---|---|---|\n"
            "| 2026-01-01 | mostly works | sam | ran it |\n",
        )
        self.file_detail("FR-ACC/FR-ACC-01.md", text)
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("records the verdict mostly works", err)

    def test_a_verdict_inside_the_four_passes(self):
        self.detail_on()
        text = self.detail().replace(
            "## Verification\n",
            "## Verification\n\n| Date | Verdict | By | Evidence |\n|---|---|---|---|\n"
            "| 2026-01-01 | gap | sam | no cross-tenant case |\n",
        )
        self.file_detail("FR-ACC/FR-ACC-01.md", text)
        self.green()

    def test_two_files_for_one_requirement_fail(self):
        self.detail_on()
        self.file_detail("FR-ACC/FR-ACC-01.md", self.detail())
        self.file_detail("FR-ACC/nested/FR-ACC-01.md", self.detail(area="nested"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("is already detailed by", err)

    def test_the_backlog_is_listed_and_does_not_fail_the_build(self):
        """`FR-ACC-01` is satisfied with no reviewed file. Listed, not averaged away, not fatal."""
        self.detail_on()
        self.green()
        coverage = self.fx.read("docs/process/COVERAGE.md")
        self.assertIn("### Satisfied, and not yet reviewable by hand", coverage)
        self.assertIn("| FR-ACC-01 | none |", coverage)

    def test_requiring_a_detail_for_every_satisfied_requirement_is_opt_in(self):
        self.detail_on(require_detail_for_satisfied=True)
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("FR-ACC-01 is satisfied and has no detail file", err)

    def test_the_track_is_silent_when_it_is_not_installed(self):
        """A project that declined the track is not failed for a directory it does not have."""
        self.green()
        self.assertNotIn("## Requirement detail", self.fx.read("docs/process/COVERAGE.md"))

    def test_the_directory_readme_is_not_read_as_a_detail_file(self):
        self.detail_on()
        self.file_detail("README.md", "# Requirement detail\n\nProse, no front matter.\n")
        self.green()

    def test_headings_match_loosely(self):
        self.assertEqual(ledger.normalise("§9 Functional requirements"), "9functionalrequirements")
        self.assertEqual(ledger.normalise("9. Functional requirements"), "9functionalrequirements")

    def test_a_family_is_matched_by_its_longest_prefix(self):
        families = ledger.parse_registry(
            REGISTRY + "| `FRX` | `FRX-NN` | `spec/BRD.md` | * | x | no |\n"
        )
        self.assertEqual(ledger.family_for("FRX-01", families).family, "FRX")
        self.assertEqual(ledger.family_for("FR-ACC-01", families).family, "FR")

    def test_front_matter_drops_an_inline_comment(self):
        """Every template carries aligned comments on its front matter; a drafter leaves them."""
        data, _body = ledger.parse_front_matter(
            "---\nid: SL-F1\nstatus: queued          # queued | in-progress | done\n"
            'dep: "—"                # or an external mark\n'
            "depends_on: []          # [SL-D1, SL-D2] — the order is derived from this\n"
            "title: fixes the thing\n---\nbody\n"
        )
        self.assertEqual(data["status"], "queued")
        self.assertEqual(data["dep"], "—")
        self.assertEqual(data["depends_on"], [])
        self.assertEqual(data["title"], "fixes the thing")

    def test_a_hash_inside_a_quoted_value_is_not_a_comment(self):
        data, _body = ledger.parse_front_matter('---\ntitle: "closes #12"\n---\nbody\n')
        self.assertEqual(data["title"], "closes #12")

    def test_a_work_order_whose_front_matter_keeps_its_comments_still_parses(self):
        self.fx.write(
            "docs/process/work-orders/F2.md",
            work_order("SL-F2", satisfies=["FR-ACC-02"]).replace(
                "status: queued", "status: queued          # queued | in-progress | done"
            ),
        )
        self.green()
        self.assertIn("| **SL-F2** | F | S | — | queued |", self.fx.read("docs/process/SLICE-QUEUE.md"))

    def test_front_matter_reads_inline_and_block_lists(self):
        data, body = ledger.parse_front_matter(
            "---\nid: SL-F1\nsatisfies: [FR-A-01, FR-A-02]\npartial:\n  - INV-1\n---\nbody\n"
        )
        self.assertEqual(data["id"], "SL-F1")
        self.assertEqual(data["satisfies"], ["FR-A-01", "FR-A-02"])
        self.assertEqual(data["partial"], ["INV-1"])
        self.assertEqual(body.strip(), "body")


if __name__ == "__main__":
    unittest.main(verbosity=2)
