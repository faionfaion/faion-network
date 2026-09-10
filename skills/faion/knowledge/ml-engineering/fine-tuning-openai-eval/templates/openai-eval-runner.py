"""
purpose: Eval runner: takes ft + base IDs, runs on held-out, returns scores.
consumes: see AGENTS.md ## Prerequisites
produces: report
depends-on: content/02-output-contract.xml schema for fine-tuning-openai-eval
token-budget-impact: ≤500 tokens to fill
"""
# Usage:
#   export OPENAI_API_KEY=...
#   python openai-eval-runner.py --ft ft:gpt-4o-mini-2024-07-18:org::tone_v1 \
#       --base gpt-4o-mini-2024-07-18 --eval data/eval.jsonl --train data/train.jsonl \
#       --criterion "Adopts the requested tone and keeps every fact." \
#       --threshold exact_match=0.80 --threshold judge_pass=0.85 > eval-report.json
# Requires: pip install openai>=1.0

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

from openai import OpenAI

JUDGE_PROMPT = Path(__file__).with_name("judge-prompt.txt")


def load_jsonl(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def user_hash(row: dict) -> str:
    return hashlib.sha1(next(m["content"] for m in row["messages"] if m["role"] == "user").encode()).hexdigest()


def wilson(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """r5-confidence-interval: 95% Wilson interval for a proportion."""
    if n == 0:
        return 0.0, 0.0
    p, denom = successes / n, 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return round(centre - half, 4), round(centre + half, 4)


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


class Runner:
    def __init__(self, client: OpenAI, judge_model: str, criterion: str) -> None:
        self.client, self.judge_model, self.criterion = client, judge_model, criterion
        # r4-judge-rubric-stable: the rubric is read once, hashed, and never rewritten here.
        self.rubric = JUDGE_PROMPT.read_text(encoding="utf-8")
        self.rubric_sha256 = hashlib.sha256(self.rubric.encode()).hexdigest()

    def answer(self, model: str, row: dict) -> str:
        prompt = [m for m in row["messages"] if m["role"] != "assistant"]
        resp = self.client.chat.completions.create(model=model, messages=prompt, temperature=0, max_tokens=512)
        return resp.choices[0].message.content or ""

    def judge(self, row: dict, candidate: str) -> int:
        user = next(m["content"] for m in row["messages"] if m["role"] == "user")
        reference = row["messages"][-1]["content"]
        filled = (self.rubric.replace("<criterion>", self.criterion).replace("<user_input>", user)
                  .replace("<reference_answer>", reference).replace("<candidate_response>", candidate))
        resp = self.client.chat.completions.create(
            model=self.judge_model, messages=[{"role": "user", "content": filled}],
            temperature=0, response_format={"type": "json_object"})
        return int(json.loads(resp.choices[0].message.content)["score"])

    def score_arm(self, model: str, rows: list[dict]) -> dict[str, int]:
        hits = {"exact_match": 0, "judge_pass": 0}
        for row in rows:
            out = self.answer(model, row)
            hits["exact_match"] += normalise(out) == normalise(row["messages"][-1]["content"])
            hits["judge_pass"] += self.judge(row, out) >= 4
        return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ft", required=True, help="ft:... model ID")
    ap.add_argument("--base", required=True)
    ap.add_argument("--eval", required=True, help="held-out chat JSONL (last assistant turn = reference), >= 200 rows")
    ap.add_argument("--train", action="append", default=[], help="train/val JSONL to prove disjointness")
    ap.add_argument("--judge-model", default="gpt-4o-2024-08-06")
    ap.add_argument("--criterion", required=True)
    ap.add_argument("--threshold", action="append", default=[], help="metric=min_ft_score, repeatable")
    args = ap.parse_args()

    rows = load_jsonl(args.eval)
    if len(rows) < 200:  # r2-min-200-examples
        ap.error(f"{len(rows)} eval rows < 200; the CI would swamp the metric")
    seen = {user_hash(r) for path in args.train for r in load_jsonl(path)}
    leaked = sum(user_hash(r) in seen for r in rows)
    if leaked:  # r1-held-out-required
        ap.error(f"{leaked} eval rows also appear in training data; re-split before eval")
    thresholds = dict(t.split("=") for t in args.threshold)

    runner = Runner(OpenAI(), args.judge_model, args.criterion)
    ft_hits, base_hits = runner.score_arm(args.ft, rows), runner.score_arm(args.base, rows)

    metrics, n = [], len(rows)
    for name in ("exact_match", "judge_pass"):  # r3-two-or-more-metrics
        ft, base = ft_hits[name] / n, base_hits[name] / n
        lo, hi = wilson(ft_hits[name], n)
        base_lo, base_hi = wilson(base_hits[name], n)
        threshold = float(thresholds.get(name, 0.0))
        # r6-gate-explicit: binary per metric; passes only if above threshold AND CIs do not overlap.
        passed = ft >= threshold and lo > base_hi
        metrics.append({"name": name, "ft_score": round(ft, 4), "base_score": round(base, 4), "delta": round(ft - base, 4),
                        "ci": f"[{lo}, {hi}]", "base_ci": f"[{base_lo}, {base_hi}]", "threshold": threshold, "passed": passed})
    gate = "pass" if all(m["passed"] for m in metrics) else (
        "hold" if all(m["ft_score"] >= m["threshold"] for m in metrics) else "fail")
    print(json.dumps({"ft_model_id": args.ft, "base_model_id": args.base, "eval_set_path": args.eval,
                      "eval_count": n, "eval_disjoint": True, "judge_model": args.judge_model,
                      "rubric_sha256": runner.rubric_sha256, "metrics": metrics, "gate_decision": gate}, indent=2))
    return 0 if gate == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
