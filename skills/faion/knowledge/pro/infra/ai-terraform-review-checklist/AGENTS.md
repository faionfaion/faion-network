---
slug: ai-terraform-review-checklist
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Ai Terraform Review Checklist: codified platform / SRE practice that turns the recurring 'role-devops-engineer/AI-assisted infra review gate (Dockerfile + Helm + Terraform)' decision into a repeatable, auditable artefact.
content_id: "f13fbb846f55560c"
tags: [ai-terraform-review-checklist, infra, pro]
---
# Ai Terraform Review Checklist

## Summary

**One-sentence:** Ai Terraform Review Checklist: codified platform / SRE practice that turns the recurring 'role-devops-engineer/AI-assisted infra review gate (Dockerfile + Helm + Terraform)' decision into a repeatable, auditable artefact.

**One-paragraph:** Ai Terraform Review Checklist addresses the gap identified by the role-devops-engineer/AI-assisted infra review gate (Dockerfile + Helm + Terraform) playbook: docker-security-hardening exists, but the AI-generation-specific failure pattern catalog (USER 0, latest tag, COPY . without .dockerignore, single-stage with build tools, missing HEALTHCHECK) is the high-leverage 2026 content. / Helm-charts methodology covers authoring; no methodology covers reviewing AI-generated charts (missing resource limits, missing PDB, missing securityContext, broken templating with .Values nil, hardcoded namespaces). Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-devops-engineer/AI-assisted infra review gate (Dockerfile + Helm + Terraform) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-devops-engineer/AI-assisted infra review gate (Dockerfile + Helm + Terraform) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-llm-grounding | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-terraform-review-checklist.json` | JSON schema for the Ai Terraform Review Checklist output contract |
| `templates/ai-terraform-review-checklist.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-terraform-review-checklist.py` | Enforce Ai Terraform Review Checklist output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- upstream playbook: `role-devops-engineer/AI-assisted infra review gate (Dockerfile + Helm + Terraform)`
- external: [RAGAS](https://docs.ragas.io/) · [Anthropic agent design](https://docs.anthropic.com/en/docs/build-with-claude/agents)
