# Agent Integration — Fine-tuning (LoRA)

## When to use
- Need consistent domain-specific terminology or jargon the base model handles inconsistently
- Output format must be exact and reliable (JSON schema, medical codes, proprietary syntax)
- Inference cost reduction matters: fine-tuned models need shorter system prompts
- You have 500+ quality labeled examples in the target distribution
- Style/brand voice consistency is required at high volume where per-call prompting is expensive

## When NOT to use
- Fewer than 100 high-quality examples — few-shot prompting will outperform
- Requirements are changing: fine-tuned model becomes a liability when task evolves
- Need real-time knowledge: fine-tuning bakes in a knowledge snapshot, use RAG for live data
- No GPU access and budget is limited: OpenAI fine-tuning (API-only) is a better path
- Model needs to handle wildly different tasks — specialized adapter degrades generality

## Where it fails / limitations
- Catastrophic forgetting: training only on narrow data erodes general capabilities; mitigate with 20-30% general data mixing
- LoRA adapters are architecture-specific — adapter trained on Llama-3-8B won't load on Mistral-7B
- Rank too low (r<4) → adapter underfits; rank too high (r>128) without rsLoRA → gradient instability
- QLoRA reduces precision: 4-bit quantization introduces noise; accept 5-10% quality drop vs full LoRA
- Adapter merging into base weights requires enough VRAM to hold full model; plan storage and compute separately
- Data contamination: if evaluation examples leak into training set, reported metrics are meaningless

## Agentic workflow
A subagent orchestrates the fine-tuning pipeline: it generates a config from a template (Axolotl or Unsloth YAML), submits a training job to a GPU cloud (Modal, RunPod, Lambda), polls for completion, downloads the adapter checkpoint, runs an automated eval, and gates deployment on a passing score threshold. Human review is required before pushing a merged model to production inference.

### Recommended subagents
- `faion-sdd-executor-agent` — manages training job lifecycle and eval gates in SDD-style task loop

### Prompt pattern
```
# Task: Prepare LoRA fine-tuning config
Given the dataset path, base model, and hardware constraints below, output
a valid Axolotl YAML config. Set lora_r, lora_alpha, learning_rate, and
num_epochs based on dataset size. Include validation split.

Dataset: {path}
Base model: {model_id}
GPU VRAM: {vram_gb}GB
Examples: {num_examples}
```

```python
# Minimal PEFT LoRA training stub (Unsloth path)
from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/llama-3-8b-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    lora_alpha=32,
    target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
    use_rslora=False,
    use_gradient_checkpointing="unsloth",
)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `peft` | LoRA/QLoRA/DoRA adapter API | `pip install peft` / huggingface.co/docs/peft |
| `trl` | SFT, DPO, ORPO trainers | `pip install trl` / huggingface.co/docs/trl |
| `unsloth` | 2x speed, 80% less VRAM | `pip install unsloth` / unsloth.ai |
| `axolotl` | YAML-config-driven training | `pip install axolotl` / github.com/OpenAccess-AI-Collective/axolotl |
| `llama-factory` | WebUI + CLI training | `pip install llamafactory` / github.com/hiyouga/LLaMA-Factory |
| `mergekit` | Merge LoRA adapters into base | `pip install mergekit` / github.com/arcee-ai/mergekit |
| `lm-eval` | Harness for standardized evals | `pip install lm-eval` / github.com/EleutherAI/lm-evaluation-harness |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Modal | SaaS | Yes | GPU cloud with Python SDK; ideal for agent-triggered training jobs |
| RunPod | SaaS | Yes | On-demand A100/H100; REST API for pod lifecycle |
| Lambda Cloud | SaaS | Yes | Per-hour GPU; cheaper for long runs |
| Hugging Face AutoTrain | SaaS | Partial | Web UI + API; limited config flexibility |
| Vast.ai | SaaS | Yes | Spot GPU market; cheapest option, less reliable SLA |
| Weights & Biases | SaaS | Yes | Training tracking; agent reads metrics via W&B API for eval gates |
| MLflow | OSS | Yes | Self-hosted experiment tracking; log adapter artifacts and metrics |

## Templates & scripts
See `templates.md` for full Axolotl and Unsloth YAML configs. Eval gate script (≤30 lines):

```python
# eval_gate.py — pass/fail gate for fine-tuned adapter
import json, subprocess, sys

THRESHOLD = 0.85  # minimum accuracy on task eval
MODEL_PATH = sys.argv[1]
EVAL_DATASET = sys.argv[2]

result = subprocess.run(
    ["lm_eval", "--model", "hf", "--model_args", f"pretrained={MODEL_PATH}",
     "--tasks", "custom_task", "--device", "cuda:0", "--output_path", "eval_out.json"],
    capture_output=True, text=True
)
with open("eval_out.json") as f:
    metrics = json.load(f)

score = metrics["results"]["custom_task"]["acc,none"]
print(f"Eval score: {score:.3f} (threshold: {THRESHOLD})")
sys.exit(0 if score >= THRESHOLD else 1)
```

## Best practices
- Target all linear layers (q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj) for best coverage
- Start with r=16, alpha=32; increase r only if validation loss plateaus after 2 epochs
- Mix 20-30% general instruction data with task-specific data to prevent catastrophic forgetting
- Use rsLoRA (`use_rslora=True`) when r>64 to avoid gradient instability
- Validate data quality manually: sample 50 examples before submitting any training job
- Track training and validation loss separately — diverging val loss after epoch 2 means overfit
- Save adapter only (not merged weights) until eval passes; merged weights are harder to rollback

## AI-agent gotchas
- Agent must not auto-deploy an adapter without a passing eval gate — always gate on quantitative threshold
- GPU cloud spot instances can be preempted mid-training; configure Axolotl checkpointing every 100 steps
- Training job APIs (Modal, RunPod) are async — agent must poll with backoff, not block synchronously
- W&B API key must be present in agent environment before training starts; missing key silently skips logging
- Adapter VRAM footprint is small, but inference of merged model requires full base model VRAM — size accordingly
- Human checkpoint required when deploying fine-tuned model to production serving (it may behave unexpectedly on out-of-distribution inputs)

## References
- https://arxiv.org/abs/2106.09685 (LoRA paper)
- https://arxiv.org/abs/2305.14314 (QLoRA paper)
- https://arxiv.org/abs/2402.09353 (DoRA paper)
- https://huggingface.co/docs/peft
- https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide
- https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms
