"""
purpose: A/B harness comparing two PromptLibrary versions against a golden set.
consumes: baseline prompt, candidate prompt, golden list[(input, expected)], llm_call, metric.
produces: AbRecord (overall lift + per-case regressions list).
depends-on: stdlib only; pluggable metric function.
token-budget-impact: 2 × N calls per A/B run; sample golden set if budget-constrained.
"""
from dataclasses import dataclass, field
from typing import Callable
import statistics


@dataclass
class AbRecord:
    baseline_score: float
    candidate_score: float
    lift_pct: float
    per_case_regressions: list[tuple[int, float]] = field(default_factory=list)

    def passes_gate(self, max_per_case_regression_pct: float = 5.0, min_lift_pct: float = 0.0) -> bool:
        if self.lift_pct < min_lift_pct:
            return False
        return all(reg < max_per_case_regression_pct for _, reg in self.per_case_regressions)


def run_ab(
    baseline_render: Callable[[dict], list[dict]],
    candidate_render: Callable[[dict], list[dict]],
    golden_set: list[tuple[dict, str]],
    llm_call: Callable[[list[dict]], str],
    metric: Callable[[str, str], float],
) -> AbRecord:
    """Run A/B on golden set, return AbRecord with lift and per-case regression list."""
    baseline_scores, candidate_scores = [], []
    for i, (inputs, expected) in enumerate(golden_set):
        b = metric(llm_call(baseline_render(inputs)), expected)
        c = metric(llm_call(candidate_render(inputs)), expected)
        baseline_scores.append(b)
        candidate_scores.append(c)
    baseline = statistics.mean(baseline_scores)
    candidate = statistics.mean(candidate_scores)
    lift_pct = (candidate - baseline) * 100 if baseline else 0.0
    regressions = [
        (i, (b - c) * 100)
        for i, (b, c) in enumerate(zip(baseline_scores, candidate_scores))
        if c < b
    ]
    return AbRecord(baseline, candidate, lift_pct, regressions)
