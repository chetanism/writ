# The sixteen skills

**Three set the process up. Two run the loop. Four run beside it. Six run outside it. One changes
it.** One page each; the tables below are the whole map.

## Three that set it up

Run once, at the beginning, and never again. They are user-invoked only — Claude never starts one
on its own.

| | | |
|---|---|---|
| [`/writ:solo`](solo.md) | A new project, one person plus agents | The ten-phase interview |
| [`/writ:team`](team.md) | A new project, several people | The same, plus roles, handoffs, WIP limits and CODEOWNERS |
| [`/writ:adopt`](adopt.md) | A codebase that already exists | Survey it, document what the code cannot say about itself, enforce nothing on day one |

## Two that run the loop

The day-to-day. Everything else is optional; these two are the process.

| | | |
|---|---|---|
| [`/slice-open`](slice-open.md) | Step 2 | Drafts the work order, opens the branch and draft PR, **stops before any code** |
| [`/slice-close`](slice-close.md) | Step 7 | Summary from the diff, ledger regenerated, definition of done walked row by row |

## Four that run beside it

One phase **ahead** of the queue. They block no merge and consume no WIP.

| | | |
|---|---|---|
| [`/requirement-detail`](requirement-detail.md) | Before a slice builds it | What one requirement actually means, settled in writing |
| [`/test-scenarios`](test-scenarios.md) | Once the detail file is approved | The session a tester is handed |
| [`/requirement-verify`](requirement-verify.md) | At a phase gate | Is the behaviour actually there? Four verdicts, report-only |
| [`/change-request`](change-request.md) | After launch | The only way a register changes |

## One that changes the process

| | | |
|---|---|---|
| [`/process-change`](process-change.md) | When a rule does not fit | The change landed in **every** file it touches, recorded in §15, then checked |

## Six that run outside it

None is anybody's slice, none closes an issue, none consumes WIP. They exist because a gate cannot
detect the ways a project rots *between* slices.

| | | |
|---|---|---|
| [`/cleanup`](cleanup.md) | On a cadence | Behaviour-preserving; a backlog of what it deferred and what it settled |
| [`/product-docs`](product-docs.md) | At a phase gate | The product as it is today — never a changelog |
| [`/security-audit`](security-audit.md) | On a cadence, and after a dependency change | OWASP and CWE, plus every open backlog row |
| [`/context-compact`](context-compact.md) | **On a trigger** | The only thing that ever takes a line out of `CLAUDE.md` |
| [`/maintenance`](maintenance.md) | For the full run | The four above, in the order that matters, each merged before the next |
| [`/manual-test`](manual-test.md) | When the suite is green and nobody has played with it | A seeded random walk over an isolated instance |

---

**The thirteen project skills are emitted tuned to your interview** — names, commands, stack and
cadences all differ per project, and if a skill name collides with one you already have, phase 0
offers to rename the kit's. These pages describe what each one is for; the `SKILL.md` in your
repository is the authority on what yours actually does.

[← back to the documentation index](../README.md)
