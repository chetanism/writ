# Requirement detail

> **Status:** active from <DATE>.
> **Role:** one file per requirement, saying what it **means** — the job somebody is doing, told
> as stories, with who must be turned away and what happens at the edges — so a screen can be built
> against it, test scenarios can be written from it, and a finished requirement can be checked
> against the product rather than against its own tests.
> **Owner:** <the person who owns the specification>. <In team mode, name the two who may draft and
> approve; solo, the one human is the approver and the agent is the drafter.>
> **Precedence:** the area register wins over everything here, always. See *The one rule* below.

Hand this file to anybody joining the track. It is the whole process.

## Why this exists

A requirement in the specification is one line — *"Repeated failed sign-in and password-reset
attempts are rate-limited"* — because a business requirements document states intent and stops
there. That line is enough to build against and **not** enough to test against by hand: it names no
actor, no precondition, no observable outcome and no boundary.

Nothing else in the repository fills that gap. A work order describes a *slice*, which is the
thinnest change that alters what the system can do end to end; slices and requirements are
many-to-many by design, so a work order spans several requirements and proves only the claims it
made. Read a slice to test a requirement and you get part of an answer and no way to know which
part is missing.

So: one file per requirement, named for it, elaborating it in the terms of the people who do the
work. It is the **human-facing half** of the ledger, and `writ/process/COVERAGE.md` is the
mechanical half.

**One file, two readers.** The stories are what a product conversation is held over and what a
screen is built and reviewed against; the sections after them are what the test scenarios are
written from. They are one file because a requirement described twice in two places is the failure
this whole track exists to avoid — so the stories are the primary content, and what a story cannot
carry is kept to three things: what holds across every story at once (*Observable behaviour*), what
happens when somebody is not doing the job properly (*Boundary and negative cases*), and where this
requirement stops (*Out of scope*).

**Write it for the reader, and the reader does not build software.** *Somebody who is not a member
of this organisation*, not *an actor with no membership*. *Turned off*, not *deactivated*.
Identifiers stay, because a citation is not jargon.

## The one rule

**This file never restates the requirement in its own words.**

The specification says what the product must do. This says what a person would see if it were true.
The moment a detail file paraphrases its requirement, there are two wordings of one requirement, and
the day they disagree nobody can tell which the product was built against.

Mechanically: `## The requirement` carries the specification row's own text as a blockquote, and
`python3 scripts/ledger.py check` compares it character for character. When the specification is
amended, every affected detail file fails until somebody has read the amendment and re-dated
`reviewed_against`. **That failure is the point** — it is the only thing standing between this
directory and a shadow specification.

Where the detail work finds the specification to be *wrong* — ambiguous, contradictory, impossible
— that is a finding, and it goes to the specification's owner as an amendment. It is never resolved
here.

## Layout

```text
writ/spec/requirements/<area>/index.md     the area's register — the rows themselves
writ/spec/requirements/<area>/<id>.md      FR-ACC/FR-ACC-01.md, INV/INV-001.md
```

**The register sits beside the detail files it is elaborated by.** `index.md` is the one table that
declares the area's identifiers; everything else in the directory is named for one of them and
declares nothing. The check reads the register, and refuses a detail file whose quote is not the
register row character for character.

The area is the identifier without its number, so nothing has to be kept in step with it. The check
fails if a file sits in the wrong directory, is named for an identifier the specification does not
declare, or is named for one that has since been withdrawn — which is how a struck-through
requirement's file gets found rather than quietly outliving it.

**Covered families are `FR` and `INV`** — the requirements and the invariants a person can be asked
to exercise. Not `NFR`, `DoD` or the process families: those name mechanisms and process rules, and
a mechanism is tested through the requirement it serves. The covered set is
`requirements.families` in `scripts/ledger.config.json`; changing it is a decision, not a
configuration tweak.

## One requirement, one branch

A detail file reaches `dev` through a pull request like any other change
(`DEVELOPMENT-PROCESS.md` §8). Because a requirement is settled over more than one sitting, the
branch is named for the requirement rather than for the sitting:

```text
req/<id lowercased>        req/fr-acc-01, req/inv-1
```

**The identifier and nothing else.** A slug would make the branch for a requirement something to
search for; this way it is something to compute, which is what lets a second session pick the work
up rather than start a second file.

| Where you are | What happens |
|---|---|
| Starting one | `git checkout dev && git pull --ff-only`, then `git checkout -b req/<id>`. Nothing is pushed yet — a branch carrying no file is not worth a pull request |
| The file is written and `ledger.py check` is green | Commit, push, open the pull request into `dev`. The detail file is the description, so the reviewer is handed the thing itself |
| Coming back while that pull request is open | Check out the same branch and carry on. The corrections a reviewer asks for belong on the branch they are reviewing |
| Coming back after it merged | The requirement is settled. A correction starts a fresh `req/<id>` off `dev` |

**`traceability.yml` refuses a detail file that arrives any other way** — one requirement per
branch, and the branch named for it. Renames and deletions are exempt: moving a file is not
detailing a requirement.

**Uncommitted work in the tree stops the checkout.** Whoever is at the keyboard says what happens to
it; nothing is stashed, committed or discarded on their behalf.

**Push before a sitting ends.** An unpushed branch exists on one machine, and the next session finds
no trace of the interview — so it starts the file again instead of finishing it. Where there is no
remote yet, the branch is local and the pull request waits, and the skill says so.

A verification row is a change to the same file and follows the same rule: `req/<id>`, its own pull
request, or the detail branch itself where that is still open.

## Who does what

| Step | Who |
|---|---|
| Draft the file | Anybody, with `/requirement-detail <id>` — it is a draft, not an answer |
| Correct it, and decide what the requirement actually means | The specification's owner |
| Decide a conflict between this file and what was built — ratify, fix, change request | The specification's owner, and never the drafter |
| Approve it — `status: reviewed`, `approved_by:` filled | The specification's owner, and not the same person who drafted it where that is possible |
| Write manual test scenarios from it | Whoever tests by hand, with `/test-scenarios <id>`. They land in `writ/qa/scenarios/` and never here |
| Verify a finished requirement against the product | `/requirement-verify <id>`, run by anybody; the finding goes to the slicer |

**Manual scenarios are written only from a `reviewed` file.** A draft is an agent's reading of a
one-line requirement, and an agent's reading is exactly the thing this track exists to have a human
correct. A scenarios file written against a draft says so in its front matter, and the check asks
for it to be re-read the day the draft is approved.

## When

**One phase ahead of the queue.** While phase F is being built, the next phase's requirements are
being detailed. That keeps the track genuinely parallel — nothing in the slice loop waits on its
approval, and nothing here waits on a slice.

It is deliberately **not** in the definition of done. Coupling a slice to the approval of every
requirement it touches would put the specification's owner on the critical path of every merge,
which is the serial process this replaces. What `requirements.out_of_order: fail` asks is smaller:
a slice is claimed only for a requirement that has a detail file, and a draft is enough. That
reaches the drafter only when this track has fallen behind the queue.

Do not bulk-generate the whole specification. Four hundred requirements drafted by an agent and read
by nobody is not coverage; it is a directory that looks like coverage, which is worse than an empty
one. Draft what the phase in view needs.

## Drafting one

**It is a conversation, and the file is what it leaves behind.** Nobody reads ninety generated
lines carefully; a reviewer handed a plausible document agrees with it, which is the failure this
track exists to avoid.

1. `/requirement-detail <id>` — it reads the requirement's row, the specs that govern the
   area, the slices that claim it and the tests that name it, and then **reads the requirement back
   to you in eight lines**: what it says, the job somebody is doing, where they meet it today, who
   does it and who is turned away, what it appears to mean, and what it leaves unsettled.
2. **It interviews you** — two to four numbered questions at a time, each carrying the answer it
   would pick and why, so you can reply *"1 yes, 2 the second one, 3 ask the owner"*. It reads the
   stories back one line each before committing them — which situations this requirement covers,
   which are really the same one, which belong elsewhere — because that list is where your
   knowledge is worth the most.
3. It writes the file and reports what changed, rather than reciting it — and sets `revised_on` to
   today. Every later change to the claims moves that date again. It is what tells a scenarios
   file written from this one that it has to be re-read, so an amendment made without moving it is
   an amendment the test team never hears about.
4. Fill `approved_by` and set `status: reviewed`. If you own the specification and the interview
   settled it, say so and it will set both.
5. `python3 scripts/ledger.py check`, then push `req/<id>` and open its pull request — above.

**"I don't know" is a real answer**, and the honest one — it lands in *Open questions* addressed to
whoever owns it. An answer that would change what the product *does* is a specification amendment:
it says so rather than quietly writing it down here. **The parts an agent gets wrong are the same
every time**, so those are the questions it will ask: who may *not* do the thing, what happens at
the boundary, and what the requirement does not say.

**What a good file looks like** — the stories name situations somebody is really in, and every
line in *Observable behaviour* can be **wrong**. *"The queue updates correctly"* cannot be. *"A
second desk moving the same record after somebody else already moved it is refused, and told what
it would have overwritten"* can be, and whoever tests it knows what to do with it.

## When the build got here first

The order breaks, and it is not an exception: a slice builds a requirement nobody has detailed, a
file is revised after the slice that built it merged, a codebase is built first and its
requirements written afterwards. `DEVELOPMENT-PROCESS.md` §12.1 is the rule. This is what it means
for a detail file.

**`/requirement-detail` looks at the build before it writes.** Where a slice or a test already
built the requirement, the draft is a **backfill**: the stories are read off the tests, summaries
and work orders, each marked *observed*, and every conflict with the build — something the
requirement rules out, a choice it never made, a part left out — is put to you as a decision:

- **ratify** — the build is what was wanted, and the story loses its *observed* mark;
- **fix** — the build is wrong, and a queued slice corrects it;
- **change request** — the requirement is wrong (`writ/spec/changes/`);
- **leave open** — nobody present can decide, and it goes to whoever can.

**The build is evidence, never authority.** A description of the code reads plausibly and gets
agreed with, and that is how a specification becomes whatever was built, bugs included. Only the
specification's owner ratifies.

**The decisions land in the file's *Reconciliation* table**: one row per slice that built the
requirement against an older reading of this file, dated no earlier than `revised_on`. `holds` is
the row for a slice nothing conflicts with. Each work order records `detail_read_on`, the day it
read these files, so the check can tell which slices those are. **Every revision re-dates every
row** after re-reading that slice. A row older than the file is a statement about a file that no
longer exists.

**How hard this is held is `requirements.out_of_order`**: `fail` for a project that started in
order, `backfill` for one whose build runs ahead, `report` for one that has not chosen. Under
`backfill` the unreconciled requirements are a queue in `COVERAGE.md`, most urgent first, and a
milestone cannot be marked `done` until the requirements aimed at it have caught up. In every mode
but `report`, a reviewed file that a slice has drifted from fails.

## Verifying one

`/requirement-verify <id>` runs against a requirement the ledger reads as `●` satisfied — an
annotated test names it and the slice claiming it is done. It reads **one** requirement's file, its
tests and its code, and answers one question: *is the behaviour this file describes actually there?*

Four verdicts, and they go in the file's `## Verification` table:

| Verdict | Means |
|---|---|
| `implemented` | The observable behaviour is present and the boundary cases hold |
| `gap` | Partly present; the gap is named precisely enough to become a work item |
| `absent` | The requirement is credited as satisfied and the behaviour is not there |
| `detail-wrong` | The file was wrong about the requirement, and the file is what gets fixed |

It is **report-only**, in the way `/manual-test` is. It never edits code, never edits the
specification, and never quietly relaxes a detail file to match what was built. A `gap` goes to the
slicer as a work item; a `detail-wrong` goes back through the drafting step above, which moves
`revised_on`, which fails the scenarios file read before it — so the correction reaches the test
team through the check and not through memory. A verification row on its own moves nothing: it
records what was found and changes no claim.

Run it **per phase gate**, over the requirements that turned `●` during the phase. Not per slice: a
requirement is usually finished by several slices, and verifying one half-built produces a finding
about the queue rather than about the product.

## What the check enforces

`python3 scripts/ledger.py check` — the same command CI runs — fails on any of:

- a file named for an identifier the specification does not declare, or one outside the covered
  families
- a file in the wrong area directory, or whose front matter disagrees with its own filename
- a missing front-matter field, a `status` outside `draft|reviewed`, or a `reviewed` file naming no
  approver
- a phase that disagrees with the specification's
- **a quoted requirement that is not the specification's text, character for character**
- a missing template section, **a file that tells no story**, or a verification verdict outside
  the four above
- a *Reconciliation* row with no date, nobody who decided it, or a decision outside `holds`,
  `ratified`, `fix`, `change-request` and `open`; a `fix` naming no slice, a `change-request`
  naming no request, or an `open` row on a reviewed file naming no registered question
- whatever `requirements.out_of_order` holds it to (above): a slice claimed for an undetailed
  requirement, a slice built against an older reading and not reconciled, a closed milestone not
  caught up

`COVERAGE.md` grows one section from the same data: how many files exist, how many are reviewed,
every satisfied requirement with no reviewed file behind it, **what was built ahead of any detail
file** — the backfill queue, most urgent first — and **what was built against an older reading**.
Each list is a backlog, listed rather than averaged away. `python3 scripts/ledger.py stats` adds
whether the backfill is catching up with the build, week by week.

## What this is not

It is not the specification, and it is not a PRD. It adds no requirement, changes no scope and sets
no priority — the moment it does, it is a specification with no owner. It sits beside the BRD
because that is where a reader looks for what a requirement means, and it borrows none of the
BRD's authority by sitting there: the quote check is what keeps the two apart.

**It is not the test cases either.** Those are `writ/qa/scenarios/`, one file per requirement again,
written from this one and holding what somebody does at a keyboard — in what order, with which
accounts, through the product's own screens. The split is deliberate: what a requirement means is
settled here by the specification's owner, and what a session covers is the test manager's.

It is not `MANUAL-REGRESSION.md`, which is the short list of by-hand scenarios worth re-running, and
it is not the oracle set in `.claude/skills/manual-test/reference/areas.md`, which is what an
exploratory walk predicts against. **An invariant's oracle is cited from here, never copied.** Three
copies of what "correct" means is three documents that drift.
