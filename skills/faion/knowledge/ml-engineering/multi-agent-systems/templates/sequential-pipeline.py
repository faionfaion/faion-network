# purpose: Sequential pipeline runner: per-step state, retries, typed handoff contract
# consumes: pipeline config + per-step prompts
# produces: Python module running the pipeline with traces
# depends-on: content/02-output-contract.xml + content/04-procedure.xml
# token-budget-impact: medium

"""
Minimal 3-agent sequential pipeline: researcher → writer → reviewer.
State is serialized as JSON and passed explicitly between agents.
"""
import anthropic
import json
from pathlib import Path

client = anthropic.Anthropic()
STATE_FILE = Path("/tmp/agent-state.json")


def run_agent(role: str, instruction: str, state: dict, model: str = "claude-sonnet-4-5") -> dict:
    """Run a single agent with the current state. Returns parsed JSON dict."""
    resp = client.messages.create(
        model=model,
        max_tokens=4096,
        system=f"You are the {role}. Return valid JSON only — no prose outside JSON.",
        messages=[{
            "role": "user",
            "content": f"Current state:\n{json.dumps(state, indent=2)}\n\nTask: {instruction}"
        }],
    )
    return json.loads(resp.content[0].text)


def run_pipeline(task: str) -> dict:
    state = {"task": task, "research": None, "draft": None, "review": None}

    # Stage 1: Research
    state["research"] = run_agent(
        "researcher",
        'Research the task and return {"findings": "..."}.',
        state,
        model="claude-sonnet-4-5",
    )

    # Stage 2: Write
    state["draft"] = run_agent(
        "writer",
        'Write a draft using the research findings. Return {"draft": "..."}.',
        state,
        model="claude-sonnet-4-5",
    )

    # Stage 3: Review
    state["review"] = run_agent(
        "reviewer",
        'Review the draft critically. Return {"verdict": "pass|fail", "notes": "...", "revised_draft": "..."}.',
        state,
        model="claude-opus-4-5",  # Opus for final quality gate
    )

    STATE_FILE.write_text(json.dumps(state, indent=2))
    return state
