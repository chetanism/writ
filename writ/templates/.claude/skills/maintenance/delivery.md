# Delivering a maintenance pass

The loop around `/cleanup`, `/product-docs`, `/security-audit` and `/context-compact`. Each of those
files owns **what changes**; this file owns **how it lands** — the branch, the gate, the commits,
the pull request, the merge, and the check that the next run will be able to find this one. It
exists once, here, so that the passes cannot drift apart in how they are delivered. Read it before
the pass, and follow it around the pass.

> **Filled at bootstrap.** `<INTEGRATION BRANCH>` and `<GATE COMMAND>` come from the interview.
> Delete this blockquote once they are filled.

## What each pass tells you

| Pass | Branch | PR title | Marker its commits must carry |
|---|---|---|---|
| `/cleanup` | `maintenance/cleanup-DATE` | `chore: regular maintenance DATE` | the phrase `regular maintenance` |
| `/product-docs` | `maintenance/documentation-DATE` | `docs: update product documentation` | the subject line `docs: update product documentation` |
| `/security-audit` | `maintenance/security-DATE` | `chore(security): periodic security audit DATE` | the marker `[security-review]` |
| `/context-compact` | `maintenance/context-DATE` | `docs: compact the agent map DATE` | the phrase `compact the agent map` |

`DATE` is today's date as `YYYY-MM-DD` — the same value for every pass in one `/maintenance` run.
**The marker is how the next run finds its baseline**, so it is not optional and not
paraphrasable. `/context-compact` is the one exception to *why*: its scope is a budget rather than a
diff, so its marker is how a reader finds where a section went rather than how the next run starts.
It is no more optional for that.

## The loop

Complete every step before starting another pass.

1. **Start clean.**
   ```bash
   git checkout <INTEGRATION BRANCH> && git pull --ff-only && git fetch --prune
   git status --porcelain   # must be empty
   ```
   A dirty tree is a stop, not something to stash: it is someone else's work.
2. **Branch.** `git checkout -b <branch from the table>`.
3. **Read the pass's `SKILL.md` in full and follow it.** It defines its own scope detection, its
   own work, and its own verification. Do not substitute your judgement for its scope rules; if its
   scope comes out empty, say so and go to step 8.
4. **Verify.** `<GATE COMMAND>` must pass. Where the pass asks for more — a build, the integration
   suite — run that too. A red gate is not a PR: fix it, or revert the change that caused it and
   record the revert for the PR body.
5. **Commit.** Small, logically grouped commits, each carrying the pass's marker from the table.
6. **Push and open the PR** into `<INTEGRATION BRANCH>`, titled per the table. The body is the
   report the pass handed back — what changed, what was deliberately not changed and why,
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
   pattern. If a marker does not survive, that pass's next run will silently re-scan from an older
   baseline; say so rather than amending the integration branch.
8. **Report one line** — pass, PR number, merged or skipped.

> **No pull-request flow?** If this project merges locally rather than through pull requests,
> steps 6 and 7 collapse to a squash merge into the integration branch and the marker check moves
> to the resulting commit. Everything else is unchanged — especially step 1 and step 5.

## Rules

- **An empty scope is a normal outcome, not a failure.** `/context-compact` under its budget and
  `/cleanup` with nothing changed since the last pass both end at step 8 with one line.
- **Never commit to the integration branch or the release branch directly.** Every change goes
  through the flow in `writ/process/DEVELOPMENT-PROCESS.md` §8.
- **No agent attribution** in the commit, pull request or issue — `CLAUDE.md` §Git. A maintenance
  pass closes no issue, so it carries no `Closes` line and the slice trailer block in
  `DEVELOPMENT-PROCESS.md` §6.3 does not apply to it — that block is a *slice* obligation.
- **One pass at a time.** Do not open a second PR before the first is merged. Each pass's scope
  detection reads `HEAD`, and a run whose predecessor is still unmerged computes a scope that
  excludes work already done.
- **A failing pass does not stop a run.** If one cannot be completed — a red gate that cannot be
  fixed without changing behaviour, a merge conflict — abandon that branch, say why, and let
  `/maintenance` continue with the next. Report the skip at the end.
- **The pass is the specification.** If a pass's instructions and this file disagree about *what*
  to change, the pass wins. If they disagree about *how it is delivered*, this file wins.

## The standing records

Two files outlive any single run and are the reason a pass does not re-derive the same judgement
every time. They are **maintained by the passes, not by this file**. `/context-compact` keeps
neither: its record is the pointer it leaves behind in `CLAUDE.md`.

| | |
|---|---|
| `writ/maintenance/cleanup-backlog.md` | what a cleanup pass deferred, and what it settled and will not re-open |
| `writ/maintenance/security-backlog.md` | the live security findings list; the dated reports in `audits/` are history |
