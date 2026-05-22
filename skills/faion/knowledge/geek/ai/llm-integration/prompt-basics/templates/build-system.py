"""
purpose: Compose a system prompt from role + constraints list + output_format spec.
consumes: role string, constraints list[str], output_format string.
produces: assembled system string ready for PromptTemplate.system.
depends-on: stdlib only.
token-budget-impact: target ≤2K tokens per system prompt; trim constraints if longer.
"""


def build_system(
    role: str,
    constraints: list[str] | None = None,
    output_format: str = "",
) -> str:
    """Build a structured system prompt. Keep under 2K tokens."""
    parts = [f"You are {role}."]
    if constraints:
        parts.append("Constraints:\n" + "\n".join(f"- {c}" for c in constraints))
    if output_format:
        parts.append(f"Output format:\n{output_format}")
    return "\n\n".join(parts)


# Example system prompts
ASSISTANT = build_system(
    role="a helpful, harmless, and honest AI assistant",
    constraints=[
        "Be concise and direct",
        "Acknowledge uncertainty",
        "Never make up information",
    ],
)

CODE_EXPERT = build_system(
    role="an expert software developer",
    constraints=[
        "Include type hints in Python code",
        "Add docstrings to functions",
        "Handle errors appropriately",
    ],
)
