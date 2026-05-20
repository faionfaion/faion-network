---
slug: rag-feature-acceptance-contract
tier: geek
group: ml-engineer
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "d2cc4a1584dc2cbc"
summary: Three-party signed contract (PM + SME + ML engineer) that defines, per intent class, what counts as a correct RAG answer, which eval metrics gate ship, and which production telemetry confirms the win.
tags: [rag, evaluation, acceptance-criteria, ship-gate, ml-engineer]
---

# RAG Feature Acceptance Contract

## Summary

**One-sentence:** Three-party signed contract — Product Manager (intent + business outcome), Subject-Matter Expert (correctness rubric), ML engineer (offline + online metric gate) — that defines what "good answer" means per intent class and gates the RAG feature ship.

**One-paragraph:** RAG features routinely ship on vanity metrics (BLEU, ROUGE, "looks fluent") because nobody on the team agreed in writing what a correct answer is for each user intent. This methodology forces three roles to co-author a single document — the Acceptance Contract — keyed by intent class (e.g. `policy-lookup`, `troubleshooting`, `comparison`, `summarization`). For each class the contract pins: (a) PM's user outcome and tolerable failure mode, (b) SME's correctness rubric with worked examples of pass / borderline / fail, (c) ML engineer's offline metric set with threshold (faithfulness ≥ X, answer-relevance ≥ Y, retrieval-recall@k ≥ Z) AND a matched online metric (CSAT, deflection, escalation rate). Ship is blocked until all three signatures are recorded. Once signed, the contract is the source of truth for the eval harness, regression gates, and post-launch monitoring. Mechanism: contract → eval-set construction → CI gate → shadow-deploy → online metric → recontract on drift. Primary output: a versioned `acceptance-contract.yaml` per RAG feature, machine-readable, that the eval harness and the production monitor both consume.

## Applies If (ALL must hold)

- feature_type == RAG (retrieval-augmented generation: docs, code, support KB, product catalog)
- target_user_population is identifiable and reachable for either CSAT survey or behavioral telemetry
- ≥2 distinct intent classes have been observed in user queries (logs, beta data, or domain analysis)
- a Subject-Matter Expert with authority over correctness is available for ≥4 hours of rubric work
- eval harness exists or is being built in the same iteration (see `geek/ai/ml-engineer/agentic-rag-self-correction`)

## Skip If (ANY kills it)

- single-intent search-only feature (lexical search, no LLM synthesis) — recall@k is sufficient; full contract is over-engineering
- internal-only demo with no ship date — contracting takes 1-3 days, do not block exploration
- the dataset is < 50 labelled queries — there is no way to set defensible thresholds; sample more first
- no SME has authority over correctness (consumer-grade chit-chat) — use preference labels + Elo instead
- you are still in the spike phase deciding whether RAG is the right architecture — defer until architecture is committed

## Prerequisites

- Per-intent query sample: ≥50 real or representative queries per intent class, tagged with intent label
- Draft retrieval pipeline + generator prompt (can be vN-1; the contract drives v1)
- Access to production or beta logs OR a domain-expert-curated query bank
- Stakeholder commitment to the three-signature gate; without it, this is just a doc nobody reads
- Eval framework picked (Ragas, TruLens, Phoenix, DeepEval, in-house) — contract values must be expressible in the chosen framework

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/rag-evaluation-frameworks` | Vocabulary for faithfulness / answer-relevance / context-precision metrics |
| `geek/ai/ml-engineer/golden-dataset-construction` | The eval set referenced by the contract |
| `geek/ai/ml-engineer/llm-as-judge-design` | Many rubric checks are implemented as LLM-judges; calibration discipline lives there |
| `pro/pm/project-manager/release-gates-and-approvals` | Sign-off workflow pattern this contract slots into |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: per-intent decomposition, three signatures, offline+online pairing, threshold defensibility, recontract trigger | ~1000 |
| `content/02-output-contract.xml` | essential | YAML schema for `acceptance-contract.yaml`, required fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 7 failure modes with detector + repair: vanity-metric trap, single-intent flattening, SME-skipped contract, threshold drift, missing online metric, etc. | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `intent_class_extraction_from_logs` | sonnet | Cluster + label real queries; bounded judgement at scale |
| `rubric_drafting_with_sme_interview` | opus | Cross-domain synthesis of PM outcome + SME expertise; needs depth |
| `acceptance_yaml_lint` | haiku | Schema check; cheap and deterministic |
| `regression_gate_check` | sonnet | Per-PR judgement vs contract thresholds; volume; bounded |
| `recontract_recommendation` | opus | Reason about drift evidence and whether to relax / tighten thresholds |

## Templates

| File | Purpose |
|------|---------|
| `templates/acceptance-contract.schema.yaml` | JSON-Schema (YAML form) for the contract document |
| `templates/intent-rubric-card.md` | Per-intent rubric: outcome, pass/borderline/fail examples, metric thresholds |
| `templates/sme-interview-guide.md` | 45-minute structured interview with the SME, role-play of edge cases |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-contract.py` | Lints `acceptance-contract.yaml` against schema, checks every intent has all three signatures | Pre-commit hook on the contract file |
| `scripts/contract-to-eval-config.py` | Generates Ragas / TruLens config from the contract so eval harness cannot drift from contract | After contract signed, before CI gate |

## Related

- parent skill: `geek/ai/ml-engineer/`
- peer methodologies: `rag-evaluation-frameworks`, `golden-dataset-construction`, `shadow-traffic-rollout-pattern`, `retrieval-drift-alerting-recipe`
- external: [Ragas docs](https://docs.ragas.io/) · [TruLens RAG triad](https://www.trulens.org/trulens_eval/getting_started/core_concepts/rag_triad/) · [Microsoft RAG eval guidance](https://learn.microsoft.com/en-us/azure/ai-studio/concepts/evaluation-approach-gen-ai)
