---
slug: eval-driven-development-tdd-for-ai
tier: pro
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: TDD discipline for AI features — write the eval before the prompt, fail CI on regression, treat the eval suite as production code, never ship a prompt change without a green eval delta.
content_id: 66790a9c1c7a07fd
---

# Eval-Driven Development: TDD for AI

## Summary

Faion has many eval primitives (rag-eval-*, model-evaluation, llm-judge-rubric-evidence-first) but no methodology that states the disciplinary rule: write the eval first, fail CI on regression, treat eval suites as production code. Eval-as-afterthought is the most common ML-engineer failure mode — teams ship a prompt, observe "it looks better in spot-checks", and discover six weeks later that quality on a critical persona has collapsed. This methodology defines the TDD-for-AI loop: eval-before-prompt, regression-gated CI, eval-suite ownership, drift watch, and the explicit kill criterion for an eval suite that has lost signal value.

## Applies If

- The team ships AI features (prompts, agents, RAG, fine-tunes) into a product where regressions are user-visible or cost-visible.
- A change to a prompt, model, retrieval, or tool schema happens at least monthly.
- The team can wire eval execution into CI and gate merges on a configurable threshold.
- A budget exists for the inference cost of eval runs (or a cached/mock plan exists for cheap evals).

## Skip If

- One-shot prototype with no plan to ship, no users, no rollback need.
- The feature is so deterministic (rule-based, no LLM) that unit tests fully capture behaviour — use ordinary TDD.

## Content
See `content/01-core-rules.xml`.

## Related
- [[eval-contract-template]]
- [[eval-set-stratified-sampling-recipe]]
- [[prompt-ab-power-calculator]]
- [[model-eval-control-bands]]
- [[llm-drift-daily-triage]]
