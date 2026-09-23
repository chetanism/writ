---
name: requirement-detail
description: Work out with the reader what one requirement means, then write its detail file — a short read-back, an interview in rounds, and the file last, so the job stories can be built against and test scenarios can be written from it. Use when asked to detail, elaborate or write up a requirement by its identifier, or when preparing a phase's requirements for the test team.
---

# Detail one requirement

The parallel track described in `writ/spec/requirements/README.md`. **You are drafting, not
deciding.** What a requirement means belongs to the specification's owner; what you produce is a
first reading they correct.

Invoked as `/requirement-detail FR-ACC-01`.

**It is a conversation, not a delivery.** Read the requirement, put eight lines in front of the
reader, ask them the handful of questions whose answers change the file, and write it once you both
know what it says. Generating ninety lines and asking somebody to find the wrong three is the shape
this replaces — a reviewer reading a plausible document agrees with it, which is exactly the failure
the whole track exists to avoid.

**Write it for the people who will read it, and they are not engineers.** The reader is the
specification's owner, and after them whoever builds the screen and whoever tests it. So: *somebody
who is not a member of this organisation*, not *an actor with no membership*. *Turned off*, not
*deactivated*. *What they see*, not *the response payload*. The one place this does not apply is
the requirement's own quote, which is copied and never touched. Identifiers stay — `INV-3` is a
citation, not jargon — but a sentence should read to somebody who has never opened the code.

## 0. One requirement at a time

**One identifier per invocation.** Given an area or a phase, list the identifiers it covers, say
which have files already, and ask which one to start with. Given several identifiers, do the first
and stop.

This is not politeness. A session holding twelve requirements writes twelve files that blur into
each other, and the blurring is invisible in review — which is the failure this whole track exists
to avoid.

## 1. Refuse the ones that are not yours

- **Not declared in the specification** — stop and say so. The identifier may have been withdrawn
  (`Status: withdrawn` in its register, which retires it) or mistyped.
- **Outside the covered families** — `requirements.families` in `scripts/ledger.config.json` names
  them. The rest name mechanisms and process rules, not things a person is asked to exercise. Say
  which requirement the mechanism serves and offer that instead.
- **A file already exists** — read it. **It may exist only on the requirement's branch**, so this
  bullet is settled after step 1a rather than before it. If it is `reviewed`, do not rewrite it;
  propose the specific correction and stop — **unless `ledger.py check` names slices built against
  an older reading of it**, which is step 2a's reconciliation, done on the reviewed file and reviewed
  again like any correction. If it is a `draft`, this is the **review conversation**
  rather than a first draft: summarise it in step 3 the same way, add a line saying where you would
  now write it differently, and interview from there. Working through the existing drafts with
  their owner is what this mode is for.

## 1a. Get onto the requirement's branch

**Before reading anything, and before writing anything.** One requirement, one branch, named for the
identifier lowercased and nothing else — `req/fr-acc-01`. `writ/spec/requirements/README.md`
says why; this is how.

**A dirty tree stops here.** `git status --porcelain` — if it is not empty, say what is uncommitted
and ask what to do with it. Never stash, commit or discard on the reader's behalf, and never bare
`git stash`: the stack is shared with every other worktree on the machine.

**Check the repository's shape first**, with `git remote`. Where there is no remote, the branch is
local, the fetch and the pull request below are skipped, and you say so — never fall back to
working on `dev`.

Then `git fetch origin --prune` and take the first case that holds.
`git rev-parse --verify req/<id>` finds a local branch and
`git ls-remote --heads origin req/<id>` a pushed one:

1. **The branch exists and its pull request is open** — `gh pr list --head req/<id> --state open`.
   Check it out and carry on; a reviewer's corrections belong on the branch they are reviewing.
   Read the file that is already there before asking anything, and treat this as step 1's review
   conversation rather than a first draft.
2. **The branch exists and there is no pull request** — an interview somebody stopped halfway.
   Check it out, say so, and read what is on it.
3. **Its pull request merged** — the requirement is settled and a correction is new work. Say so,
   `git branch -D req/<id>` if a local copy survived the squash, and start again from case 4.
4. **Nothing exists** — `git checkout dev && git pull --ff-only && git checkout -b req/<id>`.
   Nothing is pushed until there is a file to push.

## 2. Read, and read only this

| Read | For |
|---|---|
| The requirement's row in its area's register, `writ/spec/requirements/<AREA>/index.md`, **and the rows around it** | Its own words, its target milestone, and where its neighbours' scope begins — that is the *Out of scope* fence |
| `writ/spec/BRD.md` §7, and the area's paragraph in §8 | The job in prose — what the requirements are *for* |
| `writ/INDEX.md`, the requirement's line | Whether a question is open against it, and what already stands behind it |
| The foundation spec that governs the area | The shape the behaviour must take |
| Its row in `writ/process/COVERAGE.md` | Which slices claim it and which tests name it |
| Those slices' work orders and summaries | What was actually built, what was deferred, and to which slice |
| The annotated tests themselves | The behaviour that is really asserted, in its own words |
| `.claude/skills/manual-test/reference/areas.md`, the section covering the area | The oracles — **cite them, never restate them** |
| The surface: the command-line usage, the published contract | Where a person can actually exercise it today |
| `requirements` in `scripts/ledger.config.json` | `out_of_order`, which says how hard a conflict with the build is held, and `code_inspection`, which says whether step 2a may open the code |

Do **not** read the other requirements' detail files. Do not read the whole specification.

## 2a. Already built? Then the order has broken, and this is a backfill

**Look downstream before writing anything** (`writ/process/DEVELOPMENT-PROCESS.md` §12.1). If a
slice claiming this requirement is in progress or done, or tests name it with no slice behind them
(`≈` in the ledger), the build got here first. The file then has two jobs: say what the requirement
means, and reconcile that with what was built. Neither job is allowed to do the other's work.

- **Read the evidence, strongest first.** The annotated tests are what is really asserted. The slice
  summaries say what was built and what was deferred. The work orders' acceptance criteria say what
  was intended. Where `requirements.code_inspection` is `true`, also read the code those tests
  exercise. Where it is `false`, leave the code closed, and say in the read-back that behaviour no
  criterion or test names was not looked for.
- **List the slices this file has to reconcile with**: every slice claiming it that is in progress
  or done, whose `detail_read_on` is empty or earlier than the day you will date this file.
  `ledger.py check` names them. `COVERAGE.md` lists them under *Built ahead of its detail* while
  no file exists, and under *Built against an older reading* once one does.
- **Find the conflicts.** There are three kinds: the build does something the requirement's words
  rule out; the build made a choice the requirement is silent on — who may, what happens at the
  edge, what a blank field does; the build leaves out part of what the requirement says. **A choice
  the requirement was silent on is still a conflict**, because its owner never made it.
- **Draft the stories from the evidence, and mark each one *observed*.** A story read off the build
  is a guess about what was wanted, not a finding. It becomes the requirement only when the owner
  says so in round one.

**The build is evidence, never authority.** The easiest file to write here is a description of the
code, and a reviewer handed a plausible description agrees with it. That is how a specification
quietly becomes whatever got built, bugs included. It is the failure this step exists to stop.

## 3. Summarise it in eight lines, before writing anything

**Do not write the file yet.** Put the requirement in front of the reader first, short enough to
take in at a glance:

```
FR-ACC-01 · target M1 · ● satisfied by SL-001, SL-002 · Q-004 open

Says      <the specification's own words, one line, quoted>
The job   <when … somebody needs to … so that …, in their words rather than the system's>
Where     <where they meet it today — a screen, a desk, a phone call — and what is not built yet>
Who       <who does the job, and the one or two who must be turned away>
Reads as  <one sentence: what you believe it means in practice>
Unsettled <the two or three things the requirement does not answer>
Built     <only when step 2a found a build: the slices, and each conflict with it in one line>
```

That last line is the point of the exercise. Everything after it is a conversation, not a document
review — the reviewer should never be handed ninety lines and asked to find the three that are
wrong.

## 4. Interview, in rounds of two to four

Ask only questions **whose answer changes the file**. Never ask what the specification already
answers, what the tests already show, or what you could read in the code — those are yours to find
out, and asking them is how an interview becomes an interrogation nobody finishes.

- **Batch two to four at a time,** numbered, each option lettered with what it leads to and why it is or is not recommended, one
  marked **(recommended)**, and enough quoted context to answer without opening a file — the shape
  in `CLAUDE.md` §*Asking me to decide*. The reviewer should be able to reply *"1a, 2b, 3 ask the
  owner"*. Use
  `AskUserQuestion` where the answers are a closed set, so it is one click rather than a sentence.
- **Round one is meaning**: who does the job and who must be turned away, the situation the
  requirement is silent about, the neighbouring requirement the fence runs against.
- **For a backfill, round one is the conflicts instead**, one numbered ask each, quoting the
  requirement's words beside what the build does. The options are the decisions of §12.1: **a.
  ratify** — the build is what was wanted, and the story loses its *observed* mark; **b. fix** —
  the build is wrong, and a slice corrects it; **c. change request** — the requirement is wrong;
  **d. leave open** — nobody here can decide, and it goes to the person who can. Recommend one and
  say why — where the build contradicts the requirement's own words, never recommend ratifying.
  Then read the *observed* stories that raised no conflict back in one line each, and ask for one
  answer covering them all: every story the owner does not take is a conflict of its own.
- **Round two is the stories**: read back the situations you believe this requirement covers, one
  line each — *opening a second location*, *an address somebody already used*, *closing one for
  the season* — and ask which are missing, which are really the same one, and which belong to a
  different requirement. **This is where the reviewer's real knowledge lands.** A situation nobody
  can name is a screen nobody can build.
- **Round three, only if it earns itself**: what a story does not reach. The two people editing at
  once, the same thing sent twice, the field at its limit, the person from another tenant.
- Stop when the answers stop changing anything. Three rounds is plenty; if a fourth is needed, the
  requirement is probably two requirements, and that is a finding for its owner.

**Two answers you must not simply take:**

1. **An answer that changes what the product should do** is a specification amendment, not a
   detail-file answer. Say so, write the reviewer's reading into *Open questions* naming them, and
   let them decide whether to raise a change request (`/change-request`) — after launch, that is
   the only way a register row changes.
2. **An answer that contradicts an invariant.** Name the invariant, name the two answers, and stop
   — the same rule the slicer works under (`DoD-12`). One that contradicts **shipped behaviour** is
   a conflict with the build: it goes through the decisions above and into *Reconciliation*, and is
   never settled by quietly writing the file one way or the other.

If the reader says to skip the interview, skip it: draft the file and put every question you would
have asked into *Open questions*, and every conflict with the build into *Reconciliation* as `open`.
A drafted file with five honest open questions is a good outcome.

## 5. Write it

Copy `writ/process/templates/requirement-detail.md` to
`writ/spec/requirements/<area>/<id>.md` — the area is the identifier without its number, and the
check fails if the file sits anywhere else.

**The quote is copied, never composed.** `## The requirement` carries the second cell of the
requirement's register row, verbatim, as a blockquote, and `target:` mirrors its `Target` column; `python3 scripts/ledger.py check` compares it against
the specification character for character, so a paraphrase is a failing build rather than a slow
divergence. Wrapping it across several `>` lines is fine.

Then the rest, in the words of somebody doing the work rather than somebody building software:

- **The stories are the file.** One per situation somebody actually finds themselves in, named for
  the situation and not for a feature — *closing a location for the season*, not *facility
  deactivation*. Each one has to be checkable on its own: if nobody could tell afterwards whether
  it happened, it is not written finely enough yet. `ledger.py check` fails a file with no story in
  it, because a requirement nobody can tell a story about has not been understood yet.
- **Write the *When* as the situation, not the click.** *When the organisation opens a new
  location* is a situation. *When the admin clicks Add Location* is a click, and it dates the
  moment somebody moves the button.
- **Personas: fill the *May not* column properly.** It is the column that is always thin and always
  where the interesting cases are, and it is the half no story carries — a story is about somebody
  doing the job right.
- **Observable behaviour and Boundary are the residue, and they are allowed to be short.** Only
  what no story reaches: the things that hold across all of them at once, the timing, the sameness.
  `None — the stories cover it.` is a real answer and a better one than padding. Every line must
  still be capable of being **wrong**: *"the queue updates correctly"* cannot be; *"a second desk
  moving the same record after somebody else already moved it is refused, and told what it would
  have overwritten"* can be.
- **Mandatory and non-mandatory fields: the third column is the decision.** What happens when
  somebody leaves it blank is the question, and *refused* is one answer among several — a field
  that stops the desk when the information is genuinely unknown is a bad field.
- **Say what is not built yet, and name the slice that builds it.** A requirement a future slice
  claims still gets a file; whoever tests it needs to know which half is real today.
- **Out of scope is a fence, not a formality.** Name the neighbouring requirement that owns each
  thing this one does not.
- **Set `revised_on` to today, every time the claims change** — the first draft, a correction from
  the review conversation, an answered open question, a `detail-wrong` from verification. A
  scenarios file under `writ/qa/scenarios/` records the day it read this file, and `ledger.py
  check` fails it once this date is later. That is the only way an amendment here reaches the test
  team, so a change that leaves the date alone is a change nobody downstream hears about.
- **Reconciliation: one row per slice step 2a listed, dated today** — the same day as `revised_on`,
  which is what the check compares. `holds` where nothing conflicts; otherwise the decision round
  one reached, the conflict in one line, and who decided. **Every revision re-dates every row**,
  after re-reading that slice against the new claims: a row older than `revised_on` says only that
  the build held against a file that no longer exists. A `fix` names the slice that makes it; where
  none is queued yet, ask the slicer to queue one — a queued work order is a plan and costs nothing
  — and until then the row is `open`. A `change-request` names the request. A reviewed file may
  carry an `open` row only if it names the registered question that holds it.

## 6. Do not guess

Where the interview did not settle something whoever tests this would hit — because nobody in the
room owns it, or because the answer would change the product — it goes in **Open questions**,
addressed to a person by name, with the two answers named. Never resolve it in the file — a detail
file that answers a question the specification left open is a specification with no owner, and
nobody will ever know it happened.

Where the specification is genuinely wrong — self-contradictory, or contradicted by an invariant —
that is a finding for its owner, said out loud in your reply, not a correction made here.

**Never write `ratified` yourself**, and never let an *observed* story stand as the requirement
without the owner saying so. Accepting what was built as what was wanted is the owner's decision,
and it is the one this track most easily makes by accident.

## 7. Close the loop without a wall of text

Run `python3 scripts/ledger.py` and `python3 scripts/ledger.py check`. Then commit, push, and open
the pull request — the file is what the reviewer reads, so the file is the body:

```bash
git add writ/spec/requirements/<area>/<id>.md writ/process/COVERAGE.md
git commit -m "docs(requirements): detail <id>"
git push -u origin req/<id>
gh pr create --base dev --title "<id> — <what it settles, in a few words>" \
  --body-file writ/spec/requirements/<area>/<id>.md
```

**A branch whose pull request is already open gets the commit and the push, and no second pull
request.** Push before you report, either way: an interview that ended on one machine is worth
nothing on the next. Where there is no remote, commit and say plainly that the push and the pull
request are waiting on one.

Then report **in a dozen lines or fewer**:

- what changed from what you read back in step 4 — one line each, and nothing that did not change;
- the stories, numbered, one line each, and the observables that no story reaches;
- the open questions by number, and who each is addressed to;
- for a backfill, each conflict and the decision it got, and any slice still not reconciled;
- the two or three places you are still least sure.

**Never print the file back.** The reviewer has been in the conversation; they do not need it
recited, and a recitation is how the parts nobody discussed get read as agreed.

`status` stays `draft` and `approved_by` stays empty unless the person you have just interviewed
**owns the specification** and says plainly that the file now reads right — then set both, naming
them. Where that is also the person who asked you to draft it, say that `drafted_by` and
`approved_by` are now the same person, which the process accepts and prefers not to. Approval is
theirs to give and never yours to assume.
