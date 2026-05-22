---
slug: prompt-techniques
tier: geek
group: ai
domain: llm-integration
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Generates advanced prompting artefacts (XML delimiters, meta-prompts, PromptChain pipelines, A/B test harness, versioned PromptLibrary) with regression gates.
content_id: "8a91c3e7b2d5f648"
complexity: deep
produces: code
est_tokens: 4400
tags: [prompt-optimization, meta-prompting, prompt-chaining, prompt-testing, a-b-testing]
---
# Advanced Prompt Techniques

## Summary

**One-sentence:** Production prompt-engineering toolkit — XML delimiters for injection safety, meta-prompting for optimisation, PromptChain for multi-step pipelines, PromptLibrary for versioning, and A/B harness for regression gating.

**One-paragraph:** Advanced prompting patterns, testing, and management strategies. Delimiters (XML tags, backticks) prevent injection and disambiguate sections. Meta-prompting uses an LLM to generate better prompts but produces model-specific outputs. PromptChain decouples discrete LLM steps. PromptLibrary versions prompts as committed YAML, enabling hot-fixes without redeploy. A/B tests are mandatory before promoting any prompt change to production.

**Ефективно для:** AI-інженера, що тримає продакшн-pipeline з ≥3 LLM-кроками — закриває петлю між prompt change, regression test і безпечним rollout.

## Applies If (ALL must hold)

- Prompt is underperforming and needs systematic improvement (meta-prompting + A/B).
- Pipeline has multiple discrete LLM steps to decouple into PromptChain.
- Project needs versioned PromptLibrary so prompts can be updated without code deploys.
- Need to validate prompt accuracy against a known test set before release.
- Prompt injection or delimiter confusion is causing failures.

## Skip If (ANY kills it)

- Single-call use case — `prompt-basics` is sufficient.
- No golden test set exists — meta-prompting and A/B both need ground truth.
- Latency budget &lt; 1s end-to-end — multi-call chains break it.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Existing PromptTemplate | code | `prompt-basics` |
| Golden test set | list[dict] with input + expected | curated by domain expert |
| LLM client | object | pipeline SDK init |
| Eval metric | callable | per-task accuracy / BLEU / F1 |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/prompt-basics` | PromptTemplate is the unit chained by PromptChain. |
| `geek/ai/llm-integration/openai-chat-completions` | The retry-client wraps every chain step. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: XML delimiters mandatory, meta-prompt outputs reviewed by human, chain step idempotency, A/B before promote, version YAML, regression block | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for PromptLibrary entry (slug, version, model, prompt, eval_score) | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: model-specific meta-prompt, chain partial-failure, golden drift, untested promote, delimiter collision | ~900 |
| `content/04-procedure.xml` | deep | 7-step procedure: baseline → meta-prompt → A/B → diff → promote → snapshot → monitor | ~800 |
| `content/06-decision-tree.xml` | essential | Picks meta-prompting vs manual tuning, single-step vs chain | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `generate-meta-prompt` | opus | Cross-prompt synthesis; the model needs to understand failure modes. |
| `apply-meta-prompt` | sonnet | Domain-aware rewrite. |
| `score-ab-results` | haiku | Mechanical metric computation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-library.yaml` | Schema for versioned PromptLibrary entries (slug, version, model, prompt, eval_score). |
| `templates/prompt-chain.py` | PromptChain class composing PromptTemplate steps with error propagation. |
| `templates/ab-test-harness.py` | A/B harness comparing two PromptLibrary versions against a golden set. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prompt-techniques.py` | Validate a PromptLibrary entry JSON matches the output contract. | Pre-merge in CI; nightly drift scan. |

## Related

- [[prompt-basics]] — base PromptTemplate.
- [[chain-of-thought]] — one chaining pattern.
- [[structured-output-patterns]] — output-shape enforcement.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks (a) meta-prompting vs manual tuning by failure-mode count, (b) single PromptTemplate vs PromptChain by step independence, and (c) A/B vs replace by deployment risk. Use it before authoring any new prompt change.
