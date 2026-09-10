# Slice summaries

One committed summary per completed slice, written in that slice's own commit.

**Filed at `<milestone>/<phase>/<slice id>.md`, mirroring the work order** — `m1-mvp/F/SL-000.md`
for `work-orders/m1-mvp/F/000.md`. `python3 scripts/ledger.py check` looks there and nowhere else,
so a summary filed flat reads as a missing one. Phase directories are created when the first slice
in that phase closes, not before: an empty directory is not worth committing.
