---
id: <FR-AREA-NN>
area: <FR-AREA>              # the identifier without its number. It is also the directory
phase: <V1>                  # mirrored from the requirement's row; the check fails if they disagree
status: draft                # draft | reviewed
drafted_by: <name>
approved_by: ""              # required once status is reviewed
reviewed_against: <1.0>      # the specification version this was read at
surface: []                  # where it can be exercised: a route, a command, a screen, the database
---

# <FR-AREA-NN> — <five words, what it is about>

> Written at whatever point the phase that builds this requirement comes into view, **before** the
> slices land, and never during one. Drafted by an agent (`/requirement-detail <ID>`), then read and
> corrected by the person the `status` field is about.
>
> **This file never restates the requirement in its own words.** The specification says what the
> product must do; this says what a person would see if it held. Where they disagree, the
> specification is right and this is amended — and where the specification is the one that is
> wrong, it is amended by its owner, not here.
>
> Delete this blockquote.

## The requirement

> <the second cell of the requirement's row in `docs/spec/BRD.md`, verbatim — quoted, never
> reworded. `ledger.py check` compares this against the specification character for character>

## What it means in the application

<Three to six lines: where a person meets this requirement — the screen, the route, the command —
and what it is for. Written for somebody who has read nothing else and has to test it.>

## Actors

| Who | May | May not |
|---|---|---|
|  |  |  |

## Preconditions and data

<What must already exist before this can be exercised: an account, a role, the core object, a
seeded artefact. Name the command that creates each one where there is one.>

## Observable behaviour

> **Numbered, and each one falsifiable.** *"Sign-in works"* is not an observable. *"An address
> nobody holds and a wrong password return the same bytes and take the same time"* is. These are
> what a manual test case is written from, one case per line or one case per few.

1.
2.

## Boundary and negative cases

> The ones a case written from the one-line requirement will not reach. Delete the rows that do not
> apply to this requirement and add the ones that do — an empty row is worse than a missing one.

| Case | Expected |
|---|---|
| Another tenant's data, or another tenant's address |  |
| An actor with no membership, or a deactivated one |  |
| The same request sent twice |  |
| Two people acting on one record at once |  |
| A value at its limit — empty, maximum, expired |  |

## Out of scope

<What this requirement does **not** say, especially where a neighbouring requirement says it. This
is the fence that stops the file growing into a second specification.>

## Open questions

> Where the drafter could not tell what the requirement means, the question goes here — never a
> guess dressed as a statement. **A question about what the product should do belongs to the
> specification's owner**, and it is answered by amending the specification, not by answering it
> here. `None.` is a normal entry.

## Related

<Identifiers, one line each: the `INV-*` invariants that govern it, the neighbouring requirements,
the slices that build it, and the oracle in `.claude/skills/manual-test/reference/areas.md` where
one exists. **An invariant's oracle is cited, never restated.**>

## Verification

> Written by `/requirement-verify <ID>`, run against a requirement the ledger reads as `●`. It is
> report-only: a finding goes back to the slicer as a gap, or to the specification's owner as an
> amendment.

| Date | Verdict | By | Evidence |
|---|---|---|---|
