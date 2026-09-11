#!/usr/bin/env python3
"""The survey tool's own suite: `python3 scripts/test_survey.py`.

Every test builds a real git repository and makes real commits in it. Nothing here fakes `git log`
output, because the shape of that output is most of what the tool is: a format string, a merge
exclusion, and a NUL-ish record separator holding it together. A fixture that produced the text
this parser wants would test the parser against itself.

Stdlib only, and no network.
"""

from __future__ import annotations

import importlib.util
import io
import contextlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location("survey", os.path.join(HERE, "survey.py"))
survey = importlib.util.module_from_spec(SPEC)
sys.modules["survey"] = survey
SPEC.loader.exec_module(survey)


class Repo:
    """A throwaway git repository. `commit` takes {path: contents} and makes one commit of it."""

    def __init__(self):
        self.root = tempfile.mkdtemp()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "nobody@example.com")
        self.git("config", "user.name", "Sam")

    def git(self, *args):
        done = subprocess.run(
            ["git", "-C", self.root] + list(args), capture_output=True, text=True
        )
        if done.returncode:
            raise AssertionError("git " + " ".join(args) + ": " + done.stderr)
        return done.stdout

    def commit(self, files, author="Sam", message="a change", years_ago=0):
        """`years_ago` backdates both dates. `--since` filters on the committer date, so setting
        only the author date — the thing `--date` does — would change nothing."""
        for rel, text in files.items():
            path = os.path.join(self.root, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as handle:
                handle.write(text)
        self.git("add", "-A")
        when = None
        if years_ago:
            import datetime

            day = datetime.date.today() - datetime.timedelta(days=365 * years_ago)
            when = day.isoformat() + "T12:00:00"
        env = {"GIT_COMMITTER_DATE": when, "GIT_AUTHOR_DATE": when} if when else {}
        done = subprocess.run(
            ["git", "-C", self.root, "commit", "-q", "-m", message,
             "--author", author + " <" + author + "@x.com>"],
            capture_output=True, text=True, env=dict(os.environ, **env),
        )
        if done.returncode:
            raise AssertionError(done.stderr)

    def close(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def survey(self, months=24, top=12):
        return survey.survey(self.root, months, top)


class TestShapeTest(unittest.TestCase):
    """What counts as a test file. Every stack names them differently and getting this wrong
    reports a well-tested repository as having no tests at all, which is the one finding somebody
    would act on hardest."""

    def test_the_shapes_the_common_stacks_actually_use(self):
        for path in (
            "scripts/test_ledger.py",
            "src/a.test.ts",
            "src/a.spec.tsx",
            "tests/foo.py",
            "test/foo.rb",
            "spec/models/user.rb",
            "src/foo_test.go",
            "src/__tests__/a.js",
        ):
            self.assertTrue(survey.is_test(path), path)

    def test_a_word_that_merely_contains_test_is_not_a_test(self):
        """`testing.py` and `contest.py` are the two that a naive substring match swallows."""
        for path in ("src/testing.py", "src/contest.py", "src/latest.ts", "src/protest.go"):
            self.assertFalse(survey.is_test(path), path)

    def test_a_non_source_file_is_never_a_test(self):
        self.assertFalse(survey.is_test("tests/fixtures/a.json"))
        self.assertFalse(survey.is_test("docs/testing.md"))


class SurveyTest(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()
        self.addCleanup(self.repo.close)

    def test_it_counts_source_and_tests_apart(self):
        self.repo.commit({"src/api/a.py": "x = 1\n", "src/api/test_a.py": "def test_x(): pass\n"})
        data = self.repo.survey()
        self.assertEqual(data["source_files"], 2)
        self.assertEqual(data["test_files"], 1)

    def test_areas_are_two_levels_deep_and_ordered_by_movement(self):
        """One level is usually `src`, which tells nobody anything."""
        self.repo.commit({"src/billing/a.py": "1\n", "src/mail/b.py": "1\n"})
        for n in range(3):
            self.repo.commit({"src/billing/a.py": str(n) + "\n"})
        data = self.repo.survey()
        self.assertEqual(list(data["areas"])[0], "src/billing")
        self.assertIn("src/mail", data["areas"])

    def test_files_that_change_together_are_reported_as_coupled(self):
        """The cheapest way there is to find an invariant nobody wrote down."""
        self.repo.commit({"src/a/one.py": "1\n", "src/a/two.py": "1\n"})
        for n in range(3):
            self.repo.commit({"src/a/one.py": str(n) + "\n", "src/a/two.py": str(n) + "\n"})
        pairs = {(r["a"], r["b"]) for r in self.repo.survey()["coupled"]}
        self.assertIn(("src/a/one.py", "src/a/two.py"), pairs)

    def test_a_sweeping_commit_does_not_couple_everything_to_everything(self):
        """A rename, a format or a dependency bump touches half the repository at once. Counted,
        it swamps every genuine pair — which is the failure that makes this section worthless."""
        wide = {"src/a/f" + str(i) + ".py": "1\n" for i in range(20)}
        self.repo.commit(wide)
        for n in range(4):
            self.repo.commit({k: str(n) + "\n" for k in wide})
        self.assertEqual([], self.repo.survey()["coupled"])

    def test_a_merge_commit_is_not_read_as_one_enormous_simultaneous_change(self):
        self.repo.commit({"src/a/one.py": "1\n", "src/a/two.py": "1\n"})
        self.repo.git("checkout", "-q", "-b", "side")
        self.repo.commit({"src/a/one.py": "2\n"})
        self.repo.git("checkout", "-q", "main")
        self.repo.commit({"src/a/three.py": "1\n"})
        self.repo.git("merge", "-q", "--no-ff", "-m", "merge", "side")
        for author, _day, files in survey.commits(self.repo.root, 24):
            self.assertLess(len(files), 4, files)

    def test_a_source_file_no_commit_in_the_window_touched_is_quiet(self):
        """Candidates for dead, and the report says so: stable and abandoned look identical here."""
        self.repo.commit({"src/a/live.py": "1\n", "src/a/dead.py": "1\n"}, years_ago=3)
        self.repo.commit({"src/a/live.py": "2\n"})
        data = self.repo.survey(months=24)
        self.assertIn("src/a/dead.py", data["quiet"])
        self.assertNotIn("src/a/live.py", data["quiet"])

    def test_tests_are_never_reported_as_quiet(self):
        """A test nobody has changed is a test doing its job, not a candidate for deletion."""
        self.repo.commit({"src/a/test_a.py": "def test_x(): pass\n"}, years_ago=3)
        self.assertEqual([], self.repo.survey(months=24)["quiet"])

    def test_an_area_only_one_person_has_touched_is_named(self):
        """Where the undocumented knowledge is, and who to bring into the process second."""
        self.repo.commit({"src/solo/a.py": "1\n"}, author="Priya")
        self.repo.commit({"src/shared/b.py": "1\n"}, author="Priya")
        self.repo.commit({"src/shared/b.py": "2\n"}, author="Ade")
        hands = self.repo.survey()["hands"]
        self.assertEqual(["Priya"], hands["src/solo"])
        self.assertNotIn("src/shared", hands)

    def test_build_output_and_dependencies_are_not_the_product(self):
        self.repo.commit({"node_modules/x/i.js": "1\n", "dist/b.js": "1\n", "src/a/real.py": "1\n"})
        data = self.repo.survey()
        self.assertEqual(data["source_files"], 1)
        self.assertEqual(list(data["areas"]), ["src/a"])

    def test_a_hotspot_with_no_test_beside_it_is_marked(self):
        self.repo.commit({"src/a/charge.py": "1\n", "src/a/mail.py": "1\n", "src/a/test_mail.py": "t\n"})
        self.repo.commit({"src/a/charge.py": "2\n", "src/a/mail.py": "2\n"})
        by_path = {r["path"]: r["tested"] for r in self.repo.survey()["hotspots"]}
        self.assertFalse(by_path["src/a/charge.py"])
        self.assertTrue(by_path["src/a/mail.py"])

    def test_a_test_file_is_not_marked_as_having_no_test_beside_it(self):
        self.repo.commit({"src/a/test_a.py": "1\n"})
        self.repo.commit({"src/a/test_a.py": "2\n"})
        self.assertTrue(self.repo.survey()["hotspots"][0]["tested"])


class RunTest(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()
        self.addCleanup(self.repo.close)

    def run_main(self, *argv):
        err, out = io.StringIO(), io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
            code = survey.main(["--root", self.repo.root] + list(argv))
        return code, out.getvalue(), err.getvalue()

    def test_it_writes_nothing(self):
        """A survey that edits the repository it is surveying has stopped being one."""
        self.repo.commit({"src/a/a.py": "1\n"})
        before = self.repo.git("status", "--porcelain")
        self.run_main()
        self.assertEqual(before, self.repo.git("status", "--porcelain"))

    def test_a_repository_with_no_history_in_the_window_says_so_rather_than_reporting_nothing(self):
        """An empty report reads as *this codebase has no shape*, which is never the finding."""
        self.repo.commit({"src/a/a.py": "1\n"}, years_ago=3)
        code, _out, err = self.run_main("--since", "12")
        self.assertEqual(code, 1)
        self.assertIn("widen the window", err)

    def test_json_and_prose_carry_the_same_findings(self):
        import json

        self.repo.commit({"src/a/a.py": "1\n", "src/a/test_a.py": "t\n"})
        _code, prose, _ = self.run_main()
        _code, raw, _ = self.run_main("--json")
        self.assertEqual(json.loads(raw)["source_files"], 2)
        self.assertIn("Areas", prose)

    def test_somewhere_that_is_not_a_repository_fails_cleanly(self):
        where = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, where, True)
        err, out = io.StringIO(), io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
            code = survey.main(["--root", where])
        self.assertEqual(code, 1)
        self.assertIn("not a git repository", err.getvalue())

    def test_the_report_says_out_loud_that_none_of_it_is_a_finding(self):
        """The whole risk of this tool is somebody acting on a hotspot without asking why. The
        prose carrying that warning is load-bearing, so it is checked like anything else."""
        self.repo.commit({"src/a/a.py": "1\n"})
        _code, prose, _ = self.run_main()
        self.assertIn("none of this is a finding until somebody confirms it", prose)


if __name__ == "__main__":
    unittest.main(verbosity=2)
