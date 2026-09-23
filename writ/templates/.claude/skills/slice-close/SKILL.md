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
python3 scripts/velocity.py --diff dev
```

It counts the code lines this branch added — outside tests, comments, blanks and generated files —
and the lines of Markdown beside them. Report both. There is nothing to write into the front matter:
size is measured from git, after the fact, and `velocity.py` is what reads it later.

Where `size_budget` in `scripts/ledger.config.json` names tiers, also write the measurement into
the front matter as `code_lines:` and correct `size:` if it lands in a different tier; never touch
`estimated:`. With `size_budget` `{}` — the default — skip this paragraph.

## 3. Draft the summary

Copy `writ/process/templates/slice-summary.md` to
`writ/process/slices/<milestone>/<phase>/<ID>.md` — the path mirrors the work order's, and the
check looks there and nowhere else — and fill it. Five sections and a line:

- **What the system can do now** — behaviour, not files.
- **How it works** — name the entry point so a reader can start in the right place.
- **Decisions made** — one row each; a decision that binds a later slice also has an ADR.
- **Surprises** — the most valuable section. Ask the human directly: *what surprised you?* Include
  surprises about the process itself.
- **Falsification** — the section that finds defects, and it stays whatever else goes. See 3a.
- **Played** — one line: the demo command and what was seen. A demo worth keeping is promoted to
  `MANUAL-REGRESSION.md` (DoD-10), not pasted here.

Coverage is not restated — `COVERAGE.md` is generated — and what the slice deliberately left out is
already the work order's *Out of scope*.

## 3a. Falsify

For each control the slice added — a guard, a check, a constraint, a branch that refuses something —
remove it, run the tests that should catch that, and record which failed. A test that still passes
with the control gone was not testing it. **Do it with the tool, not by hand**: the cost was never
the test runs, it was the loop around them — find, edit, run, read, restore, write the row —
repeated for every control.

Write the plan to `writ/process/slices/<milestone>/<phase>/<ID>.falsify.json`, one entry per control:

```json
[
  {"control": "refuses a second sign-up", "file": "src/accounts/signup.ts",
   "find": "if (existing) throw new Conflict()", "with": "", "expect": ["FR-ACC-02"]}
]
```

```bash
python3 scripts/falsify.py writ/process/slices/<milestone>/<phase>/<ID>.falsify.json
```

It runs **only the test files annotated with each `expect` identifier**, not the whole suite; runs
a baseline once first, so a file already red is reported as unreliable rather than as a catch;
refuses a removal that does not change the file; and restores every file even on Ctrl-C. Paste its
table into the Falsification section. A control nothing caught is a finding: write the missing test
now, or say plainly why not.

**Probe a database constraint inside a transaction you roll back — never drop it.** A dropped
constraint left behind by a crashed run costs more than the whole falsification pass.

## 4. Regenerate and check

```bash
python3 scripts/ledger.py
python3 scripts/ledger.py check
```

Set `status: done` in the work order's front matter first, or the check will fail for the summary
it cannot find. `writ/INDEX.md` regenerates with the ledger and is committed with it. Fix everything it reports — each error is one document disagreeing with another.

## 5. Walk the definition of done

Report **the rows a command proves in one line** — *"DoD-2, 3, 4, 7: gate and `ledger.py check`
green"* — and walk every other row of `DEVELOPMENT-PROCESS.md` §4 one at a time, met or not, with
the evidence. The rows a green build says nothing about — DoD-5, DoD-10, DoD-12 and the human half
of DoD-1, DoD-6, DoD-8, DoD-9 — are reported as `[you]` with what was actually done; where the answer
is *not yet*, say so plainly rather than inferring it from a passing gate.

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

Report: the size (code and Markdown lines), the falsification table, the definition-of-done walk, the ledger delta (which
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

**End by recommending how to start the next slice** — the last lines of the report, as an ask in
the shape of `CLAUDE.md` §*Asking me to decide*:

```
1. Before the next slice:
   a. /clear (recommended), once the merge command has run — everything this slice learned is
      now in the summary, the ledger and the queue, and a fresh context reads those faster than
      this one carries its history.
   b. /compact — keeps a summary of this session; worth it only if something from it is not in a
      file yet.
```

Recommend `/compact` instead when something from this session is not yet in a file — an unmerged
pull request, a finding still to be raised, a follow-up the human asked for — and say which.

Then stop. Marking the pull request ready, running that command, clearing or compacting, and
sweeping the local branch are the human's.
