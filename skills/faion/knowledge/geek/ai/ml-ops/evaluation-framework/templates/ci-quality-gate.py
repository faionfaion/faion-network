"""
CI quality gate using ModelEvaluator with exact_match metric.
Input:  test_cases (list of EvaluationCase), system_prompt, thresholds dict
Output: {"passed": bool, "means": {metric: float}, "thresholds": dict}
"""
import json
from dataclasses import dataclass
from typing import Optional
from openai import OpenAI


@dataclass
class EvaluationCase:
    input: str
    expected_output: Optional[str] = None
    metadata: dict = None


def exact_match(input: str, actual: str, expected: Optional[str]) -> Optional[float]:
    if expected is None:
        return None
    return 1.0 if actual.strip() == expected.strip() else 0.0


def run_ci_gate(
    test_cases: list,
    system_prompt: str,
    thresholds: dict,
    model: str = "gpt-4o-mini",
) -> dict:
    client = OpenAI()
    results = []
    for case in test_cases:
        resp = client.chat.completions.create(
            model=model,
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": case.input},
            ],
        )
        output = resp.choices[0].message.content
        metrics = {"exact_match": exact_match(case.input, output, case.expected_output)}
        results.append({"output": output, "metrics": metrics})

    means = {}
    for metric in thresholds:
        vals = [
            r["metrics"].get(metric)
            for r in results
            if isinstance(r["metrics"].get(metric), float)
        ]
        means[metric] = sum(vals) / len(vals) if vals else 0.0

    passed = all(means.get(m, 0) >= t for m, t in thresholds.items())
    return {"passed": passed, "means": means, "thresholds": thresholds}
