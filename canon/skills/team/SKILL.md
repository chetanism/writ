---
name: team
description: Interview a team and generate their project's agent-first development process with named roles, handoffs, WIP limits and CODEOWNERS on top of the solo kit. Use when starting a project that more than one person will build.
disable-model-invocation: true
---

# Canon — team

You are setting up a development process for a project several people will build in parallel, each
with coding agents. The output is a `canon/` tree, a CI gate, a traceability tool, and — the part
that is only in this skill — **a pipeline with named roles and explicit handoffs**.

> **If exactly one human will make every decision, stop and use `/canon:solo`.** It is the same
> process with the handoffs removed, and the ceremony here would be pure cost. Ask if you do not
> know.

## What is different when there is more than one of you

A solo build can hold the whole specification in one head, so its only real risk is velocity
outrunning comprehension. A team has two more:

- **Two people building the same thing differently.** The defence is that requirements are
  declared once, in one document, under one identifier — and that two slices touching the same
  surface cannot be in flight at once.
- **A handoff with no definition of ready.** Someone starts implementing against requirements that
  are still being edited. The defence is that every artefact has an owner and a stated point at
  which it is safe to build on.

Everything else — the declaration rule, the disbelieving ledger, criteria-as-test-names, the
by-hand demo — is identical to the solo process, and the reasoning for it is in
`skills/solo/SKILL.md`. Read that file's *"What you are building"* section; it is not
repeated here.

## How you report while running this

As solo — `skills/solo/SKILL.md`'s *How you report while running this*, and it applies
unchanged: questions read like a conversation, everything else is bullets and fragments,
conclusion first, asks numbered, nothing printed back.

One addition with more than one person in the room: **name who each ask is for.** `[ASK 2 — slicer]`
is answerable; an unaddressed question in a group conversation is answered by whoever is least busy,
which is rarely the person who knows.

## The phases

The kit root is `${CLAUDE_PLUGIN_ROOT}`, and every `references/…`, `templates/…` and `skills/…`
path here is relative to it, exactly as the solo skill describes.

Load `references/00-interview.md` first; it governs how you ask everything below. Write no files
before phase 6 — with one exception, `.canon-interview.md` at the target root, appended after every
phase and deleted at the commit. On a team it earns its place twice over: the interview spans more
than one sitting because it spans more than one person's calendar, and a phase answered while the
slicer was in a meeting is a phase somebody has to be able to pick up. `references/00-interview.md`
§*Surviving the session* is the rule.

### Phase 0 — Orient

As solo: **look for `.canon-interview.md` and offer to resume from it**, establish the target
directory, ask what to call the tree (default `canon/`, and never
`docs/`), refuse to overwrite an existing `<canon>/spec/`, check the twelve skill names for
collisions and ask once if any — prefix all with `canon-`, or name the colliding ones — and
confirm the project name. Additionally, ask **how many people** will build this and whether they
are in one timezone. Both change the answers in phase 3. Where the tree or any skill is renamed,
phase 8's rewrite step applies as solo, and `.github/CODEOWNERS` is written against the chosen
names. On a team, check the collision under the account running the bootstrap and say that a
teammate's `~/.claude/` may hold others — the project-level names are the ones that can be checked
here, and the ones that matter.

### Phase 1 — Obtain the BRD

As solo. Accept anything from two paragraphs to a finished spec, restate it in one screen, and name
your guesses.

**One addition:** ask who wrote it and who is allowed to change it. That person is the BRD owner in
phase 3, and if the answer is "several of us" you have found the first thing to fix.

### Phase 2 — Adaptive scoping

As solo — rounds of at most four numbered questions, coarse to fine, calibrated to how complete the
BRD is. Same stop rule: continue until every requirement table can be written without inventing a
fact.

**One addition:** when contributors disagree in the room, do not average the answers. Record both
positions as an open question with a named decider and a date, and carry on.

### Phase 3 — Roles and handoffs

This phase replaces the solo skill's security phase in the running order; security is phase 3b
below and is not skipped.

Load `references/08-team-pipeline.md`. Establish, by asking:

| Role | Owns | Question to ask |
|---|---|---|
| **BRD owner** | The registers under `canon/spec/`, and `BRD.md` — scope, targets, and every change request | Who decides what is in and out? |
| **Requirements author** | requirement IDs, foundation specs | Who turns an agreed scope into numbered, testable requirements? |
| **Slicer** | the queue, work orders, sizing | Who decides what the next slice is and how big it may be? |
| **Implementer** | code and tests, one slice at a time | Who builds? How many at once? |
| **Plan reviewer** | reads the plan before code exists | Who reads it — and is it ever the author? |
| **Player** | runs the demo by hand at close | Who runs it — and is it ever the implementer? |

One person may hold several roles; two people may not hold one. Say that out loud.

Then design the **handoff contract** — for each arrow, what "ready" means:

```
BRD frozen at a version  →  requirement IDs may be declared
requirements declared    →  slices may be cut
work order approved      →  a branch may be opened
plan read by a reviewer  →  implementation may begin
gate green + demo played →  the slice may merge
```

**Read every role and every handoff back to the user and get each confirmed explicitly before you
write anything.** A pipeline nobody agreed to is a pipeline that gets routed around in week two.

Finally, ask for two numbers: the **WIP limit** (how many slices may be in flight at once — the
default is one per implementer) and whether a plan reviewer must be someone other than the author
(the default is yes).

### Phase 3b — Security, conditioned on the domain

Exactly as `/canon:solo` phase 3. Load `references/02-security.md`, pick the domain profile, ask
only that profile's questions, and turn the answers into `FR-SEC-*` and `INV-*`.

Ask one extra question: **who is allowed to approve a change to an invariant?** On a team, an
invariant with no named owner is a suggestion.

### Phase 4 — Robustness, reliability, scalability

Exactly as `/canon:solo` phase 4. Load `references/03-reliability.md`. Refuse to invent a number
the user did not give you; record it as an open question with a decider instead.

### Phase 5 — Stack and gate roles

Exactly as `/canon:solo` phase 5 — fill every gate role with a concrete command, then load one
`references/stacks/*.md`.

**One addition:** on a team the gate must be a **required status check**, and the branch-protection
settings are part of the deliverable. Note the trap in `references/06-gate.md`: a workflow skipped
by `paths-ignore` reports no status at all, so a docs-only pull request blocks forever unless a
second always-running job reports success.

### Phase 6 — Write the specification set

As solo: the narrative `BRD.md`, then the registers one file each, then `ID-REGISTRY.md`, then
`MILESTONE-PLAN.md` with ordinal phases, then one foundation spec per inherited shape, then the
changelog's seed row. Delete guidance blockquotes; leave no placeholders and no example
identifier.

**One addition:** every document's front matter names its **owner**, and `canon/spec/` gets a
`CODEOWNERS` entry naming that person. A specification anyone may edit silently is a specification
nobody can rely on.

### Phase 7 — Slice, with parallelism in mind

Load `references/04-slicing.md`, ask for the slicing criteria, and cut the slices — then do the
part that is only in this skill.

Every work order's front matter carries, beyond the solo fields:

- `owner:` — who is building it, or empty while it is queued;
- `status:` — `queued` · `in-progress` · `in-review` · `done` · `blocked`;
- `touches:` — the shared surfaces it changes. Name them concretely and consistently: a schema
  (`schema/accounts`), a route group (`api/v1/orders`), a module, a config file. This list is what
  makes conflicts detectable before they are merge conflicts.

`scripts/ledger.py check` then refuses two active slices that share a `touches` entry, and refuses
more active slices than the WIP limit. Set both in `scripts/ledger.config.json`
(`"mode": "team"`, `"wip_limit": <n>`).

Order by `depends_on` as in the solo process, and **confirm the resulting order with the slicer**
before generating the queue. The generated table carries the owner column in team mode, so the
queue doubles as the board.

`references/04-slicing.md` also carries **the conflict read** — `DoD-12`, the step that asks whether
a plan would make a requirement *false* rather than which ones it advances. On a team it has a
named escalation: the conflict goes to **the slicer**, not to whoever drafted the work order, and
`touches:` is exactly the list that says which invariants to read it against. It lands in the
definition of done, in `/slice-open`'s step 2a, and in `CLAUDE.md` — all three, written in phase 8.

### Phase 8 — Emit the process

As solo, plus:

- `DEVELOPMENT-PROCESS.md` gains the roles table, the handoff contract, and definition-of-done rows
  for *plan reviewed by someone other than the author* and *demo played by someone other than the
  implementer*.
- `.github/CODEOWNERS` — `canon/spec/` to the BRD owner, `canon/decisions/` to whoever approves
  invariants, `canon/process/` to the slicer.

**And the three questions phase 8 asks**, as solo, in one call. First, attribution — the agent's
co-author trailer kept or forbidden — put to whoever owns the repository's history rules, because
on a team it is usually a policy rather than a taste. Second: does `CLAUDE.md` carry the *Talking to me* section
— the directive mode, bullets and fragments and numbered asks — or the agent's usual voice? On a
team, put it to the people who will actually read the agent's output rather than to whoever is
running the bootstrap; the mode is cheapest for one person at a terminal all day and costs the most
for a reader catching up on somebody else's session. **Emit it whole or delete it whole.**
`references/07-authoring-style.md` carries the section and the argument. Third, the tracker — an
issue per claimed slice, GitHub or none — put to whoever owns the board, with one thing said
beside the answer: the issue mirrors the work order and is never where a claim is made. The claim
is the `status: in-progress` commit, and the generated queue is the board; the issue is what the
people who do not read the repository see, and `references/08-team-pipeline.md` says why that
order matters.

Then run it:

```bash
python3 scripts/test_ledger.py
python3 scripts/ledger.py
python3 scripts/ledger.py check    # must exit 0
```

### Phase 9 — The standing skills

As solo — load `references/09-standing-skills.md`, ask the four remaining questions in one call, and
emit the four passes, `/maintenance`, `/manual-test` and `canon/maintenance/`. Then three
things that only matter with more than one person:

- **A maintenance pass is one person's, and it is announced.** It takes the whole repository —
  cleanup rewrites across the diff, documentation regenerates from the code, the audit reads what
  both left behind, the compaction rewrites the file every session starts from — so it does not
  compose with slices landing underneath it. Say in
  `SKILL.md`'s delivery loop who runs it and how the team knows one is running.
- **A maintenance pull request consumes no WIP slot.** It closes no issue and implements no slice.
  Record that in `DEVELOPMENT-PROCESS.md` beside the WIP limit, or the first pass will look like
  somebody breaking it.
- **`.github/CODEOWNERS` gains `canon/maintenance/`** — to whoever owns the security backlog,
  because the *Accepted risks* table is the one thing in this process an audit may not decide for
  itself. It is accepted by a named person on a date, and CODEOWNERS is what makes that true in
  review rather than in prose.

Then re-run `python3 scripts/ledger.py check`. It must still exit 0 with the new documents present.

### Phase 10 — The requirement detail track

Load `references/10-requirements.md`, and emit as solo: the three skills, the two process READMEs,
the detail and scenario templates, and the `requirements` and `scenarios` blocks in
`scripts/ledger.config.json`. Both directories ship **empty** but for their READMEs.

Four things are only decidable with more than one person, and they are the reason this phase is not
identical to solo's:

- **Name the drafter and the approver separately in the README's role table**, and prefer that they
  are not the same person. Solo, the agent drafts and the one human approves; on a team, approval is
  a second reader's, which is the stronger form of the same thing. Record it as names, not roles
  nobody answers to.
- **A detail file is a pull request like any other**, into the integration branch, and it consumes
  no WIP slot — it implements no slice and closes no issue. Say so beside the WIP limit, or the
  first one will look like somebody breaking it.
- **`.github/CODEOWNERS` gains `canon/spec/requirements/`** — to the approver, **on a line after
  the `canon/spec/` one**: the last matching pattern wins, so a requirements rule placed above the
  specification's is silently overridden by it. The whole track turns on somebody having actually
  read the file, and CODEOWNERS is what makes that true in review rather than in prose.
- **Name the test manager**, in `canon/qa/README.md`'s owner line and in `DEVELOPMENT-PROCESS.md`'s
  role table, and give `canon/qa/` to them in CODEOWNERS. Which scenarios are worth a session is a
  cut somebody has to make, and a file nobody cut is a file nobody runs. Prefer that it is not the
  specification's owner: what a requirement means and what a session covers are two arguments,
  and one person holding both is how the second quietly reopens the first.

Say plainly what the track is **not**: it is not in the definition of done, deliberately, because
coupling a slice to the detail of every requirement it touches puts the approver on the critical
path of every merge — which is the serial process this whole design replaces. It runs one phase
ahead of the queue instead. `DoD-12` is the one place a slice reads it, and only the `reviewed`
files.

Then re-run `python3 scripts/ledger.py check` a final time. It must exit 0 with an empty
requirements directory and an empty scenarios directory.

### Commit the bootstrap

As solo: `.canon-interview.md` deleted, `dev` created or checked out, the whole tree committed
with `docs(process): bootstrap the development process`, and the hand-over says whether a remote
exists. On a team the remote almost
always does; if it does not, branch protection cannot be set and the roles are not yet enforced by
anything, and the hand-over says that too.

### Hand over

Finish by reporting, in the terse mode above: the commit on `dev`, the tree, the counts, the confirmed roles and
handoffs, the WIP limit, what `SL-000` will do, what `CLAUDE.md` weighs against its budget, which standing skills you installed and what
`TODO:` markers remain in the manual-test harness, whether `CLAUDE.md` carries the directive mode,
who drafts and who approves a requirement detail file, who the test manager is, and every open
question with its named decider. Tell the team the first command is `/slice-open SL-000`, and that
it is one person's slice — the process is bootstrapped once, by one person, and reviewed by the
rest. The requirement track starts in parallel, one phase ahead of the queue, with
`/requirement-detail <id>`, and `/test-scenarios <id>` follows each approved work order.

## After bootstrap — the loop

Per slice: **pick → work order → plan → implement → gate → play → close**, with the plan read by
someone who did not write it and the demo run by someone who did not implement it.

`/slice-open <id>` and `/slice-close` draft the ceremony. They remove the friction, not the
judgement.

Outside the loop, on the cadences set in phase 9: `/cleanup`, `/product-docs` and
`/security-audit`, each run by one person and announced — or all four in order with
`/maintenance` — `/context-compact` whenever `ledger.py check` warns that `CLAUDE.md` is over its
budget, which on a team is more often, because every engineer's slices add to it and none of them
sees the file grow; and `/manual-test`, which is worth giving to somebody who did **not** build the
area it walks. The security audit is worth giving to whoever owns the security backlog, which is
why it is a skill of its own.

Beside the loop: `/requirement-detail <id>` one phase ahead of the queue, `/test-scenarios <id>`
once the claiming work order is approved, and `/requirement-verify <id>` at each phase gate, after
the scenarios that turned `Ready` have been run. None consumes a WIP slot, and none blocks a merge
— that is the property that keeps them parallel rather than serial. `DEVELOPMENT-PROCESS.md` §11
carries the order as a cadence, and `/slice-open` reports where each claimed requirement stands in
it without gating on any of it.

Three things are never delegated to an agent: writing and approving the work order, reading the
plan before code is written, and playing with the result by hand. On a team, add a fourth — nobody
reviews their own slice.
