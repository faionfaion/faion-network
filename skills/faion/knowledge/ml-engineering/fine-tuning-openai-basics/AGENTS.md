# Fine-tuning OpenAI — Basics (Dataset Preparation)

## Summary

**One-sentence:** Prepares JSONL chat-messages training data for OpenAI fine-tuning, validates structure + token counts with tiktoken, and synthesises extra examples with GPT-4 when below the recommended count.

**One-paragraph:** OpenAI fine-tuning expects JSONL where each line is a chat-messages payload. The wins come from clean data, not exotic hyperparameters. This methodology validates structure (system / user / assistant alternation, role correctness), enforces token-count budget per example, and uses GPT-4 to synthesise additional examples when the base count is under the 50-example floor. Records baseline cost projection BEFORE the job runs.

**Ефективно для:**

- First-time OpenAI fine-tune (typical solopreneur scenario).
- Closed API requirement + small dataset (<10k examples).
- Quick domain adaptation (legal phrasing, brand voice).
- On-platform RAG-substitute when retrieval is overkill.

## Applies If (ALL must hold)

- Closed API is the deployment target (OpenAI hosted).
- Dataset of ≥50 high-quality examples available (or budget to generate more).
- Token budget is computable in advance.

## Skip If (ANY kills it)

- Self-hosted finetune required — use finetuning-basics / fine-tuning-lora instead.
- Dataset < 50 examples and no budget for synthesis.
- Closed API ft is not allowed by data-residency policy.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Raw examples | CSV/JSONL | Internal export |
| OpenAI API key | secret | Provider |
| Token-budget cap | USD | Finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/05-examples.xml` | reference | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `validate_jsonl` | haiku | Schema check; deterministic. |
| `tiktoken_count` | haiku | Count tokens; deterministic. |
| `synth_examples` | sonnet | GPT-4 augmentation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/training-jsonl.jsonl` | Sample chat-messages training row |
| `templates/cost-estimate.yaml` | Cost projection skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fine-tuning-openai-basics.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[fine-tuning-openai-production]]
- [[finetuning-datasets]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Does the dataset have ≥50 examples? Branches route to a rule id from `content/01-core-rules.xml` (min-50-examples, token-budget-computed, role-alternation, ...) so every leaf is traceable to a testable statement.
