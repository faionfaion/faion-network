# Agent Integration — Fine-tuning OpenAI Basics

## When to use
- The application requires a consistent output format or style that prompt engineering reliably achieves only 70-80% of the time
- A domain-specific vocabulary or terminology causes the base model to produce incorrect or inconsistent terminology
- Current prompts are long (>500 tokens of examples) and reducing prompt length via fine-tuning would improve latency and cut cost
- The task type clearly benefits from fine-tuning over RAG: format adherence, stylistic consistency, or low-latency responses
- A production feature needs deterministic output structure (strict JSON schemas) that the base model produces inconsistently

## When NOT to use
- The goal is injecting new facts or knowledge — fine-tuning memorizes patterns, not facts; RAG is the correct approach
- Fewer than 50 high-quality examples are available — results will be marginal; invest in data collection first
- The task is straightforward and prompt engineering already achieves >90% quality — fine-tuning adds cost and operational overhead without meaningful gain
- The application uses many diverse tasks — a fine-tuned model for one task can regress on others; use separate prompts or separate fine-tuned models
- Rapid iteration is needed — fine-tuning jobs take 30-60 minutes and cost money to run; prompt engineering allows instant iteration

## Where it fails / limitations
- Fine-tuning does not improve reasoning ability — a fine-tuned `gpt-4o-mini` will not reason like `gpt-4o`; it will only follow patterns seen in training data
- The validation dataset in the `validate_dataset` script counts tokens but does not detect semantic quality issues — bad training examples produce a bad model even with zero format errors
- `generate_training_data` using GPT-4 to synthesize training data creates a feedback loop risk — the fine-tuned model will inherit GPT-4's errors and blind spots
- OpenAI fine-tuning does not expose training loss curves in real time — you must poll the job status API and wait for completion before knowing if training succeeded
- Once deployed, fine-tuned model behavior is opaque — there is no gradient inspection or attention visualization; behavioral debugging requires manual output analysis
- Fine-tuned model checkpoints expire after 90 days of inactivity on OpenAI — production systems must track checkpoint health and retrain before expiry

## Agentic workflow
An agent implementing OpenAI fine-tuning should operate across three phases with explicit checkpoints: (1) dataset preparation — validate JSONL format, count tokens, estimate cost, get human approval; (2) job submission — upload file, submit job, poll for completion, download metrics; (3) evaluation — run the fine-tuned model against a held-out test set, compare to the base model, decide whether to promote or retrain. Each phase is a discrete subagent step; human approval gates phases 1-to-2 and 2-to-3 transitions.

### Recommended subagents
- `faion-sdd-executor-agent` — drives fine-tuning pipeline from an SDD task card
- A data-prep subagent (custom) — runs `validate_dataset`, generates stats, flags format errors, returns go/no-go for training
- A job-monitor subagent (custom) — polls OpenAI fine-tuning job status every 5 minutes, notifies when complete or failed

### Prompt pattern
```
Review this sample of 5 training examples from a fine-tuning dataset.
Check for: consistent system prompt across all examples, assistant responses matching
the target style/format, user messages covering diverse query patterns.

Examples: {json_sample}

Return JSON: {
  "quality": "good|acceptable|poor",
  "issues": [str],
  "recommendation": "proceed|fix_and_resubmit|rebuild_dataset"
}
```

```
A fine-tuning job completed. Base model: {base_model}. Fine-tuned model: {ft_model}.
Test set results:
- Base model exact match: {base_score}
- Fine-tuned model exact match: {ft_score}
- Base model avg tokens per response: {base_tokens}
- Fine-tuned model avg tokens per response: {ft_tokens}

Should we promote the fine-tuned model to production?
Return JSON: {"promote": bool, "rationale": str, "threshold_met": bool}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` SDK | Upload files, create jobs, poll status, list models | `pip install openai` / [platform.openai.com/docs/guides/fine-tuning](https://platform.openai.com/docs/guides/fine-tuning) |
| `tiktoken` | Count tokens in training examples before upload | `pip install tiktoken` / [github.com/openai/tiktoken](https://github.com/openai/tiktoken) |
| `jsonlines` | Read/write JSONL fine-tuning datasets | `pip install jsonlines` |
| OpenAI CLI | `openai api fine_tuning.jobs.list` — list and cancel jobs | Included in `openai` package |
| `pandas` | Analyze token distribution, quality statistics | `pip install pandas` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Fine-tuning API | SaaS | Yes — REST API + Python SDK | The primary service; $3-25/1M training tokens depending on model |
| OpenAI Platform Dashboard | SaaS | Partial — no API for UI | Monitor job status, training loss curve, model list |
| Weights & Biases | SaaS | Yes — integrates via training metadata | Attach W&B run ID to fine-tuning job for experiment tracking |
| Argilla | OSS | Yes — Python SDK + REST | Data labeling and quality review platform for training data curation |
| Label Studio | OSS | Yes — REST API | Data annotation; export to JSONL format for fine-tuning |
| Scale AI | SaaS | Yes — REST API | Managed human data labeling for fine-tuning dataset creation |

## Templates & scripts
See `templates.md` for full fine-tuning pipeline script and JSONL schema.

Inline — end-to-end job submission and polling (≤45 lines):

```python
import time
from openai import OpenAI

client = OpenAI()

def submit_finetune_job(
    training_file: str,
    model: str = "gpt-4o-mini-2024-07-18",
    suffix: str = "custom-v1",
    n_epochs: int = 3,
) -> str:
    # Upload training file
    with open(training_file, "rb") as f:
        upload = client.files.create(file=f, purpose="fine-tune")
    print(f"Uploaded: {upload.id}")

    # Create fine-tuning job
    job = client.fine_tuning.jobs.create(
        training_file=upload.id,
        model=model,
        suffix=suffix,
        hyperparameters={"n_epochs": n_epochs},
    )
    print(f"Job created: {job.id}")

    # Poll until complete
    while job.status not in ("succeeded", "failed", "cancelled"):
        time.sleep(60)
        job = client.fine_tuning.jobs.retrieve(job.id)
        print(f"Status: {job.status}")

    if job.status == "succeeded":
        print(f"Fine-tuned model: {job.fine_tuned_model}")
        return job.fine_tuned_model
    else:
        raise RuntimeError(f"Fine-tuning failed: {job.error}")
```

## Best practices
- Curate quality over quantity — 200 excellent examples beat 2000 mediocre ones; have a human review a random 10% sample before submitting
- Keep system prompts identical across all training examples and match exactly the system prompt used in production inference — divergence is the most common cause of unexpected fine-tuned behavior
- Always split your dataset: 80% training, 20% held-out test; never evaluate on training data
- Run the base model on the held-out test set before fine-tuning to establish a baseline — without it you cannot measure the improvement delta
- Monitor training loss from the platform dashboard; if loss stops decreasing before epoch 2, the dataset is either too small or has quality issues
- Store fine-tuned model IDs in a config file or database with metadata (base model, dataset version, training date) — OpenAI model IDs are opaque strings that become impossible to manage at scale without a registry

## AI-agent gotchas
- Fine-tuning job submission is a human-in-loop breakpoint: agents must not auto-submit jobs without human review of the dataset stats and cost estimate — a bad dataset is expensive to discover after training
- OpenAI file upload has a 512MB limit — agents must check file size before upload; large datasets need chunking and multiple jobs
- `client.fine_tuning.jobs.retrieve()` polling in a tight loop will hit OpenAI rate limits — always sleep at least 30-60 seconds between poll calls
- The `fine_tuned_model` field in the job response is `null` until the job succeeds; agents that try to read it before checking `status == "succeeded"` will get an attribute error
- Fine-tuned models are not available in all regions or API endpoints immediately after training — there can be a 5-15 minute propagation delay before the model is callable
- Training data uploaded to OpenAI is stored by OpenAI; agents handling sensitive data must confirm data retention policies and use data opt-out headers where available

## References
- [OpenAI Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
- [Fine-tuning Best Practices — Preparing Your Dataset](https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset)
- [OpenAI Cookbook — Fine-tuning Chat Models](https://cookbook.openai.com/examples/how_to_finetune_chat_models)
- [tiktoken](https://github.com/openai/tiktoken)
- [Argilla — Data Labeling](https://argilla.io/)
- [Label Studio](https://labelstud.io/)
