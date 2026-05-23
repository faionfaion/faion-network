# Two-Pass: Free-Form Reasoning Then Structured Extraction

## Summary

**One-sentence:** Run strong model in free text for reasoning, cheap model with strict schema for extraction; restores the 10-15% accuracy that grammar-mask costs on hard tasks.

**One-paragraph:** Forcing strict JSON during reasoning measurably hurts accuracy: SLOT (arXiv:2505.04016) and BuildMVPFast 2026 report 10-15% drops on math + complex analysis when the same prompt runs with strict structured output vs free text. The grammar mask burns probability on schema-conforming tokens that are not the optimal reasoning tokens. This methodology splits the work: pass 1 runs the strong model (Opus + extended thinking) in free text; pass 2 runs a cheap extractor (Haiku) with strict structured output over the transcript. The schema lands on the consumer; the reasoning is never constrained.

**Ефективно для:**

- Math word problems, multi-step proofs, code generation з тонкими constraints — accuracy відновлюється.
- Research synthesis: довгий аналіз → коротка структурна verdict.
- Legal / medical verdict tasks: ригідна schema без compromise на reasoning.
- Будь-який pipeline, де Opus extended thinking justified, але consumer хоче strict JSON.

## Applies If (ALL must hold)

- Task requires deep reasoning (math, proofs, multi-step code, research synthesis).
- Consumer requires strict JSON / Pydantic / Zod schema output.
- Latency budget allows two model calls (not sub-second).

## Skip If (ANY kills it)

- Simple extraction tasks (entities, sentiment, key-value) — single-pass strict SO is fine.
- Latency-critical (&lt; 1 s) paths — two calls always cost wall-clock.
- High-volume routes where doubled provider cost exceeds the accuracy gain.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Strong-model client | Anthropic / OpenAI SDK | your provider |
| Extractor-model client | Haiku / GPT-4.1-nano / equivalent | your provider |
| Output schema | Pydantic / Zod / JSON Schema | consumer contract |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology is self-contained; no upstream artefact required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: two-pass-required, strong-model-free-text, extractor-deterministic, transcript-bounded, ab-vs-single-pass | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for config + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_task_difficulty` | sonnet | Difficulty scoring needs light judgment. |
| `design_pass_pair` | sonnet | Picks models + thinking budget. |
| `run_ab_eval` | haiku | Mechanical eval execution. |
| `monitor_extraction_fidelity` | haiku | Schema-violation counting. |

## Templates

| File | Purpose |
|------|---------|
| `templates/two-pass-anthropic.py` | Anthropic SDK two-pass: Opus extended-thinking → Haiku structured-output extraction |
| `templates/two-pass-openai.py` | OpenAI SDK two-pass: o-series reasoning model → gpt-4.1-nano structured outputs |
| `templates/ab-eval-runner.py` | A/B eval harness comparing single-pass strict-SO vs two-pass on a fixture set |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-two-pass-reason-then-extract.py` | Validate the config artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[weak-model-preselection]]
- [[tool-description-as-prompt]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
