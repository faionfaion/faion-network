# Agent Integration — Fine-tuning OpenAI (Production)

## When to use
- Need a fine-tuned model deployable via the OpenAI API with zero infrastructure overhead
- Task has 50-10,000 high-quality examples in JSONL chat format and consistent system prompt
- Latency tolerance: fine-tuning jobs take 15 minutes to several hours depending on dataset size
- Use case: style consistency, domain-specific tone, structured output format enforcement, task-specific classifier

## When NOT to use
- Fewer than 50 examples — base model with few-shot beats fine-tuning; data quality cannot compensate
- Task requires up-to-date factual knowledge — OpenAI fine-tuning does not inject new facts
- Cost sensitivity at inference: `ft:gpt-4o-mini` costs 3-6x more per token than base gpt-4o-mini — verify ROI before committing
- Proprietary data that must not leave your infrastructure — training data is processed on OpenAI servers
- Need for a fully private model weight — OpenAI retains training data per their data policy

## Where it fails / limitations
- `n_epochs: auto` with small datasets (<200 examples) often selects too many epochs → overfitting; set explicit `n_epochs: 2-3`
- No access to training loss curve in real-time via API — must poll events or wait for job completion
- Validation loss reported by OpenAI events is not the same as task-specific accuracy; add your own eval step
- `fine_tuned_model` ID in job response is ephemeral — model may be deprecated if OpenAI retires the base model version
- The evaluator-LLM pattern (using GPT-4o to score fine-tuned GPT-4o-mini responses) has circular bias — prefer deterministic eval metrics when possible
- Job status polling with 60-second sleep loops are blocking for agents — use async polling or webhook if available

## Agentic workflow
An agent can orchestrate the full OpenAI fine-tuning pipeline: validate and format training data → upload file → create job → poll status → retrieve model name → run evaluation against a test set → log results. The decision to deploy the fine-tuned model should be a human checkpoint, not an automated step. The agent writes the model ID to a config file; a human approves deployment by updating the production config.

### Recommended subagents
- `faion-sdd-execution` — prepare and validate JSONL training data; check format compliance and example count
- Custom eval agent — after job completion, run fine-tuned model against test set and produce score table vs. base model

### Prompt pattern
```
Validate the following JSONL fine-tuning data for OpenAI format compliance.
Check: (1) each line is valid JSON, (2) has "messages" key, (3) contains at least one
"user" and one "assistant" role, (4) system prompt is consistent across all examples.
Report violations with line numbers.
Input: {jsonl_content}
```

```
Job {job_id} has completed. Fine-tuned model: {model_id}.
Run 10 test prompts from {test_file} against both {model_id} and {base_model}.
Score each response pair on: format_match (0/1), content_quality (1-5).
Return JSON summary with average scores and failing examples.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` Python SDK | Upload files, create jobs, poll status, list events | `pip install openai` · platform.openai.com/docs/guides/fine-tuning |
| `openai` CLI | Check fine-tuning job status from terminal | `openai api fine_tuning.jobs.list` |
| `tiktoken` | Count tokens to estimate training cost before upload | `pip install tiktoken` · github.com/openai/tiktoken |
| `jsonlines` | Read/write JSONL training files cleanly | `pip install jsonlines` |
| `wandb` | Log fine-tuning run metadata and eval scores | `pip install wandb` · wandb.ai |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Fine-tuning API | SaaS | Yes — Python SDK | Native; no infra; models served at `ft:*` prefix |
| OpenAI Files API | SaaS | Yes — SDK | Upload/manage training files; 1GB limit per file |
| Weights & Biases | SaaS | Yes — REST API | Track eval scores, model versions alongside fine-tuning metadata |
| Helicone | SaaS | Yes — proxy | Log fine-tuned model inference for cost/quality tracking |
| Portkey | SaaS | Yes — gateway | Fallback from fine-tuned model to base model on errors |

## Templates & scripts
See `templates.md` for the `FineTuningPipeline` class.

Inline: estimate training token cost before upload:
```python
import json, tiktoken

def estimate_ft_cost(jsonl_path: str, model: str = "gpt-4o-mini-2024-07-18",
                     n_epochs: int = 3, cost_per_1m: float = 3.00) -> dict:
    enc = tiktoken.encoding_for_model("gpt-4o")  # same encoding family
    total_tokens = 0
    with open(jsonl_path) as f:
        for line in f:
            obj = json.loads(line)
            for msg in obj["messages"]:
                total_tokens += len(enc.encode(msg["content"]))
    training_tokens = total_tokens * n_epochs
    cost = (training_tokens / 1_000_000) * cost_per_1m
    return {"total_tokens": total_tokens, "training_tokens": training_tokens,
            "estimated_cost_usd": round(cost, 4)}

print(estimate_ft_cost("training_data.jsonl"))
```

## Best practices
- Validate JSONL format locally before upload — the API rejects malformed files after upload, wasting time
- Use `suffix` parameter for model naming: `"customer-support-v2"` → reproducible model IDs across experiments
- Always create a validation file (10% of data) and pass `validation_file` — OpenAI reports val loss in job events
- Prefer `gpt-4o-mini-2024-07-18` for fine-tuning: lowest training cost, fast inference, good quality for structured tasks
- Hold out a test set (separate from validation) for post-training eval; never evaluate on training or validation data
- After fine-tuning, compare to few-shot base model on the same test set; if improvement < 10%, reconsider
- Version and store `fine_tuned_model` IDs in config/db — OpenAI does not guarantee indefinite availability of base model versions

## AI-agent gotchas
- File upload is synchronous but job creation is async — the agent must poll `client.fine_tuning.jobs.retrieve(job_id)` with exponential backoff, not a fixed 60-second sleep
- `job.status` values include `"validating_files"`, `"queued"`, `"running"`, `"succeeded"`, `"failed"`, `"cancelled"` — agents must handle all states, not just succeeded/failed
- The evaluator-LLM pattern where GPT-4o scores fine-tuned GPT-4o-mini is useful but costs money; cap eval sample size at 50-100 examples for routine checks
- Training data uploaded via Files API persists until explicitly deleted — agents should clean up after training to avoid hitting storage limits
- Model IDs contain the organization slug — if the agent stores the ID and the org changes, the ID becomes invalid

## References
- https://platform.openai.com/docs/guides/fine-tuning
- https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset
- https://cookbook.openai.com/examples/how_to_finetune_chat_models
- https://platform.openai.com/docs/api-reference/fine-tuning
