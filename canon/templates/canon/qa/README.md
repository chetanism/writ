# Manual test scenarios

> **Status:** active from <DATE>.
> **Role:** one file per requirement, saying what somebody **does** at a keyboard to find out
> whether it holds — the happy path and the ways it gets done wrongly, runnable by a person with a
> browser and nothing else.
> **Owner:** <the test manager>. Anybody may draft one; the test manager approves it. <Solo, the
> one human is the test manager too, and the agent drafts.>
> **Precedence:** the requirement's detail file wins over everything here, and the requirement's
> register row wins over that. See *The one rule* below.

Hand this file to anybody joining the test team. It is the whole process.

## Why this exists

`canon/spec/requirements/` says what a requirement **means** — the job somebody is doing, who must
be turned away, what happens at the edges. That is the argument about the product, and it is settled
by the specification's owner.

It is still not a test session. It names no build, no accounts, no order to do things in, and
nothing about what somebody can actually reach: early on, much of a product is a command line, and
whoever tests it has a browser. So a detail file read at a keyboard becomes an hour of deciding what
to try next, which is how two testers cover two different things and neither knows what the other
left out.

So: one file per requirement, named for it, holding the scenarios themselves. **The detail file is
the argument; this is the session.**

## The one rule

**A scenario is done through the product's own screens.**

Whoever runs these has a browser and an account. No terminal, no database, no access to the server,
no command-line tool. A scenario that needs one of those is a scenario nobody on the test team can
run, and a file of them looks like coverage while producing none.

Where a precondition genuinely cannot be reached through the product — and there are a few, while
some of the product is still a command line — it goes under *Before you start*, on the **Not
through the screen** line, addressed to whoever sets the environment up. It is never a step in a
scenario, and `ledger.py check` fails a file that puts one there.

The second rule follows from the first: **say what to achieve, not what to press.** *Open the list
of the organisation's locations* keeps working when somebody moves the button. *Click Settings, then
Locations, then Add* is wrong the week the menu is rearranged. The screens are new and will keep
changing for a while yet, and a file rewritten every sprint is a file nobody runs.

## Layout

```text
canon/qa/scenarios/<area>/<id>.md      FR-ACC/FR-ACC-01.md, INV/INV-003.md
```

The area is the identifier without its number, exactly as the detail files are filed, so the two
directories line up file for file. The check fails if a file sits in the wrong directory, is named
for an identifier the specification does not declare, or is named for one that has since been
withdrawn.

**Covered families are `scenarios.families` in `scripts/ledger.config.json`** — the same ones the
detail track covers, the requirements and invariants a person can be asked to exercise.

**Every scenarios file has a detail file behind it.** A requirement with none is refused rather than
guessed at: the requirement's row is one line, and inventing the actors and the boundary from it is
the guessing the detail track exists to stop. Where the detail file is still a `draft`, the
scenarios may be written and say so — `detail_status` and `detail_read_on` record what was read —
and the check fails the day that file is approved or amended, which is the day the cases need
re-reading.

## One requirement, one branch

A scenarios file reaches `dev` through a pull request like any other change
(`DEVELOPMENT-PROCESS.md` §8), on a branch named for the requirement rather than for the sitting:

```text
qa/<id lowercased>        qa/fr-acc-01, qa/inv-1
```

**The identifier and nothing else**, for the same reason `req/<id>` is: it makes the branch
something to compute rather than something to search for, so a second sitting finds the first
instead of starting a second file.

| Where you are | What happens |
|---|---|
| Starting one | `git checkout dev && git pull --ff-only`, then `git checkout -b qa/<id>`. Nothing is pushed yet |
| The file is written and `ledger.py check` is green | Commit, push, open the pull request into `dev`. The file is the description, so the reviewer is handed the thing itself |
| Coming back while that pull request is open | Check out the same branch and carry on |
| Coming back after it merged | A correction starts a fresh `qa/<id>` off `dev` |

**`traceability.yml` refuses a scenarios file that arrives any other way** — one requirement per
branch, and the branch named for it. Renames and deletions are exempt: moving a file is not writing
scenarios.

A row added to *Runs* is a change to the same file and follows the same rule.

## Who does what

| Step | Who |
|---|---|
| Draft the file | Anybody, with `/test-scenarios <id>` — it is a draft, not an answer |
| Cut what is not worth a session, and say what the environment can actually provide | The test manager |
| Approve it — `status: reviewed`, `approved_by:` filled | The test manager |
| Run it, and add a row to *Runs* | Whoever tests by hand |
| Answer what the file could not settle | The specification's owner, by amending the **detail** file |

**A question a scenario cannot answer is never answered here.** If the detail file does not say what
should happen, the scenario is not written to a guess — the question goes back to that file's owner.
A scenarios file that decides what the product does is a specification with no owner.

## When

**After the detail file is reviewed, and the natural moment is when the claiming slice's work order
is approved.** A scenario names the part of the product that owns the behaviour, and the work order
is usually where that is settled — written earlier, every scenario rests on a guess about the
screen; written then, the file is ready the week the slice merges rather than written that week. It
is never on the slice's critical path either way: the work order does not wait for the scenarios,
and the scenarios do not wait for the code.

The order of one requirement's documents is a cadence, not a gate — `DEVELOPMENT-PROCESS.md` §11.
Requirement, detail file, its approval, the work order, the scenarios, the code and its summary,
then the scenarios are run and the requirement verified, with findings going back to the detail
file. Each document is the input the next one reads; nothing waits.

**Solo, wait for a second pair of hands.** The implementer playing the demo already happens at
every slice. A scenarios file earns its place when somebody who did not build the behaviour runs
it, and until that person exists the directory stays empty and nothing is missing.

Do not bulk-generate. A directory of scenarios nobody has cut down to a session is not coverage.

## Writing one

1. `/test-scenarios <id>` — it reads that requirement's detail file, the slices that claim it,
   the screen inventory where the project keeps one, and nothing else. **It reads the scenario list
   back as one line each** before writing anything: what each one is, its type, and whether it can
   be run today.
2. **Cut it.** A scenario per boundary row is thorough, and a session nobody finishes is not
   coverage. This is the test manager's call and it is where the list earns its shape.
3. It writes the file and reports what changed, rather than reciting it.
4. `python3 scripts/ledger.py check`, then push `qa/<id>` and open its pull request.

**Where the scenarios come from is mechanical**, and the skill does it exhaustively: every story
becomes a happy path, every **May not** cell becomes a scenario where the wrong person is turned
away, every boundary row becomes one of its own, every mandatory field becomes a scenario that
leaves it blank. Then it is cut down.

**Types, and a file needs more than one.** `happy path`, `negative`, `permission`,
`another tenant`, `repeat`, `at once`, `boundary`. A file of nothing but happy paths fails the
check: the ways somebody gets it wrong are most of what a manual session is for.

## Running one

A run is a row in the file's *Runs* table: the date, the build, `pass`, `fail` or `blocked`, who ran
it, and — for a `fail` — which scenario and what happened. A result nobody can act on is the same as
no run.

`blocked` is a real result and a useful one. It means the scenario could not be reached: the
environment was missing something, or the screen is not there yet. A file whose scenarios are mostly
`blocked` is telling the queue something.

**When to run.** `/slice-close` names the scenarios the slice it is closing has just unblocked —
the ones whose *Not testable yet* row waited on that slice — so they are run against the build that
unblocked them, and `Ready` flipped to `yes` on the `qa/<id>` branch. At the phase gate, everything
that turned `Ready` during the phase is run before `/requirement-verify` walks the requirements,
because a `pass` row here is the evidence that run reads first.

**Findings go back up, never sideways.** A `fail` that turns out to be the product is a work item
for the slicer. A `fail` that turns out to be the detail file is `/requirement-detail`'s to correct,
and the correction moves that file's `revised_on`, which fails this file until it is re-read. A
scenario is never edited to match what was built.

This is not `MANUAL-REGRESSION.md`, which is the short list of by-hand walks worth **re-running**
after a change, promoted from slice demos and kept short by deletion. A scenario here is run when
its requirement is worth checking; one that turns out to be worth running every time is promoted
there, and one an automated test comes to cover is deleted from there.

It is also not `/manual-test`, which explores what nobody wrote a step for and is report-only. That
finds what these miss by definition.

## What the check enforces

`python3 scripts/ledger.py check` — the same command CI runs — fails on any of:

- a file named for an identifier the specification does not declare, or one outside the covered
  families
- a file in the wrong area directory, or whose front matter disagrees with its own filename
- **a scenarios file with no detail file behind it**
- a `detail_status` that no longer matches the detail file, or a `detail_read_on` earlier than the
  detail file's `revised_on` — it was approved or amended after these cases were written, so they
  need re-reading and `detail_read_on` re-dated
- a missing front-matter field, a `status` outside `draft|reviewed`, or a `reviewed` file naming no
  approver
- **a quoted requirement that is not the specification's text, character for character**
- a missing template section, or a file carrying no scenario at all
- **a file whose scenarios are all `happy path`**
- a scenario whose `Type` is outside the seven, or whose `Ready` is neither `yes` nor `no`
- **a command line inside a scenario** — a shell prompt, `psql`, `docker compose`, `curl`, and the
  project's own tools named in `scenarios.commands`. Setup that genuinely needs one belongs on the
  *Not through the screen* line
- a run recorded as anything other than `pass`, `fail` or `blocked`

`COVERAGE.md` grows one section from the same data: how many files exist, how many are reviewed, and
every reviewed detail file with no scenarios behind it. That list is the track's backlog, listed
rather than averaged away.

**`require_scenarios_for_reviewed_detail` in `scripts/ledger.config.json` is `false`.** Turn it to
`true` once that backlog is cleared, and from then on a requirement cannot be detailed and approved
without scenarios behind it.

## What this is not

It is not a second reading of the requirement. Every scenario traces to a line in the detail file
through its `Covers` field, and where the detail file is silent the scenario is not written — the
question goes to its owner. Three documents each describing one requirement is three documents that
drift, and the two that have no owner drift first.

It is not an automated suite, and it does not replace one. A scenario that an automated test comes
to cover completely is worth deleting; what stays is what a person notices and a test does not — a
screen that renders wrong, a message that reads badly, a flow that technically works.
