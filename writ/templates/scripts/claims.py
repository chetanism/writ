#!/usr/bin/env python3
"""Coverage rows that are wrong rather than unbuilt, and the one correction a merged work order takes.

    python3 scripts/claims.py classify                         # the rows worth a second look, by bucket
    python3 scripts/claims.py classify --json --batch 30       # the same, cut into batches for readers
    python3 scripts/claims.py classify --skip <last report>    # minus what the last review settled
    python3 scripts/claims.py apply corrections.json           # correct claim lines; prints the commit

`COVERAGE.md` is generated from two inputs, work-order claims and annotated test names, so it is
exactly as accurate as they are. A slice that built a requirement and forgot to claim it, or claimed
`partial` out of caution, leaves the row `≈` or `◐` for good: no later slice claims work it did not
do. **`classify` finds those rows; it judges none of them.** It sorts them into four buckets from
the same collector `ledger.py` uses, so it cannot disagree with the ledger about what a row is:

  - **inherited** — `≈`: tests name it and no slice claims it. A merged slice that forgot the claim,
    or evidence older than the process. The work orders and summaries that mention it are listed.
  - **partial_only** — `◐`: every claiming slice is done, every one said `partial`, and tests exist.
    Mostly still open; now and then finished and never said so.
  - **claim_no_test** — a done slice claimed `satisfies` and no test names it. A test comes before
    any claim moves.
  - **unclaimed_mentioned** — `○`, yet a work order, a summary or a test file names it. Mostly
    scope-outs. A test-file mention is one the annotation pattern does not match, which the ledger
    cannot see — and which may not be evidence at all.

`apply` makes the correction `DEVELOPMENT-PROCESS.md` §6.2 allows on a merged work order: it edits
the `satisfies:` and `partial:` lines of its front matter and nothing else. It is run by a person,
never by `/coverage-review`, and it refuses the whole file if any entry fails the bar — the work
order is `done`, the requirement is declared and live, and a move to `satisfies` has a test naming
it. Whether that slice is the one that *finished* the requirement is the judgement the review made;
this cannot check it.

Standard library only, Python 3.9+, like `ledger.py`.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ledger as L  # noqa: E402 — the ledger's own collector, so the two cannot disagree

BUCKETS = ("inherited", "partial_only", "claim_no_test", "unclaimed_mentioned")
TARGETS = ("satisfies", "partial")
# A line the review's report carries for a row the next run may skip: `- FR-ACC-01 · 3f9a01c2 · OPEN`.
SKIP_LINE = re.compile(r"^\s*-\s*`?(?P<id>[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9.]+)+)`?\s*·\s*`?(?P<key>[0-9a-f]{8})`?")


def mention_pattern(ident: str) -> "re.Pattern":
    """The identifier as a whole token: `FR-ACC-01` and never `FR-ACC-010`."""
    return re.compile(r"(?<![A-Za-z0-9-])" + re.escape(ident) + r"(?![A-Za-z0-9])")


def summaries(root: str, config: dict) -> dict:
    """{relative path: text} of every committed slice summary."""
    pattern = os.path.join(root, config["slices"], "**", "*.md")
    return {os.path.relpath(p, root): L.read(p) for p in sorted(glob.glob(pattern, recursive=True))}


def test_texts(root: str, config: dict) -> dict:
    tests = config["tests"]
    out = {}
    for path in L.iter_files(root, tests["globs"], tests.get("exclude", [])):
        try:
            out[os.path.relpath(path, root)] = L.read(path)
        except (UnicodeDecodeError, OSError):
            continue
    return out


def fingerprint(bucket: str, claimers: list, proofs: list, mentions: list) -> str:
    """Changes whenever anything the verdict rested on changes, so a skipped row comes back then."""
    blob = json.dumps([bucket, claimers, proofs, mentions], sort_keys=True)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:8]


def classify(root: str, config: dict) -> list:
    data = L.collect(root, config)
    sections, _counts, _unknown, _unregistered, _unclaimable = L.build_ledger(data)
    by_slice = {o.slice_id: o for o in data.orders}
    summary_text = summaries(root, config)
    test_text = test_texts(root, config)

    def mentions(ident: str, annotated: bool) -> list:
        pattern = mention_pattern(ident)
        found = [o.path for o in data.orders if pattern.search(o.body)]
        found += [p for p, text in sorted(summary_text.items()) if pattern.search(text)]
        if not annotated:
            found += [p for p, text in sorted(test_text.items()) if pattern.search(text)]
        return sorted(set(found))

    rows = []
    for fam, family_rows in sections:
        for row in family_rows:
            if row.ident in data.retired:
                continue
            claimers = [by_slice[s] for s in row.slices if s in by_slice]
            done = [o for o in claimers if o.status == "done"]
            bucket = None
            if row.status == L.INHERITED:
                bucket = "inherited"
            elif row.status == L.PARTIAL and row.proofs and claimers and len(done) == len(claimers) \
                    and not any(row.ident in o.satisfies for o in claimers):
                bucket = "partial_only"
            elif row.unproven and any(row.ident in o.satisfies for o in done):
                bucket = "claim_no_test"
            elif row.status == L.NONE:
                bucket = "unclaimed_mentioned"
            if bucket is None:
                continue
            named = mentions(row.ident, bool(row.proofs))
            if bucket == "unclaimed_mentioned" and not named:
                continue
            claimed = [
                {"slice": o.slice_id, "work_order": o.path, "status": o.status,
                 "claim": "satisfies" if row.ident in o.satisfies else "partial"}
                for o in claimers
            ]
            rows.append({
                "id": row.ident,
                "family": fam.family,
                "bucket": bucket,
                "mark": L.MARK[row.status],
                "claims": claimed,
                "tests": sorted(row.proofs),
                "mentions": named,
                "key": fingerprint(bucket, [(c["slice"], c["claim"], c["status"]) for c in claimed], sorted(row.proofs), named),
            })
    return rows


def skipped(path: str) -> dict:
    """{identifier: key} from the *Skip next run* list of an earlier review's report."""
    out = {}
    for line in L.read(path).split("\n"):
        hit = SKIP_LINE.match(line)
        if hit:
            out[hit.group("id")] = hit.group("key")
    return out


def batches(rows: list, size: int) -> list:
    """Cut per bucket, so one reader judges one kind of question."""
    out, size = [], max(size, 1)
    for bucket in BUCKETS:
        these = [r for r in rows if r["bucket"] == bucket]
        for i in range(0, len(these), size):
            out.append(these[i:i + size])
    return out


def render(rows: list, dropped: int) -> str:
    lines = []
    for bucket in BUCKETS:
        these = [r for r in rows if r["bucket"] == bucket]
        lines.append(bucket + " — " + str(len(these)))
        for r in these:
            claims = ", ".join(c["slice"] + " " + c["claim"] + ("" if c["status"] == "done" else " (" + c["status"] + ")") for c in r["claims"]) or "no claim"
            lines.append("  " + r["mark"] + " " + r["id"] + "  " + r["key"] + "  " + claims)
            for t in r["tests"]:
                lines.append("      test  " + t)
            for m in r["mentions"]:
                lines.append("      named " + m)
        lines.append("")
    lines.append(str(len(rows)) + " rows to judge" + (", " + str(dropped) + " skipped as settled" if dropped else ""))
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------------------------
# apply
# --------------------------------------------------------------------------------------------


def front_matter_span(lines: list):
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i
    return None


def set_list(lines: list, end: int, key: str, values: list) -> int:
    """Rewrite one front-matter list as `key: [A, B]`, keeping its trailing comment where it was. A
    block list (`key:` then `- A` lines) is folded into the inline form. Returns the new end of the
    front matter, and adds the key before the closing `---` when the file has none."""
    rendered = "[" + ", ".join(values) + "]"
    shape = re.compile(r"^" + key + r"\s*:\s*(\[[^\]]*\]|[^#]*?)\s*(#.*)?$")
    for i in range(1, end):
        hit = shape.match(lines[i])
        if not hit:
            continue
        head = key + ": " + rendered
        if hit.group(2):
            column = hit.start(2)
            head = (head.ljust(column) if len(head) < column else head + " ") + hit.group(2)
        lines[i] = head
        while i + 1 < end and re.match(r"^\s*-\s+", lines[i + 1]):
            del lines[i + 1]
            end -= 1
        return end
    lines.insert(end, key + ": " + rendered)
    return end + 1


def check_entry(root: str, config: dict, data, proofs: dict, by_path: dict, entry) -> list:
    if not isinstance(entry, dict) or set(entry) != {"work_order", "id", "to"}:
        return ["each entry is {\"work_order\", \"id\", \"to\"} and nothing else: " + json.dumps(entry)]
    where, ident, to = entry["work_order"], entry["id"], entry["to"]
    errors = []
    rel = os.path.normpath(os.path.join(config["work_orders"], where))
    if rel.startswith("..") or not rel.startswith(os.path.normpath(config["work_orders"]) + os.sep):
        return [where + ": not a path under " + config["work_orders"]]
    order = by_path.get(rel)
    if order is None:
        return [where + ": no work order there"]
    if order.status != "done":
        errors.append(where + " is " + order.status + ", not done — edit a live work order the usual way")
    if to not in TARGETS:
        errors.append(where + ": " + ident + " to " + str(to) + " — the target is satisfies or partial")
    declared = {i for fam in data.ids.values() for i in fam}
    if ident not in declared:
        errors.append(where + ": " + ident + " is not declared")
    elif ident in data.retired:
        errors.append(where + ": " + ident + " is " + data.retired[ident] + " — nothing claims a retired row")
    if to == "satisfies" and not proofs.get(ident):
        errors.append(where + ": " + ident + " has no test naming it — write the test first, then move the claim")
    return errors


def apply(root: str, config: dict, entries: list) -> tuple:
    """Validate every entry, then edit. Returns (errors, commit message); nothing is written on error."""
    if not isinstance(entries, list) or not entries:
        return ["the corrections file is a non-empty JSON list"], ""
    data = L.collect(root, config)
    proofs = {}
    for ident, proof, _path in data.annotations:
        proofs.setdefault(ident, []).append(proof)
    by_path = {os.path.normpath(o.path): o for o in data.orders}

    errors = []
    for entry in entries:
        errors += check_entry(root, config, data, proofs, by_path, entry)
    if errors:
        return errors, ""

    changed, lines_out = {}, []
    for entry in entries:
        rel = os.path.normpath(os.path.join(config["work_orders"], entry["work_order"]))
        order = by_path[rel]
        sats, pars = changed.get(rel, (list(order.satisfies), list(order.partial)))
        ident, to = entry["id"], entry["to"]
        if to == "satisfies":
            pars = [p for p in pars if p != ident]
            sats = sats if ident in sats else sats + [ident]
            proof = sorted(set(proofs[ident]))[0]
            lines_out.append("- " + order.slice_id + " satisfies " + ident + " — proved by: " + proof)
        else:
            if ident in sats:
                continue
            pars = pars if ident in pars else pars + [ident]
            lines_out.append("- " + order.slice_id + " partial " + ident)
        changed[rel] = (sats, pars)

    for rel, (sats, pars) in changed.items():
        path = os.path.join(root, rel)
        text = L.read(path)
        lines = text.split("\n")
        end = front_matter_span(lines)
        end = set_list(lines, end, "satisfies", sats)
        set_list(lines, end, "partial", pars)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines))

    message = (
        "docs(process): correct the claims of " + str(len(changed)) + " merged work order"
        + ("" if len(changed) == 1 else "s") + "\n\n"
        + "The slices built these and did not claim them; only the claim lines change.\n\n"
        + "\n".join(lines_out) + "\n"
    )
    return [], message


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Coverage rows that are wrong rather than unbuilt, and their claim corrections.")
    parser.add_argument("command", choices=["classify", "apply"])
    parser.add_argument("corrections", nargs="?", help="apply: the JSON file of corrections")
    parser.add_argument("--json", action="store_true", help="classify: machine-readable, with batches")
    parser.add_argument("--batch", type=int, default=30, help="classify: rows per batch (default 30)")
    parser.add_argument("--skip", help="classify: an earlier review's report; rows it settled and that have not changed are left out")
    parser.add_argument("--root", default=".", help="project root")
    parser.add_argument("--config", default="scripts/ledger.config.json")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    config = L.load_config(root, args.config)

    if args.command == "classify":
        rows = classify(root, config)
        dropped = 0
        if args.skip:
            settled = skipped(args.skip)
            kept = [r for r in rows if settled.get(r["id"]) != r["key"]]
            dropped, rows = len(rows) - len(kept), kept
        if args.json:
            out = {"rows": rows, "skipped": dropped, "batches": [[r["id"] for r in b] for b in batches(rows, args.batch)]}
            sys.stdout.write(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
        else:
            sys.stdout.write(render(rows, dropped))
        return 0

    if not args.corrections:
        sys.stderr.write("error: apply takes the corrections file — python3 scripts/claims.py apply corrections.json\n")
        return 2
    with open(args.corrections, encoding="utf-8") as handle:
        try:
            entries = json.load(handle)
        except json.JSONDecodeError as err:
            sys.stderr.write("error: " + args.corrections + " is not JSON: " + str(err) + "\n")
            return 1
    errors, message = apply(root, config, entries)
    for line in errors:
        sys.stderr.write("error: " + line + "\n")
    if errors:
        sys.stderr.write("nothing was changed\n")
        return 1
    sys.stdout.write(message + "\nNext: python3 scripts/ledger.py, then commit the work orders and COVERAGE.md together with the message above.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
