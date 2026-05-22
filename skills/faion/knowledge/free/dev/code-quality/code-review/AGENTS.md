---
slug: code-review
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a structured code-review report (5 comment kinds × 6 categories) with PR-size + comment-count gates, never auto-approving.
content_id: "ee8a70147c263798"
complexity: medium
produces: report
est_tokens: 3600
tags: [code-review, pr, conventional-comments, quality]
---
# Code Review

## Summary

**One-sentence:** Reviews a PR against six categories with five-kind comment labels, capping comment volume and PR size and never auto-approving.

**One-paragraph:** A PR review without comment-kind labels turns into a Slack thread; a 1500-line PR makes meaningful review impossible. This methodology enforces Conventional Comments labels (praise, nitpick, suggestion, issue, question), six review categories (correctness, design, security, performance, tests, docs), a 400-line PR cap, and a 20-comment-per-PR ceiling. Output is a structured review report — comments grouped by category, severity flagged, recommended action explicit. Agents may draft the report; humans approve. Agent is never the sole approver.

**Ефективно для:**

- Команди з ≥3 інженерів, де review-якість тривіально дрейфує до 'looks good'.
- AI-asisted review-loop: агент драфтить, людина approve — clear roles.
- Стандартизація мови review: junior+senior коментують однаковим лексиконом.
- PR-size enforcement: 400-line cap зрізає 'mega PR' до того, як їх неможливо ревю'ити.

## Applies If (ALL must hold)

- PR workflow is in use (GitHub / GitLab / Bitbucket).
- Team is ≥3 engineers (with 1-2 review is co-located conversation).
- Quality bar matters more than throughput (early-stage prototype is exempt).

## Skip If (ANY kills it)

- Solo dev — no other reviewer exists.
- Hot-fix flow with explicit emergency bypass.
- Vendored / generated code PRs — code review provides no signal.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| PR diff | unified diff | git / PR API |
| PR description | Markdown | PR body |
| Repo conventions | Markdown | CONTRIBUTING.md / repo AGENTS.md |
| Test results | JSON | CI status check |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 400-line-cap, conventional-labels, six-categories, comment-ceiling, no-sole-approver | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for review-report artefact | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: drive-by-approval, comment-flood, missing-category, agent-sole-approver | 700 |
| `content/04-procedure.xml` | essential | 5-step review procedure | 700 |
| `content/06-decision-tree.xml` | essential | Size gate → category coverage → approve / request changes | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `size_gate_check` | haiku | Diff size + file count; deterministic. |
| `category_scan` | sonnet | Per-file judgement across six categories. |
| `synthesise_report` | sonnet | Aggregates comments into the report. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent-review.yml` | GitHub workflow that runs the agent reviewer on PRs |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-code-review.py` | Validate a review-report artefact against the schema | After draft, before posting to PR |

## Related

- - [[code-review-basics]] — Conventional Comments labels and minimal review pattern.
- - [[code-review-process]] — the workflow this review fits into (templates, metrics).

## Decision tree

See `content/06-decision-tree.xml`. Branches first on PR size — &gt;400 lines blocks review until split. Otherwise category coverage check → if any category 'critical' issue is found, request changes; else approve with human sign-off.
