---
name: slice-close
description: Close a slice — draft the summary from the diff, regenerate the coverage ledger and queue, walk the definition of done item by item, and draft the commit with its trailer block. Use at step 7 of the slice loop, after the gate is green and the demo has been played by hand.
---

# Close a slice

Step 7 of the loop in `docs/process/DEVELOPMENT-PROCESS.md`. Invoked as `/slice-close`.

## 0. Refuse to start if the demo has not been played

Ask: *has the demo been run by hand, and did it do what the work order said?* If the answer is no
or unclear, stop. **DoD-5 is not a formality** — automated tests prove the system does what it was
told to do; the demo is where the human finds out what they told it.

## 1. Read the actual change

```bash
git diff dev...HEAD --stat
git diff dev...HEAD
```

Then read the work order. You are checking two things: that every acceptance criterion has a test
whose name carries its requirement identifier, and that nothing landed which the work order did not
describe. **Report anything in the second category rather than quietly folding it into the
summary** — unplanned scope is the most useful thing this step finds.

## 2. Measure the size

```bash
git diff dev...HEAD --numstat
```

Added code lines are lines added outside test files, comments, blank lines and generated
artefacts. Report both numbers and the estimate. **If the estimate was wrong in the same direction
three slices running, say so as a finding about the estimate, not about this slice.**

## 3. Draft the summary

Copy `docs/process/templates/slice-summary.md` to `docs/process/slices/<ID>.md` and fill it.

- **What the system can do now** — behaviour, not files.
- **How it works** — name the entry point so a reader can start in the right place. Three sentences
  and a file path beat a diagram.
- **Decisions made** — the index; anything with a rejected alternative also has an ADR.
- **Surprises** — the highest-value section. What behaved differently from expectation, one bolded
  lead sentence each, **including surprises about the process itself.** Ask the human directly:
  *what surprised you?* Writing this after the fact is how a surprise becomes a thing quietly fixed
  instead of a thing learned.
- **Falsification** — remove each control the slice added, re-run the suite, record what failed,
  restore it. A test that still passes with the control removed was not testing the control.
- **Verify it yourself** — the demo as actually run, with observed output pasted in as comments.

## 4. Regenerate and check

```bash
python3 scripts/ledger.py
python3 scripts/ledger.py check
```

Set `status: done` in the work order's front matter first, or the check will fail for the summary
it cannot find. Fix everything it reports — each error is one document disagreeing with another.

## 5. Walk the definition of done

Go through `DEVELOPMENT-PROCESS.md` §4 **item by item** and report each as met or not, with the
evidence. Do not summarise it as "done". A definition of done reported in aggregate is a definition
of done nobody is applying.

Pay particular attention to the ones that are easy to skip:

- **DoD-8** — does `CLAUDE.md` reflect any new structure or convention? If this slice established a
  rule that binds later slices, add the line now, with its reasoning.
- **DoD-10** — did this slice change behaviour a `MANUAL-REGRESSION.md` entry covers? Re-run and
  re-date it. Is this slice's demo worth keeping? Promote it. Has an automated test made an
  existing entry redundant? Delete it.
- **DoD-11** — did this slice establish or change an **invariant**? Add or update its oracle in
  `.claude/skills/manual-test/reference/areas.md`, and add the area's new surface to that section.
  An oracle written now is written from the specification; one written at slice forty is written
  from memory. **If the slice found a trap the hard way — something where the reader is more likely
  to be wrong than the code is — write that down too, while it still stings.**
- **DoD-12** — was the conflict read actually done, at step 2a, *before* implementation? It is met
  by what `/slice-open` reported, not by a re-reading now. **A conflict found at close is a finding,
  not a tick**: say which requirement the shipped code makes false, and take it to the slicer. Never
  close it by reinterpreting the requirement — the whole rule exists because the person holding the
  diff is the last one who should choose between it and a requirement that inconveniences it.

## 6. Draft the commit

```
<type>(<scope>): <what changed, imperative, lowercase>

<Two or three sentences on the mechanism and why it is shaped this way.>

Slice: <ID>
Satisfies: <ids>
Partial: <ids>
Decision: ADR-NNNN

Closes #<N>
```

`Closes #N` is last and has no colon. **No agent attribution** — no co-author trailer, no session
link.

Stage the summary, the regenerated ledger and queue, and the work order's status change together
with the code: the summary is committed in the slice's own commit, not as a documentation change
afterwards.

## 7. Report and stop

Report: the size against the estimate, the definition-of-done walk, the ledger delta (which
identifiers moved, and to what), and anything you would have done differently.

Then stop. Marking the pull request ready, merging it, and sweeping the branch are the human's.
