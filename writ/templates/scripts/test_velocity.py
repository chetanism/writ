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

    def test_a_path_with_a_space_a_quote_or_a_byte_outside_ascii_is_counted(self):
        """git ends a name holding a space with a tab, and C-quotes one holding a quote or, by
        default, a byte outside ASCII. Each was read as a path nothing matched, and its lines lost."""
        self.repo.commit("2026-09-01", "feat: odd names", {
            "src/my file.py": "a = 1\nb = 2\n", "src/café.py": "a = 1\nb = 2\n", 'src/x"y.py': "a = 1\nb = 2\n",
        })
        rows = velocity.merges(self.repo.root, velocity.Ruler(velocity.load_settings(self.repo.root)))
        self.assertEqual((rows[0].code, rows[0].files), (6, 3))
        self.assertEqual(velocity.new_path('"b/caf\\303\\251 \\"x\\".py"'), 'café "x".py')

    def test_a_merge_dated_before_the_first_one_still_has_its_week(self):
        """`git log` orders by the graph, not the clock. A merge whose date is older than the first
        row's fell before the first week and vanished from every total."""
        self.repo.commit("2026-08-10", "feat: first in the graph", {"src/a.py": lines(5, "v = ")})
        self.repo.commit("2026-08-03", "feat: skewed clock", {"src/b.py": lines(7, "v = ")})
        weeks = velocity.weekly(velocity.merges(self.repo.root, velocity.Ruler(velocity.load_settings(self.repo.root))),
                                velocity.datetime.date(2026, 8, 17))
        self.assertEqual([(w[0], w[1], w[3]) for w in weeks], [("2026-W32", 1, 7), ("2026-W33", 1, 5)])

    def test_a_merge_is_dated_the_day_it_landed_not_the_day_it_was_first_written(self):
        """A rebased commit keeps its old author date; the committer date is when the branch got it."""
        self.repo.write("src/a.py", lines(4, "v = "))
        self.repo.git("add", "-A")
        env = dict(os.environ, GIT_AUTHOR_DATE="2026-07-01T12:00:00", GIT_COMMITTER_DATE="2026-08-10T12:00:00")
        subprocess.run(["git", "-C", self.repo.root, "commit", "-q", "-m", "feat: rebased"], check=True, env=env)
        rows = velocity.merges(self.repo.root, velocity.Ruler(velocity.load_settings(self.repo.root)))
        self.assertEqual(rows[0].date, "2026-08-10")

    def test_a_fractional_average_is_not_truncated_to_zero(self):
        self.repo.commit("2026-08-03", "feat: one", {"src/a.py": "v = 1\n"})
        self.repo.commit("2026-08-10", "feat: two", {"src/b.py": "v = 1\n"})
        code, out = self.repo.run("--check", "--today", "2026-08-31")
        self.assertEqual(code, 1, out)
        self.assertIn("2026-W35 added 0 code lines against a 3-week average of 0.7 (below 50%)", out)

    def test_a_repository_with_no_commits_says_so_and_exits_1(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            code = velocity.main(["--root", self.repo.root])
        self.assertEqual(code, 1)
        self.assertIn("no commits yet", err.getvalue())

    def test_a_branch_git_does_not_know_is_an_error_not_a_traceback(self):
        self.repo.commit("2026-09-01", "chore: start", {"README.md": "hi\n"})
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            code = velocity.main(["--root", self.repo.root, "--branch", "no-such-branch"])
        self.assertEqual(code, 1)
        self.assertIn("error: git log", err.getvalue())

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

    def test_outside_a_repository_it_says_so_and_exits_1(self):
        elsewhere = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, elsewhere, True)
        here = os.getcwd()
        os.chdir(elsewhere)
        self.addCleanup(os.chdir, here)
        for argv in ([], ["--root", elsewhere]):
            with self.subTest(argv=argv):
                err = io.StringIO()
                with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                    code = velocity.main(argv)
                self.assertEqual(code, 1)
                self.assertIn("not a git repository", err.getvalue())

    def test_the_stats_summary_is_empty_outside_a_repository(self):
        elsewhere = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, elsewhere, True)
        self.assertEqual(velocity.summary(elsewhere), [])
        self.assertEqual(velocity.backfill_summary(elsewhere, {}, "writ/spec/requirements"), [])

    # -- the backfill trend ---------------------------------------------------------------------

    def build(self, day, number, detail=None):
        files = {"src/%s.py" % number: "v = 1\n"}
        if detail:
            files["writ/spec/requirements/FR-A/" + detail + ".md"] = "# " + detail + "\n"
        self.repo.commit(day, "SL-%s\n\nSlice: SL-%s" % (number, number), files)

    def test_a_requirement_is_built_the_week_its_first_slice_merged_and_detailed_the_week_its_file_landed(self):
        self.build("2026-08-03", "001")
        self.build("2026-08-04", "002")
        self.repo.commit("2026-08-11", "docs: detail FR-A-01", {
            "writ/spec/requirements/FR-A/FR-A-01.md": "# FR-A-01\n",
            "writ/spec/requirements/FR-A/index.md": "| ID |\n",
        })
        claims = {"SL-001": ["FR-A-01"], "SL-002": ["FR-A-01", "FR-A-02"]}
        lines_ = velocity.backfill_summary(self.repo.root, claims, "writ/spec/requirements", velocity.datetime.date(2026, 8, 17))
        self.assertEqual(lines_, [
            "  2026-W32  built  +2  detailed  +0   gap 2",
            "  2026-W33  built  +0  detailed  +1   gap 1",
        ])

    def test_a_gap_that_keeps_growing_is_flagged(self):
        for n, day in enumerate(("2026-08-03", "2026-08-10", "2026-08-17", "2026-08-24"), start=1):
            self.build(day, "%03d" % n)
        claims = {"SL-%03d" % n: ["FR-A-%02d" % n] for n in range(1, 5)}
        lines_ = velocity.backfill_summary(self.repo.root, claims, "writ/spec/requirements", velocity.datetime.date(2026, 8, 31))
        self.assertIn("  ⚑ the gap grew from 1 to 4 over the last 3 weeks — the build is outrunning the backfill", lines_)

    def test_a_backfill_keeping_pace_is_quiet(self):
        for n, day in enumerate(("2026-08-03", "2026-08-10", "2026-08-17", "2026-08-24"), start=1):
            self.build(day, "%03d" % n, detail="FR-A-%02d" % n)
        claims = {"SL-%03d" % n: ["FR-A-%02d" % n] for n in range(1, 5)}
        lines_ = velocity.backfill_summary(self.repo.root, claims, "writ/spec/requirements", velocity.datetime.date(2026, 8, 31))
        self.assertTrue(lines_)
        self.assertFalse([line for line in lines_ if "⚑" in line], lines_)


if __name__ == "__main__":
    unittest.main(verbosity=2)
