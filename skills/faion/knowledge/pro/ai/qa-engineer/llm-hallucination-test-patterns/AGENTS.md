---
slug: llm-hallucination-test-patterns
tier: pro
group: ai
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: QA-facing pattern library for testing LLM hallucination — fact-checking probes, grounding-required questions, refusal-correctness tests, citation verification, contradiction tests, off-topic rejection.
content_id: "920ff0d43fc7c96b"
tags: [qa,llm,hallucination,grounding,refusal,citation,test-design]
---
# LLM Hallucination Test Patterns

## Summary

**One-sentence:** QA-facing pattern library for testing LLM hallucination — fact-checking probes, grounding-required questions, refusal-correctness tests, citation verification, contradiction tests, off-topic rejection.

**One-paragraph:** Hallucination is the #1 production bug class for LLM features, but eval-framework docs are abstract; QA engineers need a pattern library of CONCRETE test types they can author and maintain. This methodology defines six pattern classes, each with input shape, expected behavior, and pass/fail criteria: (1) fact_probes (verifiable facts), (2) grounding_required (must cite from given context), (3) refusal_correctness (must say "I don't know"), (4) citation_verification (cited source actually contains the claim), (5) contradiction_tests (model must not assert both A and ¬A), (6) off_topic_rejection (out-of-scope queries refused). Mechanism: per-pattern test-case schemas, gold-label authoring rules, scoring rubric. Primary output: a hallucination test suite with ≥ 10 cases per pattern, integrated with the team's eval pipeline.

## Applies If (ALL must hold)

- LLM feature is in production OR scheduled for production within 30 days
- feature consumes user-supplied or document-retrieved context
- QA owns a test suite for the feature (not LLM-eval-only)
- ≥ 1 hallucination-driven incident has occurred OR feature touches a regulated surface
- team can author test cases in plain text or JSON

## Skip If (ANY kills it)

- pure structured-output feature where hallucination is impossible by schema
- feature is offline experimentation only — no production exposure
- feature output is creative content with no factual grounding (poem, fiction)
- LLM-judge pipeline already produces hallucination-scoring with maintained pattern library
- feature has been deprecated; no further QA investment planned

## Prerequisites (must be true before starting)

- feature input + output schema documented
- representative production traffic samples available (PII-redacted)
- access to source documents the feature may cite
- LLM-eval-pipeline available OR test harness that can record per-case pass/fail
- per-pattern minimum case count agreed: default ≥ 10 per pattern

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ai/ml-engineer/golden-set-curation-and-maintenance` | Hallucination cases promote to golden set after incidents |
| `geek/ai/llm-integration/guardrails-implementation` | Provides runtime guardrails; this provides their test suite |
| `geek/ai/ml-engineer/rag-eval-test-set-generation` | Optional companion for RAG-specific cases |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 6 pattern classes, ≥ 10 cases per pattern, gold-label authoring, scoring rubric, incident-to-case pipeline | ~1000 |
| `content/02-output-contract.xml` | essential | Per-pattern case schema, suite-level metrics, expected pass-rate thresholds | ~700 |
| `content/03-failure-modes.xml` | essential | 7 failure modes (false-negative gold labels, easy-case bias, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pattern_case_generator` | sonnet | Generate candidate cases per pattern class |
| `gold_label_authoring` | opus | Authoritative pass/fail labels; high consequence |
| `citation_verifier` | sonnet | Check whether cited source contains the claim |
| `contradiction_detector` | sonnet | Detect mutually exclusive claims in same response |

## Templates

| File | Purpose |
|------|---------|
| `templates/pattern-case-schema.json` | Per-case JSON schema with pattern_class + expected behavior |
| `templates/gold-label-rubric.md` | Pass/fail rubric per pattern class |
| `templates/incident-to-case.md` | Convert hallucination incident into a hallucination test case |
| `templates/suite-scorecard.md` | Per-pattern pass-rate scorecard |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/pattern-coverage-check.py` | Verify ≥ 10 cases per pattern | Before suite ship |
| `scripts/citation-validator.py` | Auto-check citation_verification cases | Suite run |
| `scripts/contradiction-scanner.py` | Auto-detect contradictions in model outputs | Suite run |

## Related

- parent skill: `pro/ai/qa-engineer/`
- peer methodology: `golden-set-curation-and-maintenance`, `guardrails-implementation`
- external: [TruthfulQA paper](https://arxiv.org/abs/2109.07958) · [HELM evaluation suite](https://crfm.stanford.edu/helm/) · [Eugene Yan, LLM evals](https://eugeneyan.com/writing/llm-evaluators/)
