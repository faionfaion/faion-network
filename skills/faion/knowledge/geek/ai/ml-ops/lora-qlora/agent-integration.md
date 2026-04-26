# Agent Integration — LoRA and QLoRA

## When to use
- Fine-tuning an open-source model (LLaMA, Mistral, Qwen, Phi) on a custom dataset with limited GPU memory
- Training domain-specific adapters that can be swapped at inference time without reloading the base model
- Producing multiple task-specific adapters from one base model (customer support, code, summarization)
- Reducing fine-tuning cost vs. full fine-tuning: QLoRA brings a 70B model into a single 48GB GPU
- Creating a task-specific model when OpenAI fine-tuning is too expensive or the data must stay on-prem

## When NOT to use
- Fewer than 500-1000 domain-specific examples — few-shot prompting or RAG will outperform a poorly-trained adapter
- The goal is injecting new factual knowledge — LoRA improves style/format, not factual recall; use RAG for knowledge
- The target task is simple enough for a prompt template with a smaller base model
- The team lacks GPU access (even a single A100 or consumer 3090/4090); CPU-only training is impractical
- Production requires strict reproducibility; adapter merging and quantization introduce non-determinism

## Where it fails / limitations
- `prepare_model_for_kbit_training` must be called before `get_peft_model`; reversing the order silently produces wrong gradient updates
- DoRA (`use_dora=True`) is incompatible with some PEFT versions and some quantization backends — test before committing to it
- Adapter merging (`merge_and_unload`) with quantized base models can produce quality degradation vs. keeping adapter separate
- `paged_adamw_8bit` requires `bitsandbytes` which only supports Linux with CUDA; macOS and Windows fail at training time
- Scaling factor (`set_adapter_scale`) affects all LoRA layers uniformly — there is no per-layer control without custom patching
- Flash Attention 2 (often needed for long sequences) is incompatible with some quantization configs; test memory estimates before training

## Agentic workflow
An agent implementing LoRA/QLoRA fine-tuning should operate in three phases: (1) dataset validation and hyperparameter selection based on dataset size and target task complexity, (2) supervised fine-tuning run with training loss monitoring and early stopping, (3) adapter evaluation using a held-out set before merging or publishing. Each phase can be a discrete subagent step with a human-in-loop checkpoint before the expensive GPU training phase begins.

### Recommended subagents
- `faion-sdd-executor-agent` — drives task-card-based fine-tuning workflow from spec through evaluation
- A dataset-prep subagent (custom) — validates JSONL format, computes token counts, flags out-of-range examples
- A training-monitor subagent (custom) — polls training logs, detects loss divergence, sends alert if validation loss increases for N consecutive steps

### Prompt pattern
```
Given the following dataset stats (N examples, avg token length X),
select LoRA hyperparameters (rank, alpha, target_modules, learning_rate, epochs)
for task type: {classification|generation|instruction-following}.
Return JSON: {"r": int, "lora_alpha": int, "target_modules": list, "lr": float, "epochs": int, "rationale": str}
```

```
Review this training loss curve (values: {loss_list}).
Is training healthy? Flag: divergence (loss > initial after warmup),
overfitting (train loss << val loss), or plateaued (delta < 0.001 for 5 steps).
Return: {"status": "healthy|diverging|overfitting|plateaued", "action": str}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `peft` | LoRA/QLoRA adapter creation, loading, merging | `pip install peft` / [huggingface.co/docs/peft](https://huggingface.co/docs/peft) |
| `trl` | `SFTTrainer` for supervised fine-tuning | `pip install trl` / [huggingface.co/docs/trl](https://huggingface.co/docs/trl) |
| `bitsandbytes` | NF4 quantization, paged optimizers | `pip install bitsandbytes` / [github.com/TimDettmers/bitsandbytes](https://github.com/TimDettmers/bitsandbytes) |
| `transformers` | Model loading, `BitsAndBytesConfig` | `pip install transformers` / [huggingface.co/docs/transformers](https://huggingface.co/docs/transformers) |
| `axolotl` | YAML-config-driven LoRA/QLoRA training pipeline | `pip install axolotl` / [github.com/OpenAccess-AI-Collective/axolotl](https://github.com/OpenAccess-AI-Collective/axolotl) |
| `llm-foundry` | MosaicML production-grade LoRA training | [github.com/mosaicml/llm-foundry](https://github.com/mosaicml/llm-foundry) |
| `nvidia-smi` | Monitor GPU memory during training | Preinstalled with NVIDIA drivers |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Hugging Face Hub | SaaS/OSS | Yes — push/pull adapters via API | Store and version adapters; `model.push_to_hub()` |
| Modal | SaaS | Yes — GPU on-demand, Python SDK | Good for one-off training runs without managing infra |
| Replicate | SaaS | Yes — REST API for training runs | Supports fine-tuning Llama models; pay-per-GPU-second |
| RunPod | SaaS | Partial — SSH access, no native agent SDK | Cheap A100 rentals; use for longer training jobs |
| Lambda Labs | SaaS | Partial — SSH, hourly GPU billing | On-demand A10/A100 clusters |
| Weights & Biases | SaaS | Yes — `wandb` integration in `TrainingArguments` | Real-time loss curve tracking, sweep for hyperparameter search |
| Axolotl (OSS) | OSS | Yes — YAML config, CLI-driven | Best for reproducible LoRA runs without writing training code |

## Templates & scripts
See `templates.md` for full QLoRA training config and axolotl YAML.

Inline — minimal QLoRA fine-tune with W&B logging (≤50 lines):

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
from datasets import load_dataset

MODEL = "meta-llama/Llama-3.1-8B"
bnb = BitsAndBytesConfig(
    load_in_4bit=True, bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True,
)
model = AutoModelForCausalLM.from_pretrained(MODEL, quantization_config=bnb, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(MODEL)
tokenizer.pad_token = tokenizer.eos_token
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, LoraConfig(
    r=16, lora_alpha=16, lora_dropout=0.05, bias="none", task_type="CAUSAL_LM",
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
))
model.gradient_checkpointing_enable()
dataset = load_dataset("json", data_files="train.jsonl", split="train")
trainer = SFTTrainer(
    model=model, tokenizer=tokenizer, train_dataset=dataset,
    dataset_text_field="text", max_seq_length=2048,
    args=TrainingArguments(
        output_dir="./out", num_train_epochs=3, per_device_train_batch_size=2,
        gradient_accumulation_steps=4, learning_rate=2e-4, optim="paged_adamw_8bit",
        lr_scheduler_type="cosine", warmup_ratio=0.03, fp16=True,
        logging_steps=10, save_steps=100, report_to="wandb",
    ),
)
trainer.train()
model.save_pretrained("./adapter")
```

## Best practices
- Target all attention projections (q, k, v, o) plus MLP layers (gate, up, down) for instruction-following tasks — targeting only q/v (common shortcut) leaves 40-60% of trainable capacity unused
- Always call `gradient_checkpointing_enable()` before training — saves ~30% memory at ~15% throughput cost, worth it for 8B+ models
- Use `bf16=True` instead of `fp16=True` on A100/H100 — bf16 has wider dynamic range and avoids overflow on long training runs
- Validate dataset token length distribution before training; sequences truncated at `max_seq_length` mid-sentence silently degrade quality
- Evaluate with `temperature=0` on a fixed held-out set before and after training to isolate adapter effect from sampling noise
- For multiple adapters on one base model, keep adapters separate (do not merge) — merging permanently alters the base and prevents future adapter switching
- Log `trainable_parameters` percentage at the start; if it exceeds 2%, the rank is likely too high for the available GPU memory

## AI-agent gotchas
- Training is a human-in-loop breakpoint: agents must not auto-submit GPU jobs without human confirmation of dataset quality, cost estimate, and hyperparameters — a bad config on a large cluster is expensive
- `model.save_pretrained()` saves only the adapter, not the base model; agents that try to load the adapter path directly as a full model will fail with a dimension mismatch error
- bitsandbytes installation frequently fails on non-CUDA environments — agents running in CPU-only containers will hit import errors; gate on `torch.cuda.is_available()` before attempting QLoRA setup
- The `SFTTrainer` `dataset_text_field` parameter must exactly match the column name in the dataset; a mismatch raises a non-obvious KeyError during the first forward pass, not at init
- Wandb API key must be set as env var `WANDB_API_KEY` or training silently logs nowhere; agents should verify the key before starting a run

## References
- [LoRA Paper (Hu et al., 2021)](https://arxiv.org/abs/2106.09685)
- [QLoRA Paper (Dettmers et al., 2023)](https://arxiv.org/abs/2305.14314)
- [DoRA Paper (Liu et al., 2024)](https://arxiv.org/abs/2402.09353)
- [PEFT Documentation](https://huggingface.co/docs/peft)
- [TRL SFTTrainer](https://huggingface.co/docs/trl/sft_trainer)
- [Axolotl (config-driven LoRA)](https://github.com/OpenAccess-AI-Collective/axolotl)
- [bitsandbytes](https://github.com/TimDettmers/bitsandbytes)
