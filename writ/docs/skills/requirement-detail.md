# `/requirement-detail`

**Works out with you what one requirement actually means — a short read-back, an interview in
rounds, and the file written last — so that code can be built against it and test scenarios can be
written from it.**

| | |
|---|---|
| **Run it** | One phase ahead of the queue, on a requirement a slice will soon build. `/requirement-detail FR-ACC-01` |
| **Produces** | One detail file under `writ/spec/requirements/<AREA>/`, on its own branch |
| **Refuses to** | Decide what the requirement means, guess an answer, accept what was built as what was wanted, or take more than one requirement at a time |

## What it does

1. **One requirement per run**, and it refuses the ones that are not its — a requirement outside the
   configured families, or one the registry does not declare.
2. **Reads only that requirement**, its area register and the invariants that govern it.
3. **Summarises it back in eight lines, before writing anything.** This is where most of the value
   is: an eight-line read-back of a one-line requirement is usually where somebody says *no, not
   quite* for the first time.
4. **Interviews in rounds of two to four numbered questions** — never a wall of forty.
5. **Writes the file**: the job, told as stories, and **who is turned away** — the part everybody
   forgets and testers need most.
6. **Does not guess.** An unanswered question stays a question with an owner.
7. **Looks at the build first.** Where a slice or a test already built the requirement, the order
   has broken and the draft is a **backfill**: stories read off the evidence, each marked
   *observed*, and every conflict with the build put to the owner — ratify it, fix it with a slice,
   change the requirement, or leave it open. The decisions land in the file's *Reconciliation*
   table, one row per slice.

## Why this track exists

**A requirement in a BRD is one line. That is enough to build against and nowhere near enough to
test against by hand.** A tester handed *the system must prevent duplicate accounts* has to invent
the actors, the boundaries and the failure modes, and two testers will invent different ones.

The detail file settles what the requirement means, once, in writing, with an approver — and the
argument is then not reopened downstream. [`/test-scenarios`](test-scenarios.md) reads it and
nothing else.

## The check behind it

**A detail file that quotes its requirement differently from the specification fails the build,
character for character.** That is the load-bearing check of the whole track: it is what turns an
amendment to a register into a red gate rather than a slow, silent divergence that nobody notices
until the scenarios are run against a requirement that changed a month ago.

The check also catches a file filed in the wrong area, named for an identifier the specification
does not declare, missing a front-matter field or a template section, marked `reviewed` with no
approver, or recording a verdict outside the four.

## When the build got there first

Implementation running ahead of its requirements is not an exception. It is what happens on a
project built with agents, and on every codebase adopted after the fact. The danger is quiet: a
detail file written after the code is easiest to write by describing the code, and a reviewer
handed a plausible description agrees with it. **The build is evidence, never authority**, so every
conflict is a decision for the owner, and the skill never ratifies anything itself.

The check keeps it honest. A work order records `detail_read_on` when it is claimed, and a slice
that read a detail file before its last revision needs a *Reconciliation* row saying whether its
build still holds. `requirements.out_of_order` sets how hard that is held: `fail` for a project
that started in order, `backfill` for one whose build runs ahead, `report` to only list it.
`DEVELOPMENT-PROCESS.md` §12.1 in the generated tree is the rule.

## It runs beside the loop, never waiting for approval inside it

One phase ahead of the queue. It consumes no WIP, and no merge waits on its approval. Slices and
requirements are many-to-many, so a slice never waits on every requirement it touches being
approved, and a detail file never waits on a slice. Under `out_of_order: fail`, a slice is claimed
only for a requirement that has a detail file, and a draft is enough.

## See also

[`/test-scenarios`](test-scenarios.md) — the next document in the chain.
[`/requirement-verify`](requirement-verify.md) — the phase-gate check that the behaviour is
actually there. [`../references/10-requirements.md`](../../references/10-requirements.md).
