# Preference-Trained Router (RouteLLM Pattern)

## Summary

Train a tiny router (matrix factorization, BERT classifier, or similarity ranker) on Chatbot-Arena-style preference data so it can decide BEFORE inference whether each prompt should go to the weak or strong model. One round-trip, one decision, no cascade. The router is a learned binary classifier on the prompt embedding, not a heuristic — and it must be retrained when traffic distribution drifts.

## Why

Cascades (cheap→strong on low confidence) add a round-trip and rely on the cheap model's calibration, which is often poor. A preference-trained router shortcircuits this: published RouteLLM (Ong et al. 2024, ICLR 2025) reports 95% of GPT-4 quality while routing only 26% of queries to GPT-4 — roughly 48% cheaper than random baseline at matched quality. The mechanism is a learned rank between weak and strong outputs on existing preference data, not a confidence threshold on the cheap model. Cuts latency vs cascade and removes the dependence on cheap-model self-scoring, which Anthropic and Google have both shown to be unreliable for hard prompts.

## When To Use

- Latency-sensitive production traffic where the cascade round-trip is unacceptable.
- You have ≥10k logged (prompt, weak-output, strong-output) tuples to train on (or can use Arena public data + a few thousand of your own).
- Mostly-stable task distribution — router quality decays under distribution shift.
- Token spend on the strong model is the dominant line item AND the workload mixes easy and hard prompts.

## When NOT To Use

- Cold start with no preference data — train a cascade first, log Arena pairs, switch later.
- Rapidly drifting traffic (new product, weekly feature changes) — the router goes stale faster than you can retrain it.
- Adversarial or safety-critical paths where a wrong-but-confident route is unacceptable; use a cascade with explicit verification instead.
- Single-model workloads where the strong model's marginal cost is already low (small prompts, cached prefix).

## Content

| File | What's inside |
|------|---------------|
| `content/01-router-architecture.xml` | Matrix-factorization router, BERT-classifier router, similarity-ranker router; cost-quality knob; what to train on. |
| `content/02-deployment-and-drift.xml` | Calibration, drift detection, retraining cadence, fallback to cascade when router confidence is low. |

## Templates

| File | Purpose |
|------|---------|
| `templates/router_client.py` | Minimal RouteLLM Controller wrapper: wrap your OpenAI-compatible client and route per call. |
| `templates/drift_check.py` | Compare current-week routing distribution against a reference window; emit drift alert. |
