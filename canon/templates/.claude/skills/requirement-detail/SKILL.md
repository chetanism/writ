---
name: requirement-detail
description: Work out with the reader what one requirement means, then write its detail file — a short read-back, an interview in rounds, and the file last, so the job stories can be built against and test scenarios can be written from it. Use when asked to detail, elaborate or write up a requirement by its identifier, or when preparing a phase's requirements for the test team.
---

# Detail one requirement

The parallel track described in `canon/spec/requirements/README.md`. **You are drafting, not
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
  propose the specific correction and stop. If it is a `draft`, this is the **review conversation**
  rather than a first draft: summarise it in step 3 the same way, add a line saying where you would
  now write it differently, and interview from there. Working through the existing drafts with
  their owner is what this mode is for.

## 1a. Get onto the requirement's branch

**Before reading anything, and before writing anything.** One requirement, one branch, named for the
identifier lowercased and nothing else — `req/fr-acc-01`. `canon/spec/requirements/README.md`
says why; this is how.

**A dirty tree stops here.** `git status --porcelain` — if it is not empty, say what is uncommitted
and ask what to do with it. Never stash, commit or discard on the reader's behalf, and never bare
`git stash`: the stack is shared with every other worktree on the machine.

**Check the repository's shape first**, with `git remote`. Where there is no remote, the branch is
local, the fetch and the pull request below are skipped, and you say so — never fall back to
working on `dev`.

Then `git fetch origin --prune` and take the first case that holds — `git rev-parse --verify
req/<id>` finds a local branch, `git ls-remote --heads origin req/<id>` a pushed one:

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
| The requirement's row in its area's register, `canon/spec/requirements/<AREA>/index.md`, **and the rows around it** | Its own words, its target milestone, and where its neighbours' scope begins — that is the *Out of scope* fence |
| `canon/spec/BRD.md` §7, and the area's paragraph in §8 | The job in prose — what the requirements are *for* |
| `canon/INDEX.md`, the requirement's line | Whether a question is open against it, and what already stands behind it |
| The foundation spec that governs the area | The shape the behaviour must take |
| Its row in `canon/process/COVERAGE.md` | Which slices claim it and which tests name it |
| Those slices' work orders and summaries | What was actually built, what was deferred, and to which slice |
| The annotated tests themselves | The behaviour that is really asserted, in its own words |
| `.claude/skills/manual-test/reference/areas.md`, the section covering the area | The oracles — **cite them, never restate them** |
| The surface: the command-line usage, the published contract | Where a person can actually exercise it today |

Do **not** read the other requirements' detail files. Do not read the whole specification.

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
```

That last line is the point of the exercise. Everything after it is a conversation, not a document
review — the reviewer should never be handed ninety lines and asked to find the three that are
wrong.

## 4. Interview, in rounds of two to four

Ask only questions **whose answer changes the file**. Never ask what the specification already
answers, what the tests already show, or what you could read in the code — those are yours to find
out, and asking them is how an interview becomes an interrogation nobody finishes.

- **Batch two to four at a time, numbered, each with the answer you would pick and why.** The
  reviewer should be able to reply *"1 yes, 2 the second one, 3 ask the owner"*. Use
  `AskUserQuestion` where the answers are a closed set, so it is one click rather than a sentence.
- **Round one is meaning**: who does the job and who must be turned away, the situation the
  requirement is silent about, the neighbouring requirement the fence runs against.
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
2. **An answer that contradicts an invariant or a shipped behaviour.** Name the invariant, name the
   two answers, and stop — the same rule the slicer works under (`DoD-12`).

If the reader says to skip the interview, skip it: draft the file and put every question you would
have asked into *Open questions*. A drafted file with five honest open questions is a good outcome.

## 5. Write it

Copy `canon/process/templates/requirement-detail.md` to
`canon/spec/requirements/<area>/<id>.md` — the area is the identifier without its number, and the
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
  scenarios file under `canon/qa/scenarios/` records the day it read this file, and `ledger.py
  check` fails it once this date is later. That is the only way an amendment here reaches the test
  team, so a change that leaves the date alone is a change nobody downstream hears about.

## 6. Do not guess

Where the interview did not settle something whoever tests this would hit — because nobody in the
room owns it, or because the answer would change the product — it goes in **Open questions**,
addressed to a person by name, with the two answers named. Never resolve it in the file — a detail
file that answers a question the specification left open is a specification with no owner, and
nobody will ever know it happened.

Where the specification is genuinely wrong — self-contradictory, or contradicted by an invariant —
that is a finding for its owner, said out loud in your reply, not a correction made here.

## 7. Close the loop without a wall of text

Run `python3 scripts/ledger.py` and `python3 scripts/ledger.py check`. Then commit, push, and open
the pull request — the file is what the reviewer reads, so the file is the body:

```bash
git add canon/spec/requirements/<area>/<id>.md canon/process/COVERAGE.md
git commit -m "docs(requirements): detail <id>"
git push -u origin req/<id>
gh pr create --base dev --title "<id> — <what it settles, in a few words>" \
  --body-file canon/spec/requirements/<area>/<id>.md
```

**A branch whose pull request is already open gets the commit and the push, and no second pull
request.** Push before you report, either way: an interview that ended on one machine is worth
nothing on the next. Where there is no remote, commit and say plainly that the push and the pull
request are waiting on one.

Then report **in a dozen lines or fewer**:

- what changed from what you read back in step 4 — one line each, and nothing that did not change;
- the stories, numbered, one line each, and the observables that no story reaches;
- the open questions by number, and who each is addressed to;
- the two or three places you are still least sure.

**Never print the file back.** The reviewer has been in the conversation; they do not need it
recited, and a recitation is how the parts nobody discussed get read as agreed.

`status` stays `draft` and `approved_by` stays empty unless the person you have just interviewed
**owns the specification** and says plainly that the file now reads right — then set both, naming
them. Where that is also the person who asked you to draft it, say that `drafted_by` and
`approved_by` are now the same person, which the process accepts and prefers not to. Approval is
theirs to give and never yours to assume.
