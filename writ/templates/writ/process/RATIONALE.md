# Why the definition of done is shaped the way it is

> Read once, when you are new here or about to change `DEVELOPMENT-PROCESS.md` §4 — not at every
> close. The table and its one-line reporting rule are in §4; this is the reasoning behind them,
> kept out of the path read at every slice.

## Half of this is on your honour, and that is the design

Three rows are the gate's, three are half the tool's, and the rest are nobody's but yours. That is
worth saying out loud, because this process spends most of its words on machine-checked things —
*a ledger that believes its own work orders is a spreadsheet* — and a reader who absorbs that tone
without this paragraph will assume the rest is checked too. It is not, and the unchecked half is
where the value is.

**Nothing here can verify that a human did a human thing.** A demo can be recorded as run by
somebody who did not run it. A conflict read can be reported as clean by an agent that performed
it carelessly. A falsification section can be written without removing a single control. The tool
checks the *artefact* — that a demo section exists and carries no placeholder, that `/slice-open`
produced a conflict report, that a summary was committed — and the artefact is not the act.

This is not a gap to be closed. It is the reason the process is worth running: **the checkable
things are checked so that attention is left over for the things that cannot be.** Automating the
judgement out of DoD-5 or DoD-12 would not make them true, it would make them invisible — which is
exactly what a green gate over an unplayed demo already is. The defence is a named owner, §10's
list of what is never delegated, and the habit of saying which of these you actually did.

So: when you walk this list at close, **say `[you]` out loud on the rows that are yours** rather
than reporting the table as met. A definition of done reported in aggregate is a definition of done
nobody is applying, and the rows most likely to be waved through are precisely the ones no build
will ever fail on.

`DoD-12` is worth its line because the requirement a plan breaks is almost never one the plan
claims. The shape, seen in a real project: a decision recorded an amount of money in one country's
minor units with no currency stored anywhere — against a P0 invariant saying country-specific facts
are configuration, never assumptions baked into the product. Every requirement the slice claimed had
been read carefully; none of them pointed at it, because an invariant is a shape rather than a
capability and so belongs to no requirement area a slicer would search.

It is met **at step 2a, before the work order is drafted**, and `/slice-open` reports it either way.
A conflict found at close is a finding rather than a tick: say which requirement the shipped code
makes false and take it to the slicer. It is never closed by reinterpreting the requirement.
