---
name: lora-basics-dataset-prep
description: Prepare 200-2000 JSONL training examples, train a LoRA adapter on Llama 3.1 8B via axolotl or TRL, and evaluate on a held-out 10% split.
tier: geek
group: fine-tuning
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a validated JSONL dataset of 200–2000 instruction/input/output triples, a trained LoRA adapter (rank=16, alpha=32) on Llama 3.1 8B, and a held-out eval report showing ROUGE-L and perplexity on a 10% test split — all for under $30 on Modal, RunPod, or Lambda Labs.

## Prerequisites

- Python 3.11+ with `uv` or `pip` available.
- A Hugging Face account with an API token (`HF_TOKEN`) that has read access to `meta-llama/Meta-Llama-3.1-8B-Instruct` (gated — accept license first at hf.co/meta-llama).
- A GPU cloud account on one of: Modal (free $30 credit), RunPod ($10+ credit), or Lambda Labs (pay-as-you-go). A100 40 GB or H100 80 GB recommended.
- Familiarity with JSONL format and basic Python.
- Optional: a prior playbook on `rag-chunking-benchmark` if your dataset comes from a retrieval pipeline.

## Steps

### 1. Audit and shape raw source material

Collect your raw source: customer support tickets, domain Q&A, internal docs, scraped forum posts. You need at least 220 examples (200 train + 20 test floor).

```python
# audit_sources.py
import json, pathlib, random

sources = pathlib.Path("raw/").glob("*.jsonl")
rows = []
for src in sources:
    for line in src.read_text().splitlines():
        obj = json.loads(line)
        rows.append(obj)

random.seed(42)
random.shuffle(rows)
print(f"Total raw rows: {len(rows)}")
```

Target ratio: 1 domain concept per ~5 examples. If you have 10 concepts, aim for 50 examples each = 500 total.

### 2. Convert to instruction/input/output JSONL

The standard format for axolotl `alpaca` template and TRL `SFTTrainer`:

```python
# build_dataset.py
import json, pathlib, random

RAW_FILE = pathlib.Path("raw/my_domain_qa.jsonl")
OUT_TRAIN = pathlib.Path("data/train.jsonl")
OUT_TEST  = pathlib.Path("data/test.jsonl")
TEST_RATIO = 0.10

rows = [json.loads(l) for l in RAW_FILE.read_text().splitlines() if l.strip()]

random.seed(42)
random.shuffle(rows)

split = max(1, int(len(rows) * TEST_RATIO))
test_rows, train_rows = rows[:split], rows[split:]

def to_alpaca(r: dict) -> dict:
    """Map your raw keys to alpaca fields."""
    return {
        "instruction": r["question"],           # task description
        "input":       r.get("context", ""),    # optional extra context
        "output":      r["answer"],              # expected model response
    }

OUT_TRAIN.parent.mkdir(parents=True, exist_ok=True)
OUT_TRAIN.write_text("\n".join(json.dumps(to_alpaca(r)) for r in train_rows))
OUT_TEST.write_text("\n".join(json.dumps(to_alpaca(r)) for r in test_rows))

print(f"Train: {len(train_rows)}  Test: {len(test_rows)}")
```

Run: `python build_dataset.py` — confirm train/test counts.

### 3. Validate dataset quality

Check token length distribution before training; examples >2048 tokens get silently truncated, which corrupts long-output tasks.

```python
# validate_dataset.py
from transformers import AutoTokenizer
import json, pathlib, statistics

tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Meta-Llama-3.1-8B-Instruct",
    token="<your-HF_TOKEN>",
)

lengths = []
for line in pathlib.Path("data/train.jsonl").read_text().splitlines():
    r = json.loads(line)
    text = r["instruction"] + r["input"] + r["output"]
    lengths.append(len(tokenizer.encode(text)))

p50, p95, p99 = (
    statistics.median(lengths),
    sorted(lengths)[int(len(lengths) * 0.95)],
    sorted(lengths)[int(len(lengths) * 0.99)],
)
too_long = sum(1 for l in lengths if l > 2048)
print(f"p50={p50}  p95={p95}  p99={p99}  over_2048={too_long}/{len(lengths)}")
```

If `over_2048` > 5% of examples, trim `output` fields or split examples. Aim for p95 < 1800 tokens to leave room for the instruction template.

### 4. Write the axolotl config

Save as `lora_llama31_8b.yml`:

```yaml
# lora_llama31_8b.yml  — axolotl LoRA config for Llama 3.1 8B
base_model: meta-llama/Meta-Llama-3.1-8B-Instruct
model_type: LlamaForCausalLM
tokenizer_type: AutoTokenizer

load_in_8bit: false
load_in_4bit: true          # QLoRA — cuts VRAM to ~14 GB on A100
strict: false

datasets:
  - path: data/train.jsonl
    type: alpaca

dataset_prepared_path: null
val_set_size: 0.0           # we hold out test.jsonl separately

output_dir: ./lora-out

sequence_len: 2048
sample_packing: false
pad_to_sequence_len: false

adapter: lora
lora_model_dir: null
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
lora_target_linear: true    # targets all linear layers automatically

gradient_accumulation_steps: 4
micro_batch_size: 2
num_epochs: 3
optimizer: adamw_bnb_8bit
lr_scheduler: cosine
learning_rate: 2e-4

train_on_inputs: false
group_by_length: false
bf16: true
fp16: false
tf32: false

gradient_checkpointing: true
logging_steps: 10
flash_attention: true       # requires flash-attn; skip on T4

warmup_steps: 50
saves_per_epoch: 1
save_total_limit: 2

wandb_project: lora-llama31-8b
wandb_run_id: run-001
```

### 5. Alternatively: use HuggingFace TRL SFTTrainer

If you prefer TRL over axolotl (simpler dependency tree, no YAML):

```python
# train_trl.py
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM
from peft import LoraConfig, get_peft_model
from datasets import load_dataset
import torch

MODEL_ID = "meta-llama/Meta-Llama-3.1-8B-Instruct"
HF_TOKEN = "<your-HF_TOKEN>"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, token=HF_TOKEN)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    token=HF_TOKEN,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    load_in_4bit=True,
)

lora_cfg = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_cfg)
model.print_trainable_parameters()

dataset = load_dataset("json", data_files={"train": "data/train.jsonl"})

def format_prompt(row):
    parts = [f"### Instruction:\n{row['instruction']}"]
    if row.get("input"):
        parts.append(f"\n### Input:\n{row['input']}")
    parts.append(f"\n### Response:\n{row['output']}")
    return {"text": "\n".join(parts)}

dataset = dataset.map(format_prompt)

training_args = TrainingArguments(
    output_dir="./lora-trl-out",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    warmup_steps=50,
    learning_rate=2e-4,
    bf16=True,
    logging_steps=10,
    save_strategy="epoch",
    report_to="wandb",
    run_name="lora-llama31-8b-trl",
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    dataset_text_field="text",
    max_seq_length=2048,
    tokenizer=tokenizer,
)
trainer.train()
trainer.save_model("./lora-trl-out/final")
```

### 6. Launch training on Modal

```python
# modal_train.py
import modal

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "axolotl[flash-attn,deepspeed]",
        "wandb",
        "huggingface_hub",
    )
)

app = modal.App("lora-llama31-training", image=image)

@app.function(
    gpu="A100-40GB",
    timeout=7200,
    secrets=[
        modal.Secret.from_name("huggingface-token"),
        modal.Secret.from_name("wandb-token"),
    ],
    volumes={"/data": modal.Volume.from_name("lora-dataset", create_if_missing=True)},
)
def train():
    import subprocess
    subprocess.run(
        ["accelerate", "launch", "-m", "axolotl.cli.train", "lora_llama31_8b.yml"],
        check=True,
    )

@app.local_entrypoint()
def main():
    train.remote()
```

Push dataset to the Modal volume first:
```bash
modal volume put lora-dataset data/ /data/
modal run modal_train.py
```

Cost: ~A100 40 GB at $2.80/hr × ~3 hr = ~$8.40 for 500 examples, 3 epochs.

For RunPod: spin up an A100 pod → SSH → `git clone` your repo → `pip install axolotl[flash-attn]` → `accelerate launch -m axolotl.cli.train lora_llama31_8b.yml`.

### 7. Evaluate on the held-out test split

```python
# eval_lora.py
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch, json, pathlib
from rouge_score import rouge_scorer

BASE_MODEL  = "meta-llama/Meta-Llama-3.1-8B-Instruct"
ADAPTER_DIR = "./lora-out"          # or "./lora-trl-out/final"
HF_TOKEN    = "<your-HF_TOKEN>"
TEST_FILE   = pathlib.Path("data/test.jsonl")

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, token=HF_TOKEN)
base = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL, token=HF_TOKEN,
    torch_dtype=torch.bfloat16, device_map="auto",
)
model = PeftModel.from_pretrained(base, ADAPTER_DIR)
model.eval()

scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
scores = []

for line in TEST_FILE.read_text().splitlines():
    row = json.loads(line)
    prompt = f"### Instruction:\n{row['instruction']}\n### Response:\n"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=256, do_sample=False)
    pred = tokenizer.decode(out[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    s = scorer.score(row["output"], pred)["rougeL"].fmeasure
    scores.append(s)

print(f"ROUGE-L  mean={sum(scores)/len(scores):.3f}  "
      f"min={min(scores):.3f}  max={max(scores):.3f}  n={len(scores)}")
```

Baseline acceptance: ROUGE-L mean > 0.30 for extractive tasks; > 0.18 for generative. If below, increase epochs or dataset size.

## Verify

After training completes, run:

```bash
python eval_lora.py
```

Expected output (green bar):

```
ROUGE-L  mean=0.412  min=0.089  max=0.891  n=22
```

For a quick sanity check without eval, load the adapter and run one inference:

```python
prompt = "### Instruction:\nExplain RAG in one sentence.\n### Response:\n"
# ... (same load pattern as eval_lora.py)
# Output must be coherent and domain-relevant, not garbled tokens.
```

Also verify `lora-out/` (or `lora-trl-out/final/`) contains `adapter_config.json` and at least one `adapter_model.safetensors` shard.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `CUDA out of memory` during training | Batch size too large or sequence_len too long | Set `micro_batch_size: 1`, `gradient_accumulation_steps: 8`, reduce `sequence_len` to 1024 |
| `ValueError: Tokenizer class ... does not exist` | axolotl version pinned to old transformers | `pip install -U transformers` inside the container/env |
| ROUGE-L mean < 0.10 after 3 epochs | Dataset too small or label noise | Add more examples; run `validate_dataset.py` to check for empty `output` fields |
| `gated repo` 403 on model download | HF token not accepted Llama license | Visit hf.co/meta-llama/Meta-Llama-3.1-8B-Instruct, click Accept, regenerate token |
| Training loss oscillates without decreasing | Learning rate too high or no warmup | Reduce `learning_rate` to `5e-5`, increase `warmup_steps` to 100 |
| `adapter_config.json` missing in output dir | Training crashed mid-epoch | Check GPU logs; re-run from last checkpoint by setting `resume_from_checkpoint: ./lora-out/checkpoint-last` in YAML |
| Modal volume empty after upload | `modal volume put` path syntax error | Use `modal volume put lora-dataset ./data /data` (no trailing slash on destination) |

## Next

- `model-monitoring-drift` — log adapter inference calls to Postgres and run daily ROUGE drift checks to detect when the fine-tuned model degrades on new production queries.
- Merge adapter weights into base model for faster inference: `peft.merge_and_unload()` → push to Hugging Face Hub → serve with `vllm`.
- Iterate dataset with active learning: collect low-confidence outputs from production → label → add to `train.jsonl` → retrain.

## References

- [knowledge/geek/ai/ml-ops/fine-tuning-lora](../../../knowledge/geek/ai/ml-ops/fine-tuning-lora) — provides rank/alpha selection guidance and target-module patterns for Llama architecture; backs Steps 4–5 config values (r=16, alpha=32, linear targets).
- [knowledge/geek/ai/ml-ops/finetuning-datasets](../../../knowledge/geek/ai/ml-ops/finetuning-datasets) — defines alpaca JSONL schema and train/test split rationale; backs Steps 2–3 data pipeline and the 10% held-out split strategy.
- [knowledge/geek/ai/ml-ops/lora-qlora](../../../knowledge/geek/ai/ml-ops/lora-qlora) — explains QLoRA 4-bit quantisation trade-offs and memory footprint on A100; backs the `load_in_4bit: true` choice in Step 4 and the cost estimate in Step 6.
- [knowledge/geek/ai/ml-ops/evaluation-framework](../../../knowledge/geek/ai/ml-ops/evaluation-framework) — specifies ROUGE-L as the primary metric for instruction-following tasks and defines acceptance thresholds; backs the eval script and pass/fail criteria in Step 7.
