---
name: product-docs
description: Regenerate the living product documentation under docs/documentation/ from the code — what the product is today, for engineers and product readers who have read nothing else — updating only what changed since the last pass, delivered on its own branch through a pull request. Use after a phase lands or on demand; it is also the second of the three passes /maintenance runs.
---

# Update product documentation

You are updating the **living product documentation** for this project. The documentation describes
**what the product is today** — a snapshot of the current state, never a history or a changelog of
how it evolved.

Invoked as `/product-docs` on its own, or by `/maintenance` as the second of its three passes.
**This file owns what changes.** `.claude/skills/maintenance/delivery.md` owns the branch, the
commits, the pull request and the merge — read it first, and run this file inside its loop.

> **Filled at bootstrap.** `<DOC BUILD COMMAND>`, `<DOC BUILD OUTPUT>` and the site conventions in
> *Structure* come from the interview. Where the project has no site generator, the *Verification*
> section says so instead. Delete this blockquote once it is filled.

## Audience

Both **engineers** and **product or business stakeholders** joining the project who have read
nothing else. After reading, they should understand what the product does, its main domain
entities, its key workflows and its features — without needing to read the ADRs, work orders, slice
summaries or BRD themselves.

- Lead every page with plain-language explanation for product readers.
- Follow with technical detail (entities, data flow, integration points) for engineers.

## Source material and ground truth

1. **Code is the source of truth.** Derive entities, workflows and behaviour from the codebase:
   routes, domain logic, schemas, data models and contracts.
2. Written documents live in `canon/`: the BRD, the foundation specs, ADRs, work orders and slice
   summaries. Use them to understand intent, terminology and requirements.
3. **Conflicts:** if a document contradicts the code, document what the CODE does, and add a
   clearly visible flag in the affected page:
   > ⚠️ **Conflict:** `the document` says X, but the code does Y. Needs resolution in code or docs.

   Also list every conflict in the report you hand back, for the pull request description.

## Incremental update process

1. Find the most recent documentation update commit:
   ```bash
   git log --grep="docs: update product documentation" -n 1 --format=%H
   ```
   **Not anchored with `^…$`.** A squash merge composes the subject from the pull request title and
   appends ` (#N)`, so an anchored pattern misses every run delivered through a pull request — it
   matches the first such run and then silently misses the same work one merge later. Match the
   phrase, and confirm the candidate actually carried a documentation update before accepting it as
   a baseline.
2. **If a commit is found:**
    - Inspect changes since then: `git diff <commit>..HEAD --stat`, then examine the changed source
      files, schemas, migrations and documents under `canon/`.
    - Update ONLY the documentation pages affected by those changes.
    - Additionally, fix anything you notice is factually outdated even if untouched by the diff.
3. **If no commit is found (first run):** generate the full documentation from scratch.
4. **Removals:** if a feature, entity or workflow was removed from the product, remove its
   documentation — but explicitly list every removal in the report so a human can review and veto
   it during the pull request review.

## Structure

All documentation lives in `docs/documentation/`, written in Markdown. Required layout — adapt and
extend as the product requires:

```text
docs/documentation/
├── index.md             # Landing page: what the product is, who it is for, doc map
├── overview.md          # High-level product overview and core concepts
├── entities/
│   ├── index.md         # Entity map and relationships overview
│   └── one-entity.md    # One file per major entity, or grouped where sensible
├── workflows/
│   ├── index.md
│   └── one-workflow.md  # End-to-end user and system workflows
├── features/
│   ├── index.md
│   └── one-feature.md   # Features derived from the BRD, grouped logically
└── glossary.md          # Domain terms and definitions
```

Conventions, which are what a site build depends on:

- `index.md` (not `README.md`) as the landing page of the directory and of each subdirectory.
- Kebab-case filenames, one H1 per file, relative Markdown links only.
- Mermaid code blocks for workflow and entity-relationship diagrams.

**Navigation is read from the filesystem, never listed.** A page's sidebar entry is its H1 and a
section's is its directory, so a page added here appears by having been added and there is no
navigation file to update — but a file with no H1 falls back to its filename, and a link to a page
that does not exist breaks the build.

## Verification

**With a site generator:** run `<DOC BUILD COMMAND>` before committing. Its output,
`<DOC BUILD OUTPUT>`, is **gitignored and must stay that way** — it is a local read, and a hundred
regenerated files per pass would bury the Markdown diff that is the reviewable part. The build is
run for what it *checks*: a dead relative link or a missing anchor is a build failure here rather
than a broken page found by a reader. A run that ends with the build failing is not done, whatever
the Markdown looks like. Do not create, edit or delete anything in the generator's own
configuration directory; it is the build, not the documentation.

**Without one:** check every relative link and anchor in the pages you touched by reading — that
each target file exists and each `#anchor` matches a heading in it. This is the same check the
build would have done, and it is the one that matters.

## Delivery

`delivery.md` owns the branch, the push, the pull request and the merge. Two obligations are yours
alone:

1. **Commit with the subject line `docs: update product documentation`**, and give the pull request
   that same title — a squash merge appends ` (#N)` to it, which step 1's unanchored pattern still
   matches. This is the only string in this file that must not be reworded.
2. Report back, for the pull request description: what was added, what was updated, every
   **removal** (so a human can veto it in review), and every ⚠️ conflict flagged.
