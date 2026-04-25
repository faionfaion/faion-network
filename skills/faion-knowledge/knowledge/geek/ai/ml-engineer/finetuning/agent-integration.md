# Agent Integration — LLM Fine-tuning (General Guide)

## When to use
- Prompt engineering and RAG have both been tried and still fail to meet quality bar
- Domain jargon, output format, or behavioral style needs to be internalized rather than injected per-call
- Production volume is high enough that shorter prompts (from internalized instructions) reduce inference cost meaningfully
- You have 500+ verified examples in the target distribution with clear correct/incorrect labels
- Compliance requires a local or private model with no external API calls

## When NOT to use
- You have fewer than 100 quality examples — fine-tuning will overfit; use few-shot prompting
- Task requirements are exploratory or changing — fine-tuning creates a liability that degrades as the task evolves
- Real-time knowledge is required — fine-tuning bakes in a snapshot; add RAG for dynamic data
- No labeled data exists — data collection must precede training; don't skip this step
- Time-to-production is critical — fine-tuning adds days of iteration; try prompting first

## Where it fails / limitations
- Catastrophic forgetting: narrow fine-tuning erodes general capabilities unless general data is mixed in
- Evaluation gap: a fine-tuned model can score well on held-out examples but fail on real traffic distribution
- Data quality dependency: garbage in, garbage out — 1,000 clean examples beat 100K noisy ones
- Version lock: switching base model versions requires full retraining of adapters
- Cost: full fine-tuning of 70B+ models requires A100/H100 clusters; even QLoRA on 70B needs 80GB VRAM
- No rollback without versioning: deploying a bad model with no checkpoint is unrecoverable

## Agentic workflow
A subagent executes the fine-tuning pipeline in stages: data validation → config generation → job submission to GPU cloud → training monitoring → eval gate → conditional deployment. Each stage is a checkpoint; the agent does not auto-advance past the eval gate without a passing score. Human review is required before the merged model goes to production inference.

### Recommended subagents
- `faion-sdd-executor-agent` — drives training job lifecycle as an SDD task sequence

### Prompt pattern
```
# Task: Fine-tuning decision assessment
Given the following task description and dataset stats, determine whether
fine-tuning is the right approach or if prompting/RAG should be tried first.
Output: recommendation (fine-tune | prompt | rag) + one-line rationale.

Task: {task_description}
Examples available: {num_examples}
Quality verified: {quality_verified}
Latency requirement: {latency_ms}ms
Budget per inference: ${budget_per_call}
```

```python
# Framework selection helper
def select_framework(vram_gb: int, examples: int, need_webui: bool) -> str:
    if need_webui:
        return "llama-factory"
    if vram_gb < 16:
        return "unsloth"  # QLoRA, 4-bit
    if examples > 50_000:
        return "axolotl"  # handles large datasets well
    return "trl"          # HuggingFace native, most flexible
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `trl` | SFT, DPO, ORPO trainers; HuggingFace native | `pip install trl` / huggingface.co/docs/trl |
| `unsloth` | 2-5x faster, 80% less VRAM; drop-in for PEFT | `pip install unsloth` / unsloth.ai |
| `axolotl` | YAML-driven; handles complex multi-dataset configs | `pip install axolotl` / github.com/OpenAccess-AI-Collective/axolotl |
| `llama-factory` | WebUI + CLI; beginner-friendly | `pip install llamafactory` / github.com/hiyouga/LLaMA-Factory |
| `torchtune` | PyTorch-native; clean recipes | `pip install torchtune` / github.com/pytorch/torchtune |
| `lm-eval` | Standardized eval harness | `pip install lm-eval` / github.com/EleutherAI/lm-evaluation-harness |
| `mergekit` | Merge fine-tuned adapters | `pip install mergekit` / github.com/arcee-ai/mergekit |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Fine-tuning API | SaaS | Yes | No GPU needed; API-only; supports SFT + DPO + RFT |
| Modal | SaaS | Yes | Python SDK for GPU jobs; agent-submittable via `modal run` |
| RunPod | SaaS | Yes | REST API; H100/A100 pods on demand |
| Hugging Face AutoTrain | SaaS | Partial | REST API; limited config control |
| Weights & Biases | SaaS | Yes | Training metrics; agent reads via API for eval gates |
| MLflow | OSS | Yes | Self-hosted tracking; log adapters and metrics |
| Together AI | SaaS | Yes | Managed fine-tuning API; supports open models |

## Templates & scripts
See `templates.md` for full Axolotl YAML and Unsloth training configs.

Data quality validation before training:

```python
import json, sys
from pathlib import Path

def validate_jsonl(path: str, min_examples: int = 100) -> bool:
    """Validate JSONL training file format and size."""
    rows = []
    with open(path) as f:
        for i, line in enumerate(f, 1):
            try:
                row = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Line {i}: JSON error — {e}")
                return False
            if "messages" not in row:
                print(f"Line {i}: missing 'messages' key")
                return False
            rows.append(row)
    if len(rows) < min_examples:
        print(f"Only {len(rows)} examples (need {min_examples})")
        return False
    print(f"Validated {len(rows)} examples OK")
    return True

if __name__ == "__main__":
    sys.exit(0 if validate_jsonl(sys.argv[1]) else 1)
```

## Best practices
- Follow the decision tree: prompting → RAG → fine-tuning; don't skip steps
- Validate training data format and balance before any job submission
- Mix 20-30% general instruction data to prevent catastrophic forgetting
- Track training and validation loss in W&B or MLflow; stop early if val loss diverges
- Run task-specific eval (not just perplexity) against a held-out set before deployment
- Version adapters and base model checkpoints separately; never overwrite checkpoints in-place
- Keep a golden test set untouched during training — reserve it exclusively for final eval

## AI-agent gotchas
- Agent must validate data format before submitting any training job — bad JSONL fails silently on some platforms
- Training jobs are async; agent needs polling with exponential backoff (not synchronous wait)
- Eval gate is mandatory: agent must not auto-deploy on training completion without a passing score
- GPU spot preemption is common; ensure checkpoint every N steps to allow resume without full restart
- W&B / MLflow API keys must be injected into the training environment before job start
- Human-in-loop checkpoint before production deployment is non-negotiable for any model serving real users

## References
- https://huggingface.co/docs/trl
- https://huggingface.co/docs/peft
- https://github.com/unslothai/unsloth
- https://github.com/OpenAccess-AI-Collective/axolotl
- https://platform.openai.com/docs/guides/fine-tuning
- https://arxiv.org/html/2408.13296v1 (survey of LLM fine-tuning)
