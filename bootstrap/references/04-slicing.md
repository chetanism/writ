# Slicing, sizing and ordering

## The definition

> **A slice is the thinnest change that alters what the system can do, end to end, and can be
> exercised by hand.**

If it cannot be demonstrated, it is a task — fold it into the slice it serves. If it exceeds the
top size tier, it is two slices that have not been separated yet.

Requirements and slices are **many-to-many** and serve different purposes. Requirements are the
coverage ledger: the checklist that decides whether a milestone is done. Slices are the work queue:
the order in which things actually get built. Do not try to make them line up.

## Ask for the slicing criteria before cutting anything

Put this to the user as a menu, multi-select. The answer changes every boundary:

| Criterion | A slice is | Suits |
|---|---|---|
| **By capability** | One thing a user can now do that they could not before | Most projects. The default |
| **By layer, bottom-up** | The data layer, then the contract, then the surface | Projects whose foundation is the risk |
| **By user journey** | One complete path through the product | Products whose value is the flow |
| **By risk, riskiest first** | The thing most likely to invalidate the plan | Anything with an unproven core assumption |
| **By integration** | One external system, wired end to end | Integration-heavy work |
| **By screen** | One view, with everything behind it | UI-led work with a settled backend |

Then ask the follow-ups the answer implies: is a slice allowed to ship behind a flag; must every
slice be demonstrable to a non-developer; is a slice allowed to leave a stub.

## Sizing

The constraint that matters is not lines. It is: **a diff one person can read carefully in under
thirty minutes.** This is a comprehension budget, not a productivity target — the limit exists
precisely because agents can produce far more than that per session.

**Measure added code lines**: lines added outside test files, comments, blank lines, and generated
artefacts. Record the total diff beside it, but do not govern by it.

| Size | Added code lines | Shape |
|---|---|---|
| **S** | under 150 | One module, one concept |
| **M** | 150–400 | The default. One capability across two or three components |
| **L** | over 400 | Needs a justification in the work order *and* a stated reason it cannot be split |

Why the exclusions: tests are commonly 40% of a slice and read differently from logic; comments and
blanks are another 20%, and charging a slice for explaining itself is an incentive pointed exactly
the wrong way; generated artefacts are output, not input.

**Recalibrate from measurement, not intuition.** After ten merged slices, tabulate diff, tests,
comments, and code for each, and move the tiers to fit. A rule broken five times in six is not a
rule anybody is following — it is a measurement that does not fit what is being measured.

Every work order states **both numbers**: *"M — 268 code lines, 709 in the diff."* Queue estimates
are estimates; reconcile them at close, and when the estimate is wrong three times running, the
pattern is the finding rather than the individual slice.

## Ordering

Order by **dependency**, not by preference. Put each slice's prerequisites in `depends_on` and let
the queue be generated — a hand-maintained order is a second copy of the dependency graph, and it
drifts the first week.

Rules that repay themselves:

- **Numbered at creation, positioned by need.** Never renumber a slice: its id is in test names,
  commit trailers and the ledger. A slice created sixteenth may run sixth, and the queue says so.
- **The riskiest assumption goes early.** The point of a milestone gate is to find out whether the
  plan is wrong while changing it is still cheap.
- **A slice that gates every later slice runs before them, even if it is dull.** The isolation
  suite, the migration checker, the ledger.
- **Group into phases with a letter and an exit criterion.** Choose letters that do not collide
  with your identifier families — if milestones are `M0..M5`, messaging cannot be phase `M`.
- **Mark external blockers in a `dep:` field.** Then keep a table of what each external unlock
  releases, so that when a track lands the resequencing is a lookup rather than a re-analysis.

## Read the plan against the requirements, not only for coverage

**`DoD-12`, and the step that gets skipped.** Reading the requirements a slice claims is not the
same as reading the plan *against* them. The first asks which requirements this slice advances —
the front matter already answers that. The second asks whether the plan would make one **false**,
and that is a different question with a different answer set.

The ones a plan makes false are almost never the ones it claims. They are the **invariants
governing the areas the slice changes** — and an invariant is a shape rather than a capability, so
it sits in no requirement area a slicer would think to search. It may well read `○` in the ledger
with no slice claiming it. That is not evidence it does not apply; it is the normal state of a
constraint.

The shape of the failure, from a real project: a decision record stored an amount of money in one
country's minor units with no currency recorded anywhere — against a P0 invariant saying
country-specific facts are configuration, never assumptions baked into the product. Every
requirement the slice claimed had been read carefully. None of them pointed at it. The slicer
caught it, which is the argument for the rule being *the slicer's*.

So, written into `/slice-open` as its own numbered step, before the work order is drafted:

- List the claims **plus every invariant governing the areas the slice changes**.
- Ask of each: *would this plan make it false?* — not *does the plan mention it*. A plan that never
  mentions a constraint is the normal way one gets broken.
- **A conflict is escalated, never resolved by the drafter.** Name the requirement, name the part
  of the plan, name the two answers, stop. The person who wrote the plan is the last one who should
  choose between it and a requirement that inconveniences it.
- **Say *no conflicts found* out loud.** A silent check reads exactly like one that never happened
  — which is why this is a reported line rather than a habit.

## Slice zero

The first slice is the process itself, and it is a real slice with a real definition of done:
the gate runs, the registry declares its families, the ledger generates and is committed, the
templates are in place, and **one throwaway requirement is carried end to end** — declared,
claimed, annotated in a test, and shown green in the ledger.

That last part is the point. It demonstrates the machinery rather than asserting it, and it is why
`docs/process/work-orders/000.md` ships pre-filled.

## The demo is not optional

Every work order ends with a demo, in one of exactly two shapes.

**A script**, when there is a command line. Copy-pasteable, and **no identifier a reader has to
substitute**. Nobody types thirty characters of base32. If the slice creates something with an id,
the demo captures it:

```bash
ACCOUNT=$(myapp account create --json | jq -r .id)
myapp account show "$ACCOUNT"
```

This is why every command a demo needs takes `--json` and prints exactly one object. It is a
convention worth adopting in the first slice that adds a command.

**Numbered steps**, when the slice is a user interface. Each step is one action, and the section
ends with `**Expected:**` — what should be on screen, specific enough to be wrong.

Both shapes are checked mechanically: `ledger.py check` fails a work order with no demo section, a
script demo with no runnable block, a UI demo with no expectation, and any demo still carrying a
placeholder identifier.

## Demo scripts accumulate; they do not evaporate

By slice forty there are forty proofs scattered across forty closed issues, none executed since
the day it was written. Two mechanisms keep that from happening:

- **`MANUAL-REGRESSION.md`** — a short, ordered list of scenarios promoted from demo scripts
  because they are worth re-checking. Kept alive by a definition-of-done rule that re-runs and
  re-dates any entry a slice's changes touch. **Kept short by deletion**: an entry is retired the
  moment an automated test covers it. A checklist nobody reads is worse than no checklist, because
  it looks like coverage.
- **An end-to-end suite** at the API or CLI level, grown as slices land.

When the suite is green and nobody has looked at the product in three weeks, the process has failed
even though every gate is passing.
