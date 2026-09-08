# Periodic security review

You are performing a scheduled security audit of this repository. This is one of the three standing
prompts `SKILL.md` runs; it owns *what* changes, and `SKILL.md` owns the branch, the commits, the
pull request and the merge. Follow these steps precisely.

> **Filled at bootstrap.** §3's *Pay special attention to this project's stack* list is generated
> from the stack and the domain profile. Delete this blockquote once it is filled.

## 1. Determine the review scope

1. Find the last security review commit:
    - the most recent commit whose message contains the marker:
      `git log --grep="\[security-review\]" -n 1 --format=%H`.
    - **A match is only a baseline if that commit actually carried an audit.** A commit that merely
      *discusses* the marker — this prompt's own introduction does — matches the grep and yields an
      empty diff. Confirm the candidate added a report under `docs/process/maintenance/audits/`; if
      it did not, keep walking back, and if none did, treat this as the first review.
    - If no such commit exists, treat this as the first review and audit the entire codebase.
2. Collect all files modified since that commit: `git diff --name-only <commit>..HEAD`. Exclude
   generated files, lockfiles and build output.
3. **Read `docs/process/maintenance/security-backlog.md`, and add everything still open to the
   scope.** Its rows are in scope *whether or not their files appear in the diff* — which is the
   whole reason it exists. An audit scoped only by the diff sees a finding once and never again,
   because the file it is in is usually the file nobody has touched.

## 2. Load the vulnerability checklists

- OWASP Top 10: `reference/owasp.txt`
- CWE Top 25: `reference/cwe.tsv`

These two lists are the authoritative checklist for this audit. For each file in scope — the diff
**and** whatever the backlog put there — evaluate the code against every item in both.

## 3. Perform the audit

Two passes, and the second is short. **First, re-check every open backlog row** against the code as
it stands: fixed, still open, or never right. Doing this first means a finding the last run raised
is not re-discovered under a second ID and filed twice.

Then, for each file in scope, analyse the code for actual instances **and** plausible possibilities
of:

- every OWASP Top 10 category, including injection, broken access control, cryptographic failures,
  insecure design, security misconfiguration, vulnerable and outdated components, identification
  and authentication failures, software and data integrity failures, logging and monitoring
  failures, and SSRF;
- every CWE Top 25 weakness, matched by CWE ID.

**Pay special attention to this project's stack:**

> One bullet per component the project actually uses, naming the weakness class that component
> characteristically produces. The shape is *component — what to look for*:
>
> - **the HTTP layer** — routes with missing input validation, missing authorization checks, error
>   responses leaking internals.
> - **the data layer** — raw or string-interpolated queries, missing parameterization, a query
>   path that escapes the project's tenancy or row-level controls.
> - **any queue or background worker** — untrusted data in job payloads, deserialization, command
>   injection into whatever the payload names.
> - **secrets and configuration** — hardcoded credentials, tokens or keys committed to the repo.
> - **logging and observability** — PII, tokens or passwords written to logs.
> - **dependencies** — obviously vulnerable or outdated usage patterns detectable in code.
>
> Replace each with the project's real components. A generic list is one nobody reads twice.

## 4. Flag findings

For every finding, record:

| Field | Description |
|---|---|
| ID | Sequential finding ID, `SEC-YYYY-NNN` |
| File and lines | Exact location |
| Category | OWASP category and/or CWE ID from the checklists |
| Severity | Critical / High / Medium / Low |
| Type | `Instance` (confirmed) or `Possibility` (potential, needs verification) |
| Description | What the issue is and why it matters |
| Recommendation | Concrete remediation steps, with a code suggestion where practical |

Number findings **from where the last audit left off**, across the whole history rather than
restarting per run — `SEC-2026-010` follows `SEC-2026-009` even if a year passed. An ID is a handle
other documents and commit messages point at, so re-using one is worse than a gap.

## 5. Write the report

Create `docs/process/maintenance/audits/security-audit-DATE.md`, where `DATE` is today's date as
`YYYY-MM-DD`. The report must contain:

1. **Summary** — review date, last review commit hash, number of files scanned, counts of findings
   by severity.
2. **Scope** — the list of files reviewed.
3. **Findings** — the full detail from step 4, grouped by severity, Critical first.
4. **Checklist coverage** — confirmation that all OWASP Top 10 and CWE Top 25 items were checked,
   noting any that were not applicable.
5. **Recommended next actions** — a prioritized remediation list.

Write the report as a record of *this run*, not as a to-do list — the open work lives in the
backlog (step 6) and is maintained there. **A report is never rewritten later** except to mark a
finding fixed.

If no issues are found, still create the report stating that the audit was clean, and say what the
backlog looked like when you checked it.

## 6. Reconcile the backlog

`docs/process/maintenance/security-backlog.md` is the **live** list; a report is a point-in-time
record. Update the backlog in the same commit as the report:

1. **Add** every new finding that is not fixed in this run, linking it to this report.
2. **Remove** every row you confirmed fixed, and add it to the *Closed* table with one line on what
   closed it. Also add a `> **Fixed on that date.**` line to the finding in the report that raised
   it — that is the **only** amendment a report ever takes, and it is why the reports stay readable
   as history.
3. **Remove** a row you found was never a defect, and say so in this run's report. An audit that
   files something wrongly must be able to withdraw it.
4. **Leave the *Accepted risks* table alone.** A risk is accepted by a person, with a name and a
   date, and that is not the audit's to decide. Report an open row as open, however old.
5. **Carry forward** a control for a surface that does not exist yet into *Deferred to a slice that
   has not happened* rather than filing it as a finding. A finding against unwritten code cannot be
   closed, and silence about it looks like coverage. This is where the difference is kept.

If a run finds nothing new and closes nothing, say so — an unchanged backlog is a result.

## 7. Mark the review as done

Commit the report with a message that includes the marker `[security-review]`, so the next audit
can find this baseline:

```
chore(security): periodic security audit DATE [security-review]
```

## 8. Delivery

`SKILL.md` owns the branch, the push, the pull request and the merge. Step 7's marker is yours
alone, and the report file is what makes the commit a real baseline for step 1. Report back, for
the pull request description: the finding counts by severity, the scope decision you made in step
1, the path of the report you wrote, and **what changed in the backlog** — rows added, rows closed,
rows still open.
