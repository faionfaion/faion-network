# purpose: Ingress query router scaffold
# consumes: inputs declared in AGENTS.md Prerequisites table
# produces: artefact conforming to content/02-output-contract.xml (graph-rag-production)
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~150-400 tokens when loaded as context
"""router.py — classifies incoming GraphRAG queries.

GLOBAL: corpus-wide synthesis (uses community summaries).
LOCAL: entity-anchored multi-hop (uses graph neighborhood).
COMMUNITY: thematic question (single community summary).
NONE: pure vector lookup — bypass graph entirely.
"""
from __future__ import annotations

from typing import Literal

QueryType = Literal["GLOBAL", "LOCAL", "COMMUNITY", "NONE"]


def classify(question: str, llm) -> QueryType:
    prompt = (
        "Classify the question intent for GraphRAG dispatch. "
        "Reply with exactly one of GLOBAL, LOCAL, COMMUNITY, NONE."
        f"\nQUESTION: {question}"
    )
    resp = llm.complete(prompt).strip().upper()
    if resp in ("GLOBAL", "LOCAL", "COMMUNITY", "NONE"):
        return resp  # type: ignore[return-value]
    return "NONE"
