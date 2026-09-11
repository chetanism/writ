# `/cleanup`

**A behaviour-preserving cleanup pass over what changed since the last one — simplifying code and
documents, resolving contradictions, and reconciling a backlog of what it deferred and what it
deliberately settled.**

| | |
|---|---|
| **Run it** | On a cadence your team agreed, or on demand. It is also the first of `/maintenance`'s four passes |
| **Produces** | A branch and a pull request, plus a reconciled `writ/maintenance/cleanup-backlog.md` |
| **Never** | Changes behaviour. That is the whole contract |

## What it does

**Scope detection first.** It finds the last commit that actually carried a cleanup pass, takes the
files changed since, and restricts everything to those. On a first run it does the whole repository
in reviewable chunks.

Then documents, then code, then verification, then delivery through
`.claude/skills/maintenance/delivery.md` — the shared loop that owns the branch, the commits, the
pull request and the merge, so that how a pass *lands* is written once rather than four times.

## The backlog is the interesting part

It has two tables that pull in opposite directions, and both are load bearing.

**Deferred** — work a previous pass judged worth doing and did not do. It is in scope **whether or
not its files are in this run's diff**, which is the reason the file exists at all: a skipped change
in a file nobody touches again would otherwise never be seen by any pass, forever.

**Settled** — structures a previous pass examined and deliberately left alone. **A pass does not
reopen one because a scan flagged it.** A duplicate-block scan, a dead-code scan and a link check
flag the same deliberate boundaries on every single run, and without a written answer each pass
re-derives the question until one of them helpfully "fixes" something load-bearing.

## Why it is a standing pass rather than part of the loop

**A gate cannot detect a file nobody has touched since the finding in it was introduced.** Every
check in the loop looks at what changed; this is one of the only things that looks anywhere else,
and that is exactly where the things it finds live.

It is nobody's slice, it closes no issue, and it consumes no WIP.

## See also

[`/maintenance`](maintenance.md) — all four passes in order, when the order carries weight.
