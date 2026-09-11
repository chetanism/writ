---
name: manual-test
description: Run an exploratory manual-testing session — a seeded random walk over a real, isolated instance of this system, judged against written-down oracles, ending in a classified report. Use when asked to manually test, exploratorily test, "poke at", smoke-test or sanity-check the app, or to check whether the system actually works beyond what the automated suite asserts.
---

# Manual testing

A human tester does three things an automated suite does not: composes steps nobody wrote down
together, does them in an order nobody anticipated, and **notices**. This runs that, seeded so it
can be run again.

**It is not a substitute for the gate.** Everything the suite asserts is already asserted;
re-asserting it here buys nothing. What this reaches is the space *between* slices — interleavings,
mid-flight state changes, and compositions no single slice's tests build.

---

## Hard rules

1. **The isolated instance, always.** Every shell begins with
   `. .claude/skills/manual-test/env.sh`. Shell state does not survive a tool call, so a command
   run without it reaches the **development** instance — the one being worked in — and the failure
   is silent: everything works, against the wrong data.
2. **`harness.sh` is the only thing that names an instance.** Never bring anything up by hand, and
   never run the project's own dev commands for the stack; that is what points at the wrong one.
3. **Report only.** Do not edit any file in the repository, do not commit, do not open an issue, do
   not add an entry to `writ/process/MANUAL-REGRESSION.md`. Findings go in the transcript under
   `$MT_HOME` and in the reply. Promotion is the reader's call.
4. **A step without a prediction is not a test.** State the expected outcome — with the identifier
   it comes from, where one exists — *before* running the command.

---

## 0 · Refuse to start on an unfinished harness

```bash
grep -rn 'TODO' .claude/skills/manual-test/harness.sh .claude/skills/manual-test/env.sh
```

**Any hit is a stop.** Bootstrap generated this harness from an interview held before the code
existed, and left a marker everywhere it could not know the answer. Fill them **with the user** —
the isolated addresses, the bring-up, the process list, the surface — then continue. A walk against
a half-configured harness either fails at the first command or, worse, succeeds against the
development instance.

This check is why the markers are safe to ship: they block one session rather than reddening a
build.

---

## 1 · Ask

One `AskUserQuestion` call, three questions.

**Area** — "Which part of the app should this session work over?" Offer *Whole app* plus the two or
three broadest sections of `reference/areas.md`. Say in the question text that **Other** takes a
narrower area or a free-text description, and name what is available: the section titles of
`reference/areas.md`.

**Depth** — "How much should it cover?" Offer:

| | steps | roughly | what it does |
|---|---|---|---|
| **Sanity** | ~15 | 10 min | the golden path of the area, plus four or five perturbations. Answers *is it broken right now* |
| **Regular** (recommended) | ~50 | 30 min | operators drawn across the area's oracles, evidence read back |
| **Deep** | ~150 | 90 min | every oracle in the area touched at least once, plus interrupt and concurrency operators |
| **Adversarial** | ~300 | open-ended | deliberately hostile, runs until it finds something or the budget ends |

**Seed** — "New run, or replay one?" Offer *New seed* (recommended) and *Replay a previous run*;
**Other** takes a pasted seed. A replay re-runs the identical sequence of draws, so a finding is
reproducible rather than anecdotal — and a replay always starts `--fresh`.

Ask nothing else. Everything else is a default worth taking.

---

## 2 · Bring it up

```bash
. .claude/skills/manual-test/env.sh
export MT_SEED="$(python3 .claude/skills/manual-test/draw.py --seed)"   # or the replayed one
mkdir -p "$MT_HOME/$MT_SEED"
./.claude/skills/manual-test/harness.sh up --fresh   # omit --fresh to keep an existing run's data
./.claude/skills/manual-test/harness.sh servers start
```

`MT_SEED` does not survive a tool call either — re-export it in every shell, or write it into
`$MT_HOME/session.sh` with `mt_remember MT_SEED "$MT_SEED"` and let `env.sh` restore it.

`up` is idempotent; `up --fresh` destroys the data first, which is what makes a seeded replay a
replay. Read `harness.sh status` before starting the walk: everything healthy, or fix that first.

Then two reads that decide what the walk is testing against:

```bash
./.claude/skills/manual-test/harness.sh drift      # is the reference still true?
./.claude/skills/manual-test/harness.sh surface    # what the system says about itself now
```

**`drift` first, and act on what it says.** A non-zero exit means an oracle names something that no
longer exists — a **maintenance finding**, reported as such and never tested against, because an
oracle pointing at a removed thing produces a false finding every session until somebody chases it
down. Do not correct the file; the run is report-only.

**`surface` is the authority for anything enumerable.** `areas.md` keeps the *reasoning*, which
cannot be queried; the enumerations come from `surface`, which cannot be stale. Where the two
disagree, `surface` wins and the disagreement is a drift finding.

---

## 3 · Bootstrap the fixture

The state the system needs before it can do anything interesting, in order.

> **Generated at bootstrap from the core object and its lifecycle, and completed on first run.**
> Every line here should be load-bearing — present because leaving it out fails. Write it as a
> runnable block that captures its identifiers with `mt_remember`, so a later shell has them:
>
> ```bash
> . .claude/skills/manual-test/env.sh && set -e
> # create the root object, remember its id, then each prerequisite in dependency order
> ```
>
> When a step exists **because of a requirement**, say which in a comment. The most valuable lines
> in a fixture are the ones explaining why leaving a step out produces a failure that looks like
> something else entirely — a missing prerequisite that presents as a hung pipeline rather than as
> a refusal. Those comments are what stop the next session debugging the fixture instead of the
> system. Delete this blockquote once the fixture is real.

**A second actor is part of the fixture at Regular depth and above** wherever the system has an
isolation boundary, because operator 13 is the one worth spending steps on.

Where an operation is asynchronous, **poll, never sleep blind**: read the state back in a bounded
loop, and treat the bound being reached as an observation rather than a hang.

---

## 4 · Walk

Read `reference/areas.md` for the chosen area and `reference/operators.md` once, at the start. For
`whole app`, draw two or three area sections per depth band rather than reading them all.

Anything **new** in `harness.sh surface` that no section of `areas.md` mentions is a target worth
spending steps on, and worth saying so in the report: it is where the reference has gone thin,
which is the benign half of drift and the half only a run notices.

Each step, in this order:

1. **Draw.** An operator and a target, from the lists, at the current counter.
   ```bash
   grep -E '^### ' .claude/skills/manual-test/reference/operators.md | sed 's/^### //' \
     | python3 .claude/skills/manual-test/draw.py "$MT_SEED" "$N" --pick
   ```
   Increment `N` for **every** draw, including one that is redrawn. Two draws sharing a counter are
   the same draw, which is how a replay silently stops being one.
2. **Predict.** Write the expected outcome and the identifier it comes from, before running
   anything. If no oracle in `areas.md` covers it, say so — an unoracled step is exploration and is
   recorded as such, not as a pass.
3. **Run**, from one shell, with the env sourced.
4. **Judge.** Match or not. On a mismatch, go to §5 before continuing.
5. **Record** — counter, draw, prediction, command, observed, verdict — appended to
   `$MT_HOME/$MT_SEED/transcript.md`.

Rules for the walk itself:

- **Compose; do not repeat the suite.** If a single unit test would assert it, it is already
  asserted. Reach for two-step and three-step sequences, and for state that changes between the
  steps.
- **Prefer breadth early, depth late.** Touch each of the area's oracles once before spending ten
  steps on one.
- **Read the evidence.** Operator 14 is not optional filler — a correct-looking outcome with a
  missing audit row, a leaked credential in a log line, or a queued item nobody drained is a
  finding the response body cannot show you.
- **Do not clean up between steps.** Accumulated state is the point; a tester who resets is running
  the suite again by hand.
- **Two identical requests at once** means `&` and `wait`, not two sequential calls.

Stop at the step budget, or when the area's oracles are all covered and three consecutive steps
have found nothing — whichever comes first. Say which.

---

## 5 · Verify before reporting

**The prior is that the tester is wrong.** This is not modesty; it is the base rate. When a real
project first ran a live-server suite against its own written specification, it found eight
disagreements and **all eight were the test's**, not the code's. The document wins; the run changes.

On every mismatch:

1. **Re-read the oracle.** In `areas.md`, then in the document it cites. Precedence is the one in
   `CLAUDE.md`: the BRD outranks the milestone plan, which outranks the queue, which outranks
   everything else.
2. **Reproduce minimally.** A fresh fixture, the shortest sequence that shows it. A mismatch that
   does not reproduce is recorded as **not reproduced** and is not a finding.
3. **Classify.** One of four, and say which:

   | | meaning |
   |---|---|
   | **defect** | the code disagrees with a specification that is clear |
   | **spec gap** | the code is defensible and no specification decides it — the finding is the absence |
   | **tester error** | the run misread the spec, the fixture, or an intended refusal |
   | **expected** | documented behaviour that merely looks wrong |

Only **defect** and **spec gap** reach the report as findings. The other two are recorded in the
transcript, because a repeated tester error is a signal that something is badly named.

---

## 6 · Report

If `CLAUDE.md` defines a response format, follow it. Otherwise:

```
FINDINGS
  [FIX]  <one line per defect> — path:line if known · identifier · seed:counter
  [GAP]  <one line per spec gap> — what is undecided, and who decides it
CONTEXT
  [NOTE] area covered, depth, N steps, M oracles touched, K not reached
  [NOTE] drift: <stale references, or "none"> · <surface entries no oracle covers>
  [NOTE] transcript: $MT_HOME/$MT_SEED/transcript.md · replay: /manual-test seed <seed>
OPEN
  [ASK]  <only where a spec gap needs a decision>
```

State the **seed and the step counter** for every finding: that pair is the whole reproduction.

Where a finding is worth re-checking after later slices, say it would make an `MR` entry in
`writ/process/MANUAL-REGRESSION.md` — and **do not write one**. Rule 3.

Finish with `harness.sh servers stop`. Leave the instance up unless asked; the next session reuses
it, and a `--fresh` on the next `up` is cheaper than the data was.

---

## Files

| | |
|---|---|
| `env.sh` | source it in **every** shell — isolated addresses, `$MT_HOME`, `mt_remember`, `mt_log` |
| `harness.sh` | `up [--fresh]` · `down [--keep-data]` · `servers <start\|stop\|status\|logs>` · `surface` · `drift` · `status` |
| `draw.py` | deterministic choice from a seed and a counter |
| `drift.py` | do the oracles still name identifiers and decisions that exist? |
| `drift.d/` | project-specific drift checks, added as the surface becomes enumerable |
| `reference/areas.md` | per area: identifiers, surface, oracles, traps |
| `reference/operators.md` | the perturbations, and what must hold under each |

Run state — transcript, logs, pidfiles, the session's identifiers — lives under `$MT_HOME`, outside
the repository, so a session never dirties the worktree.
