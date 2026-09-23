#!/usr/bin/env python3
"""Falsify a slice: remove each control it added, run only the tests that should notice, restore.

    python3 scripts/falsify.py writ/process/slices/<milestone>/<phase>/<ID>.falsify.json
    python3 scripts/falsify.py <plan> --dry-run      # validate the plan, list what would run

**Why a tool.** Falsification is the step of `/slice-close` that finds defects — on the project this
was ported from it found one in nearly half of all slices — and its cost was never the test runs. It
was the loop around them, done by hand for every control: find the line, edit it, run the suite,
read the result, restore the file, write the row. A minute of judgement stretched over two minutes
of clerical work, a few hundred times.

**The plan** is a JSON list, one entry per control:

    [{"control": "refuses a second sign-up",
      "file": "src/accounts/signup.ts",
      "find": "if (existing) throw new Conflict()",
      "with": "",
      "expect": ["FR-ACC-02"]}]

`find` must occur exactly once in `file`; `with` replaces it (default: nothing). `expect` names the
requirements whose tests should fail with the control gone — the same identifiers the tests are
annotated with, resolved to files by `ledger.py`'s annotation reader.

**What it refuses**, each of which once produced a false *caught* by hand:

  - a removal that does not change the file's bytes — a `find` that equals its `with`;
  - a file with uncommitted changes — restoring it afterwards would destroy work;
  - an `expect` naming no annotated test file — there would be nothing to run.

**What it does instead of the whole suite.** Runs only the test files annotated with each control's
`expect`, grouped by the `falsify.runners` entry in `scripts/ledger.config.json` whose `match` they
fall under — so unit and integration files never share one run. A baseline runs **once, before
anything is removed**; a group already red is reported `unreliable` rather than counted as a catch.

**Restores every file** it touched, on success, on error and on Ctrl-C.

Exits 0 when the plan ran, whatever it found — a control nothing caught is a finding for the
summary, not a crash — and 1 when the plan itself is wrong. Standard library only, Python 3.9+.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ledger  # noqa: E402 — a sibling script, not a package

PACKAGE_MARKERS = ("package.json", "pyproject.toml", "go.mod", "Cargo.toml", "pom.xml", "build.gradle", "Gemfile")


class PlanError(Exception):
    pass


def git_clean(root: str, rel: str) -> bool:
    """No uncommitted change to `rel`, staged or not. Outside a repository nothing can be checked,
    and nothing is refused."""
    done = subprocess.run(["git", "-C", root, "status", "--porcelain", "--", rel], capture_output=True, text=True)
    if done.returncode != 0:
        return True
    return not done.stdout.strip()


def load_plan(root: str, path: str) -> list:
    try:
        with open(path, encoding="utf-8") as handle:
            plan = json.load(handle)
    except (OSError, ValueError) as err:
        raise PlanError(path + ": " + str(err))
    if not isinstance(plan, list) or not plan:
        raise PlanError(path + ": a plan is a non-empty JSON list of controls")
    problems = []
    for n, entry in enumerate(plan, start=1):
        where = "control " + str(n) + " (" + str(entry.get("control") or "unnamed") + ")"
        for key in ("control", "file", "find", "expect"):
            if not entry.get(key):
                problems.append(where + ": needs `" + key + "`")
        if problems and problems[-1].startswith(where):
            continue
        entry.setdefault("with", "")
        if entry["find"] == entry["with"]:
            problems.append(where + ": `with` equals `find` — the removal would not change the file")
            continue
        target = os.path.join(root, entry["file"])
        if not os.path.isfile(target):
            problems.append(where + ": " + entry["file"] + " does not exist")
            continue
        count = ledger.read(target).count(entry["find"])
        if count != 1:
            problems.append(where + ": `find` occurs " + str(count) + " times in " + entry["file"] + ", not once")
        if not git_clean(root, entry["file"]):
            problems.append(where + ": " + entry["file"] + " has uncommitted changes — commit or stash them first")
    if problems:
        raise PlanError("\n".join(problems))
    return plan


def runners(config: dict) -> list:
    block = config.get("falsify") or {}
    found = block.get("runners") or []
    if not found:
        raise PlanError("scripts/ledger.config.json has no falsify.runners — say how to run a list of test files")
    for runner in found:
        command = str(runner.get("command") or "")
        if "{files}" not in command:
            raise PlanError("a falsify runner's command needs a `{files}` placeholder: " + json.dumps(runner))
        if re.search(r"<[^>]+>", command):
            raise PlanError("a falsify runner is still the template's placeholder — set it in scripts/ledger.config.json: " + command)
    return found


def package_of(root: str, rel: str) -> str:
    """The nearest directory above `rel` holding a package manifest, relative to the root."""
    here = os.path.dirname(rel)
    while here:
        if any(os.path.exists(os.path.join(root, here, m)) for m in PACKAGE_MARKERS):
            return here
        here = os.path.dirname(here)
    return ""


def group(root: str, config: dict, files) -> list:
    """(runner index, working directory, [files relative to it]) — one test run each."""
    table = runners(config)
    groups: dict = {}
    for rel in sorted(set(files)):
        for index, runner in enumerate(table):
            if any(ledger.glob_regex(p).match(rel) for p in (runner.get("match") or ["**"])):
                cwd = package_of(root, rel) if runner.get("cwd") == "package" else ""
                inner = os.path.relpath(rel, cwd) if cwd else rel
                groups.setdefault((index, cwd), []).append(inner.replace(os.sep, "/"))
                break
        else:
            raise PlanError(rel + " matches no falsify runner")
    return [(index, cwd, names) for (index, cwd), names in sorted(groups.items())]


def run(root: str, config: dict, index: int, cwd: str, files: list) -> str:
    """`pass`, `fail` or `timeout` for one run of one group."""
    runner = runners(config)[index]
    command = runner["command"].replace("{files}", " ".join(shlex.quote(f) for f in files))
    timeout = float((config.get("falsify") or {}).get("timeout_seconds") or 0) or None
    try:
        done = subprocess.run(command, shell=True, cwd=os.path.join(root, cwd) if cwd else root,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "timeout"
    return "pass" if done.returncode == 0 else "fail"


class Restorer:
    """Holds every original, and puts each back — on exit, on error, and on a signal."""

    def __init__(self):
        self.originals: dict = {}

    def replace(self, path: str, find: str, with_: str) -> None:
        text = ledger.read(path)
        self.originals.setdefault(path, text)
        changed = text.replace(find, with_, 1)
        if changed == text:
            raise PlanError(path + ": the removal did not change the file")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(changed)

    def restore(self) -> None:
        for path, text in self.originals.items():
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
        self.originals.clear()


def falsify(root: str, config: dict, plan: list, dry_run: bool = False, say=print) -> list:
    """One row per control: (control, file, tests run, result)."""
    ids = sorted({i for entry in plan for i in entry["expect"]})
    annotated = ledger.annotated_files(root, config, ids)
    missing = [i for i in ids if i not in annotated]
    if missing:
        raise PlanError("no annotated test file names " + ", ".join(missing) + " — there would be nothing to run")
    per_control = []
    for entry in plan:
        files = sorted({f for i in entry["expect"] for f in annotated[i]})
        per_control.append((entry, group(root, config, files)))

    every_group = sorted({(i, c, tuple(f)) for _e, groups in per_control for i, c, f in groups})
    if dry_run:
        for entry, groups in per_control:
            say("- " + entry["control"] + " — " + entry["file"] + " — " + str(sum(len(f) for _i, _c, f in groups)) + " test files")
            for index, cwd, files in groups:
                say("    runner " + str(index) + (" in " + cwd if cwd else "") + ": " + " ".join(files))
        return []

    say("baseline: " + str(len(every_group)) + " runs, nothing removed")
    baseline = {g: run(root, config, g[0], g[1], list(g[2])) for g in every_group}
    red = [g for g, result in baseline.items() if result != "pass"]
    for g in red:
        say("  unreliable: " + " ".join(g[2]) + " is already " + baseline[g] + " with nothing removed")

    restorer = Restorer()
    previous = {sig: signal.getsignal(sig) for sig in (signal.SIGINT, signal.SIGTERM)}

    def interrupted(signum, _frame):
        restorer.restore()
        raise KeyboardInterrupt

    for sig in previous:
        signal.signal(sig, interrupted)
    rows = []
    try:
        for entry, groups in per_control:
            started = time.time()
            restorer.replace(os.path.join(root, entry["file"]), entry["find"], entry["with"])
            results = []
            try:
                for index, cwd, files in groups:
                    key = (index, cwd, tuple(files))
                    results.append("unreliable" if key in red else run(root, config, index, cwd, files))
            finally:
                restorer.restore()
            if "fail" in results:
                verdict = "caught"
            elif "timeout" in results:
                verdict = "timeout"
            elif all(r == "unreliable" for r in results):
                verdict = "unreliable"
            else:
                verdict = "**survived**"
            tests = ", ".join("`" + os.path.join(c, f).replace(os.sep, "/") + "`" for _i, c, fs in groups for f in fs)
            rows.append((entry["control"], entry["file"], tests, verdict))
            say("  " + verdict.strip("*").ljust(10) + " " + entry["control"] + " (" + str(round(time.time() - started, 1)) + "s)")
    finally:
        restorer.restore()
        for sig, handler in previous.items():
            signal.signal(sig, handler)
    return rows


def table(rows: list) -> str:
    out = ["| Control removed | From | Tests run | Result |", "|---|---|---|---|"]
    for control, where, tests, verdict in rows:
        out.append("| " + ledger.escape(control) + " | `" + where + "` | " + tests + " | " + verdict + " |")
    return "\n".join(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("plan", help="the slice's .falsify.json")
    parser.add_argument("--root", default=os.path.dirname(HERE), help="repository root")
    parser.add_argument("--config", default="scripts/ledger.config.json")
    parser.add_argument("--dry-run", action="store_true", help="validate and list, remove nothing")
    args = parser.parse_args(argv)
    root = os.path.abspath(args.root)
    config = ledger.load_config(root, args.config)
    plan_path = args.plan if os.path.isabs(args.plan) else os.path.join(root, args.plan)
    try:
        plan = load_plan(root, plan_path)
        rows = falsify(root, config, plan, dry_run=args.dry_run)
    except PlanError as err:
        print("error: " + str(err).replace("\n", "\nerror: "), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("interrupted — every file was restored", file=sys.stderr)
        return 130
    if rows:
        survived = [r for r in rows if "survived" in r[3]]
        print()
        print(table(rows))
        print()
        print(str(len(rows)) + " controls · " + str(len(survived)) + " survived"
              + (" — each is a missing test or a control that does nothing" if survived else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
