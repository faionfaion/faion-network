"""
purpose: Regex parser extracting <reasoning> + <answer> blocks from CoT output.
consumes: raw model output string
produces: dict {reasoning: str, answer: str} or raises ValueError
depends-on: content/02-output-contract.xml
token-budget-impact: zero — runtime side
"""
from __future__ import annotations

import re

REASONING_RE = re.compile(r"<reasoning>(.*?)</reasoning>", re.DOTALL)
ANSWER_RE = re.compile(r"<answer>(.*?)</answer>", re.DOTALL)


def parse_cot(text: str) -> dict[str, str]:
    r = REASONING_RE.search(text)
    a = ANSWER_RE.search(text)
    if not r or not a:
        raise ValueError("missing <reasoning> or <answer> block")
    reasoning = r.group(1).strip()
    answer = a.group(1).strip()
    if not reasoning or not answer:
        raise ValueError("empty reasoning or answer block")
    return {"reasoning": reasoning, "answer": answer}
