---
name: prelaunch
description: Run the one-shot pre-production scrub over this repository — squash the migration chain to a clean baseline, remove dead compatibility and backfill code, and fix code written against live-data assumptions — delivered on its own branch through a pull request. Use once, before the first production deploy; it refuses to run twice.
---

# Pre-launch scrub

You are performing the one-shot pre-production scrub of this repository. Invoked as `/prelaunch`,
once, before the first production deploy. **This file owns what changes.**
`.claude/skills/maintenance/delivery.md` owns the branch, the commits, the pull request and the
merge — read it first, and run this file inside its loop.

Your goal is to remove everything the build accumulated that is only true of an unlaunched
project: a migration chain full of reversals, compatibility code for data that never existed, and
code written against a live system that is not live yet.

> **Filled at bootstrap.** `<GATE COMMAND>`, `<MIGRATION TOOLING>`, `<SCHEMA DUMP COMMAND>` and
> `<SEED COMMAND>` come from the interview. Delete this blockquote once they are filled.

## The one-shot rule (read this first)

1. Find any commit whose message contains the phrase `pre-launch scrub`
   (`git log --grep="pre-launch scrub" --format=%H`). If one exists, **stop and report that the
   scrub has already run**, naming the commit. It does not run twice: after the first production
   deploy, history rewrites are forbidden and this skill's migration work becomes dangerous.
2. If the project has already deployed to production — a deploy marker, a release tag, live data
   behind the migrations — **stop and say so.** The scrub's squash step is only safe against a
   database that can be rebuilt from scratch. After launch, migration hygiene is additive-only
   (`/cleanup` scope), and assumption bugs are ordinary slices.

## Scope

The whole tree, in three parts, in order. Unlike `/cleanup` this pass is **not diff-scoped and
not behaviour-preserving** — fixing a false live-data assumption changes behaviour by definition.
That is the point. The gate and the schema-equivalence proof below are what keep it honest.

## Part 1 — Squash the migration chain

1. Read the migration history end to end. Catalogue every no-op pair: a migration that adds what
   a later one removes, creates what a later one drops, renames twice, or backfills data that no
   production database ever held.
2. Catalogue every misplaced change: a column, index or constraint added in a later migration that
   logically belongs to an earlier table definition.
3. Rewrite the chain into a clean baseline — one baseline migration per bounded context, or a
   single `0001_baseline` where the project is small — with the no-op pairs gone and every change
   in its logical position.
4. **Prove equivalence mechanically, never by eye:**
    - Build a fresh database from the old chain, dump its schema: `<SCHEMA DUMP COMMAND>`.
    - Build a fresh database from the squashed chain, dump its schema the same way.
    - The two dumps must be identical apart from migration metadata. If they differ, the squash
      is wrong — fix it, do not explain it.
5. Re-run `<SEED COMMAND>` and the smoke tests against the squashed chain.

## Part 2 — Remove dead compatibility code

Delete, do not keep "just in case":

- dual-read / dual-write paths that handle both an old and a new column or format,
- backfill scripts and one-off rake tasks for data that never existed in production,
- `TODO.*migration`, `temporary`, `backfill`, `legacy` markers that describe the build era,
  not the product,
- seed-vs-fixture confusion: seeds must produce a bootable empty-but-valid system; anything
  richer belongs in test factories.

Each deletion must keep `<GATE COMMAND>` green. A deletion that cannot be proven safe stays,
and goes in the report as deliberately kept.

## Part 3 — Fix live-data assumptions

Enumerate the false assumptions as a class and hunt each one:

- "a table has rows" — `first()`, `[0]`, `.single()` with no empty case; missing seed or backfill,
- "IDs are dense / sequential" — breaks on fresh sequences,
- "a background job already ran" — caches, denormalised counts, search indexes empty at boot,
- "an external system is already configured" — webhooks, OAuth grants, feature flags absent,
- "clock / volume is production-like" — pagination, timeouts and N+1s never exercised small.

Then run the **first-boot test**: wipe the database, run migrations plus seeds, boot the app,
and exercise every critical path with zero user data. Every failure is one of the assumptions
above made concrete — fix it.

## Verification (required before handing back)

- `<GATE COMMAND>` must pass.
- The schema-equivalence proof from Part 1 must be re-run on the final tree, not an earlier one.
- Where the gate does not itself check that committed generated artefacts are current,
  regenerate them and confirm they are unchanged.

## Process

`delivery.md` has already put you on a branch and will handle the push, the pull request and the
merge. Three obligations are yours alone:

1. Make the changes in small, logically grouped commits, one part per group (squash separate
   from code deletions separate from assumption fixes) — a reviewer must be able to read the
   migration rewrite without the bug fixes beside it.
2. **Each commit message must include the phrase `pre-launch scrub`**, unquoted, in the subject
   or the body, so a second run finds this point and refuses. This is the only string in this
   file that must not be reworded.
3. Record every decision that a later reader could mistake for churn in the report: which no-op
   pairs collapsed to nothing, what moved to its logical position, what compatibility code was
   removed, which assumptions were false and what the fix was.

Then report back, for the pull request description:

- the old chain and the new chain, migration by migration, and the equivalence proof result,
- every compatibility deletion and every assumption fix, with the test or first-boot step that
  proves it,
- anything intentionally NOT changed and why,
- confirmation that the gate is green.

## Safety rules

- If a squash step or deletion is ambiguous or risky, keep the old form and **say so in the
  report** — there is no backlog for this pass because there is no next run.
- Never rewrite git history on shared branches. The squash rewrites *migration files on this
  branch*, not pushed commits.
- **After this merges, migrations are additive-only.** Say so in the report's last line, so the
  rule lands where the team will read it.