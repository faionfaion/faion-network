---
slug: fine-tuning-openai-dpo
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a DPO training config + preference-pair dataset spec for OpenAI fine-tuning, applied after SFT to align model behaviour to subjective criteria (tone, style, safety, brand voice).
content_id: "42d542a1d58b3cb6"
complexity: deep
produces: config
est_tokens: 3600
tags: [fine-tuning, openai, dpo, alignment, preference-optimization]
---
# OpenAI Direct Preference Optimization (DPO)

## Summary

**One-sentence:** Produces a DPO training config + preference-pair dataset spec for OpenAI fine-tuning, applied after SFT to align model behaviour to subjective criteria (tone, style, safety, brand voice).

**One-paragraph:** Produces a DPO (Direct Preference Optimization) training config + preference-pair dataset spec. DPO trains an OpenAI model on (input, preferred_response, non_preferred_response) triples to align output to subjective criteria where there is no single 'correct' answer — tone, style, safety, brand voice. DPO is applied AFTER an SFT base; running DPO without SFT first wastes signal. Pairs must be label-consistent: same labeller, clear preference reason, ≥500 pairs.

**Ефективно для:** ML лід для brand-voice alignment — fixed DPO config spec до того, як labelling-team почне збирати pairs.

## Applies If (ALL must hold)

- Existing SFT fine-tune in production (or via prompting) close to but not matching subjective target.
- Target criterion is subjective: tone, style, safety, brand voice, helpfulness vs harmlessness.
- Can collect or generate ≥500 preference pairs with consistent labelling.
- Held-out preference eval set defined (LLM-as-judge or human-pair-vote).
- Budget for two-stage train (SFT + DPO) approved.

## Skip If (ANY kills it)

- No SFT base — train SFT first (per `fine-tuning-openai-sft`).
- Target is objective and verifiable (math, code, structured extraction) — SFT alone suffices.
- <500 pairs — DPO overfits; collect more pairs or use prompting.
- Pairs labelled by inconsistent labellers (no inter-rater check) — fix labelling first.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Preference pairs JSONL | jsonl with messages + non_preferred_output | labelling team |
| SFT base model ID | string (ft:...) | fine-tuning-openai-sft output |
| Held-out preference eval | jsonl | eval team |
| Inter-rater agreement | kappa or % | labelling-team-lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/fine-tuning-openai-sft` | Required prior step; SFT fine-tune is the DPO base. |
| `geek/ai/ml-engineer/fine-tuning-openai-eval` | Eval pattern reused for preference scoring. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: validate-pairs → set-beta → launch-job → eval-preference-rate → deploy. | ~700 |
| `content/06-decision-tree.xml` | essential | Branch by pair count + inter-rater agreement + base type. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `validate-pair-dataset` | haiku | Schema + count + duplicate detection. |
| `tune-beta` | sonnet | Choose beta (0.01-0.5) by pair count + agreement. |
| `audit-pair-labelling` | opus | Spot disagreements; surface labelling drift. |

## Templates

| File | Purpose |
|------|---------|
| `templates/openai-dpo-job.py` | Job-launch script with beta + epochs. |
| `templates/preference-pair-schema.json` | JSON schema for preference pairs. |
| `templates/dpo-eval-prompt.txt` | LLM-as-judge prompt for preference scoring. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fine-tuning-openai-dpo.py` | Validate that the DPO config matches the schema (pairs, beta, sft_base, eval). | Pre-merge of every DPO config PR. |

## Related

- [[fine-tuning-openai-sft]] — supplies the SFT base.
- [[fine-tuning-openai-eval]] — eval pattern.
- [[finetuning]] — parent decision; selects DPO branch.

## Decision tree

Decision tree at `content/06-decision-tree.xml` decides beta + epochs + whether DPO is even justified given pair quality.
