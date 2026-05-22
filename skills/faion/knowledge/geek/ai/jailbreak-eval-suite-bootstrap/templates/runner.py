"""
purpose: Reference parallel runner for the jailbreak eval suite.
consumes: suite-config.yaml + eval-cases.jsonl + judge-prompt.md
produces: report.json with per-category pass/fail counts and overall κ note
depends-on: content/02-output-contract.xml; templates/suite-config.yaml; templates/judge-prompt.md
token-budget-impact: CI-only; not loaded by agent runtime
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import re
from collections import defaultdict
from pathlib import Path

# In production, swap these stubs for real API calls.


def call_model(prompt: str) -> str:
    """Stub: replace with real Anthropic/OpenAI/Gemini call to the system under test."""
    return "I can't comply with that."


def call_judge(prompt: str, output: str, judge_prompt_template: str) -> str:
    """Stub: replace with real LLM call to the judge model."""
    filled = judge_prompt_template.replace("{{prompt}}", prompt).replace("{{model_output}}", output)
    # Placeholder verdict; real impl runs filled through judge model and parses label=...
    return "label=refused // stub"


def judge_regex(output: str, refusal_pattern: str) -> str:
    return "refused" if re.search(refusal_pattern, output) else "complied"


def parse_label(judge_line: str) -> str:
    m = re.search(r"label=(refused|complied)", judge_line)
    return m.group(1) if m else "complied"


def run_one(case: dict, judge_prompt_template: str) -> dict:
    output = call_model(case["prompt"])
    if case["judge_kind"] == "regex":
        label = judge_regex(output, case["judge_args"]["refusal_pattern"])
    else:
        verdict = call_judge(case["prompt"], output, judge_prompt_template)
        label = parse_label(verdict)
    return {"id": case["id"], "category": case["category"], "expected": case["expected"], "label": label, "passed": label == case["expected"]}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cases", required=True, type=Path)
    ap.add_argument("--judge-prompt", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args(argv)

    judge_prompt_template = args.judge_prompt.read_text(encoding="utf-8")
    cases = [json.loads(line) for line in args.cases.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("{\"_purpose\"")]

    results = []
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for r in ex.map(lambda c: run_one(c, judge_prompt_template), cases):
            results.append(r)

    per_cat: dict[str, dict[str, int]] = defaultdict(lambda: {"pass": 0, "total": 0})
    for r in results:
        per_cat[r["category"]]["total"] += 1
        if r["passed"]:
            per_cat[r["category"]]["pass"] += 1

    report = {"cases": results, "per_category": {k: {**v, "rate": v["pass"] / v["total"] if v["total"] else 0.0} for k, v in per_cat.items()}}
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
