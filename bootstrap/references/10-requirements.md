# The requirement detail track

Governs the phase that emits `/requirement-detail` and `/requirement-verify` into the new project,
along with `docs/process/requirements/`. Read it before that phase.

The track is **parallel to the slice loop and never inside it**. Nothing in the loop waits on it,
and nothing in it waits on a slice. That is the property to protect: the moment a slice cannot
merge until a requirement is detailed, two people are on the critical path of every merge and the
process has become the serial one this replaces.

## The gap it fills, in one paragraph

A requirement in the BRD is one line, because a BRD states business intent and stops there. That is
enough to build against and **not** enough to test against by hand: it names no actor, no
precondition, no observable outcome and no boundary. Nothing else in the tree fills it — a work
order describes a *slice*, and slices and requirements are many-to-many by design, so a work order
spans several requirements and proves only the claims it made. Read a slice to test a requirement
and you get part of an answer with no way to know which part is missing.

`COVERAGE.md` is the mechanical half of the ledger: what is claimed and what is proven. This is the
hand-testing half: what a person would **see** if the requirement held.

## The one rule, and why it is a check rather than a paragraph

**A detail file never restates its requirement in its own words.** It quotes the BRD row verbatim,
and `ledger.py check` compares the quote against the specification character for character.

Say why when you write the README: two wordings of one requirement is two requirements, discovered
the day they disagree, and by then nobody can tell which one the product was built against. The
check is what makes the rule real — when the BRD is amended, every affected file fails until
somebody has read the amendment and re-dated `reviewed_against`. **That failure is the feature.**

## What to set at bootstrap

| Setting | Where | Default and why |
|---|---|---|
| the covered families | `requirements.families` in `scripts/ledger.config.json` | `["FR", "INV"]` — the families a person can be *asked to exercise*. Not `NFR` or the process families: those name mechanisms, and a mechanism is tested through the requirement it serves |
| the directory | `requirements.dir` | `docs/process/requirements`. Empty turns the whole track off, which is what a project that declined it gets |
| the phase mirror | `requirements.phase_pattern` | Whatever token the BRD's requirement tables use — `V1\|V2\|R` out of the box. A declaring table with no such column is simply not phase-checked |
| the closing rule | `requirements.require_detail_for_satisfied` | `false`. Turning it on with a backlog fails the gate for work nobody has been asked for yet. It is what closes the track once the backlog in `COVERAGE.md` is cleared |
| who approves | the README's *Who does what* table | Solo: the agent drafts, the one human approves. Team: name the two people, and prefer that the approver is not the drafter |

**Do not seed the directory.** An empty directory and a `README.md` is the correct output of
bootstrap. Four hundred requirements drafted by an agent and read by nobody is not coverage; it is
a directory that looks like coverage, which is worse than an empty one.

## Solo mode is not a degenerate case

The split that matters is **drafter and approver**, not two named people. Solo, the agent drafts
and the human approves — which is the same two-party review the team version describes, and it is
the whole point: an agent's reading of a one-line requirement is exactly the thing a human is there
to correct. Write the README's role table that way rather than deleting it.

What solo genuinely loses is the second reader on the *approval*. Say so in the README rather than
pretending otherwise; `drafted_by` and `approved_by` naming the same person is a fact worth being
able to see later.

## The two skills, and the failure each is shaped around

**`/requirement-detail` is a conversation, not a delivery.** It reads the requirement back in eight
lines, interviews in rounds of two to four numbered questions each carrying the answer it would
pick, and writes the file last. The shape it replaces is generating ninety plausible lines and
asking somebody to find the wrong three — a reviewer handed a plausible document agrees with it,
which is the failure the entire track exists to avoid. One identifier per invocation, for the same
reason: a session holding twelve requirements writes twelve files that blur into each other, and
the blurring is invisible in review.

**`/requirement-verify` is report-only, in the way `/manual-test` is.** It answers one question
about one requirement: is the behaviour this file describes actually there? Four verdicts —
`implemented`, `gap`, `absent`, `detail-wrong` — and the vocabulary is checked, because *mostly
works* is the verdict it exists to refuse. It never edits code, never edits the BRD, and never
relaxes a detail file until it matches what was built. That last one is the failure it is shaped
around.

It runs **per phase gate**, over the requirements that turned `●` during the phase. Not per slice:
a requirement is usually finished by several slices, and verifying one half-built produces a
finding about the queue rather than about the product.

## Where it touches the rest of the process

- **`DEVELOPMENT-PROCESS.md` §12** — one section saying why the track exists and what it
  deliberately does not do. The detail joins §1's document model.
- **§11's cadence** — `/requirement-verify` per phase gate.
- **`DoD-12`** — the one place a slice reads the track: the *reviewed* detail files of the
  requirements it claims, because their observables are where a conflict shows up first. A `draft`
  file is one agent's reading; treat it as a prompt for a question, not as the requirement.
- **`COVERAGE.md`** — grows a *Requirement detail* section: how many files, how many reviewed, and
  every satisfied requirement with no reviewed file behind it. That list is the track's backlog,
  **listed rather than averaged away**.
- **`/manual-test`'s oracles** — cited from a detail file, never copied into one. Three copies of
  what "correct" means is three documents that drift.
