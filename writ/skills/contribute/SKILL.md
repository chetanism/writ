---
name: contribute
description: Offer writ something this project built that other writ projects could use — find what the project changed or added to its process, judge honestly whether it is general, strip everything private, and file it as a GitHub issue on writ's repository for writ's maintainers to consider. Never a pull request, never code pushed. Use when the user says to contribute, push, send back or share an improvement with writ.
disable-model-invocation: true
---

# Writ — contribute

The reverse of `/writ:update`. This project has lived with writ's process and improved some of it:
a faster tool, a check that caught real defects, a template that reads better, a rule that
stopped a recurring mistake. Your job is to **offer** that to writ — as an issue a maintainer
reads, judges and re-derives in writ's own shape — and nothing more.

**You write an issue, never a pull request.** Writ's maintainers decide what to take and how;
the project's code is evidence for the idea, not a patch to apply. **The issue is public**, so
nothing private leaves this repository without the user reading the exact text first.

**The kit root is `${CLAUDE_PLUGIN_ROOT}`**, as in `/writ:update`. Writ's repository is the
`repository` field of `<kit root>/.claude-plugin/plugin.json`; if it is missing, ask for it.

Load `references/00-interview.md` now; it governs every question below.

## 1. Find where the project stands

- **The tree's name** — the `registry` path in `scripts/ledger.config.json` (`writ/`, `canon/`, …).
  Every `writ/…` in the kit means that tree here.
- **The baseline** — `writ_baseline` in the same file: the newest writ changelog entry the project
  has considered. Without one, the project predates the changelog.
- **The project's record of process changes** (`DEVELOPMENT-PROCESS.md` §15 or its equivalent), and
  `git log` over the process tree, `.claude/skills/`, `scripts/`, `CLAUDE.md` and `.github/workflows/`.

If `scripts/ledger.config.json` does not exist, this is not a writ project: stop and say so.

## 2. Find the candidates, before asking anything

A candidate is something the project **has and writ does not**. Look in three places:

1. **The record of process changes** — every line is a decision the team made about its own
   process, with its reason.
2. **History** — commits touching the process tree, skills, scripts or workflows, especially ones
   whose messages name a measurement, a defect caught, or a slowdown fixed.
3. **Divergence** — the project's skills, templates, scripts and config against the kit's
   `templates/…` (with `writ/` read as the project's tree name).

Then **discard what is not a contribution**:

- **A customisation of something writ already has** — the project's stack commands, names, cadences,
  thresholds. That is the project adapting writ, not improving it.
- **Anything writ already has** — check the kit's `CHANGELOG.md`; an entry may be the same idea in
  writ's form.
- **Anything writ's issues already carry** — search open and closed issues on writ's repository
  (`gh issue list -R <repo> --state all --search "<keywords>"`). Where one exists, the useful move
  is a comment with this project's evidence, which you offer instead.

## 3. Read back, then let the user choose

One table: each candidate, where it lives in the project, one line of what it does, and your read —
**general** (another writ project would want it as it is), **general with changes** (the idea
travels, the shape does not), or **project-specific** (say why). The user picks what to offer, and
may name something you did not find.

## 4. For each one chosen, build the case

Ask only what you cannot read, in the shape of the project's `CLAUDE.md` §*Asking me to decide*:

- **The evidence.** What it measurably changed — seconds saved, defects caught, a failure that
  stopped recurring. *"It seems nicer"* is not a case; say so plainly and recommend not filing.
- **What writ would have to change** to take it — which kit files, and what a project would then
  have to adapt.
- **Whether to name the project.** Default to *a writ project*; the user may choose otherwise.

## 5. Draft the issue

**Title:** `Contribution: <what it does, in plain words>`

**Body**, in the shape of a writ changelog entry so accepting it is a short step:

```markdown
## What
<What it does, in two or three sentences a stranger follows.>

## Why
<The failure or cost it removes.>

## Evidence
<Measurements, defects caught, before and after. Numbers where there are numbers.>

## In the project
<The files involved, as paths in the project's tree (named: `canon/` here means writ's `writ/`),
and short excerpts where the idea is in the code — tens of lines, not files.>

## Suggested shape for writ
<Which kit files would change; what a project would need to adapt; what writ should NOT copy
because it is this project's own choice.>

---
Filed with /writ:contribute · project baseline <W-NNN or "none">
```

**Strip everything private** before the user sees it: client and product names unless the user
chose to name the project, people, hostnames, internal URLs, credentials, tokens, customer data,
and identifiers that only mean something inside this project (replace `FR-PAY-04` with *a
payments requirement*). An excerpt that cannot be made safe is described instead of quoted.

## 6. Show it, confirm, file

Show the **exact** title and body. File only on an explicit yes:

```bash
gh issue create -R <repo> --title "<title>" --body-file <file> --label contribution
```

If the label is refused (it may not exist, or you may not be allowed to set it), file without it.
Without `gh` or its authentication, give the user the title and body to paste at
`https://github.com/<repo>/issues/new`.

Report the issue's URL, one line per candidate — filed, commented on an existing issue, or not
filed and why — and stop. When writ takes it, its changelog entry cites the issue, and this
project's next `/writ:update` reports it as already here.

## What this never does

Open a pull request, push a branch, fork writ, attach whole files, or file anything the user has
not read in full.
