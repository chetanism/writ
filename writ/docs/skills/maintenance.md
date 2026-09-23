# `/maintenance`

**Runs all four standing passes in order — `/cleanup`, `/product-docs`, `/security-audit`,
`/context-compact` — each on its own branch and merged before the next starts, then reports across
them.**

| | |
|---|---|
| **Run it** | For a scheduled full maintenance run. To run one pass alone, invoke that pass's own skill |
| **Produces** | Four merged pull requests and one report across all four |
| **Owns** | `delivery.md` — the shared loop for how any pass branches, commits, opens a PR and merges |

## Why the four are separate skills

**So each can run on its own cadence and be handed to its own owner.** A security audit and a
documentation refresh have nothing in common except that neither belongs to a slice; forcing them
into one command means they run at the same frequency, which is the frequency of whichever one is
most annoying.

This skill exists for the full run, **where the order carries weight**, and for the report across
all four.

## Why the order is fixed

Each pass changes the input of the next one.

1. **`/cleanup`** first, so everything downstream reads a simplified tree rather than one mid-change.
2. **`/product-docs`** next, describing what is there after the cleanup rather than before it.
3. **`/security-audit`** third, auditing code that is not about to be rewritten by the pass ahead of
   it.
4. **`/context-compact`** last, because the three passes above may each add to `CLAUDE.md`.

And each is **merged before the next starts**, so no pass reviews a tree that contains another
pass's unreviewed work.

## `delivery.md`

The shared loop: branch, commits, pull request, merge. It exists so that *how a pass lands* is
written once rather than four times and drifting in three of them. It defers to `CLAUDE.md` for
project conventions, and it is explicit that the slice trailer block does not apply to a
maintenance pass — a pass is nobody's slice, closes no issue and consumes no WIP.

## Velocity, after the passes

The run ends with `python3 scripts/velocity.py --check`: a flag when last week's code fell well
below the weeks before it, or when the Markdown written per slice outgrew the code. A flag is a
finding for a person, never something the run fixes — and it never goes in the gate.

## See also

[`/cleanup`](cleanup.md) · [`/product-docs`](product-docs.md) ·
[`/security-audit`](security-audit.md) · [`/context-compact`](context-compact.md)
