---
id: CR-<NNN>
status: draft                # draft | reviewed | accepted | rejected
requested_by: <name>
approved_by: ""              # required once accepted or rejected
decided_on: ""               # YYYY-MM-DD, required once accepted or rejected
target: <M2>                 # the milestone the change is aimed at; a declared one
---

# CR-<NNN> — <what changes, five words>

> Written with `/change-request`, read and decided by the specification's owner, and applied to
> the registers **in the same change as the acceptance**. `canon/spec/changes/README.md` is the
> process. This file is the argument for one change; the registers are where the change lives
> once it is agreed.
>
> Delete this blockquote.

## The job

**When** <the situation>, **<the persona> needs to** <the outcome, in their words> **so that**
<why it matters>.

<Who asked for it, and the evidence: the customer, the support thread, the number. Two or three
lines.>

## Changes

> One row per register row this touches. `add` takes the next free number in the area. `amend`
> carries the full new text, not a diff. `withdraw` carries the reason in *Decision*. The
> identifier column is what the check reconciles against the registers once this is accepted.

| Op | ID | Text | Target |
|---|---|---|---|
| add | <FR-AREA-NN> | <One sentence, behaviour not implementation.> | <M2> |

## Impact

- **Touches:** <existing requirements this changes the meaning of, by identifier>.
- **Read against the invariants:** <each `INV-*` governing the area, and whether the change would
  make it false. Name a conflict here and stop; do not resolve it in this file>.
- **Goes stale:** <the detail files and scenario files that will need re-reading once this is
  applied — their `revised_on` and `detail_read_on` are what carry that>.
- **Out of scope:** <what a reader might think this covers and it does not>.

## Decision

<Empty while `draft` or `reviewed`. Once decided: who, when, and in a sentence what they said —
including the reason for a rejection. The reasoning behind an accepted change that rejected an
alternative is an ADR, cited here.>
