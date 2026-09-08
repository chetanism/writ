# Requirement detail

> **Status:** active from <DATE>.
> **Role:** one file per requirement, saying what a person would **see** if it held — so a manual
> test case can be written from it, and so a finished requirement can be checked against the
> product rather than against its own tests.
> **Owner:** <the person who owns the specification>. <In team mode, name the two who may draft and
> approve; solo, the one human is the approver and the agent is the drafter.>
> **Precedence:** `docs/spec/BRD.md` wins over everything here, always. See *The one rule* below.

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

So: one file per requirement, named for it, elaborating it in the application's terms. It is the
**hand-testing half** of the ledger, and `docs/process/COVERAGE.md` is the mechanical half.

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
docs/process/requirements/<area>/<id>.md      FR-ACC/FR-ACC-01.md, INV/INV-1.md
```

The area is the identifier without its number, so nothing has to be kept in step with it. The check
fails if a file sits in the wrong directory, is named for an identifier the specification does not
declare, or is named for one that has since been withdrawn — which is how a struck-through
requirement's file gets found rather than quietly outliving it.

**Covered families are `FR` and `INV`** — the requirements and the invariants a person can be asked
to exercise. Not `NFR`, `DoD` or the process families: those name mechanisms and process rules, and
a mechanism is tested through the requirement it serves. The covered set is
`requirements.families` in `scripts/ledger.config.json`; changing it is a decision, not a
configuration tweak.

## Who does what

| Step | Who |
|---|---|
| Draft the file | Anybody, with `/requirement-detail <id>` — it is a draft, not an answer |
| Correct it, and decide what the requirement actually means | The specification's owner |
| Approve it — `status: reviewed`, `approved_by:` filled | The specification's owner, and not the same person who drafted it where that is possible |
| Write manual test cases from it | Whoever tests by hand |
| Verify a finished requirement against the product | `/requirement-verify <id>`, run by anybody; the finding goes to the slicer |

**Manual cases are written only from a `reviewed` file.** A draft is an agent's reading of a
one-line requirement, and an agent's reading is exactly the thing this track exists to have a human
correct.

## When

**One phase ahead of the queue.** While phase F is being built, the next phase's requirements are
being detailed. That keeps the track genuinely parallel — nothing in the slice loop waits on it,
and nothing here waits on a slice.

It is deliberately **not** in the definition of done. Coupling a slice to the detail of every
requirement it touches would put the specification's owner on the critical path of every merge,
which is the serial process this replaces.

Do not bulk-generate the whole specification. Four hundred requirements drafted by an agent and read
by nobody is not coverage; it is a directory that looks like coverage, which is worse than an empty
one. Draft what the phase in view needs.

## Drafting one

**It is a conversation, and the file is what it leaves behind.** Nobody reads ninety generated
lines carefully; a reviewer handed a plausible document agrees with it, which is the failure this
track exists to avoid.

1. `/requirement-detail FR-ACC-01` — it reads the requirement's row, the specs that govern the
   area, the slices that claim it and the tests that name it, and then **reads the requirement back
   to you in eight lines**: what it says, where it can be exercised today, who acts, what it appears
   to mean, and what it leaves unsettled.
2. **It interviews you** — two to four numbered questions at a time, each carrying the answer it
   would pick and why, so you can reply *"1 yes, 2 the second one, 3 ask the owner"*. It reads the
   observable behaviours back as a numbered list before committing them, because that list is what
   a manual case is written from and it is where your knowledge is worth the most.
3. It writes the file and reports what changed, rather than reciting it.
4. Fill `approved_by` and set `status: reviewed`.
5. `python3 scripts/ledger.py check`, then a pull request into `dev` like any other change.

**"I don't know" is a real answer**, and the honest one — it lands in *Open questions* addressed to
whoever owns it. An answer that would change what the product *does* is a specification amendment:
it says so rather than quietly writing it down here. **The parts an agent gets wrong are the same
every time**, so those are the questions it will ask: who may *not* do the thing, what happens at
the boundary, and what the requirement does not say.

**What a good file looks like** — every line in *Observable behaviour* can be **wrong**. *"The
queue updates correctly"* cannot be. *"A second desk advancing the same record against a stale
version is refused, and the refusal names the version it read"* can be, and a tester knows what to
do with it.

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
slicer as a work item; a `detail-wrong` goes back through the drafting step above.

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
- a missing template section, or a verification verdict outside the four above

`COVERAGE.md` grows one section from the same data: how many files exist, how many are reviewed,
and every satisfied requirement with no reviewed file behind it. That list is the track's backlog,
listed rather than averaged away.

**`require_detail_for_satisfied` in `scripts/ledger.config.json` is `false`.** Turn it to `true`
once the backlog in that section is cleared, and from then on a requirement cannot read as satisfied
without a reviewed file behind it. Turning it on with a backlog only breaks the gate for work
nobody has been asked for yet.

## What this is not

It is not the specification, and it is not a PRD. It adds no requirement, changes no scope and sets
no priority — the moment it does, it is a specification with no owner.

It is not `MANUAL-REGRESSION.md`, which is the short list of by-hand scenarios worth re-running, and
it is not the oracle set in `.claude/skills/manual-test/reference/areas.md`, which is what an
exploratory walk predicts against. **An invariant's oracle is cited from here, never copied.** Three
copies of what "correct" means is three documents that drift.
