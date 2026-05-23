# US / UK / EU Compliance Matrix

## Summary

**One-sentence:** Side-by-side obligation matrix across US (CCPA/CPRA, state privacy), UK (UK-GDPR, DPA 2018), EU (GDPR, DSA, AI Act) covering entity registration, data handling, contracts, tax, so micro-agencies check obligations per market without re-reading three statutes.

**One-paragraph:** A solopreneur or micro-agency selling into US + UK + EU faces three overlapping but distinct compliance regimes. Each has its own data-protection law (CCPA/CPRA, UK-GDPR, GDPR), contract requirements (SCCs, IDTA, DPAs), tax regime (sales tax, VAT, VAT-OSS), and product-level obligations (DSA, AI Act). Without a matrix, the founder re-derives obligations every contract and misses non-obvious ones (CCPA opt-out for B2C, AI Act risk categories). This methodology produces a compliance-matrix.md per business covering: entity registration per market, data handling per category, contract templates per buyer type, tax obligations per threshold, product-level obligations per service. Output is auditable + reviewable by counsel.

**Ефективно для:**

- Solopreneur заключає US/UK/EU контракт без re-reading трьох статутів.
- Швидка перевірка — AI Act risk category для нового SaaS feature.
- Tax thresholds (CA $500k, VAT-OSS €10k) — не пропустити VAT registration.
- DPA / SCC / IDTA — який контракт template для якого buyer.

## Applies If (ALL must hold)

- Business sells digital services into US + UK + EU markets
- Business processes personal data of EU/UK/US residents
- Annual revenue or data-subject volume crosses any threshold (CCPA, VAT-OSS, AI Act)
- Counsel review needed before signing master agreements with enterprise buyers

## Skip If (ANY kills it)

- Single-market business (e.g. EU-only) — use the EU-specific methodology, not the matrix
- Business does not process personal data and does not sell to consumers — most obligations don't apply
- Enterprise legal team already maintains a matrix — use theirs

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Business entity / VAT registrations | registration certificates | founder + accountant |
| Revenue + customer location breakdown | billing data | ops |
| Counsel contact (privacy + tax) | engagement letter | founder |
| Product feature list with data flows | product wiki | product owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[contractor-agreement-template-us-uk-eu]] | Contract template references this matrix |
| [[agency-year-end-close-checklist]] | Annual close uses the matrix for tax obligations |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure with input/action/output | ~700 |
| `content/05-examples.xml` | medium | Worked example end-to-end | ~500 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `threshold_check` | haiku | Numeric comparison |
| `contract_choice` | sonnet | Bounded judgment on buyer-type → template |
| `counsel_brief` | opus | Cross-jurisdiction synthesis for counsel review |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | Skeleton template |
| `templates/skeleton.md` | Skeleton template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-us-uk-eu-compliance-matrix.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[contractor-agreement-template-us-uk-eu]]
- [[agency-year-end-close-checklist]]
- [[secrets-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
