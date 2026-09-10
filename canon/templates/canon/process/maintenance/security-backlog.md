# Security backlog

**The live list of security findings.** The dated reports in `audits/` are history — each records
one run and is never rewritten except to mark a finding fixed. This file is what is true now, and
`.claude/skills/maintenance/security.md` is the prompt that maintains it.

## Why this file exists

The audit scopes itself with `git diff <last-review>..HEAD`. Scoped only by the diff, an audit sees
a finding once and never again — because the file a finding lives in is usually the file nobody has
touched since. Every open row below is **added to the scope of every run**, whether or not its file
appears in the diff, and re-checked against the code as it stands: fixed, still open, or never
right.

Four tables, and they are not interchangeable:

| | Means | Leaves by |
|---|---|---|
| **Open** | A finding against code that exists | Being fixed, or being withdrawn as never a defect |
| **Closed** | Confirmed fixed | Nothing. It is the record |
| **Accepted risks** | A person decided to carry it | That person deciding otherwise. **Never the audit's call** |
| **Deferred to a slice that has not happened** | A control for a surface not yet built | The slice landing, at which point it becomes Open or is satisfied |

The last table is the one that is easy to get wrong. A finding filed against unwritten code can
never be closed, and saying nothing about it looks like coverage. Keeping it here says both things
at once: it is not a defect yet, and it is not forgotten.

---

## Open

| ID | Finding | Severity | Where | Raised |
|---|---|:--:|---|---|

*No rows yet.*

---

## Closed

| ID | Finding | Closed | How |
|---|---|---|---|

*No rows yet.*

---

## Accepted risks

A risk is accepted by a **named person on a date**, and the audit reports it as open however old it
is. It does not get to decide this.

| ID | Risk | Accepted by | Date | Reasoning |
|---|---|---|---|---|

*No rows yet.*

---

## Deferred to a slice that has not happened

A control the system will need once a surface exists. Not a finding, because there is nothing yet
to be wrong.

| ID | Control | Waits on | Why it is not a finding |
|---|---|---|---|

*No rows yet.*
