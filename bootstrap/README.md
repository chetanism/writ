# `bootstrap/` — an agent-first development process, ready to copy

A kit for setting up a new project's development process: a business requirements document, an
identifier registry, foundation specs, a dependency-ordered slice queue, work-order and
slice-summary templates, a CI gate, and a traceability tool that refuses to take a work order's
word for anything.

It was extracted from a real project and generalised. **The core is stack-agnostic**; the specifics
that project proved out live in a stack annex you load one of.

> This directory is inert inside its host repository. See `CLAUDE.md` here.

## Using it

Copy the directory into the new project and tell Claude Code to run it:

```bash
cp -R /path/to/bootstrap ~/projects/new-thing/bootstrap
cd ~/projects/new-thing
git init                       # if it is not a repository yet

# optional: make the skills discoverable as /bootstrap-solo and /bootstrap-team
mkdir -p .claude/skills
cp -R bootstrap/skills/* .claude/skills/
```

Then, in Claude Code:

- **One person building it** → `/bootstrap-solo`, or *"read `bootstrap/skills/bootstrap-solo/SKILL.md`
  and follow it"*.
- **More than one person** → `/bootstrap-team`. It designs the roles and handoffs, and retrofitting
  those is harder than choosing correctly at the start.

Have your BRD to hand — or do not. **Two paragraphs is a valid input**; the interview writes the
rest with you. Expect two to three rounds of questions if you arrive with a finished specification,
and six to ten if you arrive with an idea.

It finishes by committing the generated tree on `dev`. Add a remote and branch protection then, if
there is none yet; `/slice-open` works without one but the draft pull request and the CI gate wait.

Keep `bootstrap/` in place until the first slice has been through the loop — the skills read
`bootstrap/references/` by path, wherever their `SKILL.md` was copied. Then delete it: everything it
produced is the project's own, and a kit left lying around gets edited instead of the documents it
generated.

## What you get

```
docs/spec/BRD.md                     what and why
docs/spec/ID-REGISTRY.md             every identifier family
docs/spec/MILESTONE-PLAN.md          what this milestone builds; the gates; the amendment log
docs/spec/<AREA>-SPEC.md             the shapes everything inherits
docs/process/DEVELOPMENT-PROCESS.md  the loop, the sizing budget, the definition of done
docs/process/SLICE-QUEUE.md          the order — the table is generated
docs/process/MANUAL-REGRESSION.md    by-hand scenarios, kept short by deletion
docs/process/COVERAGE.md             generated ledger; never hand-edited
docs/process/requirements/README.md  the parallel detail track; the directory ships empty
docs/process/templates/              work order, slice summary, requirement detail
docs/process/work-orders/000.md      slice zero, pre-filled
docs/process/maintenance/            cleanup + security backlogs, and audits/
docs/decisions/                      ADRs, immutable once accepted
CLAUDE.md                            the agent's map of the repository
.claude/skills/slice-open|slice-close                     the loop
.claude/skills/maintenance|manual-test                    outside the loop, tuned to your answers
.claude/skills/requirement-detail|requirement-verify      beside the loop, one phase ahead
.github/workflows/gate.yml + traceability.yml
scripts/ledger.py + ledger.config.json + test_ledger.py
```

## What is in the kit

| Path | What it is |
|---|---|
| `skills/bootstrap-solo/SKILL.md` | Ten-phase interview for one developer plus agents |
| `skills/bootstrap-team/SKILL.md` | The same, plus roles, handoffs, WIP limits and parallel-safety |
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
| `references/10-requirements.md` | The parallel requirement-detail track: the one rule, what to configure, and the failure each skill is shaped around |
| `references/stacks/` | `generic`, `typescript-node`, `python` |
| `templates/` | Mirrors the generated tree exactly — copy `templates/<path>` to `<path>` |

## The six skills

Two run the loop; two run outside it; two run beside it. All six are emitted **tuned to the
interview**, not copied generically.

| | |
|---|---|
| `/slice-open <id>` | Drafts the work order from the queue, opens the branch and the draft PR, stops for approval before any code. **Reads the plan against the requirements for conflict first**, and says so out loud either way |
| `/slice-close` | Drafts the summary from the diff, regenerates the ledger, walks the definition of done item by item |
| `/maintenance` | Three standing passes — a behaviour-preserving cleanup, the documentation regenerated from the code, a security audit against OWASP/CWE. Each on its own branch, merged before the next starts. `/maintenance cleanup\|docs\|security` runs one |
| `/manual-test` | A **seeded random walk** over a real isolated instance: draw a perturbation and a target, predict from a written oracle, run, classify. Report-only. The seed and the step counter are the whole reproduction |
| `/requirement-detail <id>` | Reads one requirement back in eight lines, interviews in rounds of two to four numbered questions, then writes its detail file. **A conversation, not a delivery** |
| `/requirement-verify <id>` | Per phase gate: is the behaviour that file describes actually there? Four verdicts, and it never edits code, the BRD, or the file's claims. Report-only |

The middle two exist because a gate cannot detect the two ways a project rots between slices — a
file nobody has touched since the finding in it was introduced, and a suite that is green while
nobody has looked at the product in three weeks.

`/manual-test`'s oracles are **seeded from the invariants the interview produced**, which is the
reason these belong in bootstrap rather than being adopted at slice forty: at bootstrap they are
written from the specification, and later they are written from memory. `DoD-11` and a drift check
are what keep them true afterwards.

The last two exist because a requirement in a BRD is one line, which is enough to build against and
not enough to test against by hand. They run **parallel to the loop and never inside it** — one
phase ahead of the queue, blocking no merge, consuming no WIP. `references/10-requirements.md` is
the reference; `docs/process/requirements/README.md` is what ships.

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
python3 scripts/ledger.py          # write COVERAGE.md and the queue block
python3 scripts/ledger.py check    # verify both, plus every process check — CI runs this
python3 scripts/test_ledger.py     # its own suite
```

Two values in `scripts/ledger.config.json` are the only stack coupling in the whole kit: the test
file globs, and the annotation pattern. The default pattern matches `[ID]` anywhere on a line of a
test file, which works for vitest, pytest, `go test`, RSpec and JUnit alike.

It fails the build on: an annotation or claim naming a registered family with an undeclared number;
a traceable family that yields nothing; a family or identifier declared twice; a stale generated
artefact; an unknown dependency or a cycle; a work order naming an ADR that does not exist; a
missing or unusable demo section; an unresolved placeholder; a slice marked done with no summary.

And, where the requirement detail track is installed, on a detail file that **quotes its
requirement differently from the specification** — character for character — or one filed in the
wrong area, named for an identifier the specification does not declare, missing a front-matter
field or a template section, `reviewed` with no approver, or recording a verdict outside the four.
The quote check is the load-bearing one: it is what turns an amendment to the BRD into a failing
build rather than a slow, silent divergence.

It reports without failing: annotations and claims from families the registry does not carry —
either a new document needs a row, or the reference belongs to a document that owns no identifiers,
and **doing the right thing should not be punished with a red gate.**

## Improvements over the process this came from

| | Original | Here |
|---|---|---|
| Tooling arrival | Ledger at slice 8, migration lint at slice 18 | **Slice zero ships the gate, the registry and the ledger** before any feature slice |
| ADRs | Recorded by the time the slice closed | **The record must exist before implementation begins**, and the check enforces it |
| The queue | Hand-maintained; sizes and phase labels drifted | **Generated** from work-order front matter by topological sort. One claim site |
| Process scaffolding | Accreted slice by slice | **`SL-000` is a named slice** with its own acceptance criteria and definition of done |
| The demo | A template section, unchecked | **Mandatory and machine-checked** — a runnable block with no placeholder identifiers, or numbered UI steps with a stated expectation |
| Ceremony automation | Specified, never built | **`/slice-open` and `/slice-close` ship** |
| Requirement conflict | Requirements read for coverage; a plan quietly made an invariant false | **`/slice-open` reads the plan against them for conflict** and reports the result either way (`DoD-12`) |
| Hand testing | A one-line requirement, and a tester guessing the actors and the boundaries | **One detail file per requirement**, quoting it verbatim under a check, with `/requirement-verify` at each phase gate |

## Adapting it

- **A different stack** — copy `references/stacks/generic.md` to a new annex, fill the gate-role
  table, and set the two ledger config values.
- **A different tracker** — the process is repository-first by design; the tracker holds narrative
  and linkage. Swap the `gh` calls in `slice-open`.
- **A different identifier scheme** — change the registry rows. Nothing in the tool knows a prefix.
- **No requirement detail track** — set `requirements.dir` to `""`. Every check it adds goes quiet
  and `COVERAGE.md` loses one section; nothing else changes.
- **A surface worth drift-checking** — drop an executable into
  `.claude/skills/manual-test/drift.d/`. It runs before every walk; a non-zero exit means an oracle
  names something that no longer exists.
- **No Python** — the tool is ~600 lines with no dependencies; porting it is an afternoon. Keep the
  declaration rule and the status derivation exactly, because those are the parts that are load
  bearing.
