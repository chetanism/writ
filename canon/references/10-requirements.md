# The requirement detail track, and the test scenarios behind it

Governs the phase that emits `/requirement-detail`, `/requirement-verify` and `/test-scenarios`
into the new project, along with `canon/spec/requirements/` and `canon/qa/`. Read it before that
phase.

The track is **parallel to the slice loop and never inside it**. Nothing in the loop waits on it,
and nothing in it waits on a slice. That is the property to protect: the moment a slice cannot
merge until a requirement is detailed, two people are on the critical path of every merge and the
process has become the serial one this replaces.

## The gap it fills, in one paragraph

A requirement in the BRD is one line, because a BRD states business intent and stops there. That is
enough to build against and **not** enough to test against by hand: it names no actor, no
precondition, no observable outcome and no boundary. Nothing else in the tree fills it — a work
order describes a *slice*, and slices and requirements are many-to-many by design, so a work order
spans several requirements and proves only the claims it made. Read a slice to test a requirement
and you get part of an answer with no way to know which part is missing.

`COVERAGE.md` is the mechanical half of the ledger: what is claimed and what is proven. This is the
human-facing half: what the requirement **means** — the job somebody is doing, told as stories, who
must be turned away, and what happens at the edges.

**One file, two readers.** The stories are what a product conversation is held over and what a
screen is built against; the sections after them — what holds across every story, what happens when
somebody does the job wrongly, where the requirement stops — are what the test scenarios are
written from. They are one file because a requirement described twice in two places is the failure
the track exists to avoid. `ledger.py check` fails a file that tells no story, because the stories
are the half that would quietly stop being written: every other section has a shape a drafter
falls into, and a story does not.

## The one rule, and why it is a check rather than a paragraph

**A detail file never restates its requirement in its own words.** It quotes the BRD row verbatim,
and `ledger.py check` compares the quote against the specification character for character.

Say why when you write the README: two wordings of one requirement is two requirements, discovered
the day they disagree, and by then nobody can tell which one the product was built against. The
check is what makes the rule real — when the register row is amended, every affected file fails until
somebody has read the amendment and re-dated `reviewed_against`. **That failure is the feature.**

## What to set at bootstrap

| Setting | Where | Default and why |
|---|---|---|
| the covered families | `requirements.families` in `scripts/ledger.config.json` | `["FR", "INV"]` — the families a person can be *asked to exercise*. Not `NFR` or the process families: those name mechanisms, and a mechanism is tested through the requirement it serves |
| the directory | `requirements.dir` | `canon/spec/requirements`. Empty turns the whole track off, which is what a project that declined it gets |
| the phase mirror | `requirements.phase_pattern` | Whatever token the BRD's requirement tables use — `V1\|V2\|R` out of the box. A declaring table with no such column is simply not phase-checked |
| the closing rule | `requirements.require_detail_for_satisfied` | `false`. Turning it on with a backlog fails the gate for work nobody has been asked for yet. It is what closes the track once the backlog in `COVERAGE.md` is cleared |
| who approves | the README's *Who does what* table | Solo: the agent drafts, the one human approves. Team: name the two people, and prefer that the approver is not the drafter |
| the scenario directory | `scenarios.dir` | `canon/qa/scenarios`. Empty turns that track off on its own; it reads the detail files, so it cannot run without the first |
| the project's tools | `scenarios.commands` | The names of the project's own command-line tools, from the stack phase. The command check knows a shell prompt, `psql`, `docker compose` and `curl` by shape; it knows the project's tool only by name, and an empty list leaves it blind to the command a drafter is most likely to paste |
| the scenario closing rule | `scenarios.require_scenarios_for_reviewed_detail` | `false`, for the same reason as the detail rule. Turn it on once every reviewed detail file has reviewed scenarios behind it |
| the test manager | `canon/qa/README.md`'s owner line, and the role table | Solo: the one human. Team: prefer somebody other than the specification's owner — what a requirement means and what a session covers are two arguments |

**Do not seed either directory.** An empty directory and a `README.md` is the correct output of
bootstrap, for both. Four hundred requirements drafted by an agent and read by nobody is not
coverage; it is a directory that looks like coverage, which is worse than an empty one. A directory
of scenarios nobody has cut down to a session is the same thing one step later.

## Solo mode is not a degenerate case

The split that matters is **drafter and approver**, not two named people. Solo, the agent drafts
and the human approves — which is the same two-party review the team version describes, and it is
the whole point: an agent's reading of a one-line requirement is exactly the thing a human is there
to correct. Write the README's role table that way rather than deleting it.

What solo genuinely loses is the second reader on the *approval*. Say so in the README rather than
pretending otherwise; `drafted_by` and `approved_by` naming the same person is a fact worth being
able to see later.

## One requirement, one branch

A detail file is settled over more than one sitting, so its branch is named for the requirement
rather than for the sitting: `req/<id>`, the identifier lowercased and nothing else. That makes the
branch something to compute rather than something to search for, which is what lets a second
session pick the work up instead of starting a second file. The scenarios use `qa/<id>` for the
same reason. `traceability.yml` refuses a file from either track arriving on any other branch, in
one loop over both, so the rule is a check rather than a convention. Both skills stop on a dirty
tree and ask, and neither stashes on the reader's behalf.

Where the project has no remote yet, both skills branch locally and say the pull request is
waiting, exactly as `/slice-open` does — never falling back to `dev`.

## The three skills, and the failure each is shaped around

**`/requirement-detail` is a conversation, not a delivery.** It reads the requirement back in eight
lines, interviews in rounds of two to four numbered questions each carrying the answer it would
pick, and writes the file last. The shape it replaces is generating ninety plausible lines and
asking somebody to find the wrong three — a reviewer handed a plausible document agrees with it,
which is the failure the entire track exists to avoid. One identifier per invocation, for the same
reason: a session holding twelve requirements writes twelve files that blur into each other, and
the blurring is invisible in review.

**`/requirement-verify` is report-only, in the way `/manual-test` is.** It answers one question
about one requirement: is the behaviour this file describes actually there? Four verdicts —
`implemented`, `gap`, `absent`, `detail-wrong` — and the vocabulary is checked, because *mostly
works* is the verdict it exists to refuse. It never edits code, never edits the BRD, and never
relaxes a detail file until it matches what was built. That last one is the failure it is shaped
around.

It runs **per phase gate**, over the requirements that turned `●` during the phase. Not per slice:
a requirement is usually finished by several slices, and verifying one half-built produces a
finding about the queue rather than about the product.

**`/test-scenarios` is a list before it is a file, and it never goes around the detail file.** It
reads one requirement's detail file — the stories, the *May not* cells, the boundary rows, the
mandatory fields — and derives the scenario list mechanically: every story a happy path, every
*May not* a permission case, every boundary row one of its own, every mandatory field a blank one.
Then it reads that list back one line each, with a type and whether it can be run today, and the
test manager cuts it — a scenario per boundary row is thorough, and a session nobody finishes is
not coverage. Only then is the file written. Where the detail file does not say what should happen,
the scenario is not written to a guess: the question goes back to that file's owner, because a
scenarios file that decides what the product does is a specification with no owner.

Two properties of the file are checked rather than trusted, because both fail silently and both
look like coverage: **a scenario is done through the product's own screens** — a command in a
scenario is a scenario nobody on the test team can run, and the one place a command belongs is the
*Not through the screen* line under *Before you start* — and **a file of nothing but happy paths
fails**, being the natural thing to write and the least useful thing to run. A scenarios file with
no detail file behind it fails too, and one written against a `draft` detail file records that and
fails the day the draft is approved, which is the day its cases need re-reading.

The screens are new and will keep moving, so the skill writes what to achieve rather than what to
press — *open the list of the organisation's locations*, not *click Settings, then Locations, then
Add*. A file rewritten every sprint is a file nobody runs.

**It trails the work order rather than leading the slice.** A scenario names the part of the
product that owns the behaviour, and the work order is usually where that is settled, so the
natural moment to write one is the work order's approval — never before the detail file is
reviewed, and never on the slice's critical path in either direction. **Solo, it waits for a
second pair of hands**: the implementer playing the demo is `DoD-5`, and a scenarios file earns its
place only when somebody who did not build the behaviour runs it. Say that in the QA README's owner
line and in the hand-over, and leave the directory empty.

## The order is a cadence, not a gate

One requirement's documents arrive in a fixed order — requirement, detail file, its approval, the
work order, the scenarios, the code and its summary, then the scenarios are run and the requirement
verified. Nothing in that order waits on anything else: slices and requirements are many-to-many,
so a slice cannot wait on every requirement it touches being detailed without putting the
specification owner and the test manager on the critical path of every merge, which is the serial
process this replaces. Write it in `DEVELOPMENT-PROCESS.md` §11 as an order of *inputs* — each
document is what the next one reads — and make it visible rather than enforced: `/slice-open`
reports, for every requirement a slice claims, whether its detail file and scenarios exist and in
what state.

**The return path is the half that is easy to leave out, so it is checked.** A scenarios file
records the detail file's status and the day it was read; the detail file carries `revised_on`,
moved by every amendment to its claims. The check fails the scenarios the day the detail file is
approved *and* the day it is amended while staying reviewed — without the date, an amended reviewed
file would fail nothing, since `status` moves once and the quote moves only with the BRD.
`/slice-close` names the scenarios a slice has just unblocked and any reviewed detail file the
slice makes stale; `/requirement-verify` reads a `pass` row in the scenarios as its first evidence
and says that a `detail-wrong` will fail them.

## Where it touches the rest of the process

- **`DEVELOPMENT-PROCESS.md` §12** — one section saying why the track exists and what it
  deliberately does not do. The detail joins §1's document model.
- **§11's cadence** — `/requirement-verify` per phase gate.
- **`DoD-12`** — the one place a slice reads the track: the *reviewed* detail files of the
  requirements it claims, because their observables are where a conflict shows up first. A `draft`
  file is one agent's reading; treat it as a prompt for a question, not as the requirement.
- **§13** — the scenario track, written from §12's output once the work order is approved, and the
  `qa/<id>` branch beside `req/<id>` in §8's table. The test manager joins the role table.
- **§11's cadence** — the order of one requirement's documents, as a cadence and not a gate, and
  the phase gate running the scenarios that turned `Ready` before `/requirement-verify`.
- **`/slice-open` and `/slice-close`** — the first reports the state of both tracks for every
  claimed requirement without gating on it; the second names the scenarios the slice unblocked and
  any detail file it made stale.
- **`COVERAGE.md`** — grows a *Requirement detail* section: how many files, how many reviewed, and
  every satisfied requirement with no reviewed file behind it — and a *Manual test scenarios*
  section: how many, how many reviewed, and every reviewed detail file with no reviewed scenarios
  behind it. Both lists are backlogs, **listed rather than averaged away**.
- **`/manual-test`'s oracles** — cited from a detail file, never copied into one. Three copies of
  what "correct" means is three documents that drift.
