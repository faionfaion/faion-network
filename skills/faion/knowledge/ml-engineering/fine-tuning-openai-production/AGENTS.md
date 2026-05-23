# Fine-tuning OpenAI — Production Pipeline

## Summary

**One-sentence:** End-to-end OpenAI fine-tune pipeline: file upload, job create with hyperparameter control, status polling, LLM-as-judge evaluation on held-out set, model ID registry.

**One-paragraph:** Going from a prepared dataset (fine-tuning-openai-basics) to a production model requires a pipeline, not a one-off CLI command. This methodology defines: file upload → job creation with explicit hyperparameters (n_epochs, batch_size, learning_rate_multiplier) → status polling with backoff → LLM-as-judge eval on the held-out set → model ID registry write so prod traffic can pin a version. Each stage is idempotent and resumable.

**Ефективно для:**

- Promoting a successful OpenAI ft from notebook to production.
- Versioned model registry across multiple finetune iterations.
- CI gate before traffic rollout.
- Rollback capability when a new ft regresses.

## Applies If (ALL must hold)

- Dataset already prepared and validated (fine-tuning-openai-basics done).
- Production traffic > 0 (rollout matters).
- Eval harness exists (evaluation-framework done).

## Skip If (ANY kills it)

- Self-hosted ft target — use finetuning-basics / lora pipeline.
- One-off experiment with no rollout — Notebook is fine.
- No held-out eval set — author one first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Prepared dataset | JSONL | fine-tuning-openai-basics |
| Eval set | JSONL | evaluation-framework |
| Model registry | DB / git tag scheme | DevOps |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/05-examples.xml` | reference | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `file_upload` | haiku | OpenAI files API; deterministic. |
| `job_create` | haiku | OpenAI fine-tunes API. |
| `status_poll` | haiku | Polling loop with backoff. |
| `judge_eval` | sonnet | Quality scoring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/finetune-pipeline.py` | Pipeline orchestrator skeleton |
| `templates/model-registry.yaml` | Registry schema skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fine-tuning-openai-production.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[fine-tuning-openai-basics]]
- [[evaluation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Has the file been uploaded? Branches route to a rule id from `content/01-core-rules.xml` (idempotent-resume, hyperparameter-explicit, eval-on-held-out, ...) so every leaf is traceable to a testable statement.
