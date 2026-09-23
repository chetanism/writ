# A worked example

**This is a real tree with the tool run over it, not an illustration.** Three files a person wrote
went in; four files the tool generated came out, and everything below was copied out of that run
verbatim. If you want to know what this kit actually produces before you run a ten-phase interview
on your own project, this is the page.

It is regenerated and diffed on every push — see [Keeping it honest](#keeping-it-honest) — so it
cannot quietly stop being true.

---

## The product

A lending library for an office bookshelf. Deliberately dull; the interesting part is not the
product but that five requirements are enough to show every state the ledger can report.

| Identifier | What it says | Ends up |
|---|---|:--|
| `FR-LEND-01` | Somebody can borrow a copy that is on the shelf | **● satisfied** |
| `FR-LEND-02` | Somebody can return a copy they borrowed | **◐ partial** |
| `FR-LEND-03` | Somebody can join the queue for a copy that is out | **◐ partial** |
| `NFR-AUD-01` | Every borrow and return is attributable to a person and a time | **○ none** |
| `INV-001` | A copy is never on loan to two people at once | **≈ inherited** |

**`FR-LEND-02` is the row worth stopping on.** The work order says the slice satisfied it. No test
names it. The ledger reports it as *partial* and lists it under "Claimed without proof" — because
a work order is a claim and only a test is evidence. That single disagreement, surfaced rather
than averaged away, is most of what this kit is for.

---

## What a person wrote

| | |
|---|---|
| [`source-register.md`](source-register.md) | The area register. A requirement exists because it is a row in this table, and nowhere else. |
| [`source-work-order.md`](source-work-order.md) | The work order for `SL-001`, written before any code. Its front matter is the only place a slice claims coverage. |
| [`source-tests.ts`](source-tests.ts) | The tests. The identifier in the test name is the entire proof mechanism. |

## What the tool made of it

| | |
|---|---|
| [`generated-COVERAGE.md`](generated-COVERAGE.md) | The coverage ledger — every identifier, its state, what claimed it and which test names it |
| [`generated-INDEX.md`](generated-INDEX.md) | Every identifier in the repository, with where it was declared |
| [`generated-SLICE-QUEUE.md`](generated-SLICE-QUEUE.md) | The queue, ordered from the `depends_on` in work-order front matter |
| [`generated-stats.txt`](generated-stats.txt) | The instrument you run at a phase gate. It never fails a build |
| [`generated-graph.json`](generated-graph.json) | The same graph, for something other than a person to read |

---

## The chain, in four steps

**1. A requirement is declared.** One row in one table, under a header that begins `| ID |`:

```
| FR-LEND-01 | Somebody can borrow a copy that is on the shelf. | M1 | v0.1 | active |
```

Nothing else mints an `FR-LEND-*`. There is no second list to keep in step, which is why there is
no second list to go wrong.

**2. A slice claims it,** in work-order front matter, before any code exists:

```
satisfies: [FR-LEND-01, FR-LEND-02]
```

**3. A test proves it,** by naming it:

```js
it("[FR-LEND-01] lends a copy that is on the shelf to the person who asked", () => {
```

**4. The tool reads all three and disagrees with the work order:**

```
| ID | State | Claimed by | Proven by |
| FR-LEND-01 | ● | SL-001 | `[FR-LEND-01] lends a copy that is on the shelf...` |
| FR-LEND-02 | ◐ | SL-001 |  |
| INV-001    | ≈ |        | `[INV-001] refuses a second borrow of a copy already out...` |
```

`INV-001` is **inherited**: a test proves it and no work order ever claimed it. On a brownfield
codebase that column is where most of your existing test suite lands, and it is how `/writ:adopt`
gives you credit for work that predates the process.

---

## What a phase gate looks like

`python3 scripts/ledger.py stats`, in full, from this example:

```
SL — 3 slices: 2 queued, 1 done
  P01  Foundation            1/3 done

Coverage — 1 satisfied of 20
  FR    ● 1   ≈ 0   ◐ 2   ○ 0     2 claimed with no test behind them
  NFR   ● 0   ≈ 0   ◐ 0   ○ 1
  INV   ● 0   ≈ 1   ◐ 0   ○ 0
  DoD   ● 0   ≈ 0   ◐ 1   ○ 11    1 claimed with no test behind them

Adoption — what this process is in force over
  annotations  **
  work_order   **
  test files   1 of 1 name a requirement · 1 inside the perimeter
  inherited    1 rows proven by tests no work order claimed — the characterisation queue

Tracks — beside the loop
  detail     reviewed 0 · draft 0 · none 4   of 4 requirements the track covers
  scenarios  reviewed 0 · draft 0 · none 4   of 4 requirements the track covers

Backfill — out_of_order: backfill
  built ahead    3 requirements with no detail file · 2 aimed at M1, the active milestone

Standing records
  cleanup-backlog.md      0 open
  security-backlog.md     0 open
  last audit              never — /security-audit has not run
```

Read that as a status report nobody wrote. **"2 claimed with no test behind them"** is the sentence
a weekly meeting is otherwise spent discovering. **"3 requirements with no detail file"** is the
other one: SL-001 was built before anybody wrote down what borrowing and returning mean, so nobody
has yet decided whether what it built is what was wanted. This example runs `out_of_order: backfill`,
so they are a queue in `generated-COVERAGE.md` rather than a failure; a bootstrap's `fail` would
have stopped SL-001 at its claim. Note that `stats` reports and never fails —
an instrument that can fail a build is a gate wearing a different name.

---

## Taking the data with you

`python3 scripts/ledger.py graph` prints the whole thing as JSON — every identifier with its state,
what claimed it, which test names it, and every slice with its phase, status and claims:

```json
{
  "id": "FR-LEND-02",
  "family": "FR",
  "state": "partial",
  "claimed_by": ["SL-001"],
  "proven_by": [],
  "claimed_without_proof": true
}
```

That is there for dashboards, badges, reports spanning several repositories — and for leaving. A
process kit whose data can only be read by its own renderer is a lock-in, and the argument this kit
makes about documents applies to the kit itself: if the data cannot get out, calling it *your*
process is decorative. Like `stats`, it reads everything, writes nothing, and cannot fail a build.

---

## Keeping it honest

A worked example pasted into a document by hand is a second description of the tool's behaviour,
immediately less true than the tool and maintained by nobody. That is the exact failure this whole
process is shaped around, so committing one would have been an unfortunate way to illustrate it.

The example is built by a script and checked in CI:

```bash
python3 writ/tests/build_example.py           # regenerate this directory
python3 writ/tests/build_example.py --check   # fail if it has drifted
```

The second form runs in `.github/workflows/kit.yml`. Change the tool's output and this page goes
red until it is rebuilt.

---

Next: [How to use it](../using-it.md) for the loop this example is one turn of, or
[The nineteen skills](../skills/README.md) for what runs each step.
