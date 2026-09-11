# `/requirement-detail`

**Works out with you what one requirement actually means — a short read-back, an interview in
rounds, and the file written last — so that code can be built against it and test scenarios can be
written from it.**

| | |
|---|---|
| **Run it** | One phase ahead of the queue, on a requirement a slice will soon build. `/requirement-detail FR-ACC-01` |
| **Produces** | One detail file under `canon/spec/requirements/<AREA>/`, on its own branch |
| **Refuses to** | Decide what the requirement means, guess an answer, or take more than one requirement at a time |

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

## It runs beside the loop, never inside it

One phase ahead of the queue. It blocks no merge and consumes no WIP. Slices and requirements are
many-to-many, so a slice never waits on every requirement it touches being detailed, and a detail
file never waits on a slice.

## See also

[`/test-scenarios`](test-scenarios.md) — the next document in the chain.
[`/requirement-verify`](requirement-verify.md) — the phase-gate check that the behaviour is
actually there. [`../references/10-requirements.md`](../../references/10-requirements.md).
