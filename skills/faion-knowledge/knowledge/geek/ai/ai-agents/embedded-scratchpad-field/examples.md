# Examples — Embedded Scratchpad Field

## Example 1: GSM8k +60% with one field

A team running GSM8k benchmark on Sonnet measured 31% accuracy on a schema like `{answer: int}`. Adding `reasoning: str` BEFORE `answer` raised accuracy to 49%. AWS reported similar gains across math benchmarks.

The model had been forced to compute mentally; the scratchpad let it externalize.

## Example 2: Code review with evidence first

```python
class Review(BaseModel):
    evidence: list[str] = Field(description="Code snippets being commented on (max 5).")
    issues_found: list[str]
    severity_high_to_low: list[str] = Field(description="ordered severity tags")
    summary: str
    verdict: Literal["approve", "request_changes"]
```

Before evidence-first ordering, "verdict" often didn't match "issues_found" because the model decided early. Evidence-first locks the model into citing specific code BEFORE deciding.

## Example 3: Triage classification

```python
class Triage(BaseModel):
    rationale: str = Field(description="Why this category fits.")
    category: Literal["billing", "auth", "performance", "feature_request", "other"]
    priority: Literal["low", "medium", "high", "critical"]
```

Without `rationale`, "other" was the model's escape hatch (~25% of items). With `rationale`, "other" dropped below 5% — having to justify the choice forced more specific classification.

## Example 4: Anti-example

```python
# BAD
class Bad(BaseModel):
    answer: str
    reasoning: str   # placed after — CANNOT be CoT
```

The reasoning field is now post-hoc rationalization. Token-spent but no quality benefit.

Fix: swap the order.

## Example 5: Multi-stage pipeline

Stage 1 (planner):
```python
class Plan(BaseModel):
    plan_steps: list[str]
    next_action: str
```

Stage 2 (executor):
```python
class Step(BaseModel):
    interpretation: str = Field(description="How you interpret the next_action from the plan.")
    tool_to_call: Literal["search", "read", "edit", "run_tests"]
    tool_args: dict
```

Each stage has its own scratchpad, scoped to that stage's responsibility.

## Example 6: faion-cli SDD task execution

The pipeline state's per-task schema:
```python
class TaskExecution(BaseModel):
    plan_in_my_words: str   # scratchpad — re-states the task
    files_to_change: list[str]
    test_strategy: str
    final_diff_summary: str
```

`plan_in_my_words` re-grounds the model on the task spec; `files_to_change` is the agent's commitment; the rest follow.

## Example 7: Length-pegged scratchpad

```python
class Output(BaseModel):
    quick_thoughts_under_50_words: str
    answer: str
```

Useful when you DON'T want the model to over-think — bounding scratchpad to 50 words keeps the call cheap while still benefiting from CoT.

## Example 8: Tab-CoT for math

```python
class Step(BaseModel):
    operation: str
    intermediate: str

class Solution(BaseModel):
    steps: list[Step]
    final_answer: str
```

Each step has its own structured pair — operation + intermediate result. Forces the model to show its work in a parseable way that you can verify post-hoc.
