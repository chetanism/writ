# Registers, the changelog, and names that sort

Governs how phase 6 writes the specification set and how phase 7 names phases and slices. Read it
before phase 6. `references/05-traceability.md` is the declaration rule and the tool; this is the
shape of the documents the tool reads, and why.

## The failure this exists to prevent

By the second milestone, every specification written as one document has become three: the
narrative it started as, a set of tables inside it, and its own history — inline `(new — v3.0)`
markers, `Amended 2026-…` notes in cells, questions closed by strikethrough with a paragraph of
reasoning, an amendment table whose rows are essays. The milestone plan grows a risk commentary and
closed questions; the queue grows the reasoning behind its order and a second copy of the amendment
index. A reader cannot find the current state of anything without reading its past, and a team
that cannot find the current state stops reading and starts asking.

## One kind of thing per file

| Kind | Holds | Emitted as |
|---|---|---|
| **Narrative** | The case for the product. No identifier tables | `spec/BRD.md`, `spec/glossary.md` |
| **Registers** | One table of identified rows each, short preamble, `Since` and `Status` columns | `spec/requirements/<AREA>/index.md`, `invariants.md`, `compliance.md`, `strategic-decisions.md`, `personas.md`, `milestones.md`, `dependencies.md`, `risks.md`, `assumptions.md`, `out-of-scope.md`, `questions.md` |
| **Plans** | Tables only | `spec/MILESTONE-PLAN.md`, `process/SLICE-QUEUE.md` |
| **History** | One line per amendment, dated | `spec/CHANGELOG.md` |
| **Elaboration** | One file per identifier | detail files, change requests, ADRs, work orders, summaries |

`spec/README.md` ships saying this, and `INDEX.md` is generated over all of it so that a reader
opens one file to find any identifier and its state.

**Status is a column.** A withdrawn requirement keeps its row and number and says `withdrawn`;
it leaves the coverage ledger and can still be cited. A closed question says `closed` and names
what closed it. **History is never in a cell**: `Since` names the version, amendment or change
request that introduced a row; the changelog says what changed; an ADR or a slice summary says
why. The check refuses a cell carrying history, a register with two ID tables, a narrative with
one, an unresolved reference, an empty `Since`, and a changelog line over the length budget.

**One family per kind.** `Q-*` for every open question with a `Scope` column, wherever it arose.
`RSK-*` for every risk, product or delivery. `X-*` for every amendment in the one changelog. The
interview does not mint `MQ`, `OQ`, `DR` or a second amendment family because a second document
appeared.

## Names that sort and never collide

- **Phases are ordinals with names**: `P01 Foundation`, `P02 Access`. The code is the order, the
  directory under `work-orders/<milestone>/`, and the value of `phase:`. A phase is referenced only
  from front matter and directory names, both mechanical to renumber, so inserting one is a script;
  prose refers to a phase by its name. Letters collided with families — `M` with milestones, `G`
  with gates, `D` with decisions — and the workaround was letters that meant nothing.
- **Slices are a global zero-padded number**: `SL-042`, filed at `work-orders/m1/P02/042.md`. The
  id encodes nothing about the phase, so a slice that runs late does not carry a wrong letter and a
  split mints `SL-083` and `SL-084` rather than `SL-042b`. The queue shows the phase beside it.
- **Every family's pattern fixes a width**, stated in `ID-REGISTRY.md`. Three digits for
  requirements, questions and amendments; four for ADRs; two for gates. The check refuses an
  identifier outside its width or carrying a suffix.

## After launch: the registers are the store

The BRD is authored once by people arguing a case; requirements arrive forever. So the narrative
freezes at launch and is re-cut only at a milestone boundary, and every change to the registers
arrives as a **change request** — one file under `spec/changes/`, with the rows it adds, amends or
withdraws, the conflict read against the invariants done at proposal time, what it makes stale,
and who decided. Accepting one applies it: rows land with `Since: CR-NNN`, one changelog line, the
index regenerated. The request's own state is derived — *applied* when its rows exist, *built* when
its identifiers read satisfied — so "did January's change ship" is a lookup. `/change-request` is
the detail interview pointed at a change, and the kit's eleventh skill.

Priorities tied to dates end at launch. A register row carries a `Target` milestone instead, and
the next milestone plan is read from the rows aimed at it.

## What phase 6 writes, in order

1. `spec/BRD.md` — the narrative, with no identifier table in it.
2. The registers, one file each, from the interview's answers. Requirement areas as
   `spec/requirements/<AREA>/index.md` from `process/templates/requirement-area.md`. Every row
   carries `Since: v0.1` and `Status: active`, and a `Target` where the family is aimed at a
   milestone.
3. `spec/milestones.md`, with the first marked `active`.
4. `spec/ID-REGISTRY.md` — a row per family, patterns with widths, directory owners for the
   requirement areas, change requests and decisions.
5. `spec/MILESTONE-PLAN.md` — purpose, gates, phases as ordinals, foundation specs, not built,
   external tracks. Nothing else.
6. `spec/<AREA>-SPEC.md` per inherited shape.
7. `spec/CHANGELOG.md` with its one seed row, `X-001`, touching `v0.1`.

Then `registers` and `narrative` in `scripts/ledger.config.json` list what was written, so the
check holds them to their kind from the first commit.

## What to leave alone

- **Do not seed `spec/changes/`.** A README and nothing else; the track starts at launch.
- **Do not put reasoning in a register row or a changelog line.** The check bounds the line, and a
  row that needs a paragraph is an ADR or a question.
- **Do not cite an identifier that does not exist**, even as an example. The reference check reads
  prose and inline code; fenced blocks and blockquotes are notation. The templates keep their
  examples there, and so must anything the interview writes.
