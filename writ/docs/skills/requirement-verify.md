# `/requirement-verify`

**At a phase gate: is the behaviour the detail file describes actually there? One requirement per
run, four verdicts, report-only.**

| | |
|---|---|
| **Run it** | At a phase gate, over the requirements the coverage ledger has turned `●`. `/requirement-verify FR-ACC-01` |
| **Produces** | One row appended to the detail file's `## Verification` section — date, verdict, who ran it, evidence a reader can chase |
| **Refuses to** | Edit code, edit the BRD, or change any claim the detail file makes |

## Why it exists

**A slice proves the claims it made. Nothing proves that a *requirement* is met** — because a
requirement is finished by several slices and none of them owns it.

Every slice can be green, every claim honoured, every test passing, and the requirement still not
be met: each slice did its part correctly and the parts do not add up to the behaviour. That gap is
invisible to the gate by construction, and this is the only thing that looks at it.

## The four verdicts

| Verdict | When |
|---|---|
| `implemented` | Every observable has evidence, and the boundary cases hold |
| `gap` | Some do and some do not. **Named precisely enough to become a work item** |
| `absent` | The requirement reads satisfied and the behaviour is not there. It says what the tests are actually asserting |
| `detail-wrong` | The file described the requirement wrongly. **The file is what gets fixed, not the product** |

`absent` is the serious one — something is credited as done that is not — and it names the slice
that claimed it.

## The rules it holds itself to

**It never picks the reading that makes the verdict come out well.** A requirement the specification
states ambiguously enough that two verdicts are defensible is a finding for its owner, reported as
one.

**A gap is not fixed here, and it is never fixed by widening a test.** It goes to the slicer as a
work item with the observable it failed.

**An observable nobody can exercise yet is a fact about the product, not a gap in the run**, and it
is reported as such.

## See also

[`/requirement-detail`](requirement-detail.md) — where the observables it checks were written down,
and where a `detail-wrong` verdict goes back to.
