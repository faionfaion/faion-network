---
slug: ai-feature-spec-contract
tier: pro
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Feature-management method for ai feature spec contract — what the brief, gate, and rollout artefacts must contain to move a feature from idea to production safely.
content_id: "b130ff95eefac25f"
tags: [ai, feature-mgmt, product]
---
# AI Feature Spec Contract

## Summary

**One-sentence:** Feature-management method for ai feature spec contract — what the brief, gate, and rollout artefacts must contain to move a feature from idea to production safely.

**One-paragraph:** Feature-management method for ai feature spec contract — what the brief, gate, and rollout artefacts must contain to move a feature from idea to production safely. ML engineers receive fuzzy 'add AI to X' asks; nothing in faion teaches them to nail an input/output contract, success metric, and out-of-scope list for a single feature embedded in a non-AI product. ai-native-product-development covers the whole product, not one feature.

## Applies If (ALL must hold)

- You shepherd a feature through the SDLC gate covered by ai feature spec contract.
- There is a named owner accountable for the gate exit criteria.
- Rollback or kill-criteria for the feature are explicit before the gate.
- Cross-team consumers (support, finance, legal) are pre-briefed.

## Skip If (ANY kills it)

- Spikes / research with no production path — gate criteria are inapplicable.
- Hot-fix or restore-path changes — incident response, not feature gating.
- Internal-only, blameless dogfood features with no external customer signal.

## Prerequisites

- Feature brief or RFC at the gate's expected maturity.
- Named gate-owner and downstream consumer-owner.
- Roll-back or kill-criteria decision recorded.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | The 4 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `artefact_check` | haiku | Lint the feature brief against gate criteria |
| `gap_diagnosis` | sonnet | Identify which exit criteria are unmet |
| `gate_decision` | opus | Author go/no-go with consequence narrative |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `pro/product/product-manager/`
- peer methodologies: see siblings under `pro/product/product-manager/`
- external: industry references cited inline in `content/01-core-rules.xml`
