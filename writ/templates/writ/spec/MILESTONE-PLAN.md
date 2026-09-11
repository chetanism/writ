# Milestone plan — <M1, the milestone's name>

> **Status:** active, for the milestone `milestones.md` marks `active`.
> **Role:** what *structure* this milestone builds and the gates that say it is finished. **Tables,
> and two paragraphs.** Risks are `risks.md` with this milestone as their scope; open questions are
> `questions.md`; every departure from this plan is a line in `CHANGELOG.md` with the affected
> table here amended in the same change. None of those lives in this file.
> **Precedence:** the registers > `BRD.md` > this document > `process/SLICE-QUEUE.md`.
> **Owner:** <the slicer>. Scope is the specification owner's and arrives as a change request, not
> as an edit here.
>
> Delete this blockquote.

## 1. What this milestone is for

<Two paragraphs at most. What becomes possible that was not, and what question it answers. Cite
the objective and the risk it retires by identifier.>

## 2. Gates

> A gate is a demonstrable property of the finished milestone, not a task. Each one is checked at
> the end, by hand, against a named demo. A gate may close twice: provisionally against a
> stand-in, marked `◐`, and finally against the real thing. **A `◐` is not milestone-complete.**

| ID | Gate | Demonstrated by | Since | Status |
|---|---|---|---|---|
| G-01 | <The process runs: gate green in CI, registry declaring, ledger generated, one requirement carried end to end> | <Slice zero's demo, re-run> | v0.1 | open |

## 3. Phases

> Ordinals, in dependency order, each with the exit criterion the phase gate reads. The code is
> the order, the directory under `process/work-orders/<milestone>/`, and the value of a work order's
> `phase:`; `scripts/ledger.config.json` carries the same list. Inserting a phase renumbers the
> ones after it — a script over front matter and directory names — and prose refers to a phase by
> name so that nothing goes stale.

| Code | Phase | Establishes | Exit criterion |
|---|---|---|---|
| P01 | <Foundation> | <The process, the workspace, the tenant boundary, the thin spine> | <A journey runs end to end at its thinnest, and the queue is sized against the date> |
| P02 | <Access> | <…> | <…> |

## 4. Foundation specs

| Spec | Fixes | Slices it shapes |
|---|---|---|
| `<AREA>-SPEC.md` | <…> | <…> |

## 5. What this milestone deliberately does not build

| Not here | Lands at |
|---|---|
| <…> | <M2, or OOS-NN> |

## 6. External tracks

> Anything with a lead time that is not code, cited from `dependencies.md`. One row each, with what
> it unblocks, so that when a track lands the resequencing is a lookup rather than a re-analysis.
> The mark is what a work order's `dep:` carries.

| Mark | Needs | Typical wait | Unblocks |
|:--:|---|---|---|
| — | Nothing but a laptop | none | everything not listed below |
| <meta> | <DEP-01> | <1–3 weeks> | <G-NN's final close> |
