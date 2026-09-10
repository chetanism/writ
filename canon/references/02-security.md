# Security, conditioned on the domain

Ask the questions this project's domain earns, and skip the rest. A todo app asked about card-data
scope learns the process wastes its time; a payments app not asked learns it too late.

## Step 1 — pick the profile

Ask one question with these as options, and let the user pick more than one:

| Profile | You are in it if | Non-negotiables |
|---|---|---|
| **Personal / internal tool** | One org, trusted users, no regulated data | Auth, backups, secrets not in the repo |
| **Multi-tenant B2B SaaS** | Customers must never see each other's data | A tenancy invariant enforced at the data layer, audit trail, per-tenant export and deletion |
| **Consumer app with accounts** | Anyone can sign up | Account takeover defence, rate limits, abuse controls, privacy rights |
| **Payments / fintech** | You move or hold money | Idempotent writes, immutable ledger, reconciliation, PCI scope decision, sanctions/KYC posture |
| **Health / clinical** | Identifiable health data | Access purpose logging, minimum necessary, retention limits, a named data protection lead |
| **Developer platform / public API** | Third parties hold credentials | Scoped tokens, revocation, quotas, versioning, a documented deprecation policy |
| **Content / social** | Users publish to other users | Moderation, reporting, takedown, jurisdictional obligations |

## Step 2 — the universal five

Ask these regardless of profile. They are short and they change the architecture.

1. **What is the worst realistic breach?** Not the worst imaginable — the realistic one. The answer
   tells you which control matters most, and it belongs in the BRD's risk section verbatim.
2. **Who is the adversary?** A bored user, a competitor's customer, an insider, a script, a funded
   attacker. Each implies a different first control, and "all of them" implies none.
3. **Is there a boundary that must never be crossed?** If yes, that is an **invariant**, not a
   requirement — numbered `INV-*`, enforced at the lowest layer that can enforce it, and a defect
   to violate rather than a style preference.
4. **What does "authenticated" mean here?** Sessions, API keys, OIDC, machine-to-machine, or
   several. Then: what does *revocation* mean, and how fast must it take effect?
5. **What must be recorded, and who reads it?** An audit trail nobody reads is a storage bill. An
   audit trail written by the same transaction as the thing it records is evidence.

## Step 3 — profile questions

**Multi-tenant B2B SaaS**
- Where is the tenant boundary enforced — the database, or application code? *Push for the
  database. Application convention fails silently the first time somebody writes a new query.*
- May one tenant's data be read for analytics, benchmarking, or model training? A "no" written as
  an invariant is a commercial asset, not just a control.
- Is there a support path that reads customer data, and is using it audited and visible?
- What does deleting a tenant do — and how long until it is irreversible?

**Payments / fintech**
- Is the same payment instruction submitted twice one payment or two? *Idempotency key, its scope,
  and its lifetime.*
- Which records are append-only? Anything that answers "how much" usually is.
- Do you touch card data, or is it tokenised by a processor? This one answer decides PCI scope.
- What is the reconciliation process, and what does a mismatch trigger?

**Consumer app with accounts**
- Password, magic link, or federated? If password: what KDF, and what is the reset flow's weakest
  step?
- What stops credential stuffing — rate limits by what key, and lockout with what recovery?
- What are the privacy rights obligations: export, deletion, correction, and in what timeframe?
- What is abusable at scale — invites, uploads, notifications, search?

**Developer platform / public API**
- Scopes: the vocabulary, and whether it is a one-way door. *It is. Adding a scope later is
  additive; changing one's meaning is a breaking change nobody can see.*
- Are keys hashed at rest, and does revocation destroy the secret or set a flag?
- Quotas: per key, per tenant, or both — and what does exhaustion return?
- Can a caller act on behalf of someone else, and how is that recorded?

**Health / clinical, Content / social**
- Who may read a record, and is the *purpose* of each access recorded?
- What is the retention limit, and what enforces it — a policy document or a job?
- For content: what is reportable, who acts on a report, and in what time?

## Step 4 — write it down

- Behaviour the system must have → `FR-SEC-*`.
- A property that must always hold → `INV-*`, in the BRD's invariants section, with the layer that
  enforces it named.
- A legal or contractual obligation → `CMP-*`.
- A measurable target (patch latency, key rotation period) → `NFR-SEC-*`.

Two rules worth stating in the process document while they are fresh:

- **A secret is recognised by the shape of its name, not by a list.** Anything matching `_SECRET`,
  `_TOKEN`, `_KEY`, `_PASSWORD`, `_CREDENTIALS` is redacted in logs and in configuration dumps.
  A list is a thing somebody forgets to add to.
- **A configuration failure names variables, never values.**
