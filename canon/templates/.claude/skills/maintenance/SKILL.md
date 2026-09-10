---
name: maintenance
description: Run all three of this repository's standing maintenance passes in order — /cleanup, /product-docs and /security-audit — each on its own branch and merged before the next one starts, then report across them. Use for a scheduled full maintenance run; to run one pass alone, invoke that pass's own skill.
---

# Maintenance run

You are running the three standing passes in order, each delivered by the loop in `delivery.md`
and merged before the next one starts. Each pass is a skill of its own — `/cleanup`,
`/product-docs`, `/security-audit` — and can be run alone on its own cadence. This file exists for
the full run, where the order carries weight, and for the report across all three.

## Which passes to run

`/maintenance` with no argument runs **all three, in order**. An argument runs exactly one, which
is the same as invoking that skill directly:

| Argument | Runs |
|---|---|
| *(none)* | all three, in the order below |
| `cleanup` | `/cleanup` |
| `docs` | `/product-docs` |
| `security` | `/security-audit` |

## The order, and why it is fixed

| # | Pass | Reads |
|---|---|---|
| 1 | `/cleanup` | the tree as it stands |
| 2 | `/product-docs` | the code the cleanup just changed — the documentation is derived from it |
| 3 | `/security-audit` | the tree the first two leave behind |

Do not reorder them, and do not start one before the previous has merged: each pass's scope
detection reads `HEAD`, and a pass started on top of an unmerged predecessor computes a scope
that excludes work already done. `delivery.md` says the same rule from the other side.

## The run

For each pass selected, in order: read `delivery.md`, read the pass's own `SKILL.md`, and run the
pass inside the delivery loop — start clean, branch, do the pass, verify, commit with the marker,
open the pull request, merge, confirm the marker survived, report one line. Then the next pass.

A pass that cannot be completed is abandoned with its reason and the run continues; the skip goes
in the final report. **A failing pass never stops the run**, because the passes after it do not
depend on it having succeeded — only on the tree being merged and clean.

## Final report

When every selected pass has run, report:

- one row per pass: PR number, merged / skipped, and a one-line summary,
- what changed in each standing record: rows added, closed, settled, still open,
- every marker string that did not survive its squash merge,
- anything a human needs to decide — a vetoed removal, a finding too large for a maintenance PR, a
  conflict between a document and the code.
