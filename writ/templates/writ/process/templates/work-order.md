---
id: SL-<NNN>             # the next free number across the repository, zero-padded
title: <one line, lowercase: what lands>
phase: <P01>             # the phase code from MILESTONE-PLAN.md §3 — also the folder this file sits in
kind: feature            # feature, or characterisation: adds tests around behaviour that already
                        # exists and changes none of it. Only characterisation may say `demo: none`
status: queued          # queued | in-progress | in-review | done | blocked
dep: "—"                # or an external-track mark from MILESTONE-PLAN.md §8
owner: ""               # team mode only
issue:                  # the tracker issue number, no `#`, and nothing after it on the line
depends_on: []          # [SL-040, SL-041] — slices that must be done first; the queue order comes from this
touches: []             # team mode: shared areas, e.g. [schema/accounts, api/v1/orders]
satisfies: []           # [FR-ACC-01] — requirements this slice fully proves with a test
partial: []             # [INV-003] — requirements it moves forward without finishing
adr: []                 # [ADR-0004] — decision records; each must exist before coding starts
demo: script            # script | ui | none (characterisation only)
---

# Slice <ID> — <title>

> **What this is:** the plan for one slice, agreed before any code is written. It becomes the pull
> request description. List requirements in the front matter only — nowhere else in the file — so
> there is one place to look. Delete this note.

## Why this slice exists

<Two sentences. What goes wrong for somebody while this is missing, then what the slice changes.>

## Decisions this slice makes

| Decision | Choosing | Over | ADR |
|---|---|---|---|
|  |  |  |  |

> A decision that later slices will have to live with gets a decision record (ADR), written before
> coding starts and named in `adr:`. A decision that only shapes this slice just needs a row here.

## Contract change

<What changes in the public API or other published surface — or **none**. For a new endpoint:
path, method, what it needs, and whether calling it twice is safe.>

## Acceptance criteria

> Each one becomes a test name, so start each with the requirement it proves — for example
> `1. [FR-ACC-01] a second sign-up with the same email is refused`. Include the awkward cases: a
> double submit, another customer's data, an empty list. If you cannot picture the test, the
> criterion is not precise enough yet.

1.
2.

## Demo

> How a person sees this working, by hand. Keep exactly one of the three options below and delete
> the others. `ledger.py check` fails a missing demo, a script with no code block, a UI demo with no
> **Expected:** line, or any `<placeholder>` left in.

### Nothing new to show — `kind: characterisation` only

> Nothing changed, so there is nothing new to play. Instead say what behaviour the new tests now
> pin, and who confirmed that behaviour is actually wanted — a test written by reading the code
> will lock in a bug just as firmly as a feature. Anything found to be wrong becomes a `DEBT-NNN`
> row and is pinned as-is, not fixed here.

### Script

> Something a person can paste and run. Never make them type an ID: capture it instead.

```bash
ACCOUNT=$(myapp account create --json | jq -r .id)
myapp account show "$ACCOUNT"     # criterion 1 — status is active
```

### By hand (UI)

1. <One action.>
2. <One action.>

**Expected:** <what is on screen — specific enough that it could be wrong.>

## Out of scope

| Not in this slice | Where it lands |
|---|---|
|  |  |

> What a reader might reasonably expect here and will not get. It tells a deliberate choice apart
> from something forgotten.
