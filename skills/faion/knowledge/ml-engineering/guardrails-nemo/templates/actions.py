"""actions.py.
purpose: NeMo custom @action() skeletons for jailbreak + fact-check
consumes: user_input / bot_message / knowledge_base
produces: bool / dict result returned to Colang flow
depends-on: nemoguardrails >= 0.10
token-budget-impact: +260t when imported.
"""
from __future__ import annotations

import re

from nemoguardrails.actions import action

JAILBREAK_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"ignore\s+(?:all\s+)?(?:previous|above|prior)\s+(?:instructions?|prompts?)",
        r"you\s+are\s+now\s+(?:in\s+)?(?:developer|debug|admin)\s+mode",
        r"<\|im_start\|>|<\|im_end\|>",
    ]
]


@action()
async def check_jailbreak_action(user_input: str) -> bool:
    """Return True if the input matches a known jailbreak signature."""
    return any(p.search(user_input) for p in JAILBREAK_PATTERNS)


@action()
async def check_facts(context: dict, llm: object, kb: object) -> bool:
    """Return True iff bot_message is supported by KB documents."""
    bot_message: str = context.get("bot_message", "")
    if not bot_message or kb is None:
        return False
    docs = kb.search(bot_message, top_k=3)
    if not docs:
        return False
    prompt = (
        "Decide if RESPONSE is supported by DOCS. Reply 'supported' or 'not_supported'.\n"
        f"RESPONSE:\n{bot_message}\n"
        f"DOCS:\n" + "\n---\n".join(d.content for d in docs)
    )
    verdict = (await llm.generate(prompt)).strip().lower()
    return verdict == "supported"
