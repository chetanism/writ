---
name: prelaunch
description: Run the one-shot pre-production scrub over this repository — squash the migration chain to a clean baseline, remove dead compatibility code, sweep the whole tree for dead code, dependencies, variables and flags, remove or lock down dev-only surface, and fix code written against live-data assumptions — catalogued and approved before anything changes, delivered on its own branch through a pull request. Use once, before the first production deploy; it refuses to run twice.
---

# Pre-launch scrub

You are performing the one-shot pre-production scrub of this repository. Invoked as `/prelaunch`,
once, before the first production deploy. **This file owns what changes.**
`.claude/skills/maintenance/delivery.md` owns the branch, the commits, the pull request and the
merge — read it first, and run this file inside its loop.

Your goal is to remove everything the build accumulated that is only true of an unlaunched
project: a migration chain full of reversals, compatibility code for data that never existed, code
and dependencies nothing reaches any more, surface that only made sense on a laptop, and code
written against a live system that is not live yet.

> **Filled at bootstrap.** `<GATE COMMAND>`, `<MIGRATION TOOLING>` (the command that applies the
> chain to an empty database, and the one that generates a new migration), `<SCHEMA DUMP COMMAND>`
> and `<SEED COMMAND>` come from the interview. Delete this blockquote once they are filled.

## The one-shot rule (read this first)

1. Look for `writ/maintenance/audits/prelaunch-*.md` on the integration branch. If one exists,
   **stop and report that the scrub has already run**, naming the file and the date in it. It
   does not run twice: after the first production deploy, this skill's migration work becomes
   dangerous. The record is written by this run and lands only when its pull request merges, so a
   run abandoned before the merge leaves no record and can be started again.
2. If the project has already deployed to production — a deploy marker, a release tag, live data
   behind the migrations — **stop and say so.** The squash is only safe against databases that can
   be rebuilt from scratch. After launch, migration hygiene is additive-only (`/cleanup` scope),
   and assumption bugs are ordinary slices.

## Scope

The whole tree, in five parts, in order. Unlike `/cleanup` this pass is **not diff-scoped and not
behaviour-preserving** — deleting a debug route or fixing a false live-data assumption changes
behaviour by definition. That is the point. The catalogue below, the gate and the
schema-equivalence proof are what keep it honest.

Exclude generated artefacts, vendored code and `writ/` itself from every sweep.

## Catalogue first — change nothing until it is approved

This is the one skill that rewrites migrations, and most of what it deletes cannot be told apart
from churn afterwards. So it decides everything before it does anything.

1. Run the *catalogue* step of each part below, all five, without editing a file.
2. **Read the catalogue back** as one list per part: the old chain against the proposed one, every
   no-op pair and every move; every deletion with the evidence that nothing reaches it; every
   dev-only route, setting and fallback, and whether it goes or is guarded; every suspected
   live-data assumption.
3. **Stop for approval.** The user strikes, keeps or adds lines. What is approved is the scope;
   what is struck goes in the record as deliberately kept, with the user's reason.
4. Something found while carrying out the approved list that is not on it — a migration change of
   any kind, or a deletion with any doubt — goes back to the user before it is made. A mechanical
   consequence of an approved line (a test of deleted code deleted with it) does not.

## Part 1 — Squash the migration chain

**Catalogue:**

1. Read the migration history end to end. List every no-op pair: a migration that adds what a
   later one removes, creates what a later one drops, renames twice, or backfills data that no
   production database ever held.
2. List every misplaced change: a column, index or constraint added in a later migration that
   logically belongs to an earlier table definition.
3. List every migration that **writes data** — reference rows, lookup tables, enum values, a
   default tenant or role. A schema dump does not see these, so the squash can lose one silently.
4. List every database that has already applied the current chain — developers' local databases,
   CI caches, staging, preview environments. Each will need rebuilding once the chain changes.

**Then:**

1. Rewrite the chain into a clean baseline — one baseline migration per bounded context, or a
   single `0001_baseline` where the project is small — with the no-op pairs gone and every change
   in its logical position, using `<MIGRATION TOOLING>`.
2. Where the gate holds migrations immutable — recorded checksums, a lint that fails an edited
   or deleted migration — this rewrite is the one sanctioned exception. Regenerate the checksums
   or the lint's baseline in the same commit as the squash and name the exception in the record.
   **Never switch the check off**: it is what holds the additive-only rule from the next commit on.
3. Reference data the product needs to boot stays in a migration or moves to `<SEED COMMAND>`;
   either way it is written once, in one place, and named in the record.
4. **Prove equivalence mechanically, never by eye:**
    - Build a fresh database from the old chain with `<MIGRATION TOOLING>`, dump its schema:
      `<SCHEMA DUMP COMMAND>`.
    - Build a fresh database from the squashed chain, dump its schema the same way.
    - The two dumps must be identical apart from migration metadata. If they differ, the squash
      is wrong — fix it, do not explain it.
    - For every data-writing migration from the catalogue's step 3, query the rows it wrote from both
      databases (after `<SEED COMMAND>` on each) and compare them. Different rows are a wrong
      squash in the same way.
5. Re-run `<SEED COMMAND>` against the squashed chain and confirm the app boots on it.

## Part 2 — Remove dead compatibility code

**Catalogue** — every one of these, with where it is and why nothing needs it:

- dual-read / dual-write paths that handle both an old and a new column or format,
- backfill scripts and one-off tasks for data that never existed in production,
- API surface kept for a client that no longer exists — deprecated fields still serialised,
  aliases for renamed routes, a `v0` kept beside `v1`. No outside client has ever called them,
- `TODO.*migration`, `temporary`, `backfill`, `legacy` markers that describe the build era, not
  the product,
- seed-vs-fixture confusion: seeds must produce a bootable empty-but-valid system; anything
  richer belongs in test factories.

**Then** delete, do not keep "just in case". Each deletion must keep `<GATE COMMAND>` green. A
deletion that cannot be proven safe stays, and goes in the record as deliberately kept.

## Part 3 — Sweep the whole tree for dead code

`/cleanup` only ever sees what changed since its last pass, so what died during the build — a
module superseded at slice twelve, a package added for a spike — is never in its scope. Before
launch is the one time a whole-tree sweep is cheap.

**Catalogue:**

- modules, files and exported symbols nothing imports or calls,
- dependencies in the manifest that no code imports — and the lockfile entries only they pulled in,
- environment variables read nowhere, and variables read in code but set nowhere,
- feature flags that hold one value in every environment — the flag and its dead branch both go,
- tests, fixtures and scripts that exist only for something on this list.

Use the stack's own finders for unused exports and dependencies where it has them. **A finder's
hit is a lead, not proof**: dynamic imports, reflection, framework conventions, entry points named
in config, and scripts run by CI or a deploy all reach code no import graph shows. Search for the
name as a string before listing anything.

**Then** delete each approved line with its tests. `<GATE COMMAND>` green after each group.

## Part 4 — Remove or lock down dev-only surface

What was convenient while nobody but the team could reach the system is a hole the day somebody
else can.

**Catalogue:**

- debug, test-only and admin-convenience routes: database reset, seed or fixture loaders,
  impersonation, "log in as", health pages that print configuration,
- debug toolbars, verbose error pages and stack traces sent to clients, permissive CORS or CSP
  set for local development, development-only middleware,
- credentials with a known value: seeded users with fixed passwords, default admin accounts,
  sample API keys,
- configuration that falls back to a development value when a variable is missing — a secret key
  of `"dev"`, a database URL of `localhost`, a mail sender that silently does nothing,
- `.env.example` (or its equivalent) against the variables the code actually reads.

**Then:**

- Delete what production never needs. What development genuinely does need is **guarded**: on
  only under an explicit development setting, off by default, so a missing setting is the safe
  one.
- Seeds create no account with a known password. An operator's first account is created by a
  documented first-run step, not by the seed.
- **Every required variable fails at boot**, naming itself, when it is missing. No fallback for
  anything that differs between development and production.
- `.env.example` lists every variable the code reads and nothing else.

A finding here that is a vulnerability in its own right rather than build-era residue is fixed
here too — and, where `/security-audit` is installed, named in the record so its next run does
not re-derive it.

## Part 5 — Fix live-data assumptions

This part runs last, because the first-boot test below is also the check on everything the first
four removed.

**Catalogue** — the false assumptions as a class, each hunted:

- "a table has rows" — `first()`, `[0]`, `.single()` with no empty case; missing seed or backfill,
- "IDs are dense / sequential" — breaks on fresh sequences,
- "a background job already ran" — caches, denormalised counts, search indexes empty at boot,
- "an external system is already configured" — webhooks, OAuth grants, feature flags absent,
- "clock / volume is production-like" — pagination, timeouts and N+1s never exercised small.

**Then** run the **first-boot test**: wipe the database, run migrations plus `<SEED COMMAND>`,
boot the app with only the variables `.env.example` lists, and exercise every critical path with
zero user data. Where `/manual-test` is installed and its harness is filled, `harness.sh up
--fresh` is that boot. Every failure is one of the assumptions above made concrete — fix it. Then
boot once more with one required variable removed: it must refuse to start and name the variable.

## Verification (required before handing back)

- `<GATE COMMAND>` must pass.
- The schema-equivalence proof and the reference-data comparison from Part 1 must be re-run on the
  final tree, not an earlier one.
- The first-boot test from Part 5 must pass on the final tree.
- Where the gate does not itself check that committed generated artefacts are current,
  regenerate them and confirm they are unchanged.

## Process

`delivery.md` has already put you on a branch and will handle the push, the pull request and the
merge. Four obligations are yours alone:

1. Make the changes in small, logically grouped commits, one part per group — a reviewer must be
   able to read the migration rewrite without the bug fixes beside it.
2. **Each commit message must include the phrase `pre-launch scrub`**, unquoted, in the subject
   or the body. It is how a reader finds this run in the log; the record below is the lock.
3. **Write the record**, `prelaunch-DATE.md` in `writ/maintenance/audits/`, where `DATE` is today's
   date as `YYYY-MM-DD`, in the last commit:
    - the old chain and the new chain, migration by migration, the equivalence proof result and
      the reference-data comparison,
    - every deletion and every guard, by part, with the evidence that nothing reached it,
    - every assumption that was false, its fix, and the first-boot step that proves it,
    - everything struck from the catalogue or deliberately kept, and why,
    - every database from Part 1's step 4 that must now be rebuilt,
    - confirmation that the gate and the first-boot test are green,
    - and, as its last line: **after this merges, migrations are additive-only.**
4. Hand the record back as the pull request description.

## Safety rules

- If a squash step or deletion is ambiguous or risky, keep the old form and **say so in the
  record** — there is no backlog for this pass because there is no next run.
- Never rewrite git history on shared branches. The squash rewrites *migration files on this
  branch*, not pushed commits.
- **Every database that applied the old chain must be rebuilt after this merges** — local, CI,
  staging, previews. Say so in the pull request description in as many words; an environment that
  is migrated forward instead will fail on its first deploy.
