#!/usr/bin/env python3
"""Read an existing codebase's shape out of its git history.

    python3 scripts/survey.py                  the whole report
    python3 scripts/survey.py --since 18       months of history to read (default 24)
    python3 scripts/survey.py --top 20         how many rows per section (default 12)
    python3 scripts/survey.py --json           the same findings, for a tool rather than a person

**This is an input to an interview, not a substitute for one.** Everything here is a question
worth asking, and none of it is an answer. A file changed ninety times is not thereby important;
it may be a configuration file somebody keeps bumping. Two files that always change together are
not thereby coupled; they may both be touched by the formatter. What the report does is stop the
survey starting from whoever happens to be in the room and what they happen to remember.

Why history rather than source: an agent reads source well and reads history not at all, because
it is not in the working tree. The facts here are the ones the code cannot state about itself —
what is churning, what is dead, what moves together, and who is the only person who has ever
touched a directory. Those are the questions a brownfield survey is made of.

Stdlib only, Python 3.9+, and it writes nothing. `git` is the single dependency.
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
import subprocess
import sys

# Extensions worth counting as source. Deliberately short: the point is proportion between areas,
# and a list that tries to be exhaustive goes stale in a way a list that does not try never does.
SOURCE = (
    ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".rb", ".java", ".kt", ".cs",
    ".php", ".swift", ".scala", ".ex", ".exs", ".c", ".h", ".cc", ".cpp", ".hpp", ".sql",
)
# Paths that say nothing about the shape of the product.
NOISE = re.compile(
    r"(^|/)(node_modules|vendor|dist|build|target|\.venv|venv|__pycache__|\.git|"
    r"coverage|\.next|\.turbo|third_party)(/|$)"
)
# A directory called `tests`, or a filename that opens or closes with `test`/`spec` against a
# separator. `/` counts as a separator: `scripts/test_ledger.py` is a test file, and leaving it
# out made every Python project report that it had none.
TESTISH = re.compile(
    r"(^|/)(tests?|spec|specs|__tests__)(/|$)"
    r"|(^|[/._-])(test|spec)s?[._-]"
    r"|[._-](test|spec)s?(\.[A-Za-z0-9]+)*$"
)


def git(root: str, *args) -> str:
    try:
        done = subprocess.run(
            ["git", "-C", root] + list(args), capture_output=True, text=True, check=False
        )
    except FileNotFoundError:
        raise SystemExit("survey.py needs git on PATH")
    if done.returncode:
        raise SystemExit("git " + " ".join(args) + " failed: " + done.stderr.strip())
    return done.stdout


def commits(root: str, months: int) -> list:
    """Every commit in the window, as (author, date, [paths]).

    Merges are excluded. A merge's file list is the union of everything it brought in, which would
    make every branch look like one enormous simultaneous change and destroy the coupling signal
    entirely."""
    raw = git(
        root, "log", "--no-merges", "--since=" + str(months) + " months ago",
        "--name-only", "--format=%x01%an%x09%ad", "--date=short",
    )
    out = []
    for block in raw.split("\x01"):
        if not block.strip():
            continue
        head, _, rest = block.partition("\n")
        author, _, day = head.partition("\t")
        files = [f for f in rest.split("\n") if f.strip() and not NOISE.search(f)]
        if files:
            out.append((author.strip(), day.strip(), files))
    return out


def tracked(root: str) -> list:
    return [f for f in git(root, "ls-files").split("\n") if f.strip() and not NOISE.search(f)]


def area_of(path: str, depth: int = 2) -> str:
    """The directory a file belongs to, at a fixed depth.

    Two levels rather than one because one level is usually `src`, which tells nobody anything,
    and three is usually a single file's own folder."""
    parts = path.split("/")[:-1]
    if not parts:
        return "(root)"
    return "/".join(parts[:depth])


def is_source(path: str) -> bool:
    return path.endswith(SOURCE)


def is_test(path: str) -> bool:
    return is_source(path) and bool(TESTISH.search(path))


def survey(root: str, months: int, top: int) -> dict:
    log = commits(root, months)
    files = tracked(root)

    touches = collections.Counter()
    authors = collections.defaultdict(set)
    last_seen = {}
    together = collections.Counter()
    for author, day, changed in log:
        here = [f for f in changed if is_source(f)]
        for path in here:
            touches[path] += 1
            authors[area_of(path)].add(author)
            if path not in last_seen or day > last_seen[path]:
                last_seen[path] = day
        # A commit touching half the repository is a rename, a format or a dependency bump, and it
        # would swamp every genuine pair. Ten is the point past which the signal is gone.
        if 2 <= len(here) <= 10:
            ordered = sorted(set(here))
            for i, one in enumerate(ordered):
                for other in ordered[i + 1:]:
                    together[(one, other)] += 1

    areas = {}
    for path in files:
        if not is_source(path):
            continue
        row = areas.setdefault(area_of(path), {"files": 0, "tests": 0, "changes": 0, "hands": 0})
        row["files"] += 1
        row["tests"] += 1 if is_test(path) else 0
        row["changes"] += touches.get(path, 0)
    for name, row in areas.items():
        row["hands"] = len(authors.get(name, ()))

    quiet = [
        path for path in files
        if is_source(path) and not is_test(path) and path not in last_seen
    ]

    return {
        "window_months": months,
        "commits": len(log),
        "source_files": len([f for f in files if is_source(f)]),
        "test_files": len([f for f in files if is_test(f)]),
        "areas": dict(sorted(areas.items(), key=lambda kv: -kv[1]["changes"])),
        "hotspots": [
            {"path": p, "changes": n, "tested": is_test(p) or bool(near_test(p, files))}
            for p, n in touches.most_common(top)
        ],
        "coupled": [
            {"a": a, "b": b, "together": n}
            for (a, b), n in together.most_common(top)
            if n >= 3
        ],
        "quiet": sorted(quiet)[:top],
        "quiet_total": len(quiet),
        "hands": {
            name: sorted(who) for name, who in sorted(authors.items(), key=lambda kv: len(kv[1]))
            if len(who) == 1
        },
    }


def near_test(path: str, files: list) -> bool:
    """Whether anything test-shaped names the same stem. A weak signal, honestly labelled: it is
    the difference between *there is probably something* and *there is certainly nothing*."""
    stem = os.path.splitext(os.path.basename(path))[0]
    if not stem:
        return False
    return any(is_test(f) and stem in os.path.basename(f) for f in files)


def render(data: dict) -> str:
    out = [
        "Survey — " + str(data["commits"]) + " commits over " + str(data["window_months"])
        + " months, " + str(data["source_files"]) + " source files, "
        + str(data["test_files"]) + " of them tests",
        "",
    ]

    out.append("Areas — by how much they move")
    out.append("  " + "area".ljust(34) + "files  tests  changes  hands")
    for name, row in list(data["areas"].items())[:14]:
        out.append(
            "  " + name.ljust(34) + str(row["files"]).rjust(5) + str(row["tests"]).rjust(7)
            + str(row["changes"]).rjust(9) + str(row["hands"]).rjust(7)
        )
    out += [
        "",
        "  These are the candidate requirement areas, and the order is the order to survey them",
        "  in. An area with many changes and few tests is where both the risk and the return are.",
        "",
    ]

    if data["hotspots"]:
        out.append("Hotspots — the files that keep changing")
        for row in data["hotspots"]:
            out.append(
                "  " + str(row["changes"]).rjust(4) + "  " + row["path"]
                + ("" if row["tested"] else "   (nothing test-shaped names it)")
            )
        out += [
            "",
            "  A file changed this often is one somebody is still working out. Ask what keeps",
            "  bringing people back to it — the answer is usually a requirement nobody wrote down.",
            "",
        ]

    if data["coupled"]:
        out.append("Coupled — changed together, and the code may not say why")
        for row in data["coupled"]:
            out.append("  " + str(row["together"]).rjust(4) + "  " + row["a"] + "\n        " + row["b"])
        out += [
            "",
            "  Two files that always move together either belong to one area or share a rule",
            "  neither states. The second is an invariant, and this is the cheapest way to find one.",
            "",
        ]

    if data["quiet"]:
        out.append(
            "Quiet — " + str(data["quiet_total"]) + " source files untouched in the window"
        )
        for path in data["quiet"]:
            out.append("  " + path)
        out += [
            "",
            "  Candidates for dead, not evidence of it. **Ask before believing any of it**: stable",
            "  and abandoned look identical in a log. What an agent cannot tell from the source is",
            "  which of these is still called, and that is exactly what the survey must write down.",
            "",
        ]

    if data["hands"]:
        out.append("One pair of hands — areas only one person has touched")
        for name, who in list(data["hands"].items())[:10]:
            out.append("  " + name.ljust(34) + who[0])
        out += [
            "",
            "  Where the undocumented knowledge is, and who to interview for it. Also the answer to",
            "  which colleague to bring into the process second: the one who owns an area alone.",
            "",
        ]

    out += [
        "Next — none of this is a finding until somebody confirms it",
        "  1. Take the area table to the interview. Confirm the boundaries and the names.",
        "  2. Ask what each hotspot keeps being changed for.",
        "  3. Ask, for each coupled pair, what rule holds them together. Those become `INV-*`.",
        "  4. Ask which quiet files are dead. Dead code deleted is the cheapest slice there is.",
        "  5. Write what is *wrong* into `canon/spec/debt.md` before writing what is required.",
        "",
    ]
    return "\n".join(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Read a codebase's shape out of its git history.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--since", type=int, default=24, help="months of history (default 24)")
    parser.add_argument("--top", type=int, default=12, help="rows per section (default 12)")
    parser.add_argument("--json", action="store_true", help="findings as JSON")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    if not os.path.isdir(os.path.join(root, ".git")):
        sys.stderr.write("not a git repository: " + root + "\n")
        return 1

    data = survey(root, args.since, args.top)
    if not data["commits"]:
        sys.stderr.write(
            "no commits in the last " + str(args.since) + " months — widen the window with --since\n"
        )
        return 1
    sys.stdout.write(json.dumps(data, indent=2) + "\n" if args.json else render(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
