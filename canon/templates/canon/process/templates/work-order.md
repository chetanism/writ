---
id: SL-<NNN>             # a global number, zero-padded, that encodes nothing else
title: <one line, lowercase, what lands>
phase: <P01>             # the phase code from MILESTONE-PLAN.md §3; also the directory this sits in
size: <S|M|L>           # the tier this slice *is*. Corrected at close if the measurement says otherwise
estimated:              # added code lines, guessed at open. Never corrected — it is the only
                        # evidence the tiers can be recalibrated from
code_lines:             # added code lines, measured at close. `size` has to contain it
status: queued          # queued | in-progress | in-review | done | blocked
dep: "—"                # or an external-track mark from MILESTONE-PLAN.md §8
owner: ""               # team mode only
issue:                  # the tracker issue, opened at the claim. A number, no `#`, no comment
                        # after it — the front matter is not YAML and will keep what follows
depends_on: []          # [SL-040, SL-041] — the queue order is derived from this
touches: []             # team mode: shared surfaces, e.g. [schema/accounts, api/v1/orders]
satisfies: []           # [FR-ACC-01] — claimed here and nowhere else
partial: []             # [INV-003]
adr: []                 # [ADR-0004] — the record must exist before implementation begins
demo: script            # script | ui
---

# Slice <ID> — <title>

> Written at step 2 of the loop, **before any code**, and committed on the slice branch with the
> draft pull request. This file is the pull request description.
>
> **The front matter is the only claim site.** Do not restate `satisfies` in a table below — one
> claim site means there is nothing to drift.
>
> Delete this blockquote.

## Why this slice exists

<The requirement being served, and the failure mode if it is absent. Two or three sentences. Lead
with what breaks, not with what gets built.>

## Decisions this slice makes

| Decision | Choosing | Over | ADR |
|---|---|---|---|
|  |  |  |  |

> **Anything with a credible rejected alternative gets an ADR, and the record is written before
> implementation starts** — a decision recorded afterwards is a justification. Name it in the front
> matter's `adr:` field; `ledger.py check` fails if the file does not exist.

## Contract change

<What appears or changes in the published surface, or **none**. For a new endpoint: path, method,
what it requires, and whether it is safe to retry.>

## Size

**<S|M|L> — <N> code lines, <N> in the diff.** Estimated <N>.

> Added code lines: outside tests, comments, blanks and generated files.
>
> **Both numbers are in the front matter and `ledger.py check` holds them together**: `size` has to
> be the tier `code_lines` falls in, so a slice that came in at 420 is an `L` whatever anybody
> guessed. `estimated` is never corrected — it is the only evidence the tiers can be recalibrated
> from, and editing it to match the outcome is how that evidence gets destroyed. `ledger.py stats`
> is where the two are compared; after three misses in the same direction the finding is about the
> tiers rather than about a slice.
>
> **The top tier has to argue for itself.** An `L` states, here, why it could not be split, and the
> check fails a Size section that says only what it measured.

## Acceptance criteria

> Numbered, independently checkable, and precise enough that **each becomes a test name**. If a
> criterion cannot become a test name, it is not written precisely enough yet.

1.
2.

## Demo

> Exactly one of the two shapes below. Delete the other. This section is checked mechanically: a
> missing section, a script with no runnable block, a UI demo with no expectation, or **any
> placeholder identifier** fails `ledger.py check`.

### Script

> Copy-pasteable, with **no identifier for the reader to substitute** — nobody types thirty
> characters of base32. Capture what the slice creates:

```bash
ACCOUNT=$(myapp account create --json | jq -r .id)
myapp account show "$ACCOUNT"     # criterion 1 — status is active
```

### By hand (UI)

1. <One action.>
2. <One action.>

**Expected:** <what is on screen, specific enough to be wrong.>

## Out of scope

| Not here | Lands at |
|---|---|
|  |  |

> What a reasonable reader might expect in this slice and will not get. This distinguishes a
> decision from an oversight — the distinction a future reader cannot recover from the diff.

## Open questions

> Resolve them **in place**, with strikethrough and the answer, rather than deleting them. Empty is
> a valid answer.

1.
