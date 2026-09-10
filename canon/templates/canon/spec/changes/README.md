# Change requests

> **Status:** active from launch.
> **Role:** after the first release, the registers under `../` are the store and **a change request
> is the unit of change** — one file per change, holding the rows it adds, amends or withdraws,
> accepted by the specification's owner and then applied mechanically. The narrative `BRD.md`
> is never edited for one.
> **Owner:** <the specification's owner> decides; anybody may draft, with `/change-request`.
>
> Delete this blockquote.

## Why this exists

The BRD is a document authored once, by people arguing the case for a product. Requirements keep
arriving for the life of the product, and each one edited into that document makes it less the
thing it was and more a ledger nobody can read. So the two jobs are separated: the registers are
the living truth, the narrative freezes at launch, and every change to the registers arrives as a
small file with its own identifier that says what, why, and who agreed.

## Layout

```text
changes/CR-NNN-<slug>.md        CR-012-a-second-location.md
```

Numbered in the order they are raised, three digits, never reused. The front matter's `id` is the
authority; the filename carries it so a directory listing reads as a log.

## What one holds

Copy `../../process/templates/change-request.md`. Four sections, and the check wants all four:

| Section | Holds |
|---|---|
| **The job** | When, who needs to, so that — the way a detail file tells it. Who asked, and the evidence |
| **Changes** | A table: `add`, `amend` or `withdraw`, the identifier, the text, the target milestone. New identifiers take the next number in their area |
| **Impact** | Existing requirements it touches, the invariants read against it for conflict, and the detail files and scenarios it makes stale |
| **Decision** | Who decided, when, and what they said. The front matter carries the status |

**The conflict read happens here, at proposal time**, when it is cheapest — the same question
`/slice-open` asks at step 2a, against the invariants and the neighbouring requirements, before
anybody has built anything on the answer.

## Lifecycle

| Status | Means | Who sets it |
|---|---|---|
| `draft` | Written, not yet read by the owner | the drafter |
| `reviewed` | Read, corrections made, not yet decided | the owner |
| `accepted` | Approved — and the rows are now applied, in the same change | the owner, with `approved_by` and `decided_on` |
| `rejected` | Declined, with the reason in *Decision*. The file stays | the owner |

**Applying an accepted request is mechanical, and the check enforces it.** The added and amended
rows land in their registers with `Since: CR-NNN`; withdrawn ones get `Status: withdrawn`; one
row goes in `../CHANGELOG.md` naming the request and the identifiers; `python3 scripts/ledger.py`
regenerates the index. An accepted request whose rows are not in the registers fails the check,
and so does a register row that says `Since: CR-NNN` while the request is still a draft.

**The request's own state is derived, never written down.** `../../INDEX.md` shows each one as
*applied* when its rows exist and *built* when every one of its identifiers reads satisfied in the
coverage ledger. "Did the change we agreed in January ship" is a lookup.

## Then the machinery you already have

The new identifiers are detailed with `/requirement-detail`, the slicer cuts work orders that
claim them, tests annotate them, the coverage ledger marks them. Nothing downstream is different
for a requirement that arrived by change request rather than in the first specification, except
that `Since` says where it came from.

## What this is not

It is not a way to change the narrative. `BRD.md` is re-cut at a milestone boundary when the
story genuinely changed, as a version bump logged in the changelog — not one request at a time.

It is not a place to decide what the product does in prose. A request that cannot be expressed as
rows to add, amend or withdraw is either a decision, which is an ADR, or a question, which is a
row in `../questions.md`.
