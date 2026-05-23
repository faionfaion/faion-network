---
slug: test-golden-master-legacy-rewrite
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a committed (input, expected_output) corpus that the AI rewrite of a legacy module must reproduce byte-for-byte, with every diff individually approved.
content_id: "f467681fd641ed07"
complexity: deep
produces: code
est_tokens: 4200
tags: [golden-master, legacy-rewrite, corpus, snapshot-testing, agent-testing]
---
# Golden-Master Corpus for AI-Driven Legacy Rewrites

## Summary

**One-sentence:** Capture inputs and outputs of the current legacy implementation into a committed corpus; an AI rewrite passes only when it reproduces every pair byte-for-byte (or each diff is explicitly approved row-by-row).

**One-paragraph:** When you ask a coding agent to rewrite a 5000-line legacy module, you have no spec — you have current behaviour. Capture inputs and outputs of the current implementation from production traffic, fixtures, or a fuzzer into a committed corpus of (input, expected_output) pairs; the agent's rewrite passes only when it reproduces every pair, byte-for-byte, or each diff is explicitly approved row-by-row. This is the only test that scales to AI-driven rewrites of untested legacy: it is the spec the legacy never had, captured automatically, and it gives the agent a deterministic GREEN signal that does not depend on human ability to read the old code.

**Ефективно для:**

- 5k-LoC legacy module без юніт-тестів — corpus стає specs.
- AI rewrite, де human can't read the old code чи валідувати manually.
- Strangler-fig migration: corpus гарантує parity step-by-step.
- Compliance: byte-for-byte parity proof для audit.

## Applies If (ALL must hold)

- Legacy module ≥ 500 LoC slated for AI-driven rewrite.
- Production traffic or fixtures exist to sample inputs from.
- Outputs are deterministic (or non-determinism can be canonicalized).

## Skip If (ANY kills it)

- Module is 50 LoC where a hand-written test suite is faster.
- Outputs depend on wall-clock time or external state that cannot be mocked.
- No traffic source exists and inputs cannot be generated synthetically.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Legacy module source | code | repo |
| Traffic capture or fixture source | HAR / pickle / DB dump | ops |
| Canonicalization function (if non-deterministic) | code | team |

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
| `templates/capture_corpus.py` | Python script sampling top-N+tail+fuzz inputs and capturing legacy outputs. |
| `templates/golden_master_test.py` | pytest runner that diffs (input, expected) pairs and checks `approved_diffs.yaml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-test-golden-master-legacy-rewrite.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[test-mutation-feedback-loop]]
- [[test-property-based-llm-invariants]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
