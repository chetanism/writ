# Slice queue

> **Status:** active.
> **Role:** in what order we build. **Sequence is the commitment; sizes are estimates.** The table
> is generated from work-order front matter: edit the work order, then run
> `python3 scripts/ledger.py`. Reasoning does not live here — an out-of-order run is one note
> below, linking the ADR that argued it, and a departure from the milestone plan is a line in
> `../spec/CHANGELOG.md`.
> **Precedence:** the registers > `../spec/BRD.md` > `../spec/MILESTONE-PLAN.md` > this document.
>
> Delete this blockquote.

## Reading the identifiers

> | Form | Is | Example |
> |---|---|---|
> | `SL-NNN` | A slice — a global number, zero-padded, that encodes nothing else | `SL-042` |
> | `slice/NNN-slug` | Its branch | `slice/042-rls-policies` |
> | `work-orders/<milestone>/<phase>/NNN.md` | Its work order, filed under the phase its front matter declares | `work-orders/m1/P02/042.md` |

**Numbered at creation, positioned by need.** A slice is never renumbered: its id is in test names,
commit trailers and the ledger. A slice created forty-second may run sixth, and the table says so.
A slice that moves phase keeps its number; a split mints two fresh ones. The phase is the column
beside it, never part of the name.

## Reading the dependency column

| Mark | Needs | Typical wait |
|:--:|---|---|
| **—** | Nothing but a laptop and this repository | none |

> The marks are `../spec/MILESTONE-PLAN.md` §6's, one row each.

## The queue

<!-- generated:queue -->
<!-- /generated -->

## Notes

> One paragraph per out-of-order run, at most, naming the slice and the ADR that carries the
> reasoning. Nothing else goes here: a queue whose order is partly explained in prose is a queue
> that gets re-derived, differently, by whoever reads it next.

- **`SL-NNN` runs <where> rather than <where the phase order puts it>** — `ADR-NNNN`.
