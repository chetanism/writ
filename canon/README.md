# `canon` — an agent-first development process, as a plugin

A kit for setting up a new project's development process: a business requirements document, an
identifier registry, foundation specs, a dependency-ordered slice queue, work-order and
slice-summary templates, a CI gate, and a traceability tool that refuses to take a work order's
word for anything.

It was extracted from a real project and generalised. **The core is stack-agnostic**; the specifics
that project proved out live in a stack annex you load one of.

## Documentation

This file is the **reference** — the full generated tree, the four mechanisms, the tool, and every
adaptation switch. The guides are next door in [`docs/`](docs/):

| | |
|---|---|
| [How to use it](docs/using-it.md) | Running a bootstrap skill, then living in the loop, and what each step buys you |
| [The fifteen skills](docs/skills/README.md) | One page each — what it does, when to run it, what it refuses to do |
| [Changing the process](docs/changing-the-process.md) | It is not a static library. How to reshape it by prompting, and the three parts to think twice about |

> This directory is a Claude Code plugin. It is inert inside the repository that carries it — see
> `CLAUDE.md` here — and nothing of it is copied into the projects it bootstraps.

## Installing it

From the repository that carries this directory, which is also a plugin marketplace:

```bash
claude plugin marketplace add /path/to/this/repository     # once
claude plugin install canon@nevic-skills               # once
```

Or, to try it without installing, start Claude Code in the new project with the plugin loaded for
that session only:

```bash
cd ~/projects/new-thing && git init        # if it is not a repository yet
claude --plugin-dir /path/to/this/repository/canon
```

## Using it

In the new project, in Claude Code:

- **A new project, one person building it** → `/canon:solo`.
- **A new project, more than one person** → `/canon:team`. It designs the roles and handoffs, and
  retrofitting those is harder than choosing correctly at the start.
- **A codebase that already exists** → `/canon:adopt`. Different problem, so a different skill
  rather than a flag on the other two: the code is the most reliable document in the room, and the
  job is writing down what it *cannot* say about itself.

All three are user-invoked only; Claude never starts one on its own.

Have your BRD to hand — or do not. **Two paragraphs is a valid input**; the interview writes the
rest with you. Expect two to three rounds of questions if you arrive with a finished specification,
and six to ten if you arrive with an idea.

It finishes by committing the generated tree on `dev`. Add a remote and branch protection then, if
there is none yet; `/slice-open` works without one but the draft pull request and the CI gate wait.

Everything it produced is the project's own. The kit reads its references and templates from the
plugin's install directory, so there is nothing to delete afterwards and nothing of the kit to
edit by mistake instead of the documents it generated.

**The tree is called `canon/` by default** — the authoritative body of documents an agent reads
before it writes code: the specification, the registry, the process, the decisions, the
requirement detail and the test scenarios. Phase 0 asks what to call it, and any single path
segment works; `docs/` stays free for the generated product documentation `/product-docs`
writes.

## When not to use it

This document argues for the process everywhere else in it, so here is the other side, stated as
plainly: **the kit is a bet that the project will outlive anybody's memory of it.** Every mechanism
in it trades effort now for legibility in six months. Where there is no six months, it is overhead
with no return.

Do not run it for:

- **Something you will throw away.** A spike, a bake-off, a script that answers one question. The
  interview alone is forty questions before the first line of code, and the answer to most of them
  is *it does not matter, this is going in the bin.*
- **A codebase that already has a process.** Adopting the parts is fine — the declaration rule and
  the ledger stand alone — but running the bootstrap over a working process replaces something
  people already follow with something they have to learn, and the second one loses.
- **Something one person will build in a fortnight and then finish.** The failure this is shaped
  around is velocity outrunning comprehension over months. Over a fortnight nobody has forgotten
  anything yet.
- **A project whose requirements genuinely are not knowable yet.** Research, a prototype whose
  point is to find out what it should do. Registers assume there is something to declare; declaring
  a guess as a requirement is worse than writing nothing down, because everything downstream will
  be built and tested against it and nobody will remember it was a guess.

Where it is worth it: **more than one milestone, more than one person's memory, and code written
faster than it can be read** — which is every project built with coding agents that anybody intends
to keep.

And the parts separate. `scripts/ledger.py` with a registry and some work orders is perhaps a
quarter of the value for an afternoon of setup, and it is the quarter that compounds. Phase 10's
requirement track, the standing passes and the tracker mirror are each a decision of their own —
the bootstrap asks, and `DEVELOPMENT-PROCESS.md` §15 says how to turn any of them down afterwards
and what it costs.

## What you get

```
canon/INDEX.md                        generated: every identifier, where it is, what state it is in
canon/spec/README.md                  which file holds which kind of thing, and the rules
canon/spec/BRD.md                     why — the case for the product, in prose; declares nothing
canon/spec/requirements/<AREA>/index.md   what — one register per area, beside its detail files
canon/spec/invariants.md … questions.md   the other registers: one table each, Since and Status columns
canon/spec/CHANGELOG.md               one line per amendment, whatever it amended
canon/spec/changes/README.md          change requests — the unit of post-launch change; ships empty
canon/spec/ID-REGISTRY.md             every identifier family, with its width and owner
canon/spec/MILESTONE-PLAN.md          what this milestone builds; the gates; the phases as P01, P02, …
canon/spec/<AREA>-SPEC.md             the shapes everything inherits
canon/spec/requirements/README.md     the parallel detail track; no detail file ships
canon/process/DEVELOPMENT-PROCESS.md  the loop, the sizing budget, the definition of done
canon/process/SLICE-QUEUE.md          the order — the table is generated
canon/process/MANUAL-REGRESSION.md    by-hand scenarios, kept short by deletion
canon/process/COVERAGE.md             generated ledger; never hand-edited
canon/process/templates/              work order, slice summary, requirement area, requirement detail, test scenarios, change request
canon/process/work-orders/m1/P01/000.md   slice zero, SL-000; work orders and summaries file under <milestone>/<phase>/NNN.md
canon/qa/README.md                    the test scenario track, written from the detail files; also empty
canon/maintenance/                    cleanup + security backlogs, and audits/ — the standing records
canon/decisions/                      ADRs, immutable once accepted
CLAUDE.md                            the agent's map of the repository
.claude/skills/slice-open|slice-close                     the loop
.claude/skills/cleanup|product-docs|security-audit        outside the loop, tuned to your answers
.claude/skills/context-compact                            outside the loop: CLAUDE.md compacted back under its budget
.claude/skills/maintenance                                the four above in order; delivery.md is their shared loop
.claude/skills/manual-test                                outside the loop, tuned to your answers
.claude/skills/requirement-detail|requirement-verify      beside the loop, one phase ahead
.claude/skills/change-request                             after launch: the rows to change, decided, then applied
.claude/skills/process-change                             the process changing itself, landed everywhere and recorded
.claude/skills/test-scenarios                             from the detail file, once the work order is approved
.github/workflows/gate.yml + traceability.yml
scripts/ledger.py + ledger.config.json + test_ledger.py
```

## What is in the kit

| Path | What it is |
|---|---|
| `skills/solo/SKILL.md` | `/canon:solo` — ten-phase interview for one developer plus agents |
| `skills/team/SKILL.md` | `/canon:team` — the same, plus roles, handoffs, WIP limits and parallel-safety |
| `skills/adopt/SKILL.md` | `/canon:adopt` — survey an existing codebase into the process, enforcing nothing on day one |
| `references/00-interview.md` | How to ask: batching, numbering, the stop rule |
| `references/01-scoping.md` | BRD intake and the scoping bank |
| `references/02-security.md` | Domain-keyed security questions — ask only the profile's |
| `references/03-reliability.md` | Availability, RTO/RPO, idempotency, backpressure, scale, observability |
| `references/04-slicing.md` | Slicing criteria, the size budget, dependency ordering, the demo rule |
| `references/05-traceability.md` | The declaration rule, claims, proof, what fails the build |
| `references/06-gate.md` | Gate roles, the `paths-ignore` trap, branch protection |
| `references/07-authoring-style.md` | How the committed documents are written |
| `references/08-team-pipeline.md` | Roles, handoffs, claiming work, CODEOWNERS |
| `references/09-standing-skills.md` | Emitting and tuning `/maintenance` and `/manual-test` — and what not to ask |
| `references/10-requirements.md` | The parallel requirement-detail track and the test-scenario track behind it: the one rule of each, what to configure, and the failure each skill is shaped around |
| `references/11-registers.md` | One kind of thing per file: the narrative BRD, the registers, the one changelog, change requests after launch, and names that sort |
| `references/12-survey.md` | Reading an existing codebase into registers: what to document and what the code already says, the two tiers, provenance, where inherited invariants come from |
| `references/13-adoption.md` | Arriving in a team that has not agreed to it: the enforcement perimeter, the ladder, the annotation harvest, and the three things that decay |
| `references/stacks/` | `generic`, `typescript-node`, `python` |
| `templates/` | Mirrors the generated tree exactly — copy `templates/<path>` to `<path>` |
| `.claude-plugin/plugin.json` | The plugin manifest |

## The thirteen skills

Two run the loop; six run outside it; four run beside it; one changes it. All thirteen are emitted
**tuned to the interview**, not copied generically.

| | |
|---|---|
| `/slice-open [id]` | Asks which slice to start, naming the next in the queue; drafts its work order, opens the branch and the draft PR, stops for approval before any code. **Reads the plan against the requirements for conflict first**, and says so out loud either way |
| `/slice-close` | Drafts the summary from the diff, regenerates the ledger, walks the definition of done item by item |
| `/cleanup` | A behaviour-preserving cleanup of what changed since the last pass, with a backlog of what it deferred and what it settled |
| `/product-docs` | The product documentation regenerated from the code — what the product is today, never a changelog |
| `/security-audit` | A security audit against OWASP/CWE of what changed plus every open backlog row, with a dated report |
| `/context-compact` | The only thing that ever takes a line **out** of `CLAUDE.md`: over the budget in `ledger.config.json`, whole sections move into the documents that own them and a one-line pointer stays behind. No fact is deleted, and `ledger.py check` is what says when to run it |
| `/maintenance` | The four passes above in that order, each on its own branch and merged before the next starts. One shared delivery loop, so how a pass lands is written once |
| `/manual-test` | A **seeded random walk** over a real isolated instance: draw a perturbation and a target, predict from a written oracle, run, classify. Report-only. The seed and the step counter are the whole reproduction |
| `/requirement-detail <id>` | Reads one requirement back in eight lines, interviews in rounds of two to four numbered questions, then writes its detail file — the job, told as stories, and who is turned away. **A conversation, not a delivery** |
| `/requirement-verify <id>` | Per phase gate: is the behaviour that file describes actually there? Four verdicts, and it never edits code, the BRD, or the file's claims. Report-only |
| `/change-request [apply <id>]` | After launch, the only way a register changes: one file with the rows to add, amend or withdraw, read against the invariants for conflict, decided by the owner, then applied with `Since: CR-NNN` on every row and a changelog line. Its applied and built states are derived by the index |
| `/test-scenarios <id>` | Turns one detail file into manual test scenarios done through the product's own screens — the list read back one line each and cut by the test manager before anything is written. A file with a command in a scenario, or nothing but happy paths, fails the check |
| `/process-change` | The process changing itself: one change, read back as the table of files it lands in before anything is edited, recorded in `DEVELOPMENT-PROCESS.md` §15, then checked. It never edits `ledger.py` and never turns a check off to get a green run — **a change that lands in some of its files and not the rest is the failure it exists to prevent** |

The middle six exist because a gate cannot detect the three ways a project rots between slices — a
file nobody has touched since the finding in it was introduced, a suite that is green while nobody
has looked at the product in three weeks, and the agent map growing by a line a slice until the
document every session starts from costs more than it earns. The passes are separate skills so each
can run on its own cadence and be handed to its own owner; `/maintenance` exists for the full run,
where the order carries weight. `/context-compact` is the one with a trigger rather than a cadence:
`DoD-8` adds to `CLAUDE.md` every time a slice establishes a convention, `scripts/ledger.py` warns
when the file passes `context_budget` and fails when it passes the ceiling, and the pass is the
remedy. **A budget with no remedy is a rule people learn to route around.**

`/manual-test`'s oracles are **seeded from the invariants the interview produced**, which is the
reason these belong in bootstrap rather than being adopted at slice forty: at bootstrap they are
written from the specification, and later they are written from memory. `DoD-11` and a drift check
are what keep them true afterwards.

`/requirement-detail`, `/requirement-verify` and `/test-scenarios` exist because a requirement in
a BRD is one line, which is enough to build against
and not enough to test against by hand. They run **parallel to the loop and never inside it** — one
phase ahead of the queue, blocking no merge, consuming no WIP. The detail file settles what a
requirement means; the scenarios file, written from it and from nothing else, is the session a
tester is handed. `references/10-requirements.md` is the reference; `canon/spec/requirements/README.md`
and `canon/qa/README.md` are what ship.

`/process-change` is the thirteenth and it is about the process rather than the product. Everything
above has a switch, `DEVELOPMENT-PROCESS.md` §15 lists what each one costs, and this is what throws
one: it reads the rule and names the failure it was written against, reads the change back as the
**table of files it would land in**, applies it, records it in §15, and runs the check. That table
is the whole point — a change that lands in `ledger.config.json` and not in the process document is
an enforced rule nobody agreed to, and the other way round it is a documented rule the build
ignores, and both are silent. Two fences: it never edits `ledger.py`, because a skill that can
change the tool that checks it can make any process change pass; and it never switches a check off
to get a green run.

## The four mechanisms

Everything else is prose around these.

1. **One declaration rule.** The registry declares identifier *families*, never identifiers. An
   identifier is declared *iff* it is the first cell of a table row, under an `| ID |` header,
   inside its family's declared section. Adding a family is a Markdown row, never a code change.
2. **A ledger that disbelieves its inputs.** A work order claims; a test proves. Only both together
   count, and a claim with no test is downgraded and listed. *A ledger that believes its own work
   orders is a spreadsheet.*
3. **Acceptance criteria become test names.** The only thing keeping a work order honest rather
   than decorative.
4. **Every slice is demonstrated by hand.** Tests prove the system does what it was told to do; the
   demo is where you find out what you told it.

## The tool

`scripts/ledger.py` is stdlib-only Python 3.9+, single file, and the one piece of real code in the
kit.

```bash
python3 scripts/ledger.py          # write COVERAGE.md, INDEX.md and the queue block
python3 scripts/ledger.py check    # verify both, plus every process check — CI runs this
python3 scripts/ledger.py stats    # is the process being followed? reports, never fails
python3 scripts/test_ledger.py     # its own suite
```

`scripts/survey.py` is the second, and only an adopted project gets it. It reads a codebase's
shape out of its git history — churn, co-change, quiet files, who is the only person to have
touched a directory — because that is the one body of evidence an agent has no access to: it is
not in the working tree. Everything it prints is a question for the interview and none of it is a
finding, which the report says out loud.

```bash
python3 scripts/survey.py          # the whole report
python3 scripts/survey.py --json   # the same findings, for a tool rather than a person
python3 scripts/test_survey.py     # its own suite, against real throwaway repositories
```

## Testing the kit itself

```bash
python3 canon/tests/test_templates.py   # from the repository that carries the plugin
```

`templates/scripts/test_ledger.py` tests the *tool*, against a tree it writes itself, and travels
into every project the kit bootstraps. `tests/test_templates.py` tests the *templates*, and stays
here: it copies the shipped tree into a temporary directory, does the mechanical half of phases 6
to 10 — declares the identifiers the traceable families need, answers every placeholder — and runs
`ledger.py check` over the result.

**A green run is the claim that the documents the kit ships agree with each other and with the
tool.** That claim was untested until it was false in four places at once, which is the ordinary
way it goes: a kit whose whole argument is that generated artefacts are verified and claims are
disbelieved had no gate of its own. Run it before every change to `templates/`.

Two values in `scripts/ledger.config.json` are the only stack coupling in the whole kit: the test
file globs, and the annotation pattern. The default pattern matches `[ID]` anywhere in a
test file, which works for vitest, pytest, `go test`, RSpec and JUnit alike. It is matched against
the **whole file**, because a formatter wraps a long test name onto its own line and a per-line scan
would see the call and the name as two unrelated lines.

It fails the build on: an annotation or claim naming a registered family with an undeclared number;
a traceable family that yields nothing; a family or identifier declared twice; a stale generated
artefact; an unknown dependency or a cycle; a work order naming an ADR that does not exist; a
missing or unusable demo section; an unresolved placeholder; a slice marked done with no summary.

And, where the requirement detail track is installed, on a detail file that **quotes its
requirement differently from the specification** — character for character — or one filed in the
wrong area, named for an identifier the specification does not declare, missing a front-matter
field or a template section, `reviewed` with no approver, or recording a verdict outside the four.
The quote check is the load-bearing one: it is what turns an amendment to a register into a failing
build rather than a slow, silent divergence.

It reports without failing: annotations and claims from families the registry does not carry —
either a new document needs a row, or the reference belongs to a document that owns no identifiers,
and **doing the right thing should not be punished with a red gate.**

`stats` is the other half, and it answers a different question. Every check above asks whether the
documents agree with each other, at one moment. `stats` asks whether the process is still being
followed, which is what goes wrong slowly and invisibly: the size tiers nobody recalibrated, the
audit nobody has run since the spring, the detail track that stopped at requirement nine, the
backlog that only grows. It reports the median slice size in each tier and how often the estimate
held, coverage per family, where each parallel track stands, the open rows in each standing
backlog, the age of the last audit, and what the agent map weighs. **It never fails** — an
instrument that can fail a build is a gate wearing a different name. `DEVELOPMENT-PROCESS.md` §11
puts it at every phase gate.

## Improvements over the process this came from

| | Original | Here |
|---|---|---|
| Tooling arrival | Ledger at slice 8, migration lint at slice 18 | **Slice zero ships the gate, the registry and the ledger** before any feature slice |
| ADRs | Recorded by the time the slice closed | **The record must exist before implementation begins**, and the check enforces it |
| The queue | Hand-maintained; sizes and phase labels drifted | **Generated** from work-order front matter by topological sort. One claim site |
| Process scaffolding | Accreted slice by slice | **`SL-000` is a named slice** with its own acceptance criteria and definition of done |
| The demo | A template section, unchecked | **Mandatory and machine-checked** — a runnable block with no placeholder identifiers, or numbered UI steps with a stated expectation |
| Ceremony automation | Specified, never built | **`/slice-open` and `/slice-close` ship** |
| The tracker | The issue *was* the work order, and drifted from the tree | **The file is the work order; the issue mirrors it**, opened at the claim, re-synced at close, and the pull request carries the summary at merge. A claimed slice with no issue fails the check |
| The squash merge | The trailer block lost on every multi-commit branch; issues stayed open | **`/slice-close` hands over `gh pr merge --body-file`** with the close message it saved |
| Requirement conflict | Requirements read for coverage; a plan quietly made an invariant false | **`/slice-open` reads the plan against them for conflict** and reports the result either way (`DoD-12`) |
| The size budget | Tiers in the process document, measured by hand at close, enforced by nothing | **`size` and `code_lines` are front matter and the check holds them together.** The estimate is recorded separately and never corrected, so `stats` can say whether the tiers were ever right |
| Whether the process was working | Unanswerable without reading sixty files | **`ledger.py stats`** — sizing, coverage, both tracks, both backlogs, the age of the last audit, in one screen |
| A bootstrap that ran out of session | Start the ten-phase interview again from question one | **`.canon-interview.md`**, appended after every phase, found and offered at phase 0, deleted at the commit |
| The specification | One document that was narrative, tables and its own history at once; requirements edited in place for years | **One kind of thing per file**: a narrative BRD that declares nothing, a register per kind with `Since` and `Status` columns, one changelog held to a line per row, a generated index, and after launch a change request per change. A cell carrying history, a dangling reference or an unapplied accepted request fails the check |
| Naming | Phase letters chosen to dodge family collisions; slice ids that encoded a phase the slice no longer ran in; `SL-P3b` | **Phases are `P01`, `P02`; slices are a global `SL-NNN`** named for the file, and every family's width is fixed |
| Hand testing | A one-line requirement, and a tester guessing the actors and the boundaries | **One detail file per requirement**, quoting it verbatim under a check, with `/requirement-verify` at each phase gate |
| Test sessions | A detail file read at a keyboard, and two testers covering two different things | **One scenarios file per requirement**, written from the detail file only, done through the product's screens — a command in a scenario fails the build |

## Adapting it

- **A different stack** — copy `references/stacks/generic.md` to a new annex, fill the gate-role
  table, and set the two ledger config values.
- **A different tracker** — the process is repository-first by design; the tracker holds narrative
  and linkage. GitHub ships: an issue per claimed slice whose body is the work order file, the
  summary as a comment, closed by the trailer. For another tool, keep that shape and swap the `gh`
  calls in `slice-open` and `slice-close`; `tracker` in the ledger config is what the check and
  the queue read. Set it to `""` for none.
- **A different identifier scheme** — change the registry rows. Nothing in the tool knows a prefix.
- **Identifiers that predate the width rule** — an adopting project has them, cited and satisfied, and
  renumbering is the thing the registry forbids. Name each one in `legacy_identifiers`. The list can
  only shrink; a *new* identifier that would need an entry should have taken a fresh number.
- **A queue that is prose** — a milestone plan whose cells carry the reasoning rather than a title.
  Set `queue_out` to `""` and no block is written or demanded, the way `index_out` and `state_out`
  already behave.
- **A different folder name** — answer phase 0's question. The templates say `canon/` and the emit
  step rewrites every `canon/` path to the name you chose; the tool reads every path from its
  config, so nothing else knows the name. Renaming later is a `git mv` plus the same substitution.
- **A skill name that is already taken** — phase 0 checks the thirteen names against the project's
  and your own `.claude/skills/` and `.claude/commands/`, and asks once if any collide: prefix
  every kit skill with `canon-`, or name the colliding ones yourself. Nothing of yours is
  overwritten or renamed, and the emit step rewrites the cross-references the same way it
  rewrites the folder.
- **No requirement detail track** — set `requirements.dir` to `""`. Every check it adds goes quiet
  and `COVERAGE.md` loses one section; nothing else changes.
- **A surface worth drift-checking** — drop an executable into
  `.claude/skills/manual-test/drift.d/`. It runs before every walk; a non-zero exit means an oracle
  names something that no longer exists.
- **Less of it** — every part has a switch and `canon/process/DEVELOPMENT-PROCESS.md` §15 is the
  list: what each one turns off, and what it costs. Three things have no switch, and it says why.
  `/process-change` is what throws one and lands it in every file it touches.
- **No Python** — the tool is a single stdlib-only file with no dependencies; porting it is an afternoon. Keep the
  declaration rule and the status derivation exactly, because those are the parts that are load
  bearing.
