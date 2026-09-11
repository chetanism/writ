# The standing skills

Governs phase 9 of both bootstrap skills: emitting the four maintenance passes — `/cleanup`,
`/product-docs`, `/security-audit`, `/context-compact` — their orchestrator `/maintenance`, and
`/manual-test` into the new project, **tuned to the answers already given**. Read it before phase 9.

All are *standing* skills — they run outside the slice loop, on a cadence or on demand, and they
are what keeps a codebase from decaying between slices. `/slice-open` and `/slice-close` automate
the loop; these automate what the loop does not cover.

**The passes are separate skills, and `/maintenance` is only their order.** Each pass owns what
changes; `maintenance/delivery.md` owns how any of them lands — branch, gate, marker, pull request,
merge — and exists once so the four cannot drift in delivery. Split this way, each pass has a name
the model cannot misread, a description that triggers on its own job, a cadence of its own, and an
owner of its own on a team. The orchestrator survives because the order of a full run is not
arbitrary: cleanup rewrites code, the documentation is derived from what it changed, the audit
reads what both leave behind, and the compaction reads `CLAUDE.md` as all three leave it.

**`/context-compact` is the one pass with a trigger rather than a cadence.** `DoD-8` puts a line
into `CLAUDE.md` every time a slice establishes a convention, and until this pass existed nothing
ever took one out — so the highest-leverage document in the repository, the one read at the start of
every session, grew monotonically for as long as the project lasted. `scripts/ledger.py` measures it
against `context_budget` in `ledger.config.json` and warns over `warn_chars`; the pass moves whole
sections into the documents that own them and leaves a pointer. It is emitted always, and it is the
only pass whose scope is a number rather than a diff.

## The rule that makes this phase cheap

**Ask nothing you can derive.** By the time phase 9 runs, the interview has already settled almost
everything both skills need. Deriving it is not a nicety: a user who has answered forty questions
answers the forty-first carelessly, and phase 9 is where that would land.

| What the templates need | Already answered in |
|---|---|
| the gate command, for cleanup's verification | phase 5's gate-role table |
| the agent map's budget, and what else is read every session | nothing to ask: `context_budget` ships with `CLAUDE.md` and the kit's numbers |
| the integration branch, the PR flow, the squash policy | `DEVELOPMENT-PROCESS.md` §8, written in phase 8 |
| the attribution rule for maintenance commits | phase 8's attribution question, recorded in `CLAUDE.md` §Git |
| generated artefacts to exclude from cleanup | phase 5 |
| the stack-attention list in `security-audit/SKILL.md` §3 | phase 5's stack + phase 3's domain profile |
| which operators survive, and whether operator 13 exists at all | phase 3 (tenancy) and phase 4 (queues, leases, retention) |
| the areas, and the oracles inside them | the BRD's requirement tables and its invariants |
| the fixture's shape | the core object and its lifecycle, phases 2 and 6 |

**Four questions are left, and they fit in one `AskUserQuestion` call** — the limit in
`00-interview.md` is the budget, not the target:

1. **Which standing skills to install.** Multi-select over `/cleanup`, `/product-docs`,
   `/security-audit` and `/manual-test`, all four by default. A project that will never run a
   security audit should not carry the skill that says it does. **`/context-compact` is not on the
   menu** — it is the remedy for a rule the kit imposes on every project it bootstraps, so a project
   that declines it gets `DoD-8` with nothing to balance it. `/maintenance` is emitted whenever two
   or more passes are, and its order table carries only the passes that exist; with one pass there is
   nothing to order, so it is dropped and `delivery.md` still ships beside that pass.
2. **Documentation tooling** — none, or the generator this project will use. Decides
   `product-docs/SKILL.md`'s verification step and nothing else.
3. **How a throwaway instance of this system starts** — containers, a script, in-process, or *not
   decided yet*. **"Not decided yet" is a first-class answer**, and the most honest one at
   bootstrap; see *The harness* below.
4. **Cadence per pass** — cleanup, documentation and the audit each get their own, recorded in
   `DEVELOPMENT-PROCESS.md` §11. They differ in practice: cleanup often, documentation at a phase
   gate, the audit on a longer clock and after any dependency change. **Do not ask for
   `/context-compact`'s**: its trigger is the budget warning, and §11 says so rather than naming a
   clock nobody would keep.

## Two kinds of gap, and they are not interchangeable

The templates carry two markers, and using the wrong one is the mistake this section exists to
prevent:

| | `<ANGLE BRACKETS>` | `TODO:` |
|---|---|---|
| Means | Phase 9 knows this and must fill it now | Nobody can know this yet |
| Left behind is | **A bug.** The interview had the answer | Correct, and expected |
| Caught by | the ledger's placeholder scan, on `canon/**` | `/manual-test` §0, which refuses to walk |

**Leave no angle-bracket placeholder in anything you emit.** Leave `TODO:` markers exactly where
the truth is not knowable yet, and *say in the closing report that they are there*.

## Where things go

```
.claude/skills/cleanup/          the cleanup pass
.claude/skills/product-docs/     the documentation pass
.claude/skills/security-audit/   the audit, with reference/owasp.txt and cwe.tsv beside it
.claude/skills/context-compact/  the agent map compacted back under its budget
.claude/skills/maintenance/      SKILL.md — the full run; delivery.md — the loop every pass uses
.claude/skills/manual-test/      instructions and the harness
canon/maintenance/               the record — two backlogs, and audits/
```

Instructions live under `.claude/skills/`; the mutable record lives under `canon/`, at the top
level beside `qa/`, because both are maintained by skills that run outside the loop and both are
the first thing somebody looks for when a pass is due. A backlog inside a skills directory is a
record nobody reading `canon/` will ever find.

**Watch the placeholder scan.** `scripts/ledger.py` scans the prose of `canon/**/*.md` and `CLAUDE.md`
for any `<...>` token — whatever its case — outside inline code, fenced blocks and blockquotes, and
fails the build on one. Notation such as `/slice-open <id>` is safe inside backticks; a placeholder
to fill never is, which is why the templates keep theirs bare. Everything emitted into
`canon/maintenance/` spells dates and formats bare — `YYYY-MM-DD`, not the angle-bracketed
form. `.claude/skills/**` is not scanned, which is exactly why the harness can ship with `TODO:`
markers in it.

## Tuning the passes

Fill `<INTEGRATION BRANCH>` and `<GATE COMMAND>` in `maintenance/delivery.md`, once — every pass
reads them from there; `<GATE COMMAND>` and `<GENERATED ARTEFACTS>` in `cleanup/SKILL.md`;
`<DOC BUILD COMMAND>` and `<DOC BUILD OUTPUT>` in `product-docs/SKILL.md`; and write
`security-audit/SKILL.md` §3's stack-attention list from the real components.
`context-compact/SKILL.md` has nothing to fill — it reads its budget from the config and its gate
from `delivery.md` — but **its §3 destination table is worth one read against the tree you just
emitted**: if phase 0 renamed `canon/`, the destinations name the new tree.

Two things to get right rather than fast:

- **The stack-attention list must name this project's components**, not a generic OWASP restatement.
  *"The HTTP layer — routes with missing input validation"* is the shape; fill in the framework, the
  data layer, the queue, the config module, the logger. A generic list is one nobody reads twice.
- **If the project has no pull-request flow**, say so in `delivery.md` rather than leaving
  instructions that assume one. The marker-string discipline still applies — it is the only
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
  walk; `/cleanup` against a first commit has nothing to clean.
- **It does not add either to the gate.** These are standing skills, invoked by a human on a
  cadence. A maintenance pass in CI is a pass nobody reads the output of.
- **It does not emit the requirement detail track.** That is phase 10 and
  `references/10-requirements.md`. The two are easy to conflate — every one of these skills runs
  outside the slice loop — but these run on a *cadence* over the whole repository, and those run
  on *one identifier* one phase ahead of the queue. The questions and the failure modes are different,
  so keep the phases apart.
