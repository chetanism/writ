# `/prelaunch`

**The one-shot pre-production scrub — squash the migration chain to a clean baseline, remove dead
compatibility and backfill code, and fix code written against live-data assumptions. Run once,
before the first production deploy; it refuses to run twice.**

| | |
|---|---|
| **Run it** | Once, after the last pre-launch slice merges and before the first deploy. Never after launch |
| **Produces** | A squashed baseline migration chain, deleted compat code, fixed first-boot bugs — on a branch through a pull request |
| **Refuses to** | Run when a `pre-launch scrub` commit already exists, or when the project has deployed. Squash by eye without the schema-equivalence proof |
| **Installed** | Always — emitted in phase 9 beside the standing skills, with no question asked |

## Why it is a skill and not a slice

Three things a greenfield build accumulates are only true before launch: a migration chain full
of reversals (migration-6 adds a column, migration-10 removes it), compatibility code for data
that never existed (dual-read paths, backfill scripts for an empty production database), and code
written against a live system that is not live yet (tables assumed non-empty, jobs assumed
already run). A slice cannot own this work — it spans the whole tree, crosses every area, and its
migration half is forbidden the day after launch. So it is a standing skill with a one-shot rule
instead: the gate is the deploy, not a cadence.

## The three parts

1. **Squash the migration chain** — no-op pairs collapse to nothing, every change moves to its
   logical position, and the result is proven by building a fresh database from the old chain and
   the new one and diffing the schemas. After this merges, migrations are additive-only.
2. **Remove dead compatibility code** — dual-write paths, backfill scripts, `legacy` markers
   that describe the build era rather than the product. Seeds must boot an empty-but-valid
   system; anything richer belongs in test factories.
3. **Fix live-data assumptions** — the first-boot test (wipe, migrate, seed, boot, exercise
   every critical path with zero user data) turns each false assumption into a concrete failure,
   and the pass fixes it.

## Why it is not in `/maintenance`

`/maintenance` runs on a clock, forever; this runs once, on a gate. Its marker —
`pre-launch scrub` — is not a baseline for a next run but a lock that refuses one. It lands
through the same `delivery.md` as the passes, so *how* it merges never drifts from them.

## See also

[`/cleanup`](cleanup.md) — the behaviour-preserving pass that owns migration hygiene after
launch · [`/manual-test`](manual-test.md), whose isolated instance is the other half of the
first-boot discipline
