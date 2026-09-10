# The team pipeline

Read with `skills/team/SKILL.md` phase 3. Everything here is confirmed with the user
before it is written down.

## Roles

One person may hold several; two people may not hold one. Say that out loud, because "we both own
the BRD" is the most common answer and it is the thing to fix.

| Role | Owns | Cannot also be |
|---|---|---|
| **BRD owner** | Scope, priority, the requirement set | — |
| **Requirements author** | Requirement IDs, foundation specs | — |
| **Slicer** | The queue, work orders, sizing | — |
| **Implementer** | Code and tests for one slice | The plan reviewer for that slice |
| **Plan reviewer** | Reads the plan before code exists | The implementer of that slice |
| **Player** | Runs the demo by hand at close | The implementer of that slice, by default |

The last two exclusions are the whole reason a team runs this process differently from one person.
A solo developer reviews their own plan because there is nobody else; a team that does it is
choosing to.

## Handoffs, each with a definition of ready

```
BRD frozen at a version   →  requirement IDs may be declared
requirements declared     →  slices may be cut against them
work order approved       →  a branch and draft PR may open
plan read by a reviewer   →  implementation may begin
gate green + demo played  →  the slice may merge
```

Write this into `DEVELOPMENT-PROCESS.md` as a table with a column for *who says it is ready*. The
failure this prevents is somebody implementing against requirements still being edited — which
surfaces as a merge conflict in a specification, three days late.

**Freezing is a version bump, not a lock.** The BRD keeps changing; what a slice builds against is
a stated version of it. If a frozen requirement must change mid-slice, that is an amendment with a
log entry, and the slice's work order says which version it was cut against.

## Running in parallel without collisions

Three mechanisms, all mechanical:

1. **`touches:` in the work-order front matter.** The shared surfaces a slice changes, named
   concretely and consistently — `schema/accounts`, `api/v1/orders`, `config/gate`. Two active
   slices sharing an entry is a hard error from `ledger.py check`. Agree the vocabulary once, in
   `DEVELOPMENT-PROCESS.md`, or the field is decorative.
2. **A WIP limit.** Default: one in-flight slice per implementer. Raising it is a decision with a
   reason, not a default that drifts upward. Enforced by the same check.
3. **`depends_on:`.** The generated queue is a topological sort, so "what can I start now" is a
   lookup: the highest-ranked `queued` slice whose dependencies are `done` and whose `touches` do
   not collide with anything active.

## Claiming work

Set `owner:` and `status: in-progress` in the work order, in a small commit on the integration
branch, before opening the slice branch. Two people cannot claim the same slice because the second
commit conflicts — which is the cheapest lock available and needs no tooling.

The generated queue carries the owner column in team mode, so it doubles as the board — and the
issue column where a tracker is configured. The issue is a mirror of the work order, opened at the
claim with the file as its body and re-synced at close, never the place the claim is made: a claim
in a tracker is invisible to `ledger.py check` and to the second person's commit conflict, which
are the two things that make claiming safe. `Closes #N` in the close commit is what shuts it, and
the merge has to be told to keep that trailer — the default squash message of a two-commit branch
is the title and nothing else. `/slice-close` hands over the command that keeps it.

## Review

- **The plan review is the cheapest comprehension the process offers**, and on a team it is also
  the only moment a second person sees the design before it exists. A plan the reviewer cannot
  follow is a signal that the slice is too large or the design is wrong — say so then, not in the
  diff review.
- **The diff review is not a substitute.** By then the cost of a different approach is the whole
  slice.
- **The demo is played by someone who did not implement it.** They will use it wrong, which is the
  entire value.

## CODEOWNERS

Generate it from the roles:

```
canon/spec/               @brd-owner @requirements-author
canon/spec/requirements/  @detail-approver
canon/decisions/          @invariant-approver
canon/process/            @slicer
canon/qa/                 @test-manager
canon/maintenance/        @security-backlog-owner
scripts/                  @slicer
```

**Order matters: the last matching pattern wins.** The requirements line has to come after the
specification's, or the approver is silently overridden by the BRD owner on every detail file.

An invariant with no named approver is a suggestion. That is the single most useful line in the
file.

## Cadence

- **Per slice** — the loop.
- **Per week** — read the queue together. Re-order what has changed; confirm nothing has been
  in-progress for two weeks.
- **Per phase** — read the ledger against the phase's exit criterion. Retire manual-regression
  entries that automated tests now cover.
- **Per milestone** — measure against the exit criterion, not against the number of merged slices.

## Scaling down

If the team shrinks to one, delete the roles table, set the WIP limit to one, drop the reviewer and
player exclusions, and keep everything else. The two processes are the same process; only the
handoffs differ.
