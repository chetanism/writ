# Work orders

One per slice, opened before any code is written. A work order is the pull request description at
open, and the tracker issue's body where one is configured.

## Layout

```text
work-orders/<milestone>/<phase>/<number>.md   m1-mvp/F/000.md
slices/<milestone>/<phase>/<slice id>.md      m1-mvp/F/SL-000.md
```

**The milestone directory is `m<n>-<slug>`** — numbered so it sorts, named so it means something.
It matches the milestone plan it was cut from: `m1-<slug>` is `canon/spec/MILESTONE-PLAN.md`,
whose lifetime is one milestone. A new milestone gets a new plan and a new directory here, and the
finished one is left exactly as it is.

**The phase directory is the phase letter**, expanded in `scripts/ledger.config.json`. It must be
the phase the work order's front matter declares: `python3 scripts/ledger.py check` fails naming
both when they disagree, because the directory is how a person finds a slice and the front matter
is how the queue orders it, and a reader who is quietly wrong is the worse failure.

**A slice summary is filed at the mirrored path** under `slices/`, so both halves of one slice sit
in the same place in two trees. The check looks there and nowhere else.

Directories are created when they are first needed. Sixty files in one directory is what this
layout exists to prevent, so do not pre-create empty phases to make the tree look complete.

## Reading order

`SLICE-QUEUE.md` is the index — it is generated from the front matter here, in dependency order.
Do not infer order from the filesystem.
