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


def repository_root(start: str = None) -> str:
    """The top of the git repository `start` (default: the current directory) is in, or `None`.
    Never the repository this file sits in — run as `python3 ../elsewhere/scripts/falsify.py`, using
    *elsewhere* would be silently wrong."""
    done = subprocess.run(["git", "-C", start or os.getcwd(), "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 else None


NOT_A_REPOSITORY = "not a git repository — run it inside one, or pass --root <repository>"


TEMPLATE_PLACEHOLDER = re.compile(r"<[A-Za-z][A-Za-z ,/-]*[A-Za-z]>")


class PlanError(Exception):
    pass


def git_clean(root: str, rel: str) -> bool:
    """No uncommitted change to `rel`, staged or not. `main` has already refused a root outside a
    repository, so a failing `git status` here is a reason to refuse, never to wave the file through."""
    # `:(literal)`: a pathspec is a glob to git, so `app/[id]/page.tsx` would name `app/i/page.tsx`
    # and the rest of its class — and a clean answer about those files is no answer about this one.
    done = subprocess.run(["git", "-C", root, "status", "--porcelain", "--", ":(literal)" + rel],
                          capture_output=True, text=True)
    return done.returncode == 0 and not done.stdout.strip()


def raw(path: str) -> str:
    """The file exactly as it is on disk — `ledger.read` folds CRLF into LF, and a file restored
    from that would stay modified after the run."""
    with open(path, "rb") as handle:
        return handle.read().decode("utf-8")


def in_its_line_endings(text: str, snippet: str) -> str:
    """`snippet`, as a plan writes it (with LF line breaks), in the line endings of `text` — in a
    CRLF file, a `find` that spans a line break with LF alone would never occur."""
    if "\r\n" in text and "\r" not in snippet:
        return snippet.replace("\n", "\r\n")
    return snippet


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
        if not isinstance(entry, dict):
            problems.append("control " + str(n) + ": each control is a JSON object — {\"control\", \"file\", \"find\", \"expect\"}")
            continue
        where = "control " + str(n) + " (" + str(entry.get("control") or "unnamed") + ")"
        # One requirement written as a string is a list of one, not a list of its characters.
        if isinstance(entry.get("expect"), str):
            entry["expect"] = [entry["expect"]]
        for key in ("control", "file", "find", "expect"):
            if not entry.get(key):
                problems.append(where + ": needs `" + key + "`")
        if problems and problems[-1].startswith(where):
            continue
        entry.setdefault("with", "")
        if not isinstance(entry["expect"], list) or not all(isinstance(i, str) and i for i in entry["expect"]):
            problems.append(where + ": `expect` is a list of requirement identifiers")
            continue
        if not all(isinstance(entry[k], str) for k in ("file", "find", "with")):
            problems.append(where + ": `file`, `find` and `with` are strings")
            continue
        if entry["find"] == entry["with"]:
            problems.append(where + ": `with` equals `find` — the removal would not change the file")
            continue
        target = os.path.join(root, entry["file"])
        if not os.path.isfile(target):
            problems.append(where + ": " + entry["file"] + " does not exist")
            continue
        text = raw(target)
        count = text.count(in_its_line_endings(text, entry["find"]))
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
        # Only the template's own shape — `<unit test command, run on a list of files>`: words
        # against both brackets. A shell redirection has a space or a digit at one of its ends
        # (`< fixtures.txt`, `>out.log 2>&1`), and refusing it would refuse a working command.
        if TEMPLATE_PLACEHOLDER.search(command):
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
    # A session of its own, so the whole tree can be stopped: with `shell=True` the child is
    # `/bin/sh`, and killing only that leaves the test runner it started still running — against
    # the removed code, and on into the next control's run.
    process = subprocess.Popen(command, shell=True, cwd=os.path.join(root, cwd) if cwd else root,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               start_new_session=hasattr(os, "killpg"))
    try:
        returncode = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        stop(process)
        return "timeout"
    except BaseException:
        # Ctrl-C or a signal: the runner is in another session, so the terminal's SIGINT never
        # reached it. Stopped here, or it outlives the run it belonged to.
        stop(process)
        raise
    return "pass" if returncode == 0 else "fail"


def stop(process) -> None:
    """Kill a runner and everything it started, and wait for it."""
    try:
        if hasattr(os, "killpg"):
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
    except (ProcessLookupError, PermissionError):
        pass  # already gone
    process.wait()


class Restorer:
    """Holds every original, and puts each back — on exit, on error, and on a signal."""

    def __init__(self):
        self.originals: dict = {}

    def replace(self, path: str, find: str, with_: str) -> None:
        # Bytes in, bytes back: the original is kept exactly as read, and the edit is made in the
        # file's own line endings, so a restored file is the committed file and `git status` is
        # clean after the run.
        with open(path, "rb") as handle:
            original = handle.read()
        self.originals.setdefault(path, original)
        text = original.decode("utf-8")
        changed = text.replace(in_its_line_endings(text, find), in_its_line_endings(text, with_), 1)
        if changed == text:
            raise PlanError(path + ": the removal did not change the file")
        with open(path, "wb") as handle:
            handle.write(changed.encode("utf-8"))

    def restore(self) -> None:
        for path, original in self.originals.items():
            with open(path, "wb") as handle:
                handle.write(original)
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
    # SIGHUP too: a closed terminal or a dropped SSH session is the likeliest way a long run ends
    # early, and its default is to exit on the spot with the control still removed.
    handled = [getattr(signal, name) for name in ("SIGINT", "SIGTERM", "SIGHUP") if hasattr(signal, name)]
    previous = {sig: signal.getsignal(sig) for sig in handled}

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
    parser.add_argument("--root", default=None, help="repository root (default: the git repository of the current directory)")
    parser.add_argument("--config", default="scripts/ledger.config.json")
    parser.add_argument("--dry-run", action="store_true", help="validate and list, remove nothing")
    args = parser.parse_args(argv)
    # The dirty-file refusal is what keeps a restore from destroying unsaved work, and only git can
    # answer it. Outside a repository the tool would have to remove code it cannot prove is safe to
    # put back, so it does not start.
    root = repository_root(os.path.abspath(args.root) if args.root else None)
    if root is None:
        print("error: " + NOT_A_REPOSITORY, file=sys.stderr)
        return 1
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
