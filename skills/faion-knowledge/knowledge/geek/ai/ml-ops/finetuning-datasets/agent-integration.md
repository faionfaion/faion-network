# Agent Integration — Fine-tuning Datasets (Datasets, Training & Deployment)

## When to use
- Preparing a domain-specific dataset for LoRA/QLoRA or OpenAI fine-tuning
- Evaluating a fine-tuned model against baselines using standard benchmarks
- Deploying a fine-tuned model to a local (Ollama) or production (vLLM/TGI) inference server
- Estimating GPU cost and training duration before committing cloud spend

## When NOT to use
- When you have fewer than 100 cleaned, verified examples — dataset preparation overhead is not justified
- When the deployment target does not support GGUF or HF-format models (some cloud platforms restrict to specific providers)
- When benchmark accuracy on MMLU/HellaSwag is the primary goal — fine-tuning on task-specific data often hurts general benchmarks

## Where it fails / limitations
- Deduplication by exact (instruction, output) key pair misses semantic duplicates — a model trained on near-duplicate data overfits silently
- `len(output) < 10` filters remove valid short-answer examples (yes/no, single-word answers) — tune thresholds per task
- Validation split must be random-stratified; sequential splitting leaks temporal distribution bias
- vLLM requires a merged model (not a PEFT adapter) — agents that skip the merge step produce a broken deployment
- GPU cost estimates from `estimate_training_time()` assume constant throughput; real throughput varies ±30% by sequence length distribution
- TGI Docker image versions lag behind HF model releases — new model families may require a specific image tag

## Agentic workflow
Dataset preparation is well-suited for agent automation: an agent reads raw source data, applies cleaning rules, formats to the target schema (Alpaca/ShareGPT/OpenAI), deduplicates, and writes validated JSONL. Deployment steps (GGUF export, Ollama model creation, vLLM server launch) are scripted commands that an agent can orchestrate via shell calls. Human checkpoints are required before: (1) uploading training data to a provider, (2) running evaluation benchmarks, (3) serving the model in production.

### Recommended subagents
- `faion-sdd-execution` — automate dataset cleaning pipeline: read raw data → deduplicate → filter → format → validate → write JSONL
- Custom eval agent — run `lm-eval` after training and produce a comparison table vs. base model

### Prompt pattern
```
Clean the following dataset. Remove duplicates (by instruction+output pair), filter outputs
shorter than 20 chars or longer than 2000 chars, and remove any item containing PII
(email addresses, phone numbers, full names). Return cleaned JSON array.
Input: {raw_json}
```

```
Format these Q&A pairs as ShareGPT-format JSON for LLaMA-Factory fine-tuning.
Each pair: {"conversations": [{"from": "human", "value": Q}, {"from": "gpt", "value": A}]}
Input pairs: {qa_list}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `lm-eval` | Run standard benchmarks (MMLU, HellaSwag, HumanEval) | `pip install lm-eval` · github.com/EleutherAI/lm-evaluation-harness |
| `datasets` | HF library for loading, processing, splitting datasets | `pip install datasets` · huggingface.co/docs/datasets |
| `ollama` | Local model serving from GGUF | `curl -fsSL https://ollama.com/install.sh \| sh` · ollama.ai |
| `vllm` | Production OpenAI-compatible inference server | `pip install vllm` · docs.vllm.ai |
| `docker` | Run TGI inference container | docker.com · ghcr.io/huggingface/text-generation-inference |
| `unsloth` | Export to GGUF directly from training | `pip install unsloth` · github.com/unslothai/unsloth |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Hugging Face Hub | SaaS/OSS | Yes — SDK + REST | Dataset hosting, model registry, AutoTrain |
| Weights & Biases | SaaS | Yes — REST API | Experiment tracking, loss curves, eval scores |
| RunPod | SaaS | Partial | GPU rental for training/inference; no managed eval |
| Lambda Labs | SaaS | Partial | Cheaper than AWS for A100/H100; SSH access only |
| Vast.ai | SaaS | Partial — REST API | Auction-based GPU; cheapest but variable reliability |
| Ollama | OSS | Yes — REST API on :11434 | Local serving; agent can call `/api/generate` |
| vLLM | OSS | Yes — OpenAI-compatible API | Production serving; best throughput for batched inference |

## Templates & scripts
See `templates.md` for the data cleaning pipeline and deployment scripts.

Inline: split dataset into train/val with stratification proxy (shuffle + ratio):
```python
import json, random

def split_dataset(path: str, val_ratio: float = 0.1, seed: int = 42) -> tuple:
    with open(path) as f:
        data = json.load(f)
    random.seed(seed)
    random.shuffle(data)
    split = int(len(data) * val_ratio)
    return data[split:], data[:split]  # train, val

train, val = split_dataset("cleaned.json", val_ratio=0.1)
with open("train.json", "w") as f: json.dump(train, f)
with open("val.json", "w") as f: json.dump(val, f)
print(f"Train: {len(train)}, Val: {len(val)}")
```

## Best practices
- Minimum viable dataset: 100 examples for narrow task, 500+ for general instruction following, 1000+ for style/persona transfer
- Quality > quantity: 200 expertly curated examples outperform 2000 noisy ones consistently
- Format consistency is the single highest-impact factor — use the same system prompt across all examples or omit it entirely
- For ShareGPT multi-turn data: include at least 3 turns per conversation; single-turn ShareGPT is equivalent to Alpaca
- Use q4_k_m GGUF for Ollama (good balance); q8_0 only if perplexity difference is measurable on your eval set
- Run `lm_eval` on MMLU before and after fine-tuning to detect catastrophic forgetting early
- TGI requires `--max-input-length` and `--max-total-tokens` tuned to your data distribution — default values cause OOM on long contexts

## AI-agent gotchas
- Dataset generation by LLM introduces systematic bias (same vocabulary, similar sentence structures) — validate with diversity metrics (unique bigram ratio)
- An agent writing GGUF files to `/tmp` on a cloud instance will lose them on pod termination — always specify a persistent volume path
- vLLM `--tensor-parallel-size` must match available GPU count exactly; wrong value silently hangs at startup
- `lm-eval` benchmarks can take 2-8 hours on a 7B model — agents must dispatch async and await completion signal, not poll in a tight loop
- Perplexity on the training set is not a valid eval metric — always compute on held-out data from the same distribution

## References
- https://github.com/EleutherAI/lm-evaluation-harness
- https://huggingface.co/docs/datasets
- https://docs.vllm.ai/en/latest/
- https://ollama.ai/docs
- https://github.com/huggingface/text-generation-inference
- https://arxiv.org/abs/2305.14314 (QLoRA — memory savings tables)
- https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset
