---
slug: tracker-github-copilot-workspace
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a Workspace PR template + gate-enforcement policy that forces issue → spec → plan → diff → PR through four explicit AI-edited gates with snapshot links.
content_id: "58bffe7c41b1f35c"
complexity: medium
produces: playbook-step
est_tokens: 4200
tags: [github-copilot, copilot-workspace, pull-request, agentic-pr, tracker]
---
# GitHub Copilot Workspace Four-Gate Pipeline

## Summary

**One-sentence:** Drive every GitHub ticket-to-PR through Copilot Workspace's four explicit gates (spec, plan, diff, PR) with a human edit point at each gate and a snapshot link in every Workspace PR.

**One-paragraph:** Drive every GitHub-hosted ticket-to-PR through Copilot Workspace's four explicit gates: (1) AI generates a current-state plus desired-state spec from the issue, (2) AI generates a file-level plan, (3) AI generates the diff, (4) AI opens the PR. The human can edit at every stage, and skipping any gate is a hard refusal — agents that go straight from issue to diff are configured to abort. Every Workspace PR includes an auto-attached comment with a read-only Workspace snapshot link so reviewers can see the spec and plan that produced the diff, not just the diff itself.

**Ефективно для:**

- GitHub orgs з Workspace seat-enabled.
- Compliance teams: spec + plan visible поряд із diff.
- Onboarding agent в monorepo — gates тримають його in scope.
- Audit trails: Workspace snapshot — durable reviewable artifact.

## Applies If (ALL must hold)

- Project is on GitHub with Copilot Workspace enabled.
- Issues carry enough text for spec generation (≥ 1 paragraph + AC).
- Reviewers expect spec + plan visibility, not just code diffs.

## Skip If (ANY kills it)

- Project on GitLab / Bitbucket / Forgejo — wrong runtime.
- Issues are one-liners with no spec material.
- Team has no review capacity for 4-gate output.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Copilot Workspace access | GitHub setting | org billing |
| Issue with ≥ 1-paragraph description + AC | Markdown | tracker |
| PR template `templates/pr-template.md` | Markdown | this methodology |

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
| `templates/pr-template.md` | PR description template embedding Workspace metadata + snapshot link. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tracker-github-copilot-workspace.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[tracker-gitlab-duo-developer-flow]]
- [[tracker-jira-rovo-mcp-agents]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
