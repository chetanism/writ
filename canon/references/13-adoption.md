# Adopting the process into a team that has not agreed to it

## Partial adoption is not the degraded case

Nobody converts a five-person team on a live codebase in one go. One person installs this, uses it
on their own work, finds out what it is worth, and brings people in one at a time — or it does not
get adopted at all.

So the default output of an adoption is **one user and zero enforcement**, and everything else is
opt-in escalation. That is a different default from `/canon:solo`, which assumes the repository is
yours because you created it five minutes ago.

The failure this is shaped around is not technical. **Turn every rule on over somebody else's
directory and their pull requests start failing for rules that arrived in a commit they never
read.** That is how a process is removed from a repository inside a week, and no amount of being
right about the rules survives it.

## The perimeter

`enforce` in `scripts/ledger.config.json` says which paths each rule is in force over.

```json
"enforce": {
  "default": [],
  "annotations": ["**"],
  "work_order": ["src/billing/**"]
}
```

Three things to know, and the third is the one people get wrong:

1. **`default` covers every rule not named.** The common case stays one line.
2. **`[]` encloses nothing.** That is how the whole thing stays quiet on day one.
3. **A named rule *replaces* the default for that rule — it does not add to it.** So a rule can be
   widened past the default or narrowed below it. The narrowing is the case that matters:
   annotations demanded across the repository while work orders are demanded in one directory is
   the ordinary shape of a half-adopted project, and a union could not express it.

**Only two rules are path-shaped, and that is not an oversight.** Ledger freshness, the
placeholder scan and registry integrity are about the canon tree itself and are global always. The
size budget and the ADR rule are fields *on a work order* — outside one there is nothing to check,
so they follow `work_order` by construction.

| Rule | Costs a bystander | Where it belongs early |
|---|---|---|
| `annotations` | Seven characters and no understanding | Repository-wide, within weeks |
| `work_order` | The entire process | One directory, and only once two people run the loop |

`work_order` is enforced in CI rather than by the tool, because it is a fact about a diff and
`ledger.py` only ever sees one commit's worth of tree. The workflow **reads the perimeter from
`ledger.config.json`** rather than repeating it: two copies of the adopted path list is two
answers to *is this directory in force yet*, discovered the day somebody widens one of them.

The canon tree is outside the perimeter whatever the patterns say. Documents are how this process
gets corrected, and a correction that needed its own slice would never be made.

## The ladder

Each rung has to pay for itself before the next one is climbed.

| | Rung | Who is affected | What it buys |
|---|---|---|---|
| 0 | **One person, read-only.** Survey, `CLAUDE.md`, area map, debt register. Nothing in CI | Nobody else | The adopter's own agent sessions get better immediately |
| 1 | **Their own slices.** `/slice-open`, `/slice-close` on their own work | Nobody else | The team sees *better pull requests*. This is the only marketing that works |
| 2 | **The annotation harvest.** One mechanical pass | Nobody else | Coverage stops reading zero. Numbers recruit |
| 3 | **A second person, by pairing on a slice** | One colleague, by choice | The process stops being one person's hobby |
| 4 | **Perimeter on, one area** | Anyone touching that directory | The first real gate |
| 5 | **Team mode** — WIP limits, `touches` collisions | Everyone running the loop | Contention management, once there is contention |

**Rung 3 before rung 4, and hold that one firmly.** Do not block other people's work until at
least two people run the loop. Otherwise the adopter is the only person who can regenerate the
ledger, read a check failure or explain a rejection — the process is their pet, it blocks everyone
else, and it dies the week they go on holiday. Two people is also the first honest test of whether
any of this works when its author is not driving.

Rung 0 has to be **genuinely useful alone**. If it is not, nothing later happens. It is also
unobjectionable, which is the point: nobody can reasonably refuse a colleague writing documents.

## The annotation harvest

The highest-return operation in the whole adoption, and it is mechanical.

The suite already contains hundreds of tests that are already a requirements document. Adding
`[FR-012]` to a describe block is seven characters, carries no design decision, and cannot break
anything. **On an existing codebase, coverage is earned by naming the tests you already have, not
by writing new ones** — which is not what anybody expects, and is why the first fortnight can show
real movement rather than pure cost.

A row with tests and no claiming slice reads `≈ inherited`, not `○`. That is the state the harvest
produces, and the ledger keeps it separate from `◐ partial` on purpose: `◐` is a promise somebody
made and did not keep, `≈` is evidence nobody has claimed yet. Averaging them reports a brownfield
repository as uniformly half-done, which is the one number nobody can act on.

Do it as one pull request per area, and do not correct a test while annotating it. A harvest that
also fixes things is a harvest nobody can review.

## Characterisation slices

`kind: characterisation` — a slice that changes no behaviour and writes the tests that pin what
the code already does. It is how an `≈` row becomes `●`: the tests exist, the work order finally
claims them, and the claim is now something the process can hold somebody to.

It is the only kind that may declare `demo: none`, because there is nothing to play that was not
playable yesterday. What replaces the demonstration is not nothing. **The question a
characterisation slice gets wrong is whether the behaviour it froze was the behaviour anybody
wanted** — a test written from the code asserts the bug exactly as confidently as it asserts the
feature, and afterwards the suite defends it. So the Demo section says what was pinned and who
confirmed it was intended, against what. If something turns out to be wrong, it becomes a
`DEBT-NNN` row and the slice pins the behaviour *as it stands* rather than fixing it — mixing a
fix into a characterisation slice destroys the one property that made it safe.

## Solo or team

**A five-person team with one canon user installs solo.** Team mode is about contention, and
contention needs a crowd; turning it on for one person is pure overhead with no failure to
prevent.

Promotion later is cheap and it is worth saying so, because an adopter who thinks they are
choosing a door that locks will choose neither. In the tool, `mode` decides only whether the queue
renders an Owner column, and the two real team checks — the WIP limit and `touches` collisions —
key off `wip_limit` being non-zero rather than off `mode` at all. So promotion is: set `mode` to
`team`, set `wip_limit`, and start writing `owner:` and `touches:` on new work orders. Nothing is
retrofitted and no existing slice becomes invalid.

## What the other four need to know

**One screen, and not a word more.** If bringing somebody in requires them to read
`DEVELOPMENT-PROCESS.md`, it will not happen.

It says: which directories are inside the perimeter and what that demands there; that annotating a
test means putting `[FR-012]` at the front of its name; and who to ask. That is the whole briefing
for somebody who is not running the loop.

## The three things that decay, and what notices

- **Annotations.** A colleague refactors an annotated test file and drops the `[FR-012]`, or adds
  twenty tests with none. Coverage silently regresses. `ledger.py` reports a proof that has
  disappeared — evidence *lost* reads identically to evidence never present in a generated table,
  and they are not the same event. It is a warning and never an exit code: failing the adopter's
  build for somebody else's deletion is how the tool gets removed.
- **Requirements drift from the code.** Four people ship behaviour no row describes, and the
  registers slowly become a specification for a product that no longer exists. Nothing detects
  this. It is what the perimeter is for: inside it, drift fails; outside it, drift is a thing the
  team has knowingly accepted, which is a far better position than pretending otherwise.
- **The adopter becomes the bottleneck.** Rung 3 exists for this, and it is why it comes first.

## Reading whether it is taking

`python3 scripts/ledger.py stats` grows an **Adoption** block whenever the perimeter is narrower
than everything, a row is inherited, or a register carries `observed` rows. Four numbers:

- what each rule is in force over;
- how many test files name a requirement, and how many are inside the perimeter;
- the characterisation queue — inherited rows waiting for a work order;
- how many rows are still read off the code rather than decided.

The adopter needs these to make the case internally, which is a use no other part of this process
has. A greenfield project sees none of it.
