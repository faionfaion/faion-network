"""
Minimal LangGraph supervisor pattern.
Replace route_with_llm, run_research, run_code_generation with real implementations.
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal


class State(TypedDict):
    task: str
    agent: str
    result: str
    iteration: int


MAX_ITER = 10


def supervisor(state: State) -> dict:
    """Route task to appropriate worker via LLM call."""
    agent = route_with_llm(state["task"])  # replace with real LLM routing
    return {"agent": agent, "iteration": state.get("iteration", 0) + 1}


def research_agent(state: State) -> dict:
    result = run_research(state["task"])  # replace with real impl
    return {"result": result}


def code_agent(state: State) -> dict:
    result = run_code_generation(state["task"])  # replace with real impl
    return {"result": result}


def router(state: State) -> Literal["research", "code", "__end__"]:
    if state.get("iteration", 0) >= MAX_ITER:
        return "__end__"
    return state.get("agent", "__end__")


graph = StateGraph(State)
graph.add_node("supervisor", supervisor)
graph.add_node("research", research_agent)
graph.add_node("code", code_agent)
graph.set_entry_point("supervisor")
graph.add_conditional_edges("supervisor", router, {
    "research": "research",
    "code": "code",
    "__end__": END,
})
graph.add_edge("research", END)
graph.add_edge("code", END)
app = graph.compile()

# Usage:
# result = app.invoke({"task": "Research AI trends", "agent": "", "result": "", "iteration": 0})
