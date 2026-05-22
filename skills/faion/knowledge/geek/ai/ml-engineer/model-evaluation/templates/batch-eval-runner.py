# purpose: Batch-runs an evaluation suite end to end and emits a report
# consumes: eval suite + model id + dataset
# produces: report JSON for templates/_smoke-test.md
# depends-on: content/02-output-contract.xml + scripts/validate-model-evaluation.py
# token-budget-impact: medium

"""
Async batch evaluation runner using Anthropic SDK.
Reads JUDGE_PROMPT from llm-judge-prompt.txt; rate-limits concurrent calls.
"""

import asyncio
import json
from pathlib import Path
from anthropic import AsyncAnthropic

JUDGE_PROMPT = (Path(__file__).parent / "llm-judge-prompt.txt").read_text()
MAX_CONCURRENT = 10  # stay within API rate limits

client = AsyncAnthropic()


async def evaluate_sample(question: str, reference: str, candidate: str) -> dict:
    """Score one sample with LLM-as-judge. Returns parsed score dict."""
    prompt = JUDGE_PROMPT.format(
        question=question,
        reference_answer=reference,
        model_output=candidate,
    )
    response = await client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": "parse_failed", "raw": text}


async def run_evaluation(dataset: list[dict]) -> list[dict]:
    """
    Evaluate all samples with rate-limited concurrency.
    Each item in dataset: {"question": ..., "reference": ..., "candidate": ...}
    """
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    async def bounded_eval(item: dict) -> dict:
        async with semaphore:
            score = await evaluate_sample(
                item["question"], item["reference"], item["candidate"]
            )
            return {**item, "score": score}

    tasks = [bounded_eval(item) for item in dataset]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Replace exceptions with error dicts
    return [
        r if not isinstance(r, Exception) else {"error": str(r)}
        for r in results
    ]


def aggregate(results: list[dict]) -> dict:
    """Compute mean scores and failure rate."""
    valid = [r for r in results if "score" in r and "error" not in r.get("score", {})]
    if not valid:
        return {"error": "no_valid_results"}
    keys = ["accuracy", "completeness", "clarity", "hallucination", "total"]
    return {
        k: sum(r["score"].get(k, 0) for r in valid) / len(valid)
        for k in keys
    } | {"n_samples": len(valid), "n_failed": len(results) - len(valid)}


# Usage:
# results = asyncio.run(run_evaluation(dataset))
# print(aggregate(results))
