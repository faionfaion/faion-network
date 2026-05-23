---
slug: solo-self-code-review-protocol
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Self-review protocol for the solo founder: fixed 10-item checklist, AI second-reviewer mandatory, 24h cool-off for risk-flagged diffs, CI green or revert.
content_id: "1aed6b5ad56965e2"
complexity: medium
produces: checklist
est_tokens: 4700
tags: [code-review, solo, ai-pair, self-review]
---
# Solo Self Code Review Protocol

## Summary

**One-sentence:** Self-review protocol for the solo founder: fixed 10-item checklist, AI second-reviewer mandatory, 24h cool-off for risk-flagged diffs, CI green or revert.

**One-paragraph:** Existing code-review methodologies assume a human peer. A solo founder doesn't have one - and the review they 'do' between coding and merging is often skipped under deadline. This methodology fixes a four-stage self-review: (1) checklist against the diff (>=10 items), (2) AI second-reviewer with a structured prompt, (3) CI must be green at the merge SHA, (4) 24h cool-off mandatory for risk-flagged diffs. The methodology does not try to simulate a peer; it institutionalises distance from just-written code.

**Ефективно для:**

- Solo founder без peer reviewer - підвищити якість self-review.
- AI-generated PR не пройшов peer review - формалізувати second-reviewer step.
- Risky migration / billing / auth - впровадити 24h cool-off.
- Часті hot-fixes на main - впровадити CI green or revert.
- Checklist drift - зафіксувати написаний 10-item canon.

## Applies If (ALL must hold)

- The operator is solo (no peer reviewer available).
- Code is going to production, not just a personal sandbox.
- The PR contains hand-written or AI-generated code that wasn't run through a peer.
- The codebase already has a CI pipeline (tests + linter at minimum).

## Skip If (ANY kills it)

- A peer reviewer is available - use a real peer-review methodology.
- The change is a documentation or copy edit with no code path touched.
- The change is a hotfix during an active incident (incident-triage rules apply).
- The codebase is a throwaway prototype with no production users.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Self-review checklist | markdown with >=10 items + risk-flag list | operator |
| AI second-reviewer prompt | prompt template | operator |
| CI pipeline | tests + linter + typecheck on PR | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[spec-driven-debugging]] | bug-scale SDD shares the AI-pair discipline. |
| [[xp-extreme-programming]] | shared trunk-based + CI-green discipline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: checklist >=10 items, AI second-reviewer required, risk-flag list, 24h cool-off, CI green or revert, in-PR record, versioned checklist | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step protocol: checklist, AI review, risk flags, cool-off, CI green | ~900 |
| `content/05-examples.xml` | essential | Worked example for a risky migration PR | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `run-checklist` | haiku | Mechanical tick / waive. |
| `ai-second-review` | sonnet | Per-diff judgement on bugs + edge cases. |
| `risk-flag-detection` | haiku | Path match against risk list. |
| `decide-cooloff-override` | opus | Stakes high; override skips the safety pause. |

## Templates

| File | Purpose |
|------|---------|
| `templates/self-review-checklist.md` | Self-review checklist (>=10 items) + risk-flag list. |
| `templates/ai-review-prompt.md` | AI second-reviewer prompt template. |
| `templates/_smoke-test.json` | Minimum viable self-review record for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-self-code-review-protocol.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[spec-driven-debugging]]
- [[xp-extreme-programming]]
- [[supply-chain-risk-checklist-spike]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - peer availability, risk flags, AI review, cool-off, CI status - onto a rule from `content/01-core-rules.xml`. Use it before every merge: it catches skip-checklist-fast-merge and ai-review-absent upstream.
