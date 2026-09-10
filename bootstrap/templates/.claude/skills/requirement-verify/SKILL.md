---
name: requirement-verify
description: Check one finished requirement against the product — does the behaviour its detail file describes actually exist? Report-only, one requirement per run, for requirements the coverage ledger reads as satisfied. Use at a phase gate, or when asked whether a requirement is really met.
---

# Verify one requirement

The other half of the track in `docs/process/requirements/README.md`. A slice proves the claims it
made; nothing proves that a **requirement** is met, because a requirement is finished by several
slices and none of them owns it.

Invoked as `/requirement-verify FR-ACC-01`.

**Report-only.** It may append one row to the requirement's `## Verification` table. It may not
change anything else — not the code, not the tests, not the specification, and not the rest of the
detail file. Relaxing a detail file until it matches what was built is the exact failure this
exists to catch.

## 0. One requirement, and only the finished ones

**One identifier per invocation**, and its file is the only detail file you read. A run holding
several requirements produces findings about the wrong one.

Check `docs/process/COVERAGE.md` first:

- **`●` satisfied** — proceed. An annotated test names it and the slice claiming it is done.
- **`◐` partial or `○` none** — stop. Say what it is waiting on: a claiming slice that has not
  landed, or a claim with no test behind it. Verifying half-built behaviour produces a finding
  about the queue, not about the product.
- **No detail file, or one still `draft`** — stop and say so. There is nothing to judge against;
  `/requirement-detail` comes first, and a human approves it.

## 1. Read

The detail file, its tests, and the code those tests exercise. The work orders and slice summaries
that claim the identifier. Nothing else — you are answering one question about one requirement.

## 2. Take the stories, then the observables, one at a time

**The stories first.** Each `## Story N` is a situation somebody is really in, and its
*Given / When / Then* is what you go and reproduce — that is the strongest evidence there is, and
it is what the file was written to be checked against. Then the numbered lines under *Observable
behaviour* and the rows under *Boundary and negative cases*, which are what no story reaches.

For each of them, find the evidence and say what it is:

1. **Run it** where it can be run. The command line usually reaches most of the product; the
   throwaway instance in `.claude/skills/manual-test/` and the demo in the claiming slice's summary
   are the shortest path to a real one. A behaviour observed is worth more than a test read.
2. **Otherwise read the test that asserts it** — and judge whether it asserts *the observable* or a
   proxy for it. A test named for the requirement that checks a different thing is the most common
   way a requirement reads satisfied and is not.
3. **Then the boundary and negative cases**, which are where the gaps actually are. An
   implementation that handles the happy path and not the cross-tenant case is a `gap`, not an
   `implemented`.

Say, for each, whether it is proven, proven by proxy, or unproven.

## 3. One verdict

| Verdict | When |
|---|---|
| `implemented` | Every observable has evidence, and the boundary cases hold |
| `gap` | Some do and some do not. **Name which, precisely enough to become a work item** |
| `absent` | The requirement reads satisfied and the behaviour is not there. Say what the tests are actually asserting |
| `detail-wrong` | The file described the requirement wrongly. The file is what gets fixed, not the product |

Append one row to `## Verification` — date, verdict, who ran it, and evidence a reader can chase
(a command, a test name, a `path:line`). Nothing else in the file changes.

That row is a change to a tracked file, so it travels like one: `req/<id>` off `dev`, pushed with
its own pull request — or onto the detail file's own branch where that one is still open.
`/requirement-detail`'s step 1a is the resolution, dirty-tree rule included, and it applies here
unchanged.

## 4. Hand it on

- A **`gap`** goes to the slicer as a work item, with the observable it failed. It is not fixed
  here, and it is not fixed by widening a test.
- An **`absent`** is the serious one: something is credited as done that is not. Say it plainly, and
  name the slice that claimed it.
- A **`detail-wrong`** goes back through `/requirement-detail`, and the correction is reviewed like
  any other.
- A requirement the specification states ambiguously enough that two verdicts are defensible is a
  finding for its owner. Report it; never pick the reading that makes the verdict come out well.

Report in the terminal: the verdict, the observables that failed with their evidence, and anything
you could not reach — an observable nobody can exercise yet is a fact about the product, not a
gap in the run.
