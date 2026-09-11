---
name: slice-close
description: Close a slice — draft the summary from the diff, regenerate the coverage ledger and queue, walk the definition of done item by item, and draft the commit with its trailer block. Use at step 7 of the slice loop, after the gate is green and the demo has been played by hand.
---

# Close a slice

Step 7 of the loop in `writ/process/DEVELOPMENT-PROCESS.md`. Invoked as `/slice-close`.

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
artefacts. Report both numbers and the estimate.

Then **write the measurement into the front matter** as `code_lines:`, and correct `size:` if the
measurement lands in a different tier — `ledger.py check` refuses a work order whose declared tier
does not contain its own number, because `size` is what the queue shows a reader. **Never touch
`estimated:`.** A slice guessed at 140 that came in at 287 is an `M` whose estimate missed, and
both halves are worth keeping; editing the guess to match the outcome is how a process stops being
able to learn from itself.

**If the estimate was wrong in the same direction three slices running, say so as a finding about
the tiers, not about this slice** — `python3 scripts/ledger.py stats` is where that pattern is
visible, and §2.1 asks for the recalibration after the first ten.

## 3. Draft the summary

Copy `writ/process/templates/slice-summary.md` to
`writ/process/slices/<milestone>/<phase>/<ID>.md` — the path mirrors the work order's, and the
check looks there and nowhere else — and fill it.

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
it cannot find. `writ/INDEX.md` regenerates with the ledger and is committed with it. Fix everything it reports — each error is one document disagreeing with another.

## 5. Walk the definition of done

Go through `DEVELOPMENT-PROCESS.md` §4 **item by item** and report each as met or not, with the
evidence. Do not summarise it as "done". A definition of done reported in aggregate is a definition
of done nobody is applying.

**Use the table's third column, and mark the rows it says are the human's.** Roughly half of them
are caught by nothing — DoD-5, DoD-10, DoD-12 and the human half of DoD-1, DoD-6, DoD-8, DoD-9 —
and those are the rows a green build says nothing about. Report them as `[you]` with what was
actually done, and where the answer is *not yet*, say so plainly rather than inferring it from a
passing gate. §4.1 is why: the tool checks the artefact, and the artefact is not the act.

Pay particular attention to the ones that are easy to skip:

- **DoD-8** — does `CLAUDE.md` reflect any new structure or convention? If this slice established a
  rule that binds later slices, add the line now, with its reasoning — **one line, and delete the
  line it supersedes.** That file is read at the start of every session, so it is the one document
  where adding without removing has a cost on every task. If `ledger.py check` warns that it is
  over budget, say so in the report and name `/context-compact`; do not start compacting inside a
  slice, and never buy room by deleting a convention that still holds.
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

## 5a. Name the scenarios this slice unblocks

Under `writ/qa/scenarios/`, find every scenario whose *Not testable yet* row, or whose `Ready`
field, names this slice. List them in the report — file, scenario, what it waits for — as the ones
to run against this build once it merges. **Do not edit those files**: `Ready` flips to `yes` and
the *Runs* row is added on the requirement's own `qa/<id>` branch, by whoever runs the session.

Then look the other way. If this slice changed a behaviour a `reviewed` detail file describes, that
is a finding for the specification's owner, not a silent edit — the file moves through
`/requirement-detail`, its `revised_on` moves with it, and the scenarios read before that date fail
until re-read. Say which files, or say plainly that none is affected.

## 6. Draft the commit

```
<type>(<scope>): <what changed, imperative, lowercase>

<Two or three sentences on the mechanism and why it is shaped this way.>

Slice: <ID>
Satisfies: <ids>
Partial: <ids>
Decision: ADR-NNNN
Amends: X-NNN

Closes #<N>
```

`Amends:` names the changelog line this slice added, where it amended a register or a plan, and is
omitted where it did not — `git log --grep 'X-NNN'` is then how the amendment's commit is found.

`Closes #N` is last and has no colon, and **N is the work order's `issue:`, never the pull
request's own number** — GitHub numbers both from one sequence, so a wrong number is a valid one
pointing at nothing and nothing fails. With no tracker configured, the line is omitted. Attribution
follows `CLAUDE.md` §Git, whichever way it was decided at bootstrap.

Stage the summary, the regenerated ledger and queue, and the work order's status change together
with the code: the summary is committed in the slice's own commit, not as a documentation change
afterwards.

**Write the message to `.git/SLICE_MSG` as well as into the commit.** A squash merge does not
inherit it — step 8 says why — so the file is what puts it back. `.git/` is never tracked and never
cleaned by a checkout, which is why it goes there rather than into the tree.

```bash
git commit -F .git/SLICE_MSG
```

## 7. Refresh the pull request and the issue, and post the summary

The pull request body was set from the work order at the claim and is now a snapshot of what the
slice was *going* to be. **Push the commit first**, so everything below points at the same bytes.
Then the pull request carries the summary — the outcome, for whoever reviews the merge — and the
issue carries the work order as it finally reads, with the summary as a comment:

```bash
git push
gh pr edit <PR> --body-file writ/process/slices/<milestone>/<phase>/<ID>.md
gh issue edit <N> --body-file writ/process/work-orders/<milestone>/<phase>/<NNN>.md
gh issue comment <N> --body-file writ/process/slices/<milestone>/<phase>/<ID>.md
```

The repository copy is the record and the comment is the notification (`DEVELOPMENT-PROCESS.md`
§1) — so **never edit the summary into the comment or the body**. If either would say something
the file does not, the file is wrong. With no tracker, the `gh issue` lines are skipped; with no
remote, all of it waits and you say so.

## 8. Report, hand over the merge command, and stop

Report: the size against the estimate, the definition-of-done walk, the ledger delta (which
identifiers moved, and to what), the scenarios this slice unblocked and any detail file it makes
stale, and anything you would have done differently.

**Then hand over the merge command in full, with `--body-file`.** A squash merge composes its own
message, and what it composes depends on how many commits the branch has: with one it reuses that
commit's message, and with more it uses the pull request's title and nothing else. A slice branch
has at least two — the claim and the close — so **the default silently discards the trailer
block**, and with it `Slice:`, `Satisfies:`, `Partial:`, `Decision:` and `Closes #N`. The issue
stays open and `git log --grep` stops answering *where did this get built*, which is the whole
reason §6.3 asks for the block.

```bash
gh pr merge <PR> --squash --delete-branch \
  --subject "<ID> — <title> (#<PR>)" --body-file .git/SLICE_MSG
```

Then stop. Marking the pull request ready, running that command, and sweeping the local branch are
the human's.
