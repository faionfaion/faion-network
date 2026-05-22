---
slug: anti-slop-rubric
tier: geek
group: marketing
domain: marketing
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Codified anti-slop rubric that gates AI-assisted content pipelines on typed inputs, named owner, semver versioning, and a per-rule automated detector."
content_id: "96087030558f7f7b"
complexity: medium
produces: rubric
est_tokens: 2900
tags: [anti-slop, ai-content, rubric, marketing, geek]
---

# Anti-Slop Rubric

## Summary

**One-sentence:** Codified anti-slop rubric that gates AI-assisted content pipelines on typed inputs, named owner, semver versioning, and a per-rule automated detector.

**One-paragraph:** Closes the gap surfaced by 'role-growth-marketing/Content Engine Build from Zero (12 weeks)': AI-assisted content stacks without explicit anti-slop guardrails ship plausible-but-unrankable posts. The rubric forces six testable preconditions on every published piece — bounded scope, typed input with source, named owner, semver + last_reviewed date, automated detector defined before the corrective action, and pre-declared attribution windows — then emits an audited artefact downstream agents can read without re-deriving the judgement.

**Ефективно для:** in-house content teams running AI drafts at >10 pieces/week; agencies needing a defensible quality gate; growth marketers shipping under E-E-A-T pressure.

## Applies If (ALL must hold)

- AI is producing first drafts that humans publish without enrichment
- Pipeline currently has no detector for slop signals (generic openings, unsourced claims)
- An owner exists and can be named on every artefact
- Output will be consumed by downstream automation or a human reviewer

## Skip If (ANY kills it)

- Single-pass throwaway content (one-off announcement) — overhead exceeds value
- Regulated content (medical/legal/financial) — defer to compliance review, not this rubric
- Brand voice not yet codified — rubric amplifies the gap, fix voice first

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| AI draft pipeline definition | Markdown / YAML | team runbook |
| Brand voice guide with examples | Markdown | marketing repo |
| Owner directory (handles / emails) | YAML or CSV | team wiki |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/marketing/marketing-manager` | parent role context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema, valid + invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom + root cause + fix | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Mechanical template fill |
| `synthesize_decision` | sonnet | Per-instance judgement with bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/anti-slop-rubric.json` | JSON schema for the anti-slop rubric output contract |
| `templates/anti-slop-rubric.md` | Markdown skeleton with all required fields |
| `templates/_smoke-test.json` | Minimum-viable filled example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-anti-slop-rubric.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/marketing/`
- [[content-attribution-model]]
- [[ai-content-strategy]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether anti-slop-rubric applies: root question — "Is the content artefact produced by AI drafting AND consumed downstream by automation or a human reviewer?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-detector-first, r6-conversion-window.
