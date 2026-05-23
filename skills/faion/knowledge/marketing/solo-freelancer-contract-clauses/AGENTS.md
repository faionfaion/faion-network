# Solo Freelancer Contract Clauses

## Summary

**One-sentence:** Clause pack designed for a single technical freelancer signing direct contracts with mid-sized clients, replacing the standard $40k web-build SOW boilerplate with five lean, defensible provisions.

**One-paragraph:** `statement-of-work` covers a heavy SOW between two LLCs. SaaS-side ops-legal-basics covers ToS / Privacy. Solo freelancers landing $5–30k projects need neither — they need a small, opinionated clause pack: (1) IP assignment-on-PAID, not on-signed (the single most important inversion); (2) late-fee with automatic stop-work after N days unpaid; (3) kill fee for client-initiated termination (typically 30% of remaining); (4) mutual NDA scoped to the engagement; (5) jurisdiction defaulted to the freelancer's country with arbitration carve-out. The pack is meant to slot into an otherwise-simple email-signed agreement, with no MSA prereq. Anchored to "Inbound-to-signed-retainer in one client cycle" for the technical freelancer.

**Ефективно для:**

- Solo фрілансера, що підписує сам, без $2k legal review.
- Lean pack для B2B-сервісів $5-30k.
- IP-on-PAID, late-fee + auto-stop-work, mutual NDA, home-jurisdiction.
- Не enterprise MSA — звичайний email-signed agreement.

## Applies If (ALL must hold)

- Solo technical freelancer (one human, no employees, may have subcontractors).
- Client engagement is B2B services, sub-$30k initial project value.
- Freelancer wants to ship a signed agreement without a $2k lawyer review per deal.
- Local jurisdiction recognizes electronic signatures for service agreements.

## Skip If (ANY kills it)

- Engagement is with a regulated industry that mandates specific clauses (gov, healthcare, defense) — escalate to counsel.
- Client is an enterprise procurement org that pushes their MSA — negotiate within their MSA, not against it.
- Cross-border with hostile jurisdiction risk (sanctions-list, no treaty) — escalate to counsel.

## Prerequisites

- Freelancer's company / sole-trader registration in place.
- A baseline service-agreement document (one page) into which the clauses slot.
- A payment processor that supports invoicing with explicit due-dates (Stripe, Wise, etc.).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/AGENTS.md` | Parent group context |
| `pro/marketing/freelance-tax-cashflow-basics` if present | Sibling — the operational side of the contract |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules + self-routing anchors (run-the-checklist + skip-this-methodology) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with description + reason + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on preconditions → rule from `01-core-rules.xml` | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list, low cost. |
| `populate-evidence-fields` | sonnet | Per-section judgment: select correct evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change behaviour at the next iteration? |

## Templates

| File | Purpose |
|------|---------|
| `templates/solo-freelancer-contract-clauses.md` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/solo-freelancer-contract-clauses.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-freelancer-contract-clauses.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

- parent skill: `pro/marketing/`
- triggering activity: `p3-technical-freelancer/Inbound-to-signed-retainer in one client cycle`
- adjacent: `pro/pm/solo-change-order-mini-contract`, `pro/marketing/late-invoice-dunning-sequence`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.

