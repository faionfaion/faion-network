# purpose: Typed pipeline-state object for sequential / hierarchical multi-agent flows
# consumes: agent-edge messages
# produces: TypedDict / Pydantic state for the orchestrator
# depends-on: content/02-output-contract.xml
# token-budget-impact: small

"""
Typed state models for multi-agent patterns.
Use with LangGraph StateGraph or pass as context dict to agent frameworks.
"""

from typing import TypedDict, Optional, Any
from pydantic import BaseModel


# --- Pydantic models for inter-agent messages (prefer over raw dicts) ---

class PipelineState(BaseModel):
    """Minimal sequential pipeline state."""
    raw_input: str
    parsed: Optional[dict] = None
    enriched: Optional[dict] = None
    validated: Optional[bool] = None
    output: Optional[str] = None


# --- TypedDict state for LangGraph ---

class SupervisorState(TypedDict):
    task: str
    routed_to: str
    worker_results: dict[str, Any]
    final_response: Optional[str]
    iteration: int
    error: Optional[str]


class HierarchicalState(TypedDict):
    goal: str
    subtasks: list[dict]
    team_assignments: dict[str, list[str]]
    team_results: dict[str, list[dict]]
    final_output: Optional[str]
    iteration: int
    error: Optional[str]


class SequentialState(TypedDict):
    pipeline_stage: int
    stage_outputs: dict[str, Any]
    validation_passed: bool
    final_output: Optional[str]
    error: Optional[str]


class PeerToPeerState(TypedDict):
    message_history: list[dict]
    visited_agents: list[str]
    routing_path: list[str]
    consensus_reached: bool
    final_output: Optional[str]
    error: Optional[str]


def create_state(pattern: str, **kwargs) -> dict:
    """Create initial state dict for a given pattern."""
    defaults = {
        "supervisor": SupervisorState(
            task="", routed_to="", worker_results={},
            final_response=None, iteration=0, error=None,
        ),
        "hierarchical": HierarchicalState(
            goal="", subtasks=[], team_assignments={},
            team_results={}, final_output=None, iteration=0, error=None,
        ),
        "sequential": SequentialState(
            pipeline_stage=0, stage_outputs={},
            validation_passed=True, final_output=None, error=None,
        ),
        "peer_to_peer": PeerToPeerState(
            message_history=[], visited_agents=[], routing_path=[],
            consensus_reached=False, final_output=None, error=None,
        ),
    }
    base = dict(defaults.get(pattern, {}))
    base.update(kwargs)
    return base
