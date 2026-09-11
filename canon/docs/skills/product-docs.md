# `/product-docs`

**Regenerates the living product documentation from the code — what the product *is today*, for a
reader who has read nothing else. Never a changelog.**

| | |
|---|---|
| **Run it** | After a phase lands, or on demand. Also the second of `/maintenance`'s four passes |
| **Produces** | `docs/documentation/`, updated only where things changed, on a branch through a pull request |
| **Never** | Describes how the product evolved. That is what `CHANGELOG.md` and the slice summaries are for |

## The one rule

**A snapshot of the current state, never a history.**

This is the discipline that keeps product documentation readable, and it is the one that always
erodes. Documentation that accretes *and then in version 2.3 we moved this* becomes a geological
record: every reader has to reconstruct the present state by mentally replaying the past, and the
document gets longer forever. The history exists elsewhere and is better recorded there.

## Audience

**Engineers and product readers who have read nothing else.** Not the team. The test is whether
somebody joining next month could read it end to end and know what the product does — which is a
much harder test than it sounds, because the people writing it cannot un-know the context.

## Why it is incremental

It updates only what changed since the last pass. A full regeneration each time produces a diff
nobody can review, which means nobody reviews it, which means the documentation is only as good as
the generation — and it is documentation, so it is not.

## See also

[`/maintenance`](maintenance.md). Note that this writes under `docs/`, which is deliberately kept
free of the `canon/` tree — the specification and the product documentation have different readers
and different lifetimes.
