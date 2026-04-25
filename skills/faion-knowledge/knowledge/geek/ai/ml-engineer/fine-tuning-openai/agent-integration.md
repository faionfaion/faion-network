# Agent Integration — Fine-tuning (OpenAI)

## When to use
- Need task specialization on GPT-4.1/gpt-4o-mini without managing GPU infrastructure
- Output format must be consistent (JSON schema, structured extraction, specific tone)
- Prompt length reduction at scale: internalize long system prompts into the model
- DPO alignment needed: subjective preferences, brand voice, safety refinements
- Prototyping quickly: OpenAI fine-tuning requires no hardware — only JSONL data and an API key

## When NOT to use
- Fewer than 50 quality labeled examples — use few-shot prompting instead
- Need a private/on-premise model (OpenAI fine-tuned models stay on OpenAI infra)
- Real-time data dependency — fine-tuned model has a static knowledge snapshot; use RAG
- Task is exploratory or requirements will change within weeks — retrain cost makes this prohibitive
- Need full model weights (e.g., for offline inference) — OpenAI does not export weights

## Where it fails / limitations
- Fine-tuned model inference costs 2-3x the base model at equivalent quality for some tasks
- Training data quality is the main failure mode: a JSONL file with 10% noisy examples degrades the whole run
- DPO requires paired (preferred, non-preferred) examples — generating them is labor-intensive
- Model behavior on out-of-distribution inputs is unpredictable; eval on real traffic samples
- No direct access to training logs — only loss curve via API; debugging is harder than self-hosted
- Epoch count miscalibration (too many epochs → overfit, too few → underfit) is common; always use validation split

## Agentic workflow
A subagent builds and validates the JSONL training file, uploads it to the OpenAI Files API, creates a fine-tuning job, polls for completion (typically 15-60 minutes), runs an automated eval comparing fine-tuned vs base model on a held-out set, and gates deployment on a quality threshold. The fine-tuned model ID is written to a config file for downstream agents to consume. Human review is required before switching production traffic to the new model.

### Recommended subagents
- `faion-sdd-executor-agent` — orchestrates the multi-step job lifecycle as sequential SDD tasks

### Prompt pattern
```python
# Minimal OpenAI SFT fine-tuning job lifecycle
from openai import OpenAI
import time

client = OpenAI()

# 1. Upload training file
with open("train.jsonl", "rb") as f:
    training_file = client.files.create(file=f, purpose="fine-tune")

# 2. Create job
job = client.fine_tuning.jobs.create(
    training_file=training_file.id,
    model="gpt-4.1-mini",
    hyperparameters={"n_epochs": 3},
    validation_file=None,  # recommended: add validation file
)

# 3. Poll until done
while job.status not in ("succeeded", "failed", "cancelled"):
    time.sleep(60)
    job = client.fine_tuning.jobs.retrieve(job.id)
    print(f"Status: {job.status}")

print(f"Fine-tuned model: {job.fine_tuned_model}")
```

```
# Data format for SFT (JSONL, one example per line)
{"messages": [
  {"role": "system", "content": "You are a medical coding assistant."},
  {"role": "user", "content": "Patient has type 2 diabetes with neuropathy."},
  {"role": "assistant", "content": "E11.40"}
]}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` Python SDK | Jobs, file upload, model listing | `pip install openai` / platform.openai.com/docs/api-reference/fine-tuning |
| `openai` CLI | `openai api fine_tuning.jobs.list` for monitoring | bundled with SDK |
| `tiktoken` | Count tokens in training file before upload | `pip install tiktoken` / github.com/openai/tiktoken |
| `jsonlines` | Read/write JSONL files | `pip install jsonlines` |
| `openai-evals` | Eval harness for comparing base vs fine-tuned | `pip install evals` / github.com/openai/evals |
| `promptfoo` | A/B eval fine-tuned vs base | `npx promptfoo` / promptfoo.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Fine-tuning API | SaaS | Yes | REST + Python SDK; no GPU management needed |
| OpenAI Files API | SaaS | Yes | Upload training/validation JSONL; manage with `client.files` |
| OpenAI Evals | OSS | Partial | Eval harness; complex setup; better to write custom eval |
| Weights & Biases | SaaS | Yes | Log eval metrics; track model versions; agent reads via API |
| Braintrust | SaaS | Yes | Eval + tracing for OpenAI models; agent-friendly REST API |
| Langfuse | OSS/SaaS | Yes | Observability; compare base vs fine-tuned via traces |

## Templates & scripts
See `templates.md` for full training data templates and DPO pair format.

Training cost estimator (≤20 lines):

```python
import tiktoken

def estimate_training_cost(
    jsonl_path: str,
    model: str = "gpt-4.1-mini",
    epochs: int = 3
) -> float:
    prices = {"gpt-4.1": 25, "gpt-4.1-mini": 3, "gpt-4.1-nano": 1}  # $ per 1M tokens
    enc = tiktoken.encoding_for_model(model.replace("gpt-4.1", "gpt-4o"))
    total_tokens = 0
    with open(jsonl_path) as f:
        import json
        for line in f:
            row = json.loads(line)
            for msg in row["messages"]:
                total_tokens += len(enc.encode(msg["content"]))
    cost = (total_tokens / 1_000_000) * prices.get(model, 3) * epochs
    print(f"Tokens: {total_tokens:,} | Epochs: {epochs} | Est. cost: ${cost:.2f}")
    return cost
```

## Best practices
- Always include a validation file (10-20% split) — without it, overfitting is invisible
- Verify training data format with a script before uploading — malformed JSONL fails only at job start
- Use 3 epochs as a baseline; increase only if validation loss is still decreasing at epoch 3
- Enable data sharing (`integrations` param) for inference discounts if data is non-sensitive
- Compare fine-tuned model against base model on a held-out eval set before switching production traffic
- For DPO: generate non-preferred responses from the base model, not manually — ensures realistic negatives
- Document the fine-tuned model ID and training data hash in version control alongside config

## AI-agent gotchas
- Fine-tuning jobs run for 15-120 minutes; agent must poll asynchronously, not block a synchronous thread
- `client.fine_tuning.jobs.list_events(job_id)` is the only way to see training progress — parse these for loss values
- A failed job still returns 200 OK on creation; check `job.status` not HTTP status
- OpenAI fine-tuned model IDs look like `ft:gpt-4.1-mini-2025-01-01:org::xxxxx` — store in config, never hardcode
- Human checkpoint before routing live traffic to a new fine-tuned model is mandatory — eval on synthetic data is not enough
- Do not share training data containing PII with OpenAI unless you have a DPA in place and user consent

## References
- https://platform.openai.com/docs/guides/fine-tuning
- https://platform.openai.com/docs/api-reference/fine-tuning
- https://platform.openai.com/docs/guides/direct-preference-optimization
- https://platform.openai.com/docs/guides/supervised-fine-tuning
- https://cookbook.openai.com/examples/how_to_finetune_chat_models
- https://openai.com/api/pricing/
