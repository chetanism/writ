# `/security-audit`

**A periodic audit against the OWASP Top 10 and the CWE Top 25 — scoped to what changed since the
last audit plus every open backlog row — ending in a dated report and a reconciled backlog.**

| | |
|---|---|
| **Run it** | On a cadence, after any dependency change, or on demand. Also the third of `/maintenance`'s four passes |
| **Produces** | A dated report under `canon/maintenance/audits/`, a reconciled `security-backlog.md`, delivered on a branch |
| **Ships with** | Its own OWASP and CWE checklists — `reference/owasp.txt` and `reference/cwe.tsv` |

## What it does

1. **Determines the scope** — what changed since the last audit, **plus every open backlog row**
   regardless of whether its files changed.
2. **Loads the checklists.** Two of them, shipped with the skill, so the audit is against a fixed
   list rather than against whatever the agent happens to remember that day.
3. **Audits**, flags findings, writes a dated report.
4. **Reconciles the backlog** — findings in, fixed rows out, deferred rows justified.
5. **Marks the review as done**, which is what makes *the age of the last audit* a number `stats`
   can report.

## Why the scope includes the whole backlog

**An open finding does not become less true because nobody touched its file this month.** Scoping
an audit purely to the diff means a finding recorded in March is never looked at again unless
somebody happens to edit that file — and the findings most likely to sit in a backlog are exactly
the ones in code nobody wants to touch.

## Why a dated report rather than just a backlog

Because *when did we last actually look* is a question a backlog cannot answer. A backlog with no
open rows means either a clean codebase or an audit nobody has run since the spring, and those are
very different situations. `ledger.py stats` reports the age of the last audit for precisely this
reason.

## See also

[`/maintenance`](maintenance.md) — where this runs third, after `/cleanup` and `/product-docs`, so
that it audits a codebase that has already been simplified rather than one mid-change.
