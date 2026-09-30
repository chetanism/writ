# Conventions

> **What this is.** The rules set here and binding afterwards, one numbered section per area of the
> code. `CLAUDE.md` §*Where the conventions are* says which section to read for what you are about
> to touch. **Read those sections in full before writing code**, and only those.
>
> **Each bullet is the rule and its citation, and nothing else.** The bug that taught it, the
> alternative it rejected and how far the damage reached are already in the slice summary or ADR it
> cites. Write the rule, cite where it came from, and stop. **A rule that has become a check — a
> lint rule, a test, a `ledger.py` check — is the check's name and no prose at all**, so *can this
> be a check?* is the first question a new convention gets.
>
> **This file has its own cap**, in `context_budget` in `scripts/ledger.config.json`, because a cap
> on `CLAUDE.md` alone moves the growth here. When it warns, `/context-compact` takes each bullet
> back to its rule and citation; it never deletes a rule that still holds.

## How it changes

| | |
|---|---|
| **A new rule** | Added by the slice that sets it (DoD-8), to its area's section, replacing whatever it supersedes. The citation, in brackets after the rule, is the slice's identifier and the ADR's number if there is one |
| **A new area** | A new section at the end, and a row for it in `CLAUDE.md`'s routing table in the same commit. **Sections are never renumbered**: the routing table and old summaries cite them by number |
| **A rule for every area** | It goes in `CLAUDE.md`'s *spans every area* list instead, and nowhere here. That list stays short — ten rules at most |
| **A rule that became a check** | Replace its prose with the check's name, in the commit that adds the check |
| **A rule that no longer holds** | Deleted, in the slice that ends it. Git holds it, and a rule left standing here is read as a live one |

---

## 1. Tests and the gate

- **Test files sit beside their source.** <Unit test suffix> is a unit test; <Integration test
  suffix> needs a live dependency and runs only under <Integration test command>.
- **Never put an annotation-shaped string in a test file that is not a real test** — the collector
  reads it as evidence. (`DEVELOPMENT-PROCESS.md` §6.1)

## 2. Data and migrations

*No rules yet.*

## 3. Interfaces — routes, commands, errors

- **Every demo-facing command takes `--json` and prints exactly one object.**
  (`DEVELOPMENT-PROCESS.md` §5)

## 4. Security and credentials

*No rules yet.*

## 5. The user interface

*No rules yet.*
