---
slug: tracker-gitlab-duo-developer-flow
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a duo-flows YAML wiring Developer / Code Review / Software Development / CI-CD Flows to issue labels and protected-branch rules, with GitLab ≥ 18.8 as the floor.
content_id: "b4c3aa3f9fce2c82"
complexity: medium
produces: config
est_tokens: 4200
tags: [gitlab, gitlab-duo, merge-request, agent-platform, tracker]
---
# GitLab Duo Agent Platform Developer Flow

## Summary

**One-sentence:** Drive issue-to-MR through GitLab Duo named flows (Developer, Code Review, Software Development, CI/CD) triggered by labels like `agent:implement` on GitLab ≥ 18.8, respecting protected-branch + approval rules.

**One-paragraph:** Drive every GitLab issue-to-merge-request transition through the GitLab Duo Agent Platform's named flows: Developer Flow turns an issue into an MR, Code Review Flow runs automated review on the MR, Software Development Flow handles multi-step plan-before-execute changes, and CI/CD Flows handle pipeline migrations and failing-build fixes. Every flow respects the GitLab project's protected-branch rules, CODEOWNERS, and approval-rule policies — the human approver still merges. Triggers are issue labels (`agent:implement`) or scheduled pipelines, never raw API calls. Pre-18.8 GitLab versions are explicitly out of scope because of the locking bug plus feature-flag config issues tracked in GitLab incident #21171.

**Ефективно для:**

- GitLab orgs з Duo Agent Platform license.
- Protected-branch repos з approval rules.
- Pipeline migrations: CI/CD Flow ідеальна для них.
- Failing-build triage: автоматичне fix proposal.

## Applies If (ALL must hold)

- GitLab self-managed or SaaS ≥ 18.8 with Duo Agent Platform licensed.
- Projects use protected branches + approval rules.
- Issue labels drive automation (no raw API triggers).

## Skip If (ANY kills it)

- GitLab < 18.8 — locking bug invalidates the flows.
- Project on GitHub / other forge — wrong runtime.
- No approval-rule policy — flows would merge without review.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| GitLab ≥ 18.8 | version check | infra |
| Duo Agent Platform license | GitLab subscription | billing |
| Approval-rule policy | GitLab setting | project settings |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/duo-flows.yaml` | GitLab Duo Agent Platform flows config mapping labels to named flows. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tracker-gitlab-duo-developer-flow.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[tracker-github-copilot-workspace]]
- [[tracker-jira-rovo-mcp-agents]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
