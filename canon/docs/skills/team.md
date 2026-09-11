# `/canon:team`

**Everything `/canon:solo` does, plus the part that only exists here: a pipeline with named roles,
explicit handoffs, WIP limits, parallel-safety and CODEOWNERS.**

| | |
|---|---|
| **Run it** | Once, at the start of a greenfield project more than one person will build |
| **Takes** | Longer than solo — phase 3 is an extra interview about who does what |
| **Produces** | The solo tree, plus roles in the process document, `owner:` and `touches:` on work orders, a WIP limit, and CODEOWNERS |
| **Never** | Starts on its own |

## What is different

**Choose this at the start rather than promoting later, because roles and handoffs are the
expensive retrofit.** The tool's own team features — the WIP limit and `touches` collision
detection — are genuinely cheap to switch on afterwards, but the *agreements* are not: who approves
a work order, who owns the specification, who decides a change request, and what a handoff between
two people actually consists of.

| | |
|---|---|
| **Phase 3 — Roles and handoffs** | The interview solo does not have. Who slices, who approves, who owns the spec, who runs the test sessions |
| **Parallel-safe slicing** (phase 7) | The queue is ordered for *dependency* in solo and for dependency **and contention** here — two people should be able to take the top two slices without touching the same files |
| **`touches:` on work orders** | Declared file scope, so a collision is detected at claim time rather than at merge |
| **A WIP limit** | Contention management. It is what `wip_limit` in the config actually drives |
| **CODEOWNERS** | The gate roles from phase 5, expressed where GitHub will enforce them |

## Sizing the team honestly

**A five-person team where one person is actually going to run this should install
[`/canon:solo`](solo.md), not this.** Team mode is about contention, and contention needs a crowd;
turning it on for one person is overhead with no failure to prevent.

Promotion later is cheap and worth knowing about in advance: in the tool, `mode` decides only
whether the queue renders an Owner column, and both real team checks key off `wip_limit` being
non-zero. So the move is: set `mode`, set `wip_limit`, start writing `owner:` and `touches:` on new
work orders. Nothing is retrofitted and no existing slice becomes invalid.

## See also

[`../references/08-team-pipeline.md`](../../references/08-team-pipeline.md) — roles, handoffs,
claiming work and CODEOWNERS, argued out. [`/canon:adopt`](adopt.md) if the codebase already
exists and the team has not agreed to any of this yet.
