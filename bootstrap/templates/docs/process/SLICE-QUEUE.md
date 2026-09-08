# Slice queue

> **Status:** active.
> **Role:** in what order we build. **Sequence is the commitment; sizes are estimates.**
> **Precedence:** `spec/BRD.md` > `spec/MILESTONE-PLAN.md` > this document > everything else.
> **Divergence:** a departure from the milestone plan is logged in `MILESTONE-PLAN.md` §9 and the
> affected section there is amended in the same change. An unrecorded divergence is a defect, not
> a shortcut.
>
> **The table below is generated.** Edit the work order's front matter, then run
> `python3 scripts/ledger.py`. The prose around it is hand-written and is where the reasoning goes.

## Reading the identifiers

| Form | Is | Example |
|---|---|---|
| `SL-<PHASE><N>` | A slice | `SL-D3` |
| `slice/<PHASE><N>-<slug>` | Its branch — the short form, since `slice/` already namespaces it | `slice/D3-rls-policies` |

**Numbered at creation, positioned by need.** A slice is never renumbered: its id is in test names,
commit trailers and the ledger. A slice created sixteenth may run sixth, and the queue says so.

## Reading the dependency column

| Mark | Needs | Typical wait |
|:--:|---|---|
| **—** | Nothing but a laptop and this repository | none |

> Add a row per external track, matching `MILESTONE-PLAN.md` §8.

## Phases

| Letter | Name | Exit criterion |
|---|---|---|
| <F> | <Foundation> | <what must be true> |

> Choose phase letters that do not collide with your identifier families — if milestones are
> `M0..M5`, messaging cannot be phase `M`.

## The queue

<!-- generated:queue -->
<!-- /generated -->

## Out-of-order runs

> Every departure from phase order is written out here with its reason. A queue whose order is
> partly implicit is a queue that gets re-derived, differently, by whoever reads it next.

## Counts

| Phase | Slices | Blocked | Note |
|---|--:|--:|---|
