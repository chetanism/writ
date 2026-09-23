# `/writ:solo`

**Interviews one developer and writes their new project's whole development process — specification,
registers, identifier registry, dependency-ordered slice queue, CI gate, coverage ledger and fourteen
project skills tuned to the answers.**

| | |
|---|---|
| **Run it** | Once, at the start of a greenfield project one person plus their agents will build |
| **Takes** | About an hour. Two paragraphs about the product is a sufficient input; a written BRD shortens it |
| **Produces** | A `writ/` tree, `CLAUDE.md`, `.github/workflows/`, `scripts/`, fourteen skills — committed on `dev` |
| **Never** | Starts on its own. All three bootstrap skills are user-invoked only |

## What happens

Ten phases. You answer questions; it writes documents; nothing is decided silently.

| Phase | What it settles |
|---|---|
| 0 | The tree's name, where things go, and whether any of the fourteen skill names collides with one you already have |
| 1 | The BRD — obtained, or built from what you can tell it |
| 2 | Adaptive scoping: what this is, what it explicitly is not, who it is for |
| 3 | Security, **conditioned on your domain** — it asks the questions your profile earns and skips the rest |
| 4 | Reliability: availability, RTO/RPO, idempotency, backpressure, scale, observability |
| 5 | The stack and the gate roles — and it **runs each command** rather than believing your README |
| 6 | The specification set: registers, invariants, foundation specs, the registry |
| 7 | Slicing: the queue, dependency-ordered and sized, with `SL-000` shipping the tooling before any feature |
| 8 | Emission: config, workflows, `CLAUDE.md`, the loop skills |
| 9 | The standing passes, tuned to the cadence you say you will keep |
| 10 | The requirement detail track, if you want it |

## Three things worth knowing before you start

**It asks rather than assumes, and *I do not know* is a real answer.** An unanswered question
becomes a row in `writ/spec/questions.md` with an owner. That is a much better outcome than a
guess, because a guessed availability target or a guessed volume gets built against, tested against
and staffed against by everything downstream, and nobody remembers it was a guess.

**Slice zero ships the tooling.** The gate, the registry and the ledger are a named slice with its
own acceptance criteria, before any feature slice. In the process this was extracted from the
ledger arrived at slice eight and the migration lint at slice eighteen, which meant the first
seventeen slices were never actually held to the rules.

**It can be resumed.** `.writ-interview.md` is appended after every phase, offered back at phase 0
if the session ran out, and deleted at the commit.

## After it finishes

It hands over and stops. Add a remote and branch protection if there is none yet, then
[How to use it](../using-it.md#2-the-loop) is the next page.

## See also

[`/writ:team`](team.md) if more than one person will build it — the roles and handoffs are far
harder to retrofit than to choose. [`/writ:adopt`](adopt.md) if the code already exists.
