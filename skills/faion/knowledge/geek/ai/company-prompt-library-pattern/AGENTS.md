---
slug: company-prompt-library-pattern
tier: geek
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Company Prompt Library Pattern: codified ai practice that turns the recurring 'p6-product-dev-team/Adopt faion org-wide and override with company patterns' decision into a repeatable, auditable artefact.
content_id: "4522da5dafd9e9ef"
tags: [company-prompt-library-pattern, ai, geek]
---
# Company Prompt Library Pattern

## Summary

**One-sentence:** Company Prompt Library Pattern: codified ai practice that turns the recurring 'p6-product-dev-team/Adopt faion org-wide and override with company patterns' decision into a repeatable, auditable artefact.

**One-paragraph:** Company Prompt Library Pattern addresses the gap surfaced by 'p6-product-dev-team/Adopt faion org-wide and override with company patterns'. Each dev now googles/copies prompts differently from ChatGPT/Claude. Need a checked-in `prompts/` directory pattern with: company tone, internal context (data model, conventions), per-role prompt sets (PM prompts, code-review prompts, QA prompts). Faion has llm-integration + claude-code knowledge but nothing on AUTHORING the company-internal prompt library. Direct competitor to Faion is `prompts.chat` and PromptLayer — Faion should own this as part of geek Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'p6-product-dev-team/Adopt faion org-wide and override with company patterns' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'p6-product-dev-team/Adopt faion org-wide and override with company patterns' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-traceable-decision | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment with bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/company-prompt-library-pattern.json` | JSON schema for the Company Prompt Library Pattern output contract |
| `templates/company-prompt-library-pattern.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-company-prompt-library-pattern.py` | Enforce Company Prompt Library Pattern output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/ai/ml-engineer/`
- upstream playbook: `p6-product-dev-team/Adopt faion org-wide and override with company patterns`
- methodology family: `geek/ai/` (gap-p2 batch, F-059-063)
