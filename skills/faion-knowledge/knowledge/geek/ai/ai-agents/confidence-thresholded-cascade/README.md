# Confidence-Thresholded Cascade

**Category:** `mm-` (multi-model orchestration)

## The Rule

Send the request to a CHEAP model first. The cheap model returns an answer AND a confidence score. If confidence is above threshold, accept it. Otherwise, escalate to the expensive model. This is FrugalGPT's core insight — most tasks are easy, and a cheap model can self-detect when it's out of its depth.

```
cheap_answer = cheap_model(task)
if cheap_answer.confidence >= 0.85:
    return cheap_answer
return expensive_model(task)
```

## Empirical Anchor

FrugalGPT (Stanford, 2023) showed up to **98% cost reduction while matching the BEST individual LLM** on benchmarks via cascade. RouteLLM (2024) hit 95% of GPT-4 performance at 26% of GPT-4 calls (~48% cheaper). Industry deployments (OpenRouter cascades, OpenAI hosted routing) confirm 50-80% savings on most workloads.

## Why It Works

The accuracy of cheap models on EASY tasks is often within 1-3% of expensive models. The accuracy gap explodes only on HARD tasks. A cheap model with calibrated confidence can self-route — it knows when it's guessing.

## When To Use

- High-volume traffic where cost dominates (chatbots, classifiers, batch processing)
- Mixed task difficulty (some easy, some hard) — cascade adapts
- Latency-tolerant production paths (cascade adds one round-trip)
- Tasks where confidence is calibrate-able (classification, factual extraction)

## When NOT To Use

- Mission-critical decisions where ANY error has high cost (skip cascade; go straight to strong model)
- Tasks where "confidence" is hard to elicit (creative writing, planning)
- Cold-start: cheap model doesn't know its limits yet — needs eval data first
- Latency-critical interactive flows where the second hop blows the budget

## Calibrating Confidence

Two approaches:

1. **Self-reported confidence**: cheap model emits `confidence: 0..1` field in structured output. Calibrate by measuring actual accuracy at each confidence bucket.
2. **Logprob-based**: use the cheap model's token logprobs of the answer. More reliable but requires API access to logprobs (OpenAI yes; Anthropic limited).

In practice, self-reported is good enough if you tune the threshold on a small eval set.

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Threshold set without measurement | Calibrate on 100+ tasks; pick threshold where escalation rate is acceptable |
| Cheap model's confidence not calibrated | Run eval at each bucket; if 0.9 confidence is only 70% accurate, adjust threshold |
| Always escalating regardless of confidence | You've reverted to single-model — measure and remove the always-escalate path |
| Cascade with > 3 levels | Diminishing returns; usually 2 levels suffice |
| Cheap model is just a smaller version of strong model | Often best; but check if a different family (cheaper provider) does better at filter-tier |

## Composition

- + **weak-model-preselection**: similar idea but for filter (returns refs); cascade returns answer
- + **schema-field-order**: cheap model's schema = `[reasoning, answer, confidence]` (reasoning first, confidence last)
- + **trajectory-eval-otel**: track escalation rate over time; alert if drift

## References

- [FrugalGPT (Chen et al., 2023)](https://arxiv.org/abs/2305.05176)
- [RouteLLM (Ong et al., 2024)](https://arxiv.org/abs/2406.18665)
- [OpenRouter routing modes](https://openrouter.ai/docs/features/model-routing)

See `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.
