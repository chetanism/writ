---
name: maintenance
description: Run this repository's standing maintenance passes — a behaviour-preserving cleanup, a regeneration of the product documentation from the code, and a security audit against the OWASP Top 10 and CWE Top 25 — each on its own branch and merged before the next one starts. Use for scheduled or on-demand maintenance; pass "cleanup", "docs" or "security" to run one pass alone.
---

# Maintenance run

You are running this repository's standing maintenance prompts, one at a time, each on its own
branch and merged before the next one starts. **This file owns delivery** — the branch, the push,
the pull request, the merge, the cleanup. Each sub-prompt owns **what changes**.

> **Filled at bootstrap.** `<INTEGRATION BRANCH>`, `<GATE COMMAND>` and the attribution rule in
> §Rules come from the interview. Delete this blockquote once they are filled.

## Which passes to run

`/maintenance` with no argument runs **all three, in order**. An argument runs exactly one, with
the same delivery loop around it:

| Argument | Runs |
|---|---|
| *(none)* | all three, in the order below |
| `cleanup` | `cleanup.md` |
| `docs` | `documentation.md` |
| `security` | `security.md` |

## The prompts, in order

Run them in this order and do not reorder them. The order is not arbitrary: cleanup rewrites code
and docs, documentation is derived from the code cleanup just changed, and the security audit
should read the tree the first two leave behind.

| # | Prompt | Branch | PR title |
|---|---|---|---|
| 1 | `cleanup.md` | `maintenance/cleanup-DATE` | `chore: regular maintenance DATE` |
| 2 | `documentation.md` | `maintenance/documentation-DATE` | `docs: update product documentation` |
| 3 | `security.md` | `maintenance/security-DATE` | `chore(security): periodic security audit DATE` |

`DATE` is today's date as `YYYY-MM-DD`, the same value for all three.

## The loop

For each prompt selected, in order, complete every step before starting the next prompt.

1. **Start clean.**
   ```bash
   git checkout <INTEGRATION BRANCH> && git pull --ff-only && git fetch --prune
   git status --porcelain   # must be empty
   ```
   A dirty tree is a stop, not something to stash: it is someone else's work.
2. **Branch.** `git checkout -b <branch from the table>`.
3. **Read the prompt file in full and follow it.** It defines its own scope detection, its own
   work, and its own verification. Do not substitute your judgement for its scope rules; if its
   scope comes out empty, say so and go to step 8.
4. **Verify.** `<GATE COMMAND>` must pass. Where the prompt asks for more — a build, the
   integration suite — run that too. A red gate is not a PR: fix it, or revert the change that
   caused it and record the revert for the PR body.
5. **Commit.** Small, logically grouped commits. **Each prompt names a marker string its commit
   messages must carry** — that marker is how the *next* run finds its baseline, so it is not
   optional and not paraphrasable:
    - `cleanup.md` — the phrase `regular maintenance`
    - `documentation.md` — the subject line `docs: update product documentation`
    - `security.md` — the marker `[security-review]`
6. **Push and open the PR** into `<INTEGRATION BRANCH>`, titled per the table. The body is the
   report the prompt handed back — what changed, what was deliberately not changed and why,
   conflicts found and how they were resolved, and confirmation that the gate is green.
7. **Merge it.** Squash merge, wait for it to land, then:
   ```bash
   git checkout <INTEGRATION BRANCH> && git pull --ff-only && git fetch --prune
   git branch -D <branch>
   ```
   Squash merge means the branch commits never become ancestors of `<INTEGRATION BRANCH>`, so `-d`
   refuses.

   **Confirm the squashed commit still carries the marker string.** GitHub composes that commit
   from the PR title and body — but on a **single-commit branch it uses the branch commit's own
   message instead**, so a marker placed only in the PR body will not survive. It also appends
   ` (#N)` to the subject, which is why no marker may ever be matched with an anchored `^…$`
   pattern. If a marker does not survive, that prompt's next run will silently re-scan from an
   older baseline; say so rather than amending the integration branch.
8. **Report one line** — prompt, PR number, merged or skipped — and move to the next prompt.

> **No pull-request flow?** If this project merges locally rather than through pull requests,
> steps 6 and 7 collapse to a squash merge into the integration branch and the marker check moves
> to the resulting commit. Everything else is unchanged — especially step 1 and step 5.

## Rules

- **Never commit to the integration branch or the release branch directly.** Every change goes
  through the flow in `docs/process/DEVELOPMENT-PROCESS.md` §8.
- **Attribution follows `CLAUDE.md`.** A maintenance run closes no issue, so it carries no `Closes`
  line and the slice trailer block in `DEVELOPMENT-PROCESS.md` §6.3 does not apply to it — that
  block is a *slice* obligation. Nothing else about attribution is decided here.
- **One prompt at a time.** Do not open the second PR before the first is merged. Each prompt's
  scope detection reads `HEAD`, and a run whose predecessor is still unmerged computes a scope that
  excludes work already done.
- **A failing prompt does not stop the run.** If one cannot be completed — a red gate that cannot
  be fixed without changing behaviour, an empty scope, a merge conflict — abandon that branch, say
  why, and continue with the next prompt. Report the skip at the end.
- **The prompts are the specification.** If a prompt's instructions and this file disagree about
  *what* to change, the prompt wins. If they disagree about *how it is delivered*, this file wins.

## The standing records

Two files outlive any single run and are the reason a pass does not re-derive the same judgement
every time. They are **maintained by the prompts, not by this file**:

| | |
|---|---|
| `docs/process/maintenance/cleanup-backlog.md` | what a cleanup pass deferred, and what it settled and will not re-open |
| `docs/process/maintenance/security-backlog.md` | the live security findings list; the dated reports in `audits/` are history |

## Final report

When every selected prompt has run, report:

- one row per prompt: PR number, merged / skipped, and a one-line summary,
- what changed in each standing record: rows added, closed, settled, still open,
- every marker string that did not survive its squash merge,
- anything a human needs to decide — a vetoed removal, a finding too large for a maintenance PR, a
  conflict between a document and the code.
