# Changelog — enhancements a project can pull

One entry per enhancement to what writ puts into a project, newest first. `/writ:update` reads this
to offer each one to a project that already has writ's process, and a project records the last entry
it has considered as `writ_baseline` in `scripts/ledger.config.json`.

**An entry is written for a project deciding whether it wants the change**, not for somebody
reviewing the commit. Each says what it does, why it exists, the files it touches in the emitted
tree (`writ/…` there is the project's own tree name — `canon/`, `docs/` or whatever it chose),
and what a project will usually need to adapt. Changes to the kit's own documentation, tests or
interview are not entries: a project cannot pull them.

Add the entry in the same commit as the change. Numbers are never reused. An entry that came from a
project's `/writ:contribute` issue carries a `From: #<issue>` line, so the contributing project's
next `/writ:update` recognises it as already its own.

---

## W-023 — A written local gate for when a pull request's checks cannot start

*2026-09-30*

From: #8

- **What:**
  - `CLAUDE.md` §Git states the rule the process had only implied: never merge a red pull request,
    and run `gh pr checks <PR>` before every merge.
  - `DEVELOPMENT-PROCESS.md` §8.2 covers the one exception, checks that never started (a spending
    limit, failed billing, an outage, an offline runner). The local gate then takes CI's place:
    the full gate command on the exact commit, uncached and not narrowed, plus what
    `traceability.yml` runs. The merge commit names the check that could not start and carries a
    `Local-gate: <short sha> — <what ran>: <result>` trailer. It does not license trimming CI, and
    it ends when the checks run again.
  - `/slice-close` reads the checks before handing over the merge command. A failed check stops it.
    For a check that never started, it re-runs the job once, then runs the local gate itself and
    writes the trailer into `.git/SLICE_MSG`. Checks still running get `gh pr checks --watch`
    before the merge.
  - `maintenance/delivery.md` step 7 merges a pass on green checks only, or on the local gate with
    the same trailer.
- **Why:** a job the CI provider refuses to start fails in seconds, and so does every re-run. A
  project then either stops shipping or merges on nothing, and a merge that skipped the gate looks
  the same as one that passed it. The contributing project merged 77 pull requests this way during
  one Actions billing outage. Two of the rules came from its failures. A cached run was stale,
  because the cache key did not include migrations. A local gate run alone missed the docs-only
  checks that a separate workflow runs.
- **Files:** `CLAUDE.md` §Git, `writ/process/DEVELOPMENT-PROCESS.md` §6.3 and §8.2 (new),
  `.claude/skills/slice-close/SKILL.md` §6 and §8, `.claude/skills/maintenance/delivery.md` step 7
  and *Rules*.
- **Adapt:**
  - Say in §8.2 how your build tool bypasses its cache (`--force`, `--no-cache`, a clean output
    directory).
  - If your CI has workflows beyond `gate.yml` and `traceability.yml`, name each one's steps in
    item 2.
  - Without GitHub Actions, replace `gh pr checks` with your CI's own status command. The rule and
    the trailer stay the same.

## W-022 — Conventions in their own file, one section per area, with a cap of their own

*2026-09-30*

From: #9

- **What:**
  - Conventions move out of `CLAUDE.md` into a new `writ/process/CONVENTIONS.md`, one numbered
    section per area. Each bullet is the rule and its citation, the slice and the ADR that set it,
    and nothing else. A rule that has become a check is just the check's name.
  - `CLAUDE.md` §*Where the conventions are* replaces §*Conventions set here and binding
    afterwards*. It is a routing table, *touching X → read §N*, plus the few rules that span every
    area.
  - `/slice-open` reads, in full, every section the plan touches. DoD-8 and `/slice-close` send a
    new convention to its section, and `CLAUDE.md` changes only for structure, a new area or a rule
    that spans every area.
  - `context_budget.files` entries may be `{"path", "warn_chars", "max_chars"}` beside plain
    paths. A plain path keeps the shared numbers, and an entry that is neither is a check error.
    `CONVENTIONS.md` is budgeted at 40,000 characters (warn) and 60,000 (ceiling).
  - `/context-compact` covers both files. For conventions it cuts each bullet back to its rule and
    citation where the cited summary or ADR already carries the story.
- **Why:** a cap on `CLAUDE.md` alone doesn't stop the growth; it moves it into files with no cap.
  On the contributing project the conventions file had grown to 352k characters of incident
  narrative, and the pre-code read to 150–250k tokens, while the agent map's budget stayed green.
  Cutting each bullet to its rule and citation took it to 198k with every rule kept. Reading only
  the sections a change touches is what keeps the read small once the file is large.
- **Files:** `CLAUDE.md`, `writ/process/CONVENTIONS.md` (new), `writ/process/DEVELOPMENT-PROCESS.md`
  §1, §4 DoD-8, §9 and §15, `scripts/ledger.py`, `scripts/test_ledger.py`,
  `scripts/ledger.config.json`, `.claude/skills/slice-open/SKILL.md`,
  `.claude/skills/slice-close/SKILL.md`, `.claude/skills/context-compact/SKILL.md`,
  `.claude/skills/design-system/SKILL.md`.
- **Adapt:**
  - Move your existing conventions list into sections named for your own areas, not the template's
    five, and write the routing table to match.
  - Cut each bullet to its rule and citation as you move it. Set the cap from what the file weighs
    after that cut, not before.
  - Your tree name replaces `writ/` in the budget entry's path.

## W-021 — A falsify control can name the test files that can notice it

*2026-09-30*

From: #11

- **What:** an entry in a falsify plan may carry `files`: the test files, among those its `expect`
  identifiers resolve to, that can notice this control. Only those run. `falsify.py` refuses a file
  no `expect` identifier annotates, and an empty or malformed `files`. Without the key nothing
  changes.
- **Why:** a requirement is usually tested by a unit file and an integration file. When the control
  sits in code the unit file already decides, running the integration file too adds a full-stack
  run to every control and catches nothing more. On the contributing project a 15-control plan took
  139 s with `files` and 890 s without, with the same verdict. The subset rule keeps the narrowing
  honest: a control can never be caught by a test its claim does not cover.
- **Files:** `scripts/falsify.py`, `scripts/test_falsify.py`, `.claude/skills/slice-close/SKILL.md`
  §3a.
- **Adapt:** nothing. The key is optional, and existing plans run as before.

## W-020 — A usage guide for the product's users, and the product documentation re-aimed at the team

*2026-09-30*

From: #10

- **What:**
  - A new `/product-guide` writes a living usage guide for the product's own users under
    `docs/documentation/guides/`. It has one directory per persona from `writ/spec/personas.md`,
    for people only, never system actors or the team. Each task is walked step by step through the
    real screens, UI first, with the API only for a persona who integrates the product.
  - A role that lacks a control is noted inline on the step it affects, from the permission check in
    the code, rather than forking the page. Every quoted label is checked against the source.
  - It is incremental, anchored on its own commit subject, `docs: update product guide`. It lands
    through `maintenance/delivery.md` like a pass, and `/maintenance` does not run it.
  - `/product-docs` is re-aimed at the team building the product: developers, engineering and
    product managers, and new joiners. The line between the two is absolute: what the product is
    and how it is built is the documentation's, what to click, type or run is the guide's, and each
    links to the other rather than repeating it. `/product-docs` never writes, restructures or
    removes `guides/`.
- **Why:** `/product-docs` addressed engineers and business stakeholders at once, which serves
  neither, and nothing in writ was written for somebody using the product. Once a product has
  users, that gap is the first thing a support team or a first customer runs into.
- **Files:**
  - `.claude/skills/product-guide/SKILL.md` (new).
  - `.claude/skills/product-docs/SKILL.md` (§Audience, *Structure*, removals).
  - `.claude/skills/maintenance/delivery.md` (a row for the guide) and `maintenance/SKILL.md`.
  - `.claude/skills/cleanup/SKILL.md` and `writ/maintenance/cleanup-backlog.md` `CL-S1`.
  - `.claude/skills/context-compact/SKILL.md` §3.
  - `writ/process/DEVELOPMENT-PROCESS.md` §9 and §11.
  - `CLAUDE.md` *Skills*.
- **Adapt:**
  - Fill the persona table from the project's own personas. Personas who work in the same
    application share a directory.
  - With no user interface, keep only the persona who integrates the product. With no users
    outside the team, skip the skill and take only the `/product-docs` audience change.
  - Fill `<DOC BUILD COMMAND>` from `product-docs/SKILL.md`.
  - A project whose documentation already addresses users in `/product-docs` moves those pages to
    `guides/` in the guide's first run.
  - Set the guide's cadence in §11.

## W-019 — The tools read what a project actually writes, and restore what they touch exactly

*2026-09-30*

- **What:** fixes to every script writ puts into a project, found by a review of each against
  plausible input.
  - `ledger.py`
    - A detail or scenario file no longer declares the requirement it elaborates. With the shipped
      config, the first `/requirement-detail` made `check` fail with *declared twice*, and a detail
      file brought a withdrawn requirement back to life.
    - A table cell may carry an escaped `\|` or a pipe inside a code span.
    - A code fence closes only on its own character and length, so a ```` ```bash ```` example
      inside a ```` ````markdown ```` block is no longer read as prose, and a table inside any fence
      declares nothing.
    - A section name matches whole words: `BRD requirements` no longer matches `# BRD`.
    - A byte-order mark no longer hides a work order's front matter, and `id: 042` stays `042`.
    - `Withdrawn.` retires a row as `Withdrawn` does.
    - The queue block is spliced idempotently even when `<!-- /generated -->` appears above it.
    - `stats` reads a phase keyed `letter`.
    - A change request with no rows is neither applied nor built.
    - Globs understand `[...]`.
    - `size_budget` is the project's own tiers, replacing the defaults rather than merged into
      them, and a slice over a non-zero top-tier ceiling fails.
  - `falsify.py`
    - It restores every file byte for byte, CRLF included.
    - On timeout, it kills the whole runner process group.
    - A hangup restores the tree the way an interrupt does.
    - It accepts shell redirections in the runner and a one-identifier `expect` string.
    - A path with glob characters (`app/[id]/page.tsx`) is read as the file it names.
  - `claims.py apply` keeps a CRLF work order's line endings.
  - `velocity.py`
    - It counts files whose names hold a space or a character outside ASCII.
    - It dates a merge by when it landed (committer date), so a rebased commit keeps its week.
    - It says *no commits yet* instead of a traceback.
  - `survey.py` runs from a subdirectory or a linked worktree, and reads paths outside ASCII.
  - `design_tokens.py`
    - A theme block redeclares every token that depends on an override, so `data-theme` on an
      element below `<html>` themes it fully.
    - `extract` keeps the spaces in `oklch(0.5 0.1 200)`.
    - Zero is never a finding in any unit.
    - `PR #123` in a component's text is not a colour, and a member name such as `theme.red` is
      not a named colour.
    - A one-line `@media` rule's declarations are scanned.
    - An exemption needs a reason after the marker.
    - A malformed tokens file is a finding, not a traceback.
    - The shipped `design.sources` scans what the defaults scan: `.vue`, `.svelte` and `.less`
      files are read, and `build/` and `.next/` are skipped.
  - `.github/workflows/traceability.yml` runs every tool's own suite, not only the ledger's.
- **Why:** each was a false failure in the gate, a check that silently did not run, or a file left
  changed on disk. The duplicate declaration broke the requirement track on first use.
- **Files:** every file under `scripts/` except `ledger.config.json`, which changes only in its
  `design.sources` block and `writ_baseline`. Also `.github/workflows/traceability.yml`.
- **Adapt:**
  - If the project sets its own `size_budget`, list every tier it wants, in order, because the
    defaults are no longer merged in. A top tier with a ceiling now fails a slice over it; set that
    tier to `0` for no ceiling.
  - If it trimmed `design.sources`, re-apply the trim to the new block.
  - `velocity.py`'s weekly figures can move between weeks for rebased history.
  - Otherwise nothing, unless the project changed one of these functions.

## W-018 — A design system for the web interface, with a check that holds the code to it

*2026-09-30*

- **What:** a new `/design-system` skill designs the web interface's design system with the reader,
  or recovers it from the code. It covers colour, type, space, radius, elevation and motion tokens
  in every theme, and the component inventory with every state and keyboard contract. It runs as a
  slice of its own before the first screen. The values live only in a tokens file (the W3C design
  tokens shape). They compile to CSS custom properties, and optionally to a Tailwind v4
  `@theme inline` block (which resets the default palette) and a TypeScript module. The rules live in `writ/spec/UI-SPEC.md`, a
  foundation spec with a `UI-NN` index that names tokens and never values. A new stdlib-only
  `scripts/design_tokens.py` has three commands:
  - `build` writes every output named in `design.outputs`.
  - `check` fails on a reference that does not resolve, an output that is not what the tokens
    compile to, a declared contrast pair below its floor in any theme (WCAG 2), or a raw colour
    (including a named colour where a colour is set) or length in the source.
  - `extract` counts every literal an existing codebase uses and groups the colours the eye cannot
    tell apart. It is where the skill starts on a codebase that already has an interface.

  Before the interview, the skill settles the aesthetic direction. It offers the taste skills the
  session already has, or helps the reader find one, presenting candidates and never installing
  them. The choice is recorded in `design.taste` and an ADR, under two rules: tokens win, and the
  check never bends. A direction round records reference products and bans. The specimen page is
  screenshotted in each theme and reviewed, and the review says so when no browser tool is there.

  `/design-system audit` is report-only and writes a dated report of drift and of which directory
  to bring inside the rule next. The raw-value rule is a new perimeter rule, `enforce.design_values`,
  so an adopted codebase turns it on one directory at a time.
- **Why:** a design system written down and not checked is a style guide, and a style guide stops
  being followed within a quarter. Somebody writes a grey that is not quite any of the greys into a
  component, nothing objects, and a year later there are forty greys and a dark theme that works on
  half the screens. Contrast failures show up in an accessibility complaint rather than in the build.
- **Files:** `.claude/skills/design-system/SKILL.md`, `reference/foundations.md` and
  `reference/components.md` (new); `scripts/design_tokens.py` and `scripts/test_design_tokens.py`
  (new); `scripts/ledger.config.json` (`design` block with `outputs`, `prefix` and `taste`,
  `enforce.design_values`, `path_scan.allow`);
  `.github/workflows/gate.yml` (the `design tokens` step); `writ/process/DEVELOPMENT-PROCESS.md`
  §6.4, §11, §15; `writ/maintenance/audits/README.md`; `CLAUDE.md` *Commands* and *Skills*.
- **Adapt:** take it only if the project has a web interface. With `design.tokens` empty the check
  reports itself off and passes, so the gate step is safe to add before the first run. Set
  `design.sources.globs` to the framework's files (`**/*.vue`, `**/*.svelte`). A project that
  already has code should set `enforce.design_values` to `[]` before the first run and widen it one
  directory at a time. A project whose component library has its own theme variables maps the
  semantic tokens onto them rather than replacing them. The spec records that mapping. The
  Tailwind output needs `design.prefix`, and its palette reset removes Tailwind's default colour
  classes, so migrate their uses first.

## W-017 — A coverage review finds ledger rows that are wrong, and merged work orders' claims can be corrected

*2026-09-25*

From: #7

- **What:** a new report-only `/coverage-review` looks for rows in `COVERAGE.md` that are **wrong
  rather than unbuilt**. A new `scripts/claims.py classify` sorts them into four buckets, using the
  ledger's own collector: `inherited` (`≈`, tests and no claim), `partial_only` (every claiming
  slice done and `partial`), `claim_no_test` and `unclaimed_mentioned` (`○`, but named in a work
  order, summary or test file). Each row is judged clause by clause against its register row, and
  every `DONE` is re-read. The review writes a dated report and a corrections JSON under
  `writ/maintenance/audits/`, with a skip list keyed to each row's evidence so the next run judges
  only what moved. `claims.py apply` is run by a person. It checks every entry first — the work
  order is `done`, the identifier is declared and live, a move to `satisfies` has a test naming it
  — then edits only the `satisfies:` and `partial:` lines, and prints the commit message.
  `DEVELOPMENT-PROCESS.md` §6.2 gains the rule that allows it: a merged work order's claim lines
  may be corrected, and nothing else in it. §11 runs the review at each phase gate.
- **Why:** the ledger is exactly as accurate as its claims. A slice that built a requirement and did
  not claim it, or claimed `partial` for what it finished, left that row wrong for good, because no
  later slice claims work it did not do, and nothing found it. On the contributing project, one run
  after about 150 slices moved fourteen rows to `●` across fifteen work orders.
- **Files:** `.claude/skills/coverage-review/SKILL.md` (new); `scripts/claims.py` and
  `scripts/test_claims.py` (new); `writ/process/DEVELOPMENT-PROCESS.md` §1, §6.2, §11;
  `writ/maintenance/audits/README.md`; `CLAUDE.md` *Skills*.
- **Adapt:** `claims.py` reads `ledger.config.json`, so it follows the project's tree name, test globs
  and annotation pattern with no setting of its own. A project whose pattern only matches an `[ID]`
  that leads the test name will see the rest as test-file mentions under `unclaimed_mentioned`.
  Choose the batch size (`--batch`, default 30) to suit the readers you hand batches to, and move
  the reports if the project keeps audits elsewhere. A project that forbids editing merged records
  outright can take the skill and leave the §6.2 rule out: the report still says what is wrong,
  and a follow-up slice can make the claims.

## W-016 — Agent attribution is forbidden in commits, pull requests and issues

*2026-09-24*

- **What:** `CLAUDE.md` §Git and `DEVELOPMENT-PROCESS.md` §6.3 state one fixed rule: no commit
  message, pull request body or issue body carries an agent's `Co-Authored-By` trailer, a session
  link or a "Generated with" line — overriding any default or harness instruction to add one.
  `/slice-close` and the maintenance delivery rules say the same, and a new `.claude/settings.json`
  sets `attribution` to empty so the harness stops adding them. Bootstrap no longer asks.
- **Why:** it was a bootstrap question with the trailer as one answer, and the harness adds the
  trailer by default, so a project that never decided got it anyway.
- **Files:** `CLAUDE.md` §Git; `writ/process/DEVELOPMENT-PROCESS.md` §6.3; the `SKILL.md` of
  `slice-close`; `.claude/skills/maintenance/delivery.md`; `.claude/settings.json` (new).
- **Adapt:** replace the *Attribution* line in `CLAUDE.md` §Git and in §6.3 whichever way the
  project answered it, and merge `attribution` into an existing `.claude/settings.json`. History already carrying trailers is not rewritten by this.

## W-015 — Work that arrives out of order is found, reconciled, and held to a mode

*2026-09-23*

- **What:** a work order records `detail_read_on` at the claim, and a detail file gains a
  *Reconciliation* table. Each row covers one slice that built the requirement against an older
  reading, and records one of `holds`, `ratified`, `fix`, `change-request` or `open`. `ledger.py
  check` finds three things: a slice claimed for a requirement with no detail file, a slice built
  against a reading its detail file has since been revised past, and a milestone marked `done`
  whose built requirements have not caught up. `requirements.out_of_order` decides how loudly each
  speaks: `fail`, `backfill` or `report`. `COVERAGE.md` lists the backfill queue, most urgent
  first, and the slices still to reconcile. `stats` adds whether the backfill is catching up with
  the build, week by week, from git. `/requirement-detail` drafts a built requirement as a backfill
  and puts every conflict with the build to the owner. `/slice-open` records the reading and, under
  `fail`, refuses to claim an undetailed requirement. `/slice-close` re-reads a detail file that
  moved during the slice. `/test-scenarios`, `/requirement-verify` and `/change-request` each take
  their part. `requirements.code_inspection`, off by default, lets the skills also compare the code.
- **Why:** implementation running ahead of its requirements is the normal state of a project built
  with agents, not an exception. Before this, nothing noticed when it happened, and a detail file
  written after the code tended to describe the code, so the requirement quietly became whatever
  got built. The owner now decides each conflict, and only the owner ratifies.
- **Files:** `scripts/ledger.py`, `scripts/velocity.py`, their tests, `scripts/ledger.config.json`
  (`requirements.out_of_order`, `requirements.code_inspection`); `writ/process/DEVELOPMENT-PROCESS.md`
  §1, §11, §12, the new §12.1 and §15; `writ/process/templates/work-order.md` and
  `requirement-detail.md`; `writ/spec/milestones.md`; `writ/spec/requirements/README.md`; the
  `SKILL.md` of `requirement-detail`, `slice-open`, `slice-close`, `test-scenarios`,
  `requirement-verify` and `change-request`.
- **Adapt:** choose the mode. `fail` suits a project whose detail files already lead its slices.
  `backfill` suits one whose build runs ahead of its requirements, or an adopted codebase. Leaving
  it unset means `report`, which fails nothing. Slices in progress need `detail_read_on` before the
  next check (except under `report`). Finished work orders have none, and they are listed as
  `not recorded` warnings against every detail file of what they built until a *Reconciliation* row
  settles each one. Setting a done work order's `detail_read_on` to its merge date clears that
  faster, but only where the project is sure its detail files did not change while the slice was
  open. `require_detail_for_satisfied` is superseded by `out_of_order` and still honoured; drop it
  once the mode is set.

## W-014 — `velocity.py` and `falsify.py` refuse to run outside a git repository

*2026-09-24*

- **What:** with no repository at the current directory or at `--root`, both tools print *not a git
  repository — run it inside one, or pass --root* and exit 1.
- **Why:** `velocity.py` crashed with a traceback from `git log`. `falsify.py` quietly skipped the
  uncommitted-changes refusal that keeps a restore from destroying unsaved work — it would remove
  code it could not prove was safe to put back.
- **Files:** `scripts/velocity.py`, `scripts/falsify.py`, and their tests.
- **Adapt:** nothing, unless the project changed either tool's `main()` or `repository_root()`.

## W-013 — `velocity.py` and `falsify.py` measure the repository they are run from

*2026-09-24*

- **What:** with no `--root`, both tools now use the git repository of the current directory, and
  `velocity.py` uses `ledger.py`'s glob matcher instead of its own copy.
- **Why:** run from another checkout (`python3 ../elsewhere/scripts/velocity.py`), the old default
  silently measured the repository the script sat in. Two copies of the matcher could drift.
- **Files:** `scripts/velocity.py`, `scripts/falsify.py`.
- **Adapt:** nothing, unless the project changed either tool's `main()`.

## W-012 — `/slice-open` opens with a brief; `/slice-close` ends with `/clear` or `/compact`

*2026-09-23 · 8f89c56*

- **What:** the slice-open report starts with two or three plain sentences on what the slice will
  do. The slice-close report ends with a lettered ask recommending `/clear` once the merge has run,
  or `/compact` when something from the session is not in a file yet.
- **Why:** the approver can tell at a glance it is the slice they meant; the next slice starts from
  the files rather than from a long session's history.
- **Files:** `.claude/skills/slice-open/SKILL.md` §5, `.claude/skills/slice-close/SKILL.md` §8.
- **Adapt:** the example slice in the brief.

## W-011 — Plain-language templates

*2026-09-23 · b93957a*

- **What:** the work-order, slice-summary, requirement-detail, test-scenarios, requirement-area,
  change-request and ADR templates open with a short *What this is:* note in plain words, and the
  long guidance blockquotes are cut to the rules a writer would otherwise get wrong. The authoring
  style asks for plain words first. Every heading `ledger.py` checks is unchanged.
- **Why:** these documents are read by testers, product owners and new teammates, not only by the
  people who wrote the process.
- **Files:** `writ/process/templates/*.md`, `writ/decisions/template.md`.
- **Adapt:** a project with its own thinner template keeps it and takes only the *What this is:*
  note. Drop the `Provenance` paragraph from the area template unless the project was adopted.

## W-010 — Asks carry a recommendation and their own context

*2026-09-23 · b93957a*

- **What:** an always-emitted *Asking me to decide* section in `CLAUDE.md`: asks numbered, options
  lettered, each option saying why it is or is not recommended, exactly one recommended, the fact
  each turns on quoted, and a one-line summary of any document the ask points at. The skills that
  ask questions follow it, and the open-questions register gains a `Recommended` column.
- **Why:** answering should never mean opening another file, and a bare menu hands the thinking back.
- **Files:** `CLAUDE.md`, `writ/spec/questions.md`, the `SKILL.md` of `requirement-detail`,
  `test-scenarios`, `manual-test`, `change-request`, `process-change`, `slice-open`.
- **Adapt:** the example ask. A project with its own ask format usually takes only the parts it
  lacks.

## W-009 — `/test-all`, and affected-only runs while working

*2026-09-23 · b93957a*

- **What:** a new skill that runs the whole suite on demand — ledger check, unit, stack up,
  integration, stack down — timing each part and naming the slowest tests. `CLAUDE.md` gains an
  *affected test* command for the inner loop, and the process says: affected while working,
  everything before close.
- **Why:** running everything after every edit is how a suite gets slow enough that people stop
  running it; something still has to run everything, on purpose, before the push.
- **Files:** `.claude/skills/test-all/SKILL.md` (new), `CLAUDE.md` commands and skills tables,
  `writ/process/DEVELOPMENT-PROCESS.md` §3.3.
- **Adapt:** the commands, the order (a suite that times out with the stack up stops it first), and
  how the stack is brought down — never a command that destroys volumes other work depends on.

## W-008 — Falsification by tool

*2026-09-23 · b93957a*

- **What:** `scripts/falsify.py` reads a per-slice JSON plan of controls, removes each, runs only the
  test files annotated with the requirements it should break, and restores the file even on Ctrl-C.
  It runs a baseline first and reports an already-red file as unreliable. `ledger.py annotations`
  maps identifiers to test files. `/slice-close` §3a uses it.
- **Why:** falsification is the step that finds defects, and its cost was the hand loop around the
  test runs — a few hundred times per project.
- **Files:** `scripts/falsify.py`, `scripts/test_falsify.py` (new), `scripts/ledger.py`
  (`annotated_files`, the `annotations` subcommand), `falsify` block in `scripts/ledger.config.json`,
  `.claude/skills/slice-close/SKILL.md`.
- **Adapt:** `falsify.runners` — how the stack runs a named list of test files, split so unit and
  integration never share a run. `cwd: "package"` gives one run per package in a monorepo.

## W-007 — Velocity from git, and size tiers off

*2026-09-23 · b93957a*

- **What:** `scripts/velocity.py` counts code and Markdown lines per merge and per week from git, and
  `--check` flags a week well below the ones before it or Markdown outgrowing code. `/maintenance`
  runs it; `ledger.py stats` shows it; it never runs in the gate. Size tiers are off by default
  (`size_budget: {}`), the work order loses its size fields and the queue its Size column.
- **Why:** both projects this came from found the declared tiers served no reader, and a slowdown
  nobody measured went unnoticed for weeks.
- **Files:** `scripts/velocity.py`, `scripts/test_velocity.py` (new), `velocity` and `size_budget` in
  `scripts/ledger.config.json`, `scripts/ledger.py` (`velocity_lines`, the queue), the work-order
  template, `/slice-open`, `/slice-close` §2, `/maintenance`, `DEVELOPMENT-PROCESS.md` §2.1.
- **Adapt:** `velocity.generated` — every generated path in the project. The thresholds after a
  month of history.

## W-006 — New `ledger.py` checks: decisions, cited paths, acceptance criteria

*2026-09-23 · b93957a*

- **What:** `check_decisions` refuses an ADR constraining nothing, two with one number, or a name no
  audit can read. `check_paths` refuses a path cited in a standing document that is not there
  (`path_scan`). An open slice's acceptance criterion must name an identifier its front matter
  claims. A CLAUDE.md budget message names the three largest sections.
- **Why:** each is a way two documents disagreed with the gate still green.
- **Files:** `scripts/ledger.py`, `scripts/test_ledger.py`, `path_scan` in the config, the work-order
  template's criteria note, slice zero's criteria.
- **Adapt:** `path_scan` include, exclude and allow. Existing ADRs need a `Constrains` row before
  this lands.

## W-005 — Decisions read from an index, and written only when they bind later work

*2026-09-23 · b93957a*

- **What:** `INDEX.md` carries one table of every ADR with its decision and what it constrains, and
  `/slice-open` reads that instead of grepping the directory. An ADR is written only for a decision
  that binds a later slice, in a short form; one that shapes only the current slice is a code
  comment and a row in its summary.
- **Why:** an area grep over a mature decisions directory was most of a context window per slice.
- **Files:** `scripts/ledger.py` (`decision_facts`, `render_index`), `writ/decisions/README.md` and
  `template.md`, `/slice-open` §2a, `CLAUDE.md`, `DEVELOPMENT-PROCESS.md` §7.
- **Adapt:** older records whose constraint row is spelled differently.

## W-004 — A thinner close: five sections and a line, one-line DoD for command-proven rows

*2026-09-23 · b93957a*

- **What:** the slice summary is what it does now, how it works, decisions, surprises,
  falsification, and a one-line *Played*. `/slice-close` reports the definition-of-done rows a
  command proves in one line and walks only the rest. The DoD rationale moves to
  `writ/process/RATIONALE.md`.
- **Why:** the per-slice writing cost stayed fixed while slices shrank; the dropped sections
  restated the work order or a generated file.
- **Files:** `writ/process/templates/slice-summary.md`, `writ/process/RATIONALE.md` (new),
  `DEVELOPMENT-PROCESS.md` §4, `/slice-close` §3 and §5.
- **Adapt:** which DoD rows the project's gate actually proves.

## W-003 — CI: pull requests only, and complementary workflows

*2026-09-23 · b93957a*

- **What:** no `push:` triggers; the traceability workflow runs on exactly the pull requests the gate
  skips; the work-order perimeter check moves into the gate, so code-only pull requests run it; a
  cache step with a warning about task caches reading repository-wide files.
- **Why:** re-checking a tree the pull request already passed was over half of one project's CI
  minutes, and the perimeter check never ran on the pull requests it was about.
- **Files:** `.github/workflows/gate.yml`, `.github/workflows/traceability.yml`.
- **Adapt:** the cache paths. Skip the perimeter move if the project has no `enforce` perimeter.

## W-002 — Faster `ledger.py`

*2026-09-23 · b93957a*

- **What:** excluded subtrees are pruned during the walk instead of listed and discarded; the
  reference scan asks one combined question per line before the per-family ones; the fence regex is
  compiled once.
- **Why:** on a large monorepo `check` went from tens of seconds to a few.
- **Files:** `scripts/ledger.py` (`iter_files`, `walk_matching`, `check_references`).
- **Adapt:** nothing. The walk only helps unrooted `**/` include globs; a project whose globs start
  at `apps/*/src/` will not see a difference.

## W-001 — Stack guidance for a fast suite

*2026-09-23 · b93957a*

- **What:** the stack references now cover an *affected* gate role, parallel unit tests, integration
  in parallel once each test owns its data, migrations applied once per run, no per-test timeout on
  unit tests, one local stack per session, and `.claude/worktrees/` kept out of git and linters.
- **Why:** these are what made the two projects' suites fast and reliable.
- **Files:** none emitted directly — the project's own test config, `.gitignore` and lint ignores.
- **Adapt:** everything; it is guidance for the project's stack.

## W-000 — The baseline

Everything writ emitted before this changelog began. A project bootstrapped earlier has no
`writ_baseline` and is offered every entry above, each checked against what it already has.
