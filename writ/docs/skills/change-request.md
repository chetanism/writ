# `/change-request`

**After launch, the only way a requirement register changes: one page of rows to add, amend or
withdraw, read against the invariants for conflict, decided by the specification's owner, then
applied to the registers, the changelog and the index.**

| | |
|---|---|
| **Run it** | `/change-request` to raise one; `/change-request apply CR-014` once it is accepted |
| **Produces** | One file under `writ/spec/changes/`, then — on apply — amended rows carrying `Since: CR-NNN`, and one changelog line |
| **Refuses to** | Decide. It drafts; the specification's owner says yes or no |

## Why registers stop being edited directly

**Before launch, a requirement changes because you learned something. After launch, it changes
because somebody decided something — and the decision is the part worth keeping.**

Editing a register in place loses it. Six months later the row says what it says, and the question
nobody can answer is *who agreed to this, when, and what did it replace?* The `Since` column, the
changelog line and the request file together are that answer, and the index derives an *applied* and
*built* state from them so an accepted-but-unapplied request cannot sit quietly forever.

## What it does

1. **One change per request.** A request bundling three unrelated changes is one the owner cannot
   say yes to.
2. **Refuses the ones that are not its** — a register it does not own, a code change wearing a
   requirement's clothes.
3. **Gets onto the request's branch** before touching anything.
4. **Reads the change back as rows, before writing anything** — the exact rows that would be added,
   amended or withdrawn.
5. **Reads them against the invariants for conflict**, and lists what else goes stale: detail files,
   scenario files, manual regression entries.
6. **One round of questions**, and only what changes the rows.
7. **Stops for the owner.** Then `apply` writes the rows, the `Since`, the changelog line.

## The check behind it

An accepted change request that has not been applied, or a `Since` that resolves to nothing, fails
`ledger.py check`. **A decision that was made and never landed is the failure this whole file
exists to prevent.**

## Turning it off

Pre-launch, `changes.dir: ""` switches the track off and registers change by being edited. You lose
the record of who agreed, and the index's *applied* and *built* columns.
[Changing the process](../changing-the-process.md) has the rest.
