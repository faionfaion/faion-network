"""
build_system — compose a system prompt from role, constraints, and output format.

Usage:
    system = build_system(
        role="a JSON extraction agent",
        constraints=["Return only valid JSON", "Never add prose"],
        output_format='{"field1": "string", "field2": ["list"]}'
    )
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
