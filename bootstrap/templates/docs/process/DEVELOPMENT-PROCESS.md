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
| **Work order** | `docs/process/work-orders/<N>.md`, mirrored as the tracker issue's body | What this slice will do, and how it will be proven | Committed before the code |
| **Slice summary** | `docs/process/slices/<ID>.md`, the pull request's description at merge, and an issue comment | What changed, what was decided, what surprised us | Permanent |
| **Coverage ledger** | `docs/process/COVERAGE.md` | What is actually proven | Generated every slice |
| **Requirement detail** | `docs/process/requirements/<area>/<id>.md` | What this one requirement means — the job, told as stories, and who is turned away | Amended when the requirement is |
| **Test scenarios** | `docs/qa/scenarios/<area>/<id>.md` | What somebody does at a keyboard to find out whether it holds | Re-read when the detail file moves |
| **Agent map** | `CLAUDE.md` | Where everything is and what the conventions are | Read at the start of every session |

The repository holds truth; the issue tracker holds narrative and linkage. The slice summary is
committed **in the slice's own commit** and *then* posted as a comment. The repository copy is the
record; the comment is the notification. The same holds for the issue's body, which is the work
order file re-synced at the claim and at the close: where the two differ, the file is right.

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
| 2 | **Work order** | Human + agent | `work-orders/<N>.md`, the issue, branch, draft PR |
| 3 | **Plan** | Agent proposes, **human reads** | A file-level implementation plan |
| 4 | **Implement** | Agent | Code and tests in one pass |
| 5 | **Verify** | Automated | The gate |
| 6 | **Play** | **Human, by hand** | The demo from step 2, executed |
| 7 | **Close** | Human + agent | Summary, ledger, commit; PR carries the summary, merged, issue closed |

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
| DoD-9 | Committed with the trailer block (§6.3), the pull request description is the summary, and — where a tracker is configured — the merge closes the issue |
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

`Closes #14` is last and has no colon — that is the form the issue-closing parser wants. **14 is
the work order's `issue:`, never the pull request's number**: GitHub draws both from one sequence,
so a wrong number is a valid one pointing at nothing, and nothing fails. Without a tracker the line
is omitted. The lines above it are trailers, so `git log --grep 'FR-ACC-01'` answers *where did
this get built*.

**The squash merge discards this block unless told otherwise.** With one commit on the branch a
squash reuses its message; with more it uses the pull request's title and nothing else — and a
slice branch always has at least two, the claim and the close. So the close commit's message is
also written to `.git/SLICE_MSG`, and the merge is `gh pr merge --squash --body-file .git/SLICE_MSG`.
`/slice-close` hands that command over; the default one silently loses the trailers and leaves the
issue open.

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
| `req/<id>` | One per requirement in the detail track — the identifier lowercased and nothing else, so §12's branch is computed from the identifier rather than searched for |
| `qa/<id>` | The same, for the manual test scenarios written from that requirement's detail file (§13) |
| `docs/<slug>` | Specification and process changes that are not a slice |

Squash into `dev`; merge `dev` into `main` without squashing. The branch and a **draft** pull
request open at step 2, so the diff arrives against a stated intent instead of explaining itself.
Its description is the work order at open and the slice summary at close, so the merge is reviewed
against what was built rather than against what was planned.

### 8.1 The tracker

<Where a tracker is configured — `tracker` in `scripts/ledger.config.json`:> one issue per slice,
opened at the claim with the work order file as its body, labelled by phase and size, and closed by
the merge through the trailer's `Closes #N`. `issue:` in the work order's front matter is where the
number lives, and `ledger.py check` fails a claimed slice that has none — so the number exists
before the branch does and the close has something to resolve. The issue is re-synced from the
file at close and gets the summary as a comment. It is never the place a claim is made, a decision
is recorded, or a plan is changed: it does not survive a clone, and forty closed issues are a worse
record than one file each. Maintenance, requirement and scenario pull requests get no issue.

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
confirm the queue ahead; retire manual-regression entries an automated test now covers; **run the
scenarios that turned `Ready` during the phase** (§13), and **run `/requirement-verify` over the
requirements that turned `●`** (§12). **Per milestone** — measure against the exit criterion, not
against the number of merged slices.

**The order in which one requirement's documents arrive is fixed; the moment each arrives is
not.** The requirement is declared, its detail file is drafted and approved, the slice that builds
it gets a work order, the scenarios are written from the detail file and cut by the test manager,
the code lands with its summary, the scenarios are run, and at the phase gate the requirement is
verified — with every finding flowing back to the detail file rather than being settled downstream.
That is a cadence, not a gate. Slices and requirements are many-to-many, so a slice never waits on
every requirement it touches being detailed, and a detail file never waits on a slice. What keeps
the order honest is that each document is the input the next one reads, and that `/slice-open`
says out loud, for every requirement a slice claims, which of those documents exist yet.

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
the requirement means — the job somebody is doing, told as stories, who must be turned away, and
what happens at the edges — and the test scenarios (§13) are written from it.

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
  because their stories and observables are where a conflict shows up first.

**A requirement is one branch.** `req/<id>` off `dev`, created when the interview starts and pushed
with its pull request once the file is written — a detail file is settled over more than one
sitting, so naming the branch for the requirement rather than the sitting is what lets the second
sitting find the first. Re-opening one whose pull request is still open checks that branch out
again; an uncommitted tree stops that and asks. `traceability.yml` refuses a detail file arriving
on any other branch, so this is a check rather than a convention. The README holds the table.

`/requirement-verify` is the other half, and it is what §4's `DoD-1` cannot reach: a requirement
that reads `●` in the ledger is one whose *claims* are tested, which is not the same as one whose
behaviour is there. It runs per phase gate over the requirements that turned `●` during the phase,
it is report-only in the way `/manual-test` is, and its verdict goes in the file. A `gap` is a work
item for the slicer; an `absent` is a requirement credited as done that is not.

## 13. The manual test scenario track

Written from §12's output, and owned by the test manager rather than by the specification's owner.
`docs/qa/README.md` is the whole process; this section says why it exists and where it touches this
document.

A detail file settles what a requirement **means**. It is still not a test session: it names no
build, no accounts, no order to do things in, and nothing about what somebody can actually reach.
Early on, much of a product is a command line and whoever tests it has a browser, so a detail file
read at a keyboard becomes an hour of deciding what to try next — which is how two testers cover
two different things and neither knows what the other left out.

So: one file per requirement under `docs/qa/scenarios/<area>/`, holding the scenarios themselves —
what somebody does, in what order, and what they should see.

**Two properties are checked rather than trusted, because both fail silently.**

- **A scenario is done through the product's own screens.** No terminal, no database, no
  command-line tool. Setup that genuinely cannot be reached that way goes under *Before you start*,
  addressed to whoever prepares the environment, and `ledger.py check` fails a file that puts one in
  a scenario. A file of unrunnable scenarios looks exactly like coverage.
- **A file of nothing but happy paths fails.** It is the natural thing to write and the least useful
  thing to run.

**When: after the detail file is reviewed, and the natural moment is the claiming slice's work
order being approved.** A scenario has to name the part of the product that owns the behaviour, and
the work order is often where that is settled — written before it, every scenario rests on a guess
about the screen. Written after it, the scenarios are ready the week the slice merges. Either way
they are never on the slice's critical path: the work order does not wait for them, and they do not
wait for the code.

**The return path is enforced, not remembered.** A scenarios file records which detail file it read
and when. It fails the day that file is approved, and it fails the day that file's claims change —
`revised_on` in the detail file's front matter, moved by every amendment — so a `detail-wrong`
verdict at the phase gate reaches the scenarios through the check rather than through somebody's
memory. `/slice-close` names the scenarios a slice has just unblocked, so they are run against the
build that unblocked them.

Two things it deliberately does **not** do, both inherited from §12:

- **It is not in the definition of done**, and it does not gate a merge.
- **It is not read during a slice.** `/test-scenarios <id>` takes one identifier and reads one
  requirement's detail file.

**A requirement is one branch here too** — `qa/<id>` off `dev`, and `traceability.yml` refuses a
scenarios file arriving on any other. It is written from the detail file and from nothing else: a
scenario that decides what the product does is a specification with no owner, so where the detail
file is silent the question goes back to it rather than being answered in a test case.

**Solo, the track waits for a second pair of hands.** The implementer playing the demo is `DoD-5`,
and a scenarios file earns its place only when somebody who did not build the behaviour runs it.
Until that person exists the skill is installed, the directory is empty, and nothing here is
missing.
