# Fine-tuning (LoRA)

## Summary

LoRA (Low-Rank Adaptation) fine-tuning methodology using PEFT + TRL: freezing base model weights and injecting small trainable matrices (rank 8-64) into attention layers, reducing trainable parameters by 100-250x. Covers QLoRA (4-bit quantization), multiple-adapter management, hyperparameter search, and the `LoRATrainingPipeline` production class.

## Why

LoRA enables fine-tuning on consumer GPUs (8-24GB VRAM) where full fine-tuning requires 80GB+. The adapter approach preserves general capabilities (frozen base) while specializing behavior for the target task. Multiple adapters can share one base model and be switched at runtime — critical for multi-tenant or multi-task production deployments.

## When To Use

- Consumer GPU available (8-24GB VRAM) and full fine-tuning is not feasible
- Need to maintain multiple task-specific adapters on one base model without reloading weights
- Quick iteration experiments where training must complete in hours, not days
- Adapting model style/behavior without degrading general capabilities
- Production scenario where a specialized smaller model is cheaper to serve than a large prompted model

## When NOT To Use

- Task requires injecting new factual knowledge — LoRA adapters do not reliably encode facts; use RAG
- Dataset is smaller than 50 examples — adapter overfits immediately; use few-shot prompting
- Target inference server does not support on-the-fly adapter loading — merge the adapter first
- Real-time latency requirement below 100ms — adapter overhead adds ~5-10ms; merging eliminates this
- Multiple simultaneous LoRA experiments on the same GPU — they will OOM; serialize jobs

## Content

| File | What's inside |
|------|---------------|
| `content/01-lora-config.xml` | `LoraConfig` parameters, rank selection guide, target_modules by model family, trainable-param check |
| `content/02-qlora.xml` | `BitsAndBytesConfig`, 4-bit QLoRA memory savings table, `prepare_model_for_kbit_training` ordering |
| `content/03-training-pipeline.xml` | `SFTTrainer` pattern, `LoRATrainingPipeline` class, multiple-adapter switching, merge-and-unload |

## Templates

| File | Purpose |
|------|---------|
| `templates/lora-pipeline.py` | `LoRATrainingPipeline` class with QLoRA, SFTTrainer, and merge-and-unload (~80 lines) |
| `templates/check-trainable-params.py` | Verify trainable parameter count after applying LoRA; raises if 0 (~10 lines) |
| `templates/lora-config-prompt.txt` | Prompt for selecting rank, target_modules, and learning rate given model family and task |
