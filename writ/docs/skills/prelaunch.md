# `/prelaunch`

**The one-shot pre-production scrub — squash the migration chain to a clean baseline, remove dead
compatibility code, sweep the whole tree for dead code, remove or lock down dev-only surface, and
fix code written against live-data assumptions. Run once, before the first production deploy; it
refuses to run twice.**

| | |
|---|---|
| **Run it** | Once, after the last pre-launch slice merges and before the first deploy. Never after launch |
| **Produces** | A catalogue you approve first, then a squashed baseline migration chain, deleted compat and dead code, guarded dev surface, fixed first-boot bugs — on a branch through a pull request — and a record in `writ/maintenance/audits/` |
| **Refuses to** | Run when its record already exists, or when the project has deployed. Change anything before the catalogue is approved. Squash by eye without the schema-equivalence proof |
| **Installed** | Always on a greenfield project — emitted in phase 9 beside the standing skills, with no question asked. Never on an adoption |

## Why it is a skill and not a slice

A greenfield build accumulates things that are only true before launch: a migration chain full
of reversals (migration-6 adds a column, migration-10 removes it), compatibility code for data
that never existed, modules and packages nothing reaches any more, surface that only made sense
while nobody else could reach the system, and code written against a live system that is not live
yet (tables assumed non-empty, jobs assumed already run). A slice cannot own this work — it spans
the whole tree, crosses every area, and its migration half is forbidden the day after launch. So
it is a standing skill with a one-shot rule instead: the gate is the deploy, not a cadence.

## Catalogue first

It reads the whole tree and lists everything it would change — the old chain against the new one,
every deletion with the evidence that nothing reaches it, every dev route and fallback — and
**stops for your approval before editing a file**. It is the one skill that rewrites migrations,
and most of what it deletes cannot be told apart from churn once it is gone.

## The five parts

1. **Squash the migration chain** — no-op pairs collapse to nothing, every change moves to its
   logical position, and the result is proven by building a fresh database from the old chain and
   the new one and diffing the schemas *and* the reference data migrations wrote. Every database
   that applied the old chain is rebuilt afterwards. After this merges, migrations are
   additive-only.
2. **Remove dead compatibility code** — dual-write paths, backfill scripts, API fields and route
   aliases kept for a client that never existed, `legacy` markers that describe the build era
   rather than the product. Seeds must boot an empty-but-valid system; anything richer belongs in
   test factories.
3. **Sweep the whole tree for dead code** — unused modules, dependencies and environment
   variables, and feature flags that hold one value everywhere. [`/cleanup`](cleanup.md) only
   sees what changed since its last pass, so this is the one whole-tree sweep a project gets.
4. **Remove or lock down dev-only surface** — debug and reset routes, verbose errors, permissive
   CORS, seeded accounts with known passwords, and configuration that falls back to a development
   value. Every required variable fails at boot, naming itself.
5. **Fix live-data assumptions** — the first-boot test (wipe, migrate, seed, boot, exercise every
   critical path with zero user data) turns each false assumption into a concrete failure, and the
   pass fixes it. It runs last because it is also the check on everything the first four removed.

## Why it is not in `/maintenance`

`/maintenance` runs on a clock, forever; this runs once, on a gate. Its record —
`writ/maintenance/audits/prelaunch-DATE.md` — is not a baseline for a next run but a lock that
refuses one. It lands through the same `delivery.md` as the passes, so *how* it merges never
drifts from them.

## See also

[`/cleanup`](cleanup.md) — the behaviour-preserving pass that owns migration hygiene after
launch · [`/manual-test`](manual-test.md), whose isolated instance is the first boot when it is
installed · [`/security-audit`](security-audit.md), which Part 4 does not replace
