# Slice <ID> — summary

> Committed to `writ/process/slices/<milestone>/<phase>/<ID>.md`, mirroring the work order, **in the slice's own commit**, then posted as a
> comment on the issue at step 7. The repository copy is the record; the comment is the
> notification.
>
> Written for a reader six months from now who was not present — which, for a small team, is you.
> Delete this blockquote.

## What the system can do now that it could not before

<One or two sentences, in terms of behaviour rather than files.>

## How it works

<The mechanism, at the altitude of "which pieces talk to which". Name the entry point so a reader
can start reading the code from the right place. Prefer three sentences and a file path over a
diagram.>

## Decisions made

| Decision | Chose | Over | Why | ADR |
|---|---|---|---|---|
|  |  |  |  |  |

> Anything with a credible rejected alternative also has an ADR. This table is the index, not the
> record. A decision too small for an ADR still gets a row, with `—` in the last column.

## Deliberately not done

<Scope consciously left out, and where it lands. Distinguishes a decision from an oversight.>

## Surprises

> **The highest-value section in this file.** What behaved differently from expectation, one bolded
> lead sentence each. Include the ones that are about the process rather than the code — a size
> estimate that was wrong three times running, an ADR that had to be superseded a slice after it
> was written. Writing this after the fact is how a surprise becomes a thing quietly fixed instead
> of a thing learned.

**<Bolded lead sentence.>** <Explanation.>

## Falsification

> Each control removed, the suite re-run, then restored. A test that still passes with the control
> removed was not testing the control.

| Control removed | Tests that failed |
|---|---|
|  |  |

## Size

**<S|M|L> — <N> code lines, <N> in the diff.** Queued <S|M|L>, estimated <N>.

## Verify it yourself

> The demo **as actually run**, with observed output as comments. Copy-pasteable, so the check is
> repeatable after later slices change things underneath it.

```bash
```

## Requirement coverage

| ID | Before | After | Proof |
|---|---|---|---|
|  | none | satisfied | `<test name>` |
