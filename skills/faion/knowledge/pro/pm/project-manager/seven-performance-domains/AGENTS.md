---
slug: seven-performance-domains
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: PMBoK 8's seven canonical domains (Governance, Scope, Schedule, Finance, Stakeholders, Resources, Risk); audit walks them in fixed order and emits artefact / owner / status / next-action per domain.
content_id: "14b9ca9570c3c135"
complexity: medium
produces: rubric
est_tokens: 4000
tags: [pmbok, domains, governance, project-planning, audit]
---
# Seven Performance Domains (PMBoK 8)

## Summary

**One-sentence:** PMBoK 8's seven canonical domains (Governance, Scope, Schedule, Finance, Stakeholders, Resources, Risk); audit walks them in fixed order and emits artefact / owner / status / next-action per domain.

**One-paragraph:** PMBoK 8 reorganises project management into seven performance domains: Governance, Scope, Schedule, Finance, Stakeholders, Resources, Risk. Quality, Communications, and Procurement are integrated throughout, not standalone. Each domain maps to observable artefacts and measurable outcomes. The canonical list is fixed — agents must never invent an 8th domain or reintroduce 'Integration Management' / 'Quality' as standalone items. Audit walks the seven in fixed order and emits artefact_path | MISSING + owner + last_updated + status + next-action per domain.

**Ефективно для:**

- Structuring a project charter or status pack around a known taxonomy
- Auditing an existing plan: walk each domain, surface missing artefacts
- Weekly project status dashboard: one panel per domain, RAG per outcome
- Onboarding a PM agent — seven domains is the smallest anchor that covers everything

## Applies If (ALL must hold)

- Structuring a project charter or status pack around a known taxonomy
- Auditing an existing project plan: walk each domain and surface missing artefacts
- Building a weekly project status dashboard (one panel per domain, RAG per outcome)
- Tailoring methodology selection — domains are stable; processes inside them vary by approach
- Onboarding a PM agent: seven domains is the smallest anchor that still covers everything

## Skip If (ANY kills it)

- Pure-Scrum teams where Scrum events already cover domains implicitly
- Solopreneur projects under 1 week with a single deliverable
- Shops still on PMBoK 6 in mid-project — switching narrative confuses sponsors
- Domain-driven design conversations — overloaded term

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| PMBoK edition pin | string | system prompt — '8' |
| Project root | path | workspace containing project artefacts |
| Threshold table | YAML | team consensus for RAG |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ref-pmbok]] | Edition vocabulary + EVM constants |
| [[six-core-principles]] | PMBoK 8 principles audited alongside domains |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: canonical-seven, fixed-domain-order, audit-before-steering, gap-equals-risk, default-to-governance | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `walk-domains` | haiku | Mechanical artefact existence check |
| `status-per-domain` | sonnet | Threshold comparison + next-action sentence |
| `gap-to-risk` | sonnet | Map missing artefacts to risk-register entries |

## Templates

| File | Purpose |
|------|---------|
| `templates/domain-audit.md` | Seven-row audit table per domain: artefact / owner / last-updated / status / next-action |
| `templates/domain-artefact-map.yaml` | Mapping table from canonical domains to expected artefacts |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/domain-audit.py` | Walk seven domains against a project root; emit JSON gap matrix | Pre-steering-committee; weekly |
| `scripts/validate-seven-performance-domains.py` | Validate audit output has exactly 7 domains in canonical order | Pre-commit |

## Related

- parent skill: `pro/pm/project-manager/`
- [[ref-pmbok]]
- [[six-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
