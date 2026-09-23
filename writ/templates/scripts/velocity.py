#!/usr/bin/env python3
"""How fast this repository is moving, measured from git, and whether it has slowed down.

    python3 scripts/velocity.py                 # every merge on the current branch, then by week
    python3 scripts/velocity.py --diff dev      # what this branch adds against dev (slice close)
    python3 scripts/velocity.py --check         # exit 1 when a threshold in the config trips

Every first-parent commit is one merge, measured on one ruler:

  - **code** — added lines outside tests, comments, blank lines and generated files. The ruler
    `DEVELOPMENT-PROCESS.md` §2.1 describes, recovered from history so nobody has to record it.
  - **test** — added lines in test files.
  - **md** — added Markdown lines: what the change cost to write down.
  - **slice** — the `Slice:` line `/slice-close` writes into the commit message, if there is one.

**Why `git show -U0` and not `--numstat`.** numstat cannot see which added lines are comments or
blanks, and those are a fifth of a typical source diff. Counting them is the mis-measurement both
projects this was built from made first and then corrected.

**What it flags**, from the `velocity` block of `scripts/ledger.config.json`:

  - *Throughput dropped* — the last complete week added less than `drop_ratio` of the code the
    `trailing_weeks` before it averaged. Code per week is the number that fell five-fold on a real
    project while every individual slice still looked fine.
  - *Ceremony grew* — across the last `ceremony_slices` slice merges, Markdown lines per code line
    exceeded `max_md_per_code`. A per-slice document cost that stays fixed while slices shrink is
    how the process starts to cost more than the work.

A flag is a reason to look, not a verdict: a holiday week trips the first and a documentation-heavy
milestone the second. That is why `--check` belongs in `/maintenance`, never in the gate — failing a
merge on it would only teach people to raise the threshold.

Standard library only, Python 3.9+, like `ledger.py`.
"""

from __future__ import annotations

import argparse
import collections
import datetime
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ledger import glob_regex  # noqa: E402 — one matcher for every tool here, so they cannot drift


def repository_root() -> str:
    """The git repository the command was run from — never the one this file sits in. Run as
    `python3 ../elsewhere/scripts/velocity.py`, measuring *elsewhere* would be silently wrong."""
    done = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 else os.getcwd()

DEFAULTS = {
    # Files whose added lines measure their generator rather than the work. The ledger's own
    # outputs are added from the config at load time.
    "generated": [
        "**/package-lock.json", "**/pnpm-lock.yaml", "**/yarn.lock", "**/poetry.lock", "**/uv.lock",
        "**/Cargo.lock", "**/go.sum", "**/*.snap", "**/__snapshots__/**", "**/openapi.json",
    ],
    # Test files, on top of the ledger's `tests.globs`.
    "tests": [
        "**/test/**", "**/tests/**", "**/__tests__/**", "**/*.test.*", "**/*.spec.*",
        "**/test_*.py", "**/*_test.py", "**/*_test.go",
    ],
    "trailing_weeks": 3,
    "drop_ratio": 0.5,
    "ceremony_slices": 5,
    "max_md_per_code": 1.0,
}

CODE_EXT = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py", ".go", ".rs", ".rb", ".java", ".kt", ".cs",
    ".swift", ".php", ".sql", ".sh", ".css", ".scss", ".html", ".vue", ".svelte", ".yml", ".yaml",
    ".json", ".toml",
}
C_LIKE = ("//", "/*", "*", "*/")
COMMENT = {ext: C_LIKE for ext in (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".go", ".rs", ".java",
                                   ".kt", ".cs", ".swift", ".php", ".css", ".scss")}
COMMENT.update({ext: ("#",) for ext in (".py", ".rb", ".sh", ".yml", ".yaml", ".toml")})
COMMENT.update({".sql": ("--",), ".html": ("<!--",), ".vue": ("<!--", "//"), ".svelte": ("<!--", "//")})


def load_settings(root: str) -> dict:
    """`DEFAULTS`, overlaid with the config's `velocity` block and its test globs and outputs."""
    settings = {k: (list(v) if isinstance(v, list) else v) for k, v in DEFAULTS.items()}
    try:
        with open(os.path.join(root, "scripts", "ledger.config.json"), encoding="utf-8") as handle:
            config = json.load(handle)
    except (OSError, ValueError):
        config = {}
    block = config.get("velocity") or {}
    for key, value in block.items():
        if key in ("generated", "tests"):
            settings[key] = settings[key] + list(value)
        else:
            settings[key] = value
    settings["tests"] += list((config.get("tests") or {}).get("globs") or [])
    settings["generated"] += [config[k] for k in ("coverage_out", "queue_out", "index_out") if config.get(k)]
    return settings


class Ruler:
    def __init__(self, settings: dict):
        self.generated = [glob_regex(p) for p in settings["generated"]]
        self.tests = [glob_regex(p) for p in settings["tests"]]

    def measure(self, patch: str) -> dict:
        """Added lines by kind, from a `-U0` patch."""
        tally = {"code": 0, "test": 0, "md": 0, "files": 0}
        path, ext, kind = None, "", None
        for line in patch.splitlines():
            if line.startswith("+++ "):
                path = line[6:] if line.startswith("+++ b/") else None
                if path is None:
                    kind = None
                    continue
                tally["files"] += 1
                ext = os.path.splitext(path)[1].lower()
                if any(r.match(path) for r in self.generated):
                    kind = None
                elif ext in (".md", ".mdx"):
                    kind = "md"
                elif any(r.match(path) for r in self.tests):
                    kind = "test"
                elif ext in CODE_EXT:
                    kind = "code"
                else:
                    kind = None
                continue
            if kind is None or not line.startswith("+") or line.startswith("+++"):
                continue
            body = line[1:].strip()
            if not body:
                continue
            if kind == "code" and body.startswith(COMMENT.get(ext, ())):
                continue
            tally[kind] += 1
        return tally


def git(root: str, *args: str) -> str:
    done = subprocess.run(["git", "-C", root, *args], capture_output=True, check=True)
    return done.stdout.decode("utf-8", errors="replace")


Merge = collections.namedtuple("Merge", "sha date slice subject code test md files")

SEP, END = "\x1f", "\x1e"
# The `Slice:` line `/slice-close` writes. Read from the body rather than as a git trailer, because
# the commit ends with `Closes #N` in a paragraph of its own and git parses trailers only from the
# last paragraph — every slice would read as not one.
SLICE_LINE = re.compile(r"^Slice:\s*(\S+)", re.M)


def merges(root: str, ruler: Ruler, branch: str = "HEAD", since: str = "") -> list:
    """Every first-parent commit on `branch`, oldest first, measured."""
    fmt = SEP.join(["%h", "%ad", "%s", "%b"]) + END
    args = ["log", "--first-parent", "--reverse", "--date=short", "--pretty=format:" + fmt]
    if since:
        args.append("--since=" + since)
    out = []
    for record in git(root, *args, branch).split(END):
        if not record.strip():
            continue
        sha, date, subject, body = record.lstrip("\n").split(SEP, 3)
        found = SLICE_LINE.search(body)
        # `--first-parent` on a merge commit diffs against the first parent: what the merge added.
        patch = git(root, "show", sha, "-U0", "--format=", "--no-color", "--first-parent", "--no-renames")
        tally = ruler.measure(patch)
        out.append(Merge(sha, date, found.group(1) if found else "", subject,
                         tally["code"], tally["test"], tally["md"], tally["files"]))
    return out


def week_of(date: str) -> tuple:
    year, week, _ = datetime.date.fromisoformat(date).isocalendar()
    return year, week


def weekly(rows: list, today: datetime.date) -> list:
    """(week label, merges, slices, code, md) for every ISO week from the first merge to the last
    **complete** week, with empty weeks included — a week nothing merged is the loudest signal."""
    if not rows:
        return []
    buckets = collections.defaultdict(lambda: [0, 0, 0, 0])
    for row in rows:
        bucket = buckets[week_of(row.date)]
        bucket[0] += 1
        bucket[1] += 1 if row.slice else 0
        bucket[2] += row.code
        bucket[3] += row.md
    start = datetime.date.fromisoformat(rows[0].date)
    start -= datetime.timedelta(days=start.weekday())
    this_week = today - datetime.timedelta(days=today.weekday())
    out = []
    day = start
    while day < this_week:
        key = week_of(day.isoformat())
        n, s, c, m = buckets.get(key, [0, 0, 0, 0])
        out.append(("%d-W%02d" % key, n, s, c, m))
        day += datetime.timedelta(days=7)
    return out


def flags(rows: list, weeks: list, settings: dict) -> list:
    """The thresholds that tripped, each as one sentence a reader can act on."""
    found = []
    trailing = int(settings["trailing_weeks"])
    ratio = float(settings["drop_ratio"])
    if trailing and ratio and len(weeks) > trailing:
        last = weeks[-1]
        before = weeks[-1 - trailing:-1]
        mean = sum(w[3] for w in before) / trailing
        if mean and last[3] < ratio * mean:
            found.append(
                "throughput dropped: %s added %d code lines against a %d-week average of %d (below %d%%)"
                % (last[0], last[3], trailing, mean, ratio * 100)
            )
    count = int(settings["ceremony_slices"])
    ceiling = float(settings["max_md_per_code"])
    slices = [r for r in rows if r.slice]
    if count and ceiling and len(slices) >= count:
        recent = slices[-count:]
        code = sum(r.code for r in recent)
        md = sum(r.md for r in recent)
        if md > ceiling * max(code, 1):
            found.append(
                "ceremony grew: the last %d slices added %d Markdown lines for %d code lines (%.2f per code line, ceiling %.2f)"
                % (count, md, code, md / max(code, 1), ceiling)
            )
    return found


def summary(root: str, today: datetime.date = None) -> list:
    """A few lines for `ledger.py stats`. Empty outside a git repository — stats never fails."""
    try:
        settings = load_settings(root)
        rows = merges(root, Ruler(settings))
    except (OSError, subprocess.CalledProcessError, ValueError):
        return []
    if not rows:
        return []
    weeks = weekly(rows, today or datetime.date.today())
    slices = [r for r in rows if r.slice]
    out = ["Velocity — " + str(len(rows)) + " merges, " + str(len(slices)) + " of them slices"]
    for label, n, s, c, m in weeks[-4:]:
        out.append("  " + label + "  " + str(s).rjust(2) + " slices  " + str(c).rjust(6) + " code  " + str(m).rjust(6) + " md")
    for flag in flags(rows, weeks, settings):
        out.append("  ⚑ " + flag)
    return out


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root", default=None, help="repository root (default: the git repository of the current directory)")
    parser.add_argument("--branch", default="HEAD")
    parser.add_argument("--since", default="", help="YYYY-MM-DD")
    parser.add_argument("--diff", metavar="BASE", help="measure what this branch adds against BASE, and stop")
    parser.add_argument("--last", type=int, default=0, help="list only the last N merges")
    parser.add_argument("--check", action="store_true", help="exit 1 when a threshold trips")
    parser.add_argument("--today", default="", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    root = os.path.abspath(args.root or repository_root())
    settings = load_settings(root)
    ruler = Ruler(settings)

    if args.diff:
        tally = ruler.measure(git(root, "diff", args.diff + "...HEAD", "-U0", "--no-color", "--no-renames"))
        print("code %d · test %d · md %d · files %d  (against %s)" % (tally["code"], tally["test"], tally["md"], tally["files"], args.diff))
        return 0

    rows = merges(root, ruler, args.branch, args.since)
    today = datetime.date.fromisoformat(args.today) if args.today else datetime.date.today()
    weeks = weekly(rows, today)
    shown = rows[-args.last:] if args.last else rows
    print("%-11s%-10s%-9s%7s%7s%7s  %s" % ("date", "sha", "slice", "code", "test", "md", "subject"))
    for r in shown:
        print("%-11s%-10s%-9s%7d%7d%7d  %s" % (r.date, r.sha, r.slice or "—", r.code, r.test, r.md, r.subject[:60]))
    if weeks and not args.last:
        print("\nweek       merges slices   code     md  md/code")
        for label, n, s, c, m in weeks:
            print("%-10s %6d %6d %6d %6d  %6.2f" % (label, n, s, c, m, m / max(c, 1)))
    tripped = flags(rows, weeks, settings)
    print()
    for flag in tripped:
        print("⚑ " + flag)
    if not tripped:
        print("no velocity threshold tripped")
    return 1 if (args.check and tripped) else 0


if __name__ == "__main__":
    sys.exit(main())
