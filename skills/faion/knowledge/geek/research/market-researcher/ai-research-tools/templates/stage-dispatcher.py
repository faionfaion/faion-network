"""
stage-dispatcher.py — Orchestrator for multi-stage market research.
Input:  topic (str), stages (list[dict]) — each has 'name' and 'query'
Output: str — JSON list of {stage, tool, query, expected_output}
Selects tool per stage from STAGE_TOOLS map.
"""
import anthropic
import json

client = anthropic.Anthropic()

STAGE_TOOLS = {
    "exploration": "perplexity",
    "competitor-intel": "serpapi",
    "trend": "google-trends",
    "interview-analysis": "dovetail-export",
    "synthesis": "claude-sonnet",
}


def select_tool(task_type: str) -> str:
    tool = STAGE_TOOLS.get(task_type)
    if not tool:
        raise ValueError(
            f"Unknown task type: {task_type}. Valid: {list(STAGE_TOOLS)}"
        )
    return tool


def orchestrate_research(topic: str, stages: list[dict]) -> str:
    """Generate optimal query for each stage's assigned tool."""
    stage_summary = "\n".join(
        f"- {s['name']} ({select_tool(s['name'])}): {s['query']}"
        for s in stages
    )
    prompt = f"""<research_orchestration>
<topic>{topic}</topic>
<stages>{stage_summary}</stages>
<instruction>For each stage, generate the optimal query for the assigned tool.
Output JSON: [{{"stage": "...", "tool": "...", "query": "...", "expected_output": "..."}}]
</instruction>
</research_orchestration>"""
    r = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return r.content[0].text
