"""
purpose: Reference runner for self-consistency CoT (N parallel samples + majority vote).
consumes: anthropic client + base prompt + N
produces: dict {final_answer, votes, samples}
depends-on: content/01-core-rules.xml r5; templates/cot-config.schema.json
token-budget-impact: N x baseline-CoT cost per call
"""
from __future__ import annotations

import concurrent.futures as cf
from collections import Counter
from typing import Callable


def vote(answers: list[str], rule: str = "majority") -> str:
    if rule == "majority":
        return Counter(answers).most_common(1)[0][0]
    if rule == "median":
        nums = sorted(float(a) for a in answers)
        return str(nums[len(nums) // 2])
    raise ValueError(f"unsupported voting rule: {rule}")


def self_consistency(prompt: str, n: int, llm_call: Callable[[str], str], parse_answer: Callable[[str], str], voting_rule: str = "majority") -> dict:
    with cf.ThreadPoolExecutor(max_workers=min(n, 8)) as ex:
        samples = list(ex.map(lambda _: llm_call(prompt), range(n)))
    answers = [parse_answer(s) for s in samples]
    final = vote(answers, voting_rule)
    return {"final_answer": final, "votes": dict(Counter(answers)), "samples": samples}
