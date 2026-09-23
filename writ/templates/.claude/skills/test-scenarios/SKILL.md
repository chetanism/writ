---
name: test-scenarios
description: Turn one requirement's detail file into manual test scenarios a tester can run through the product's own screens — happy paths and the ways somebody gets it wrong, read back as a list before anything is written. Use when asked to write test scenarios, test cases or a test plan for a requirement by its identifier, or when preparing a phase for the test team.
---

# Write one requirement's test scenarios

The track described in `writ/qa/README.md`. **The detail file already settled what the requirement
means** — that argument was had in `/requirement-detail` and it is not reopened here. This turns it
into things somebody does at a keyboard.

Invoked as `/test-scenarios FR-ACC-01`.

**Two rules govern everything below, and both come from who runs these.**

1. **A tester has the product and nothing else.** A browser, an account, and no terminal, no
   database, no server. Never write *run the seed command* into a scenario. Where a precondition
   genuinely cannot be reached through the product, it goes under *Before you start* addressed to
   whoever sets the environment up — that is the one place a command belongs, and `ledger.py check`
   fails a scenario carrying one anywhere else.
2. **The screens are not settled and will keep moving.** So write what to achieve, never what to
   press. *Open the list of the organisation's locations* survives a redesign; *click Settings, then
   Locations, then the Add button* is wrong the week somebody rearranges a menu, and a file of
   those is a file the test manager rewrites every sprint instead of running.

**When: after the detail file is reviewed, and ideally once the claiming slice's work order is
approved.** The work order is where the part of the product that owns the behaviour gets settled,
and a scenario written before it rests on a guess about the screen. It is never on the slice's
critical path: the work order does not wait for this, and this does not wait for the code. Solo,
this track waits for a second pair of hands — say so and stop if the person asking is also the one
who will build and demo it, unless they say otherwise.

**Write it for the person running it, who does not build software.** *Somebody who is not a member
of this organisation*, not *an actor with no membership*. *Turned off*, not *deactivated*.
Identifiers stay — `INV-3` is a citation, not jargon — but every step should read to somebody who
has never opened the code.

## 0. One requirement at a time

**One identifier per invocation.** Given an area or a phase, list the identifiers that have a detail
file, say which already have scenarios, and ask which to start with. Given several, do the first and
stop.

A session holding twelve requirements writes twelve files that blur into each other, and the
blurring is invisible in review.

## 1. Refuse the ones that are not yours

- **No detail file** — stop. Say so, and offer `/requirement-detail <id>` instead. There is nothing
  here to write scenarios from: the requirement's row is one line, and inventing the actors and the
  boundary from it is exactly the guessing the detail track exists to stop.
- **Not declared in the specification, or outside the covered families** — stop and say which.
  `scenarios.families` in `scripts/ledger.config.json` names the families. A withdrawn requirement
  says so under `Status` in its register, which retires it.
- **The detail file is a `draft`** — carry on, and **say so plainly in the reply**. Record its
  status and the date in `detail_status` and `detail_read_on`. `writ/spec/requirements/README.md`
  says cases are written only from a `reviewed` file; this makes that visible rather than blocking
  a test manager working a phase ahead of the reviewers. The cases will need re-reading when the
  detail file is approved, and the check will ask for it.
- **A scenarios file already exists** — read it. **It may exist only on the requirement's branch**,
  so this is settled after step 1a rather than before it. If it is `reviewed`, do not rewrite it:
  propose the specific correction and stop. If it is a `draft`, this is the review conversation —
  summarise it in step 3, say where you would now write it differently, and go from there.

## 1a. Get onto the requirement's branch

**Before reading anything, and before writing anything.** One requirement, one branch, named for the
identifier lowercased — `qa/fr-acc-01`. `writ/qa/README.md` says why; this is how.

**A dirty tree stops here.** `git status --porcelain` — if it is not empty, say what is uncommitted
and ask what to do with it. Never stash, commit or discard on the reader's behalf, and never bare
`git stash`: the stack is shared with every other worktree on the machine.

**Check the repository's shape first**, with `git remote`. Where there is no remote, the branch is
local, the fetch and the pull request below are skipped, and you say so — never fall back to
working on `dev`.

Then `git fetch origin --prune` and take the first case that holds.
`git rev-parse --verify qa/<id>` finds a local branch and
`git ls-remote --heads origin qa/<id>` a pushed one:

1. **The branch exists and its pull request is open** — `gh pr list --head qa/<id> --state open`.
   Check it out and carry on; a reviewer's corrections belong on the branch they are reviewing.
2. **The branch exists and there is no pull request** — a sitting somebody stopped halfway. Check it
   out, say so, and read what is on it.
3. **Its pull request merged** — the scenarios are settled and a correction is new work. Say so,
   `git branch -D qa/<id>` if a local copy survived the squash, and start again from case 4.
4. **Nothing exists** — `git checkout dev && git pull --ff-only && git checkout -b qa/<id>`.
   Nothing is pushed until there is a file to push.

## 2. Read, and read only this

| Read | For |
|---|---|
| `writ/spec/requirements/<area>/<id>.md` | **The source.** The stories, the personas, the fields, the observables, the boundary rows — every scenario below comes from a line in this file |
| Its row in `writ/process/COVERAGE.md`, and the slices it names | Which half is built, so `Ready` is a fact rather than a hope |
| The claiming slice's work order, where one is approved | The surface it builds and its acceptance criteria — the part of the product a scenario names, and the slice a blocked one waits on |
| The screen inventory, where the project keeps one; otherwise the claiming slices' work orders | Which screen owns this, whether it exists, and the slice that brings it. **Name the part of the product the way that document names it**, not the way the code does |
| `.claude/skills/manual-test/reference/areas.md`, the section covering the area | The oracles — **cite them, never restate them** |
| `writ/qa/scenarios/<area>/`, the neighbouring files | What a tester will already have run, so this file does not repeat it |

Do **not** read the specification beyond the requirement's own row, the other requirements' detail
files, the foundation specs, or the code. **The detail file is the source; going around it produces
a second reading of the requirement, which is the one thing this whole track exists to prevent.**
If the detail file does not answer something a tester would hit, that is an open question for its
owner — step 6 — and never something to look up.

## 3. Read the scenarios back before writing anything

**Do not write the file yet.** Put the list in front of the test manager, one line each, short
enough to take in at a glance:

```
FR-ACC-01 · detail file: draft, sam, 2026-09-10 · settings, the location list

S1  opening a second location          happy path      ready
S2  an address somebody already used   negative        ready
S3  a receptionist tries to close one  permission      ready
S4  a location from another tenant     another tenant  ready
S5  closing one twice                  repeat          no — SL-042
…
Setup   two accounts, a second tenant; nothing outside the product
Missing <what the detail file does not say and a tester would hit>
```

That last line is the point of the exercise. A list of twelve is a conversation; twelve written-out
scenarios is a document nobody reads carefully.

**Where the list comes from — this is mechanical, so do it exhaustively:**

| From the detail file | Becomes |
|---|---|
| Each **story** | At least one `happy path` scenario, doing that job properly |
| Each **May not** cell in the persona table | A `permission` scenario — the wrong person tries and is turned away |
| Each row of **Boundary and negative cases** | A scenario of the matching type: `another tenant`, `repeat`, `at once`, `boundary` |
| Each **Mandatory** field | A `negative` scenario leaving it blank, and the third column is the expectation |
| Each numbered **Observable behaviour** no story reaches | A scenario of its own |
| **Out of scope** | Nothing. Name it in *Related* and leave it to the requirement that owns it |

**A file of nothing but happy paths fails the check**, and rightly: the ways somebody gets it wrong
are most of what a manual session is for.

## 4. One round of questions, and only what changes the file

Ask two to four, numbered, each option lettered with what it leads to and why it is or is not recommended, one
marked **(recommended)**, and enough quoted context to answer without opening a file — the shape
in `CLAUDE.md` §*Asking me to decide*. The reviewer should be able to reply *"1a, 2b, 3 ask the
owner"*. Use `AskUserQuestion` where the answers are a closed
set.

The questions worth asking are almost always the same three:

1. **Which of the list are worth a tester's time?** A scenario per boundary row is thorough and a
   session nobody finishes is not coverage. The test manager cuts.
2. **What can they actually set up themselves?** Whether a second tenant, a turned-off account or a
   second person signed in at once exists in their environment decides whether those scenarios are
   `ready` or belong under *Not testable yet*.
3. **What does the detail file not say that a tester will hit?** That is step 6's list.

Never ask what the detail file already answers. Stop when the answers stop changing anything: one
round is usually right, two is the most this ever needs.

If the reader says to skip the questions, skip them — draft the file, and put every question you
would have asked into the reply.

## 5. Write it

Copy `writ/process/templates/test-scenarios.md` to `writ/qa/scenarios/<area>/<id>.md` — the area is
the identifier without its number, and the check fails if the file sits anywhere else.

**The quote is copied, never composed.** `## The requirement` carries the second cell of the
requirement's row, verbatim, as a blockquote — the same rule the detail file works under, and
`ledger.py check` compares it against the specification character for character. Take it from the
detail file, which already carries it correctly.

Then, in the words of somebody at a keyboard doing the work:

- **A step says what to achieve.** *Open the list of the organisation's locations.* *Start adding a
  location.* *Save it.* Not the menu path, not the button's label, not a link. Three to six steps
  is the shape; a scenario with fourteen is two scenarios.
- **An expectation has to be capable of being wrong.** *"It works"* cannot be. *"The location is in
  the list straight away, with every field exactly as it was typed"* can be, and a tester knows
  what to do with it. Say what must **not** happen where that is the interesting half — a refusal
  that half-wrote the record is a defect only an expectation that mentions it will catch.
- **Every scenario stands alone.** Somebody picking `S4` out of the middle runs it. `Given` carries
  who is signed in and what exists; it never says *continuing from S3*.
- **`Ready` is a fact.** `yes` only where the screen exists today — check the screen inventory and
  the slice's status in `COVERAGE.md`. Otherwise `no` and the slice that unblocks it, and the same
  scenario goes in *Not testable yet*. Write the blocked ones **fully**, against the screen the
  project says will own it: they are what makes this file runnable the week that slice lands,
  rather than rewritten.
- **Preconditions go in one place.** Everything a tester needs before scenario one, with who
  provides each. A tester who gets three scenarios in and finds they needed a second tenant has lost
  the session.
- **No commands in a scenario, ever.** If a precondition truly cannot be reached through the
  product, it goes on the *Not through the screen* line under *Before you start*, addressed to
  whoever runs it. The check enforces this, and the honest answer there is usually `None.`
- **`detail_status` and `detail_read_on` are what you actually read.** Today's date, and the
  status the detail file carries now. The check compares the date to that file's `revised_on` and
  fails this file the day the detail file moves past it — that is how an amendment upstream reaches
  the test team, and it only works if the date is honest.

## 6. Do not guess

Where the detail file does not answer something a tester will hit, **do not decide it here**. Say it
in the reply, addressed to the detail file's owner, with the two answers named — it belongs in that
file's *Open questions*, and a scenario file that answers it has become a second specification with
no owner.

Where the detail file contradicts itself, or contradicts something already shipped, name the two
answers and stop. That is the slicer's rule (`DoD-12`) and it holds here.

## 7. Close the loop without a wall of text

Run `python3 scripts/ledger.py` and `python3 scripts/ledger.py check`. Then commit, push, and open
the pull request — the file is what the reviewer reads, so the file is the body:

```bash
git add writ/qa/scenarios/<area>/<id>.md writ/process/COVERAGE.md
git commit -m "docs(qa): test scenarios for <id>"
git push -u origin qa/<id>
gh pr create --base dev --title "<id> — manual test scenarios" \
  --body-file writ/qa/scenarios/<area>/<id>.md
```

**A branch whose pull request is already open gets the commit and the push, and no second pull
request.** Push before you report, either way. Where there is no remote, commit and say plainly
that the push and the pull request are waiting on one.

Then report **in a dozen lines or fewer**:

- what changed from the list you read back in step 3 — one line each, and nothing that did not;
- the counts: how many scenarios, how many of each type, how many `ready`;
- what is waiting on which slice;
- the questions for the detail file's owner, numbered, addressed by name.

**Never print the file back.** The test manager has been in the conversation.

`status` stays `draft` and `approved_by` stays empty unless the person you have just talked to owns
this track and says plainly that it now reads right — then set both, naming them.
