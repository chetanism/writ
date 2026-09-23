# Changelog — enhancements a project can pull

One entry per enhancement to what writ puts into a project, newest first. `/writ:update` reads this
to offer each one to a project that already has writ's process, and a project records the last entry
it has considered as `writ_baseline` in `scripts/ledger.config.json`.

**An entry is written for a project deciding whether it wants the change**, not for somebody
reviewing the commit. Each says what it does, why it exists, the files it touches in the emitted
tree (`writ/…` there is the project's own tree name — `canon/`, `docs/` or whatever it chose),
and what a project will usually need to adapt. Changes to the kit's own documentation, tests or
interview are not entries: a project cannot pull them.

Add the entry in the same commit as the change. Numbers are never reused.

---

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
