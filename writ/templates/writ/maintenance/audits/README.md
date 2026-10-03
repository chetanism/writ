# Audit reports

One file per run, dated, written by a report-only skill — and one, once, by the pre-launch scrub:

- `security-audit-YYYY-MM-DD.md` — `.claude/skills/security-audit/SKILL.md`.
- `coverage-review-YYYY-MM-DD.md`, with its corrections in `coverage-review-YYYY-MM-DD.json` —
  `.claude/skills/coverage-review/SKILL.md`.
- `design-audit-YYYY-MM-DD.md` — `.claude/skills/design-system/SKILL.md`, run as
  `/design-system audit`.
- `prelaunch-YYYY-MM-DD.md` — `.claude/skills/prelaunch/SKILL.md`. There is only ever one, and
  **its existence is the lock**: `/prelaunch` refuses to run when it finds it.

**A report is a record of one run, not a to-do list.** The open security work lives in
`../security-backlog.md`; a coverage review's corrections are applied once, by a person, and its
*Skip next run* list is what the next review reads. A report is never rewritten after the fact
except to add a single line marking a finding fixed — which is what keeps these readable as
history.
