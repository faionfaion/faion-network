"""Claude Extended Thinking invocation with task-type budget selector."""
import anthropic

client = anthropic.Anthropic()


def reasoning_budget(task_type: str) -> int:
    """Return thinking token budget by task type."""
    budgets = {
        "format": 1024,       # Reformatting, extraction
        "analysis": 4096,     # Code review, logic check
        "planning": 8192,     # Architecture, multi-step plan
        "research": 32768,    # Deep synthesis, theorem proving
    }
    return budgets.get(task_type, 4096)


def think(
    task: str,
    task_type: str = "analysis",
    model: str = "claude-opus-4-5",
) -> str:
    """Invoke Claude Extended Thinking and return the final answer only."""
    budget = reasoning_budget(task_type)

    response = client.messages.create(
        model=model,
        max_tokens=budget + 4000,  # thinking budget + answer buffer
        thinking={"type": "enabled", "budget_tokens": budget},
        messages=[{"role": "user", "content": task}],
    )

    # content[0] is ThinkingBlock (internal), content[1] is TextBlock (answer)
    for block in response.content:
        if block.type == "text":
            return block.text

    return ""


def route_and_think(task: str) -> str:
    """Classify task complexity, choose model, invoke thinking if needed."""
    classifier = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=20,
        messages=[{"role": "user", "content":
            f"Classify task complexity: simple/complex. Task: {task[:200]}"}],
    )
    complexity = classifier.content[0].text.lower()

    if "complex" in complexity:
        return think(task, task_type="analysis", model="claude-opus-4-5")
    else:
        # Simple task: standard model, no extended thinking
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": task}],
        )
        return response.content[0].text
