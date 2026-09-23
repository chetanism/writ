# `/slice-close`

**Step 7 of the loop. Drafts the summary from the actual diff, falsifies the controls the slice
added, regenerates the ledger and the queue, walks the definition of done, drafts the commit with its trailer block, and hands you
the merge command.**

| | |
|---|---|
| **Run it** | After the gate is green **and the demo has been played by hand** |
| **Produces** | `writ/process/slices/<milestone>/<phase>/NNN.md`, a regenerated `COVERAGE.md` and `INDEX.md`, a drafted commit, a refreshed PR and issue |
| **Refuses to** | Start if the demo has not been played |

## What it does

1. **Refuses to start** until you confirm the demo was run by hand and did what the work order said.
2. **Reads the actual change** — the diff, not the work order's intentions.
3. **Measures the size** with `scripts/velocity.py --diff dev` — code and Markdown lines, read from
   git. Nothing is estimated or recorded by hand.
4. **Drafts the summary** — five sections and a line: what it does now, how it works, decisions,
   surprises, falsification, and what was seen when the demo was played.
5. **Falsifies it** with `scripts/falsify.py`: each safeguard the slice added is removed, only the
   tests that should notice are run, and the file is restored. A safeguard nothing noticed is a
   missing test.
6. **Regenerates and checks** — `ledger.py` then `ledger.py check`.
7. **Walks the definition of done** — the rows a command proves in one line, every other row one at
   a time.
8. **Names the scenarios this slice unblocks.**
9. **Drafts the commit** with its trailer block, refreshes the pull request and the issue, posts the
   summary, and hands over the merge command.

## The part that matters most

**It says `[you]` out loud on the rows that are yours.**

The definition of done is twelve rows. Three belong to the gate, three are half the tool's, and the
rest are nobody's but yours — the demo was played, the conflict read was done properly, the ADR
records a decision that was actually made, `CLAUDE.md` reflects anything.

A definition of done reported in aggregate is one nobody is applying, and **the rows most likely to
be waved through are precisely the ones no build will ever fail on.** So the skill walks them
individually and asks, rather than ticking the table. A slice closed with `DoD-5` marked *not done
— demo not played* is a better outcome than one where it was quietly assumed.

## Why the summary comes from the diff

Because the alternative is a summary written from memory, and memory reliably describes what the
slice was *for* rather than what it did. The gap between those two is where the interesting parts
of a change hide: the thing that turned out to be harder, the file that had to be touched, the
assumption that turned out to be wrong.

## See also

[`/slice-open`](slice-open.md) — step 2, and where the acceptance criteria this closes against were
written. [`/context-compact`](context-compact.md) — for when `DoD-8` has grown `CLAUDE.md` past its
budget.
