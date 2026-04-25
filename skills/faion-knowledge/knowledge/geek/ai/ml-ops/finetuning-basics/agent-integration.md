# Agent Integration — Fine-tuning Basics (Techniques & Frameworks)

## When to use
- Need a model to consistently follow a domain-specific format or writing style that prompting cannot reliably enforce
- Building a product where inference latency matters and a smaller fine-tuned model can replace a larger prompted one
- Alignment work: converting RLHF/DPO preference data into a tuned model for controlled output behavior
- Repeated task patterns (extraction, classification, rewriting) where a small fine-tuned model beats few-shot on cost per call

## When NOT to use
- Adding new factual knowledge — fine-tuning memorizes patterns, not facts; use RAG instead
- Fewer than 100 high-quality examples — insufficient signal; use few-shot prompting
- One-off tasks — fine-tuning overhead (data prep, training, eval, hosting) is not justified
- Rapidly changing requirements — every dataset update requires a retrain cycle

## Where it fails / limitations
- Catastrophic forgetting: full fine-tuning and high LoRA ranks degrade general capabilities on tasks not in the training set
- Data leakage: PII or proprietary content in training data persists in model weights indefinitely
- Evaluation gap: training loss decreasing does not guarantee downstream task improvement — requires task-specific eval
- Framework fragility: Unsloth, Axolotl, LLaMA-Factory update frequently; pinned dependency versions break on new model releases
- ORPO/DPO requires chosen/rejected pairs — collecting rejection data from production is non-trivial for agents

## Agentic workflow
Claude subagents are effective for data preparation and experiment configuration, not for running training loops (those are long-running GPU jobs). An agent can generate training examples from a seed dataset, format them into the correct JSONL schema, validate format compliance, and produce an Axolotl or LLaMA-Factory config. The actual training job runs outside the agent via CLI; the agent can poll job status via the Weights & Biases API or cloud provider API and summarize results.

### Recommended subagents
- `faion-sdd-execution` — generate and validate training dataset from existing examples or documents
- Custom eval agent — after training completes, run lm-eval on benchmarks and compare to baseline

### Prompt pattern
```
Convert the following support ticket Q&A pairs into OpenAI fine-tuning JSONL format.
System prompt: "You are a customer support agent for {product}."
Output one JSON object per line. Include only pairs where the answer is complete and accurate.
Input: {raw_pairs}
```

```
Given this LLaMA-Factory training config template, fill in the correct values for:
base_model={model}, dataset_path={path}, lora_rank={rank}, output_dir={dir}.
Return only the completed YAML, no explanation.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `llamafactory-cli` | Train, export, chat with LLMs via CLI or WebUI | `pip install llamafactory` · github.com/hiyouga/LLaMA-Factory |
| `accelerate` | Multi-GPU/CPU training launcher for HF Trainer | `pip install accelerate` · huggingface.co/docs/accelerate |
| `axolotl` CLI | YAML-configured fine-tuning for complex scenarios | `pip install axolotl` · github.com/OpenAccess-AI-Collective/axolotl |
| `unsloth` | 2x faster LoRA training with 80% less VRAM | `pip install unsloth` · github.com/unslothai/unsloth |
| `mergekit` | Merge multiple fine-tuned models (SLERP, TIES, DARE) | `pip install mergekit` · github.com/arcee-ai/mergekit |
| `lm-eval` | Benchmark fine-tuned models on standard tasks | `pip install lm-eval` · github.com/EleutherAI/lm-evaluation-harness |
| `wandb` | Experiment tracking, loss curves, artifact storage | `pip install wandb` · wandb.ai |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Hugging Face Hub | SaaS/OSS | Yes — Python SDK | Model hosting, dataset storage, AutoTrain for no-code fine-tuning |
| Weights & Biases | SaaS | Yes — REST API | Training metrics, model registry, sweep orchestration |
| RunPod | SaaS | Partial — API for pod launch | On-demand GPU rental; no managed training but full control |
| Lambda Labs | SaaS | Partial | GPU cloud; cheaper than AWS for long runs |
| Modal | SaaS | Yes — Python SDK | Serverless GPU; good for short training jobs triggered by agents |
| Vast.ai | SaaS | Partial — REST API | Cheapest GPUs via auction; reliability varies |
| Google Colab | SaaS | No — browser-only | Suitable for prototyping; not agent-drivable |

## Templates & scripts
See `templates.md` for LLaMA-Factory and Unsloth quick-start scripts.

Inline: validate JSONL format before upload:
```python
import json, sys

def validate_ft_jsonl(path: str) -> list[str]:
    errors = []
    with open(path) as f:
        for i, line in enumerate(f, 1):
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"Line {i}: invalid JSON — {e}")
                continue
            if "messages" not in obj:
                errors.append(f"Line {i}: missing 'messages' key")
                continue
            roles = [m.get("role") for m in obj["messages"]]
            if "assistant" not in roles:
                errors.append(f"Line {i}: no assistant turn")
    return errors

errs = validate_ft_jsonl("training_data.jsonl")
if errs:
    print("\n".join(errs)); sys.exit(1)
print(f"Valid")
```

## Best practices
- Start with LoRA rank 8-16; only increase if validation loss plateaus and you have >5k examples
- Use DoRA over LoRA for tasks requiring nuanced style adaptation (it decomposes magnitude and direction separately)
- Always hold out 10% for validation and monitor validation loss independently — training loss alone is misleading
- Target all attention projections (q, k, v, o) plus MLP layers (gate, up, down) for complex tasks; q+v only for simple ones
- Use `bfloat16` over `float16` on A100/H100 — avoids NaN loss without quality loss
- Set `train_on_inputs: false` in Axolotl to avoid the model learning to repeat instructions
- Export to GGUF q4_k_m for local serving via Ollama; q8_0 for quality-critical deployments

## AI-agent gotchas
- Training jobs run for hours — agents cannot poll synchronously; use async job dispatch + webhook or file-based completion signal
- Dataset generation by LLM produces systematically biased examples (same phrasing, same edge-case coverage gaps) — mix with human-curated data
- Merging LoRA adapters before serving is mandatory for vLLM/TGI — PEFT adapters are not natively supported by all inference servers
- ORPO/DPO training requires the base model as reference; if the agent selects a wrong reference model, KL divergence calculation is invalid
- Model registry versioning is a human checkpoint: the agent should tag and store each fine-tuned model but not auto-deploy without review

## References
- https://arxiv.org/abs/2106.09685 (LoRA paper)
- https://arxiv.org/abs/2305.14314 (QLoRA paper)
- https://arxiv.org/abs/2403.07691 (ORPO paper)
- https://huggingface.co/docs/peft
- https://huggingface.co/docs/trl
- https://github.com/hiyouga/LLaMA-Factory
- https://github.com/unslothai/unsloth
- https://github.com/OpenAccess-AI-Collective/axolotl
- https://platform.openai.com/docs/guides/fine-tuning
