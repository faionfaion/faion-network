"""
tool-recommender.py — Haiku-based phase mapper for research tool selection.
Input:  task_description (str), budget (str) = "free" | "mid" | "enterprise"
Output: str — JSON with phase, recommended_tools, rationale
"""
import anthropic

client = anthropic.Anthropic()

PHASE_MAP = {
    "exploration": ["Perplexity", "Claude", "Google Trends"],
    "competitor-intel": ["Crayon", "Klue", "Contify", "AlphaSense"],
    "interview-analysis": ["Looppanel", "Dovetail", "Insight7"],
    "survey-analysis": ["Qualtrics", "SurveyMonkey AI"],
    "sentiment": ["Brandwatch", "Sprout Social"],
    "synthesis": ["Miro AI", "Condens", "EnjoyHQ"],
    "synthetic-research": ["Synthetic Users", "Viewpoints.ai"],
}


def recommend_tools(task_description: str, budget: str = "mid") -> str:
    """Map a task description to its research phase and recommend tools."""
    phase_list = "\n".join(
        f"- {p}: {', '.join(t)}" for p, t in PHASE_MAP.items()
    )
    prompt = f"""<tool_selection>
<task>{task_description}</task>
<budget>{budget}</budget>
<phases>
{phase_list}
</phases>
<output>JSON: {{"phase": "...", "recommended_tools": [...], "rationale": "..."}}</output>
</tool_selection>"""
    r = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return r.content[0].text
