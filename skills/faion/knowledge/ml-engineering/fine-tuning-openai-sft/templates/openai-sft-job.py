"""
purpose: Job-launch + polling script.
consumes: see AGENTS.md ## Prerequisites
produces: config
depends-on: content/02-output-contract.xml schema for fine-tuning-openai-sft
token-budget-impact: ≤500 tokens to fill
"""
# Usage:
#   export OPENAI_API_KEY=...
#   python openai-sft-job.py --training-file file-abc123 --validation-file file-def456 \
#       --base gpt-4o-mini-2024-07-18 --train-count 3346 --suffix tone_v1 \
#       --registry infra/model-id-registry.yaml
# Prints the SFT output-contract JSON on success; exits 1 if the job fails.
# Requires: pip install openai>=1.0 pyyaml

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
from pathlib import Path

import yaml
from openai import OpenAI

BASES = {"gpt-4o-mini-2024-07-18", "gpt-4o-2024-08-06", "gpt-4.1-2025-04-14",
         "gpt-4.1-mini-2025-04-14", "gpt-4.1-nano-2025-04-14"}
TERMINAL = {"succeeded", "failed", "cancelled"}


def epochs_for(train_count: int) -> int:
    """r3-epochs-by-size: 5 below 300 rows, 3 default, 2 above 10k; never above 8."""
    if train_count < 300:
        return 5
    return 2 if train_count > 10_000 else 3


def poll(client: OpenAI, job_id: str) -> dict:
    """r5-poll-async: exponential backoff 5s -> 60s cap; surfaces new events as they arrive."""
    delay, seen = 5.0, set()
    while True:
        job = client.fine_tuning.jobs.retrieve(job_id)
        for ev in reversed(client.fine_tuning.jobs.list_events(job_id, limit=20).data):
            if ev.id not in seen:
                seen.add(ev.id)
                print(f"[{ev.level}] {ev.message}", file=sys.stderr)
        if job.status in TERMINAL:
            return job.model_dump()
        time.sleep(delay)
        delay = min(delay * 2, 60.0)


def record(registry: Path, entry: str, job: dict, args: argparse.Namespace) -> None:
    """r6-model-id-version: append to the registry before anything downstream sees the ID."""
    reg = yaml.safe_load(registry.read_text(encoding="utf-8")) if registry.exists() else {}
    reg.setdefault("models", {})[entry] = {
        "model_id": job["fine_tuned_model"], "job_id": job["id"],
        "created": dt.date.today().isoformat(), "base_model": args.base,
        "training_file_id": args.training_file, "validation_file_id": args.validation_file,
        "n_epochs": args.epochs, "lr_multiplier": args.lr_multiplier,
        "trained_tokens": job.get("trained_tokens"),
        "eval_gate": {"passed": False, "report": None},  # deployment flips this after eval
        "rollout": {"pct": 0, "stage": "pending"},
    }
    registry.write_text(yaml.safe_dump(reg, sort_keys=False), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--training-file", required=True, help="file-... ID from data-prep upload")
    ap.add_argument("--validation-file", required=True, help="file-... ID; mandatory, not optional")
    ap.add_argument("--base", default="gpt-4o-mini-2024-07-18", choices=sorted(BASES))
    ap.add_argument("--train-count", type=int, required=True, help="rows in train.jsonl (from data-prep spec)")
    ap.add_argument("--epochs", type=int, help="override r3 policy; capped at 8")
    ap.add_argument("--lr-multiplier", type=float, default=1.0, help="r4: 1.0 default, 2.0 plateau, 0.5 oscillating")
    ap.add_argument("--suffix", required=True, help="becomes the ft:...::<suffix> tail and registry key")
    ap.add_argument("--registry", default="infra/model-id-registry.yaml")
    args = ap.parse_args()

    # r1-validated-files-only + r2-validation-file-required: both IDs must be real uploads.
    for fid in (args.training_file, args.validation_file):
        if not fid.startswith("file-"):
            ap.error(f"{fid!r} is not an OpenAI file ID; run data-prep upload first")
    args.epochs = min(args.epochs or epochs_for(args.train_count), 8)
    if not 0 < args.lr_multiplier <= 4:
        ap.error("lr_multiplier must be in (0, 4]")

    client = OpenAI()  # reads OPENAI_API_KEY
    job = client.fine_tuning.jobs.create(
        model=args.base,
        training_file=args.training_file,
        validation_file=args.validation_file,
        suffix=args.suffix,
        method={"type": "supervised", "supervised": {"hyperparameters": {
            "n_epochs": args.epochs, "learning_rate_multiplier": args.lr_multiplier}}},
    )
    print(f"launched {job.id} on {args.base} epochs={args.epochs} lr={args.lr_multiplier}", file=sys.stderr)

    final = poll(client, job.id)
    if final["status"] != "succeeded":
        print(json.dumps({"job_id": final["id"], "status": final["status"], "error": final.get("error")}))
        return 1
    record(Path(args.registry), args.suffix, final, args)
    print(json.dumps({
        "base_model": args.base, "training_file_id": args.training_file,
        "validation_file_id": args.validation_file, "n_epochs": args.epochs,
        "lr_multiplier": args.lr_multiplier, "job_id": final["id"],
        "fine_tuned_model_id": final["fine_tuned_model"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
