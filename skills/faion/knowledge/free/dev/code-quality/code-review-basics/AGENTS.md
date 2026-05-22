---
slug: code-review-basics
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a minimal-viable PR review checklist (5-item) using Conventional Comments labels with a 400-line cap and no-agent-approver rule.
content_id: "ebfbd4c873ba00ab"
complexity: light
produces: checklist
est_tokens: 2800
tags: [code-review, basics, conventional-comments, pr]
---
# Code Review Basics

## Summary

**One-sentence:** Five-item PR review checklist with Conventional Comments labels; 400-line cap; agent never sole approver.

**One-paragraph:** The simplest workable review: five questions, five comment labels, hard caps on PR size and comment volume. Output is a checklist artefact a junior reviewer can use without prior training. Intended as the floor for `code-review` and the input to `code-review-process`. Conventional Comments give the label vocabulary; the cap stops mega-PRs from polluting the inbox.

**Ефективно для:**

- Junior-QA / junior-eng review training: чек-лист дає 'що поставити в комент'.
- Solo / 2-person team: процес-overhead мінімальний, але якість фіксована.
- AI-агенти: draft a structured 5-item PR review без надмірних reasoning steps.
- Hot-fix flow: легка форма дозволяє швидкий, але not-zero review.

## Applies If (ALL must hold)

- PR workflow exists.
- Reviewer needs a deterministic starting point.
- Team accepts Conventional Comments vocabulary.

## Skip If (ANY kills it)

- Repo already runs the full code-review methodology — basics is the floor, full is the ceiling.
- Solo project with no second reviewer.
- Vendored / generated code PRs.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| PR diff | unified diff | git / PR API |
| PR description | Markdown | PR body |
| CI status | string | GitHub check API |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: conventional-labels, 400-cap, 20-cap, ask-not-assert, human-approver | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema for checklist artefact | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: nit-bombing, opinion-as-issue, agent-merging-own-PR | 600 |
| `content/06-decision-tree.xml` | essential | Size + label decision tree | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `size_gate` | haiku | Deterministic; line count check. |
| `checklist_walk` | sonnet | Per-question structured pass over the diff. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pr-context.sh` | Shell that gathers PR context (diff, CI status, description) for the reviewer |
| `templates/review-prompt.txt` | LLM prompt that drives the checklist walk |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-code-review-basics.py` | Validate the checklist artefact against schema | After checklist walk, before posting |

## Related

- - [[code-review]] — the full 6-category methodology.
- - [[code-review-process]] — workflow templates this checklist plugs into.

## Decision tree

See `content/06-decision-tree.xml`. Branches: PR &gt; 400 lines? → block. Else walk the 5-item checklist; emit issue-labels if any gap; recommend approve if all 5 pass and CI is green.
