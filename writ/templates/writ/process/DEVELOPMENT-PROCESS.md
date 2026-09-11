# Development process

> **Status:** active. This is *how* we build. The registers under `spec/` are *what* we build and `spec/BRD.md` is *why*;
> `spec/MILESTONE-PLAN.md` is *what structure* this milestone builds; `SLICE-QUEUE.md` is
> *in what order*.
> **Precedence:** the registers > `BRD.md` > `MILESTONE-PLAN.md` > `SLICE-QUEUE.md` > this document. Where this
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
| **BRD** | `writ/spec/BRD.md` | Why — the case for the product, in prose. Declares nothing | Frozen at launch; re-cut at a milestone boundary |
| **Registers** | `writ/spec/requirements/<AREA>/index.md`, `invariants.md`, `questions.md`, … | What — one table of identified rows each, with `Since` and `Status` columns | Living; after launch changed only through a change request |
| **Changelog** | `writ/spec/CHANGELOG.md` | What changed, when, touching what — one line per amendment | Append-only |
| **Change request** | `writ/spec/changes/CR-NNN-*.md` | One post-launch change to the registers, and who agreed to it | Immutable once decided |
| **Index** | `writ/INDEX.md` | Where every identifier is declared and what state it is in | Generated every slice |
| **Milestone plan** | `writ/spec/MILESTONE-PLAN.md` | What structure this milestone builds | Per milestone |
| **Foundation specs** | `writ/spec/<AREA>-SPEC.md` | The shapes everything inherits | Amended in place |
| **ADRs** | `writ/decisions/NNNN-*.md` | Why one option was chosen over the others | Immutable; superseded, never edited |
| **Work order** | `writ/process/work-orders/<milestone>/<phase>/<N>.md`, mirrored as the tracker issue's body | What this slice will do, and how it will be proven | Committed before the code |
| **Slice summary** | `writ/process/slices/<milestone>/<phase>/<ID>.md`, beside its work order in the mirrored tree; the pull request's description at merge, and an issue comment | What changed, what was decided, what surprised us | Permanent |
| **Coverage ledger** | `writ/process/COVERAGE.md` | What is actually proven | Generated every slice |
| **Requirement detail** | `writ/spec/requirements/<area>/<id>.md` | What this one requirement means — the job, told as stories, and who is turned away | Amended when the requirement is |
| **Test scenarios** | `writ/qa/scenarios/<area>/<id>.md` | What somebody does at a keyboard to find out whether it holds | Re-read when the detail file moves |
| **Agent map** | `CLAUDE.md` | Where everything is and what the conventions are | Read at the start of every session, and held under the budget in `scripts/ledger.config.json` |

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

**And the front matter carries them, so the budget is checked rather than remembered.** `estimated`
is written at step 2 and `code_lines` at step 7, and `ledger.py check` refuses a work order whose
`size` is not the tier its measurement falls in — the same disbelief the ledger applies to a
`satisfies` claim, pointed at the claim a slice makes about its own size. The tiers live in
`size_budget` in `scripts/ledger.config.json`; an empty object turns the check off.

`estimated` is **never corrected afterwards**. A slice that was guessed at 140 and came in at 287
is an `M` whose estimate missed, and both facts are worth having: the first is what the queue
should show, the second is the only evidence these tiers can be recalibrated from. Editing the
estimate to match the outcome is how a process quietly stops being able to learn.

If a slice cannot be demonstrated, it is a task — fold it into the slice it serves. If it exceeds
**L**, it is two slices that have not been separated yet — and an `L` that does land states, in its
Size section, why it could not be split; the check fails one that says only what it measured.

**Recalibrate these tiers from measurement after the first ten slices**, and record the
recalibration here. `python3 scripts/ledger.py stats` is what to read: it reports the median in
each tier, how often the estimate held, and how often a slice came in over. Three misses in the
same direction is a finding about the tiers rather than about a slice.

## 3. The slice loop

| # | Step | Owner | Output |
|---|---|---|---|
| 1 | **Pick** | Human | One slice from `SLICE-QUEUE.md` |
| 2 | **Work order** | Human + agent | `work-orders/<milestone>/<phase>/<N>.md`, the issue, branch, draft PR |
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

The third column says **what would notice if it did not** — and it is the most important column in
this document.

| ID | Condition | Caught by |
|---|---|---|
| DoD-1 | Every acceptance criterion has a corresponding passing test, named with its requirement id | the gate runs the tests · **you** that each criterion has one |
| DoD-2 | The full local gate is green: <the gate commands> | the gate |
| DoD-3 | <The crown-jewel invariant suite> is green | the gate |
| DoD-4 | <Any published contract> validates against its generated document | the gate |
| DoD-5 | The demo ran, by hand, and did what the work order said it would | **you** — the check reads the demo's *shape*, never that anybody ran it |
| DoD-6 | Every decision with a credible rejected alternative has an ADR, written **before** the code | `ledger.py` that a named record exists · **you** that it preceded the code, and that the decision was named at all |
| DoD-7 | The slice summary is committed to `writ/process/slices/<milestone>/<phase>/<ID>.md`, mirroring the work order, and the ledger and `writ/INDEX.md` regenerated | `ledger.py` |
| DoD-8 | `CLAUDE.md` reflects any new structure, package or convention — **in one line, replacing whatever it supersedes**, and still under its budget | `ledger.py` the budget · **you** that it reflects anything |
| DoD-9 | Committed with the trailer block (§6.3), the pull request description is the summary, and — where a tracker is configured — the merge closes the issue | `ledger.py` that a claimed slice names an issue · **you** the rest |
| DoD-10 | Any `MANUAL-REGRESSION.md` entry this slice's changes touch was re-run and re-dated; a demo worth keeping was promoted into that file | **you** |
| DoD-11 | Any invariant this slice established or changed has its oracle in `.claude/skills/manual-test/reference/areas.md` added or updated | `drift.py` that an oracle is not *stale* · **you** that a missing one gets written |
| DoD-12 | Every requirement the slice touches — its claims, **and every invariant governing the areas it changes** — was read against the plan for conflict before implementation began, and any conflict was raised with the slicer rather than resolved in the work order | **you** — `/slice-open` asks and reports, and a report is not a proof |

### 4.1 Half of this is on your honour, and that is the design

Three rows are the gate's, three are half the tool's, and the rest are nobody's but yours. That is
worth saying out loud, because this process spends most of its words on machine-checked things —
*a ledger that believes its own work orders is a spreadsheet* — and a reader who absorbs that tone
without this paragraph will assume the rest is checked too. It is not, and the unchecked half is
where the value is.

**Nothing here can verify that a human did a human thing.** A demo can be recorded as run by
somebody who did not run it. A conflict read can be reported as clean by an agent that performed
it carelessly. A falsification section can be written without removing a single control. The tool
checks the *artefact* — that a demo section exists and carries no placeholder, that `/slice-open`
produced a conflict report, that a summary was committed — and the artefact is not the act.

This is not a gap to be closed. It is the reason the process is worth running: **the checkable
things are checked so that attention is left over for the things that cannot be.** Automating the
judgement out of DoD-5 or DoD-12 would not make them true, it would make them invisible — which is
exactly what a green gate over an unplayed demo already is. The defence is a named owner, §10's
list of what is never delegated, and the habit of saying which of these you actually did.

So: when you walk this list at close, **say `[you]` out loud on the rows that are yours** rather
than reporting the table as met. A definition of done reported in aggregate is a definition of done
nobody is applying, and the rows most likely to be waved through are precisely the ones no build
will ever fail on.

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

**Four states, and the middle two are opposite failures.**

| | | Means | What to do |
|:--:|---|---|---|
| `●` | satisfied | a slice claimed it and a test names it | nothing |
| `≈` | inherited | tests name it and no slice claims it | a work order the evidence already earned — see below |
| `◐` | partial | claimed and not proven, or proven in part | somebody promised this and has not delivered it |
| `○` | none | nothing claims it and nothing proves it | build it, or withdraw the row |

`≈` and `◐` were one state until this process had to run on a codebase older than itself.
Collapsing them reports every such repository as uniformly half-done, which is the one number
nobody can act on. Keep them apart: **`◐` is a broken promise and `≈` is unclaimed evidence**, and
only the first is anybody's fault.

A `≈` row is discharged by a **characterisation slice** — `kind: characterisation`, a slice that
changes no behaviour and writes down what the code already does. It is the only kind that may
declare `demo: none`, because there is nothing to play that was not playable yesterday. Its Demo
section instead says what was pinned and who confirmed that behaviour was wanted: **a test written
from the code asserts the bug exactly as confidently as the feature**, and afterwards the suite
defends it.

### 6.3 Commit trailers

One commit per slice, squashed:

```
feat(accounts): refuse duplicate addresses at the database

Sign-up now fails closed on a unique violation rather than checking first,
which removes the race between the check and the insert.

Slice: SL-042
Satisfies: FR-ACC-01, FR-ACC-02
Partial: INV-003
Decision: ADR-0004

Closes #14
```

`Amends: X-NNN` is present where the slice added a changelog line — an amended register, a
departure from the plan — and absent where it did not; it is how the amendment's commit is found.
`Closes #14` is last and has no colon — that is the form the issue-closing parser wants. **14 is
the work order's `issue:`, never the pull request's number**: GitHub draws both from one sequence,
so a wrong number is a valid one pointing at nothing, and nothing fails. Without a tracker the line
is omitted. The lines above it are trailers, so `git log --grep '<ID>'` answers *where did
this get built*.

**The squash merge discards this block unless told otherwise.** With one commit on the branch a
squash reuses its message; with more it uses the pull request's title and nothing else — and a
slice branch always has at least two, the claim and the close. So the close commit's message is
also written to `.git/SLICE_MSG`, and the merge is `gh pr merge --squash --body-file .git/SLICE_MSG`.
`/slice-close` hands that command over; the default one silently loses the trailers and leaves the
issue open.

**Attribution:** <no agent attribution anywhere in git or the tracker | the default co-author trailer
is kept>. Chosen at bootstrap; `CLAUDE.md` §Git carries the same answer.

### 6.4 The enforcement perimeter

`enforce` in `scripts/ledger.config.json` says which paths each rule is in force over. `default`
covers every rule not named; a named rule **replaces** the default for that rule rather than adding
to it, so a rule can be narrowed below the default as well as widened past it.

Only two rules are path-shaped — `annotations` and `work_order` — and that is not an oversight.
Ledger freshness, the placeholder scan and registry integrity are about this tree itself and are
always global; the size budget and the ADR rule are fields on a work order, so outside one there is
nothing to check.

A project that wrote its own first commit has no use for this and leaves it at `["**"]`. It exists
for the case where this process arrives in a repository other people are already working in, where
turning every rule on over somebody else's directory means their pull requests start failing for
rules that arrived in a commit they never read — which is how a process gets deleted in a week,
whatever its merits.

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
| `slice/<NNN>-<slug>` | One per slice, named for its number |
| `req/<id>` | One per requirement in the detail track — the identifier lowercased and nothing else, so §12's branch is computed from the identifier rather than searched for |
| `qa/<id>` | The same, for the manual test scenarios written from that requirement's detail file (§13) |
| `cr/<id>` | One per change request (§14) |
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

Six more run **outside** the loop, because what they do does not belong to any one slice:

| | |
|---|---|
| `/cleanup` | a behaviour-preserving cleanup of what changed since the last pass, and the cleanup backlog reconciled |
| `/product-docs` | the product documentation regenerated from the code — what the product is today |
| `/security-audit` | a security audit of what changed plus every open backlog row, with a dated report |
| `/context-compact` | `CLAUDE.md` compacted back under its budget: whole sections moved into the documents that own them, a pointer left behind, no fact lost |
| `/maintenance` | all four of the above in that order, each on its own branch and merged before the next starts — the order matters, because each reads the tree the previous one leaves |
| `/manual-test` | the seeded walk of §5.2 |

The four passes share one delivery loop, `.claude/skills/maintenance/delivery.md`, so how a pass
lands — the branch, the gate, the marker its commits carry, the merge — is written once. Three of
them keep a standing record rather than a one-off report, which is most of the point of them:
`writ/maintenance/cleanup-backlog.md` and `security-backlog.md` are what stop each run
re-deriving the same judgement, and re-fixing the thing a previous run deliberately left alone.
`/context-compact` keeps no backlog; the one-line pointer it leaves where a section used to be is
its record, and it is read by everyone rather than by the next pass.

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

**And at every phase gate, read `python3 scripts/ledger.py stats`.** Every other check here asks
whether the documents agree with each other, at one moment. That one asks whether this process is
still being followed, which is the question that goes wrong slowly and invisibly: the tiers nobody
recalibrated, the audit nobody has run since the spring, the detail track that stopped at
requirement nine, the backlog that only grows. It reports and never fails — an instrument that can
fail a build is a gate wearing a different name, and these are numbers to look at together rather
than thresholds to route around.

**The order in which one requirement's documents arrive is fixed; the moment each arrives is
not.** The requirement is declared, its detail file is drafted and approved, the slice that builds
it gets a work order, the scenarios are written from the detail file and cut by the test manager,
the code lands with its summary, the scenarios are run, and at the phase gate the requirement is
verified — with every finding flowing back to the detail file rather than being settled downstream.
That is a cadence, not a gate. Slices and requirements are many-to-many, so a slice never waits on
every requirement it touches being detailed, and a detail file never waits on a slice. What keeps
the order honest is that each document is the input the next one reads, and that `/slice-open`
says out loud, for every requirement a slice claims, which of those documents exist yet.

**On cadences of their own** — `/cleanup` <as often as the team agreed>, `/product-docs` <at each
phase gate, or as agreed>, `/security-audit` <as agreed, and after any dependency change>, and
`/context-compact` **whenever `ledger.py check` warns that the agent map is over budget** — the one
pass with a trigger rather than a clock, because `DoD-8` adds to that file every slice and nothing
else takes anything out; or all four at once with `/maintenance`. None is anybody's slice and none closes an issue, so they
consume no WIP; they are also the only things that ever look at a file nobody has touched, which
is exactly where the things they find live.

**When the suite is green and nobody has played with the product** — `/manual-test`. That state is
undetectable by any gate, which is why it needs a cadence rather than a trigger.

## 12. The requirement detail track

Parallel to the loop, and owned by the specification's owner rather than by the slicer.
`writ/spec/requirements/README.md` is the whole process; this section says why it exists and
where it touches this document.

A requirement in the specification is one line, because a BRD states business intent. That is
enough to build against and not enough to **test** against by hand: it names no actor, no
precondition, no observable outcome and no boundary. Nothing else here fills the gap — §2 says
requirements and slices are many-to-many by design, so a work order spans several requirements and
proves only the claims it made. Read a slice to test a requirement and you get part of an answer
with no way to know which part is missing.

So: one file per requirement, named for it, under `writ/spec/requirements/<area>/`. It says what
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
`writ/qa/README.md` is the whole process; this section says why it exists and where it touches this
document.

A detail file settles what a requirement **means**. It is still not a test session: it names no
build, no accounts, no order to do things in, and nothing about what somebody can actually reach.
Early on, much of a product is a command line and whoever tests it has a browser, so a detail file
read at a keyboard becomes an hour of deciding what to try next — which is how two testers cover
two different things and neither knows what the other left out.

So: one file per requirement under `writ/qa/scenarios/<area>/`, holding the scenarios themselves —
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

## 14. One kind of thing per file

Every document in `writ/` holds one of five kinds of thing, and `writ/spec/README.md` says which
file holds which: **narrative** that argues, **registers** that declare, **plans** that order,
**history** that records, and **elaboration** that explains one identifier. The failure this
prevents is the one every specification reaches by its second milestone: a BRD that is also its
own version log, a milestone plan that is also a risk commentary and an amendment essay, a queue
that is also the reasoning behind its order. Each of those is a file nobody can read for its
current state without reading its past.

**Status is a column.** A withdrawn requirement says `withdrawn` under `Status`, keeps its row and
its number, leaves the coverage ledger and can still be cited. A closed question says `closed`
and names what closed it. Nothing is struck through and nothing is deleted.

**History is one file.** `writ/spec/CHANGELOG.md` takes one line per amendment, whatever document
it amended, and the check holds it to a line: dated, touching identifiers that exist, short enough
that the reasoning has to go where reasoning lives — an ADR for a decision, a slice summary for a
finding. A register row's `Since` names the version, amendment or change request that introduced
it. A cell that carries history inline fails the build.

**One family per kind.** `Q-*` is every open question, `RSK-*` every risk, `X-*` every amendment,
wherever it arose; a `Scope` column says where. `ID-REGISTRY.md` fixes each family's width and the
check refuses an identifier outside it or carrying a suffix.

**Every identifier resolves, and one file lists them all.** An identifier cited anywhere under
`writ/` that nothing declares fails the check naming the file and line. `writ/INDEX.md` is
generated with the coverage ledger and byte-checked like it: one line per identifier, where it is
declared, its status, its coverage, its detail and scenario state, and the questions open against
it. It is the file to open first.

**After launch, the registers change only through a change request.** `writ/spec/changes/README.md`
is the process: one file per change with the rows it adds, amends or withdraws, decided by the
specification's owner, applied mechanically with `Since: CR-NNN` on every row and a changelog line,
and derived by the index as *applied* and then *built*. The narrative BRD is never edited for one.

## 15. Turning it down

A process nobody can turn down is one people route around, and routing around it is worse than
switching a part off — the switched-off part is a decision somebody can find, and the routed-around
part looks like it is still running. So each part has a switch, and what each costs is written
here rather than discovered.

| Turn off | How | What you lose |
|---|---|---|
| The tracker | `tracker: ""` | The issue mirror. `/slice-open` stops opening one, `DoD-9`'s second clause and §8.1 go, and the generated queue loses its Issue column. **The queue is still the board** |
| The requirement detail track | `requirements.dir: ""` | The quote check, and the file `/test-scenarios` and `/requirement-verify` read. Both skills stop having an input; `COVERAGE.md` loses a section |
| The scenario track | `scenarios.dir: ""` | The scenarios a tester is handed. `DoD-5`'s demo is then the only by-hand check of a requirement |
| Change requests | `changes.dir: ""` | The record of who agreed to a change, and the index's *applied* and *built* columns. Registers then change by editing them, and `Since` stops resolving to anything |
| The size budget | `size_budget: {}` | `estimated` and `code_lines` become prose. §2.1's tiers stop being checkable and stop being recalibratable |
| The context budget | `warn_chars: 0`, `max_chars: 0` | The only thing that ever says `CLAUDE.md` has grown too big. `DoD-8` still adds to it |
| The generated queue | `queue_out: ""` | The ordered table. `depends_on` is still read, and the order is still derived — there is just nowhere it is written down |
| A standing pass | delete its skill directory, and its row in `/maintenance` | That pass. The backlog it kept stops being reconciled and becomes a list |
| Enforcement, in part or whole | `enforce.default: []`, or a narrower path list per rule | Nothing, until somebody changes code inside the perimeter without a slice or adds a test naming no requirement. §6.4 |
| The whole tool | delete `scripts/` and the two workflows | Everything generated: `COVERAGE.md`, `INDEX.md`, the queue table. The documents remain and become hand-maintained, which is the state this was built to leave |

Three things have **no** switch, because each is load bearing for something else here:

- **The declaration rule.** Every tool, check and generated file reads it. Changing the registry's
  rows is how it bends; removing it is a rewrite.
- **`/context-compact`.** `DoD-8` adds a line to the agent map every time a slice establishes a
  convention and nothing else ever removes one. A project without the remedy has a file that only
  grows, and it is read at the start of every session.
- **The by-hand demo.** It is not enforced by anything (§4.1), which is exactly why it cannot be
  switched off: there is nothing to switch. It stops happening the day somebody stops doing it,
  and no gate will ever go red.

**Turning a part down is a decision, so record it.** A line in this document saying what was
switched off and why, and — where it was a gate role in §5 or a check — the same in `CLAUDE.md`,
so the next person reads *we chose not to* rather than *this seems to be broken*.

The same applies to turning something **on** — a new definition-of-done row, a widened perimeter, a
gate role added. This section is the register of what this team decided about its own process, not
only of what it removed.

**`/process-change` is how this section gets used.** It reads the rule and names the failure it was
written against; reads the change back as the table of files it would land in, before editing any
of them; applies it; records it here; and runs the check. That table is the point of the skill — a
change that lands in `scripts/ledger.config.json` and not in this document is an enforced rule
nobody agreed to, and one that lands here and not in the config is a documented rule the build
ignores. Both are silent.

Two things it never does: **edit `scripts/ledger.py`** — a skill that can change the tool that
checks it can make any process change pass, and a change that genuinely needs the tool changed is a
slice like any other — and **switch a check off to get a green run.** A process change is nobody's
slice: it consumes no WIP, advances no requirement and closes no issue.
