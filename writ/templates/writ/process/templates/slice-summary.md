# Slice <ID> — summary

> **What this is:** what the slice actually delivered, written for someone reading it months from
> now who was not there. Saved beside its work order in `writ/process/slices/<milestone>/<phase>/`,
> committed with the slice's code, and posted to the issue. Five sections and a line. Delete this
> note.

## What the system can do now that it could not before

<One or two sentences about behaviour a person would notice, not about files.>

## How it works

<Which pieces talk to which, in three sentences or so. Name the file to start reading from.>

## Decisions made

| Decision | Chose | Over | ADR |
|---|---|---|---|
|  |  |  | — |

> One row per choice that had a real alternative. Only a decision later slices must follow gets an
> ADR; the rest are just a row, with `—` in the last column.

## Surprises

> **The most useful section here.** Anything that behaved differently from what you expected, one
> bold opening sentence each — including surprises about the process, not just the code. Written
> down, a surprise becomes something the next slice knows; left out, it gets quietly fixed and
> learned again.

**<What surprised you, in one sentence.>** <What happened, and what it means for the next slice.>

## Falsification

> For each safeguard the slice added — a check, a guard, a rule that refuses something — it was
> removed, the tests that should notice were run, and it was put back. A safeguard nothing noticed
> is either untested or doing nothing. **This section finds real defects; never drop it.** Paste
> the table `python3 scripts/falsify.py` prints, and say what you did about any row that survived.

| Control removed | From | Tests run | Result |
|---|---|---|---|
|  |  |  |  |

## Played

<One line: the demo command you ran, or the screen you used, and what you saw.>
