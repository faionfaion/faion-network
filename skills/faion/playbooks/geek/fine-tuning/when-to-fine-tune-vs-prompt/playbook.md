---
name: when-to-fine-tune-vs-prompt
description: Decide whether to fine-tune an LLM or stay on prompting, using a structured decision tree and a cost break-even calculator.
tier: geek
group: fine-tuning
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a documented decision — prompt-only, few-shot, or fine-tuned model — backed by a break-even calculation. You will know the token-volume threshold at which a fine-tuned model becomes cheaper than a frontier model, and you will have a Python script that computes that threshold for your actual pricing numbers.

## Prerequisites

- OpenAI or Anthropic API access with billing enabled.
- Python 3.11+ installed locally; `pip install anthropic openai` available.
- A representative sample of ≥50 input/output pairs from your production workload (needed for dataset quality evaluation in Step 3).
- Familiarity with few-shot prompting — if not, complete `prompt-techniques` first.
- A rough sense of monthly inference volume (requests/month or tokens/month) for your use case.

## Steps

1. **Run a prompt-baseline evaluation before touching fine-tuning tooling.**

   Write 20 representative input/output pairs as a `golden-set.jsonl` file. Run `claude-sonnet-4-6` (or `gpt-4o-mini` if OpenAI-only) with zero-shot and 5-shot prompts, score with your task metric (exact-match, ROUGE-L, LLM-as-judge). Record baseline F1 or accuracy.

   ```python
   import anthropic, json, pathlib

   client = anthropic.Anthropic()
   golden = [json.loads(l) for l in pathlib.Path("golden-set.jsonl").read_text().splitlines()]

   def score_zero_shot(item: dict) -> str:
       msg = client.messages.create(
           model="claude-sonnet-4-6",
           max_tokens=256,
           messages=[{"role": "user", "content": item["input"]}],
       )
       return msg.content[0].text.strip()

   results = [(g["expected"], score_zero_shot(g)) for g in golden]
   accuracy = sum(e == p for e, p in results) / len(results)
   print(f"Zero-shot accuracy: {accuracy:.1%}")
   ```

2. **Add few-shot examples and re-evaluate.**

   Select 5–10 diverse examples from the golden set as in-context shots. Re-run the same 20-item evaluation. If accuracy improves to within 5 percentage points of your target, stop here — prompting is sufficient.

   ```python
   FEW_SHOT = [
       {"role": "user", "content": golden[0]["input"]},
       {"role": "assistant", "content": golden[0]["expected"]},
       # ... repeat for 4 more examples
   ]

   def score_few_shot(item: dict) -> str:
       msg = client.messages.create(
           model="claude-sonnet-4-6",
           max_tokens=256,
           messages=FEW_SHOT + [{"role": "user", "content": item["input"]}],
       )
       return msg.content[0].text.strip()
   ```

3. **Apply the fine-tuning decision checklist.**

   Fine-tuning is worth pursuing only if ≥1 of these three gates is triggered:

   | Gate | Trigger condition | Signal to look for |
   |------|-------------------|--------------------|
   | Quality plateau | Few-shot accuracy still ≥5 pp below target after ≥3 prompt iterations | Task requires deep domain style or implicit formatting rules impossible to express in instructions |
   | Latency-critical | p95 response latency > your SLA threshold | Each extra few-shot token adds ~2–4 ms; fine-tuned model needs no shots |
   | Cost-critical + high volume | Monthly inference cost on frontier model > $500 AND volume > break-even (see Step 4) | Break-even typically 100M–500M tokens/month for OpenAI; lower for self-hosted LoRA |

   If no gate fires → stay on prompting. Document the decision in your `LLM_DECISIONS.md`.

4. **Calculate the fine-tuning break-even point.**

   Training cost is a one-time fee (or repeated quarterly for data drift). Per-token cost is cheaper on fine-tuned models but training must amortize.

   Concrete example: `gpt-4o-mini` fine-tuning costs ~$0.003/1K training tokens (one-time ~$500 for 1M tokens) and inference drops from $0.60/1M output tokens (base `gpt-4o`) to $0.40/1M (fine-tuned `gpt-4o-mini`). Against `claude-sonnet-4-6` at $3.00/1M output tokens, the saving per million tokens is $2.60, so break-even = $500 / $0.0026 = ~192M output tokens total.

   Run the calculator for your actual numbers:

   ```python
   def fine_tune_break_even(
       training_cost_usd: float,        # one-time training bill
       frontier_cost_per_1m: float,     # e.g. 3.00 for claude-sonnet-4-6 output
       finetuned_cost_per_1m: float,    # e.g. 0.40 for gpt-4o-mini fine-tuned output
       monthly_output_tokens: int,      # tokens/month in production
   ) -> dict:
       saving_per_1m = frontier_cost_per_1m - finetuned_cost_per_1m
       if saving_per_1m <= 0:
           return {"verdict": "no_saving", "break_even_tokens": None}
       break_even_tokens = (training_cost_usd / saving_per_1m) * 1_000_000
       months_to_break_even = break_even_tokens / monthly_output_tokens
       monthly_saving = (monthly_output_tokens / 1_000_000) * saving_per_1m
       return {
           "verdict": "fine_tune" if months_to_break_even < 6 else "marginal",
           "break_even_tokens": int(break_even_tokens),
           "months_to_break_even": round(months_to_break_even, 1),
           "monthly_saving_usd": round(monthly_saving, 2),
       }

   # Real scenario: indie AI product, 300M output tokens/month
   print(fine_tune_break_even(
       training_cost_usd=500,
       frontier_cost_per_1m=3.00,    # claude-sonnet-4-6
       finetuned_cost_per_1m=0.40,   # gpt-4o-mini fine-tuned
       monthly_output_tokens=300_000_000,
   ))
   # → {'verdict': 'fine_tune', 'break_even_tokens': 192307692,
   #    'months_to_break_even': 0.6, 'monthly_saving_usd': 780.0}
   ```

   At 300M output tokens/month the training cost pays back in under 1 month, saving $780/month thereafter.

5. **Prepare and validate your fine-tuning dataset.**

   Fine-tuning needs at least 100 examples (OpenAI recommends 200+). Format as JSONL with `messages` arrays. Validate distribution: check that all output categories appear in the training split.

   ```python
   import json, pathlib, collections

   def validate_ft_dataset(path: str) -> None:
       rows = [json.loads(l) for l in pathlib.Path(path).read_text().splitlines() if l.strip()]
       assert len(rows) >= 100, f"Too few examples: {len(rows)}"
       lengths = [sum(len(m["content"]) for m in r["messages"]) for r in rows]
       print(f"Examples: {len(rows)}, avg chars: {sum(lengths)/len(lengths):.0f}")
       # Check for malformed rows
       for i, row in enumerate(rows):
           assert "messages" in row, f"Row {i} missing 'messages'"
           roles = [m["role"] for m in row["messages"]]
           assert roles[-1] == "assistant", f"Row {i} last role must be 'assistant'"

   validate_ft_dataset("ft-dataset.jsonl")
   ```

6. **Run fine-tuning job (OpenAI example) or equivalent.**

   ```python
   import openai, pathlib

   client_oai = openai.OpenAI()

   upload = client_oai.files.create(
       file=pathlib.Path("ft-dataset.jsonl").open("rb"),
       purpose="fine-tune",
   )

   job = client_oai.fine_tuning.jobs.create(
       training_file=upload.id,
       model="gpt-4o-mini-2024-07-18",
       hyperparameters={"n_epochs": 3},
   )
   print(f"Job ID: {job.id} — Status: {job.status}")
   # Poll: client_oai.fine_tuning.jobs.retrieve(job.id)
   ```

   For Anthropic fine-tuning (when available via API), follow the same pattern using `anthropic.beta.models.fine_tune` with `claude-haiku-4-5-20251001` as the base.

7. **Evaluate the fine-tuned model against your golden set.**

   Re-run Step 1's evaluation loop substituting `model=job.fine_tuned_model` (OpenAI) or the returned model ID (Anthropic). Compare quality, latency (p50/p95), and cost metrics in a 3-column table.

8. **Document the decision and set a drift review date.**

   Create or update `LLM_DECISIONS.md` in your repo:

   ```markdown
   ## 2026-05-02 — customer-intent-classifier

   Decision: fine-tune gpt-4o-mini (ft:gpt-4o-mini-2024-07-18:org::AbcXYZ)
   Reason: 63% → 91% accuracy (gate: quality plateau), break-even 0.6 months
   Review date: 2026-08-02 (data drift check, re-run golden-set eval)
   ```

## Verify

Run the break-even calculator from Step 4 with your production numbers. Confirm `verdict` is either `fine_tune` (months_to_break_even < 6) or `marginal`/`no_saving` (stay on prompting). Then run the golden-set evaluation from Step 1 against the fine-tuned model — accuracy must meet or exceed your target threshold. If both checks pass, the decision is validated.

```bash
python3 -c "
from playbook_utils import fine_tune_break_even
result = fine_tune_break_even(500, 3.00, 0.40, 300_000_000)
assert result['verdict'] == 'fine_tune', f'Expected fine_tune, got {result}'
print('Break-even check passed:', result)
"
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Fine-tuned model quality is worse than few-shot baseline | Training data too small or poorly filtered | Increase to 300+ examples; audit for mislabeled outputs with LLM-as-judge; add 10% held-out validation split |
| Training job fails with `invalid_request_error` | JSONL rows missing required `messages` key or last message role is not `assistant` | Run `validate_ft_dataset()` from Step 5; fix malformed rows and re-upload |
| Break-even > 18 months | Monthly token volume is too low | Stay on prompting; revisit when volume grows or training costs drop |
| Latency of fine-tuned model is not lower than baseline | Fine-tuned model is same size with shorter prompt, but inference hardware is shared | Benchmark at peak traffic; dedicated deployment (e.g. OpenAI dedicated capacity) eliminates shared-queue jitter |
| Data drift: accuracy degrades 2 months post-launch | Production inputs shifted from training distribution | Collect 200+ new examples from recent prod logs, re-run fine-tune job quarterly |
| `months_to_break_even` is 0.1 — suspiciously low | Input `monthly_output_tokens` uses total tokens not output-only | Re-check: only output (completion) tokens cost the differential rate; input tokens are cheaper and differ less |

## Next

- `fine-tuning-openai-production` methodology in `knowledge/geek/ai/ml-ops/` — production checklist for monitoring, rollback, and A/B gating a fine-tuned model.
- `llm-cost-basics` in `knowledge/geek/ai/ml-ops/` — full token cost model including prompt caching, batching, and tiered pricing to refine the break-even calculation.
- `evaluation-framework` in `knowledge/geek/ai/ml-ops/` — build an automated regression suite that gates fine-tune deploys on quality metrics.

## References

- [knowledge/geek/ai/ml-ops/fine-tuning-openai-production](../../../knowledge/geek/ai/ml-ops/fine-tuning-openai-production) — production deployment checklist (A/B rollout, rollback triggers, drift monitoring) that this playbook's decision feeds directly into once fine-tune verdict is confirmed.
- [knowledge/geek/ai/ml-ops/llm-cost-basics](../../../knowledge/geek/ai/ml-ops/llm-cost-basics) — token pricing model underpinning the break-even formula in Step 4; validates the frontier vs. fine-tuned per-token differential used in the calculator.
- [knowledge/geek/ai/llm-integration/prompt-techniques](../../../knowledge/geek/ai/llm-integration/prompt-techniques) — few-shot construction patterns referenced in Steps 1–2; the baseline quality ceiling from this methodology determines whether the quality-plateau gate in Step 3 fires.
