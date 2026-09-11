# `/manual-test`

**A seeded random walk over a real, isolated instance — draw a perturbation and a target, predict
from a written oracle, run it, classify what happened. Report-only, and reproducible from the seed
and the step counter alone.**

| | |
|---|---|
| **Run it** | When the suite is green and nobody has played with the product in weeks — a state **no gate can detect** |
| **Produces** | A classified report in the transcript. Nothing in the repository changes |
| **Never** | Edits a file, commits, opens an issue, or adds a manual-regression entry. Promotion is the reader's call |

## What it is for

**A human tester does three things an automated suite does not: composes steps nobody wrote down,
does them in an order nobody anticipated, and *notices*.** This runs that, seeded so it can be run
again.

It is not a substitute for the gate. Everything the suite asserts is already asserted. This is
aimed at the space between the assertions.

## The four hard rules

1. **The isolated instance, always.** Every shell begins by sourcing `env.sh`. Shell state does not
   survive a tool call, so a command run without it reaches the *development* instance — and the
   failure is silent: everything works, against the wrong data.
2. **`harness.sh` is the only thing that names an instance.** Never bring anything up by hand.
3. **Report only.** Findings go in the transcript and the reply; nothing in the repository moves.
4. **A step without a prediction is not a test.** State the expected outcome — with the identifier
   it comes from — *before* running the command.

The fourth is the one that makes this testing rather than clicking about. A prediction written
afterwards always matches.

## It refuses to start on an unfinished harness

The harness was generated at bootstrap, from an interview held **before the code existed**, and it
left a `TODO` marker everywhere it could not know the answer. Any remaining marker is a stop: you
fill them in with the user, then continue.

That check is why the markers are safe to ship — they block one session rather than reddening a
build, and a walk against a half-configured harness either fails at the first command or, far
worse, succeeds against the development instance.

## Where the oracles come from

**Seeded from the invariants the bootstrap interview produced** — which is the reason this skill
belongs in bootstrap rather than being adopted at slice forty. At bootstrap the oracles are written
from the specification; later they would be written from memory. `DoD-11` and `drift.py` are what
keep them true afterwards, and you can add your own checks by dropping an executable into
`drift.d/`.

## See also

[`/test-scenarios`](test-scenarios.md) — the scripted half of by-hand testing, written from a
requirement. This is the unscripted half.
