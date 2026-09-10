# Cleanup pass

You are performing a scheduled cleanup pass over this repository. This is one of the three standing
prompts `SKILL.md` runs; it owns *what* changes, and `SKILL.md` owns the branch, the commits, the
pull request and the merge.

Your goal is to keep the code and documentation clean, consistent, and maintainable **without
changing observable behaviour**.

> **Filled at bootstrap.** `<GATE COMMAND>`, `<GENERATED ARTEFACTS>` and the stack-shaped entries
> in *Ignore* come from the interview. Delete this blockquote once they are filled.

## Scope detection (do this first)

1. Find the most recent commit whose message contains the phrase `regular maintenance`
   (`git log --grep="regular maintenance" -n 1 --format=%H`).
    - **A match is only a baseline if that commit actually carried a cleanup pass.** A commit that
      merely *discusses* the phrase — this prompt's own introduction does — matches the grep. Check
      the candidate's diff; if it is not a cleanup, keep walking back, and if none is, treat this
      as the first run.
2. Collect the files changed since that commit: `git diff --name-only <commit>..HEAD`.
3. Restrict ALL work in this run to those files.
    - If no such commit exists (first run), process the entire repository, but split the work into
      reviewable chunks if it is large.
4. Ignore generated files, build artefacts, lockfiles and vendored dependencies:
   `<GENERATED ARTEFACTS>`.
5. **Read `canon/process/maintenance/cleanup-backlog.md` before you start.** It has two tables and
   they pull in opposite directions:
    - **Deferred** — work a previous pass judged worth doing and did not do. In scope *whether or
      not its files are in the diff*, which is the reason the file exists: a skipped change in a
      file nobody touches again would otherwise never be seen. Each one may have expired, so
      reconsider rather than assume.
    - **Settled** — structures a previous pass examined and deliberately left alone. **Do not
      re-open one because a scan flagged it.** A duplicate-block scan, a dead-code scan and a link
      check flag the same deliberate boundaries every run, and without a written answer each pass
      re-derives it until one of them "fixes" something load-bearing.

## Documentation (all `*.md` files in scope)

- Simplify: make the docs precise and concise.
- Do NOT lose information — condense, do not delete facts.
- Resolve conflicts and contradictions:
    - between different documents,
    - between documents and the actual code or configuration (**the code is the source of truth**,
      unless the document clearly describes intended future behaviour — in that case flag it).
- Fix broken links, outdated file paths, stale command examples and outdated version numbers.
- Keep a consistent tone, heading structure and formatting across documents.
- If a document duplicates another, merge them and leave a link instead of a copy.

**Two directories are out of bounds, for opposite reasons:**

- **`docs/documentation/**` belongs to the documentation pass**, which regenerates it from the code
  and runs immediately after this one in the same run. Editing it here collides with that, and the
  two would disagree inside one pull request.
- **`canon/decisions/`, `canon/process/work-orders/` and `canon/process/slices/` are immutable by
  status.** An ADR records why a decision was made *then*; a work order and a slice summary record
  what was agreed and what happened. A later fact does not make them wrong, it makes them history,
  and correcting them destroys the record. A superseded decision gets a **new** ADR.

## Code (all source files in scope)

- MOST IMPORTANT: no change may break the code or alter its functionality. Refactors must be
  strictly behaviour-preserving.
- Simplify the code — improve readability and maintainability:
    - remove dead or unreachable code and unused exports, imports and dependencies,
    - eliminate needless duplication,
    - replace convoluted logic with clearer equivalents,
    - fix obviously inefficient patterns (redundant loops, repeated I/O).
- Resolve conflicts and contradictions in code:
    - inconsistent naming for the same concept,
    - comments that contradict the code (update the comment, not the behaviour),
    - conflicting configuration values or duplicated constants.
- Do NOT:
    - change public APIs, wire formats, database schemas or configuration keys,
    - upgrade dependencies or change tooling versions,
    - reformat files that are otherwise untouched.

## Verification (required before handing back)

- `<GATE COMMAND>` must pass.
- Where the gate does not itself check that committed generated artefacts are current, regenerate
  them and confirm they are unchanged. **A gate that can be green on a tree CI rejects is worse
  than no gate**, because it is believed.
- If any check fails and cannot be fixed without changing behaviour, revert the offending change
  and note it in the report instead.

## Process

`SKILL.md` has already put you on a branch and will handle the push, the pull request and the
merge. Three obligations are yours alone:

1. Make the changes in small, logically grouped commits (documentation separate from code).
2. **Each commit message must include the phrase `regular maintenance`**, unquoted, in the subject
   or the body, so the next run's scope detection finds this point. This is the only string in this
   file that must not be reworded.
3. **Reconcile `canon/process/maintenance/cleanup-backlog.md` in the same commits.**
    - **Remove** a *Deferred* row you did, and add it to *Done* with the PR that closed it.
    - **Add** a row for anything you skipped as ambiguous or risky.
    - **Move** a row to *Settled* when you conclude it should never be done, with the reasoning —
      that is what stops the next pass spending the same thought on it.
    - **Remove** a *Deferred* row whose reason has expired and which no longer applies, and say so;
      a row that stopped being true is not a row to leave for someone else.
    - Leave *Settled* alone unless you are deliberately overturning it, and say so plainly if you
      are.
    - An unchanged backlog is a fine result. Say that rather than inventing a row.

Then report back, for the pull request description:

- a summary of what was simplified or fixed,
- a list of contradictions found and how they were resolved,
- anything intentionally NOT changed and why, and where it now lives in the backlog,
- what changed in the backlog — rows added, done, settled,
- confirmation that the gate is green.

## Safety rules

- If a change is ambiguous or risky, skip it — and **write it into the backlog under *Deferred*,
  not only into the pull request description.** A PR body is read once; this rule produces no
  lasting record without the file.
- Never rewrite git history on shared branches.
- If there are no files in scope **and the backlog's *Deferred* table is empty**, do nothing and
  report "no maintenance needed". A diff with nothing in it is not an idle run while something is
  still deferred.
