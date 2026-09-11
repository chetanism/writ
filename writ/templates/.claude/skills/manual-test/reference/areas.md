# Areas, and what "correct" means in each

One section per area. Each carries the **identifiers** it is answerable to, the **surface** a walk
can reach it through, the **oracles** — falsifiable statements the system must satisfy, which is
what turns poking around into testing — and the **traps**, which are places a tester is more likely
to be wrong than the code is.

An oracle is written so that a run can be **wrong about it**. *"Orders are created correctly"* is
not one. *"A checkout against an expired cart leaves no order, no reservation, no payment intent
and no audit row"* is.

Read only the sections the chosen area covers. `whole app` draws two or three sections per depth
band rather than reading them all.

**This file holds the reasoning, not the enumerations.** Anything countable — the route set, the
error catalogue, the capability descriptors — is read live from `harness.sh surface`, which cannot
be stale. What is written down here is the part that cannot be queried: why a given answer is the
right one, and where a tester is more likely to be wrong than the code is. Where the two disagree,
`surface` wins. `drift.py` checks that every identifier and decision named below still exists, and
a run reports what it finds rather than correcting it.

---

> **Generated at bootstrap, and grown every slice.** At bootstrap there is no code, so the oracles
> below come from the only falsifiable statements that exist yet: the **invariants** in
> `writ/spec/invariants.md`.
> That is the right starting point and a thin one. **DoD-11 is what keeps this file alive** — a
> slice that establishes or changes an invariant adds or updates its oracle here, and a slice that
> found a trap the hard way writes it down while it still stings.
>
> One section per requirement area (`writ/spec/requirements/<AREA>/`). Delete this blockquote and the specimen section below once the
> real sections are written.

## 1 · The specimen area

**IDs** the requirement, invariant and non-functional identifiers this area answers to
**Surface** how a walk reaches it — routes, commands, jobs. *"Not built yet"* is a valid entry at
bootstrap, and is itself worth knowing before a session spends steps looking for it.

**Oracles**
- One falsifiable statement per line, each ending in the identifier it comes from. Prefer the
  shape *"doing X leaves exactly Y and nothing else"* over *"X works"* — the first can be checked,
  and the second can only be agreed with.
- State what is **indistinguishable** where the design says so: two conditions that must produce
  one answer are an oracle, and a run that can tell them apart has found something.
- Where an oracle exists **because a thing does not exist**, name the absent thing and exempt it:
  `<!-- drift:absent some.token -->` on the same line. The exemption travels with the sentence that
  needs it rather than living in a list elsewhere.

**Traps**
- Places a tester will misread the system and file a finding against itself. Empty at bootstrap;
  every entry here was earned by somebody being wrong.
