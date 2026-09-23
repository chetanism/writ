---
name: adopt
description: Survey an existing codebase and put an agent-first development process around it — area registers read off the code and its history, a debt register, an enforcement perimeter that starts empty, and the fourteen project skills. Use when adding this process to a repository that already has code, especially one other people are still working in.
disable-model-invocation: true
---

# Writ — adopt

You are putting a development process around a codebase that already exists and already works.
The output is a `writ/` tree, a survey, a perimeter that enforces nothing yet, and the fourteen
project skills.

> **Read this first if you are not sure which skill to run.** `/writ:solo` and `/writ:team`
> interview a project that has no code into existence. This one is the opposite problem: the code
> is the most reliable document in the room, and your job is to write down what it cannot say
> about itself. If the repository has no code yet, stop and run one of those instead — everything
> below is shaped around evidence that does not exist for a greenfield project.

## The two things that make this different from a bootstrap

**1. You are not deciding requirements. You are recovering them, and some of what you recover is
wrong.** A requirement read off working code describes what happens, which includes every bug old
enough that somebody now depends on it. That is why rows carry `Provenance`, why `writ/spec/debt.md`
is filled before the requirement registers, and why you must never quietly promote a defect to a
requirement because it was easier than asking.

**2. You are almost certainly not the only person committing to this repository.** Assume you are
one of five until told otherwise. Every rule this process can enforce starts **off**, and the
perimeter is how it gets turned on later, one path at a time, by somebody who decided to. A gate
that rejects a colleague's pull request for a rule that arrived in a commit they never read is how
this process gets deleted in a week — and being right about the rule does not save it.

Everything else — the declaration rule, the ledger that disbelieves its inputs, acceptance criteria
as test names, every slice demonstrated by hand — is exactly as `/writ:solo` describes it. Read
that skill's *What you are building* section if you have not.

## How you report while running this

The same mode as the other two: the survey is a conversation and reads like one; everything that
is not a question is terse. Bullets and fragments, conclusion first, numbered asks,
never print a file back, one line per fact. `references/07-authoring-style.md` carries the rule.

**One extra discipline here.** You will be reading things off code and history and saying them
back. **Label every one of them as a guess until the user confirms it.** A survey finding stated
in the same voice as a fact the user gave you is how an invented requirement gets into a register
and is never caught again.

## The phases

**The kit root is `${CLAUDE_PLUGIN_ROOT}`**, and every `references/…`, `templates/…` and `skills/…`
path below is relative to it. If that variable reads as literal text, the skill was loaded outside
the plugin and the kit root is two directories above this file.

**`.writ-interview.md` at the target root** works exactly as it does in `/writ:solo`: append a
section at the end of every phase, resume from it if one is there, delete it at the commit.
`references/00-interview.md` §*Surviving the session* is the rule. It matters more here — the
survey is longer than an interview, and its findings are expensive to reproduce.

Load `references/00-interview.md`, `references/12-survey.md` and `references/13-adoption.md`
**now**. The first governs how you ask; the second two are what this skill is.

### Phase 0 — Orient, and find out who else is here

- **Look for `.writ-interview.md`** and offer to resume. As `/writ:solo` phase 0.
- Establish the target directory and confirm it is a git repository. **If there is no history,
  stop** — you are in the wrong skill.
- **Ask what to call the tree.** Default `writ/`; any single lowercase segment that does not
  already exist. Not `docs/`. Phase 8 rewrites the paths if the answer differs.
- If `<writ>/spec/` already exists, **stop and report what is there.** Offer to adopt around it.
- **Check the fourteen skill names against what is already there**, and handle collisions exactly as
  `/writ:solo` phase 0 does — `.claude/skills/<name>/` and `.claude/commands/<name>.md`, in the
  target and under `~/.claude/`. Prefixing the whole set with `writ-` is the default.
- **Then the question that shapes everything else.** One `AskUserQuestion`, and do not skip it
  because the answer seems obvious:

  1. **How many people commit to this repository?** Not how many will use this process — how many
     push code.
  2. **How many of them have agreed to use it?** The honest answer on day one is usually *one*.
  3. **Is there a branch protection rule or a required check today?** If yes, adding to it is a
     conversation with the whole team, not a config change.

  Say why you are asking: the answers set the perimeter, and the perimeter is the difference
  between a gate and a grievance. **If more than one person commits and only one has agreed, say
  plainly that you will install solo mode with every rule off**, and that
  `references/13-adoption.md` §*The ladder* is how it turns on later.

- Confirm the target, the project name and the number of hands back in one line.

### Phase 1 — Run the survey

Copy `templates/scripts/survey.py` to `scripts/survey.py` and run it:

```bash
python3 scripts/survey.py --since 24
```

**Read it back to the user section by section, and treat every line as a question.** None of it is
a finding. `references/12-survey.md` has what each section is for; the short version:

- **Areas** → are these the requirement areas, and what are they called?
- **Hotspots** → what keeps bringing people back to this file?
- **Coupled** → what rule holds these two together? *This is where invariants come from.*
- **Quiet** → is this dead? Only a person can tell you.
- **One pair of hands** → who do you interview, and who joins the process second?

If the repository is younger than the window or the window is empty, widen `--since` and say so.

**Then read the existing tests, before you read any source.** Test names and describe blocks are a
requirements document somebody already wrote, in the words of the person who built the thing, and
they are far closer to intent than the implementation is. Say back what you found as candidate
rows.

Produce, in your reply, a one-screen restatement: what this system appears to be, who appears to
use it, what the areas are, and **what you are guessing**. The guesses are phase 2's agenda.

### Phase 2 — The interview the survey earned

Rounds of questions, at most four per `AskUserQuestion`, numbered, coarse to fine.

Unlike a bootstrap you are not building a product from nothing, so the bank is different. Work
through, in order:

1. **The area map.** Confirm, rename, merge, split. These become the register directories.
2. **What is live and what is not.** Of the quiet files: dead, stable, or nobody knows? *Nobody
   knows* is a real answer and becomes a `Q-NNN` row.
3. **The load-bearing parts.** What would you never let a new joiner change without asking?
4. **The scars.** What has broken in production? Each answer is either an invariant or a debt row.
5. **What is wrong.** Straight out: what in here do you know is bad? Write every answer into
   `writ/spec/debt.md`. **Ask this before you ask what the requirements are** — a user who has
   been invited to say what is broken gives far better requirements afterwards than one who thinks
   they are being asked to defend the codebase.
6. **What is actually being built next.** This decides which areas get tier-two documentation, and
   it is the only thing that does.

**The stop rule is different here, and it is narrower.** Greenfield you keep going until you could
write every requirement table. Here you stop when you can write **the map** — areas, invariants,
debt, and the areas the next three months will touch. *You are not documenting the whole codebase
in this sitting.* Say that out loud, because a user expecting the full description will read a
correct stopping point as an unfinished job.

### Phase 3 — Security, against what is already deployed

Load `references/02-security.md` and identify the domain profile, as `/writ:solo` does. Two
differences, both of which make this phase more urgent rather than less:

- **The questions are in the past tense.** Not *what will the tenancy boundary be* but *what is it,
  and where is it enforced, and has anybody checked?* An inherited boundary is an assertion with
  an unknown truth value.
- **Anything you cannot confirm is a `Q-NNN` row or a `DEBT-NNN` row, never an `INV-*`.** An
  invariant the code may already violate, declared as though it holds, is worse than no invariant:
  it will be cited in a review as though something enforces it.

If the system is deployed and handles anybody else's data, say plainly that `/security-audit` is a
day-one skill here rather than a later one. That is the reverse of the greenfield advice, and the
reason is simply that there is already something to audit.

### Phase 4 — Robustness, from what is observable now

Load `references/03-reliability.md`. Ground every question in the running system: what does it do
under load *today*, what has actually fallen over, what is monitored, what is not.

**Refuse to write a number the user did not give you.** An SLO invented for an existing service is
worse than one invented for a new one, because somebody will compare it to reality and conclude
the specification is fiction. *We do not know* is a `Q-NNN` row and a perfectly good answer.

### Phase 5 — The stack and the gate, verified by running it

Ask the stack, then fill every gate role — format, static analysis, types, affected, unit, integration,
contract, traceability — as `/writ:solo` phase 5 does.

**Then run each command.** Not "is it in the README" — run it, and record what actually happened.
This is the phase that most often finds the first `DEBT-NNN` row: the test suite that has been
failing for two months, the lint config nobody can pass, the integration tests that need a service
nobody can start. A gate role whose command does not pass today is recorded as debt and its role
is marked as not in force, which is honest. **Never write a gate command into the process document
without having watched it run.**

Then load exactly one of `references/stacks/*.md` and follow it.

### Phase 6 — Write the specification set

Load `references/11-registers.md` and `references/12-survey.md`. Copy each template from the kit's
`templates/<path>` and fill it. Delete every guidance blockquote; leave no `<PLACEHOLDER>`.

Order matters, and **it is not the greenfield order** — debt comes before requirements:

1. `writ/spec/debt.md` — every answer from phase 2's fifth question, one row each. **Fill this
   first.** It is what makes the rest honest, and a specification that reads as though the
   codebase were clean is one the team knows to be false on day one.
2. `writ/spec/BRD.md` — the case for the product, in prose, in the past tense where it has to be.
   It declares nothing. Where you do not know why something was built, say so rather than inventing
   a rationale.
3. The area registers, `writ/spec/requirements/<AREA>/index.md`, **carrying a `Provenance`
   column**: `decided` for anything the user stated in phase 2, `observed` for anything you read
   off code or tests. Be strict about the difference. Only write rows for the areas phase 2's
   sixth question named — the rest ship as an empty register with a line of prose saying it has
   not been surveyed yet, which is a true statement and an obvious prompt.
4. `invariants.md` — from the coupled pairs, the scars and the load-bearing answers. **Mark any
   you could not confirm as unverified in the Status cell**, and say in the hand-over that a
   characterisation slice is what settles one.
5. The rest of the registers: `compliance.md`, `strategic-decisions.md`, `personas.md`,
   `milestones.md`, `dependencies.md`, `risks.md`, `assumptions.md`, `out-of-scope.md`,
   `questions.md`. Every row `Since: v0` — there was no `v0.1`, the history is in git, and
   pretending this specification predates the code is the one lie that would undermine all of it.
6. `writ/spec/ID-REGISTRY.md` — a row per family used, including `DEBT`.
7. `writ/spec/MILESTONE-PLAN.md` — what the *next* milestone builds. Not a retrospective plan for
   what already exists.
8. `writ/spec/CHANGELOG.md` — the seed row, dated today, touching `v0`.

Then list what you wrote under `registers` and `narrative` in `scripts/ledger.config.json`.

### Phase 7 — Slice, starting with the two slices adoption always needs

Load `references/04-slicing.md` and ask for the slicing criteria, as `/writ:solo` does. Then cut
the next milestone's slices from the milestone plan.

**Two kinds of slice exist here that do not exist greenfield, and both go at the front of the
queue.** `references/13-adoption.md` has the detail:

- **The annotation harvest.** One slice per area, mechanical: put `[<ID>]` at the front of the
  test names that already prove something. No behaviour changes, nothing is corrected while
  annotating — a harvest that also fixes things is one nobody can review. This is the highest-return
  work in the whole adoption, and it is what turns a ledger reading zero into an instrument.
- **Characterisation slices**, `kind: characterisation`, for rows the harvest leaves `≈` — and for
  every invariant you marked unverified. They pin existing behaviour and change none of it, and
  they are the only slices that may declare `demo: none`. Their Demo section says what was pinned
  and **who confirmed it was wanted** — a test written from the code asserts the bug exactly as
  confidently as the feature.

Everything else follows the ordinary rules: dependency order, one work order each under
`<milestone>/<phase>/`, sized against the budget.

### Phase 8 — Emit the process, with every rule off

Copy the remaining templates exactly as `/writ:solo` phase 8 does — `DEVELOPMENT-PROCESS.md`,
`RATIONALE.md`, `SLICE-QUEUE.md`, `MANUAL-REGRESSION.md`, both `writ/process/templates/`, `writ/decisions/`,
`CLAUDE.md`, `.github/workflows/`, `.claude/skills/slice-open`, `slice-close`, `test-all`, `change-request`,
`process-change`,
and `scripts/` — including `survey.py` and `test_survey.py`, which stay in the project.

Apply the tree rename and any skill rename table from phase 0, in that step, exactly as
`/writ:solo` describes.

**Then the one setting this whole skill exists for.** In `scripts/ledger.config.json`:

```json
"enforce": { "default": [], "annotations": null, "work_order": null }
```

**An empty default. Every rule off.** Write it that way even when the user says they are the only
committer, and tell them what you did and why: the first perimeter is widened by somebody who
decided to widen it, and a process that arrives already enforcing is one that arrives as an
imposition. `references/13-adoption.md` §*The ladder* is the sequence, and the hand-over names the
next rung.

**Three questions here, in one `AskUserQuestion`**, and they are the same three `/writ:solo`
asks: attribution, reply mode, and the tracker. Handle each exactly as that skill does — the
answers land in the same places and a half-applied one is worse than either extreme.

Then run it:

```bash
python3 scripts/test_ledger.py     # the tool's own suite
python3 scripts/test_survey.py     # the survey tool's suite
python3 scripts/ledger.py          # write COVERAGE.md, INDEX.md and the queue block
python3 scripts/ledger.py check    # must exit 0
python3 scripts/ledger.py stats    # read the Adoption block out loud
```

`check` must exit 0. `stats` will show a large inherited count, a large observed count, and a
perimeter enforcing nothing — **that is the correct day-one reading**, and saying so matters,
because it looks like failure to somebody who expected a bootstrap.

### Phase 9 — The standing skills

Load `references/09-standing-skills.md` and proceed as `/writ:solo` phase 9. One difference in the
advice, and it runs the opposite way:

**On an existing codebase most of the standing skills have already earned their place.** The
greenfield argument for deferring them is that their prerequisite does not exist yet — there is no
product to document, nothing deployed to audit, no instance to walk. Here there usually is. Say so
rather than repeating the greenfield default:

| Pass | Greenfield | Here |
|---|---|---|
| `/security-audit` | wait until something is deployed | **install it** if anything is deployed or holds somebody else's data |
| `/product-docs` | wait until there is enough product | **install it** if reading the code is already slower than reading about it |
| `/manual-test` | wait until an instance can be started | **install it** if one can be started today — and its `TODO:` markers are real gaps, not placeholders |
| `/cleanup` | on a cadence | **install it**, and expect its first pass to be large |

`/context-compact` is never declinable, here as anywhere.

### Phase 10 — The requirement detail track

Load `references/10-requirements.md` and ask the one question: install the track, or defer it.

**Recommend installing it**, which is the opposite of the greenfield default, and the reason is
specific: `/requirement-detail` on an `observed` row is the mechanism that promotes it to
`decided`. That is not a nicety here — it is the only thing standing between a recovered
specification and a document that has quietly enshrined every long-standing bug. Say exactly that
when you ask.

Emit the three skills and two directories, and set `requirements` and `scenarios` in
`scripts/ledger.config.json` as `/writ:solo` phase 10 describes, with **`out_of_order: "backfill"`**
and `require_scenarios_for_reviewed_detail: false`. An adopted codebase is the order broken by
definition — the code came first, and its requirements are written afterwards — so every inherited
requirement is built ahead of its detail. `backfill` makes that a queue in `COVERAGE.md`, most urgent
first, rather than a failing build (`DEVELOPMENT-PROCESS.md` §12.1). It fails only a requirement that
slips after it was caught up, and a milestone marked `done` before its requirements are. `fail` on a
hundred inherited requirements would fail the build for work nobody has been asked for.

Say one thing about the backfill when you ask: **`/requirement-detail` on a built requirement reads
the build as evidence and never as authority.** Every story it drafts from the code is put to the
owner to ratify, and anything the owner does not take is a `fix` or a change request. That is how
an `observed` row becomes `decided` without enshrining the bug that happens to be in it.

**Leave the requirements directory free of detail files.** Only the area `index.md` registers. A
hundred detail files drafted by an agent and read by nobody is a directory that looks like
coverage, which on a brownfield project is worse than an empty one — it will be believed.

### Commit the adoption

```bash
rm -f .writ-interview.md
git checkout -b docs/adopt-writ
git add -A
git commit -m "docs(process): adopt the development process"
```

**Not on `dev`, and not on `main`.** Greenfield the bootstrap *is* the first commit, so it commits
to `dev` directly. Here other people are working, and a hundred new files appearing on the shared
branch without a pull request is the first impression this process makes. Open it as a pull
request, and say in the description what it does and does not turn on.

Attribution follows the phase 8 answer.

### Hand over

Report in the terse mode: what you created and where; the survey's headline numbers; the counts
from `stats` — inherited, observed, and the perimeter enforcing nothing; which standing skills you
installed; what `TODO:` markers remain; and every question you left open, numbered.

**Then the three things that decide whether this is still in use in three months**, said plainly:

1. **Nothing is enforced.** The perimeter is empty, on purpose. Nobody else's pull request can
   fail because of anything you just installed.
2. **The next rung is the annotation harvest**, not turning a gate on. It is mechanical, it is
   safe, and it is what makes the ledger worth reading. Name the first area to do.
3. **Do not turn on the `work_order` perimeter until a second person has run a slice.** Give the
   reason: until then this is one person's process, and a gate that only its author understands
   blocks everyone and dies the week they are away.

Then the table of what is not installed and what each is waiting for, as `/writ:solo` does — and
name the areas left unsurveyed, with the same framing. **An unsurveyed area is a decision, not a
gap**: it gets documented by the first slice that touches it, which is the whole design.

Tell the user the first command is `/slice-open` on the first harvest slice, and that
`python3 scripts/ledger.py stats` is the instrument for whether any of this is taking.

## After adoption — the loop

The same loop as everywhere else: **pick → work order → plan → implement → gate → play by hand →
close.** `references/13-adoption.md` is the document to re-read when it is time to climb a rung —
it holds the ladder, the perimeter and the three things that decay.

Two habits are specific to a codebase that predates its process, and neither is enforced by
anything:

- **Document the area the slice touches, as part of the slice**, before changing it. Not in
  advance, and not afterwards. This is what makes tier two affordable, and it is the reason the
  registers do not have to be filled in up front.
- **Read `debt.md` for the area before planning.** It is the cheapest thing in the tree and it is
  the record of every afternoon somebody already lost.
