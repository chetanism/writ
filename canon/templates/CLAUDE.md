# CLAUDE.md

Guidance for coding agents working in this repository. **These instructions override default
behaviour.**

## What belongs in this file

This file is read at the start of every session, so every line in it is paid for on every task.
**The test for a line is whether an agent would write the wrong code without it** on a task that
never opens the document it came from. If it is reference — a procedure, a rationale, an
enumeration of cases, an example — it belongs in `canon/` or in the skill that needs it, and here
as a pointer of one line.

- **One line per rule, and the new one replaces what it supersedes.** A superseded rule left
  standing beside its replacement is read as a live one.
- **Never restate what `canon/` says.** Point at it. Two wordings of one rule is two rules, found
  the day they disagree.
- **Nothing dated, nothing generated, nothing that changes every slice** — except *Project state*.
- `python3 scripts/ledger.py check` warns when this file is over the budget in
  `scripts/ledger.config.json` and fails when it is over the ceiling. **`/context-compact` is the
  remedy** — it moves whole sections into the documents that own them and leaves the pointer
  behind. Deleting a fact is not the remedy.

## Project state

<One paragraph: what this is, and what exists today. Update it every slice — this file is read at
the start of every session, which makes it the highest-leverage document here.>

## Canonical specification

The registers under `canon/spec/` are the source of truth for requirements, invariants and
constraints — one table each, `canon/spec/README.md` says which file holds which — and
`canon/spec/BRD.md` is the case for the product in prose. `canon/INDEX.md` lists every identifier
with where it is declared and what state it is in; **open it first**. Requirement identifiers are
stable — reference them, never renumber them, and never cite one the index does not list.

## Document map

| Document | Role |
|---|---|
| `canon/INDEX.md` | **Generated.** Every identifier, where it is declared, what state it is in. Open first |
| `canon/spec/BRD.md` | The case for the product, in prose. Declares nothing; frozen at launch |
| `canon/spec/requirements/<AREA>/index.md` and the other registers | **Source of truth.** One table of identified rows each, with `Since` and `Status` |
| `canon/spec/CHANGELOG.md` | One line per amendment, whatever it amended. The only history outside git |
| `canon/spec/changes/` | Change requests — the unit of post-launch change to the registers |
| `canon/spec/ID-REGISTRY.md` | **Every identifier family** — owner, declaring section, traceability |
| `canon/spec/MILESTONE-PLAN.md` | What structure this milestone builds, the gates, the phases. Tables only |
| `canon/spec/<AREA>-SPEC.md` | Foundation specs — the shapes everything inherits |
| `canon/process/DEVELOPMENT-PROCESS.md` | **How we work.** The slice loop, the definition of done, traceability |
| `canon/process/SLICE-QUEUE.md` | **In what order.** The queue table is generated from work-order front matter |
| `canon/process/MANUAL-REGRESSION.md` | Standing by-hand scenarios, promoted from demos. Kept short by deletion |
| `canon/process/work-orders/<milestone>/<phase>/` | One per slice. Opened before any code; it is the pull request description |
| `canon/process/slices/<milestone>/<phase>/` | One committed summary per completed slice, filed beside its work order |
| `canon/process/COVERAGE.md` | **Generated** requirement ledger. Never hand-edited |
| `canon/spec/requirements/<area>/` · `canon/qa/scenarios/<area>/` | One file per requirement — the specification elaborated, never extended — and the manual test scenarios written from it, done through the product's screens and never a command. **Never read during a slice** — `/requirement-detail`, `/requirement-verify`, `/test-scenarios` |
| `canon/decisions/` | ADRs — why one option was chosen over another. Immutable once accepted |
| `canon/maintenance/` | The standing records: what a cleanup pass settled, and the live security backlog. The dated reports in `audits/` are history |

**Precedence:** the registers > `BRD.md` > `MILESTONE-PLAN.md` > `SLICE-QUEUE.md` > everything else.

## Identifier convention

Every identifier is prefixed, and every family is declared in `canon/spec/ID-REGISTRY.md` with its
owner document, declaring section and traceability.

> **An identifier is declared iff it is the first cell of a table row, under an `| ID |` header,
> inside its declared section.** Everything else is a reference.

**Add a family by adding a registry row — never by teaching a parser a new prefix.**

## How to work here

Work proceeds in **slices**, not requirement by requirement. A slice is the thinnest change that
alters what the system can do end to end and can be exercised by hand. Before writing code:

1. There must be an agreed work order with acceptance criteria.
2. **Read the plan against the requirements for conflict, not only for coverage** (`DoD-12`). The
   question is whether the plan would make one *false*, and the ones it will make false are the
   `INV-*` invariants governing the areas the slice changes — an invariant is a shape, so it belongs
   to no requirement area you would think to search. **A conflict is the slicer's to resolve: name
   the requirement, the part of the plan, and the two answers, and stop.** Never take the reading
   that makes the plan work, and say *no conflicts* out loud when there are none.
3. Propose a **file-level plan** and wait for it to be read. The human reads the plan, not just the
   diff.
4. Acceptance criteria become test names, annotated with identifiers: `it('[<ID>] …')`.
5. Keep the slice inside the size budget in `DEVELOPMENT-PROCESS.md` §2.1 — **added code lines**,
   outside tests, comments, blanks and generated files. If it will not fit, say so and propose a
   split rather than exceeding it.
6. **Any decision with a credible rejected alternative gets an ADR before implementation begins**,
   not before the slice closes.
7. Update this file when structure, packages or conventions change — one line, and replace the
   line it supersedes rather than adding beside it (*What belongs in this file*).
8. **The slice summary is written in the slice's own commit**, before the pull request opens.

## Binding invariants

<From `canon/spec/invariants.md`. Violating one is a defect, not a style preference. Name the layer
that enforces each.>

## Commands

| Command | Does |
|---|---|
| <Gate command> | The full local gate — what CI runs |
| <Unit test command> | Unit tests, held to <N> seconds |
| <Integration test command> | Adds integration tests; needs <Stack-up command> |
| `python3 scripts/ledger.py` | Regenerates `COVERAGE.md`, `INDEX.md` and the queue block |
| `python3 scripts/ledger.py check` | Fails if either is stale, or any process check fails; warns when this file is over its budget. CI runs this |
| `python3 scripts/ledger.py stats` | Is the process being followed? Sizing, coverage, the tracks, the backlogs. Reports, never fails — read it at each phase gate |
| `python3 scripts/test_ledger.py` | The traceability tool's own suite |

## Skills

| | |
|---|---|
| `/slice-open [id]` | Step 2 of the loop — asks which slice to start, naming the next in the queue, then drafts the work order, opens its issue, the branch and the draft pull request |
| `/slice-close` | Step 7 — drafts the summary from the diff, regenerates the ledger, walks the definition of done, puts the summary on the pull request and the issue, and hands over the merge command that keeps the trailers |
| `/cleanup` | Outside the loop — a behaviour-preserving cleanup of what changed since the last pass |
| `/product-docs` | Outside the loop — the product documentation under `docs/documentation/` regenerated from the code |
| `/security-audit` | Outside the loop — a security audit against OWASP and CWE, with a dated report and the backlog reconciled |
| `/maintenance` | All four passes in that order, each merged before the next. They share `.claude/skills/maintenance/delivery.md` for how a pass lands |
| `/manual-test` | Outside the loop — a seeded walk over an isolated instance. **Report-only; it never edits this repository** |
| `/context-compact` | Outside the loop — moves sections out of this file into the documents that own them when it is over budget, leaving a pointer |
| `/requirement-detail <id>` | The parallel track — reads one requirement back in eight lines, interviews, then writes its detail file |
| `/requirement-verify <id>` | Per phase gate — checks one satisfied requirement against the product. **Report-only** |
| `/change-request [apply <id>]` | After launch — raises one change to the registers as rows, reads it for conflict, stops for the owner; applies an accepted one |
| `/test-scenarios <id>` | After the detail file is reviewed, ideally once the claiming work order is approved — reads the scenario list back, then writes the manual test scenarios from one requirement's detail file |

## Conventions set here and binding afterwards

> One line per convention, added by the slice that establishes it, replacing whatever it
> supersedes. This section is the reason this file is worth reading — it is where the reasoning
> lives that the code cannot carry. When a convention needs an example or a counter-example to be
> understood, the line stays here and the example goes in the document it points at.

- **Test files sit beside their source.** <Unit test suffix> is a unit test; <Integration test
  suffix> needs a live dependency and runs only under <Integration test command>.
- **Every test name starts with its requirement identifier** — `it('[<ID>] …')`.
- **Never put an annotation-shaped string in a test file that is not a real test.** The collector
  scans them for evidence.
- **A generated artefact is committed, verified byte-for-byte in CI, and excluded from the
  formatter.** A formatter and a generator writing the same file disagree about it forever.
- **No pre-commit hooks, by decision.** The gate is CI. A hook that re-runs the same checks more
  slowly is how people learn to pass `--no-verify`.
- **Every demo-facing command takes `--json` and prints exactly one object**, so a demo script can
  capture an identifier instead of asking the reader to paste one.

## Talking to me

> **Emitted only if the directive mode was chosen at bootstrap.** If the answer was the usual
> voice, delete this whole section — a half-applied interaction rule is worse than none, because
> the reader cannot tell which replies were meant to follow it. Delete this blockquote either way.

One reader, eyeballing a terminal. **Terseness is a correctness requirement — never spend 100
tokens where 50 will do.** Final output only: no preamble, recap, closing summary, restatement of
the question, or narration of what you are about to do.

- **Bullets and fragments. Not prose, not sentences.**
- **Group under `IMPORTANT` / `NOTE` / `FYI` / `ASK`** — only the groups a reply needs.
- **Tag by direction; get the verb right.** Past tense = done by me (`[NOTED]` `[FIXED]` `[ADDED]`
  `[DROPPED]`). Imperative = yours to do (`[NOTE]` `[FIX]` `[CHECK]` `[DECIDE]`). Never one for the
  other.
- **Number every ask** — `[ASK 1]`, `[ASK 2]` — restarting each reply, so the answer is "2. yes".
  One question still gets a number.
- **One line per fact.** A reason earns its line only if omitting it misleads.
- **File refs as `path:line`.** Never quote a diff back or re-show what was just written.
- **Conclusion first; rationale only when asked.** Never web-search or write a file unasked; ask for
  a missing detail rather than assuming it.
- **A recommendation names what was read.** A library, tool, version or convention proposed without
  checking what this repository and its neighbours already use is a prior dressed as a finding —
  label it unverified, or go and look.
- **A file-level plan is paths plus one line each**, with the `DEVELOPMENT-PROCESS.md` §2.1 budget
  number and whether it fits. Code only where the shape is non-obvious.

**Documents obey this too.** An ADR, spec or work order keeps its template, but every line earns its
place: a document is read far more often than written.

## Git

- **Attribution:** <No agent attribution anywhere in git or the tracker — no co-author trailer, no
  session link | The default co-author trailer is kept>.
- **Never commit to `dev` or `main` directly.** Branch — `slice/<NNN>-<slug>`, `req/<id>`,
  `qa/<id>`, `cr/<id>`, `docs/<slug>` — push, open a pull request into `dev`, squash merge.
- Commit with the trailer block in `DEVELOPMENT-PROCESS.md` §6.3.
