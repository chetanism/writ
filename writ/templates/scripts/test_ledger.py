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


ADR = """# ADR-0001 — A thing is decided

| | |
|---|---|
| **Constrains** | INV-1 |
"""


REGISTRY = """# Identifier registry

## Families

| Family | Pattern | Owner (relative to `writ/`) | Declared in | Kind | Traceable |
|---|---|---|---|---|:--:|
| `FR` | `FR-AREA-NN` | `spec/BRD.md` | 3 Functional requirements | requirement | yes |
| `INV` | `INV-N` | `spec/BRD.md` | 2 Invariants | invariant | yes |
| `SL` | `SL-NNN` | `process/work-orders/` | * | slice | no |
| `M` | `MN` | `spec/milestones.md` | * | milestone | no |
| `Q` | `Q-NNN` | `spec/questions.md` | * | open question | no |
| `X` | `X-NNN` | `spec/CHANGELOG.md` | * | amendment | no |
| `CR` | `CR-NNN` | `spec/changes/` | * | change request | no |
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

| ID | Requirement | Target |
|---|---|---|
| FR-ACC-01 | Sign up. | M1 |
| FR-ACC-02 | Sign in. | M1 |
| FR-ACC-03 | Sign out. | M1 |
"""

MILESTONES = """# Milestones

| ID | Milestone | Exit criterion | Status |
|---|---|---|---|
| M1 | First release | Somebody signs up. | active |
| M2 | Second release | Somebody signs in twice. | planned |
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
        "include": ["writ/**/*.md"],
        "exclude": ["writ/process/COVERAGE.md", "writ/process/SLICE-QUEUE.md"],
    },
    "phases": [{"code": "P01", "name": "Foundation"}, {"code": "P02", "name": "Access"}],
}


def work_order(slice_id, body=None, **kw):
    front = {
        "id": slice_id,
        "title": "does a thing",
        "phase": "P01",
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


CHANGELOG = """# Changelog

| ID | Date | Touches | Change | Cause | By |
|---|---|---|---|---|---|
"""


def change_request(ident="CR-001", status="accepted", approved_by="neha", decided_on="2026-09-10", target="M2"):
    return "\n".join([
        "---",
        "id: " + ident,
        "status: " + status,
        "requested_by: neha",
        "approved_by: " + approved_by,
        "decided_on: " + decided_on,
        "target: " + target,
        "---",
        "",
        "# " + ident + " — sign out twice",
        "",
        "## The job",
        "",
        "When somebody leaves a shared machine, they need to be signed out everywhere.",
        "",
        "## Changes",
        "",
        "| Op | ID | Text | Target |",
        "|---|---|---|---|",
        "| add | FR-ACC-04 | Sign out twice. | M2 |",
        "",
        "## Impact",
        "",
        "Touches FR-ACC-03. No invariant conflicts.",
        "",
        "## Decision",
        "",
        "Accepted.",
        "",
    ])


class Fixture:
    """A minimal project tree. Every test starts from a green one and breaks exactly one thing."""

    def __init__(self):
        self.root = tempfile.mkdtemp()
        self.write("writ/spec/ID-REGISTRY.md", REGISTRY)
        self.write("writ/spec/BRD.md", BRD)
        self.write("writ/spec/milestones.md", MILESTONES)
        self.write("writ/process/SLICE-QUEUE.md", QUEUE)
        self.write("writ/decisions/0001-a-thing.md", ADR)
        self.write("writ/process/work-orders/001.md", work_order("SL-001", satisfies=["FR-ACC-01"]))
        self.write(
            "writ/process/work-orders/002.md",
            work_order("SL-002", satisfies=["FR-ACC-02"], depends_on=["SL-001"]),
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


STORY_MD = """## Story 1 — a visitor signs up

**Job:** When somebody wants an account, I want to create one, so I can sign in.

- **Given** an address nobody holds
  **When** the visitor signs up
  **Then** the account exists
"""


def detail_md(ident="FR-ACC-01", quote="Sign up.", area="FR-ACC", target="M1", sections=None, story=STORY_MD, **front):
    """A detail file that passes. The story sits after *Preconditions and data*, where the
    template puts it; `story=""` writes a file that tells none."""
    data = {
        "id": ident,
        "area": area,
        "target": target,
        "status": "draft",
        "drafted_by": "sam",
        "approved_by": '""',
        "reviewed_against": "1.0",
        "revised_on": "2026-09-01",
        "surface": "[cli]",
    }
    data.update(front)
    out = ["---"] + [k + ": " + str(v) for k, v in data.items()] + ["---", "", "# " + ident, ""]
    for title in ledger.DETAIL_SECTIONS if sections is None else sections:
        out += ["## " + title, ""]
        if title == "The requirement":
            out += ["> " + quote, ""]
        if title == "Preconditions and data" and story:
            out += [story]
    return "\n".join(out) + "\n"


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
        coverage = self.fx.read("writ/process/COVERAGE.md")
        self.assertIn("# Requirement coverage", coverage)
        self.assertIn("| FR-ACC-01 | ● | SL-001 |", coverage)
        self.assertIn(ledger.QUEUE_BEGIN, self.fx.read("writ/process/SLICE-QUEUE.md"))

    def test_status_is_derived_from_claim_and_proof_together(self):
        self.green()
        coverage = self.fx.read("writ/process/COVERAGE.md")
        self.assertIn("| FR-ACC-01 | ● |", coverage)
        self.assertIn("| FR-ACC-02 | ◐ |", coverage)
        self.assertIn("## Claimed without proof", coverage)
        self.assertIn("| FR-ACC-02 | SL-002 |", coverage)
        self.assertIn("| FR-ACC-03 | ○ |", coverage)
        self.assertIn("| INV-1 | ○ |", coverage)

    def test_the_proof_column_carries_the_test_name_not_the_line(self):
        self.green()
        self.assertIn("`[FR-ACC-01] signs a person up`", self.fx.read("writ/process/COVERAGE.md"))

    def test_output_is_byte_identical_across_runs(self):
        self.fx.run("all")
        first = self.fx.read("writ/process/COVERAGE.md")
        self.fx.run("all")
        self.assertEqual(first, self.fx.read("writ/process/COVERAGE.md"))

    def test_the_queue_is_ordered_by_dependency(self):
        self.fx.write("writ/process/work-orders/000.md", work_order("SL-000", satisfies=["FR-ACC-03"]))
        self.fx.write(
            "writ/process/work-orders/001.md",
            work_order("SL-001", satisfies=["FR-ACC-01"], depends_on=["SL-000"]),
        )
        self.green()
        queue = self.fx.read("writ/process/SLICE-QUEUE.md")
        self.assertLess(queue.index("**SL-000**"), queue.index("**SL-001**"))
        self.assertLess(queue.index("**SL-001**"), queue.index("**SL-002**"))

    def test_the_prose_around_the_generated_block_survives(self):
        self.green()
        queue = self.fx.read("writ/process/SLICE-QUEUE.md")
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
        self.fx.write("writ/process/work-orders/002.md", work_order("SL-002", satisfies=["FR-ACC-77"]))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("FR-ACC-77", err)

    def test_a_traceable_family_with_no_identifiers_is_fatal(self):
        self.fx.write("writ/spec/BRD.md", BRD.replace("## 2. Invariants", "## 2. Invariance"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("registry declares family INV, which yields no identifiers", err)

    def test_a_family_declared_twice_in_the_registry_is_fatal(self):
        self.fx.write(
            "writ/spec/ID-REGISTRY.md",
            REGISTRY + "| `FR` | `FR-AREA-NN` | `spec/OTHER.md` | * | requirement | yes |\n",
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("registry declares family FR twice", err)

    def test_an_identifier_declared_twice_in_one_section_is_fatal(self):
        self.fx.write("writ/spec/BRD.md", BRD.replace("| FR-ACC-03 |", "| FR-ACC-01 |"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("FR-ACC-01 is declared twice", err)

    def test_a_traceable_family_may_own_a_directory_of_registers(self):
        """One register file per area, beside that area's detail files — and a file named for an
        identifier is an elaboration, never a register, whatever tables it carries."""
        self.fx.write(
            "writ/spec/ID-REGISTRY.md",
            REGISTRY.replace("| `FR` | `FR-AREA-NN` | `spec/BRD.md` | 3 Functional requirements | requirement | yes |",
                             "| `FR` | `FR-AREA-NN` | `spec/requirements/` | * | requirement | yes |"),
        )
        self.fx.write("writ/spec/BRD.md", BRD.split("## 3. Functional requirements")[0])
        self.fx.write(
            "writ/spec/requirements/FR-ACC/index.md",
            "# FR-ACC\n\n| ID | Requirement | Target |\n|---|---|---|\n| FR-ACC-01 | Sign up. | M1 |\n| FR-ACC-02 | Sign in. | M1 |\n",
        )
        self.fx.write(
            "writ/spec/requirements/FR-ACC/FR-ACC-01.md",
            "# FR-ACC-01\n\n| ID | Requirement |\n|---|---|\n| FR-ACC-02 | Not a second declaration. |\n",
        )
        self.green()
        self.assertIn("| FR-ACC-01 | ● |", self.fx.read("writ/process/COVERAGE.md"))
        self.assertEqual(self.fx.read("writ/INDEX.md").split("## SL")[0].count("| FR-ACC-02 |"), 1)

    def test_a_named_adr_that_does_not_exist_is_fatal(self):
        self.fx.write(
            "writ/process/work-orders/002.md",
            work_order("SL-002", satisfies=["FR-ACC-02"], adr=["ADR-0009"]),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("names ADR-0009", err)

    def test_a_named_adr_that_exists_is_accepted(self):
        self.fx.write(
            "writ/process/work-orders/002.md",
            work_order("SL-002", satisfies=["FR-ACC-02"], adr=["ADR-0001"]),
        )
        self.green()

    def test_a_missing_demo_section_is_fatal(self):
        self.fx.write(
            "writ/process/work-orders/002.md",
            work_order("SL-002", "## Notes\n\nNothing.\n", satisfies=["FR-ACC-02"]),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("has no Demo section", err)

    def test_a_script_demo_with_no_code_block_is_fatal(self):
        self.fx.write(
            "writ/process/work-orders/002.md",
            work_order("SL-002", "## Demo\n\nRun it and look.\n", satisfies=["FR-ACC-02"]),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("carries no runnable code block", err)

    def test_a_demo_carrying_a_placeholder_identifier_is_fatal(self):
        self.fx.write(
            "writ/process/work-orders/002.md",
            work_order(
                "SL-002",
                "## Demo\n\n```bash\ncurl /v1/accounts/<ACCOUNT ID>\n```\n",
                satisfies=["FR-ACC-02"],
            ),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("nobody types an identifier", err)

    def test_a_ui_demo_needs_numbered_steps_and_an_expectation(self):
        self.fx.write(
            "writ/process/work-orders/002.md",
            work_order("SL-002", "## Demo\n\nClick around.\n", satisfies=["FR-ACC-02"], demo="ui"),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("numbered steps and an Expected line", err)

    def test_a_ui_demo_that_is_specific_is_accepted(self):
        self.fx.write(
            "writ/process/work-orders/002.md",
            work_order(
                "SL-002",
                "## Demo\n\n1. Open the sign-up page.\n2. Submit a used address.\n\n"
                "**Expected:** the field reports the address is taken, and no account is created.\n",
                satisfies=["FR-ACC-02"],
                demo="ui",
            ),
        )
        self.green()

    def test_a_dependency_on_an_unknown_slice_is_fatal(self):
        self.fx.write(
            "writ/process/work-orders/002.md",
            work_order("SL-002", satisfies=["FR-ACC-02"], depends_on=["SL-F9"]),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("depends_on names SL-F9", err)

    def test_a_dependency_cycle_is_fatal(self):
        self.fx.write(
            "writ/process/work-orders/001.md",
            work_order("SL-001", satisfies=["FR-ACC-01"], depends_on=["SL-002"]),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("cycle", err)

    def test_a_done_slice_with_no_summary_is_fatal(self):
        self.fx.write(
            "writ/process/work-orders/001.md",
            work_order("SL-001", satisfies=["FR-ACC-01"], status="done"),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("status is done", err)

    def test_a_done_slice_with_a_summary_is_accepted(self):
        self.fx.write(
            "writ/process/work-orders/001.md",
            work_order("SL-001", satisfies=["FR-ACC-01"], status="done"),
        )
        self.fx.write("writ/process/slices/SL-001.md", "# Slice SL-001 - summary\n")
        self.green()

    def test_an_unresolved_placeholder_in_a_document_is_fatal(self):
        self.fx.write("writ/spec/NOTES.md", "# Notes\n\nOwned by <THE TEAM>.\n")
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("unresolved placeholder <THE TEAM>", err)

    def test_a_placeholder_inside_template_guidance_is_ignored(self):
        self.fx.write("writ/spec/NOTES.md", "# Notes\n\n> Replace <THE TEAM> with a name.\n")
        self.green()

    def test_a_placeholder_is_caught_whatever_its_first_character(self):
        """The templates spell placeholders every way — `<N>`, `<the gate commands>`, `<150>`,
        `<test:all>` — and a scan that only knew the capitalised shape let most of them through."""
        for token in ("<the gate commands>", "<150>", "<test:all>", "<dev cli>", "<suffix>"):
            self.fx.write("writ/spec/NOTES.md", "# Notes\n\nRun " + token + " first.\n")
            code, err = self.fx.run("check")
            self.assertEqual(code, 1, token)
            self.assertIn("unresolved placeholder " + token, err)

    def test_markup_in_angle_brackets_is_not_a_placeholder(self):
        self.fx.write(
            "writ/spec/NOTES.md",
            "# Notes\n\nSee <https://example.com/x> or <ops@example.com>.<br>\n"
            "<!-- a comment --> and <details><summary>more</summary></details>\n"
            "where a < b and c > d.\n",
        )
        self.green()

    def test_notation_inside_code_is_not_a_placeholder(self):
        """A finished document still says `/slice-open <id>` and `slice/<ID>-<slug>`. Those are
        shapes, not gaps, and a scan that failed on them would fail every project for ever."""
        self.fx.write(
            "writ/spec/NOTES.md",
            "# Notes\n\nRun `/slice-open <id>` on `slice/<ID>-<slug>`.\n\n"
            "```text\n### MR-NN — <short title>\n```\n",
        )
        self.green()
        self.fx.write("writ/spec/NOTES.md", "# Notes\n\nRun `/slice-open <id>` before <The gate>.\n")
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("unresolved placeholder <The gate>", err)
        self.assertNotIn("<id>", err)

    def test_a_registry_section_the_document_does_not_carry_is_named(self):
        """An empty table and a missing heading are different mistakes with different fixes."""
        self.fx.write("writ/spec/BRD.md", BRD.replace("## 2. Invariants", "## 2. Invariance"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("INV is declared in spec/BRD.md", err)
        self.assertIn("has no such heading", err)

    def test_a_stale_artefact_fails_the_check(self):
        self.fx.run("all")
        self.fx.write("writ/process/COVERAGE.md", "# hand-edited\n")
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("is stale", err)

    def test_a_duplicate_slice_id_is_fatal(self):
        self.fx.write("writ/process/work-orders/003.md", work_order("SL-001", satisfies=["FR-ACC-03"]))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("is already used by", err)

    # -- parallel work ------------------------------------------------------------------------

    def test_two_active_slices_touching_one_surface_are_fatal_when_a_limit_is_set(self):
        config = dict(BASE_CONFIG, mode="team", wip_limit=4)
        self.fx.config(config)
        for name, sid, req in (("F1", "SL-001", "FR-ACC-01"), ("F2", "SL-002", "FR-ACC-02")):
            self.fx.write(
                "writ/process/work-orders/" + name + ".md",
                work_order(sid, satisfies=[req], status="in-progress", touches=["schema/accounts"]),
            )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("both touch schema/accounts", err)

    def test_the_wip_limit_is_enforced(self):
        self.fx.config(dict(BASE_CONFIG, mode="team", wip_limit=1))
        for name, sid, req in (("F1", "SL-001", "FR-ACC-01"), ("F2", "SL-002", "FR-ACC-02")):
            self.fx.write(
                "writ/process/work-orders/" + name + ".md",
                work_order(sid, satisfies=[req], status="in-progress"),
            )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("over the limit of 1", err)

    # -- the milestone and phase layout -------------------------------------------------------

    def test_a_work_order_under_a_milestone_and_phase_is_found(self):
        self.fx.write("writ/process/work-orders/m1/P01/001.md", work_order("SL-001", satisfies=["FR-ACC-01"]))
        os.remove(os.path.join(self.fx.root, "writ/process/work-orders/001.md"))
        self.green()
        self.assertIn("SL-001", self.fx.read("writ/process/SLICE-QUEUE.md"))

    def test_a_work_order_in_the_wrong_phase_directory_is_fatal(self):
        self.fx.write("writ/process/work-orders/m1/P02/001.md", work_order("SL-001", satisfies=["FR-ACC-01"]))
        os.remove(os.path.join(self.fx.root, "writ/process/work-orders/001.md"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("sits in phase directory P02 and declares phase P01", err)

    def test_a_summary_is_looked_for_beside_its_work_order(self):
        self.fx.write(
            "writ/process/work-orders/m1/P01/001.md",
            work_order("SL-001", satisfies=["FR-ACC-01"], status="done"),
        )
        os.remove(os.path.join(self.fx.root, "writ/process/work-orders/001.md"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("writ/process/slices/m1/P01/SL-001.md does not exist", err)
        self.fx.write("writ/process/slices/m1/P01/SL-001.md", "# Slice SL-001 - summary\n")
        self.green()

    def test_a_directory_readme_is_not_read_as_a_work_order(self):
        self.fx.write("writ/process/work-orders/README.md", "# Work orders\n\nProse, no front matter.\n")
        self.green()

    # -- the tracker --------------------------------------------------------------------------

    def test_a_claimed_slice_with_no_issue_is_fatal_once_the_tracker_is_on(self):
        self.fx.config(dict(BASE_CONFIG, tracker="github"))
        self.fx.write(
            "writ/process/work-orders/002.md",
            work_order("SL-002", satisfies=["FR-ACC-02"], status="in-progress"),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("names no issue", err)

    def test_a_queued_slice_needs_no_issue(self):
        """Planning sixty-four issues into a tracker nobody reads is how a tracker stops being
        read. SL-002 is queued and carries nothing, which is the case under test."""
        self.fx.config(dict(BASE_CONFIG, tracker="github"))
        self.green()

    def test_a_claimed_slice_naming_its_issue_is_accepted_and_linked_in_the_queue(self):
        self.fx.config(dict(BASE_CONFIG, tracker="github"))
        self.fx.write(
            "writ/process/work-orders/002.md",
            work_order("SL-002", satisfies=["FR-ACC-02"], status="in-progress", issue=71),
        )
        self.green()
        queue = self.fx.read("writ/process/SLICE-QUEUE.md")
        self.assertIn("| Issue |", queue)
        self.assertIn("| #71 |", queue)

    def test_a_slice_that_predates_the_tracker_says_so(self):
        self.fx.config(dict(BASE_CONFIG, tracker="github"))
        self.fx.write(
            "writ/process/work-orders/002.md",
            work_order("SL-002", satisfies=["FR-ACC-02"], status="in-progress", issue='"\u2014"'),
        )
        self.green()

    def test_an_issue_that_is_not_a_number_is_fatal(self):
        self.fx.config(dict(BASE_CONFIG, tracker="github"))
        self.fx.write(
            "writ/process/work-orders/002.md",
            work_order("SL-002", satisfies=["FR-ACC-02"], status="in-progress", issue="soon"),
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("neither a number nor", err)

    def test_without_a_tracker_a_claimed_slice_needs_no_issue_and_the_queue_has_no_column(self):
        self.fx.write(
            "writ/process/work-orders/002.md",
            work_order("SL-002", satisfies=["FR-ACC-02"], status="in-progress"),
        )
        self.green()
        self.assertNotIn("| Issue |", self.fx.read("writ/process/SLICE-QUEUE.md"))

    def test_the_queue_names_an_owner_in_team_mode(self):
        self.fx.config(dict(BASE_CONFIG, mode="team"))
        self.fx.write(
            "writ/process/work-orders/001.md",
            work_order("SL-001", satisfies=["FR-ACC-01"], owner="ada"),
        )
        self.green()
        self.assertIn("| Owner |", self.fx.read("writ/process/SLICE-QUEUE.md"))
        self.assertIn("| ada |", self.fx.read("writ/process/SLICE-QUEUE.md"))

    # -- deliberately not fatal ---------------------------------------------------------------

    def test_an_annotation_from_an_unregistered_family_is_reported_not_fatal(self):
        self.fx.write("src/other.test.ts", "it('[Process-4] holds', () => {});\n")
        self.green()
        coverage = self.fx.read("writ/process/COVERAGE.md")
        self.assertIn("## Annotations outside the registry", coverage)
        self.assertIn("| Process-4 |", coverage)

    def test_a_claim_from_an_unregistered_family_is_reported_not_fatal(self):
        self.fx.write(
            "writ/process/work-orders/002.md",
            work_order("SL-002", satisfies=["FR-ACC-02", "Process-4"]),
        )
        self.green()
        coverage = self.fx.read("writ/process/COVERAGE.md")
        self.assertIn("## Claims outside the registry", coverage)
        self.assertIn("| Process-4 | SL-002 |", coverage)

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
            "writ/process/work-orders/002.md",
            work_order(
                "SL-002",
                "## Demo\n\n### Script\n\n```bash\n# 1 - the first step\nmake test\n```\n\n"
                "## Out of scope\n\nNothing.\n",
                satisfies=["FR-ACC-02"],
            ),
        )
        self.green()

    # -- the requirement detail track -----------------------------------------------------------

    def detail_on(self, **over):
        """Turn the track on. Off by default, so every existing test stays a test of the loop."""
        spec = {"dir": "writ/spec/requirements", "families": ["FR", "INV"], "target_column": "Target"}
        spec.update(over)
        config = dict(BASE_CONFIG)
        config["requirements"] = spec
        self.fx.config(config)

    def detail(self, **kw):
        return detail_md(**kw)

    def file_detail(self, rel, text):
        self.fx.write("writ/spec/requirements/" + rel, text)

    def test_a_detail_file_that_quotes_the_requirement_verbatim_passes(self):
        self.detail_on()
        self.file_detail("FR-ACC/FR-ACC-01.md", self.detail())
        self.green()
        coverage = self.fx.read("writ/process/COVERAGE.md")
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
        self.file_detail("INV/INV-1.md", self.detail(ident="INV-1", area="INV", target="", quote="Every row carries a tenant."))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("belongs to no family the detail track covers", err)

    def test_an_invariant_whose_table_has_no_phase_column_is_not_phase_checked(self):
        self.detail_on()
        self.file_detail("INV/INV-1.md", self.detail(ident="INV-1", area="INV", target="M1", quote="Every row carries a tenant."))
        self.green()

    def test_a_phase_that_disagrees_with_the_specification_fails(self):
        self.detail_on()
        self.file_detail("FR-ACC/FR-ACC-01.md", self.detail(target="M2"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("says target M2 and the specification says M1", err)

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
        self.assertIn("| reviewed | 1 |", self.fx.read("writ/process/COVERAGE.md"))

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

    def test_a_detail_file_telling_no_story_fails(self):
        """The stories are the primary content, and the half that would quietly stop being
        written: every other section has a shape a drafter falls into, and a story does not."""
        self.detail_on()
        self.file_detail("FR-ACC/FR-ACC-01.md", self.detail(story=""))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("tells no story", err)

    def test_a_story_is_recognised_by_its_number_rather_than_its_words(self):
        """The heading is free-form after the number, and the matcher sees it normalised — so
        `## Story 4 — the walk-in` has no word boundary after `story` to anchor on."""
        self.detail_on()
        text = self.detail().replace("## Story 1 — a visitor signs up", "## Story 4 — the walk-in")
        self.file_detail("FR-ACC/FR-ACC-01.md", text)
        self.green()

    def test_a_requirement_whose_row_carries_emphasis_can_still_be_quoted_verbatim(self):
        """The cell arrives stripped of its markup. A blockquote that keeps the specification's own
        emphasis is verbatim, and the comparison has to say so."""
        self.detail_on()
        self.fx.write("writ/spec/BRD.md", BRD.replace("| FR-ACC-01 | Sign up. |", "| FR-ACC-01 | Sign up **now**. |"))
        self.file_detail("FR-ACC/FR-ACC-01.md", self.detail(quote="Sign up **now**."))
        self.green()

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
        coverage = self.fx.read("writ/process/COVERAGE.md")
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
        self.assertNotIn("## Requirement detail", self.fx.read("writ/process/COVERAGE.md"))

    def test_the_directory_readme_is_not_read_as_a_detail_file(self):
        self.detail_on()
        self.file_detail("README.md", "# Requirement detail\n\nProse, no front matter.\n")
        self.green()


    # -- one kind of thing per file -----------------------------------------------------------

    def test_an_identifier_outside_its_pattern_width_is_fatal(self):
        self.fx.write("writ/spec/BRD.md", BRD.replace("| FR-ACC-03 | Sign out. | M1 |", "| FR-ACC-3 | Sign out. | M1 |"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("FR-ACC-3 does not fit the FR pattern FR-AREA-NN", err)

    def test_a_suffix_letter_is_fatal(self):
        """A split mints two fresh numbers. `SL-003b` is how a numbering scheme starts lying."""
        self.fx.write("writ/spec/BRD.md", BRD.replace("| FR-ACC-03 | Sign out. | M1 |", "| FR-ACC-03b | Sign out. | M1 |"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("FR-ACC-03b does not fit", err)

    def withdrawn_brd(self):
        return BRD.replace(
            "| ID | Requirement | Target |\n|---|---|---|\n| FR-ACC-01 | Sign up. | M1 |\n| FR-ACC-02 | Sign in. | M1 |\n| FR-ACC-03 | Sign out. | M1 |",
            "| ID | Requirement | Target | Status |\n|---|---|---|---|\n| FR-ACC-01 | Sign up. | M1 | active |\n"
            "| FR-ACC-02 | Sign in. | M1 | active |\n| FR-ACC-03 | Sign out. | M1 | withdrawn |\n\nFR-ACC-03 was withdrawn; see the changelog.\n",
        )

    def test_a_withdrawn_requirement_leaves_the_ledger_and_can_still_be_cited(self):
        self.fx.write("writ/spec/BRD.md", self.withdrawn_brd())
        self.green()
        self.assertNotIn("| FR-ACC-03 |", self.fx.read("writ/process/COVERAGE.md"))
        self.assertIn("| FR-ACC-03 | `writ/spec/BRD.md` | withdrawn |", self.fx.read("writ/INDEX.md"))

    def test_a_detail_file_for_a_withdrawn_requirement_fails(self):
        self.fx.write("writ/spec/BRD.md", self.withdrawn_brd())
        self.detail_on()
        self.file_detail("FR-ACC/FR-ACC-03.md", self.detail(ident="FR-ACC-03", quote="Sign out."))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("FR-ACC-03 is not declared", err)

    def test_history_written_into_a_register_cell_is_fatal(self):
        for marker in ("Sign out. *(new — v3.0)*", "Sign out. **Amended 2026-09-02 (X-075)**", "~~Sign out.~~"):
            self.fx.write("writ/spec/BRD.md", BRD.replace("| FR-ACC-03 | Sign out. | M1 |", "| FR-ACC-03 | " + marker + " | M1 |"))
            code, err = self.fx.run("check")
            self.assertEqual(code, 1, marker)
            self.assertIn("FR-ACC-03 carries history inline", err)

    def since_brd(self, since):
        return BRD.replace(
            "| ID | Requirement | Target |\n|---|---|---|\n| FR-ACC-01 | Sign up. | M1 |",
            "| ID | Requirement | Target | Since |\n|---|---|---|---|\n| FR-ACC-01 | Sign up. | M1 | " + since + " |",
        ).replace("| FR-ACC-02 | Sign in. | M1 |", "| FR-ACC-02 | Sign in. | M1 | v1.0 |").replace(
            "| FR-ACC-03 | Sign out. | M1 |", "| FR-ACC-03 | Sign out. | M1 | v1.0 |")

    def test_a_since_that_names_nothing_is_fatal_and_a_version_or_amendment_passes(self):
        self.fx.write("writ/spec/BRD.md", self.since_brd("X-099"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("FR-ACC-01 says Since X-099, which is neither a version tag nor a declared amendment", err)
        self.fx.write("writ/spec/BRD.md", self.since_brd("v1.0"))
        self.green()
        self.fx.write("writ/spec/CHANGELOG.md", CHANGELOG + "| X-001 | 2026-09-10 | FR-ACC-01 | Reworded. | Review. | sam |\n")
        self.fx.write("writ/spec/BRD.md", self.since_brd("X-001"))
        self.green()

    def test_an_empty_since_is_fatal(self):
        self.fx.write("writ/spec/BRD.md", self.since_brd(""))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("FR-ACC-01 has an empty Since", err)

    def test_a_register_carries_exactly_one_id_table(self):
        self.fx.config(dict(BASE_CONFIG, registers=["writ/spec/BRD.md"]))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("a register carries exactly one `| ID |` table, and this carries 2", err)
        self.fx.config(dict(BASE_CONFIG, registers=["writ/spec/milestones.md"]))
        self.green()

    def test_a_narrative_declares_nothing(self):
        self.fx.config(dict(BASE_CONFIG, narrative=["writ/spec/BRD.md"]))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("a narrative document declares nothing, and this carries 2", err)
        self.fx.write("writ/spec/NOTES.md", "# Notes\n\nProse only.\n")
        self.fx.config(dict(BASE_CONFIG, narrative=["writ/spec/NOTES.md"]))
        self.green()

    def test_a_changelog_row_is_dated_touches_something_real_and_stays_a_line(self):
        self.fx.write("writ/spec/CHANGELOG.md", CHANGELOG + "| X-001 | yesterday | FR-ACC-01 | Reworded. | Review. | sam |\n")
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("X-001 has the date yesterday", err)
        self.fx.write("writ/spec/CHANGELOG.md", CHANGELOG + "| X-001 | 2026-09-10 | FR-ACC-77 | Reworded. | Review. | sam |\n")
        code, err = self.fx.run("check")
        self.assertIn("X-001 touches FR-ACC-77, which is not declared anywhere", err)
        self.fx.write("writ/spec/CHANGELOG.md", CHANGELOG + "| X-001 | 2026-09-10 | FR-ACC-01 | " + ("long " * 60) + " | Review. | sam |\n")
        code, err = self.fx.run("check")
        self.assertIn("X-001 Change is 299 characters, over the 240", err)
        self.fx.write("writ/spec/CHANGELOG.md", CHANGELOG + "| X-001 | 2026-09-10 | FR-ACC-01, v1.1 | Reworded. | Review, ADR-0001. | sam |\n")
        self.green()

    def test_the_agent_map_warns_over_its_budget_and_fails_over_its_ceiling(self):
        self.fx.config(dict(BASE_CONFIG, context_budget={"files": ["CLAUDE.md"], "warn_chars": 500, "max_chars": 900}))
        self.fx.write("CLAUDE.md", "# CLAUDE.md\n\n" + "A convention. " * 30)
        self.green()
        self.fx.write("CLAUDE.md", "# CLAUDE.md\n\n" + "A convention. " * 50)
        code, err = self.fx.run("check")
        self.assertEqual(code, 0, err)
        self.assertIn("warning: CLAUDE.md is 713 characters, over the 500", err)
        self.fx.write("CLAUDE.md", "# CLAUDE.md\n\n" + "A convention. " * 80)
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("over the ceiling of 900", err)
        self.assertNotIn("warning:", err)

    def test_a_budgeted_file_that_does_not_exist_and_a_budget_of_zero_are_both_silent(self):
        self.green()  # the default budget names CLAUDE.md, and this tree has none
        self.fx.config(dict(BASE_CONFIG, context_budget={"files": ["CLAUDE.md"], "warn_chars": 0, "max_chars": 0}))
        self.fx.write("CLAUDE.md", "A convention. " * 5000)
        code, err = self.fx.run("check")
        self.assertEqual(code, 0, err)
        self.assertEqual(err, "")

    def test_a_dangling_reference_in_prose_is_fatal_and_a_real_one_resolves(self):
        self.fx.write("writ/spec/BRD.md", BRD + "\nSee FR-ACC-77, and INV-1, and ADR-0001, and SL-001.\n")
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("writ/spec/BRD.md:", err)
        self.assertIn("FR-ACC-77 is not declared anywhere it could be", err)
        self.assertNotIn("INV-1 is not", err)
        self.assertNotIn("ADR-0001 is not", err)
        self.assertNotIn("SL-001 is not", err)
        self.fx.write("writ/spec/BRD.md", BRD + "\nSee INV-1, ADR-0001 and SL-001.\n")
        self.green()

    def test_an_example_identifier_inside_a_fence_or_a_blockquote_is_notation(self):
        self.fx.write("writ/spec/BRD.md", BRD + "\n```\nSatisfies: FR-ACC-77\n```\n\n> Cite it as FR-ACC-88.\n\nBut `FR-ACC-01` in prose is a reference.\n")
        self.green()

    def test_the_index_is_generated_and_byte_checked(self):
        self.green()
        index = self.fx.read("writ/INDEX.md")
        self.assertIn("## FR — requirement", index)
        self.assertIn("| FR-ACC-01 | `writ/spec/BRD.md` | active | ● | SL-001 |", index)
        self.assertIn("## SL — slice", index)
        self.assertIn("| SL-001 | `writ/process/work-orders/001.md` | P01 | queued | FR-ACC-01 |", index)
        self.fx.write("writ/INDEX.md", "# edited\n")
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("writ/INDEX.md is stale", err)

    def test_a_work_order_is_named_for_its_number(self):
        self.fx.write("writ/process/work-orders/F1.md", work_order("SL-001", satisfies=["FR-ACC-01"]))
        os.remove(os.path.join(self.fx.root, "writ/process/work-orders/001.md"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("is SL-001 and its file is not named 001.md", err)

    def test_an_unknown_phase_is_fatal(self):
        self.fx.write("writ/process/work-orders/002.md", work_order("SL-002", satisfies=["FR-ACC-02"], phase="P09"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("declares phase P09, which is not one of P01, P02", err)

    def test_the_queue_orders_by_phase_code_then_number(self):
        self.fx.write("writ/process/work-orders/002.md", work_order("SL-002", satisfies=["FR-ACC-02"], phase="P01"))
        self.fx.write("writ/process/work-orders/003.md", work_order("SL-003", satisfies=["FR-ACC-03"], phase="P02"))
        self.fx.write("writ/process/work-orders/001.md", work_order("SL-001", satisfies=["FR-ACC-01"], phase="P02"))
        self.green()
        queue = self.fx.read("writ/process/SLICE-QUEUE.md")
        self.assertLess(queue.index("**SL-002**"), queue.index("**SL-001**"))
        self.assertLess(queue.index("**SL-001**"), queue.index("**SL-003**"))

    # -- the size budget ------------------------------------------------------------------------

    def sized(self, **kw):
        """A work order with a Size section, which is where an L has to argue for itself."""
        body = "## Size\n\n**L — 900 code lines, 2100 in the diff.**\n\n## Demo\n\n```bash\nmake test\n```\n"
        return work_order("SL-001", body=kw.pop("body", body), satisfies=["FR-ACC-01"], **kw)

    def test_a_size_outside_the_configured_tiers_is_fatal(self):
        self.fx.write("writ/process/work-orders/001.md", self.sized(size="Medium"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("size is Medium, not one of S, M, L", err)

    def test_a_recorded_measurement_outside_the_declared_tier_is_fatal(self):
        """The queue shows the tier, so the tier is what has to be true. A slice that came in at
        420 lines is an L whatever anybody estimated, and `estimated:` is where the guess lives."""
        self.fx.write("writ/process/work-orders/001.md", self.sized(size="M", estimated=200, code_lines=420))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("declares size M and records 420 code lines, which is L", err)

    def test_an_estimate_that_missed_is_not_an_error(self):
        """Only the pair `size` and `code_lines` has to agree. A wrong estimate is the finding the
        recalibration is made of — failing the build on one would delete the evidence."""
        self.fx.write("writ/process/work-orders/001.md", self.sized(size="S", estimated=400, code_lines=90))
        self.green()

    def test_the_top_tier_states_why_it_could_not_be_split(self):
        self.fx.write("writ/process/work-orders/001.md", self.sized(size="L", code_lines=900))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("its Size section says only what it measured", err)

        body = ("## Size\n\n**L — 900 code lines, 2100 in the diff.**\n\nThe migration and its "
                "backfill cannot land apart: either half alone leaves the table unreadable.\n\n"
                "## Demo\n\n```bash\nmake test\n```\n")
        self.fx.write("writ/process/work-orders/001.md", self.sized(size="L", code_lines=900, body=body))
        self.green()

    def test_a_slice_that_has_not_closed_yet_is_measured_by_nothing(self):
        """`code_lines` arrives at close. Until then there is nothing to disbelieve."""
        self.fx.write("writ/process/work-orders/001.md", self.sized(size="S", estimated=120))
        self.green()

    def test_an_empty_object_in_the_config_replaces_rather_than_merges(self):
        """Merging `{}` would keep every default, which is the opposite of what writing it looks
        like. The trap sat under every dict-valued key until an off-switch was documented for one."""
        self.fx.config(dict(BASE_CONFIG, size_budget={}))
        self.assertEqual({}, ledger.load_config(self.fx.root, "scripts/ledger.config.json")["size_budget"])

    def test_an_empty_budget_turns_the_whole_check_off(self):
        self.fx.config(dict(BASE_CONFIG, size_budget={}))
        self.fx.write("writ/process/work-orders/001.md", self.sized(size="enormous", code_lines=9000))
        self.green()

    # -- stats ------------------------------------------------------------------------------

    def test_stats_reports_and_never_fails(self):
        """An instrument, not a gate. It is read at a phase gate and decides nothing, which is why
        it is allowed to look at things no check could hold anybody to."""
        self.fx.write("writ/process/work-orders/001.md", work_order(
            "SL-001", satisfies=["FR-ACC-01"], status="done", size="S", estimated=90, code_lines=94))
        self.fx.write("writ/process/slices/SL-001.md", "# SL-001\n")
        self.fx.write("writ/process/work-orders/002.md", work_order(
            "SL-002", satisfies=["FR-ACC-02"], status="done", size="M", estimated=140, code_lines=287,
            body="## Size\n\n**M**\n\n## Demo\n\n```bash\nmake test\n```\n"))
        self.fx.write("writ/process/slices/SL-002.md", "# SL-002\n")
        self.fx.write("writ/maintenance/security-backlog.md",
                      "# Security backlog\n\n## Open\n\n| ID | Finding |\n|---|---|\n| SEC-01 | A thing. |\n")
        self.fx.config(dict(BASE_CONFIG, maintenance="writ/maintenance"))

        code, err = self.fx.run("stats")
        self.assertEqual(code, 0, err)
        # `stats` writes to stdout, so read it back off the tool rather than the run helper.
        config = ledger.load_config(self.fx.root, "scripts/ledger.config.json")
        data = ledger.collect(self.fx.root, config)
        sections, counts, _unknown, _unreg, _unclaim = ledger.build_ledger(data)
        report = ledger.render_stats(self.fx.root, config, data, sections, counts)

        self.assertIn("2 slices: 2 done", report)
        self.assertIn("estimate held its tier in 1 of 2", report)   # SL-002 was estimated an S
        self.assertIn("security-backlog.md", report)
        self.assertIn("1 open", report)

    def test_stats_survives_a_project_with_nothing_in_it_yet(self):
        """Slice zero runs it before there is anything to report, and a traceback there would be
        the first thing a new project saw the tool do."""
        code, err = self.fx.run("stats")
        self.assertEqual(code, 0, err)

    # -- graph ------------------------------------------------------------------------------

    def graph(self):
        """The graph, parsed. Like `stats` it writes to stdout, so read it off the tool."""
        config = ledger.load_config(self.fx.root, "scripts/ledger.config.json")
        data = ledger.collect(self.fx.root, config)
        sections, counts, _unknown, _unreg, _unclaim = ledger.build_ledger(data)
        return json.loads(ledger.render_graph(config, data, sections, counts))

    def test_the_graph_carries_every_state_the_ledger_can_report(self):
        """The point of a machine-readable export is that nothing has to be re-derived from the
        rendered table. If a consumer has to parse the bullet marks back out of Markdown to learn
        what is satisfied, the export has failed."""
        self.fx.write("writ/process/work-orders/001.md", work_order(
            "SL-001", satisfies=["FR-ACC-01", "FR-ACC-02"], status="done", size="S",
            estimated=90, code_lines=94))
        self.fx.write("writ/process/slices/SL-001.md", "# SL-001\n")
        self.fx.write("src/a.test.ts", 'it("[FR-ACC-01] does the thing", () => {});\n')
        self.fx.write("src/b.test.ts", 'it("[FR-ACC-03] signs a person out", () => {});\n')

        code, err = self.fx.run("graph")
        self.assertEqual(code, 0, err)
        graph = self.graph()

        states = {r["id"]: r["state"] for r in graph["requirements"]}
        self.assertEqual(states["FR-ACC-01"], "satisfied")   # claimed and proven
        self.assertEqual(states["FR-ACC-02"], "partial")     # claimed, nothing proves it
        self.assertEqual(states["FR-ACC-03"], "inherited")   # proven, never claimed

        by_id = {r["id"]: r for r in graph["requirements"]}
        self.assertEqual(by_id["FR-ACC-01"]["claimed_by"], ["SL-001"])
        self.assertTrue(by_id["FR-ACC-01"]["proven_by"])
        # The distinction the ledger makes in prose, carried rather than left to be guessed at.
        self.assertTrue(by_id["FR-ACC-02"]["claimed_without_proof"])
        self.assertFalse(by_id["FR-ACC-03"]["claimed_without_proof"])

        self.assertEqual(graph["counts"]["total"], sum(
            graph["counts"][s] for s in ("satisfied", "inherited", "partial", "none")))

    def test_the_graph_agrees_with_the_ledger_it_was_built_beside(self):
        """Two renderers over one build. If they can disagree, one of them is a second source of
        truth about coverage, which is the thing this tool exists to prevent."""
        self.fx.write("writ/process/work-orders/001.md", work_order(
            "SL-001", satisfies=["FR-ACC-01"], status="done", size="S", estimated=90, code_lines=94))
        self.fx.write("writ/process/slices/SL-001.md", "# SL-001\n")
        self.fx.write("src/a.test.ts", 'it("[FR-ACC-01] does the thing", () => {});\n')

        config = ledger.load_config(self.fx.root, "scripts/ledger.config.json")
        data = ledger.collect(self.fx.root, config)
        sections, counts, _u, _n, _c = ledger.build_ledger(data)
        graph = json.loads(ledger.render_graph(config, data, sections, counts))

        for state in ("satisfied", "inherited", "partial", "none"):
            self.assertEqual(graph["counts"][state], counts[state], state)
        self.assertEqual(
            len(graph["requirements"]),
            sum(len(rows) for _fam, rows in sections))

    def test_the_graph_never_fails_and_writes_nothing(self):
        """Same contract as stats. A project with nothing in it yet still gets valid JSON, and a
        broken tree does not turn an instrument into a gate."""
        code, err = self.fx.run("graph")
        self.assertEqual(code, 0, err)
        graph = self.graph()
        self.assertEqual(graph["version"], 1)
        self.assertEqual(graph["counts"]["total"], sum(
            graph["counts"][s] for s in ("satisfied", "inherited", "partial", "none")))

        # An identifier claimed by a work order that does not exist is an error for `check` and
        # merely a fact for `graph`.
        self.fx.write("writ/process/work-orders/009.md", work_order("SL-009", satisfies=["FR-NOPE-99"]))
        code, err = self.fx.run("graph")
        self.assertEqual(code, 0, err)

    # -- change requests ----------------------------------------------------------------------

    def cr_on(self):
        self.fx.config(dict(BASE_CONFIG, changes={"dir": "writ/spec/changes", "family": "CR"}))

    def test_an_accepted_change_request_is_applied_and_reads_so_in_the_index(self):
        self.cr_on()
        self.fx.write("writ/spec/changes/CR-001-sign-out-twice.md", change_request())
        self.fx.write("writ/spec/BRD.md", self.since_brd("v1.0").replace(
            "| FR-ACC-03 | Sign out. | M1 | v1.0 |", "| FR-ACC-03 | Sign out. | M1 | v1.0 |\n| FR-ACC-04 | Sign out twice. | M2 | CR-001 |"))
        self.green()
        index = self.fx.read("writ/INDEX.md")
        self.assertIn("## CR — change request", index)
        self.assertIn("| CR-001 | `writ/spec/changes/CR-001-sign-out-twice.md` | accepted | M2 | yes | no |", index)

    def test_an_accepted_change_request_that_was_not_applied_is_fatal(self):
        self.cr_on()
        self.fx.write("writ/spec/changes/CR-001-sign-out-twice.md", change_request())
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("CR-001-sign-out-twice.md: is accepted and FR-ACC-04 is not in its register", err)

    def test_a_change_applied_before_acceptance_is_fatal(self):
        self.cr_on()
        self.fx.write("writ/spec/changes/CR-001-sign-out-twice.md", change_request(status="draft", approved_by='""'))
        self.fx.write("writ/spec/BRD.md", self.since_brd("v1.0").replace(
            "| FR-ACC-03 | Sign out. | M1 | v1.0 |", "| FR-ACC-03 | Sign out. | M1 | v1.0 |\n| FR-ACC-04 | Sign out twice. | M2 | CR-001 |"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("is draft and FR-ACC-04 already says Since CR-001 — applied before it was accepted", err)

    def test_a_decided_change_request_names_who_decided_and_when(self):
        self.cr_on()
        self.fx.write("writ/spec/changes/CR-001-sign-out-twice.md", change_request(approved_by='""', decided_on='""'))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("is accepted and names nobody who decided it", err)
        self.assertIn("is accepted and decided_on is not a date", err)

    def test_a_change_request_targets_a_declared_milestone_and_uses_the_three_ops(self):
        self.cr_on()
        self.fx.write("writ/spec/changes/CR-001-sign-out-twice.md", change_request(target="M9"))
        code, err = self.fx.run("check")
        self.assertIn("targets M9, which is not a declared milestone", err)
        self.fx.write("writ/spec/changes/CR-001-sign-out-twice.md", change_request().replace("| add | FR-ACC-04", "| tweak | FR-ACC-04"))
        code, err = self.fx.run("check")
        self.assertIn("has the op tweak, not one of add, amend, withdraw", err)

    def test_a_draft_request_may_name_the_row_it_is_asking_for(self):
        """`add` names a row that does not exist yet — that is the whole point of raising one.

        The reference scan resolves every identifier-shaped token in prose, and a change request's
        *Changes* table is prose to it, so a draft request proposing a new requirement failed the
        check for the identifier it was asking for. Nobody could ever be shown a green pull
        request to decide on, which is the one thing the track is for."""
        self.cr_on()
        self.fx.write("writ/spec/changes/CR-001-sign-out-twice.md", change_request(status="draft", approved_by='""'))
        self.green()

    def test_an_accepted_withdrawal_needs_the_row_retired(self):
        self.cr_on()
        self.fx.write("writ/spec/changes/CR-001-sign-out-twice.md", change_request().replace(
            "| add | FR-ACC-04 | Sign out twice. | M2 |", "| withdraw | FR-ACC-03 | — | — |"))
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("is accepted and FR-ACC-03 is not withdrawn in its register", err)
        self.fx.write("writ/spec/BRD.md", self.withdrawn_brd())
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
            "---\nid: SL-001\nstatus: queued          # queued | in-progress | done\n"
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
            "writ/process/work-orders/002.md",
            work_order("SL-002", satisfies=["FR-ACC-02"]).replace(
                "status: queued", "status: queued          # queued | in-progress | done"
            ),
        )
        self.green()
        self.assertIn("| **SL-002** | P01 | S | — | queued |", self.fx.read("writ/process/SLICE-QUEUE.md"))

    def test_front_matter_reads_inline_and_block_lists(self):
        data, body = ledger.parse_front_matter(
            "---\nid: SL-001\nsatisfies: [FR-A-01, FR-A-02]\npartial:\n  - INV-1\n---\nbody\n"
        )
        self.assertEqual(data["id"], "SL-001")
        self.assertEqual(data["satisfies"], ["FR-A-01", "FR-A-02"])
        self.assertEqual(data["partial"], ["INV-1"])
        self.assertEqual(body.strip(), "body")


# -- the manual test scenario track -------------------------------------------------------------

    # -- standing citations and open work orders ----------------------------------------------

    def test_a_cited_path_that_is_not_there_is_fatal_and_one_that_is_passes(self):
        self.fx.config(dict(BASE_CONFIG, path_scan={"include": ["writ/**/*.md"], "allow": ["dist/app.js"]}))
        self.fx.write(
            "writ/spec/glossary.md",
            "See `writ/spec/BRD.md`, `writ/spec/gone.md`, `dist/app.js`, `spec/relative.md` and `src/`.\n",
        )
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("writ/spec/glossary.md:1: writ/spec/gone.md is cited and is not there", err)
        for quiet in ("writ/spec/BRD.md is", "dist/app.js", "spec/relative.md", "src/ is"):
            self.assertNotIn(quiet, err)

    def test_path_scan_is_off_until_it_names_something(self):
        self.fx.write("writ/spec/glossary.md", "See `writ/spec/gone.md`.\n")
        self.green()

    CRITERIA = "## Acceptance criteria\n\n1. [FR-ACC-02] signs in\n2. {second}\n\n## Demo\n\n```bash\nmake test\n```\n"

    def test_an_open_slice_criterion_naming_nothing_or_an_unclaimed_id_is_fatal(self):
        for second, message in (
            ("rejects a bad password", "acceptance criterion `2. rejects a bad password` names no identifier"),
            ("[FR-ACC-01] rejects a bad password", "names FR-ACC-01, which the front matter does not claim"),
        ):
            with self.subTest(second=second):
                self.fx.write(
                    "writ/process/work-orders/002.md",
                    work_order("SL-002", body=self.CRITERIA.format(second=second), satisfies=["FR-ACC-02"],
                               depends_on=["SL-001"], status="in-progress"),
                )
                code, err = self.fx.run("check")
                self.assertEqual(code, 1)
                self.assertIn(message, err)

    def test_a_queued_slice_and_an_empty_template_slot_are_not_read_as_criteria(self):
        self.fx.write(
            "writ/process/work-orders/002.md",
            work_order("SL-002", body=self.CRITERIA.format(second="rejects a bad password"),
                       satisfies=["FR-ACC-02"], depends_on=["SL-001"]),
        )
        self.assertEqual(ledger.criteria("> guidance\n\n1.\n2.\n"), [])
        code, err = self.fx.run("all")
        self.assertNotIn("acceptance criterion", err)

    def test_a_budget_message_names_the_largest_sections(self):
        self.fx.config(dict(BASE_CONFIG, context_budget={"files": ["CLAUDE.md"], "warn_chars": 100, "max_chars": 0}))
        self.fx.write("CLAUDE.md", "# Map\n\n## Small\n\nx\n\n## Big\n\n" + "y" * 400 + "\n\n## Middle\n\n" + "z" * 50 + "\n")
        code, err = self.fx.run("check")
        self.assertIn("Largest sections: Big (", err)
        self.assertLess(err.index("Big ("), err.index("Middle ("))

    def test_annotations_names_the_test_files_behind_each_identifier(self):
        self.fx.write("src/more.test.ts", "it('[FR-ACC-01] again', () => {});\nit('[FR-ACC-02] other', () => {});\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = ledger.main(["annotations", "FR-ACC-01", "--root", self.fx.root])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out.getvalue()), {"FR-ACC-01": ["src/accounts.test.ts", "src/more.test.ts"]})

    # -- decision records ----------------------------------------------------------------------

    def test_the_index_lists_each_decision_with_what_it_constrains(self):
        self.green()
        self.assertIn("| ADR-0001 | A thing is decided | INV-1 | active | `writ/decisions/0001-a-thing.md` |", self.fx.read("writ/INDEX.md"))

    def test_a_decision_constraining_nothing_is_fatal(self):
        self.fx.write("writ/decisions/0001-a-thing.md", "# ADR-0001 — A thing\n")
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("0001-a-thing.md: names nothing it constrains", err)

    def test_two_records_with_one_number_are_fatal(self):
        self.fx.write("writ/decisions/0001-another-thing.md", ADR)
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("ADR-0001 is two files", err)

    def test_a_record_whose_name_no_audit_can_read_is_fatal(self):
        self.fx.write("writ/decisions/12-Bad-Name.md", ADR)
        code, err = self.fx.run("check")
        self.assertEqual(code, 1)
        self.assertIn("12-Bad-Name.md: not `NNNN-kebab-slug.md`", err)


SCENARIO_SECTIONS_MD = """
## The requirement

> Sign up.

## Before you start

| What is needed | Who provides it |
|---|---|
| An account that may sign somebody up | The test manager |

**Not through the screen:** None.

## Scenarios

### S1 — somebody signs up

**Covers** story 1 · **Type** happy path · **Where** the sign-up page · **Ready** yes

**Given** nobody holds the address

1. Sign up with an address nobody holds.

**Expect** the account exists and can sign in.

### S2 — an address already taken

**Covers** story 1 · **Type** negative · **Where** the sign-up page · **Ready** yes

**Given** somebody already holds the address

1. Try to sign up with it again.

**Expect** refused, naming the address, and no second account.

## Not testable yet

None — all of it can be run today.

## Related

`FR-ACC-01`.

## Runs

| Date | Build | Result | By | Notes |
|---|---|---|---|---|
"""


def scenarios_md(ident="FR-ACC-01", body=None, **kw):
    front = {
        "id": ident,
        "area": ident.rsplit("-", 1)[0],
        "status": "draft",
        "written_by": "kim",
        "approved_by": '""',
        "detail_status": "draft",
        "detail_read_on": "2026-09-10",
        "areas": "[sign-up]",
    }
    front.update(kw)
    lines = ["---"] + [k + ": " + str(v) for k, v in front.items()] + ["---", "", "# " + ident, ""]
    return "\n".join(lines) + (SCENARIO_SECTIONS_MD if body is None else body)


def reconciled(text, *rows):
    """A detail file with a *Reconciliation* table carrying `rows`, each a tuple of the six cells."""
    table = ["## Reconciliation", "", "| Date | Against | Conflict | Decision | Where | By |", "|---|---|---|---|---|---|"]
    table += ["| " + " | ".join(row) + " |" for row in rows]
    return text.replace("## Verification\n", "\n".join(table) + "\n\n## Verification\n")


QUESTIONS = """# Open questions

| ID | Question | Touches | Owner | Status |
|---|---|---|---|---|
| Q-001 | Does a second sign-up merge the accounts? | FR-ACC-01 | dana | open |
"""


class OutOfOrderTest(unittest.TestCase):
    """Work that arrived out of order: built ahead of its detail, built against an older reading, a
    closed milestone that is not caught up. Found by the check and settled by a decision recorded in
    the detail file — `requirements.out_of_order` says how loudly each finding speaks."""

    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.close)
        self.mode("fail")

    def mode(self, mode, **over):
        spec = {"dir": "writ/spec/requirements", "families": ["FR", "INV"], "target_column": "Target"}
        if mode is not None:
            spec["out_of_order"] = mode
        spec.update(over)
        self.fx.config(dict(BASE_CONFIG, requirements=spec))

    def order(self, number, status, satisfies=("FR-ACC-01",), **kw):
        slice_id = "SL-" + number
        self.fx.write(
            "writ/process/work-orders/" + number + ".md",
            work_order(slice_id, satisfies=list(satisfies), status=status, **kw),
        )
        if status == "done":
            self.fx.write("writ/process/slices/" + slice_id + ".md", "# " + slice_id + "\n")

    def detail(self, text=None, **kw):
        self.fx.write("writ/spec/requirements/FR-ACC/FR-ACC-01.md", text if text is not None else detail_md(**kw))

    def check(self):
        self.fx.run("all")
        return self.fx.run("check")

    def assert_fails(self, fragment):
        code, err = self.check()
        self.assertEqual(code, 1, "expected a failure mentioning " + fragment + ", got none")
        self.assertIn("error: ", err)
        self.assertIn(fragment, [line for line in err.split("\n") if line.startswith("error: ") and fragment in line][0])

    def assert_warns(self, fragment):
        code, err = self.check()
        self.assertEqual(code, 0, err)
        self.assertIn("warning: ", err)
        self.assertTrue([line for line in err.split("\n") if line.startswith("warning: ") and fragment in line], err)

    def coverage(self):
        self.fx.run("all")
        return self.fx.read("writ/process/COVERAGE.md")

    # -- the claim gate, under `fail` -----------------------------------------------------------

    def test_a_slice_claimed_for_an_undetailed_requirement_fails(self):
        """The cheapest moment to catch it: before any code exists to describe instead."""
        self.order("001", "in-progress", detail_read_on="2026-09-10")
        self.assert_fails("SL-001 claims FR-ACC-01, which has no detail file")

    def test_a_draft_detail_file_is_enough_to_claim_it(self):
        """The drafter is on the critical path when the track falls behind — never the approver."""
        self.detail()
        self.order("001", "in-progress", detail_read_on="2026-09-10")
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_a_queued_slice_is_a_plan_and_is_not_gated(self):
        self.order("001", "queued")
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_a_slice_building_something_outside_the_covered_families_is_not_gated(self):
        self.mode("fail", families=["INV"])
        self.order("001", "in-progress", detail_read_on="2026-09-10")
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_a_slice_that_records_no_reading_fails(self):
        self.detail()
        self.order("001", "in-progress")
        self.assert_fails("SL-001 is in-progress and records no detail_read_on")

    def test_a_reading_that_is_not_a_date_fails_in_every_mode(self):
        self.mode("report")
        self.detail()
        self.order("001", "in-progress", detail_read_on="last-tuesday")
        self.assert_fails("detail_read_on is last-tuesday, which is not a date")

    # -- built against an older reading ---------------------------------------------------------

    def test_a_detail_file_revised_after_the_slice_read_it_fails(self):
        self.detail(revised_on="2026-09-12")
        self.order("001", "done", detail_read_on="2026-09-10")
        self.assert_fails("SL-001 was built against the reading of 2026-09-10")

    def test_a_reconciliation_row_dated_after_the_revision_settles_it(self):
        text = reconciled(detail_md(revised_on="2026-09-12"), ("2026-09-12", "SL-001", "—", "holds", "—", "sam"))
        self.detail(text)
        self.order("001", "done", detail_read_on="2026-09-10")
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_a_row_is_against_the_slice_its_cell_names(self):
        text = reconciled(detail_md(revised_on="2026-09-12"), ("2026-09-12", "SL-001 (done)", "—", "holds", "—", "sam"))
        self.detail(text)
        self.order("001", "done", detail_read_on="2026-09-10")
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_a_reading_written_as_a_dash_is_no_reading(self):
        """The front matter's other blanks mean *none* here too, not a date that failed to parse."""
        self.detail()
        self.order("001", "in-progress", detail_read_on="—")
        self.assert_fails("SL-001 is in-progress and records no detail_read_on")

    def test_a_reconciliation_row_older_than_the_revision_does_not(self):
        """The file changed again after somebody said the build held — so nobody has said it yet."""
        text = reconciled(detail_md(revised_on="2026-09-20"), ("2026-09-12", "SL-001", "—", "holds", "—", "sam"))
        self.detail(text)
        self.order("001", "done", detail_read_on="2026-09-10")
        self.assert_fails("SL-001 was built against the reading of 2026-09-10")

    def test_a_slice_that_read_the_current_file_needs_no_row(self):
        self.detail(revised_on="2026-09-10")
        self.order("001", "done", detail_read_on="2026-09-10")
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_a_slice_still_building_is_told_to_re_read_rather_than_reconcile(self):
        """Its work order is still live, so the cheap remedy is its own: read again, re-date."""
        self.detail(revised_on="2026-09-12")
        self.order("001", "in-progress", detail_read_on="2026-09-10")
        self.assert_fails("re-read it and re-date detail_read_on")

    def test_a_finished_slice_from_before_readings_were_recorded_warns_and_never_fails(self):
        """Not new drift, and not knowable as drift: listed until a row settles it."""
        self.detail(status="reviewed", approved_by="dana")
        self.order("001", "done")
        self.assert_warns("SL-001 recorded no reading of it")
        self.assertIn("| FR-ACC-01 | SL-001 | not recorded | 2026-09-01 |", self.coverage())

    def test_under_backfill_a_draft_being_backfilled_warns(self):
        self.mode("backfill")
        self.detail(revised_on="2026-09-12")
        self.order("001", "done", detail_read_on="2026-09-10")
        self.assert_warns("SL-001 was built against the reading of 2026-09-10")

    def test_under_backfill_a_reviewed_requirement_is_locked(self):
        """Backfilling is allowed to lag. A requirement it has caught up with may not slip again."""
        self.mode("backfill")
        self.detail(revised_on="2026-09-12", status="reviewed", approved_by="dana")
        self.order("001", "done", detail_read_on="2026-09-10")
        self.assert_fails("SL-001 was built against the reading of 2026-09-10")

    # -- the reconciliation rows ----------------------------------------------------------------

    def row(self, *cells, **kw):
        self.detail(reconciled(detail_md(**kw), cells))
        self.order("001", "done", detail_read_on="2026-09-01")

    def test_a_decision_outside_the_vocabulary_fails(self):
        self.row("2026-09-01", "SL-001", "sign-up is by invitation", "probably fine", "—", "sam")
        self.assert_fails("decides probably fine, not one of holds, ratified, fix, change-request, open")

    def test_a_row_nobody_decided_fails(self):
        self.row("2026-09-01", "SL-001", "sign-up is by invitation", "ratified", "—", "—")
        self.assert_fails("names nobody who decided it")

    def test_a_fix_names_the_slice_that_makes_it(self):
        self.row("2026-09-01", "SL-001", "a second sign-up is not refused", "fix", "the next slice", "dana")
        self.assert_fails("is a fix and names no slice")

    def test_a_fix_naming_a_queued_slice_passes(self):
        self.order("002", "queued", satisfies=("FR-ACC-02",))
        self.detail(reconciled(detail_md(), ("2026-09-01", "SL-001", "a second sign-up is not refused", "fix", "SL-002", "dana")))
        self.order("001", "done", detail_read_on="2026-09-01")
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_a_change_request_decision_cites_the_request(self):
        self.row("2026-09-01", "SL-001", "the requirement is wrong", "change-request", "—", "dana")
        self.assert_fails("needs a change request and names none")

    def test_an_open_row_on_a_draft_is_a_real_answer(self):
        self.row("2026-09-01", "SL-001", "invitation or open sign-up", "open", "—", "sam")
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_an_open_row_on_a_reviewed_file_names_its_question(self):
        self.row("2026-09-01", "SL-001", "invitation or open sign-up", "open", "—", "sam", status="reviewed", approved_by="dana")
        self.assert_fails("is still open on a reviewed file and names no registered question")

    def test_an_open_row_citing_a_registered_question_may_be_reviewed(self):
        self.fx.write("writ/spec/questions.md", QUESTIONS)
        self.row("2026-09-01", "SL-001", "invitation or open sign-up", "open", "Q-001", "sam", status="reviewed", approved_by="dana")
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_a_malformed_row_fails_even_under_report(self):
        """A vocabulary, not prose — whatever the mode. `report` quiets drift, not a broken file."""
        self.mode("report")
        self.row("yesterday", "SL-001", "—", "holds", "—", "sam")
        self.assert_fails("has the date yesterday, which is not YYYY-MM-DD")

    # -- built ahead: the backfill queue ------------------------------------------------------

    def test_under_backfill_building_ahead_is_a_queue_not_a_failure(self):
        self.mode("backfill")
        self.order("001", "done")
        self.assert_warns("1 requirement is built ahead of a detail file")
        coverage = self.coverage()
        self.assertIn("### Built ahead of its detail", coverage)
        self.assertIn("| FR-ACC-01 | M1 | SL-001 | — | M1 is active |", coverage)
        # Listed once, in the queue, rather than in the older backlog as well.
        self.assertNotIn("| FR-ACC-01 | none |", coverage)

    def test_inherited_behaviour_is_built_ahead_too(self):
        """Tests older than the process pin behaviour nobody has said is wanted."""
        self.mode("backfill")
        self.fx.write("writ/process/work-orders/001.md", work_order("SL-001", satisfies=["FR-ACC-03"]))
        self.assertIn("| FR-ACC-01 | M1 | tests (≈) |", self.coverage())

    def test_the_queue_puts_what_a_later_slice_builds_on_first(self):
        self.mode("backfill")
        self.fx.write("writ/process/work-orders/001.md", work_order(
            "SL-001", satisfies=["FR-ACC-03"], partial=["FR-ACC-02", "INV-1"], status="done"))
        self.fx.write("writ/process/slices/SL-001.md", "# SL-001\n")
        self.fx.write("writ/process/work-orders/002.md", work_order("SL-002", satisfies=["FR-ACC-02"]))
        coverage = self.coverage()
        queue = coverage[coverage.index("### Built ahead of its detail"):]
        self.assertIn("| FR-ACC-02 | M1 | SL-001 | SL-002 | SL-002 builds on it; M1 is active |", queue)
        order = [queue.index("| " + i + " |") for i in ("FR-ACC-02", "INV-1", "FR-ACC-03")]
        self.assertEqual(order, sorted(order), queue)

    def test_under_fail_a_finished_slice_built_ahead_fails(self):
        self.order("001", "done", detail_read_on="2026-09-10")
        self.assert_fails("SL-001 claims FR-ACC-01, which has no detail file")

    # -- the milestone gate ---------------------------------------------------------------------

    def close_m1(self):
        self.fx.write("writ/spec/milestones.md", MILESTONES.replace("| active |", "| done |"))

    def test_a_closed_milestone_with_a_requirement_still_undetailed_fails(self):
        self.mode("backfill")
        self.close_m1()
        self.order("001", "done")
        self.assert_fails("M1 is closed and FR-ACC-01, aimed at it and built, has no detail file")

    def test_a_closed_milestone_wants_the_detail_reviewed(self):
        self.mode("backfill")
        self.close_m1()
        self.detail()
        self.order("001", "done", detail_read_on="2026-09-01")
        self.assert_fails("has a detail file nobody has reviewed")

    def test_a_closed_milestone_that_caught_up_passes(self):
        self.mode("backfill")
        self.close_m1()
        self.detail(status="reviewed", approved_by="dana")
        self.order("001", "done", detail_read_on="2026-09-01")
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_an_active_milestone_is_not_gated(self):
        self.mode("backfill")
        self.order("001", "done")
        code, err = self.check()
        self.assertEqual(code, 0, err)

    # -- the modes ------------------------------------------------------------------------------

    def test_report_fails_nothing_it_finds(self):
        self.mode("report")
        self.close_m1()
        self.detail(revised_on="2026-09-12", status="reviewed", approved_by="dana")
        self.order("001", "done", detail_read_on="2026-09-10")
        self.order("002", "in-progress", satisfies=("FR-ACC-02",))
        code, err = self.check()
        self.assertEqual(code, 0, err)
        for fragment in ("built against the reading", "records no detail_read_on", "M1 is closed"):
            self.assertIn(fragment, err)

    def test_an_unset_mode_is_report(self):
        """A project that updates the tool without choosing is not failed by the choice."""
        self.mode(None)
        self.order("001", "in-progress")
        self.assert_warns("SL-001 is in-progress and records no detail_read_on")

    def test_a_mode_outside_the_three_fails(self):
        self.mode("strict")
        self.assert_fails("requirements.out_of_order is strict, not one of fail, backfill, report")

    def test_the_track_switched_off_is_silent(self):
        self.fx.config(BASE_CONFIG)
        self.order("001", "in-progress")
        code, err = self.check()
        self.assertEqual(code, 0, err)
        self.assertNotIn("Built ahead", self.coverage())

    def test_stats_reports_the_backfill(self):
        self.mode("backfill")
        self.order("001", "done")
        config = ledger.load_config(self.fx.root, "scripts/ledger.config.json")
        data = ledger.collect(self.fx.root, config)
        sections, counts, _unknown, _unreg, _unclaim = ledger.build_ledger(data)
        report = ledger.render_stats(self.fx.root, config, data, sections, counts)
        self.assertIn("Backfill — out_of_order: backfill", report)
        self.assertIn("1 requirements with no detail file · 1 aimed at M1, the active milestone", report)


class ScenarioTrackTest(unittest.TestCase):
    """One file per requirement, and every way one can be unrunnable by the person it was written
    for. Both tracks are on: the scenarios are written from the detail files."""

    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.close)
        config = dict(BASE_CONFIG)
        config["requirements"] = {
            "dir": "writ/spec/requirements",
            "families": ["FR", "INV"],
            "target_column": "Target",
            "require_detail_for_satisfied": False,
        }
        config["scenarios"] = {
            "dir": "writ/qa/scenarios",
            "families": ["FR", "INV"],
            "commands": ["acme"],
            "require_scenarios_for_reviewed_detail": False,
        }
        self.fx.config(config)
        self.fx.write("writ/spec/requirements/FR-ACC/FR-ACC-01.md", detail_md())
        self.fx.write("writ/qa/scenarios/FR-ACC/FR-ACC-01.md", scenarios_md())

    def check(self):
        # Written first, then verified: a stale generated artefact would otherwise mask the error
        self.fx.run("all")
        return self.fx.run("check")

    def assert_fails(self, fragment):
        code, err = self.check()
        self.assertEqual(code, 1, "expected a failure mentioning " + fragment + ", got none")
        self.assertIn(fragment, err)

    def write(self, body=None, **kw):
        self.fx.write("writ/qa/scenarios/FR-ACC/FR-ACC-01.md", scenarios_md(body=body, **kw))

    def test_a_green_scenario_file_passes_and_is_counted(self):
        code, err = self.check()
        self.assertEqual(code, 0, err)
        coverage = self.fx.read("writ/process/COVERAGE.md")
        self.assertIn("## Manual test scenarios", coverage)
        self.assertIn("| **total** | **1** |", coverage)

    def test_a_scenario_asking_the_tester_to_run_the_project_s_own_tool_fails(self):
        # The whole point of the track: whoever runs these has a browser and no terminal, so a
        # scenario carrying a command is one nobody on the test team can run. The tool is known
        # by name, from `scenarios.commands`.
        self.write(body=SCENARIO_SECTIONS_MD.replace(
            "1. Sign up with an address nobody holds.",
            "1. Run `acme org create --slug demo` and then sign up.",
        ))
        self.assert_fails("a scenario is done through the product's own screens")

    def test_a_shell_prompt_on_a_later_line_of_a_scenario_fails(self):
        # The prompt is anchored to a line rather than to the block, which is not the same thing:
        # a command is never the first thing in a scenario, so an unanchored pattern would have
        # caught nothing at all.
        self.write(body=SCENARIO_SECTIONS_MD.replace(
            "**Expect** the account exists and can sign in.",
            "2. Seed the address first:\n\n```\n$ seed --address nobody@example.test\n```\n\n"
            "**Expect** the account exists and can sign in.",
        ))
        self.assert_fails("a scenario is done through the product's own screens")

    def test_a_project_tool_that_is_not_named_in_the_config_is_not_caught(self):
        # The generic shapes are deliberately few, so the project's own tool has to be named.
        config = json.loads(self.fx.read("scripts/ledger.config.json"))
        config["scenarios"]["commands"] = []
        self.fx.config(config)
        self.write(body=SCENARIO_SECTIONS_MD.replace(
            "1. Sign up with an address nobody holds.",
            "1. Run `acme org create --slug demo` and then sign up.",
        ))
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_setup_a_scenario_says_is_not_through_the_screen_is_allowed(self):
        # The escape hatch, and it has to exist: some of a product is a command line for a while,
        # and a precondition nobody can reach through a screen is somebody else's to run.
        self.write(body=SCENARIO_SECTIONS_MD.replace(
            "**Given** nobody holds the address",
            "**Not through the screen:** the second tenant is seeded with `acme org create`, by "
            "whoever sets the environment up.\n\n**Given** nobody holds the address",
        ))
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_a_file_of_nothing_but_happy_paths_fails(self):
        self.write(body=SCENARIO_SECTIONS_MD.replace("**Type** negative", "**Type** happy path"))
        self.assert_fails("is every scenario a happy path")

    def test_a_file_with_no_scenario_in_it_fails(self):
        self.write(body=SCENARIO_SECTIONS_MD.replace("### S1 — somebody signs up", "### Notes")
                   .replace("### S2 — an address already taken", "### More notes"))
        self.assert_fails("carries no scenario")

    def test_a_type_outside_the_vocabulary_fails(self):
        self.write(body=SCENARIO_SECTIONS_MD.replace("**Type** negative", "**Type** sad path"))
        self.assert_fails("is a sad path scenario, not one of")

    def test_a_scenario_that_does_not_say_whether_it_can_be_run_fails(self):
        self.write(body=SCENARIO_SECTIONS_MD.replace(" · **Ready** yes", "", 1))
        self.assert_fails("says Ready nothing")

    def test_a_scenario_waiting_on_a_slice_is_a_real_answer(self):
        self.write(body=SCENARIO_SECTIONS_MD.replace(
            "**Ready** yes", "**Ready** no — the screen arrives with SL-001", 1))
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_a_quote_that_is_not_the_specification_s_words_fails(self):
        # The same rule the detail file works under: an amendment fails the cases written against
        # the old wording, rather than leaving them quietly testing it.
        self.write(body=SCENARIO_SECTIONS_MD.replace("> Sign up.", "> Sign up, more or less."))
        self.assert_fails("quotes FR-ACC-01 differently from the specification")

    def test_scenarios_with_no_detail_file_behind_them_fail(self):
        self.fx.write("writ/qa/scenarios/FR-ACC/FR-ACC-02.md", scenarios_md(ident="FR-ACC-02"))
        self.assert_fails("has no detail file under writ/spec/requirements")

    def test_a_detail_file_approved_since_the_cases_were_written_fails(self):
        # The one that makes the track self-correcting. Cases written from a draft are fine and
        # have to be re-read the day it is approved.
        self.fx.write(
            "writ/spec/requirements/FR-ACC/FR-ACC-01.md",
            detail_md(status="reviewed", approved_by="dana"),
        )
        self.assert_fails("was written against a draft detail file")

    def test_a_detail_file_revised_since_the_cases_were_read_fails(self):
        # The other half of the return path. Approval moves `status` once; every later amendment
        # to a reviewed file moves only `revised_on`, and this is what notices it.
        self.fx.write(
            "writ/spec/requirements/FR-ACC/FR-ACC-01.md",
            detail_md(revised_on="2026-09-12"),
        )
        self.assert_fails("was revised on 2026-09-12 — re-read it")

    def test_a_detail_file_revised_on_the_day_it_was_read_passes(self):
        self.fx.write(
            "writ/spec/requirements/FR-ACC/FR-ACC-01.md",
            detail_md(revised_on="2026-09-10"),
        )
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_a_missing_section_fails(self):
        self.write(body=SCENARIO_SECTIONS_MD.replace("## Before you start", "## Setup"))
        self.assert_fails("has no Before you start section")

    def test_a_reviewed_file_naming_no_approver_fails(self):
        self.write(status="reviewed")
        self.assert_fails("is reviewed and names no approver")

    def test_a_run_recorded_as_anything_but_the_three_results_fails(self):
        self.write(body=SCENARIO_SECTIONS_MD + "| 2026-09-10 | 1.2.0 | mostly fine | kim | — |\n")
        self.assert_fails("records the result mostly fine")

    def test_a_run_recorded_as_blocked_is_a_real_result(self):
        self.write(body=SCENARIO_SECTIONS_MD + "| 2026-09-10 | 1.2.0 | blocked | kim | no screen |\n")
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_a_file_in_the_wrong_area_directory_fails(self):
        self.fx.write("writ/qa/scenarios/FR-BIL/FR-ACC-01.md", scenarios_md())
        self.assert_fails("sits under FR-BIL and its identifier files under FR-ACC")

    def test_the_backlog_is_listed_and_the_gate_is_opt_in(self):
        self.fx.write(
            "writ/spec/requirements/FR-ACC/FR-ACC-02.md",
            detail_md(ident="FR-ACC-02", quote="Sign in.", status="reviewed", approved_by="dana"),
        )
        code, err = self.check()
        self.assertEqual(code, 0, err)
        coverage = self.fx.read("writ/process/COVERAGE.md")
        self.assertIn("### Settled, and nobody can be handed a session for it", coverage)
        self.assertIn("| FR-ACC-02 | none |", coverage)

        config = json.loads(self.fx.read("scripts/ledger.config.json"))
        config["scenarios"]["require_scenarios_for_reviewed_detail"] = True
        self.fx.config(config)
        self.assert_fails("FR-ACC-02 has a reviewed detail file and no scenarios")

    def test_a_project_with_no_scenario_directory_configured_ignores_the_track(self):
        config = json.loads(self.fx.read("scripts/ledger.config.json"))
        del config["scenarios"]
        self.fx.config(config)
        code, err = self.check()
        self.assertEqual(code, 0, err)
        self.assertNotIn("## Manual test scenarios", self.fx.read("writ/process/COVERAGE.md"))

    def test_the_directory_readme_is_not_read_as_a_scenarios_file(self):
        self.fx.write("writ/qa/scenarios/README.md", "# Scenarios\n\nProse, no front matter.\n")
        code, err = self.check()
        self.assertEqual(code, 0, err)



class CarriedBackTest(unittest.TestCase):
    """Three fixes a project carrying this tool found and sent back.

    Each is a case the kit's own suite could not have produced, because it tests the tool against a
    tree it writes itself: a formatter it does not run, identifiers it would never mint, and a queue
    shape it does not emit.
    """

    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.close)

    def check(self):
        self.fx.run("all")
        return self.fx.run("check")

    def test_a_test_name_on_its_own_line_is_still_an_annotation(self):
        # What a formatter does to a long test name. Per-line, the call and the name are two
        # unrelated lines and the annotation is invisible — in the one place evidence is counted.
        self.fx.write(
            "src/accounts.test.ts",
            "describe('a group', () => {\n  it(\n    '[FR-ACC-01] signs a person up with an address"
            " nobody holds',\n    async () => {},\n  );\n});\n",
        )
        code, err = self.fx.run("all")
        self.assertEqual(code, 0, err)
        self.assertIn("●", self.fx.read("writ/process/COVERAGE.md"))

    def test_an_identifier_off_its_pattern_fails_unless_it_is_named(self):
        # An adopting project meets the width rule with identifiers already cited and satisfied.
        # Renumbering them is the thing the registry forbids, so the escape is by name and shrinks.
        self.fx.write("writ/spec/BRD.md", BRD.replace("| FR-ACC-01 |", "| FR-ACC-01a |"))
        self.fx.write("src/accounts.test.ts", "it('[FR-ACC-01a] signs a person up', () => {});\n")
        self.fx.write("writ/process/work-orders/001.md",
                      work_order("SL-001", satisfies=["FR-ACC-01a"], status="done"))
        self.fx.write("writ/process/slices/001.md", "# SL-001\n")
        code, err = self.check()
        self.assertEqual(code, 1, err)
        self.assertIn("does not fit the FR pattern", err)

        config = dict(BASE_CONFIG)
        config["legacy_identifiers"] = ["FR-ACC-01a"]
        self.fx.config(config)
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_an_empty_queue_out_writes_no_block_and_demands_none(self):
        # A queue that is prose has nothing for the splice to write. `index_out` and `state_out`
        # already switched off this way; this was the one path with no off-switch.
        config = dict(BASE_CONFIG)
        config["queue_out"] = ""
        self.fx.config(config)
        self.fx.write("writ/process/SLICE-QUEUE.md", "# Queue\n\nProse, and no markers.\n")
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_a_queue_out_that_is_set_still_needs_its_block(self):
        self.fx.write("writ/process/SLICE-QUEUE.md", "# Queue\n\nProse, and no markers.\n")
        code, err = self.check()
        self.assertEqual(code, 1, err)
        self.assertIn("has no", err)


# ------------------------------------------------------------------------------------------------
# Adoption — the process arriving in a repository that predates it
# ------------------------------------------------------------------------------------------------
#
# Every test here is about a state greenfield never reaches: evidence older than the process,
# rules in force over part of a tree, and a slice whose whole job is to pin behaviour it did not
# write. The fixture is the same green tree; what changes is that somebody else got there first.


class AdoptionTest(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.close)

    def enforce(self, **rules):
        config = dict(BASE_CONFIG)
        config["enforce"] = rules
        self.fx.config(config)

    def check(self):
        """Regenerate, then verify. Every test here changes an input the ledger reads, and a
        stale artefact would fail the check before the rule under test got a chance to."""
        code, err = self.fx.run("all")
        if code:
            return code, err
        return self.fx.run("check")

    # -- the fourth state ---------------------------------------------------------------------

    def test_a_test_naming_a_requirement_no_slice_claims_reads_as_inherited(self):
        """The normal condition of every requirement read off an existing codebase."""
        self.fx.write("src/signout.test.ts", "it('[FR-ACC-03] signs a person out', () => {});\n")
        code, err = self.fx.run("all")
        self.assertEqual(code, 0, err)
        coverage = self.fx.read("writ/process/COVERAGE.md")
        self.assertIn("| FR-ACC-03 | ≈ |", coverage)
        self.assertIn("inherited | 1", coverage)

    def test_a_claim_with_no_test_is_still_partial_and_not_inherited(self):
        """The two were one state, and they are opposite failures: a broken promise against
        evidence nobody has claimed yet. Averaging them is what made the ledger unreadable on a
        codebase where most rows are the second."""
        code, err = self.fx.run("all")
        self.assertEqual(code, 0, err)
        coverage = self.fx.read("writ/process/COVERAGE.md")
        self.assertIn("| FR-ACC-02 | ◐ |", coverage)
        self.assertIn("| FR-ACC-03 | ○ |", coverage)

    def test_inherited_does_not_count_as_satisfied(self):
        """`≈` is evidence, not a discharged claim: nothing downstream may treat it as one."""
        self.fx.write("src/signout.test.ts", "it('[FR-ACC-03] signs a person out', () => {});\n")
        code, err = self.fx.run("all")
        self.assertEqual(code, 0, err)
        coverage = self.fx.read("writ/process/COVERAGE.md")
        self.assertIn("| ● satisfied | 1 |", coverage)
        self.assertIn("| ≈ inherited | 1 |", coverage)

    # -- the perimeter ------------------------------------------------------------------------

    def test_a_test_file_inside_the_perimeter_naming_nothing_fails(self):
        self.fx.write("src/billing.test.ts", "it('charges a card', () => {});\n")
        code, err = self.check()
        self.assertEqual(code, 1, err)
        self.assertIn("names no requirement", err)

    def test_an_empty_perimeter_turns_the_rule_off(self):
        """How the whole thing stays quiet on day one, with four other people committing."""
        self.enforce(default=[])
        self.fx.write("src/billing.test.ts", "it('charges a card', () => {});\n")
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_a_named_rule_replaces_the_default_rather_than_adding_to_it(self):
        """The reason it is not a union. Narrowing one rule below the default is the ordinary
        shape of a half-adopted repository, and a union cannot express it."""
        self.enforce(default=["**"], annotations=["src/billing/**"])
        self.fx.write("src/legacy.test.ts", "it('charges a card', () => {});\n")
        code, err = self.check()
        self.assertEqual(code, 0, err)
        self.fx.write("src/billing/charge.test.ts", "it('charges a card', () => {});\n")
        code, err = self.check()
        self.assertEqual(code, 1, err)
        self.assertIn("src/billing/charge.test.ts", err)

    def test_a_named_rule_may_widen_past_the_default(self):
        self.enforce(default=[], annotations=["**"])
        self.fx.write("src/billing.test.ts", "it('charges a card', () => {});\n")
        code, err = self.check()
        self.assertEqual(code, 1, err)

    def test_a_rule_not_named_inherits_the_default(self):
        self.enforce(default=["src/billing/**"])
        self.assertEqual(ledger.perimeter({"enforce": {"default": ["a/**"]}}, "annotations"), ["a/**"])
        self.assertEqual(ledger.perimeter({"enforce": {"default": ["a/**"], "annotations": []}}, "annotations"), [])

    def test_the_perimeter_language_is_the_same_glob_language_as_everything_else(self):
        self.assertTrue(ledger.within("src/a/b.test.ts", ["**"]))
        self.assertTrue(ledger.within("b.test.ts", ["**/*.test.ts"]))
        self.assertTrue(ledger.within("src/a/b.test.ts", ["**/*.test.ts"]))
        self.assertTrue(ledger.within("src/billing/x.ts", ["src/billing/**"]))
        self.assertFalse(ledger.within("src/billings/x.ts", ["src/billing/**"]))
        self.assertFalse(ledger.within("src/a/b.ts", ["src/*.ts"]))

    def test_a_partly_annotated_file_is_caught_only_when_a_case_pattern_is_configured(self):
        """File-level by default: a second pattern that has to be right about every stack is how
        this check would start inventing failures. Opt in and it counts cases."""
        self.fx.write(
            "src/accounts.test.ts",
            "it('[FR-ACC-01] signs a person up', () => {});\nit('signs a person in', () => {});\n",
        )
        code, err = self.check()
        self.assertEqual(code, 0, err)
        config = dict(BASE_CONFIG)
        config["tests"] = dict(BASE_CONFIG["tests"], case=r"\bit\s*\(")
        self.fx.config(config)
        code, err = self.check()
        self.assertEqual(code, 1, err)
        self.assertIn("has 2 tests and 1 annotated", err)

    # -- evidence that disappears -------------------------------------------------------------

    def test_a_proof_that_vanishes_is_reported_against_the_ledger_it_replaces(self):
        """Absence and loss read identically in a generated table. They are not the same event,
        and on a repository where other people commit without running this, the second is the
        one worth hearing about."""
        code, err = self.fx.run("all")
        self.assertEqual(code, 0, err)
        os.remove(os.path.join(self.fx.root, "src/accounts.test.ts"))
        code, err = self.fx.run("all")
        self.assertEqual(code, 0, err)
        self.assertIn("FR-ACC-01 was satisfied and is now partial", err)
        self.assertIn("a test that named it is gone", err)

    def test_a_proof_that_was_never_there_is_not_reported_as_lost(self):
        code, err = self.fx.run("all")
        self.assertEqual(code, 0, err)
        code, err = self.fx.run("all")
        self.assertEqual(code, 0, err)
        self.assertNotIn("is gone", err)

    def test_losing_a_proof_is_a_warning_and_never_the_exit_code(self):
        """The person who sees it is the one regenerating, and failing their build for somebody
        else's deletion is how the tool gets removed from the repository."""
        self.fx.run("all")
        os.remove(os.path.join(self.fx.root, "src/accounts.test.ts"))
        self.fx.write("writ/process/work-orders/001.md", work_order("SL-001"))
        code, err = self.fx.run("all")
        self.assertEqual(code, 0, err)
        self.assertIn("warning:", err)

    # -- characterisation slices --------------------------------------------------------------

    def test_a_characterisation_slice_may_have_no_demo(self):
        """It changes nothing, so there is nothing to play that was not playable yesterday."""
        self.fx.write(
            "writ/process/work-orders/003.md",
            work_order(
                "SL-003", kind="characterisation", demo="none",
                body="## Demo\n\nNothing new to show. This pins the existing sign-out behaviour,"
                     " which Priya confirmed against the support log is the behaviour intended.\n",
            ),
        )
        code, err = self.check()
        self.assertEqual(code, 0, err)

    def test_a_slice_that_changes_behaviour_may_not_say_demo_none(self):
        self.fx.write(
            "writ/process/work-orders/003.md",
            work_order("SL-003", demo="none", body="## Demo\n\nNothing to see.\n"),
        )
        code, err = self.check()
        self.assertEqual(code, 1, err)
        self.assertIn("only a `kind: characterisation` slice may say", err)

    def test_a_characterisation_slice_still_says_what_it_pinned(self):
        """The question a characterisation slice gets wrong is whether the behaviour it froze was
        wanted. A test written from the code asserts the bug as confidently as the feature."""
        self.fx.write(
            "writ/process/work-orders/003.md",
            work_order("SL-003", kind="characterisation", demo="none", body="## Demo\n\nNone.\n"),
        )
        code, err = self.check()
        self.assertEqual(code, 1, err)
        self.assertIn("does not say what behaviour", err)

    def test_a_kind_outside_the_vocabulary_fails(self):
        self.fx.write("writ/process/work-orders/003.md", work_order("SL-003", kind="cleanup"))
        code, err = self.check()
        self.assertEqual(code, 1, err)
        self.assertIn("kind is cleanup", err)

    # -- the instrument -----------------------------------------------------------------------

    def test_stats_reports_the_perimeter_and_the_characterisation_queue(self):
        self.enforce(default=["**"], work_order=["src/billing/**"])
        self.fx.write("src/signout.test.ts", "it('[FR-ACC-03] signs a person out', () => {});\n")
        self.fx.run("all")
        err, out = io.StringIO(), io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
            ledger.main(["stats", "--root", self.fx.root])
        report = out.getvalue()
        self.assertIn("Adoption — what this process is in force over", report)
        self.assertIn("work_order   src/billing/**", report)
        self.assertIn("the characterisation queue", report)

    def test_stats_counts_the_rows_still_read_off_the_code(self):
        """The documentation backlog of an adopted project, and the number that says how much of
        this specification describes behaviour rather than stating intent."""
        self.fx.write("writ/spec/BRD.md", BRD.replace(
            "| ID | Requirement | Target |\n|---|---|---|",
            "| ID | Requirement | Target | Provenance |\n|---|---|---|---|",
        ).replace("| M1 |", "| M1 | observed |"))
        self.fx.run("all")
        err, out = io.StringIO(), io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
            ledger.main(["stats", "--root", self.fx.root])
        self.assertIn("observed     3 of 3 rows are still read off the code", out.getvalue())

    def test_stats_says_nothing_about_adoption_on_a_greenfield_tree(self):
        """A project bootstrapped from the interview has a perimeter of everything and no
        inherited rows, and never sees this block."""
        self.fx.run("all")
        err, out = io.StringIO(), io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
            ledger.main(["stats", "--root", self.fx.root])
        self.assertNotIn("Adoption", out.getvalue())


class FileWalkTest(unittest.TestCase):
    """`iter_files` prunes excluded subtrees instead of listing them, and must still give exactly
    the answer `glob` would."""

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, True)
        for rel in (
            "src/a.test.ts",
            "src/deep/b.test.ts",
            "src/.hidden/c.test.ts",
            "src/.d.test.ts",
            "node_modules/pkg/x.test.ts",
            "packages/p/node_modules/y.test.ts",
            "packages/p/src/z.test.ts",
            "packages/p/dist/z.test.ts",
            "writ/process/templates/t.md",
            "writ/process/w.md",
            "writ/INDEX.md",
            ".claude/skills/s/SKILL.md",
            "a.test.ts",
        ):
            path = os.path.join(self.root, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w").close()

    def reference(self, includes, excludes):
        """What the walk replaced: expand everything, then discard."""
        excluded = set()
        for pattern in excludes:
            excluded.update(glob_all(self.root, pattern))
        found = set()
        for pattern in includes:
            found.update(h for h in glob_all(self.root, pattern) if os.path.isfile(h) and h not in excluded)
        return sorted(found)

    def test_the_answer_is_the_one_glob_gives(self):
        cases = [
            (["**/*.test.ts"], ["**/node_modules/**", "**/dist/**"]),
            (["writ/**/*.md", ".claude/skills/**/*.md"], ["writ/process/templates/**", "writ/INDEX.md"]),
            (["**"], []),
            (["src/*.test.ts", "a.test.ts"], []),
        ]
        for includes, excludes in cases:
            with self.subTest(includes=includes, excludes=excludes):
                self.assertEqual(ledger.iter_files(self.root, includes, excludes), self.reference(includes, excludes))

    def test_an_excluded_subtree_is_never_entered(self):
        visited = []
        real = os.walk

        def spy(top, *a, **k):
            for step in real(top, *a, **k):
                visited.append(os.path.relpath(step[0], self.root))
                yield step

        ledger.os.walk = spy
        self.addCleanup(setattr, ledger.os, "walk", real)
        ledger.iter_files(self.root, ["**/*.test.ts"], ["**/node_modules/**", "**/dist/**"])
        self.assertTrue(visited)
        self.assertFalse([v for v in visited if "node_modules" in v or "dist" in v], visited)


def glob_all(root, pattern):
    import glob

    return {os.path.normpath(h) for h in glob.glob(os.path.join(root, pattern), recursive=True)}


if __name__ == "__main__":
    unittest.main(verbosity=2)
