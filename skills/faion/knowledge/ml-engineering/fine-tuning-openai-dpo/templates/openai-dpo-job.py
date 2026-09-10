"""
purpose: Job-launch script with beta + epochs.
consumes: see AGENTS.md ## Prerequisites
produces: config
depends-on: content/02-output-contract.xml schema for fine-tuning-openai-dpo
token-budget-impact: ≤500 tokens to fill
"""
# Usage:
#   export OPENAI_API_KEY=...
#   python openai-dpo-job.py --sft-base ft:gpt-4o-mini-2024-07-18:org::sft_v1 \
#       --pairs data/pairs-train.jsonl --pairs-val data/pairs-val.jsonl \
#       --kappa 0.72 --strength moderate --suffix dpo_v1
# Uploads the pair files, launches a DPO job, polls, prints the DPO output-contract
# JSON with preference_eval_gate_passed=false (the eval methodology flips it).
# Requires: pip install openai>=1.0

from __future__ import annotations

import argparse
import json
import sys
import time

from openai import OpenAI

# r4-beta-default: 0.1 default; 0.05 for subtle tone/style, 0.3 for safety-grade shifts.
BETA_BY_STRENGTH = {"subtle": 0.05, "moderate": 0.1, "strong": 0.3}
TERMINAL = {"succeeded", "failed", "cancelled"}


def count_pairs(path: str) -> int:
    """Counts well-formed DPO rows: input.messages + preferred_output + non_preferred_output."""
    n = 0
    with open(path, encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            row = json.loads(line)
            if not {"input", "preferred_output", "non_preferred_output"} <= row.keys():
                raise SystemExit(f"{path}:{line_no}: not a DPO triple; run data-prep with --rejected-col")
            n += 1
    return n


def poll(client: OpenAI, job_id: str) -> dict:
    """Exponential backoff 5s -> 60s cap (same pattern as the SFT launcher)."""
    delay = 5.0
    while True:
        job = client.fine_tuning.jobs.retrieve(job_id)
        print(f"{job.id} {job.status}", file=sys.stderr)
        if job.status in TERMINAL:
            return job.model_dump()
        time.sleep(delay)
        delay = min(delay * 2, 60.0)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sft-base", required=True, help="ft:... model ID from fine-tuning-openai-sft")
    ap.add_argument("--pairs", required=True, help="training preference-pair JSONL")
    ap.add_argument("--pairs-val", required=True, help="held-out preference pairs for OpenAI eval traces")
    ap.add_argument("--kappa", type=float, required=True, help="inter-rater agreement on the 100-pair audit")
    ap.add_argument("--strength", choices=sorted(BETA_BY_STRENGTH), default="moderate")
    ap.add_argument("--beta", type=float, help="override strength mapping; must stay in [0.01, 0.5]")
    ap.add_argument("--epochs", type=int, default=2, help="1-5; DPO overfits fast")
    ap.add_argument("--suffix", required=True)
    args = ap.parse_args()

    # r1-sft-base-required: OpenAI's dpo method expects a fine-tuned base, not the foundation model.
    if not args.sft_base.startswith("ft:"):
        ap.error(f"{args.sft_base!r} is not an SFT fine-tune; train SFT first")
    # r3-inter-rater-agreement: below 0.6 kappa the pairs are noise.
    if args.kappa < 0.6:
        ap.error(f"kappa {args.kappa} < 0.6; fix labelling before spending on DPO")
    # r2-pair-floor: 500 minimum, 2000 for production grade.
    pair_count = count_pairs(args.pairs)
    if pair_count < 500:
        ap.error(f"{pair_count} pairs < 500 floor; collect more pairs")
    if pair_count < 2000:
        print(f"warning: {pair_count} pairs is below the 2000 production-grade mark", file=sys.stderr)
    beta = args.beta if args.beta is not None else BETA_BY_STRENGTH[args.strength]
    if not 0.01 <= beta <= 0.5 or not 1 <= args.epochs <= 5:
        ap.error("beta must be in [0.01, 0.5] and epochs in [1, 5]")

    client = OpenAI()  # reads OPENAI_API_KEY
    with open(args.pairs, "rb") as fh:
        train_file = client.files.create(file=fh, purpose="fine-tune")
    with open(args.pairs_val, "rb") as fh:
        val_file = client.files.create(file=fh, purpose="fine-tune")

    job = client.fine_tuning.jobs.create(
        model=args.sft_base,
        training_file=train_file.id,
        validation_file=val_file.id,
        suffix=args.suffix,
        method={"type": "dpo", "dpo": {"hyperparameters": {"beta": beta, "n_epochs": args.epochs}}},
    )
    print(f"launched {job.id}: base={args.sft_base} beta={beta} epochs={args.epochs}", file=sys.stderr)

    final = poll(client, job.id)
    if final["status"] != "succeeded":
        print(json.dumps({"job_id": final["id"], "status": final["status"], "error": final.get("error")}))
        return 1
    # r5-preference-eval-gate: the gate stays false here; only a >0.55 preference_rate
    # on held-out pairs (fine-tuning-openai-eval) may set it true before deployment.
    print(json.dumps({
        "sft_base_model_id": args.sft_base, "pair_count": pair_count, "beta": beta,
        "epochs": args.epochs, "inter_rater_agreement": args.kappa,
        "preference_eval_gate_passed": False,
        "dpo_model_id": final["fine_tuned_model"], "job_id": final["id"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
