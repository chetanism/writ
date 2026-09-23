#!/usr/bin/env python3
"""Tests for the velocity tool, against real git repositories built in a temporary directory.

    python3 scripts/test_velocity.py
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location("velocity", os.path.join(HERE, "velocity.py"))
velocity = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(velocity)


class Repo:
    def __init__(self):
        self.root = tempfile.mkdtemp()
        self.git("init", "-q", "-b", "dev")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "t")
        self.git("config", "commit.gpgsign", "false")

    def git(self, *args, date=None):
        env = dict(os.environ)
        if date:
            env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date + "T12:00:00"
        return subprocess.run(["git", "-C", self.root, *args], check=True, capture_output=True, env=env).stdout.decode()

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(text)

    def commit(self, date, message, files):
        for rel, text in files.items():
            self.write(rel, text)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message, date=date)

    def run(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = velocity.main(list(argv) + ["--root", self.root])
        return code, out.getvalue()


def lines(n, prefix="x"):
    return "".join(prefix + str(i) + "\n" for i in range(n))


class VelocityTest(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()
        self.addCleanup(shutil.rmtree, self.repo.root, True)

    def test_only_code_counts_as_code(self):
        self.repo.commit("2026-09-01", "feat: a thing", {
            "src/a.ts": "const a = 1;\n\n// a comment\n/* another */\nconst b = 2;\n",
            "src/a.test.ts": "it('[FR-A-01] works', () => {});\n",
            "writ/notes.md": "# Notes\n\nSome prose.\n",
            "pnpm-lock.yaml": lines(50),
            "writ/process/COVERAGE.md": lines(20),
        })
        self.repo.write("scripts/ledger.config.json", json.dumps({"coverage_out": "writ/process/COVERAGE.md"}))
        rows = velocity.merges(self.repo.root, velocity.Ruler(velocity.load_settings(self.repo.root)))
        self.assertEqual((rows[0].code, rows[0].test, rows[0].md), (2, 1, 2))

    def test_a_slice_is_known_by_its_trailer_and_a_merge_is_measured_against_its_first_parent(self):
        self.repo.commit("2026-09-01", "chore: start", {"README.md": "hi\n"})
        self.repo.git("checkout", "-q", "-b", "slice/001")
        self.repo.commit("2026-09-02", "feat: work", {"src/a.py": lines(7, "a = ")})
        self.repo.git("checkout", "-q", "dev")
        self.repo.commit("2026-09-02", "docs: meanwhile", {"writ/x.md": "x\n"})
        self.repo.git("merge", "-q", "--no-ff", "slice/001", "-m", "SL-001 — a thing\n\nSlice: SL-001\nSatisfies: FR-A-01\n\nCloses #4\n", date="2026-09-03")
        rows = velocity.merges(self.repo.root, velocity.Ruler(velocity.load_settings(self.repo.root)))
        merge = rows[-1]
        self.assertEqual(merge.slice, "SL-001")
        self.assertEqual(merge.code, 7)
        self.assertEqual([r.slice for r in rows[:-1]], ["", ""])

    def test_a_week_well_below_its_trailing_average_trips_the_check(self):
        for day in ("2026-08-03", "2026-08-10", "2026-08-17", "2026-08-24"):
            self.repo.commit(day, "feat: steady\n\nSlice: SL-" + day[-2:], {"src/" + day + ".py": lines(100, "v = ")})
        self.repo.commit("2026-08-31", "feat: slow\n\nSlice: SL-99", {"src/slow.py": lines(10, "v = ")})
        code, out = self.repo.run("--check", "--today", "2026-09-08")
        self.assertEqual(code, 1, out)
        self.assertIn("throughput dropped: 2026-W36 added 10 code lines against a 3-week average of 100", out)
        code, out = self.repo.run("--today", "2026-09-08")
        self.assertEqual(code, 0, "without --check a flag is a report, never a failure")

    def test_a_steady_week_and_a_short_history_are_quiet(self):
        for day in ("2026-08-03", "2026-08-10", "2026-08-17", "2026-08-24", "2026-08-31"):
            self.repo.commit(day, "feat: steady", {"src/" + day + ".py": lines(100, "v = ")})
        code, out = self.repo.run("--check", "--today", "2026-09-08")
        self.assertEqual(code, 0, out)
        self.assertIn("no velocity threshold tripped", out)

    def test_an_empty_week_counts_as_a_week(self):
        for day in ("2026-08-03", "2026-08-10", "2026-08-17", "2026-08-24"):
            self.repo.commit(day, "feat: steady", {"src/" + day + ".py": lines(100, "v = ")})
        code, out = self.repo.run("--check", "--today", "2026-09-08")
        self.assertEqual(code, 1, out)
        self.assertIn("2026-W36 added 0 code lines", out)

    def test_ceremony_outgrowing_the_code_trips_the_check(self):
        self.repo.commit("2026-08-31", "chore: configure", {
            "scripts/ledger.config.json": json.dumps({"velocity": {"ceremony_slices": 2, "trailing_weeks": 0}}),
        })
        for n in (1, 2):
            self.repo.commit("2026-09-0" + str(n), "SL-00%d\n\nSlice: SL-00%d" % (n, n),
                             {"src/%d.py" % n: lines(10, "v = "), "writ/%d.md" % n: lines(40)})
        code, out = self.repo.run("--check", "--today", "2026-09-03")
        self.assertEqual(code, 1, out)
        self.assertIn("ceremony grew: the last 2 slices added 80 Markdown lines for 20 code lines", out)

    def test_diff_measures_the_branch_against_its_base(self):
        self.repo.commit("2026-09-01", "chore: start", {"README.md": "hi\n"})
        self.repo.git("checkout", "-q", "-b", "slice/002")
        self.repo.commit("2026-09-02", "feat: work", {"src/b.go": "package b\n// note\nvar X = 1\n", "b_test.go": "package b\n"})
        code, out = self.repo.run("--diff", "dev")
        self.assertEqual(code, 0)
        self.assertIn("code 2 · test 1 · md 0", out)

    def test_with_no_root_it_measures_the_repository_it_was_run_from(self):
        self.repo.commit("2026-09-01", "feat: only in the other repository", {"src/a.py": "a = 1\n"})
        here = os.getcwd()
        os.chdir(os.path.join(self.repo.root, "src"))
        self.addCleanup(os.chdir, here)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            velocity.main(["--today", "2026-09-08"])
        self.assertIn("only in the other repository", out.getvalue())

    def test_the_stats_summary_is_empty_outside_a_repository(self):
        elsewhere = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, elsewhere, True)
        self.assertEqual(velocity.summary(elsewhere), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
