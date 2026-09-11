#!/usr/bin/env python3
"""Does `reference/areas.md` still describe the system?

The oracles in that file are hand-written, and hand-written copies of a moving surface drift. Two
failure modes, and they are not symmetric: an oracle that is **missing** is thin cover and costs a
run nothing, while an oracle that is **wrong** produces a false finding every session until
somebody chases it down. This makes the second one loud.

It checks only what is enumerable from the repository itself. The judgements in `areas.md` — that a
lattice converges, that another tenant's row is absent rather than refused — are not checkable this
way and are not meant to be: they cite stable identifiers, which is what keeps them findable when
the surface moves under them.

  python3 drift.py            report, exit 1 if anything is stale
  python3 drift.py --quiet    exit code only

Stdlib only, and the registry is read through `scripts/ledger.py` rather than re-parsed here: the
declaration rule has exactly one implementation, and this is not it.
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
QUIET = "--quiet" in sys.argv[1:]

sys.path.insert(0, os.path.join(ROOT, "scripts"))
try:
    import ledger  # noqa: E402
except ImportError:
    sys.stderr.write("drift: cannot import scripts/ledger.py from " + ROOT + "\n")
    sys.exit(2)

SOURCES = ["reference/areas.md", "SKILL.md"]

# A citation is a token whose prefix names a **registered family** and whose last segment carries a
# digit. The digit rule is what keeps `MR-NN` and `SEC-YYYY-NNN` — the shapes a document uses to
# describe a format rather than to name a thing — out of the check.
TOKEN = re.compile(r"\b([A-Z][A-Za-z0-9]*(?:-[A-Za-z0-9.]+)+)\b")
ADR = re.compile(r"\b(ADR-(\d{3,}))\b")
ABSENT = re.compile(r"<!--\s*drift:absent\s+(\S+)\s*-->")


def sources():
    out = []
    for rel in SOURCES:
        path = os.path.join(HERE, rel)
        if os.path.exists(path):
            out.append((rel, ledger.read(path)))
    return out


def declared_everything(config):
    """Every identifier a citation may resolve to, and the families that declare them.

    Through `ledger.collect()` rather than by walking the registry here. A family may own a
    *directory* — `spec/requirements/`, `decisions/`, `spec/changes/` — and reading one of those as
    a file is an `IsADirectoryError` rather than a wrong answer. There is one implementation of the
    declaration rule and this is not it."""
    if not os.path.exists(os.path.join(ROOT, config["registry"])):
        return None, None
    try:
        data = ledger.collect(ROOT, config)
    except SystemExit:
        return None, None
    # Retired identifiers, slices and change requests included: an oracle citing a withdrawn
    # requirement is stale reasoning, not a stale reference, and this check is about the second.
    return data.families, ledger.known_ids(data)


def main() -> int:
    config = ledger.load_config(ROOT, "scripts/ledger.config.json")
    families, declared = declared_everything(config)
    if families is None:
        sys.stderr.write("drift: no registry at " + config["registry"] + "\n")
        return 2

    docs = sources()
    absent = set()
    for _, text in docs:
        absent.update(ABSENT.findall(text))

    findings, seen = [], set()

    def note(kind, rel, token, detail):
        # A token cited six times is one stale reference, not six.
        key = (kind, token)
        if key in seen:
            return
        seen.add(key)
        findings.append((kind, rel, token, detail))

    # 1 · Identifiers. Only a token whose prefix names a registered family is claimed to be one,
    #     which is what keeps ordinary hyphenated prose out of the check.
    for rel, text in docs:
        for token in TOKEN.findall(text):
            if token in absent or ADR.fullmatch(token):
                continue
            if not any(ch.isdigit() for ch in token.rsplit("-", 1)[-1]):
                continue
            if ledger.family_for(token, families) is None:
                continue
            if token not in declared:
                note("identifier", rel, token, "declared nowhere the registry points at")

    # 2 · ADR numbers. An oracle citing a decision that was never accepted, or was superseded into
    #     a different file, is an oracle nobody can check.
    decisions = os.path.join(ROOT, config["decisions"])
    numbers = set()
    if os.path.isdir(decisions):
        for name in os.listdir(decisions):
            m = re.match(r"^(\d{3,})-", name)
            if m:
                numbers.add(m.group(1))
    for rel, text in docs:
        for token, number in ADR.findall(text):
            if token not in absent and number not in numbers:
                note("ADR", rel, token, "no such file in " + config["decisions"] + "/")

    # 3 · Project checks. Anything executable in `drift.d/` runs here — this is where a project
    #     puts the checks only it can make, once it has a surface to enumerate: its route set, its
    #     error catalogue, its CLI verbs. A non-zero exit is stale; stdout is the detail.
    plugins = os.path.join(HERE, "drift.d")
    if os.path.isdir(plugins):
        for name in sorted(os.listdir(plugins)):
            path = os.path.join(plugins, name)
            if name.startswith(".") or name.endswith(".md") or not os.access(path, os.X_OK):
                continue
            try:
                done = subprocess.run(
                    [path], cwd=ROOT, capture_output=True, text=True, timeout=120
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                note("drift.d", "drift.d/" + name, name, "did not run: " + str(exc))
                continue
            if done.returncode != 0:
                detail = (done.stdout + done.stderr).strip().replace("\n", "; ") or "exit " + str(
                    done.returncode
                )
                note("drift.d", "drift.d/" + name, name, detail)

    if not QUIET:
        if not findings:
            sys.stdout.write("drift: none — every identifier and decision cited still exists\n")
        else:
            sys.stdout.write("drift: %d stale reference(s)\n\n" % len(findings))
            width = max(len(kind) for kind, _, _, _ in findings)
            for kind, rel, token, detail in findings:
                sys.stdout.write("  %s  %s\n      %s — %s\n" % (kind.ljust(width), token, rel, detail))
            sys.stdout.write(
                "\nThese are maintenance findings, not defects. Report them as such and do not\n"
                "test against them: an oracle naming something that no longer exists produces a\n"
                "false finding every run until it is corrected. The run does not correct it.\n"
            )
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
