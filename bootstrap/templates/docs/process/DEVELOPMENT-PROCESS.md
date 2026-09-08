# Development process

> **Status:** active. This is *how* we build. `spec/BRD.md` is *what* we build and *why*;
> `spec/MILESTONE-PLAN.md` is *what structure* this milestone builds; `SLICE-QUEUE.md` is
> *in what order*.
> **Precedence:** `BRD.md` > `MILESTONE-PLAN.md` > `SLICE-QUEUE.md` > this document. Where this
> conflicts with any of them, they win and this gets corrected.
> **Divergence:** the queue may depart from the milestone plan only by logging it in
> `MILESTONE-PLAN.md` §9 **and** amending the affected section there in the same change.
> **Identifier convention:** every identifier is prefixed and declared in `spec/ID-REGISTRY.md`.
> **Team shape:** <one engineer plus coding agents | N engineers plus coding agents>.

## 1. The document model

**Anything an agent must know to write correct code lives in the repository.** A coding agent reads
the working tree, not an issue tracker. Context that lives only in a ticket is context the primary
implementer cannot see.

| Artefact | Location | Answers | Lifetime |
|---|---|---|---|
| **BRD** | `docs/spec/BRD.md` | What the product must do, and why | Amended, never forked |
| **Milestone plan** | `docs/spec/MILESTONE-PLAN.md` | What structure this milestone builds | Per milestone |
| **Foundation specs** | `docs/spec/<AREA>-SPEC.md` | The shapes everything inherits | Amended in place |
| **ADRs** | `docs/decisions/NNNN-*.md` | Why one option was chosen over the others | Immutable; superseded, never edited |
| **Work order** | `docs/process/work-orders/<N>.md` | What this slice will do, and how it will be proven | Committed before the code |
| **Slice summary** | `docs/process/slices/<ID>.md` | What changed, what was decided, what surprised us | Permanent |
| **Coverage ledger** | `docs/process/COVERAGE.md` | What is actually proven | Generated every slice |
| **Requirement detail** | `docs/process/requirements/<area>/<id>.md` | What a person would see if this one requirement held | Amended when the requirement is |
| **Agent map** | `CLAUDE.md` | Where everything is and what the conventions are | Read at the start of every session |

The repository holds truth; the issue tracker holds narrative and linkage. The slice summary is
committed **in the slice's own commit** and *then* posted as a comment. The repository copy is the
record; the comment is the notification.

## 2. The unit of work is a slice

> **A slice is the thinnest change that alters what the system can do, end to end, and can be
> exercised by hand.**

Requirements and slices are many-to-many. Requirements are the coverage ledger — the checklist that
decides whether a milestone is done. Slices are the work queue — the order in which we build.

### 2.1 Sizing

The binding constraint: **a diff one person can read carefully in under thirty minutes.** This is a
comprehension budget, not a productivity target — the limit exists precisely because agents can
produce far more than that per session.

**The measure is added code lines**: lines added outside test files, comments, blank lines and
generated artefacts. Record the total diff beside it; do not govern by it.

| Size | Added code lines | Shape |
|---|---|---|
| **S** | under <150> | One module, one concept |
| **M** | <150>–<400> | The default. One capability across two or three components |
| **L** | over <400> | Needs justification in the work order *and* a stated reason it cannot be split |

A work order states both numbers: *"M — 268 code lines, 709 in the diff."*

If a slice cannot be demonstrated, it is a task — fold it into the slice it serves. If it exceeds
**L**, it is two slices that have not been separated yet. Recalibrate these tiers from measurement
after the first ten slices, and record the recalibration here.

## 3. The slice loop

| # | Step | Owner | Output |
|---|---|---|---|
| 1 | **Pick** | Human | One slice from `SLICE-QUEUE.md` |
| 2 | **Work order** | Human + agent | `work-orders/<N>.md`, branch, draft PR |
| 3 | **Plan** | Agent proposes, **human reads** | A file-level implementation plan |
| 4 | **Implement** | Agent | Code and tests in one pass |
| 5 | **Verify** | Automated | The gate |
| 6 | **Play** | **Human, by hand** | The demo from step 2, executed |
| 7 | **Close** | Human + agent | Summary, ledger, commit, PR merged |

### 3.1 Step 2 — the work order

Twenty minutes, one page, written **before any code**. It fixes: which requirements are advanced,
what changes in the published contract, the size, numbered acceptance criteria, the demo, and what
is out of scope.

> **The acceptance criteria become the test names at step 4.** This is the only mechanism keeping
> the work order honest rather than decorative. If a criterion cannot become a test name, it is not
> written precisely enough yet.

**An ADR named in the front matter must exist before implementation begins.** A decision recorded
after the fact is a justification; the record is only worth keeping if it precedes the code it
governs. `ledger.py check` enforces this.

**And the requirements are read against the plan, not only for coverage** (`DoD-12`). The question
is not which requirements this slice advances — the front matter answers that — but whether the plan
would make one **false**. The ones it will make false are the invariants governing the areas the
slice changes, and an invariant is a shape rather than a capability, so it belongs to no requirement
area a slicer would think to search. **A conflict is the slicer's to resolve: name the requirement,
name the part of the plan, name the two answers, and stop.** Never take the reading that makes the
plan work, and say *no conflicts* out loud when there are none — a silent check reads exactly like
one that never happened.

### 3.2 Step 3 — read the plan

The cheapest comprehension the process offers. A plan the reader cannot follow is a signal that the
slice is too large or the design is wrong — and saying so costs a conversation, where saying it at
step 5 costs the slice.

### 3.3 Step 6 — play

Non-negotiable, and never delegated. Automated tests prove the system does what we told it to do;
step 6 is where the human finds out what we told it.

## 4. Definition of done

A slice is done when **all** of the following hold. Not most.

| ID | Condition |
|---|---|
| DoD-1 | Every acceptance criterion has a corresponding passing test, named with its requirement id |
| DoD-2 | The full local gate is green: <the gate commands> |
| DoD-3 | <The crown-jewel invariant suite> is green |
| DoD-4 | <Any published contract> validates against its generated document |
| DoD-5 | The demo ran, by hand, and did what the work order said it would |
| DoD-6 | Every decision with a credible rejected alternative has an ADR, written **before** the code |
| DoD-7 | The slice summary is committed to `docs/process/slices/<ID>.md` and the ledger regenerated |
| DoD-8 | `CLAUDE.md` reflects any new structure, package or convention |
| DoD-9 | Committed with the trailer block (§6.3); the pull request closes the issue |
| DoD-10 | Any `MANUAL-REGRESSION.md` entry this slice's changes touch was re-run and re-dated; a demo worth keeping was promoted into that file |
| DoD-11 | Any invariant this slice established or changed has its oracle in `.claude/skills/manual-test/reference/areas.md` added or updated |
| DoD-12 | Every requirement the slice touches — its claims, **and every invariant governing the areas it changes** — was read against the plan for conflict before implementation began, and any conflict was raised with the slicer rather than resolved in the work order |

`DoD-12` is worth its line because the requirement a plan breaks is almost never one the plan
claims. The shape, seen in a real project: a decision recorded an amount of money in one country's
minor units with no currency stored anywhere — against a P0 invariant saying country-specific facts
are configuration, never assumptions baked into the product. Every requirement the slice claimed had
been read carefully; none of them pointed at it, because an invariant is a shape rather than a
capability and so belongs to no requirement area a slicer would search.

It is met **at step 2a, before the work order is drafted**, and `/slice-open` reports it either way.
A conflict found at close is a finding rather than a tick: say which requirement the shipped code
makes false and take it to the slicer. It is never closed by reinterpreting the requirement.

## 5. The play harness

Built early, before there is much to exercise: the local stack, seeded fixtures using **the same
seed the automated suite uses**, a <Dev CLI name> that grows one verb per slice, and request files or
a scratch page for poking at things.

Every demo-facing command takes `--json` and prints exactly one object, so a script can capture an
identifier rather than asking the reader to paste one.

### 5.1 Demo scripts accumulate; they do not evaporate

By slice forty there are forty proofs scattered across forty closed issues, none executed since the
day it was written. `MANUAL-REGRESSION.md` holds the ones worth re-checking, kept alive by DoD-10
and **kept short by deletion**.

When the suite is green and nobody has looked at the product in three weeks, the process has failed
even though every gate is passing.

### 5.2 `/manual-test` is the harness pointed at itself

A demo proves the slice did what its work order said. It cannot reach what nobody wrote a step for:
the interleavings, the mid-flight state changes, and the compositions **between** slices that no
single slice's tests build.

`/manual-test` walks those — a seeded random walk over a real, isolated instance, drawing a
perturbation and a target at each step, predicting the outcome from a written oracle before running
anything, and classifying every mismatch before it is allowed to become a finding. The seed and the
step counter are the whole reproduction, so a finding is repeatable rather than anecdotal.

It is **report-only**: it never edits the repository, and promoting a finding into
`MANUAL-REGRESSION.md` stays a human's call. Its oracles live in
`.claude/skills/manual-test/reference/areas.md`, seeded from this project's invariants at bootstrap
and kept true by DoD-11.

## 6. Traceability

### 6.1 Annotations

Requirement identifiers appear in **test names**, because the test is the proof:

```
it('[FR-ACC-01] refuses a second account for the same address', ...)
```

Source comments may reference an identifier. Source annotations are optional; tests are not.

**Never put an annotation-shaped string in a test file that is not a real test.**

### 6.2 The coverage ledger

`python3 scripts/ledger.py` generates `COVERAGE.md` from four sources: the registry, each family's
declaring section, work-order front matter, and annotated test names. It is generated rather than
maintained because a hand-kept matrix always drifts, and a drifting matrix is worse than none — it
invites false confidence.

**A `satisfies` claim with no test behind it is recorded as partial and listed.** A ledger that
believes its own work orders is a spreadsheet.

### 6.3 Commit trailers

One commit per slice, squashed:

```
feat(accounts): refuse duplicate addresses at the database

Sign-up now fails closed on a unique violation rather than checking first,
which removes the race between the check and the insert.

Slice: SL-C3
Satisfies: FR-ACC-01, FR-ACC-02
Partial: INV-1
Decision: ADR-0004

Closes #14
```

`Closes #14` is last and has no colon — that is the form the issue-closing parser wants. The lines
above it are trailers, so `git log --grep 'FR-ACC-01'` answers *where did this get built*.

**Attribution:** <no agent attribution anywhere in git or the tracker | the default co-author trailer
is kept>. Chosen at bootstrap; `CLAUDE.md` §Git carries the same answer.

## 7. Decisions — ADRs

**Write an ADR when you rejected a credible alternative.** The test: would a competent engineer
arriving in six months reconstruct this choice from the code, or re-litigate it?

Immutable once accepted; superseding is a new record. The *Alternatives rejected* table is the
reason the record exists.

An ADR never contradicts a `D-*`. If one would, the `D-*` is amended first.

## 8. Version control

**No change reaches `dev` or `main` except through a pull request.** This holds for solo work, for
documentation, and for one-line fixes.

| Branch | Role |
|---|---|
| `main` | Releasable. Only receives merges from `dev`, at phase or milestone boundaries |
| `dev` | Integration. The base for every slice, and the default branch |
| `slice/<ID>-<slug>` | One per slice |
| `docs/<slug>` | Specification and process changes that are not a slice |

Squash into `dev`; merge `dev` into `main` without squashing. The branch and a **draft** pull
request open at step 2, so the diff arrives against a stated intent instead of explaining itself.

After a merge: `git checkout dev && git pull --ff-only && git fetch --prune`, then `git branch -D`
the merged branch — squash merging means branch commits are never ancestors of `dev`, so `-d`
refuses and locals accumulate.

## 9. Automate the ceremony or it will rot

`/slice-open <id>` drafts the work order from the queue and opens the branch and draft PR.
`/slice-close` drafts the summary from the diff, regenerates the ledger, walks the definition of
done, and drafts the commit. **The human still edits both.** The automation removes the friction,
not the judgement.

Two more run **outside** the loop, because what they do does not belong to any one slice:

| | |
|---|---|
| `/maintenance` | the standing passes — a behaviour-preserving cleanup, the product documentation regenerated from the code, and a security audit. Each on its own branch, merged before the next starts |
| `/manual-test` | the seeded walk of §5.2 |

Both keep standing records rather than one-off reports, which is the whole point of them:
`docs/process/maintenance/cleanup-backlog.md` and `security-backlog.md` are what stop each run
re-deriving the same judgement, and re-fixing the thing a previous run deliberately left alone.

## 10. What is never delegated

1. Writing and approving the work order. Deciding *what* is a human act.
2. Reading the plan before implementation.
3. Playing with the result.
4. Reviewing every foundation spec and every ADR, line by line.

The characteristic failure of a build with coding agents is velocity outrunning comprehension: a
codebase that works, that nobody understands, and that therefore cannot be safely changed.

## 11. Cadence

**Per slice** — the loop. **Per phase** — read the ledger against the phase's exit criterion;
confirm the queue ahead; retire manual-regression entries an automated test now covers; **run
`/requirement-verify` over the requirements that turned `●` during the phase** (§12).
**Per milestone** — measure against the exit criterion, not against the number of merged slices.

**On a cadence of its own** — `/maintenance`, <as often as the team agreed>. It is nobody's slice
and it closes no issue, so it consumes no WIP; it is also the only thing that ever looks at a file
nobody has touched, which is exactly where the things it finds live.

**When the suite is green and nobody has played with the product** — `/manual-test`. That state is
undetectable by any gate, which is why it needs a cadence rather than a trigger.

## 12. The requirement detail track

Parallel to the loop, and owned by the specification's owner rather than by the slicer.
`docs/process/requirements/README.md` is the whole process; this section says why it exists and
where it touches this document.

A requirement in the specification is one line, because a BRD states business intent. That is
enough to build against and not enough to **test** against by hand: it names no actor, no
precondition, no observable outcome and no boundary. Nothing else here fills the gap — §2 says
requirements and slices are many-to-many by design, so a work order spans several requirements and
proves only the claims it made. Read a slice to test a requirement and you get part of an answer
with no way to know which part is missing.

So: one file per requirement, named for it, under `docs/process/requirements/<area>/`. It says what
a person would see if the requirement held, and manual cases are written from it.

**It never restates the requirement in its own words.** The file quotes the specification's row
verbatim and `ledger.py check` compares it character for character, so an amendment fails every
file that has not been re-read. That check is the only thing standing between the directory and a
shadow specification with no owner.

Two things this deliberately does **not** do:

- **It is not in the definition of done.** Coupling a slice to the detail of every requirement it
  touches puts the specification's owner on the critical path of every merge, which is the serial
  process this replaces. The track runs one phase ahead of the queue instead.
- **It is not read during a slice.** `/requirement-detail <id>` — which reads the requirement back
  in eight lines and interviews its owner rather than handing them a finished document — and
  `/requirement-verify <id>` each take one identifier and read one file. An implementation session
  that opened the directory would be holding thirty requirements it does not need. The one
  exception is `DoD-12`: a slice reads the *reviewed* detail files of the requirements it claims,
  because their observables are where a conflict shows up first.

`/requirement-verify` is the other half, and it is what §4's `DoD-1` cannot reach: a requirement
that reads `●` in the ledger is one whose *claims* are tested, which is not the same as one whose
behaviour is there. It runs per phase gate over the requirements that turned `●` during the phase,
it is report-only in the way `/manual-test` is, and its verdict goes in the file. A `gap` is a work
item for the slicer; an `absent` is a requirement credited as done that is not.
