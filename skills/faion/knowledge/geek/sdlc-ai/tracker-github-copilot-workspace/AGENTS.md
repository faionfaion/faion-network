---
slug: tracker-github-copilot-workspace
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Drive every GitHub-hosted ticket-to-PR through Copilot Workspace's four explicit gates: (1) AI generates a current-state plus desired-state spec from the issue, (2) AI generates a file-level plan, (3) AI generates the diff, (4) AI opens the PR.
content_id: "7456b92e7a6d2593"
tags: [github-copilot, copilot-workspace, pull-request, agentic-pr, tracker]
---
# GitHub Copilot Workspace Four-Gate Pipeline

## Summary

**One-sentence:** Drive every GitHub-hosted ticket-to-PR through Copilot Workspace's four explicit gates: (1) AI generates a current-state plus desired-state spec from the issue, (2) AI generates a file-level plan, (3) AI generates the diff, (4) AI opens the PR.

**One-paragraph:** Drive every GitHub-hosted ticket-to-PR through Copilot Workspace's four explicit gates: (1) AI generates a current-state plus desired-state spec from the issue, (2) AI generates a file-level plan, (3) AI generates the diff, (4) AI opens the PR. The human can edit at every stage, and skipping any gate is a hard refusal — agents that go straight from issue to diff are configured to abort. Every Workspace PR includes an auto-attached comment with a read-only Workspace snapshot link so reviewers can see the spec and plan that produced the diff, not just the diff itself.

## Applies If (ALL must hold)

- GitHub-hosted single-repo issues with well-scoped acceptance criteria.
- Bug fixes and small-to-medium features where reviewers want to see the agent's reasoning, not just the patch.
- Greenfield bootstrap tickets where the spec gate is the only chance to align on direction before scaffolding lands.
- Teams that already enforce branch protection requiring `Closes #N` in PR body — the four-gate flow guarantees the link.

## Skip If (ANY kills it)

- Multi-repo changes — Workspace is single-repo per session and the four-gate flow does not span repos.
- SLA-critical paths where the documented ~30% agentic PR fail-rate is unacceptable; route those through human-led changes.
- Teams that prefer the autonomous Copilot coding-agent flow (assign Copilot directly, no Workspace UI) — different contract.
- Trivial typo fixes pre-flagged auto-merge; gate cost exceeds the risk and slows trivial flow.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/sdlc-ai/sdlc-ai/`
