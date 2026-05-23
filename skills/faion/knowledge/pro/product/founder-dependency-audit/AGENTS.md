---
slug: founder-dependency-audit
tier: pro
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Scores every revenue line, account, credential, and client relationship by 'breaks if founder steps away 4 weeks' to produce a ranked dependency register and remediation plan.
content_id: "ad894fe6a7470a07"
complexity: medium
produces: report
est_tokens: 5200
tags: [product, pro, audit, solo, exit-prep, continuity]
---
# Founder Dependency Audit

## Summary

**One-sentence:** Scores every revenue line, account, credential, and client relationship by 'breaks if founder steps away 4 weeks' to produce a ranked dependency register and remediation plan.

**One-paragraph:** Scores every revenue line, account, credential, and client relationship by 'breaks if founder steps away 4 weeks' to produce a ranked dependency register and remediation plan. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Exit prep: due-diligence buyer needs ranked dependency register before LOI.
- Sustainable solo ops: founder wants to take 4-week break without revenue collapse.
- Hiring gates: which dependencies must transfer to first hire before scaling.
- Insurance / continuity planning: which single points of failure to insure or document.

## Applies If (ALL must hold)

- Solo founder or micro-agency (1-5 people) with active revenue lines.
- ≥3 distinct revenue streams or ≥10 clients with named relationships.
- Founder has admin / billing access on critical SaaS, DNS, payment processor.
- A 4-week founder-absence scenario is plausible within the next 12 months.

## Skip If (ANY kills it)

- Company has dedicated ops / CTO / COO already holding parallel access.
- Single client / single revenue stream — audit reduces to one row, use a checklist.
- Pre-revenue stage — no production dependencies to audit yet.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Revenue line list | CSV/sheet with line_id, monthly_revenue, owner | billing / accounting |
| Account inventory | credentials manager export (1Password / Bitwarden) | founder's password vault |
| Client relationship map | CRM export or hand-written list | CRM / email |
| Vendor list | SaaS subscriptions list with admin owner | billing exports |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥6 testable rules with rationale + source incl. `skip-this-methodology` | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/05-examples.xml` | reference | Full worked example end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-founder-dependency-audit` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-founder-dependency-audit.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[owner-handover-sop-kit]]
- [[freelancer-to-saas-time-box]]
- [[portfolio-sunset-decision-frame]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
