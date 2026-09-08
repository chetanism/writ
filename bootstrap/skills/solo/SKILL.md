---
name: solo
description: Interview one developer and generate their project's agent-first development process — specification, registry, slice queue, CI gate, coverage ledger and six tuned project skills. Use when starting a greenfield project built by one person plus coding agents.
disable-model-invocation: true
---

# Bootstrap — solo

You are setting up a project's development process. The output is a `docs/` tree, a CI gate, and a
traceability tool that a developer and their coding agents will live inside for months. Get the
interview right and the rest is transcription.

> **Read this first if you are not sure which skill to run.** This one assumes **one human**
> making every decision. If more than one person will write requirements, cut slices, or review
> code, stop and use **`/bootstrap:team`** instead — it designs the handoffs, and retrofitting them
> is harder than choosing correctly now. Ask if you do not know.

## What you are building, and why it is shaped this way

Four mechanisms carry the whole process. Everything else is prose around them.

1. **One declaration rule.** A registry declares identifier *families* — never identifiers. An
   identifier is declared *iff* it is the first cell of a table row, under an `| ID |` header,
   inside its family's declared section. Tools learn nothing but the registry, so adding a family
   is a Markdown row rather than a code change.
2. **A generated ledger that disbelieves its inputs.** A work order claims `satisfies`; a test
   names `[ID]`. Only both together count. A claim with no test is downgraded and listed.
   *A ledger that believes its own work orders is a spreadsheet.*
3. **Acceptance criteria become test names.** This is the only thing keeping a work order honest
   rather than decorative. A criterion that cannot become a test name is not written precisely
   enough yet.
4. **Every slice is demonstrated by hand.** Automated tests prove the system does what it was
   told to do. The demo is where the human finds out what they told it.

## How you report while running this

The interview is a conversation and reads like one — a question with no context is a question
answered carelessly. **Everything that is not a question is terse.** Phase reports, file lists,
what you found, what you are about to do:

- **Bullets and fragments, conclusion first.** No preamble, no recap of what the user just said, no
  closing summary of a section they watched you write.
- **Number every ask**, restarting each round, so the answer can be *"2. yes"*.
- **Tag by direction.** Past tense is what you did (`[WROTE]`, `[SKIPPED]`); imperative is what the
  user must do (`[DECIDE]`, `[FILL]`). Never one for the other.
- **Never print a file back.** Say the path and the one line that matters in it.
- **One line per fact.** A reason earns its line only if omitting it misleads.

`references/07-authoring-style.md` carries the full rule. It is the same mode you will offer the
project in phase 8, and running the bootstrap in it is how the user finds out whether they want it.

## The phases

Work through them in order. Do not write a single file before phase 6 — an interview that has
already committed to an answer stops being an interview.

**The kit root is `${CLAUDE_PLUGIN_ROOT}`**, and every `references/…`, `templates/…` and `skills/…`
path in this file is relative to it. The kit is a plugin: nothing of it is copied into the project,
and nothing of it is left behind. If that variable reads as literal text, the skill was loaded
outside the plugin; the kit root is then two directories above this file.

Load `references/00-interview.md` **now**; it governs how you ask everything below.

### Phase 0 — Orient

- Establish the target directory. Default: the repository root you are running in.
- Confirm the kit root (see above) holds `references/` and `templates/`. If not, stop.
- Confirm it is a git repository (`git rev-parse --git-dir`). If not, `git init` and say so.
- If `docs/spec/` already exists, **stop and report what is there.** Offer to adopt around it, never
  to overwrite it.
- Read the kit's `README.md` for the file inventory.
- Confirm the target and the project name back to the user in one line before continuing.

### Phase 1 — Obtain the BRD

Ask for a business requirements document. Accept **anything** — two paragraphs, a slide, a
competitor URL and a sentence about what is different, or a finished 40-page spec.

There is no minimum. If what arrives is thin, do not demand more: say you will build the BRD
*from* the interview, and that phase 2 is where it gets written. A user who could already write
the document would not need this.

Read what you were given and produce, in your reply, **a one-screen restatement**: what the
product is, who it is for, what it must do, and what you are still guessing. The guesses are
phase 2's agenda.

`references/01-scoping.md` has the intake checklist.

### Phase 2 — Adaptive scoping

Rounds of questions, calibrated to how much the BRD already settles.

- A **detailed spec** → confirm and fill gaps. Two or three rounds.
- **A few paragraphs** → the full bank. Expect six to ten rounds.

Batch at most four questions per `AskUserQuestion` call, number them, and move from coarse to
fine: what it is → who uses it → what the core object is → its lifecycle → the boundaries →
the edges nobody thinks about until production.

**The stop rule.** Keep going until you can write every functional-requirement table without
inventing a fact the user has not stated. *When you find yourself about to invent one, ask
instead.* Say explicitly when you have reached it, and list what you are deliberately leaving
open — an open question written down is fine; a guess written as a requirement is not.

### Phase 3 — Security, conditioned on the domain

Load `references/02-security.md`. Identify the domain profile first, then ask **only that
profile's questions**. A todo app asked about PCI scope learns that this process wastes its time;
a payments app not asked about it learns that too late.

Establish: what the worst realistic breach looks like, who the adversary is, what data is
regulated, whether there is a tenancy boundary, and what "authenticated" means here. Turn the
answers into `FR-SEC-*` requirements and, where a boundary must never be crossed, an **invariant**
— a numbered `INV-*` that is a defect to violate, not a style preference.

### Phase 4 — Robustness, reliability, scalability

Load `references/03-reliability.md`. Ground every question in the domain *and* the stack: ask
about consumer-group lag if there is a queue, about connection pooling if there is a database,
about cold starts if it is serverless.

Establish the availability target and its consequences, RTO and RPO, what retry and idempotency
mean for the core write, what happens under backpressure, what degrades and what fails closed,
what the first year's scale envelope is, and what must be observable on day one. These become
`NFR-*`. **Refuse to write a number the user did not give you** — an invented SLO is worse than
none, because everything downstream will be sized against it.

### Phase 5 — Stack and gate roles

Ask what the stack is. Then fill every **gate role** with a concrete command:

| Role | Answers | Example |
|---|---|---|
| format | is it formatted? | `pnpm fmt:check` |
| static analysis | does it smell? | `pnpm lint` |
| types | does it typecheck? | `pnpm typecheck` |
| unit | does it do what we told it? | `pnpm test` |
| integration | does it do it against the real thing? | `pnpm test:all` |
| contract | did the published surface change? | `pnpm openapi --check` |
| traceability | do the claims hold? | `python3 scripts/ledger.py check` |

A role with no command is a role the user is choosing to skip — record that choice in the process
document rather than leaving a gap. Then load exactly one of `references/stacks/*.md` and follow it
for the specifics.

### Phase 6 — Write the specification set

Now you write files. Copy each template from the kit's `templates/<path>` to `<path>` and fill it.
**Delete every guidance blockquote as you go**, and leave no `<PLACEHOLDER>` behind — phase 8's
check fails on either.

Order matters, because the registry is what the tools read:

1. `docs/spec/BRD.md` — the interview, written down. Requirement tables are `| ID | Requirement |
   Phase |`, one sentence each, numbered per area, **stable forever**.
2. `docs/spec/ID-REGISTRY.md` — declare a family for every identifier kind you just used. Mark
   traceable exactly those a slice can claim and a test can prove.
3. `docs/spec/MILESTONE-PLAN.md` — what structure each milestone builds, and its exit gates.
4. `docs/spec/<AREA>-SPEC.md` — a foundation spec for each shape everything else inherits (the
   data model, the API surface, an external port). Copy `FOUNDATION-SPEC.md` once per area. Skip
   this only for a project with no such shape, and say so.

`references/05-traceability.md` is the reference for the registry; `references/07-authoring-style.md`
is how these documents are written.

### Phase 7 — Slice

Load `references/04-slicing.md`. **Ask the user for their slicing criteria before you cut
anything** — the menu is in that file, and the answer changes every slice boundary.

Then:
- Cut slices. A slice is *the thinnest change that alters what the system can do, end to end, and
  can be exercised by hand.* If it cannot be demonstrated, it is a task; fold it into the slice it
  serves.
- Give each one a work order at `docs/process/work-orders/<N>.md` with front matter, from
  `docs/process/templates/work-order.md`.
- Order by **dependency**, not by wish: `depends_on` in the front matter, and the queue is
  generated from it. Confirm the ordering with the user before you generate.
- Size every slice against the budget you set in `DEVELOPMENT-PROCESS.md`, and split anything over
  the top tier rather than shipping it.

That reference also carries **the conflict read** — `DoD-12`, the step that asks whether a plan
would make a requirement *false* rather than which ones it advances. It lands in three places, all
written in phase 8: the definition of done, `/slice-open`'s step 2a, and `CLAUDE.md`'s *How to work
here*. Do not drop it into only one of them; it is a habit that survives by being asked for in the
place the work happens.

### Phase 8 — Emit the process

Copy the remaining templates: `docs/process/DEVELOPMENT-PROCESS.md` (tailored to the answers from
phases 5 and 7), `SLICE-QUEUE.md`, `MANUAL-REGRESSION.md`, both `docs/process/templates/`,
`docs/decisions/README.md` and `template.md`, `CLAUDE.md`, `.github/workflows/`,
`.claude/skills/slice-open` and `slice-close`, and `scripts/`.

Set `scripts/ledger.config.json` from phase 5 — the test globs and the annotation pattern are the
only stack-coupled values in the whole tool.

**Two questions here, in one `AskUserQuestion` call, and they are the only ones phase 8 asks.**

The first is attribution: whether commits and pull requests carry the agent's co-author trailer and
session link, or nothing. Neither is a default; some organisations require the trailer and some
forbid it. The answer lands in three places and must agree in all of them: `CLAUDE.md` §Git,
`DEVELOPMENT-PROCESS.md` §6.3, and `/maintenance`'s rules, which defer to `CLAUDE.md`.

The second is the reply mode. `CLAUDE.md` can carry a *Talking to me*
section that puts every agent reply into a directive mode — bullets and fragments, conclusion first,
`IMPORTANT`/`NOTE`/`ASK` groups, numbered asks, no preamble and no closing summary — or it can leave
the agent's usual voice alone. Ask which, with the consequence of each: the directive mode suits
somebody who reads a terminal all day and treats preamble as a tax; the usual voice suits somebody
who wants to be walked through the reasoning. **Emit the section whole or delete it whole** — a
half-applied interaction rule is worse than either, because the reader cannot tell which replies
were meant to follow it. `references/07-authoring-style.md` carries the section and the argument.

Whichever they choose, it governs replies only. The committed documents follow
`references/07-authoring-style.md` either way.

Then run it:

```bash
python3 scripts/test_ledger.py     # the tool's own suite
python3 scripts/ledger.py          # write COVERAGE.md and the queue block
python3 scripts/ledger.py check    # must exit 0
```

Fix what it reports. A non-zero exit here means a document you just wrote disagrees with another
document you just wrote, which is exactly what it is for.

### Phase 9 — The standing skills

Load `references/09-standing-skills.md`. Two more skills go into the project — `/maintenance`, which
runs the standing cleanup, documentation and security passes, and `/manual-test`, which walks a real
isolated instance looking for what the suite cannot assert. **They run outside the loop**, and they
are what keeps a codebase from decaying between slices.

**Ask nothing you can derive.** The interview has already settled the gate command, the branch flow,
the attribution rule, the stack, the tenancy boundary and the invariants; that reference maps each
one to where it was answered. Four questions remain and they fit in **one** `AskUserQuestion` call:
which of the two skills to install, the documentation tooling, how a throwaway instance of this
system starts, and the maintenance cadence.

Then emit:

```
.claude/skills/maintenance/     instructions — SKILL.md and the three passes
.claude/skills/manual-test/     instructions and the harness
docs/process/maintenance/       the record — two backlogs, and audits/
```

Two rules govern what you leave behind, and they are opposites:

- **No `<ANGLE BRACKET>` placeholder may survive.** Phase 9 had the answer; one left behind is a
  bug, and the ledger's placeholder scan fails the build on it.
- **`TODO:` markers in the manual-test harness are correct and expected.** At bootstrap there is no
  code to isolate, and a harness invented against imagined infrastructure is worse than an honest
  gap because it looks finished. `/manual-test` §0 greps for them and refuses to walk until they are
  filled with the user.

Then re-run `python3 scripts/ledger.py check`. It must still exit 0 with the new documents present.

### Phase 10 — The requirement detail track

Load `references/10-requirements.md`. One more pair of skills and one more directory, and they run
**parallel to the loop rather than inside it**: a requirement in the BRD is one line, which is
enough to build against and not enough to test against by hand.

Solo does not weaken this. The split that matters is **drafter and approver**, and solo it is the
agent who drafts and the one human who approves — the same two-party review, and the reason the
track exists at all: an agent's reading of a one-line requirement is exactly the thing a human is
there to correct.

**Ask nothing.** Everything is already settled: the traceable families from phase 6's registry, the
approver from phase 0, the invariants from phase 3, the phase tokens from the BRD's requirement
tables. Emit:

```
.claude/skills/requirement-detail/    the drafting conversation
.claude/skills/requirement-verify/    the per-phase-gate check, report-only
docs/process/requirements/README.md   the whole process, in one file
docs/process/templates/requirement-detail.md
```

and set `requirements` in `scripts/ledger.config.json`: `dir`, the covered `families` — the ones a
person can be *asked to exercise*, `["FR", "INV"]` by default and never the mechanism families —
the `phase_pattern` matching whatever token your requirement tables carry, and
`require_detail_for_satisfied: false`.

Three things to get right, because each is a failure the track is shaped around:

- **Leave the directory empty.** A `README.md` and nothing else is the correct output. Four hundred
  requirements drafted by an agent and read by nobody is a directory that looks like coverage,
  which is worse than an empty one.
- **The quote check is the whole mechanism.** A detail file carries its requirement's words
  verbatim and `ledger.py check` compares them character for character, so an amendment to the BRD
  fails every file that has not been re-read. Say that in the README, and say why: two wordings of
  one requirement is two requirements, found the day they disagree.
- **It is not in the definition of done**, deliberately. Coupling a slice to the detail of every
  requirement it touches puts the approver on the critical path of every merge. The track runs one
  phase ahead of the queue instead. `DoD-12` is the one place a slice reads it, and only the
  `reviewed` files.

Then re-run `python3 scripts/ledger.py check` a final time. It must exit 0 with an empty
requirements directory — which is also the first thing the track proves about itself.

### Commit the bootstrap

The generated tree is the project's first commit, and the loop assumes it is on `dev`:

```bash
git checkout -b dev 2>/dev/null || git checkout dev
git add -A
git commit -m "docs(process): bootstrap the development process"
git remote                                      # empty means no remote yet
```

Attribution on this commit follows the phase 8 answer. If there is no remote, say so in the
hand-over: `/slice-open` opens branches locally without one, but the draft pull request and the CI
gate wait until it exists.

### Hand over

Finish by reporting, in the terse mode above: whether the tree is committed on `dev` and whether
a remote exists; the tree you created, the counts (requirements
declared, slices queued), what `SL-000` will do, which standing skills you installed and what
`TODO:` markers remain in the manual-test harness, whether `CLAUDE.md` carries the directive mode,
and every question you left open, numbered. Tell the user the first command is `/slice-open
SL-000`, and that the requirement track starts whenever they want it with
`/requirement-detail <id>` — one phase ahead of whatever the queue is building.

## After bootstrap — the loop

The process you just wrote is the record; you do not need this skill again. Each slice runs:

**pick → work order → plan → implement → gate → play by hand → close.**

`/slice-open <id>` drafts the work order, branch and draft PR. `/slice-close` drafts the summary
from the diff, regenerates the ledger, walks the definition of done, and drafts the commit.

Two skills run **outside** the loop, and are the reason the loop does not have to carry everything:
`/maintenance` on the cadence set in phase 9, and `/manual-test` when the suite is green and nobody
has looked at the product in three weeks — which is a state the gate cannot detect and is exactly
when this process has failed.

Two more run **beside** it, one phase ahead of the queue: `/requirement-detail <id>` writes down
what a person would see if one requirement held, and `/requirement-verify <id>` asks at each phase
gate whether that behaviour is actually there. A requirement reading `●` in the ledger is one whose
*claims* are tested, which is not the same thing, and no slice owns the difference.

Three things are **never** delegated to an agent, and the process document says so: writing and
approving the work order, reading the implementation plan before code is written, and playing with
the result by hand. The characteristic failure of one-person-plus-agents is velocity outrunning
comprehension — a codebase that works, that nobody understands, and that therefore cannot be
safely changed.
