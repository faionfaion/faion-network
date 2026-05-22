"""
purpose: Multi-agent supervisor pattern.
consumes: see AGENTS.md ## Prerequisites
produces: code
depends-on: content/02-output-contract.xml schema for langchain
token-budget-impact: ≤500 tokens to fill
"""

# LangGraph Supervisor pattern with state accumulation
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class SupervisorState(TypedDict):
    task: str
    results: Annotated[list, operator.add]  # accumulates across worker calls
    next_worker: str

def supervisor_node(state: SupervisorState) -> SupervisorState:
    decision = llm.invoke(
        f"Route task '{state['task']}' to: researcher | writer | done"
    )
    return {"next_worker": decision.strip()}

def researcher_node(state: SupervisorState) -> SupervisorState:
    result = llm.invoke(f"Research: {state['task']}")
    return {"results": [result]}  # operator.add appends this to existing list

def writer_node(state: SupervisorState) -> SupervisorState:
    result = llm.invoke(f"Write based on: {state['results']}")
    return {"results": [result]}

graph = StateGraph(SupervisorState)
graph.add_node("supervisor", supervisor_node)
graph.add_node("researcher", researcher_node)
graph.add_node("writer", writer_node)
graph.add_conditional_edges(
    "supervisor",
    lambda s: s["next_worker"],
    {"researcher": "researcher", "writer": "writer", "done": END},
)
graph.add_edge("researcher", "supervisor")
graph.add_edge("writer", "supervisor")
graph.set_entry_point("supervisor")
app = graph.compile()
