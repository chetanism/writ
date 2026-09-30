# `/product-docs`

**Regenerates the living product documentation from the code — what the product *is today* and how
it is built, for the team building it. Never a changelog.**

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

**The team building the product — developers, engineering and product managers, and whoever joins
next month.** The test is whether that newcomer could read it end to end and know what the product
does and how — which is a much harder test than it sounds, because the people writing it cannot
un-know the context.

**Not the product's own users.** Documentation addressed to both the team and the customers serves
neither: the team skims past the instructions, and the customer is handed an entity diagram when they
wanted to know which button to press. The users have [`/product-guide`](product-guide.md), which
lives in `docs/documentation/guides/`. This pass never writes there, and a sentence that tells
somebody what to do with the product open goes to the guide, as a link.

## Why it is incremental

It updates only what changed since the last pass. A full regeneration each time produces a diff
nobody can review, which means nobody reviews it, which means the documentation is only as good as
the generation — and it is documentation, so it is not.

## See also

[`/maintenance`](maintenance.md) and [`/product-guide`](product-guide.md). Note that this writes under `docs/`, which is deliberately kept
free of the `writ/` tree — the specification and the product documentation have different readers
and different lifetimes.
