# The standing skills

Governs phase 9 of both bootstrap skills: emitting `/maintenance` and `/manual-test` into the new
project, **tuned to the answers already given**. Read it before phase 9.

Both are *standing* skills — they run outside the slice loop, on a cadence or on demand, and they
are the two things that keep a codebase from decaying between slices. `/slice-open` and
`/slice-close` automate the loop; these two automate what the loop does not cover.

## The rule that makes this phase cheap

**Ask nothing you can derive.** By the time phase 9 runs, the interview has already settled almost
everything both skills need. Deriving it is not a nicety: a user who has answered forty questions
answers the forty-first carelessly, and phase 9 is where that would land.

| What the templates need | Already answered in |
|---|---|
| the gate command, for cleanup's verification | phase 5's gate-role table |
| the integration branch, the PR flow, the squash policy | `DEVELOPMENT-PROCESS.md` §8, written in phase 8 |
| the attribution rule for maintenance commits | phase 8's commit-trailer decision |
| generated artefacts to exclude from cleanup | phase 5 |
| the stack-attention list in `security.md` §3 | phase 5's stack + phase 3's domain profile |
| which operators survive, and whether operator 13 exists at all | phase 3 (tenancy) and phase 4 (queues, leases, retention) |
| the areas, and the oracles inside them | the BRD's requirement tables and its invariants |
| the fixture's shape | the core object and its lifecycle, phases 2 and 6 |

**Four questions are left, and they fit in one `AskUserQuestion` call** — the limit in
`00-interview.md` is the budget, not the target:

1. **Which standing skills to install.** Multi-select, both by default. A project that will never
   run a security audit should not carry the prompt that says it does.
2. **Documentation tooling** — none, or the generator this project will use. Decides
   `documentation.md`'s verification step and nothing else.
3. **How a throwaway instance of this system starts** — containers, a script, in-process, or *not
   decided yet*. **"Not decided yet" is a first-class answer**, and the most honest one at
   bootstrap; see *The harness* below.
4. **Maintenance cadence** — recorded in `DEVELOPMENT-PROCESS.md` §11.

## Two kinds of gap, and they are not interchangeable

The templates carry two markers, and using the wrong one is the mistake this section exists to
prevent:

| | `<ANGLE BRACKETS>` | `TODO:` |
|---|---|---|
| Means | Phase 9 knows this and must fill it now | Nobody can know this yet |
| Left behind is | **A bug.** The interview had the answer | Correct, and expected |
| Caught by | the ledger's placeholder scan, on `docs/**` | `/manual-test` §0, which refuses to walk |

**Leave no angle-bracket placeholder in anything you emit.** Leave `TODO:` markers exactly where
the truth is not knowable yet, and *say in the closing report that they are there*.

## Where things go

```
.claude/skills/maintenance/     instructions, immutable
.claude/skills/manual-test/     instructions and the harness
docs/process/maintenance/       the record — two backlogs, and audits/
```

Instructions live under `.claude/skills/`; the mutable record lives under `docs/`, beside
`SLICE-QUEUE.md` and `MANUAL-REGRESSION.md`. A backlog inside a skills directory is a record nobody
reading `docs/` will ever find.

**Watch the placeholder scan.** `scripts/ledger.py` scans `docs/**/*.md` for `<Capitalized>` tokens
and fails the build on one. Everything emitted into `docs/process/maintenance/` must therefore
spell dates and formats bare — `YYYY-MM-DD`, not the angle-bracketed form. `.claude/skills/**` is
not scanned, which is exactly why the harness can ship with `TODO:` markers in it.

## Tuning `/maintenance`

Fill `<INTEGRATION BRANCH>` and `<GATE COMMAND>` in `SKILL.md`; `<GATE COMMAND>` and
`<GENERATED ARTEFACTS>` in `cleanup.md`; `<DOC BUILD COMMAND>` and `<DOC BUILD OUTPUT>` in
`documentation.md`; and write `security.md` §3's stack-attention list from the real components.

Two things to get right rather than fast:

- **The stack-attention list must name this project's components**, not a generic OWASP restatement.
  *"The HTTP layer — routes with missing input validation"* is the shape; fill in the framework, the
  data layer, the queue, the config module, the logger. A generic list is one nobody reads twice.
- **If the project has no pull-request flow**, say so in `SKILL.md`'s delivery loop rather than
  leaving instructions that assume one. The marker-string discipline still applies — it is the only
  thing that makes each pass's scope detection work — and it moves to whatever commit the merge
  produces.

## Tuning `/manual-test`

### The operators

Delete every operator whose *Applies when* this project does not satisfy. Deleting is right and
commenting-out is wrong: an inapplicable entry still gets drawn, and the redraw costs a step from a
budget that buys depth. In particular, **operator 13 goes entirely if there is no tenancy, account
or ownership boundary** — and stays, prominently, if there is.

Then rewrite each surviving operator's *holds anyway* clause to name **this project's** mechanism
and the identifier it comes from. The generic clause states the principle; the tuned one is what a
run can actually check.

### The areas, and the oracles

`reference/areas.md` is generated, one section per area of the BRD:

| Field | Comes from |
|---|---|
| **IDs** | the BRD's requirement table for that area, plus the invariants and NFRs that bear on it |
| **Surface** | the foundation specs. **"Not built yet" is a correct entry** at bootstrap, and knowing it saves a session from hunting |
| **Oracles** | **the invariants.** Phase 3 wrote them as numbered statements that are a defect to violate — which is precisely the definition of an oracle. They transfer almost verbatim |
| **Traps** | empty. Every entry here is earned by somebody having been wrong |

That the invariants become oracles for free is the reason this belongs inside bootstrap rather than
being bolted on later. A project that adopts manual testing at slice forty writes these from
memory; a project that bootstraps them writes them from the specification, on the day the
specification was agreed.

### The harness

`harness.sh` and `env.sh` are generated from question 3 and left honestly incomplete.

- **Containers, or a script** — fill the bring-up, the teardown, the process list and the isolated
  addresses. Every address must differ from the development defaults; **same ports means same
  instance**, and the walk then destroys the state the user was working in.
- **In-process** — `up` and `down` become the fixture's own setup and teardown, `PROCESSES` stays
  empty, and that is a complete harness, not a stub.
- **Not decided yet** — leave the `TODO:` markers. `/manual-test` §0 greps for them and refuses to
  walk, offering to fill them with the user on first run. This is deliberate: at bootstrap there is
  no code to isolate, and a harness invented against imagined infrastructure is worse than an
  honest gap, because it looks finished.

Say in the closing report which markers remain and that the first `/manual-test` will stop on them.

### What keeps it alive

An `areas.md` written at bootstrap and never touched is a liability by slice ten — it names oracles
for a system that has moved. Two mechanisms prevent that, and both are already in the kit:

- **DoD-11** — a slice that establishes or changes an invariant updates its oracle here. Walked
  item by item by `/slice-close`, like every other definition-of-done item.
- **`drift.py`** — run at the start of every session, before the walk. It reports an oracle citing
  an identifier or decision that no longer exists, and the run reports it rather than fixing it.

## What phase 9 does not do

- **It does not run either skill.** `/manual-test` against a project with no code has nothing to
  walk; `/maintenance` against a first commit has nothing to clean.
- **It does not add either to the gate.** These are standing skills, invoked by a human on a
  cadence. A maintenance pass in CI is a pass nobody reads the output of.
- **It does not emit the requirement detail track.** That is phase 10 and
  `references/10-requirements.md`. The two are easy to conflate — all four skills run outside the
  slice loop — but these two run on a *cadence* over the whole repository, and those two run on
  *one identifier* one phase ahead of the queue. The questions and the failure modes are different,
  so keep the phases apart.
