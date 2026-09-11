---
name: solo
description: Interview one developer and generate their project's agent-first development process — specification, registry, slice queue, CI gate, coverage ledger and twelve tuned project skills. Use when starting a greenfield project built by one person plus coding agents.
disable-model-invocation: true
---

# Canon — solo

You are setting up a project's development process. The output is a `canon/` tree, a CI gate, and a
traceability tool that a developer and their coding agents will live inside for months. Get the
interview right and the rest is transcription.

> **Read this first if you are not sure which skill to run.** This one assumes **one human**
> making every decision. If more than one person will write requirements, cut slices, or review
> code, stop and use **`/canon:team`** instead — it designs the handoffs, and retrofitting them
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

**One exception, and it is not a document: `.canon-interview.md` at the target root.** Append a
section to it at the end of every phase, before you report that phase — the decisions in one line
each, what was left open, and what you would otherwise have to ask twice. Ten phases and up to ten
rounds of questions in phase 2 alone is more than one sitting for most people, and without this a
session that ends at phase 7 costs every answer given. It is deleted at the commit, once its
content is in the documents. `references/00-interview.md` §*Surviving the session* is the rule.

**The kit root is `${CLAUDE_PLUGIN_ROOT}`**, and every `references/…`, `templates/…` and `skills/…`
path in this file is relative to it. The kit is a plugin: nothing of it is copied into the project,
and nothing of it is left behind. If that variable reads as literal text, the skill was loaded
outside the plugin; the kit root is then two directories above this file.

Load `references/00-interview.md` **now**; it governs how you ask everything below.

### Phase 0 — Orient

- **Look for `.canon-interview.md` at the target first.** A previous run left it there if one got
  part-way; it holds one section per completed phase. Read it, say what it covers, and offer to
  resume from the next phase or to start over — `references/00-interview.md` §*Resuming* has the
  rule, including what to do when a `<canon>/spec/` exists as well. With no such file, say nothing
  and carry on.
- Establish the target directory. Default: the repository root you are running in.
- Confirm the kit root (see above) holds `references/` and `templates/`. If not, stop.
- Confirm it is a git repository (`git rev-parse --git-dir`). If not, `git init` and say so.
- **Ask what to call the tree.** Default `canon/` — the authoritative body of documents an agent
  reads before it writes code. Any single lowercase path segment that does not already exist at
  the target is fine. Not `docs/`: that is where `/product-docs` writes the generated product
  documentation, and the two colliding is the reason the default is not `docs`. Every path below
  and in every template says `canon/`; phase 8 rewrites them if the answer differs.
- If `<canon>/spec/` already exists, **stop and report what is there.** Offer to adopt around it,
  never to overwrite it.
- **Check the twelve skill names against what is already there.** The kit emits `slice-open`,
  `slice-close`, `cleanup`, `product-docs`, `security-audit`, `context-compact`, `maintenance`,
  `manual-test`, `requirement-detail`, `requirement-verify`, `test-scenarios` and `change-request`
  as bare `/name` skills, and a
  bare name can already be taken in four places: `.claude/skills/<name>/` and
  `.claude/commands/<name>.md` in the target, and the same two under `~/.claude/`. Plugin skills
  are namespaced and cannot collide. **Never overwrite one and never rename the user's.** With no
  collision, ask nothing. With one or more, list them — which name, where it lives, and whether
  it is the project's or the user's — and ask once, in one `AskUserQuestion`, with two options:
    1. **Prefix every kit skill with `canon-`** (the default): `/canon-cleanup`, `/canon-slice-open`
       and so on. One decision, and the set stays a set; a half-prefixed set is worse than either
       extreme because nobody can tell which skills belong together.
    2. **Name the colliding ones**, one at a time, for somebody who wants `/cleanup` to stay theirs.
  A user-level collision is shadowing rather than overwriting, but a `/cleanup` that resolves to
  one thing in this repository and another everywhere else is the confusion the question exists
  to avoid, so it is treated the same way. Record the resulting table of old and new names; phase
  8 applies it.
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

Load `references/11-registers.md` first: **a file holds one kind of thing, and status is a
column.** The BRD is narrative and declares nothing; every identified item is a row in a register
of its own; history is one changelog. Order matters, because the registry is what the tools read:

1. `canon/spec/BRD.md` — the case for the product, in prose. No identifier tables in it.
2. The registers, one file each, from the interview: the requirement areas as
   `canon/spec/requirements/<AREA>/index.md` from `canon/process/templates/requirement-area.md`,
   then `invariants.md`, `compliance.md`, `strategic-decisions.md`, `personas.md`,
   `milestones.md`, `dependencies.md`, `risks.md`, `assumptions.md`, `out-of-scope.md` and
   `questions.md`. Rows are `| ID | … | Target | Since | Status |`, one sentence each, numbered per
   area to the family's width, **stable forever**, every one `Since: v0.1` and `Status: active`.
   Delete the seed row in each; leave no example identifier behind.
3. `canon/spec/ID-REGISTRY.md` — a row for every family you just used, with its width, and a
   directory owner for the requirement areas. Mark traceable exactly those a slice can claim and a
   test can prove.
4. `canon/spec/MILESTONE-PLAN.md` — purpose, gates, phases as `P01`, `P02` with names, foundation
   specs, what is not built, external tracks. Risks and questions went into their registers.
5. `canon/spec/<AREA>-SPEC.md` — a foundation spec for each shape everything else inherits (the
   data model, the API surface, an external port). Copy `FOUNDATION-SPEC.md` once per area. Skip
   this only for a project with no such shape, and say so.
6. `canon/spec/CHANGELOG.md` — the seed row, `X-001`, dated today, touching `v0.1`.

Then list what you wrote under `registers` and `narrative` in `scripts/ledger.config.json`, so the
check holds each file to its kind from the first commit. `references/05-traceability.md` is the
reference for the registry; `references/07-authoring-style.md` is how these documents are written.

### Phase 7 — Slice

Load `references/04-slicing.md`. **Ask the user for their slicing criteria before you cut
anything** — the menu is in that file, and the answer changes every slice boundary.

Then:
- Cut slices. A slice is *the thinnest change that alters what the system can do, end to end, and
  can be exercised by hand.* If it cannot be demonstrated, it is a task; fold it into the slice it
  serves.
- Group the slices into phases named `P01`, `P02`, … in dependency order, each with a name and an
  exit criterion, in `MILESTONE-PLAN.md` §3 and as `phases` in `scripts/ledger.config.json`. Never
  letters: they collide with the identifier families, and the workarounds mean nothing.
- Number the slices `SL-001`, `SL-002`, … in the order you cut them — a global, zero-padded
  number that encodes nothing about the phase, so a slice that later moves phase or splits never
  carries a lie. Slice zero is `SL-000` and ships.
- Give each one a work order at `canon/process/work-orders/<milestone>/<phase>/<NNN>.md`, named
  for its number, with front matter from `canon/process/templates/work-order.md`. The milestone
  directory is `m1-<slug>`, matching the milestone plan — rename the shipped `m1/` to carry the
  slug — and the phase directory is the code the front matter declares. Slice summaries will file
  at the mirrored path under `slices/`; the README in each directory says so.
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

Copy the remaining templates: `canon/process/DEVELOPMENT-PROCESS.md` (tailored to the answers from
phases 5 and 7), `SLICE-QUEUE.md`, `MANUAL-REGRESSION.md`, both `canon/process/templates/`,
`canon/decisions/README.md` and `template.md`, `CLAUDE.md`, `.github/workflows/`,
`.claude/skills/slice-open`, `slice-close` and `change-request`, and `scripts/`.

Set `scripts/ledger.config.json` from phase 5 — the test globs and the annotation pattern are the
only stack-coupled values in the whole tool.

**If phase 0 chose a name other than `canon`, rewrite the emitted tree now**, before anything else
reads it: move `canon/` to `<name>/`, then replace every `canon/` path — the trailing slash is what
makes it a path and not the word — across the emitted files: `<name>/`, `CLAUDE.md`,
`.claude/skills/`, `.github/`, `scripts/ledger.config.json` and `scripts/test_ledger.py`. The tool
itself reads every path from the config, so `ledger.py` needs nothing. Then grep for `canon/` and
expect hits in one place only: `ledger.py`'s `DEFAULTS`, which are the fallbacks for a key the
config does not carry. Leave them. Anywhere else is a path this project will actually read.

**If phase 0 renamed any skill, apply that table in the same step.** For each old and new name:
move `.claude/skills/<old>/` to `.claude/skills/<new>/`, set `name: <new>` in its front matter,
and replace `/<old>` and `.claude/skills/<old>/` across the emitted tree — the skills name each
other throughout, the orchestrator calls the four passes, `/slice-close` names the requirement
skills, `scripts/ledger.py` names `/context-compact` in its budget warning, and every document map
lists them. Match the token with the slash or the path in front of
it, so prose that says *cleanup* is untouched. Then grep for each old name in both forms and
expect no hits.

**Three questions here, in one `AskUserQuestion` call, and they are the only ones phase 8 asks.**

The first is attribution: whether commits and pull requests carry the agent's co-author trailer and
session link, or nothing. Neither is a default; some organisations require the trailer and some
forbid it. The answer lands in three places and must agree in all of them: `CLAUDE.md` §Git,
`DEVELOPMENT-PROCESS.md` §6.3, and `.claude/skills/maintenance/delivery.md`'s rules, which defer to `CLAUDE.md`.

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

The third is the tracker: **does every claimed slice get an issue, and where?** GitHub is the
answer the kit ships — `/slice-open` opens the issue with the work order file as its body, labelled
by phase and size, `/slice-close` re-syncs it, posts the summary as a comment and closes it through
the trailer, and `ledger.py check` fails a claimed slice with no `issue:`. Anything else is `none`
today, said plainly in the hand-over, with the `gh` calls in the two skills as the thing to swap.
The answer lands in `tracker` in `scripts/ledger.config.json` — `"github"` or `""` — and in the
documents that read it: `DEVELOPMENT-PROCESS.md` §1, §3, `DoD-9`, §6.3 and §8.1, the work order
template's `issue:` line, `SL-000`'s criterion 12, and the two skills. **With no tracker, delete
rather than soften**: `Closes #N` from §6.3 and the commit template, the second clause of `DoD-9`,
§8.1, the `issue:` line, and criterion 12. A half-present tracker is a `Closes` line pointing at
nothing.

Then run it:

```bash
python3 scripts/test_ledger.py     # the tool's own suite
python3 scripts/ledger.py          # write COVERAGE.md and the queue block
python3 scripts/ledger.py check    # must exit 0
```

Fix what it reports. A non-zero exit here means a document you just wrote disagrees with another
document you just wrote, which is exactly what it is for.

### Phase 9 — The standing skills

Load `references/09-standing-skills.md`. The standing skills go into the project — `/cleanup`,
`/product-docs` and `/security-audit`, each a pass of its own with its own cadence,
`/context-compact`, which is the only thing that ever takes a line *out* of `CLAUDE.md`,
`/maintenance`, which runs the four in order through one shared delivery loop, and `/manual-test`,
which walks a real isolated instance looking for what the suite cannot assert. **They run outside
the loop**, and they are what keeps a codebase from decaying between slices.

**Ask nothing you can derive.** The interview has already settled the gate command, the branch flow,
the attribution rule, the stack, the tenancy boundary and the invariants; that reference maps each
one to where it was answered. Four questions remain and they fit in **one** `AskUserQuestion` call:
which of the standing skills to install, the documentation tooling, how a throwaway instance of
this system starts, and the cadence of each pass.

Then emit:

```
.claude/skills/cleanup/          the cleanup pass
.claude/skills/product-docs/     the documentation pass
.claude/skills/security-audit/   the audit, with its OWASP and CWE checklists beside it
.claude/skills/context-compact/  the agent map compacted back under its budget
.claude/skills/maintenance/      the full run in order, and delivery.md — the shared loop
.claude/skills/manual-test/      instructions and the harness
canon/maintenance/               the record — two backlogs, and audits/
```

A pass the user declined is not emitted, and `/maintenance`'s order table loses its row. With one
pass left there is nothing to order, so emit that pass and `delivery.md` and drop `/maintenance`.
**`/context-compact` is not one of the declinable ones**: the kit's own `DoD-8` is what makes it
necessary, so a project that ships without it ships with a file that only grows.

Two rules govern what you leave behind, and they are opposites:

- **No `<ANGLE BRACKET>` placeholder may survive.** Phase 9 had the answer; one left behind is a
  bug, and the ledger's placeholder scan fails the build on it.
- **`TODO:` markers in the manual-test harness are correct and expected.** At bootstrap there is no
  code to isolate, and a harness invented against imagined infrastructure is worse than an honest
  gap because it looks finished. `/manual-test` §0 greps for them and refuses to walk until they are
  filled with the user.

Then re-run `python3 scripts/ledger.py check`. It must still exit 0 with the new documents present.

### Phase 10 — The requirement detail track

Load `references/10-requirements.md`. Three more skills and two more directories, and they run
**parallel to the loop rather than inside it**: a requirement in the BRD is one line, which is
enough to build against and not enough to test against by hand. The detail file settles what it
means, told as stories; the scenarios file, written from it, is what somebody does at a keyboard to
find out whether it holds.

Solo does not weaken this. The split that matters is **drafter and approver**, and solo it is the
agent who drafts and the one human who approves — the same two-party review, and the reason the
track exists at all: an agent's reading of a one-line requirement is exactly the thing a human is
there to correct.

**Ask one question, and it is whether to install the track at all.** Everything else is already
settled: the traceable families from phase 6's registry, the approver from phase 0, the invariants
from phase 3, the phase tokens from the BRD's requirement tables.

The question, with both consequences said plainly:

1. **Install it now** (the default where the first milestone has more than a handful of
   requirements). Three skills and two directories that ship empty; the track starts whenever the
   user wants it, one phase ahead of the queue, and costs nothing until a file is written.
2. **Defer it.** `requirements.dir` and `scenarios.dir` stay `""`, the three skills are not
   emitted, and every check they add goes quiet. Adopting it later is copying three files and
   setting two config values — there is nothing to retrofit, because the detail files quote the
   registers rather than the registers depending on them.

**Say what the track costs before asking.** It is a second document per requirement, and its value
is entirely in somebody reading it: a project with twelve requirements and one person who wrote all
of them is one where the detail file says back what its author already knows. The failure it exists
to prevent — a one-line requirement and a tester guessing the actors — needs a tester to exist. If
the user cannot name who will read a detail file, deferring is the honest answer and the
hand-over says what has to become true first.

With the track deferred, skip to the commit; nothing below is emitted. Otherwise:

```
.claude/skills/requirement-detail/    the drafting conversation
.claude/skills/requirement-verify/    the per-phase-gate check, report-only
.claude/skills/test-scenarios/        the detail file turned into a session, list first
canon/spec/requirements/README.md   the whole detail process, in one file
canon/qa/README.md                     the whole scenario process, in one file
canon/process/templates/requirement-detail.md
canon/process/templates/test-scenarios.md
```

and set `requirements` in `scripts/ledger.config.json`: `dir`, the covered `families` — the ones a
person can be *asked to exercise*, `["FR", "INV"]` by default and never the mechanism families —
the `phase_pattern` matching whatever token your requirement tables carry, and
`require_detail_for_satisfied: false`. Then `scenarios`: `dir`, the same `families`, `commands` —
the project's own command-line tools by name, from phase 5, so a scenario that asks the tester to
run one is caught — and `require_scenarios_for_reviewed_detail: false`. Fill `<DATE>` and the
owner line in both READMEs; solo, the one human is the specification's owner and the test manager
both, and the READMEs say so rather than leaving a role nobody holds.

**Solo, the scenario track waits for a second pair of hands, and `canon/qa/README.md`'s owner line
says so.** The implementer playing the demo is already `DoD-5`; a scenarios file earns its place
only when somebody who did not build the behaviour runs it. Install the skill, leave the directory
empty, and say in the hand-over that nothing is missing until that person exists.

Four things to get right, because each is a failure the track is shaped around:

- **Leave the directory free of detail files.** The area registers live there, one `index.md` per
  area, and nothing else. Four hundred requirements drafted by an agent and read by nobody is a
  directory that looks like coverage, which is worse than an empty one.
- **The quote check is the whole mechanism.** A detail file carries its requirement's words
  verbatim and `ledger.py check` compares them character for character, so an amendment to the
  register fails every file that has not been re-read. Say that in the README, and say why: two wordings of
  one requirement is two requirements, found the day they disagree.
- **It is not in the definition of done**, deliberately. Coupling a slice to the detail of every
  requirement it touches puts the approver on the critical path of every merge. The track runs one
  phase ahead of the queue instead. `DoD-12` is the one place a slice reads it, and only the
  `reviewed` files.
- **A scenario is done through the product's own screens**, and the check enforces it. Whoever
  tests has a browser and no terminal, so a scenario carrying a command is one nobody can run, and
  a file of them looks like coverage. Name the project's tools in `scenarios.commands` or the
  check cannot see them.

Then re-run `python3 scripts/ledger.py check` a final time. It must exit 0 with an empty
requirements directory and an empty scenarios directory — which is also the first thing each track
proves about itself.

### Commit the bootstrap

The generated tree is the project's first commit, and the loop assumes it is on `dev`:

```bash
rm -f .canon-interview.md                       # its content is in the documents now
git checkout -b dev 2>/dev/null || git checkout dev
git add -A
git commit -m "docs(process): bootstrap the development process"
git remote                                      # empty means no remote yet
```

**Delete the interview record rather than committing it.** It held answers so a broken session
could be resumed; the documents hold the specification. Two homes for one fact is the failure
`references/11-registers.md` is entirely about, and committing this one would start it on day
one.

Attribution on this commit follows the phase 8 answer. If there is no remote, say so in the
hand-over: `/slice-open` opens branches locally without one, but the draft pull request and the CI
gate wait until it exists.

### Hand over

Finish by reporting, in the terse mode above: whether the tree is committed on `dev` and whether
a remote exists; the tree you created, the counts (requirements
declared, slices queued — `canon/INDEX.md` carries them), what `SL-000` will do, which standing skills you installed and what
`TODO:` markers remain in the manual-test harness, whether `CLAUDE.md` carries the directive mode
and what it weighs against its budget,
and every question you left open, numbered.

**And name what each thing you did not install is waiting for**, in one line each, so a deferred
skill reads as a decision rather than as a gap. Every one of them has a prerequisite that does not
exist on day one, and saying so is what stops somebody adopting a skill before it can do anything:

| Not installed | Earns its place when |
|---|---|
| `/product-docs` | there is enough product that reading the code is slower than reading about it |
| `/security-audit` | something is deployed, or handles somebody else's data |
| `/manual-test` | a throwaway instance can actually be started — its `TODO:` markers are that gap, written down |
| `/test-scenarios` | somebody who did not build the behaviour is going to run it |
| the detail track | somebody other than its author is going to read a requirement |

Each is three files and a config value away, and none of them is harder to adopt at slice forty
than at slice zero — which is exactly why installing one before its prerequisite exists is a cost
with no return. **`/context-compact` is never on this list**: `DoD-8` adds to `CLAUDE.md` from the
first slice, so a project without the remedy ships with a file that only grows. Tell the user the first command is `/slice-open
SL-000`, and that the requirement track starts whenever they want it with
`/requirement-detail <id>` — one phase ahead of whatever the queue is building — and that
`/test-scenarios <id>` is there for the day somebody other than them runs a session, written once
the claiming work order is approved.

## After bootstrap — the loop

The process you just wrote is the record; you do not need this skill again. Each slice runs:

**pick → work order → plan → implement → gate → play by hand → close.**

`/slice-open <id>` drafts the work order, branch and draft PR. `/slice-close` drafts the summary
from the diff, regenerates the ledger, walks the definition of done, and drafts the commit.

Six skills run **outside** the loop, and are the reason the loop does not have to carry
everything: `/cleanup`, `/product-docs` and `/security-audit` on the cadences set in phase 9 —
or all four in order with `/maintenance` — `/context-compact` whenever `ledger.py check` warns that
`CLAUDE.md` is over its budget, and `/manual-test` when the suite is green and nobody
has looked at the product in three weeks — which is a state the gate cannot detect and is exactly
when this process has failed.

After launch, `/change-request` is how a requirement changes: one file with the rows to add,
amend or withdraw, decided by the owner and applied mechanically. The narrative BRD is never
edited for one.

Three more run **beside** it: `/requirement-detail <id>` writes down what one requirement means,
as the stories somebody is in, one phase ahead of the queue; `/test-scenarios <id>` turns that file
into a session somebody runs through the product's screens, once the claiming work order is
approved and once there is somebody other than the implementer to run it; and
`/requirement-verify <id>` asks at each phase gate whether the behaviour is actually there. A
requirement reading `●` in the ledger is one whose *claims* are tested, which is not the same
thing, and no slice owns the difference. The order of those documents is a cadence, not a gate —
`DEVELOPMENT-PROCESS.md` §11 says which comes first and why none waits on another.

Three things are **never** delegated to an agent, and the process document says so: writing and
approving the work order, reading the implementation plan before code is written, and playing with
the result by hand. The characteristic failure of one-person-plus-agents is velocity outrunning
comprehension — a codebase that works, that nobody understands, and that therefore cannot be
safely changed.
