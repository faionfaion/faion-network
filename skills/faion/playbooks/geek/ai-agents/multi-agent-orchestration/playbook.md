---
name: multi-agent-orchestration
description: Wire fan-out, supervisor, and pipeline patterns into a production multi-agent system using the Anthropic Python SDK and asyncio.
tier: geek
group: ai-agents
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working Python implementation of three orchestration patterns — fan-out (parallel sub-agents with gather), supervisor (orchestrator decomposes a goal and reduces worker results), and pipeline (sequential stage-to-stage hand-off) — using the Anthropic Python SDK, with a decision tree to pick the right pattern and a worked research-summarize-publish example that ties all three together.

## Prerequisites

- Python 3.11+, `anthropic>=0.49`, `pydantic>=2.7` installed (`pip install anthropic pydantic`).
- An `ANTHROPIC_API_KEY` environment variable set.
- Familiarity with Python `asyncio` (`asyncio.gather`, `async def`, `await`).
- Understanding of Anthropic model tiers: `claude-opus-4-7` (orchestrators/judges), `claude-sonnet-4-6` (supervisors/workers), `claude-haiku-4-5-20251001` (cheap fan-out leaves).
- Rate-limit headroom: fan-out caps at 20 concurrent calls; ensure your API tier supports it.

## Steps

### 1. Choose the right pattern with the decision tree

Before writing code, classify the work:

```
Are sub-tasks independent of each other at runtime?
  YES → Are they all known upfront?
         YES → Fan-out (parallel gather)
         NO  → Fan-out with dynamic dispatch
  NO  → Does the task require goal decomposition by an orchestrator?
          YES → Supervisor (orchestrator + workers + reducer)
          NO  → Is there a fixed sequence of transforms?
                  YES → Pipeline (sequential stage hand-off)
                  NO  → Hybrid (supervisor wrapping a pipeline)
```

Rules of thumb:
- Parallel-independent subtasks with no ordering dependency → fan-out.
- Goal decomposition where the orchestrator cannot know subtasks upfront → supervisor.
- Multi-stage document transform (ingest → enrich → format → publish) → pipeline.

### 2. Implement the base agent call

All three patterns share one building block: a single async call to a named agent.

```python
import asyncio
import os
from anthropic import AsyncAnthropic
from pydantic import BaseModel

client = AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


async def call_agent(
    role: str,
    instructions: str,
    user_message: str,
    model: str = "claude-sonnet-4-6",
) -> str:
    """Call a single named agent and return its text reply."""
    response = await client.messages.create(
        model=model,
        max_tokens=2048,
        system=f"You are a {role}. {instructions}",
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text
```

### 3. Build the fan-out pattern

Fan-out maps N independent items to N parallel agent calls, then gathers results. Use `asyncio.gather` with a concurrency semaphore capped at 20.

```python
async def fan_out(
    items: list[str],
    role: str,
    instructions: str,
    model: str = "claude-haiku-4-5-20251001",
    max_concurrency: int = 20,
) -> list[str]:
    """Run one agent call per item in parallel, bounded by max_concurrency."""
    sem = asyncio.Semaphore(max_concurrency)

    async def bounded_call(item: str) -> str:
        async with sem:
            return await call_agent(role, instructions, item, model=model)

    return list(await asyncio.gather(*[bounded_call(item) for item in items]))


# Usage: score 15 research snippets in parallel
async def score_snippets(snippets: list[str]) -> list[str]:
    return await fan_out(
        items=snippets,
        role="relevance scorer",
        instructions=(
            "Score the relevance of this research snippet on a scale 1-10. "
            "Reply with JSON: {\"score\": <int>, \"reason\": \"<one sentence>\"}."
        ),
    )
```

Key constraints:
- Cap at 20 concurrent calls — above that, rate-limit tail latency dominates.
- Every branch must be idempotent: same input → same output, no shared mutable state written inside a branch.
- Collect all results before synthesizing; do not process the first result that arrives.

### 4. Build the supervisor pattern

The supervisor orchestrator decomposes a goal into a JSON assignment plan, dispatches each subtask to the right specialist worker, and reduces results into a final output.

```python
import json
from pydantic import BaseModel


class Assignment(BaseModel):
    worker: str
    task: str
    context: str


class AssignmentPlan(BaseModel):
    assignments: list[Assignment]


WORKER_REGISTRY: dict[str, tuple[str, str]] = {
    "researcher": (
        "research specialist",
        "Gather facts and return structured JSON: {\"findings\": [...], \"confidence\": 0-1}.",
    ),
    "analyst": (
        "data analyst",
        "Analyse findings and return JSON: {\"insights\": [...], \"risks\": [...]}.",
    ),
    "writer": (
        "content writer",
        "Turn insights into a polished paragraph. Return plain text.",
    ),
}


async def supervisor(goal: str) -> str:
    """Decompose goal, dispatch workers, reduce to final answer."""
    # Step 1: orchestrator decomposes the goal
    plan_raw = await call_agent(
        role="task orchestrator",
        instructions=(
            "Decompose the user goal into subtasks. "
            f"Available workers: {list(WORKER_REGISTRY.keys())}. "
            "Reply with JSON matching schema: "
            "{\"assignments\": [{\"worker\": \"<name>\", \"task\": \"<task>\", \"context\": \"<context>\"}]}. "
            "No extra keys. Workers do not communicate — pass all needed context in each assignment."
        ),
        user_message=goal,
        model="claude-opus-4-7",
    )

    plan = AssignmentPlan.model_validate_json(plan_raw)

    # Step 2: dispatch each assignment to its worker
    worker_results: dict[str, str] = {}
    for assignment in plan.assignments:
        role, instructions = WORKER_REGISTRY[assignment.worker]
        result = await call_agent(
            role=role,
            instructions=instructions,
            user_message=f"Task: {assignment.task}\nContext: {assignment.context}",
            model="claude-sonnet-4-6",
        )
        worker_results[assignment.worker] = result

    # Step 3: orchestrator reduces all results
    reduction_input = json.dumps(worker_results, ensure_ascii=False, indent=2)
    final = await call_agent(
        role="synthesis orchestrator",
        instructions="Synthesize the worker outputs into one coherent final answer.",
        user_message=f"Goal: {goal}\n\nWorker results:\n{reduction_input}",
        model="claude-opus-4-7",
    )
    return final
```

### 5. Build the pipeline pattern

A pipeline hands context from one stage to the next in a fixed sequence. Each stage receives the previous stage's output as its input.

```python
from dataclasses import dataclass


@dataclass
class PipelineStage:
    name: str
    role: str
    instructions: str
    model: str = "claude-sonnet-4-6"


async def run_pipeline(stages: list[PipelineStage], initial_input: str) -> dict[str, str]:
    """Execute stages in order; each stage receives the previous output."""
    context = initial_input
    history: dict[str, str] = {"_input": initial_input}

    for stage in stages:
        context = await call_agent(
            role=stage.role,
            instructions=stage.instructions,
            user_message=context,
            model=stage.model,
        )
        history[stage.name] = context

    return history


# Research-summarize-publish pipeline definition
PUBLISH_PIPELINE = [
    PipelineStage(
        name="research",
        role="research specialist",
        instructions=(
            "Search your knowledge for relevant facts about the topic. "
            "Return a structured list of findings: bullet points, each ≤2 sentences."
        ),
        model="claude-sonnet-4-6",
    ),
    PipelineStage(
        name="summarize",
        role="editorial summarizer",
        instructions=(
            "Condense the research findings into a 3-paragraph summary for a technically literate audience. "
            "Be concrete; avoid vague language."
        ),
        model="claude-sonnet-4-6",
    ),
    PipelineStage(
        name="publish_format",
        role="publication formatter",
        instructions=(
            "Format the summary as a Markdown article: one H1 title, three body paragraphs, "
            "a bullet-list TL;DR at the end. Return only the Markdown."
        ),
        model="claude-haiku-4-5-20251001",
    ),
]
```

### 6. Compose the worked example: research-summarize-publish flow

This example uses all three patterns: fan-out to gather multi-source research in parallel, supervisor to decompose and analyse, pipeline to format and publish.

```python
async def research_summarize_publish(topic: str) -> str:
    """
    Full research-summarize-publish flow.

    1. Fan-out: gather research from N angles in parallel.
    2. Supervisor: analyse gathered research, produce insights.
    3. Pipeline: summarize → format → ready-to-publish Markdown.
    """
    # Stage 1: fan-out research across multiple angles
    angles = [
        f"Technical architecture of {topic}",
        f"Real-world adoption and case studies of {topic}",
        f"Known failure modes and anti-patterns in {topic}",
        f"Current tooling ecosystem for {topic} as of 2026",
    ]
    raw_research = await fan_out(
        items=angles,
        role="research specialist",
        instructions="Return 3-5 bullet-point findings. Be factual and specific.",
        model="claude-haiku-4-5-20251001",
    )
    combined_research = "\n\n".join(
        f"### {angle}\n{result}" for angle, result in zip(angles, raw_research)
    )

    # Stage 2: supervisor analyses the gathered research
    analysis = await supervisor(
        goal=(
            f"Analyse the following research about '{topic}' and produce: "
            "(a) key insights, (b) risks, (c) a one-paragraph executive summary.\n\n"
            f"{combined_research}"
        )
    )

    # Stage 3: pipeline formats the analysis into publishable Markdown
    pipeline_result = await run_pipeline(
        stages=PUBLISH_PIPELINE,
        initial_input=analysis,
    )

    return pipeline_result["publish_format"]


if __name__ == "__main__":
    result = asyncio.run(
        research_summarize_publish("multi-agent orchestration with the Anthropic SDK")
    )
    print(result)
```

### 7. Add timeouts and error handling

Wrap every `call_agent` invocation in a timeout. A single hanging sub-agent should not stall the whole pipeline.

```python
import asyncio
from anthropic import APIError


async def call_agent_with_timeout(
    role: str,
    instructions: str,
    user_message: str,
    model: str = "claude-sonnet-4-6",
    timeout_s: float = 60.0,
) -> str:
    try:
        return await asyncio.wait_for(
            call_agent(role, instructions, user_message, model),
            timeout=timeout_s,
        )
    except asyncio.TimeoutError:
        return f'{{"error": "timeout", "role": "{role}"}}'
    except APIError as exc:
        return f'{{"error": "api_error", "status": {exc.status_code}, "role": "{role}"}}'
```

Replace all `call_agent(...)` calls in fan-out, supervisor, and pipeline with `call_agent_with_timeout(...)`. Default `timeout_s=60` for Haiku leaves, `timeout_s=120` for Opus orchestrators.

## Verify

Run the end-to-end example and confirm the output is valid Markdown:

```bash
python -c "
import asyncio, sys
sys.path.insert(0, '.')
from playbook import research_summarize_publish
result = asyncio.run(research_summarize_publish('multi-agent orchestration'))
assert result.strip().startswith('#'), f'Expected Markdown H1, got: {result[:80]}'
print('PASS — output starts with H1')
print(result[:400])
"
```

Expected output: `PASS — output starts with H1` followed by the first 400 chars of the article.

For fan-out specifically, verify parallelism is actually happening:

```python
import time, asyncio
from playbook import fan_out

async def verify_fanout():
    start = time.perf_counter()
    results = await fan_out(
        items=[f"item-{i}" for i in range(5)],
        role="echo agent",
        instructions="Reply with: ECHO <input>.",
    )
    elapsed = time.perf_counter() - start
    assert len(results) == 5, "Expected 5 results"
    print(f"Fan-out 5 calls in {elapsed:.2f}s (serial would be ~5x single call)")

asyncio.run(verify_fanout())
```

If `elapsed` is close to `5 × single_call_time`, the semaphore is too tight or the model is rate-limiting — reduce fan-out batch size.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `asyncio.TimeoutError` on Opus orchestrator calls | Default 60 s timeout too short for complex decomposition | Increase `timeout_s=120` for Opus; use Sonnet if latency matters more than quality |
| Fan-out returns fewer results than items | `asyncio.gather` swallows exceptions by default | Pass `return_exceptions=True` to `asyncio.gather`, then filter for `Exception` instances |
| Supervisor `AssignmentPlan.model_validate_json` raises `ValidationError` | Orchestrator returned non-JSON prose | Add retry with explicit JSON reminder: "You MUST reply with valid JSON only, no prose." |
| Pipeline stage output is empty | Model returned an empty response for the stage | Add a non-empty assertion after each stage; log the stage name and truncated input for debugging |
| Rate limit `429` errors during fan-out | Too many concurrent requests on the API tier | Reduce `max_concurrency` from 20 to 10, or move to Anthropic Batch API for N > 50 |
| Supervisor worker receives incomplete context | Orchestrator sent only a summary, not full prior output | In the assignment plan instructions, explicitly state: "Pass all context each worker needs; workers are stateless" |
| Pipeline stage produces wrong format | Model ignores formatting instructions | Use structured output with `claude-sonnet-4-6` extended thinking or add format validation after each stage |

## Next

- Add observability: log every agent call with `time.perf_counter()`, model ID, token count from `response.usage`, and truncated input/output — without this, debugging production failures is guesswork.
- Graduate fan-out to Anthropic Batch API for N > 50 items with no real-time deadline (50% cost reduction, no rate-limit risk).
- Extend the supervisor with a human-in-the-loop gate: before dispatching irreversible actions (send email, post to API), surface the plan for explicit approval.

## References

- [knowledge/geek/ai/ai-agents/multi-agent-basics](../../../knowledge/geek/ai/ai-agents/multi-agent-basics) — coordination pattern taxonomy (sequential, parallel, hierarchical) that backs the decision tree in Step 1 and the worker registry design in Step 4.
- [knowledge/geek/ai/ai-agents/multi-agent-design-patterns](../../../knowledge/geek/ai/ai-agents/multi-agent-design-patterns) — Parallel Fan-Out/Gather and Hierarchical Decomposition formal definitions that Steps 3 and 4 implement directly.
- [knowledge/geek/ai/ai-agents/multi-agent-hierarchical](../../../knowledge/geek/ai/ai-agents/multi-agent-hierarchical) — manager-worker delegation contract (stateless workers, manager holds full context) applied in the supervisor's dispatch loop in Step 4.
- [knowledge/geek/ai/ai-agents/map-reduce-send-fanout](../../../knowledge/geek/ai/ai-agents/map-reduce-send-fanout) — bounded concurrency rule (≤20 branches, idempotent leaves, reducer annotation) that governs the `asyncio.Semaphore` cap and gather semantics in Step 3.
