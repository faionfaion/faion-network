# purpose: RAGAS evaluation runner: faithfulness + answer-relevance + context metrics
# consumes: questions + answers + contexts (+ ground_truth)
# produces: RAGAS score dict for the report
# depends-on: content/02-output-contract.xml + content/04-procedure.xml
# token-budget-impact: medium

"""
RAGAS evaluation runner for RAG pipelines.
Requires: pip install ragas datasets
"""

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from datasets import Dataset


def run_ragas_evaluation(
    questions: list[str],
    generated_answers: list[str],
    retrieved_chunks: list[list[str]],
    ground_truth_answers: list[str] | None = None,
) -> dict:
    """
    Run RAGAS evaluation on a RAG pipeline output.

    Args:
        questions: List of user queries
        generated_answers: Model-generated answers
        retrieved_chunks: Per-query list of retrieved text chunks
        ground_truth_answers: Optional; required for context_recall and answer_correctness

    Returns:
        Dict of metric names to mean scores
    """
    data: dict = {
        "question": questions,
        "answer": generated_answers,
        "contexts": retrieved_chunks,
    }
    metrics = [faithfulness, answer_relevancy, context_precision]

    if ground_truth_answers is not None:
        data["ground_truth"] = ground_truth_answers
        metrics.append(context_recall)

    dataset = Dataset.from_dict(data)
    result = evaluate(dataset, metrics=metrics)
    return result.to_pandas().mean().to_dict()


# Usage:
# scores = run_ragas_evaluation(questions, answers, chunks, ground_truth)
# print(scores)
# Expected: {"faithfulness": 0.87, "answer_relevancy": 0.92, ...}
