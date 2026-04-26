# Agent Integration — Fine-tuning (LoRA)

## When to use
- Consumer GPU available (8-24GB VRAM) and full fine-tuning is not feasible
- Need to maintain multiple task-specific adapters on one base model (switch at runtime without reloading weights)
- Quick iteration experiments where training must complete in hours, not days
- Adapting model behavior/style without degrading general capabilities (low rank keeps most weights frozen)
- Production scenario requiring a specialized model that is cheaper to serve than a large prompted model

## When NOT to use
- Task requires adding substantial new factual knowledge — LoRA adapters do not reliably encode facts; use RAG
- Dataset is smaller than 50 examples — adapter overfits immediately; use few-shot prompting instead
- Target inference server (e.g., older TGI versions) does not support on-the-fly adapter loading — merge first
- Real-time latency requirement below 100ms — adapter overhead adds ~5-10ms per forward pass; full merge eliminates this

## Where it fails / limitations
- Wrong `target_modules` for a model family causes 0 trainable parameters — training proceeds silently with no effect
- Rank too low (r=4) on complex tasks causes underfitting that looks like poor data quality
- Padding token not set on the tokenizer causes silent data corruption in batch training
- `evaluation_strategy` requires a validation dataset to be passed; omitting it while setting the strategy raises a runtime error
- LoRA adapter saved without the tokenizer cannot be reproduced or shared — always save both
- `paged_adamw_8bit` optimizer is only available when `bitsandbytes` is installed and CUDA is available; CPU training requires `adamw_torch`

## Agentic workflow
Claude subagents handle the non-GPU portions of the LoRA pipeline: generating training data, selecting rank and target modules based on model family and task type, constructing the `LoraConfig`, and writing the training script. The actual `trainer.train()` call is dispatched to a GPU instance via shell command or cloud API. Post-training, an agent can load the adapter, run sample inferences, and decide whether to merge-and-export or discard. Human review is required before merging adapters into a production base model.

### Recommended subagents
- `faion-sdd-execution` — generate LoRA config from task description and model family, validate target_modules match model architecture
- Custom eval agent — load adapter, run 20-30 representative test prompts, score outputs, return pass/fail

### Prompt pattern
```
Given model family "{model_family}" and task type "{task_type}", select:
1. Appropriate lora_rank (8/16/32/64)
2. target_modules list (provide exact names for this architecture)
3. learning_rate
4. Whether to include MLP layers
Output JSON: {rank, alpha, target_modules, learning_rate, rationale}
```

```
Examine these 5 sample outputs from the LoRA-tuned model vs the base model.
Score each on: format_adherence (0-1), content_quality (0-1), regression_risk (0-1).
Flag any output where regression_risk > 0.7 for human review.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `peft` | LoRA/QLoRA adapter creation and management | `pip install peft` · huggingface.co/docs/peft |
| `trl` | SFTTrainer, DPOTrainer, ORPOTrainer | `pip install trl` · huggingface.co/docs/trl |
| `bitsandbytes` | 4-bit/8-bit quantization for QLoRA | `pip install bitsandbytes` · github.com/TimDettmers/bitsandbytes |
| `accelerate` | Multi-GPU training launcher | `pip install accelerate` · huggingface.co/docs/accelerate |
| `mergekit` | Merge LoRA adapter into base model weights | `pip install mergekit` · github.com/arcee-ai/mergekit |
| `unsloth` | 2x faster LoRA, direct GGUF export | `pip install unsloth` · github.com/unslothai/unsloth |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Hugging Face Hub | SaaS/OSS | Yes — SDK | Push/pull adapters; `model.push_to_hub()` |
| Weights & Biases | SaaS | Yes — REST | Loss tracking, adapter artifact registry |
| RunPod | SaaS | Partial | GPU pod launch via API; SSH for training |
| Modal | SaaS | Yes — Python SDK | Serverless GPU; run `trainer.train()` as a Modal function |
| Ollama | OSS | Yes — REST :11434 | Serve merged GGUF; agent calls `/api/generate` |
| vLLM | OSS | Yes — OpenAI API | Serve merged model; requires merge before deployment |

## Templates & scripts
See `templates.md` for the `LoRATrainingPipeline` class and multiple-adapter switching pattern.

Inline: verify trainable parameter count after applying LoRA:
```python
def check_lora_params(model) -> dict:
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    if trainable == 0:
        raise ValueError("No trainable parameters — check target_modules names")
    return {
        "trainable": trainable,
        "total": total,
        "pct": f"{100 * trainable / total:.4f}%"
    }

stats = check_lora_params(model)
print(stats)  # Expected: trainable% between 0.01% and 2%
```

## Best practices
- Print trainable parameter count immediately after `get_peft_model()` — if it shows 0, stop and fix `target_modules`
- Use `SFTTrainer` from TRL instead of raw `Trainer` — it handles dataset formatting, packing, and LoRA integration more reliably
- Set `use_gradient_checkpointing="unsloth"` when using Unsloth — saves ~30% VRAM vs. standard gradient checkpointing
- Always save tokenizer alongside adapter: `model.save_pretrained(path)` + `tokenizer.save_pretrained(path)`
- When doing hyperparameter search, vary rank (8/16/32) first; alpha usually set equal to rank is fine for initial experiments
- Merge the adapter before deployment to vLLM: `model.merge_and_unload()` — this has zero quality loss and removes adapter overhead
- For multi-adapter workflows: keep adapters separate, load at runtime; do not mix-merge adapters trained on incompatible tasks

## AI-agent gotchas
- `prepare_model_for_kbit_training()` must be called before `get_peft_model()` for QLoRA; reversing order causes silent training failure
- GPU OOM during training is recoverable by reducing `per_device_train_batch_size` to 1 and increasing `gradient_accumulation_steps` proportionally — an agent can attempt this automatically
- Adapter checkpointing writes partial files during training; an agent reading an intermediate checkpoint will get a corrupt model — always load from the final `output_dir`
- Multiple simultaneous LoRA experiments on the same GPU will OOM — agents must serialize GPU jobs, not parallelize them
- `evaluation_strategy="epoch"` with no `eval_dataset` raises a `ValueError` at epoch end, not at job start — a common source of wasted compute

## References
- https://arxiv.org/abs/2106.09685 (LoRA)
- https://arxiv.org/abs/2305.14314 (QLoRA)
- https://huggingface.co/docs/peft/conceptual_guides/lora
- https://huggingface.co/docs/trl/sft_trainer
- https://github.com/unslothai/unsloth
- https://github.com/arcee-ai/mergekit
