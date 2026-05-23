---
slug: beta-cohort-recruitment
tier: solo
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Recruits a private-beta / design-partner cohort with NDA, expectations contract, feedback cadence, and exit ramp — distinct from open user-interview recruiting."
content_id: "605e84f9021438d9"
complexity: medium
produces: playbook-step
est_tokens: 4000
tags: [private-beta, design-partner, recruitment, nda, research]
---
# Private-Beta / Design-Partner Cohort Recruitment

## Summary

**One-sentence:** Recruits a private-beta / design-partner cohort with NDA, expectations contract, feedback cadence, and exit ramp — distinct from open user-interview recruiting.

**One-paragraph:** Open user-interview recruiting collects opinions; design-partner cohorts collect committed feedback. This methodology pins the difference: an NDA and expectations contract gate entry, a fixed cadence (weekly write-up + monthly call) governs engagement, and a named exit ramp prevents dead-weight members from inflating the cohort. Output: a recruitment playbook step with cohort target, vetting checklist, signed contract template, and a kill-criterion for members who miss two cadence cycles.

**Ефективно для:**

- Solo SaaS founder pre-launch building a paying-beta cohort.
- PM seeking design partners for a vertical pivot.
- Indie operator who wants signed commitment beyond newsletter sign-ups.
- Researcher recruiting ongoing-feedback partners, not one-off interviewees.

## Applies If (ALL must hold)

- Recruiting a private-beta or design-partner cohort (not open interviews).
- Cohort target size 5–25 named partners.
- Partners will give recurring feedback (≥4 contact points).
- Operator can offer something in return (early access, pricing lock, naming credit).

## Skip If (ANY kills it)

- Recruiting >25 members — design-partner discipline breaks; switch to closed beta.
- Need is a one-off interview — use a research interview methodology.
- Operator cannot honour partner commitments (busy quarter).
- Product is too early to give partners meaningful access (alpha-only build).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Partner profile criteria | list (segment + role + signals) | research brief |
| NDA template | doc / pdf | legal repo |
| Expectations contract template | md | this methodology |
| Cadence calendar | ICS / Linear | operator scheduler |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/researcher/problem-validation` | validation discipline upstream of design-partner ask |
| `solo/product/beta-charter-template` | charter shape consumed at cohort opening |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-beta-cohort-recruitment` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/beta-cohort-recruitment.md` | Markdown skeleton for the playbook-step artefact, matching content/02-output-contract.xml |
| `templates/beta-cohort-recruitment.schema.json` | JSON Schema seed + filled fixture for the playbook-step artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-beta-cohort-recruitment.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[beta-charter-template]]`
- `[[problem-validation]]`
- `[[discovery-research-handoff-template]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
