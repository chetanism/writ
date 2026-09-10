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

> Written when the phase that builds this requirement comes into view, **before** the work starts
> and never during it. Drafted with `/requirement-detail <ID>`, then read and corrected by the
> person the `status` field is about.
>
> **This file never restates the requirement in its own words.** The specification says what the
> product must do; this says what somebody would see if it were true. Where the two disagree the
> specification is right and this is corrected — and where the specification is the one that is
> wrong, its owner amends it, not this file.
>
> **Two readers, one file.** The stories are what a product conversation is held over and what a
> screen is built and reviewed against. The three sections after them are what the test scenarios
> are written from. Neither half is optional, and neither repeats the other.
>
> Delete this blockquote.

## The requirement

> <the second cell of the requirement's row in `docs/spec/BRD.md`, verbatim — quoted, never
> reworded. `ledger.py check` compares this against the specification character for character>

## Summary — the job to be done

**When** <the situation that puts somebody in front of this job>, **<the persona> needs to** <the
outcome they are after, in their own words, not the system's> **so that** <why it matters — what it
costs them when the job goes undone>.

<Then two or three lines on where they meet it today: the screen, the desk, the phone call, the
paper it replaces. Written for somebody who has read nothing else.>

## Personas

*(The specification's stakeholder or persona section — quote their row, never paraphrase it into a
new description)*

> **May and May not are the half a story does not carry.** A story says what somebody does; these
> two say what happens when the wrong person tries. Both are needed, and the second is where the
> defects are.

| Persona | Relation to this job | May | May not |
|---|---|---|---|
| **<name>** (*"<the relevant clause of their row, quoted>"*) | **Does the job.** <where and how, in the product as it is today — not as it is imagined to be> |  |  |
| **<name>**, where the job has one | **Receives the outcome.** <what changes for them once it is done> |  |  |

## Mandatory and non-mandatory fields

> What somebody has to fill in, and what they may leave blank. A field nobody can leave blank is a
> field that stops the desk when it is unknown, so the second column is a decision rather than a
> formality.

| Field | Mandatory? | If it is left blank |
|---|---|---|
|  |  |  |

## Preconditions and data

<What has to exist before any of this can happen: an account, a role, the core object, a seeded
artefact. Name the command that creates each one where there is one. The stories below say *Given*
per story; this is the setup they all share.>

---

## Story 1 — <what this story is for, five words>

**Job:** When <situation>, I want to <action>, so <outcome>.

- **Given** <the state the world is in before this story starts>
  **When** <what the person does — described as doing the thing, never as running a particular
  command, unless the command line really is the surface today>
  **Then** <what becomes true, where they can see it>
  **And** <a second consequence, where there is one>

<One story per distinct situation, numbered in the order somebody meets them. Each one has to be
checkable on its own: if nobody could tell whether it happened, it is not written finely enough yet.
`ledger.py check` fails a file with no story in it — a requirement nobody could tell a story about
has not been understood yet.>

---

## Observable behaviour

> **Only what no story above reaches.** The stories are the ordinary path; this is the rest of the
> truth — the timing, the sameness, the things that hold across every story at once.
>
> **Numbered, and each one checkable.** *"Sign-in works"* is not one. *"An address nobody holds and
> a wrong password come back the same, and take the same time"* is. `None — the stories cover it.`
> is a real answer and a good one.

1.
2.

## Boundary and negative cases

> The ones no story reaches, because a story is written about somebody who is doing the job
> properly. Delete the rows that do not apply and add the ones that do — an empty row is worse than
> a missing one.

| Case | Expected |
|---|---|
| Another tenant's data, or another tenant's address |  |
| Somebody who is not a member, or whose account was turned off |  |
| The same request sent twice |  |
| Two people changing one record at once |  |
| A value at its limit — empty, longest allowed, expired |  |

## Out of scope

<What this requirement does **not** say, especially where a neighbouring one says it. This is the
fence that stops the file growing into a second specification.>

## Open questions

> Where the drafter could not tell what the requirement means, the question goes here — never a
> guess written as though it were settled. **A question about what the product should do belongs
> to the specification's owner**, and it is answered by amending the specification rather than by
> answering it here. Name who it is for. `None.` is a normal entry.

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
