#!/usr/bin/env python3
"""Tests for the claims tool, against the synthetic tree `test_ledger.py` builds.

    python3 scripts/test_claims.py
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ledger = load("ledger")
fixtures = load("test_ledger")
claims = load("claims")

BRD = """# BRD

## 2. Invariants

| ID | Invariant |
|---|---|
| **INV-1** | Every row carries a tenant. |

## 3. Functional requirements

| ID | Requirement | Target |
|---|---|---|
| FR-ACC-01 | Sign up. | M1 |
| FR-ACC-02 | Sign in. | M1 |
| FR-ACC-03 | Sign out. | M1 |
| FR-ACC-04 | Reset a password. | M1 |
| FR-ACC-05 | Close an account. | M1 |
| FR-ACC-06 | Export an account. | M1 |
| FR-ACC-07 | Rename an account. | M1 |
"""

TESTS = "\n".join([
    "it('[FR-ACC-01] signs a person up', () => {});",
    "it('[FR-ACC-02] signs a person in', () => {});",
    "it('[FR-ACC-03] signs a person out', () => {});",
    "it('[FR-ACC-07] renames an account', () => {});",
    "// FR-ACC-06 is exercised by the export spike below, which is not a test yet",
    "",
])

WO = "writ/process/work-orders/"


class ClaimsTest(unittest.TestCase):
    def setUp(self):
        self.fx = fixtures.Fixture()
        self.addCleanup(self.fx.close)
        self.fx.write("writ/spec/BRD.md", BRD)
        self.fx.write(WO + "001.md", fixtures.work_order("SL-001", status="done", satisfies=["FR-ACC-01"]))
        self.fx.write(WO + "002.md", fixtures.work_order(
            "SL-002", status="done", satisfies=["FR-ACC-04"], partial=["FR-ACC-03"],
            body="## Out of scope\n\nClosing an account (FR-ACC-05) waits for billing.\n",
        ))
        self.fx.write(WO + "003.md", fixtures.work_order("SL-003", status="in-progress", partial=["FR-ACC-07"]))
        self.fx.write("writ/process/slices/SL-001.md", "# SL-001\n\nSign-in (FR-ACC-02) came along for free.\n")
        self.fx.write("src/accounts.test.ts", TESTS)

    def classify(self):
        return {r["id"]: r for r in claims.classify(self.fx.root, ledger.load_config(self.fx.root, "scripts/ledger.config.json"))}

    def run_tool(self, *argv):
        err, out = io.StringIO(), io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
            code = claims.main(list(argv) + ["--root", self.fx.root])
        return code, out.getvalue(), err.getvalue()

    def corrections(self, entries):
        self.fx.write("corrections.json", json.dumps(entries))
        return self.run_tool("apply", os.path.join(self.fx.root, "corrections.json"))

    # -- classify ------------------------------------------------------------------------------

    def test_each_row_lands_in_the_bucket_its_ledger_state_and_claims_put_it_in(self):
        rows = self.classify()
        self.assertEqual(
            {i: r["bucket"] for i, r in rows.items()},
            {
                "FR-ACC-02": "inherited",
                "FR-ACC-03": "partial_only",
                "FR-ACC-04": "claim_no_test",
                "FR-ACC-05": "unclaimed_mentioned",
                "FR-ACC-06": "unclaimed_mentioned",
            },
        )

    def test_a_finished_row_and_one_nothing_names_are_left_out(self):
        rows = self.classify()
        self.assertNotIn("FR-ACC-01", rows)
        self.assertNotIn("INV-1", rows)

    def test_a_partial_claim_by_a_slice_still_open_is_not_a_row_to_review(self):
        self.assertNotIn("FR-ACC-07", self.classify())

    def test_the_mark_is_the_ledgers_own(self):
        rows = self.classify()
        self.assertEqual((rows["FR-ACC-02"]["mark"], rows["FR-ACC-03"]["mark"], rows["FR-ACC-05"]["mark"]), ("≈", "◐", "○"))

    def test_an_inherited_row_lists_the_summary_that_names_it(self):
        self.assertEqual(self.classify()["FR-ACC-02"]["mentions"], ["writ/process/slices/SL-001.md"])

    def test_a_test_file_mention_the_annotation_pattern_misses_is_listed(self):
        self.assertEqual(self.classify()["FR-ACC-06"]["mentions"], ["src/accounts.test.ts"])

    def test_a_mention_is_a_whole_identifier(self):
        self.fx.write("writ/process/slices/SL-002.md", "# SL-002\n\nFR-ACC-050 is not FR-ACC-05.\n")
        mentions = self.classify()["FR-ACC-05"]["mentions"]
        self.assertIn("writ/process/slices/SL-002.md", mentions)
        self.fx.write("writ/process/slices/SL-002.md", "# SL-002\n\nOnly FR-ACC-050 here.\n")
        self.assertNotIn("writ/process/slices/SL-002.md", self.classify()["FR-ACC-05"]["mentions"])

    def test_the_key_moves_when_the_evidence_does(self):
        before = self.classify()["FR-ACC-03"]["key"]
        self.fx.write("src/more.test.ts", "it('[FR-ACC-03] signs out everywhere', () => {});\n")
        self.assertNotEqual(self.classify()["FR-ACC-03"]["key"], before)

    def test_skip_leaves_out_a_settled_row_until_its_evidence_changes(self):
        key = self.classify()["FR-ACC-03"]["key"]
        self.fx.write("report.md", "## Skip next run\n\n- `FR-ACC-03` · `" + key + "` · OPEN\n")
        code, out, _ = self.run_tool("classify", "--json", "--skip", os.path.join(self.fx.root, "report.md"))
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertNotIn("FR-ACC-03", [r["id"] for r in data["rows"]])
        self.assertEqual(data["skipped"], 1)

        self.fx.write("src/more.test.ts", "it('[FR-ACC-03] signs out everywhere', () => {});\n")
        code, out, _ = self.run_tool("classify", "--json", "--skip", os.path.join(self.fx.root, "report.md"))
        self.assertIn("FR-ACC-03", [r["id"] for r in json.loads(out)["rows"]])

    def test_batches_never_mix_buckets_and_hold_at_most_the_size_asked(self):
        code, out, _ = self.run_tool("classify", "--json", "--batch", "1")
        self.assertEqual(code, 0)
        batches = json.loads(out)["batches"]
        self.assertEqual(batches, [["FR-ACC-02"], ["FR-ACC-03"], ["FR-ACC-04"], ["FR-ACC-05"], ["FR-ACC-06"]])
        code, out, _ = self.run_tool("classify", "--json", "--batch", "30")
        self.assertIn(["FR-ACC-05", "FR-ACC-06"], json.loads(out)["batches"])

    def test_classify_reports_and_writes_nothing(self):
        before = self.fx.read(WO + "002.md")
        code, out, _ = self.run_tool("classify")
        self.assertEqual(code, 0)
        self.assertIn("partial_only — 1", out)
        self.assertEqual(self.fx.read(WO + "002.md"), before)
        self.assertFalse(os.path.exists(os.path.join(self.fx.root, "writ/process/COVERAGE.md")))

    # -- apply ---------------------------------------------------------------------------------

    def test_a_partial_moved_to_satisfies_leaves_the_partial_list_and_the_ledger_follows(self):
        code, out, err = self.corrections([{"work_order": "002.md", "id": "FR-ACC-03", "to": "satisfies"}])
        self.assertEqual(code, 0, err)
        front, _ = ledger.parse_front_matter(self.fx.read(WO + "002.md"))
        self.assertEqual((front["satisfies"], front["partial"]), (["FR-ACC-04", "FR-ACC-03"], []))
        self.assertIn("SL-002 satisfies FR-ACC-03 — proved by: [FR-ACC-03] signs a person out", out)

        code, err = self.fx.run("ledger")
        self.assertEqual(code, 0, err)
        self.assertIn("| FR-ACC-03 | ● |", self.fx.read("writ/process/COVERAGE.md"))

    def test_a_missed_claim_on_an_inherited_row_is_added(self):
        code, _, err = self.corrections([{"work_order": "001.md", "id": "FR-ACC-02", "to": "satisfies"}])
        self.assertEqual(code, 0, err)
        front, _ = ledger.parse_front_matter(self.fx.read(WO + "001.md"))
        self.assertEqual(front["satisfies"], ["FR-ACC-01", "FR-ACC-02"])

    def test_only_the_two_claim_lines_change(self):
        before = self.fx.read(WO + "002.md").split("\n")
        code, _, err = self.corrections([{"work_order": "002.md", "id": "FR-ACC-03", "to": "satisfies"}])
        self.assertEqual(code, 0, err)
        after = self.fx.read(WO + "002.md").split("\n")
        self.assertEqual(len(before), len(after))
        changed = [a for b, a in zip(before, after) if a != b]
        self.assertEqual(changed, ["satisfies: [FR-ACC-04, FR-ACC-03]", "partial: []"])

    def test_a_trailing_comment_survives_and_a_block_list_is_folded(self):
        text = fixtures.work_order("SL-001", status="done").replace(
            "---\n\n", "satisfies:              # [FR-ACC-01] — what it proves\n  - FR-ACC-01\n"
            "partial:                # [INV-003] — what it moves forward\n---\n\n", 1)
        self.fx.write(WO + "001.md", text)
        code, _, err = self.corrections([{"work_order": "001.md", "id": "FR-ACC-02", "to": "satisfies"}])
        self.assertEqual(code, 0, err)
        written = self.fx.read(WO + "001.md")
        self.assertIn("satisfies: [FR-ACC-01, FR-ACC-02] # [FR-ACC-01] — what it proves\n", written)
        self.assertIn("partial: []             # [INV-003] — what it moves forward\n", written)
        self.assertNotIn("  - FR-ACC-01", written)

    def test_satisfies_without_a_test_naming_it_is_refused(self):
        code, _, err = self.corrections([{"work_order": "002.md", "id": "FR-ACC-05", "to": "satisfies"}])
        self.assertEqual(code, 1)
        self.assertIn("FR-ACC-05 has no test naming it", err)

    def test_a_work_order_not_yet_done_is_refused(self):
        code, _, err = self.corrections([{"work_order": "003.md", "id": "FR-ACC-07", "to": "satisfies"}])
        self.assertEqual(code, 1)
        self.assertIn("003.md is in-progress, not done", err)

    def test_an_undeclared_identifier_and_an_unknown_target_are_refused(self):
        code, _, err = self.corrections([
            {"work_order": "002.md", "id": "FR-ACC-99", "to": "partial"},
            {"work_order": "002.md", "id": "FR-ACC-03", "to": "done"},
        ])
        self.assertEqual(code, 1)
        self.assertIn("FR-ACC-99 is not declared", err)
        self.assertIn("the target is satisfies or partial", err)

    def test_a_path_outside_the_work_orders_is_refused(self):
        self.fx.write("writ/spec/other.md", "---\nid: SL-009\nstatus: done\n---\n")
        code, _, err = self.corrections([{"work_order": "../../spec/other.md", "id": "FR-ACC-02", "to": "partial"}])
        self.assertEqual(code, 1)
        self.assertIn("not a path under", err)

    def test_an_entry_with_other_fields_is_refused(self):
        code, _, err = self.corrections([{"work_order": "002.md", "id": "FR-ACC-03", "to": "satisfies", "body": "x"}])
        self.assertEqual(code, 1)
        self.assertIn("nothing else", err)

    def test_one_bad_entry_changes_nothing_at_all(self):
        before = self.fx.read(WO + "002.md")
        code, _, err = self.corrections([
            {"work_order": "002.md", "id": "FR-ACC-03", "to": "satisfies"},
            {"work_order": "003.md", "id": "FR-ACC-07", "to": "satisfies"},
        ])
        self.assertEqual(code, 1)
        self.assertIn("nothing was changed", err)
        self.assertEqual(self.fx.read(WO + "002.md"), before)

    def test_a_partial_claim_never_demotes_a_satisfies(self):
        code, out, err = self.corrections([{"work_order": "002.md", "id": "FR-ACC-04", "to": "partial"}])
        self.assertEqual(code, 0, err)
        front, _ = ledger.parse_front_matter(self.fx.read(WO + "002.md"))
        self.assertEqual((front["satisfies"], front["partial"]), (["FR-ACC-04"], ["FR-ACC-03"]))


if __name__ == "__main__":
    unittest.main()
