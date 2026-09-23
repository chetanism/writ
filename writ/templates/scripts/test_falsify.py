#!/usr/bin/env python3
"""Tests for the falsification runner, against a throwaway repository whose tests are plain scripts.

    python3 scripts/test_falsify.py
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import falsify  # noqa: E402

GUARD = "def allowed(n):\n    if n > 10:\n        return False\n    return True\n"
STRONG = "# [FR-A-01] refuses more than ten\nimport sys; sys.path.insert(0, 'src')\nfrom guard import allowed\nassert allowed(11) is False\n"
WEAK = "# [FR-A-02] allows a small number\nimport sys; sys.path.insert(0, 'src')\nfrom guard import allowed\nassert allowed(3) is True\n"
CONFIG = {
    "tests": {"globs": ["tests/*.py"], "exclude": []},
    "falsify": {"runners": [{"match": ["tests/**"], "command": "for f in {files}; do python3 \"$f\" || exit 1; done"}]},
}
REMOVE_GUARD = {"control": "refuses more than ten", "file": "src/guard.py", "find": "    if n > 10:\n        return False\n"}


class FalsifyTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, True)
        self.write("src/guard.py", GUARD)
        self.write("tests/test_strong.py", STRONG)
        self.write("tests/test_weak.py", WEAK)
        self.write("scripts/ledger.config.json", json.dumps(CONFIG))
        for args in (("init", "-q"), ("add", "-A"), ("-c", "user.email=t@e", "-c", "user.name=t", "commit", "-qm", "start")):
            subprocess.run(["git", "-C", self.root, *args], check=True, capture_output=True)

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)

    def read(self, rel):
        with open(os.path.join(self.root, rel), encoding="utf-8") as handle:
            return handle.read()

    def run_plan(self, plan, *extra):
        self.write("plan.json", json.dumps(plan))
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = falsify.main(["plan.json", "--root", self.root, *extra])
        return code, out.getvalue(), err.getvalue()

    def test_a_control_its_test_notices_is_caught_and_one_it_does_not_survives(self):
        code, out, err = self.run_plan([
            dict(REMOVE_GUARD, expect=["FR-A-01"]),
            dict(REMOVE_GUARD, control="the same guard, judged by the wrong test", expect=["FR-A-02"]),
        ])
        self.assertEqual(code, 0, err)
        self.assertIn("| refuses more than ten | `src/guard.py` | `tests/test_strong.py` | caught |", out)
        self.assertIn("| the same guard, judged by the wrong test | `src/guard.py` | `tests/test_weak.py` | **survived** |", out)
        self.assertIn("2 controls · 1 survived", out)
        self.assertEqual(self.read("src/guard.py"), GUARD)

    def test_only_the_annotated_files_run(self):
        self.write("tests/test_unrelated.py", "# [FR-Z-09] broken on purpose\nraise SystemExit(1)\n")
        subprocess.run(["git", "-C", self.root, "add", "-A"], check=True)
        code, out, err = self.run_plan([dict(REMOVE_GUARD, expect=["FR-A-02"])])
        self.assertEqual(code, 0, err)
        self.assertNotIn("test_unrelated", out)
        self.assertIn("**survived**", out)

    def test_a_group_red_before_anything_is_removed_is_unreliable_not_caught(self):
        self.write("tests/test_strong.py", STRONG.replace("is False", "is True"))
        subprocess.run(["git", "-C", self.root, "-c", "user.email=t@e", "-c", "user.name=t", "commit", "-qam", "red"], check=True)
        code, out, err = self.run_plan([dict(REMOVE_GUARD, expect=["FR-A-01"])])
        self.assertEqual(code, 0, err)
        self.assertIn("unreliable: tests/test_strong.py is already fail", out)
        self.assertIn("| unreliable |", out)

    def test_a_wrong_plan_is_refused_and_nothing_is_touched(self):
        cases = [
            (dict(REMOVE_GUARD, find="not in the file", expect=["FR-A-01"]), "occurs 0 times"),
            (dict(REMOVE_GUARD, find="return", expect=["FR-A-01"]), "occurs 2 times"),
            (dict(REMOVE_GUARD, **{"with": REMOVE_GUARD["find"]}, expect=["FR-A-01"]), "would not change the file"),
            (dict(REMOVE_GUARD, expect=["FR-NOPE-01"]), "no annotated test file names FR-NOPE-01"),
            (dict(REMOVE_GUARD, expect=[]), "needs `expect`"),
        ]
        for entry, message in cases:
            with self.subTest(message=message):
                code, _out, err = self.run_plan([entry])
                self.assertEqual(code, 1)
                self.assertIn(message, err)
                self.assertEqual(self.read("src/guard.py"), GUARD)

    def test_a_file_with_uncommitted_changes_is_refused(self):
        self.write("src/guard.py", GUARD + "# work in progress\n")
        code, _out, err = self.run_plan([dict(REMOVE_GUARD, expect=["FR-A-01"])])
        self.assertEqual(code, 1)
        self.assertIn("has uncommitted changes", err)
        self.assertEqual(self.read("src/guard.py"), GUARD + "# work in progress\n")

    def test_a_dry_run_lists_and_removes_nothing(self):
        code, out, err = self.run_plan([dict(REMOVE_GUARD, expect=["FR-A-01", "FR-A-02"])], "--dry-run")
        self.assertEqual(code, 0, err)
        self.assertIn("tests/test_strong.py tests/test_weak.py", out)
        self.assertNotIn("baseline", out)

    def test_an_interrupted_run_restores_the_file(self):
        real = falsify.run
        calls = []

        def interrupt(*args):
            calls.append(args)
            if len(calls) > 1:  # after the baseline, while the guard is removed
                self.assertNotEqual(self.read("src/guard.py"), GUARD)
                raise KeyboardInterrupt
            return real(*args)

        falsify.run = interrupt
        self.addCleanup(setattr, falsify, "run", real)
        code, _out, err = self.run_plan([dict(REMOVE_GUARD, expect=["FR-A-01"])])
        self.assertEqual(code, 130)
        self.assertIn("every file was restored", err)
        self.assertEqual(self.read("src/guard.py"), GUARD)

    def test_a_runner_left_as_the_template_placeholder_is_refused(self):
        self.write("scripts/ledger.config.json", json.dumps(dict(CONFIG, falsify={"runners": [{"command": "<unit test command> {files}"}]})))
        code, _out, err = self.run_plan([dict(REMOVE_GUARD, expect=["FR-A-01"])])
        self.assertEqual(code, 1)
        self.assertIn("still the template's placeholder", err)

    def test_outside_a_repository_it_refuses_to_start_and_touches_nothing(self):
        shutil.rmtree(os.path.join(self.root, ".git"))
        code, _out, err = self.run_plan([dict(REMOVE_GUARD, expect=["FR-A-01"])])
        self.assertEqual(code, 1)
        self.assertIn("not a git repository", err)
        self.assertEqual(self.read("src/guard.py"), GUARD)

    def test_a_runner_can_run_inside_each_package(self):
        config = dict(CONFIG, tests={"globs": ["pkgs/*/tests/*.py"], "exclude": []})
        config["falsify"] = {"runners": [{"match": ["**"], "cwd": "package",
                                          "command": "test -f pyproject.toml && for f in {files}; do python3 \"$f\" || exit 1; done"}]}
        self.write("scripts/ledger.config.json", json.dumps(config))
        self.write("pkgs/one/pyproject.toml", "")
        self.write("pkgs/one/src/guard.py", GUARD)
        self.write("pkgs/one/tests/test_strong.py", STRONG)
        subprocess.run(["git", "-C", self.root, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.root, "-c", "user.email=t@e", "-c", "user.name=t", "commit", "-qm", "pkg"], check=True)
        code, out, err = self.run_plan([dict(REMOVE_GUARD, file="pkgs/one/src/guard.py", expect=["FR-A-01"])])
        self.assertEqual(code, 0, err)
        self.assertIn("`pkgs/one/tests/test_strong.py` | caught |", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
