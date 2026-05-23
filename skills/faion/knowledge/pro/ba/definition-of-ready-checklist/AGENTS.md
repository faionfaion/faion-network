---
slug: definition-of-ready-checklist
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Outsource-grade DoR checklist gating stories before grooming: covers engineering readiness plus client-side dependencies (env access, data, regulator/legal/security sign-off).
content_id: "f9d825eef0dd72d1"
complexity: medium
produces: checklist
est_tokens: 4400
tags: [ba, pro, definition-of-ready, outsource, grooming, checklist]
---
# Definition Of Ready Checklist

## Summary

**One-sentence:** Outsource-grade DoR checklist gating stories before grooming: covers engineering readiness plus client-side dependencies (env access, data, regulator/legal/security sign-off).

**One-paragraph:** Definition Of Ready Checklist pins a recurring BA decision into an auditable artefact. It enforces a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. Inputs and triggers come from the engagement context; outputs feed a named downstream consumer (human or agent) without re-deriving the reasoning. The decision tree at `content/06-decision-tree.xml` routes every application to either an applicable rule or `skip-this-methodology`.

**Ефективно для:**

- Outsource / consulting BA running grooming for a foreign client.
- HealthTech / FinTech engagement with regulator sign-off on the critical path.
- Repeat 'estimated but blocked' stories burning sprint capacity.
- Mixed-team grooming where engineering + client PM + compliance must converge.

## Applies If (ALL must hold)

- You run grooming or estimation sessions for an outsource / consulting team.
- You depend on a client for environments, test data, or regulator/legal approvals.
- At least one story in the last quarter was estimated but stayed blocked on client-side dependency.
- You can name the client-side stakeholders (PM, security, legal, data, infra).

## Skip If (ANY kills it)

- You are an in-house team with full control of all environments and data.
- Team uses no-estimate flow with WIP limits — DoR is implicit in pull.
- Story is a research spike where 'ready' is intentionally fuzzy.
- You have fewer than 5 active stories at any time — overhead exceeds benefit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Client-side stakeholder map | markdown / yaml | Team CRM / client engagement doc |
| Backlog item (story / epic) | markdown / ticket | Jira / Linear / ADO |
| Compliance regime list (HIPAA, GDPR, SOC2, PCI) | yaml | Engagement contract / risk register |
| Prior DoR failure log | csv | Previous iterations of this methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source + skip rule | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-definition-of-ready-checklist` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/definition-of-ready-checklist.md` | Markdown checklist skeleton matching the 8-item shape pinned in content/01-core-rules.xml |
| `templates/definition-of-ready-checklist.schema.json` | JSON Schema for the structured checklist output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-definition-of-ready-checklist.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ba/AGENTS.md`
- [[requirement-quality-scorecard]]
- [[discovery-to-delivery-handover-protocol]]
- [[demo-recap-email-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, scope, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
