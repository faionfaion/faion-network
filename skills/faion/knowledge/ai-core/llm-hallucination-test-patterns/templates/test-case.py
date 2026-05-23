# purpose: LLM Hallucination Test Patterns code skeleton
# consumes: Prerequisites bundle (see AGENTS.md)
# produces: artefact conforming to content/02-output-contract.xml (code)
# depends-on: content/01-core-rules.xml + content/02-output-contract.xml
# token-budget-impact: ~200-1000 tokens when loaded as context


"""Test-case scaffold for LLM Hallucination Test Patterns.

Wire each case to the schema in content/02-output-contract.xml.
Run with pytest. Add ≥10 cases per attack-class / pattern.
"""
from __future__ import annotations


CASES = [
    # (case_id, attack_class_or_pattern, input_text, expected_behavior)
    ("case-001", "<class>", "<input>", "<expected: refusal | grounded | etc>"),
]


def evaluate(model_response: str, expected: str) -> bool:
    # Concrete evaluator per pattern; see content/01-core-rules.xml
    # for per-pattern pass/fail criteria.
    raise NotImplementedError("wire to your eval pipeline")


def test_all_cases():
    for case_id, cls, inp, expected in CASES:
        # response = call_model(inp)
        # assert evaluate(response, expected), f"{case_id} ({cls}) failed"
        pass
