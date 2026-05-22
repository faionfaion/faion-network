# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

"""LangGraph map-reduce fan-out reference.

Pattern:
  router  -- Send per item -->  score_one  -- reducer merges -->  aggregate
  (cap 20)                       (idempotent)                     (uses scored list)
"""
import operator
from typing import Annotated, TypedDict

from langgraph.graph import StateGraph
from langgraph.types import Send

MAX_FANOUT = 20


class State(TypedDict):
    items: list[str]
    scored: Annotated[list[dict], operator.add]   # reducer is REQUIRED


def router(state: State):
    """Emit one Send per item, capped at MAX_FANOUT."""
    batch = state["items"][:MAX_FANOUT]
    return [Send("score_one", {"item": item}) for item in batch]


def score_one(payload: dict) -> dict:
    """Idempotent per-item branch. No external mutation.

    Same input → same output, safe to retry as part of an atomic super-step.
    """
    item = payload["item"]
    score = llm_score(item)        # caller-provided; pure or read-only
    return {"scored": [{"item": item, "score": score}]}


def aggregate(state: State) -> dict:
    """Reduce — picks top by score. Runs once after all Sends complete."""
    top = max(state["scored"], key=lambda r: r["score"])
    return {"winner": top}


def llm_score(item: str) -> float:
    """Stub for the per-item scoring call. Replace with your model client."""
    raise NotImplementedError


def build_graph():
    g = StateGraph(State)
    g.add_node("score_one", score_one)
    g.add_node("aggregate", aggregate)
    g.add_conditional_edges("__start__", router, ["score_one"])
    g.add_edge("score_one", "aggregate")
    return g.compile()
