"""Eval gate: block deployment of LoRA-fine-tuned models that fail quality thresholds."""
from dataclasses import dataclass
from typing import Callable


@dataclass
class EvalGateResult:
    passed: bool
    domain_acc: float
    general_score: float
    refusal_rate: float
    failures: list[str]


def run_eval_gate(
    evaluate_domain: Callable,
    evaluate_general: Callable,
    measure_refusal: Callable,
    base_scores: dict[str, float],
    domain_eval_data: list,
    general_eval_data: list,
    domain_threshold_delta: float = 0.10,
    general_threshold_ratio: float = 0.80,
    max_refusal_rate: float = 0.05,
) -> EvalGateResult:
    """
    Run three-gate eval check before permitting model deployment.

    Gates:
    1. Domain accuracy >= base_domain_accuracy + domain_threshold_delta
    2. General score >= base_general_score * general_threshold_ratio
    3. Refusal rate <= max_refusal_rate on domain prompts
    """
    domain_acc = evaluate_domain(domain_eval_data)
    general_score = evaluate_general(general_eval_data)
    refusal_rate = measure_refusal(domain_eval_data)

    failures = []

    domain_threshold = base_scores["domain"] + domain_threshold_delta
    if domain_acc < domain_threshold:
        failures.append(
            f"Domain accuracy {domain_acc:.3f} below threshold {domain_threshold:.3f}"
        )

    general_threshold = base_scores["general"] * general_threshold_ratio
    if general_score < general_threshold:
        failures.append(
            f"General score {general_score:.3f} degraded below "
            f"{general_threshold_ratio*100:.0f}% of base ({general_threshold:.3f})"
        )

    if refusal_rate > max_refusal_rate:
        failures.append(
            f"Refusal rate {refusal_rate:.1%} exceeds {max_refusal_rate:.1%} threshold"
        )

    return EvalGateResult(
        passed=len(failures) == 0,
        domain_acc=domain_acc,
        general_score=general_score,
        refusal_rate=refusal_rate,
        failures=failures,
    )


def assert_gate(result: EvalGateResult) -> None:
    """Raise ValueError if gate failed — use in CI/CD pipeline."""
    if not result.passed:
        raise ValueError(
            "Eval gate FAILED. Model deployment blocked.\n"
            + "\n".join(f"  - {f}" for f in result.failures)
        )
