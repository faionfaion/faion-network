---
slug: sow-template-with-traced-assumptions
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Fixed-price SoW where every scope clause, exclusion, and pricing assumption carries an [A-NN] ID pointing at the discovery artefact that set it.
content_id: "fe26c75d340b057e"
complexity: medium
produces: spec
est_tokens: 5000
tags: [sow, business-analyst, fixed-price, traceability, assumptions, ba]
---
# SoW Template with Traced Assumptions

## Summary

**One-sentence:** Fixed-price SoW where every scope clause, exclusion, and pricing assumption carries an [A-NN] ID pointing at the discovery artefact that set it.

**One-paragraph:** Fixed-price SoW where every scope clause, exclusion, and pricing assumption carries an [A-NN] ID pointing at the discovery artefact that set it. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned spec artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- fixed-price engagement, де клієнт може оскаржити будь-яку фразу post-signature.
- BA володіє або співволодіє вмістом SoW (не чистий legal-handoff).
- discovery дав ≥1 артефакт (interview notes, requirements doc, decision memo).
- потрібно зробити change-request протокол операційним, не декоративним.
- audit-trail на pricing assumptions для оборони margin.

## Applies If (ALL must hold)

- engagement model is fixed-price (or fixed-price-per-phase), not pure T&M.
- a pre-bid discovery phase has produced ≥1 interview note, requirements doc, or signed decision memo.
- the BA owns or co-owns the SoW content (not pure legal hand-off).
- client is willing to sign an SoW that includes an explicit assumptions appendix.

## Skip If (ANY kills it)

- pure T&M engagement — assumptions are managed via change orders, not the SoW body.
- discovery phase did not produce written artefacts — trace targets do not exist; fix discovery first.
- standing MSA already defines all scope language — use the MSA's change protocol instead.
- engagement under 2 weeks total — overhead exceeds dispute risk.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering activity context | recent notes / tickets | operator's inbox / ticket tracker |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the spec artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, no judgement. |
| `synthesize-decision` | sonnet | Per-instance judgement against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sow-template-with-traced-assumptions.md` | Working spec skeleton with 5-line header |
| `templates/_smoke-test.md` | Minimum viable filled-in version for smoke testing |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sow-template-with-traced-assumptions.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[scope-creep-firewall]]
- [[change-request-impact-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
