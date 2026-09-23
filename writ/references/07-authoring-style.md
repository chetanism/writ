# How the committed documents are written

Terseness governs *replies*. It does not govern artefacts. A specification, an ADR, a work order or
a slice summary is a document, and it follows the rules here.

## The directive mode — what governs replies

**Offer it; do not assume it.** One question at the phase that writes `CLAUDE.md`: does this project
want the directive mode, or the usual voice? Both are defensible. The directive mode suits somebody
who reads a terminal all day and treats a paragraph of preamble as a tax; the usual voice suits
somebody who wants to be walked through the reasoning, and a project where more than one person
reads the agent's output. **A half-applied interaction rule is worse than either**, because the
reader cannot tell which replies were meant to follow it — so the section goes into `CLAUDE.md`
whole, or not at all.

Where it is chosen, this is the section, and it is `CLAUDE.md`'s, not this file's:

- **One reader, eyeballing a terminal. Terseness is a correctness requirement** — never spend 100
  tokens where 50 will do. Final output only: no preamble, recap, closing summary, restatement of
  the question, or narration of what is about to happen.
- **Bullets and fragments. Not prose, not sentences.**
- **Group under `IMPORTANT` / `NOTE` / `FYI` / `ASK`** — only the groups a reply needs.
- **Tag by direction, and get the verb right.** Past tense is what the agent did (`[FIXED]`,
  `[ADDED]`, `[DROPPED]`); imperative is what the reader must do (`[FIX]`, `[CHECK]`, `[DECIDE]`).
  Using one for the other is the failure this rule exists to catch: a reader who cannot tell a
  report from an instruction has to re-read every line.
- **Every ask takes the shape of `CLAUDE.md`'s *Asking me to decide*** — numbered, options lettered,
  each option's consequence and why it is or is not recommended, exactly one recommended, and the
  context to answer it without opening a file. That section is emitted whichever voice is chosen;
  the directive mode only makes it terser.
- **Conclusion first; rationale only when asked. File refs as `path:line`.** Never quote a diff
  back or re-show what was just written.
- **A recommendation names what was read.** A library, tool or convention proposed without checking
  what the repository and its neighbours already use is a prior dressed as a finding — label it
  unverified, or go and look.

**Documents obey it too**, in the only sense that transfers: every line earns its place. They keep
their templates and their prose; what the mode removes from a document is the sentence that repeats
the one above it. A document is read far more often than it is written.

## `CLAUDE.md` is the one document with a budget

Every other document here is read when somebody needs it. The agent map is read at the start of
every session, so a line added to it is paid for on every task the project ever runs — and
`DoD-8` adds one whenever a slice establishes a convention. Left alone, that is a document that
only grows, and the growth lands on the one file whose whole value is being read in full.

- **The test for a line is whether an agent would write the wrong code without it**, on a task that
  never opens the document it came from. Everything else is reference, and belongs in `writ/` or in
  the skill that needs it, with a pointer here.
- **One line per rule, and it replaces what it supersedes.** The example, the counter-example and
  the history go in the document the line points at.
- **Never restate what `writ/` already says.** Two wordings of one rule is two rules.
- `scripts/ledger.py` measures it against `context_budget` and warns; `/context-compact` moves
  sections out and leaves the pointer. **Deleting a fact is never how the file gets shorter.**

The file's own *What belongs in this file* section carries these rules, so the agent editing it
reads them without being told to. That is deliberate: a budget stated only in a reference nobody
loads is a budget nobody keeps.

## Voice

**Write for a person who has not read the rest of the tree** — a new teammate, a product owner, a
tester. The work orders, slice summaries, requirement detail files and test scenarios are read by
people who do not live in the process, and a document that needs a glossary to follow has failed
its reader before it starts.

- **Plain words first.** Say what a thing *does* before using its name: "the list of requirements
  for this area" before "the register". Where a process term has to stay — slice, invariant, ADR —
  it is explained once, in the glossary, and never coined anew in a template.
- **Short sentences, present tense.** "Public identifiers are prefixed" — not "we will probably use".
- **One bold opening sentence per idea**, then the detail. A reader skimming the bold text should get
  the point.
- **No hedging in a decision.** If it is genuinely uncertain, it is an open question, not softened
  wording.
- **Guidance in a template is a short note, not an essay.** Open with *What this is:* in one or two
  sentences, then only the rules a writer would otherwise get wrong. The reasoning behind a rule
  lives in `DEVELOPMENT-PROCESS.md` or `RATIONALE.md`, not in every copy of the template.
- **Name the entry point.** Three sentences and a file path beat a diagram.

## Every document opens the same way

A blockquote before the first heading, with the same clauses:

```markdown
> **Status:** active. This is *how* we build. The registers are *what*; BRD.md is *why*.
> **Precedence:** the registers > BRD.md > MILESTONE-PLAN.md > SLICE-QUEUE.md > this document.
>   Where this conflicts with any of them, they win and this gets corrected.
> **Divergence:** a departure from the milestone plan is one line in CHANGELOG.md **and** the
>   affected table amended in the same change.
```

**State the precedence order identically in every document that participates in it.** A total
order stated in one place is a fact; stated differently in two places it is a dispute.

**Every document says what it is *not*.** The manual-regression file is not an archive of every
demo script; the registry is not a list of identifiers; the ledger is not hand-edited.

## Divergence is amendable, never silent

Reality departs from the plan constantly, and that is fine. What is not fine is the plan quietly
disagreeing with the queue. One changelog for the repository, `spec/CHANGELOG.md`, with a line per
departure whatever document it departed from — and **the affected table is amended in the same
change**. The line is a line: what changed, touching which identifiers, and where the reasoning
lives. An unrecorded divergence is a defect, not a shortcut, and a reasoned essay in a changelog
cell is the other way the log stops being read.

## Document the process's own failures inside it

This is the habit that makes the documents worth reading. Three examples from a real project:

- *"Fifteen of the first eighteen slices exceeded the size budget. A rule broken five times out of
  six is not a rule anybody is following; it is a measurement that does not fit what is being
  measured."* — and the tiers were recalibrated from the data, in the section that sets them.
- *"Fourth consecutive slice queued below what it shipped. Recorded rather than rounded down — the
  pattern is now the finding rather than the individual estimate."*
- *"This ADR had to be superseded one slice after it was written. Worth noticing as a pattern: an
  ADR that enumerates the current tables to justify a mechanism will need amending the first time
  the table set changes."*

Two template sections institutionalise it: **Surprises** in every slice summary, and
**Falsification** — each control removed, the suite re-run, then restored, with a table of what
failed. A test that passes with the control removed was not testing the control.

## Work orders and open questions

- An open question goes in `writ/spec/questions.md` with a recommended answer, and is closed there
  by status — never left as a question inside a work order.
- Revise an acceptance criterion in place the same way when implementation proves it wrong. The
  revision is more informative than the corrected version alone.
- **State honest limitations in the artefact.** "The check is blind to that runtime fact,
  permanently. Review is the control there, and this makes review's job visible rather than
  replacing it."

## ADRs

Write one **when you rejected a credible alternative**. Choosing a UUID scheme over two others is
an ADR. Naming a file is not. The test: would a competent engineer arriving in six months
reconstruct this choice from the code, or re-litigate it?

- Title states the decision **as a fact**: `0035-a-credential-is-only-as-live-as-its-account.md`.
- Numbered sequentially and immutably. Numbers are never reused.
- **Never edited after acceptance**, apart from adding a `Superseded by` link. A record of what was
  believed at the time is the whole value; editing it destroys that.
- Superseding is a *new* ADR that names what it replaces and says what changed our mind.
- One decision per record.
- **The rejected-alternatives table is the reason the record exists.** Without it the next reader
  has no way to know whether their better idea was already considered and dismissed for a reason
  they cannot see. An ADR that lists only benefits was written to justify a decision rather than to
  record it.

## Prose that is generated

Anything a tool writes carries a do-not-edit banner, is committed, and is verified byte-for-byte in
CI. Exclude it from the formatter — a formatter and a generator writing the same file disagree
about it forever.
