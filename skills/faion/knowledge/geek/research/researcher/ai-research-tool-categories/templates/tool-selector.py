# tool_selector.py — filter research tools by phase and budget tier
# Returns a list of tool names matching the given phase and budget.

PHASE_MAP: dict[str, list[str]] = {
    "exploration": ["Perplexity Pro", "Claude", "Google Trends"],
    "competitor_intel": ["Crayon", "Klue", "AlphaSense", "Contify"],
    "interviews": ["Looppanel", "Dovetail", "AssemblyAI", "Whisper"],
    "survey": ["Qualtrics", "SurveyMonkey AI"],
    "sentiment": ["Brandwatch", "Sprout Social"],
    "synthesis": ["Dovetail", "Condens", "EnjoyHQ"],
    "synthetic": ["Synthetic Users", "Viewpoints.ai", "Aaru"],
}

BUDGET_SETS: dict[str, set[str]] = {
    "free": {"Claude", "Google Trends", "Whisper"},
    "mid": {
        "Perplexity Pro", "Claude", "Google Trends", "Whisper",
        "Looppanel", "Dovetail", "Condens", "SurveyMonkey AI",
        "AssemblyAI", "Synthetic Users", "Viewpoints.ai",
    },
    "enterprise": set(
        tool for tools in PHASE_MAP.values() for tool in tools
    ),
}


def recommend(phase: str, budget: str) -> list[str]:
    """Return tools matching the given research phase and budget tier."""
    if phase not in PHASE_MAP:
        raise ValueError(f"Unknown phase: {phase}. Options: {list(PHASE_MAP)}")
    if budget not in BUDGET_SETS:
        raise ValueError(f"Unknown budget: {budget}. Options: {list(BUDGET_SETS)}")
    phase_tools = set(PHASE_MAP[phase])
    budget_tools = BUDGET_SETS[budget]
    return sorted(phase_tools & budget_tools)


# Examples:
# recommend("interviews", "mid")   → ['AssemblyAI', 'Dovetail', 'Looppanel', 'Whisper']
# recommend("competitor_intel", "free") → []  (no free-tier CI tools)
# recommend("exploration", "free") → ['Claude', 'Google Trends']
