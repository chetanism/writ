#!/usr/bin/env python3
"""The kit's own templates, bootstrapped into a project and held to the kit's own check.

    python3 canon/tests/test_templates.py

`templates/scripts/test_ledger.py` tests the *tool* against a synthetic tree it writes itself.
Nothing tested the *templates*, and the gap is not academic: the shipped `DEVELOPMENT-PROCESS.md`
declared `DoD-1` against a registry pattern of `DoD-NN`, and the shipped `ledger.config.json`
pointed `requirements.dir` at the directory that holds the area registers, so the first
`ledger.py check` of every bootstrapped project failed on documents the kit wrote itself. Both are
one run of this file away from being obvious.

**This test lives in the kit and never ships.** `templates/` is copied into the projects the kit
bootstraps; a test in there that reaches back to the kit would be a test about a directory the
project does not have.

What it does is the mechanical half of phases 6 to 10: copy the tree, declare the identifiers the
traceable families need, answer every `<placeholder>` with a filler, and run the tool. The half it
does not do is the interview — so a green run means *the documents the kit ships agree with each
other and with the tool*, which is exactly the claim that was untested.
"""

from __future__ import annotations

import importlib.util
import io
import json
import os
import re
import shutil
import sys
import tempfile
import unittest

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(KIT, "templates")

SPEC = importlib.util.spec_from_file_location("ledger", os.path.join(TEMPLATES, "scripts", "ledger.py"))
ledger = importlib.util.module_from_spec(SPEC)
sys.modules["ledger"] = ledger
SPEC.loader.exec_module(ledger)


# --------------------------------------------------------------------------------------------
# The fixture bootstrap
# --------------------------------------------------------------------------------------------

DATE = "2026-01-01"
FILLER = "filled in by the interview"

# The two areas the fixture declares. `FR` and `NFR` are traceable and ship with no identifiers —
# deliberately, because inventing a requirement is the interview's job — so a bootstrap that
# declared none would fail the registry's own integrity check. One area each is enough to prove
# the registry, the ledger, the index and the detail track agree about where a requirement lives.
AREAS = {
    "FR-ACC": ("Accounts", [("FR-ACC-01", "Somebody with an address nobody holds can open an account.")]),
    "NFR-OBS": ("Observability", [("NFR-OBS-01", "Every write is attributable to an account and a time.")]),
}

AREA_REGISTER = """# {area} — {name}

The requirements of one area, one row each.

| ID | Requirement | Target | Since | Status |
|---|---|---|---|---|
{rows}
"""



def answer(placeholder: str) -> str:
    """What the interview would have put where this placeholder is.

    Typed, because three of the checks read the value rather than its presence: a changelog row
    wants a real date, and the sizing tiers want numbers. Everything else only has to stop being
    a placeholder."""
    inner = placeholder[1:-1]
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}|YYYY-MM-DD", inner):
        return DATE
    if re.fullmatch(r"\d+", inner):
        return inner
    return FILLER


def fill_line(line: str) -> str:
    """Answer every placeholder the tool would flag on this line, and nothing else.

    Through the tool's own two expressions rather than a third one of this file's, so the filler
    cannot drift from what it is meant to satisfy. The check reads a line with its code spans
    collapsed to `…`, because code is notation rather than a gap — `slice/<ID>-<slug>` is how a
    finished document describes a shape — so that collapsed form is what decides *whether* a span
    is a placeholder, while the raw line is where it is *replaced*. A placeholder that straddles a
    code span reads as one thing to the check and as three to anything that splits on backticks
    first, which is the shape this got wrong on its first run."""
    flagged = set(ledger.placeholders(ledger.INLINE_CODE.sub("`…`", line)))
    if not flagged:
        return line

    def resolve(match):
        raw = match.group(0)
        if raw in flagged or ledger.INLINE_CODE.sub("`…`", raw) in flagged:
            return answer(raw)
        return raw

    return ledger.PLACEHOLDER.sub(resolve, line)


def fill(text: str) -> str:
    return "\n".join(fill_line(line) for line in text.split("\n"))


def bootstrap(root: str) -> None:
    """Phases 6 to 10, minus the interview."""
    shutil.copytree(TEMPLATES, root, dirs_exist_ok=True)
    for junk in (".DS_Store", "__pycache__"):
        for here, dirs, files in list(os.walk(root)):
            if junk in dirs:
                shutil.rmtree(os.path.join(here, junk))
            if junk in files:
                os.remove(os.path.join(here, junk))

    # Phase 6 — the area registers, one file per area, beside the detail files that elaborate them.
    for area, (name, rows) in AREAS.items():
        directory = os.path.join(root, "canon", "spec", "requirements", area)
        os.makedirs(directory, exist_ok=True)
        table = "\n".join("| %s | %s | M1 | v0.1 | active |" % row for row in rows)
        write(os.path.join(directory, "index.md"), AREA_REGISTER.format(area=area, name=name, rows=table))

    # Phases 6 to 9 — every remaining question answered. The templates carry the guidance
    # blockquotes a real bootstrap deletes; leaving them is harmless and keeps the diff honest
    # about what this fixture did and did not do.
    for here, _dirs, files in os.walk(root):
        for name in files:
            # `.yml` as well as `.md`: `gate.yml` ships one placeholder per gate role, and an
            # unfilled gate command is the most expensive thing the bootstrap can leave behind —
            # it passes every document check and fails on the first pull request.
            if not name.endswith((".md", ".yml")):
                continue
            path = os.path.join(here, name)
            write(path, fill(read(path)))

    # Phase 8 — the tracker answer. The shipped config says `github`, and slice zero ships
    # `queued`, so no issue is required yet; the fixture keeps the shipped answer rather than
    # weakening the check it turns on.
    json.loads(read(os.path.join(root, "scripts", "ledger.config.json")))  # it has to parse


def read(path: str) -> str:
    with io.open(path, encoding="utf-8") as handle:
        return handle.read()


def write(path: str, text: str) -> None:
    with io.open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def run(root: str, *argv):
    err, out = io.StringIO(), io.StringIO()
    import contextlib

    with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
        code = ledger.main(list(argv) + ["--root", root])
    return code, err.getvalue()


# --------------------------------------------------------------------------------------------
# The tests
# --------------------------------------------------------------------------------------------


class BootstrappedTemplatesTest(unittest.TestCase):
    """A project made out of the shipped templates passes the shipped check."""

    @classmethod
    def setUpClass(cls):
        cls.root = tempfile.mkdtemp()
        bootstrap(cls.root)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root, ignore_errors=True)

    def test_the_tools_own_suite_passes_where_it_was_copied_to(self):
        """The suite travels with the tool, so it has to run from the project it lands in."""
        import subprocess

        done = subprocess.run(
            [sys.executable, os.path.join(self.root, "scripts", "test_ledger.py")],
            capture_output=True,
            text=True,
            cwd=self.root,
        )
        self.assertEqual(done.returncode, 0, done.stderr[-4000:])

    def test_generating_the_ledger_reports_nothing(self):
        """Every traceable family yields identifiers, every dependency resolves, no cycles."""
        code, err = run(self.root, "all")
        self.assertEqual(code, 0, err)

    def test_the_bootstrapped_tree_passes_check(self):
        """The one that matters. A non-zero exit here means a document the kit ships disagrees
        with another document the kit ships — which is the failure the kit exists to make loud."""
        run(self.root, "all")
        code, err = run(self.root, "check")
        self.assertEqual(code, 0, err)

    def test_stats_runs_against_the_freshly_bootstrapped_tree(self):
        """Slice zero runs it before there is a single measurement to report, and a traceback
        there is the first thing a new project would see the tool do."""
        code, err = run(self.root, "stats")
        self.assertEqual(code, 0, err)

    def test_the_area_register_is_not_read_as_a_detail_file(self):
        """`requirements.dir` holds the area registers *and* the detail files, so the tool has to
        tell them apart by name. It could not, and every bootstrap failed on its own register."""
        details = ledger.parse_details(self.root, "canon/spec/requirements")
        self.assertEqual([], [d.path for d in details])

    def test_the_generated_index_lists_the_declared_requirements(self):
        run(self.root, "all")
        index = read(os.path.join(self.root, "canon", "INDEX.md"))
        for area, (_name, rows) in AREAS.items():
            for ident, _text in rows:
                self.assertIn(ident, index, area + " is declared and the index does not list it")


    def test_the_drift_check_runs_against_a_bootstrapped_tree(self):
        """`harness.sh drift` runs before every `/manual-test` walk and a non-zero exit is a stop.

        It re-parsed the registry rather than going through the tool, so a family owning a
        *directory* — `spec/requirements/`, `decisions/`, `spec/changes/`, `process/work-orders/`,
        four of the shipped rows — raised `IsADirectoryError` and no project the kit produced could
        ever walk. Exit 1 is a real answer here (a stale citation); a traceback is not."""
        import subprocess

        drift = os.path.join(self.root, ".claude", "skills", "manual-test", "drift.py")
        done = subprocess.run([sys.executable, drift], capture_output=True, text=True, cwd=self.root)
        self.assertNotIn("Traceback", done.stderr, done.stderr[-2000:])
        self.assertIn(done.returncode, (0, 1), done.stderr[-2000:])


class ShippedDocumentsTest(unittest.TestCase):
    """Cheap structural claims about the raw templates, checkable without a bootstrap."""

    def setUp(self):
        registry = read(os.path.join(TEMPLATES, "canon", "spec", "ID-REGISTRY.md"))
        self.families = ledger.parse_registry(registry)

    def test_every_identifier_the_templates_declare_fits_its_families_pattern(self):
        """The registry fixes each family's width and the check refuses an identifier outside it.
        A template that ships identifiers of its own has to obey the registry it ships beside."""
        wrong = []
        for here, _dirs, files in os.walk(os.path.join(TEMPLATES, "canon")):
            for name in files:
                if not name.endswith(".md"):
                    continue
                path = os.path.join(here, name)
                rel = os.path.relpath(path, TEMPLATES)
                for ident, _cells in ledger.declared_rows(read(path), "*"):
                    fam = ledger.family_for(ident, self.families)
                    if fam is not None and not re.fullmatch(fam.regex, ident):
                        wrong.append(rel + ": " + ident + " does not fit " + fam.pattern)
        self.assertEqual([], sorted(set(wrong)))

    def test_every_family_the_registry_declares_owns_something_that_exists(self):
        """A registry row pointing at a document the kit does not ship is a row nobody notices is
        wrong until a project is already built on it."""
        missing = []
        for fam in self.families:
            for candidate in (
                os.path.join(TEMPLATES, "canon", fam.owner),
                os.path.join(TEMPLATES, fam.owner),
            ):
                if os.path.exists(candidate):
                    break
            else:
                missing.append(fam.family + " owns " + fam.owner)
        self.assertEqual([], missing)


class BranchCheckTest(unittest.TestCase):
    """The shell inside `traceability.yml`, run against the filenames it will actually meet."""

    def setUp(self):
        workflow = read(os.path.join(TEMPLATES, ".github", "workflows", "traceability.yml"))
        hit = re.search(r"\|\s*(grep -E '[^']*'\s*\|\s*grep -vE? '[^']*')", workflow)
        self.assertIsNotNone(hit, "traceability.yml no longer filters the changed-file list")
        self.pipeline = hit.group(1)

    def filter(self, paths):
        import subprocess

        done = subprocess.run(
            ["sh", "-c", "printf '%s\\n' \"$@\" | " + self.pipeline + " || true", "sh"] + paths,
            capture_output=True,
            text=True,
        )
        return [line for line in done.stdout.split("\n") if line]

    def test_a_detail_file_is_still_claimed_by_the_branch_rule(self):
        self.assertEqual(
            ["canon/spec/requirements/FR-ACC/FR-ACC-01.md"],
            self.filter(["canon/spec/requirements/FR-ACC/FR-ACC-01.md"]),
        )

    def test_an_area_register_is_not(self):
        """`/change-request apply` edits `<AREA>/index.md` on a `cr/` branch. Read as a detail
        file it demanded the branch be called `req/index`, which no skill ever creates — so every
        applied change request failed CI."""
        self.assertEqual(
            [],
            self.filter(
                [
                    "canon/spec/requirements/README.md",
                    "canon/spec/requirements/FR-ACC/index.md",
                    "canon/spec/requirements/NFR-OBS/index.md",
                ]
            ),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
