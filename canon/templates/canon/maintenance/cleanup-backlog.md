# Cleanup backlog

**What a cleanup pass looked at and did not change, and why.** The pass reads this before it
starts; `/cleanup` — `.claude/skills/cleanup/SKILL.md` — is the pass that maintains it.

## Why this file exists

The cleanup pass scopes itself with `git diff <last-pass>..HEAD` and its safety rule is *"if a
change is ambiguous or risky, skip it and report it."* Reporting it meant putting it in a pull
request description, which is read once. A skipped change in a file nobody touches again is never
re-seen — so the rule produced no record at all, and the same judgement had to be made from scratch
every run.

Two kinds of row live here, and conflating them is the mistake this file is shaped to avoid:

| | **Deferred** | **Settled** |
|---|---|---|
| Means | Worth doing. Not done yet | Looked at. **Deliberately not changing** |
| The next pass should | Reconsider it | **Not re-open it** |
| Leaves by | Being done | A decision that the reasoning no longer holds |

The second kind is the one a cleanup pass needs most. A pass runs a duplicate-block scan, a
dead-code scan and a link check, and those scans flag the same deliberate structures every time.
Without a written answer, each run re-derives it — and one run eventually "fixes" a boundary that
was load-bearing. A `Settled` row is a **standing answer to a recurring false positive**, written
where the reasoning fits.

Neither table is a to-do list anybody is obliged to work through. A cleanup pass is opportunistic
by design.

---

## Deferred

Worth doing, and not done. A pass should reconsider each of these against the code as it stands —
the reason for deferring may have expired.

| # | Item | Where | Why not yet |
|:--:|---|---|---|

*No rows yet.*

---

## Settled — do not re-open

Each of these has been examined and is **deliberately as it is**. A row leaves this table only when
someone decides the reasoning no longer holds — not because a scan flagged it again.

| # | What a scan flags | Why it stays | Examined |
|:--:|---|---|---|
| **CL-S1** | `docs/documentation/**` drifting from the code | **Owned by another pass.** `/product-docs` regenerates it from the code and runs immediately after this pass in a full `/maintenance` run. Editing it here collides with that, and the two would disagree inside one pull request | at bootstrap |
| **CL-S2** | Prose in `canon/decisions/`, `canon/process/work-orders/` and `canon/process/slices/` that contradicts the code as it stands now | **Immutable by status.** An ADR records why a decision was made *then*; a work order and a slice summary record what was agreed and what happened. A later fact does not make them wrong, it makes them history. Correcting them destroys the record. A decision that has been superseded gets a **new** ADR | at bootstrap |

---

## Done

A pointer, not a record — the pull request holds the detail.

| # | Item | Closed | How |
|:--:|---|---|---|

*No rows yet.*
