---
slug: ai-in-project-management
tier: geek
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "PMBOK 8's first AI appendix as an operating frame — principles for ethical AI use, AI-assisted decision traceability, sustainable delivery — with DORA paradox guards."
content_id: "1a6c16a78a705add"
complexity: deep
produces: decision-record
est_tokens: 4100
tags: [ai-in-pm, pmbok-8, productivity-paradox, dora, decision-traceability]
---
# Ai In Project Management

## Summary

**One-sentence:** PMBOK 8's first AI appendix as an operating frame — principles for ethical AI use, AI-assisted decision traceability, sustainable delivery — with DORA paradox guards.

**One-paragraph:** PMBOK 8's first AI appendix as an operating frame — principles for ethical AI use, AI-assisted decision traceability, sustainable delivery — with DORA paradox guards. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** PM-у, який пише AI-decision policy — щоб PMBOK 8 alignment не залишався паперовим документом.

## Applies If (ALL must hold)

- Org is adopting PMBOK 8 alignment.
- AI is being introduced into PM rituals (risk, scheduling, reporting).
- AI-decision documentation policy is on the roadmap.
- DORA baseline metrics are tracked.

## Skip If (ANY kills it)

- Single-person, short-duration tasks where PM overhead exceeds coordination benefit.
- Regulated industries without established AI decision documentation in compliance framework.
- Team has not established baseline metrics — AI optimisation without baseline cannot demonstrate improvement.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| PMBOK 8 reference | doc | PMI |
| DORA baseline | dashboard | engineering metrics tool |
| AI-decision documentation policy draft | doc | compliance |
| AI integration plan | Markdown | PM lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/pm-agile/ai-in-project-management` | Sister framework (pm-agile variant) — same paradox + audit rules. |
| `geek/pm/project-manager/ai-pm-tool-integration-recipes` | Concrete recipes the policy applies to. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `policy-mapping` | sonnet | Map PMBOK 8 sections to current rituals. |
| `decision-record-scaffold` | haiku | Template fill per decision. |
| `audit-trail-narrative` | opus | Cross-decision synthesis for compliance. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | AI-decision record skeleton: model + input hash + reviewer + approved/modified/rejected + rationale. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-in-project-management.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[ai-pm-tool-integration-recipes]]
- [[ai-powered-pm-tools]]
- [[ai-earned-value-management]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to adopt PMBOK 8 + AI traceability operating frame (baseline + alignment + policy draft) or block until prerequisites exist. Run at adoption kickoff before any AI tool is wired.
