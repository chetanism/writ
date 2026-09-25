# Audit reports

One file per run, dated, written by a report-only skill:

- `security-audit-YYYY-MM-DD.md` — `.claude/skills/security-audit/SKILL.md`.
- `coverage-review-YYYY-MM-DD.md`, with its corrections in `coverage-review-YYYY-MM-DD.json` —
  `.claude/skills/coverage-review/SKILL.md`.

**A report is a record of one run, not a to-do list.** The open security work lives in
`../security-backlog.md`; a coverage review's corrections are applied once, by a person, and its
*Skip next run* list is what the next review reads. A report is never rewritten after the fact
except to add a single line marking a finding fixed — which is what keeps these readable as
history.
