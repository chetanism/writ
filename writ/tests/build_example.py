#!/usr/bin/env python3
"""The worked example: one small product's tree, and what the tool actually prints about it.

    python3 writ/tests/build_example.py           # regenerate writ/docs/example/
    python3 writ/tests/build_example.py --check   # fail if the committed copy has drifted

Every template in this kit ships full of `<placeholders>`, which is correct — inventing a
requirement is the interview's job — but it means the only way to see a filled-in tree was to run
a ten-phase interview. So the one claim the kit leads with, that a tool reads the tree and reports
only what is backed by evidence, was the one thing a reader could not look at.

This builds that tree for a product small enough to hold in your head, and copies both the
*sources* a person writes and the *artefacts* the tool generates into `writ/docs/example/`.

**The example is generated, and CI regenerates it.** A worked example pasted into a document by
hand is a second description of the tool's behaviour, immediately less true than the tool and
maintained by nobody — which is the failure this whole process is shaped around. Committing one
would have been the most embarrassing possible way to illustrate it. So `--check` rebuilds and
diffs, and the kit's gate runs it.

The product is a lending library for an office bookshelf. It is deliberately dull. The interesting
thing is not the product but the four coverage states it manages to exhibit in five requirements:

    FR-LEND-01   claimed by a slice, and a test names it          -> satisfied
    FR-LEND-02   claimed by the same slice, no test names it      -> partial   (the honest one)
    INV-001      a test names it, no slice ever claimed it        -> inherited
    FR-LEND-03   queued, not started                              -> none
    NFR-AUD-01   written down, nobody has touched it              -> none

`FR-LEND-02` is the row that matters. The work order says the slice satisfied it; the ledger does
not believe work orders, so it reports it as partial and lists it under "Claimed without proof".
"""

from __future__ import annotations

import contextlib
import difflib
import json
import importlib.util
import io
import os
import shutil
import sys
import tempfile

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(KIT, "docs", "example")

_spec = importlib.util.spec_from_file_location("tt", os.path.join(KIT, "tests", "test_templates.py"))
tt = importlib.util.module_from_spec(_spec)
sys.modules["tt"] = tt
_spec.loader.exec_module(tt)


# --------------------------------------------------------------------------------------------
# The product
# --------------------------------------------------------------------------------------------

LENDING = """# FR-LEND — Lending

The requirements of one area, one row each. This table is the only place an `FR-LEND-*` comes
into existence; the generated index and the coverage ledger both read it, and neither is edited.

| ID | Requirement | Target | Since | Status |
|---|---|---|---|---|
| FR-LEND-01 | Somebody can borrow a copy that is on the shelf. | M1 | v0.1 | active |
| FR-LEND-02 | Somebody can return a copy they borrowed. | M1 | v0.1 | active |
| FR-LEND-03 | Somebody can join the queue for a copy that is out. | M1 | v0.1 | active |
"""

AUDIT = """# NFR-AUD — Auditability

| ID | Requirement | Target | Since | Status |
|---|---|---|---|---|
| NFR-AUD-01 | Every borrow and return is attributable to a person and a time. | M1 | v0.1 | active |
"""

INVARIANTS = """# Invariants

The properties that must always hold, binding on every implementation. Violating one is a defect,
not a style preference. Name the layer that enforces each; an invariant enforced only by
convention is a hope.

| ID | Invariant | Enforced by | Since | Status |
|---|---|---|---|---|
| INV-001 | A copy is never on loan to two people at once. | a unique partial index on `loan(copy_id) where returned_at is null` | v0.1 | active |
"""

WORK_ORDER_001 = """---
id: SL-001
title: borrow and return a copy
phase: P01
kind: feature
size: S
estimated: 120
code_lines: 138
status: done
dep: "—"
owner: ""
issue: 14
depends_on: []
touches: []
satisfies: [FR-LEND-01, FR-LEND-02]
partial: []
adr: []
demo: script
---

# Slice SL-001 — borrow and return a copy

## Why this slice exists

The shelf is currently a paper sheet on the wall, and it is wrong within a week of anybody going
on holiday. Nobody can tell whether a book is out or simply missing, so people buy second copies
of books the office already owns. This slice is the smallest thing that makes the shelf's state
answerable: a copy is either out to a named person or it is not.

## Decisions this slice makes

A loan is a row with a null `returned_at` rather than a status column, so the invariant is a
unique partial index the database enforces, not a rule the application remembers to apply.

## Acceptance criteria

1. Borrowing a copy that is on the shelf records a loan against the borrower and the time.
2. Returning a copy the borrower holds clears the loan and puts the copy back on the shelf.
3. Borrowing a copy that is already out is refused, and says who holds it.

## Demo

`npm run demo:lending` borrows a copy as one person, shows the second borrow refused, returns it,
and shows the copy back on the shelf. Ninety seconds.
"""

WORK_ORDER_002 = """---
id: SL-002
title: queue for a copy that is out
phase: P01
kind: feature
size: S
estimated: 90
code_lines:
status: queued
dep: "—"
owner: ""
issue:
depends_on: [SL-001]
touches: []
satisfies: [FR-LEND-03]
partial: []
adr: []
demo: script
---

# Slice SL-002 — queue for a copy that is out

## Why this slice exists

Refusing a borrow is honest but useless: the person still wants the book, and the only way to get
it today is to keep asking. Without a queue the shelf rewards whoever checks most often.

## Decisions this slice makes

None yet. This work order is written and queued; the decisions are made at step 2 when it is
claimed.

## Acceptance criteria

1. Somebody refused a borrow can join the queue for that copy.
2. Returning a copy notifies the person at the head of its queue.

## Demo

`npm run demo:queue`, showing a refused borrow, a join, a return, and the notification.
"""

SUMMARY_001 = """# Slice SL-001 — summary

## What the system can do now that it could not before

The shelf knows who has what. Borrowing a copy records a loan against a person and a time,
returning it clears the loan, and a second borrow of a copy already out is refused rather than
silently accepted.

## How it works

`src/lending.ts` is the entry point. A loan is a row in `loan` with a null `returned_at`; the
invariant that a copy is never out twice is a unique partial index on that condition, so a
concurrent double borrow fails in the database rather than in a check the application might skip.

## Decisions made

| Decision | Chose | Over | Why | ADR |
|---|---|---|---|---|
| Representing an active loan | A null `returned_at` | A status column | The invariant becomes an index the database enforces | — |

## Deliberately not done

The queue. A refused borrow says who holds the copy and stops there; SL-002 is written and queued.

## What this cost

Estimated 120 added lines, measured 138. Within the S tier.
"""

TESTS = """import { describe, it, expect } from "vitest";
import { borrow, returnCopy, shelfState } from "./lending";

// The identifier in the test name is the whole mechanism. The ledger reads these names out of
// the suite; nothing else marks a requirement as proven, and no work order can talk it into it.

describe("lending", () => {
  it("[FR-LEND-01] lends a copy that is on the shelf to the person who asked", () => {
    const loan = borrow({ copy: "c1", person: "ana" });
    expect(loan.person).toBe("ana");
    expect(shelfState("c1")).toBe("out");
  });

  it("[INV-001] refuses a second borrow of a copy already out, naming the holder", () => {
    borrow({ copy: "c1", person: "ana" });
    expect(() => borrow({ copy: "c1", person: "ben" })).toThrow(/held by ana/);
  });
});
"""

# `returnCopy` is imported and never exercised, which is the point: FR-LEND-02 is claimed by the
# work order and proven by nothing. The ledger reports it as partial rather than taking the claim.

OVERLAY = {
    "writ/spec/requirements/FR-LEND/index.md": LENDING,
    "writ/spec/requirements/NFR-AUD/index.md": AUDIT,
    "writ/spec/invariants.md": INVARIANTS,
    "writ/process/work-orders/m1/P01/001.md": WORK_ORDER_001,
    "writ/process/work-orders/m1/P01/002.md": WORK_ORDER_002,
    "writ/process/slices/m1/P01/001.md": SUMMARY_001,
    "src/lending.test.ts": TESTS,
}

# Copied into the example directory. Sources first, then what the tool made of them.
SOURCES = [
    ("writ/spec/requirements/FR-LEND/index.md", "source-register.md"),
    ("writ/process/work-orders/m1/P01/001.md", "source-work-order.md"),
    ("src/lending.test.ts", "source-tests.ts"),
]
GENERATED = [
    ("writ/process/COVERAGE.md", "generated-COVERAGE.md"),
    ("writ/INDEX.md", "generated-INDEX.md"),
]

# The queue file is mostly the guidance a real bootstrap deletes by hand; only the block between
# the splice markers is written by the tool, and that is the part worth showing.
QUEUE = ("writ/process/SLICE-QUEUE.md", "generated-SLICE-QUEUE.md")
MARKERS = ("<!-- generated:queue -->", "<!-- /generated -->")


def run(root, *argv):
    """Like the fixture's runner, but hands back stdout as well — `stats` writes there."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = tt.ledger.main(list(argv) + ["--root", root])
    return code, out.getvalue(), err.getvalue()


def spliced(text: str) -> str:
    """Just the generated block, markers included, so the example cannot show hand-written prose
    and imply the tool wrote it."""
    start, end = MARKERS
    head = text.index(start)
    tail = text.index(end, head) + len(end)
    return text[head:tail] + "\n"


def build(root: str) -> str:
    """Bootstrap the templates, overlay the product, run the tool. Returns the stats output."""
    tt.bootstrap(root)

    # The fixture's own two areas exist to prove the registry integrity check; this example
    # declares its own, and two sets of requirements would only be noise.
    for area in ("FR-ACC", "NFR-OBS"):
        shutil.rmtree(os.path.join(root, "writ", "spec", "requirements", area), ignore_errors=True)

    for rel, body in OVERLAY.items():
        path = os.path.join(root, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tt.write(path, body)

    code, _, err = run(root)
    if code != 0:
        raise SystemExit("the example tree does not pass the tool:\n" + err)

    code, stats, err = run(root, "stats")
    if code != 0 or not stats.strip():
        raise SystemExit("stats produced nothing:\n" + err)

    code, graph, err = run(root, "graph")
    if code != 0 or not graph.strip():
        raise SystemExit("graph produced nothing:\n" + err)
    json.loads(graph)  # it has to parse, or the example ships a broken export
    return stats, graph


def collect(root: str, stats: str, graph: str) -> dict:
    out = {}
    for src, name in SOURCES + GENERATED:
        out[name] = tt.read(os.path.join(root, *src.split("/")))
    out[QUEUE[1]] = spliced(tt.read(os.path.join(root, *QUEUE[0].split("/"))))
    out["generated-stats.txt"] = stats
    out["generated-graph.json"] = graph
    return out


def publish(files: dict) -> None:
    os.makedirs(DEST, exist_ok=True)
    for name, body in files.items():
        tt.write(os.path.join(DEST, name), body)
    print("wrote %d files to %s" % (len(files), os.path.relpath(DEST)))


def check(files: dict) -> int:
    bad = 0
    for name, body in files.items():
        path = os.path.join(DEST, name)
        if not os.path.exists(path):
            print("::error::%s is missing. Run: python3 writ/tests/build_example.py" % name)
            bad += 1
            continue
        committed = tt.read(path)
        if committed != body:
            print("::error::%s has drifted from what the tool prints." % name)
            for line in list(difflib.unified_diff(
                committed.splitlines(), body.splitlines(),
                fromfile="committed", tofile="rebuilt", lineterm=""))[:20]:
                print("  " + line)
            bad += 1
    print("example: %d files checked, %d stale" % (len(files), bad))
    return 1 if bad else 0


def main(argv) -> int:
    root = tempfile.mkdtemp(prefix="writ-example-")
    try:
        files = collect(root, *build(root))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    if "--check" in argv:
        return check(files)
    publish(files)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
