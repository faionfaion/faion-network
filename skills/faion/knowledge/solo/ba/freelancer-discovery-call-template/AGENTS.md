---
slug: freelancer-discovery-call-template
tier: solo
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a 30-minute freelancer discovery call template with a pre-filled question bank, a go/no-go scorecard, and a one-page proposal seed.
content_id: "c0c6eadd1bf7c270"
complexity: medium
produces: spec
est_tokens: 4200
tags: [freelancer, discovery-call, ba, solo, qualification]
---
# Freelancer Discovery Call Template

## Summary

**One-sentence:** Generates a 30-minute freelancer discovery call template with a pre-filled question bank, a go/no-go scorecard, and a one-page proposal seed.

**One-paragraph:** Enterprise BA elicitation techniques are over-engineered for a 30-min freelancer discovery call with one prospect and no formal stakeholder map. This methodology emits a stripped-down template: pre-filled question bank (5 sections: context, pain, success criteria, budget signals, decision process), a go/no-go scorecard, and a one-page proposal seed populated from the call notes. Output: 3 artefacts — call template, scorecard, proposal seed.

**Ефективно для:**

- Freelancer running prospect discovery calls weekly.
- Solo consultant qualifying leads before writing a proposal.
- Founder doing customer-discovery interviews adjacent to selling.
- Coaching a junior freelancer through their first paid call.

## Applies If (ALL must hold)

- Call length is ≤45 min (60+ uses different protocol).
- Single prospect, single decision-maker (no formal map needed).
- Goal includes both discovery + proposal (not pure discovery → use mom-test).
- Operator has authority to send proposal directly after.

## Skip If (ANY kills it)

- Enterprise client with procurement + multiple stakeholders — use formal elicitation.
- Pure customer-discovery (no sale intent) — use mom-test.
- Existing client (not discovery) — use account-review template.
- Public webinar / open Q&A — not a discovery call.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Prospect context | name + company + role + how they found you | calendar / CRM |
| Service offering | 1-line description + 3 packages | operator |
| Rate floor | minimum hourly / project rate | operator |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[mom-test]] | discovery discipline; question phrasing |
| [[active-listening]] | RASA pattern during the call |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routes by observable signal to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `freelancer_discovery_call_template_template_fill` | haiku | Template fill, no judgement. |
| `freelancer_discovery_call_template_evidence_check` | sonnet | Bounded comparison + judgement. |
| `freelancer_discovery_call_template_synthesis` | sonnet | Cross-input synthesis + final proposal. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the full output artefact |
| `templates/discovery-call-template.md` | Pre-filled 30-min call template with 5 sections |
| `templates/scorecard.md` | 5-axis go/no-go scorecard |
| `templates/proposal-seed.md` | 1-page proposal seed skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelancer-discovery-call-template.py` | Validate freelancer-discovery-call-template artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[mom-test]]
- [[active-listening]]
- [[stakeholder-communication]]
- [[selling-ideas]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on section coverage, listen ratio, and scorecard total. Any gate failure halts or routes to a no-go / repair conclusion.
