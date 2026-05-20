---
slug: solo-self-code-review-protocol
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Self-code-review protocol for a solo founder reviewing their own (or AI-generated) PRs — checklist, AI as second reviewer, 24h cool-off for risky changes.
content_id: "30a6f63a2b64f35d"
tags: [solo-self-code-review-protocol, dev, solo]
---
# Solo Self Code Review Protocol

## Summary

**One-sentence:** A code-review protocol calibrated for the case where there is no human peer — the solo founder reviews their own or an AI agent's PR, using a fixed checklist, an AI second-reviewer, and a 24h cool-off gate for risky changes.

**One-paragraph:** All existing code-review methodologies (`free/dev/code-quality/code-review*`) assume a human peer reviewer. A solo SaaS founder doesn't have one — and the review they "do" between coding and merging is often skipped under deadline. This methodology fixes a four-stage self-review: (1) checklist against the diff, (2) AI second-reviewer with a structured prompt, (3) automated checks must pass, (4) 24h cool-off mandatory for risk-flagged diffs. It does not try to simulate a peer — it institutionalises distance from the just-written code.

## Applies If (ALL must hold)

- the operator is solo (no peer reviewer available)
- code is going to production, not just a personal sandbox
- the PR contains hand-written or AI-generated code that wasn't run through a peer
- the codebase already has a CI pipeline of some kind (tests + linter at minimum)

## Skip If (ANY kills it)

- a peer reviewer is available — use a real peer review methodology
- the change is a documentation or copy edit with no code path touched
- the change is a hotfix during an active incident (incident-triage rules apply)
- the codebase is a throwaway prototype with no production users

## Prerequisites

- a CI pipeline that runs on the PR (tests + linter)
- an AI assistant (Claude / Cursor / Copilot) configured for the repo
- a written list of "risk-flag" patterns (DB migrations, billing, auth, deletes)
- a rebase / amend workflow the founder is comfortable with

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-developer` | parent skill |
| `solo/dev/ai-over-reliance-self-audit` | sibling — bounds the trust placed on the AI second-reviewer |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: fixed-checklist-pass, ai-second-reviewer-required, risk-flag-list, 24h-cooloff-risky, ci-green-or-revert | ~1000 |

## Related

- parent skill: `solo/dev/software-developer`
- upstream playbook: `p1-solo-saas-builder/AI-pair coding loop for solo SaaS (Claude/Cursor + Spec)`
- sibling: `solo/dev/ai-over-reliance-self-audit`
