---
slug: experiment-verdict-template
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Single "verdict card" format that closes A/B and campaign experiments on a fixed cadence — kills zombie tests, captures the learning, and routes the decision to a named owner.
content_id: b1dd66cee884d949
---

# Experiment Verdict Template

## Summary

A/B testing methodology covers design and statistics. What teams lack is a closing artefact: the single card that says "this experiment is done, here is the verdict, here is the decision, here is what we learned". Without it, experiments become zombie — left running long past their statistical close, results forgotten, learnings re-discovered. This methodology defines the verdict card, the weekly close cadence, and the gate that rejects experiments which try to extend past the planned sample without an explicit re-justification.

## Applies If

- The team runs A/B tests, holdout experiments, or campaign-comparison experiments at least every two weeks.
- An experimentation platform (Optimizely, Statsig, GrowthBook, Posthog, GA experiments, or a homemade tracker) captures variant assignment and metrics.
- A weekly experiment review ritual exists or can be added.
- Decisions from experiments can route into product, marketing, or pricing follow-ups.

## Skip If

- One-off campaign with no future cadence or learning need.
- Statistical power so low that the experiment can only produce inconclusive results — fix design first.

## Content
See `content/01-core-rules.xml`.

## Related
- [[experiment-hypothesis-scoring]]
- [[experiment-ledger-discipline]]
- [[learnings-database-schema]]
