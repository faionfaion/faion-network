"""
Complexity-based model router for Claude (Haiku → Sonnet → Opus).
Classifier uses Haiku for minimum overhead.
"""
from anthropic import Anthropic

client = Anthropic()

MODEL_MAP = {
    "simple": "claude-haiku-4-5",
    "medium": "claude-sonnet-4-5",
    "complex": "claude-opus-4-5",
}


def classify_complexity(task: str) -> str:
    """Returns: simple | medium | complex"""
    resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=10,
        messages=[{
            "role": "user",
            "content": (
                f"Classify task complexity as 'simple', 'medium', or 'complex'. "
                f"Output exactly one word.\nTask: {task[:200]}"
            ),
        }],
    )
    return resp.content[0].text.strip().lower()


def route_model(task: str) -> str:
    """Return the appropriate model name for the task."""
    tier = classify_complexity(task)
    return MODEL_MAP.get(tier, "claude-sonnet-4-5")


def routed_completion(task: str, max_tokens: int = 2048) -> str:
    """Complete a task using the cheapest model appropriate for its complexity."""
    model = route_model(task)
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": task}],
    )
    return resp.content[0].text
