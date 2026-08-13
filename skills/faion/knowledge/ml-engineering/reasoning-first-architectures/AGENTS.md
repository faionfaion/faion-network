# Reasoning-First Architectures

## Summary

**One-sentence:** Cost-aware routing pattern that escalates only multi-step / verification-heavy tasks to reasoning models (o3, Claude Extended Thinking, DeepSeek R1) with explicit thinking budgets, while standard models handle the simple majority.

**One-paragraph:** Reasoning models scale test-time compute for breakthroughs on hard tasks (o3 hits 83.3% AIME vs 13.4% GPT-4o) but cost 10-50× more per call. Treating every task as a reasoning task burns budget without quality gain on simple retrievals. This methodology pins the contract: a cheap classifier routes incoming tasks to {standard, reasoning} based on task-type, an eval proves the reasoning route actually outperforms the standard route on a labelled set, a thinking budget is set per task-type bucket (1K–128K depending on depth), and downstream irreversible actions sit behind human review when reasoning confidence drops. Output: a versioned `reasoning-routing.yaml` consumed by the orchestrator.

**Ефективно для:**

- Multi-step math / formal proof / theorem задач — reasoning моделі дають 6× quality lift на AIME-class задачах де standard models валяться.
- Code review з обовʼязковим self-verification — Extended Thinking ловить edge cases які SFT моделі пропускають.
- Research synthesis із competing hypotheses — reasoning room for thought бачить trade-offs.
- Cost-sensitive продуктів — eval-proven routing тримає 80% калів на cheap path і дорогі тільки коли потрібно.

## Applies If (ALL must hold)

- Workload contains ≥1 task class where reasoning depth materially affects correctness (math, code-verify, planning)
- Budget for reasoning-model inference is provisioned OR a fall-through to standard is acceptable
- A 50-100 example eval set exists to calibrate routing thresholds
- Orchestrator can intercept the request and call different model providers

## Skip If (ANY kills it)

- Simple retrieval / lookup workloads only — CoT adds latency with no quality lift
- High-throughput classification (thousands of calls per minute) — reasoning latency breaks the SLO
- Creative writing as primary use case — explicit reasoning constrains output quality
- Real-time streaming UX — reasoning tokens delay first-token, break UX

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `task-sample-labelled.jsonl` | JSONL `{task, type, expected, hard?: bool}` | log analysis + SME |
| `model-rate-cards.yaml` | YAML | provider pricing as of last review |
| `latency-budget.yaml` | YAML | product SLO per task class |
| `eval-set-routing.jsonl` | JSONL | ≥50 examples mixed across task types |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/cost-optimization` | Per-model cost vocabulary |
| `geek/ai/ml-engineer/model-evaluation` | Eval discipline that gates the routing decision |
| `geek/ai/ml-engineer/llm-decision-framework` | Provider selection backdrop |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: eval-before-spend, task-type budget, classifier-first, human-gate on irreversible, fall-through-on-budget-cap | 1100 |
| `content/02-output-contract.xml` | essential | `reasoning-routing.yaml` schema with classes + budgets + fallback | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: blanket reasoning, unset budget, no eval gate, streaming broken, missing fall-through | 900 |
| `content/04-procedure.xml` | essential | 6 steps: cluster tasks → label hard set → eval routing → set budgets → wire fall-through → ship | 800 |
| `content/05-examples.xml` | essential | Worked example: code-review router escalates only to Extended Thinking when hard | 600 |
| `content/06-decision-tree.xml` | essential | Routes by task-type to standard / Extended Thinking / o3 / DeepSeek R1 with budget per node | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `task_class_inference` | haiku | Lightweight classifier; runs per request |
| `eval_routing_decision` | sonnet | Compare reasoning vs standard outputs across labelled set |
| `budget_calibration_drafter` | opus | Picks budget per type using eval data; needs depth |
| `routing_yaml_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/extended-thinking.py` | Anthropic Extended Thinking call with budget parameter |
| `templates/prompt-reasoning.txt` | System prompt asking model to verify before answering |
| `templates/reasoning-routing.schema.yaml` | Schema for the routing spec |
| `templates/_smoke-test.yaml` | Minimum-viable routing spec |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-reasoning-first-architectures.py` | Lint reasoning-routing.yaml against schema + rules | Pre-commit + pre-deploy |

## Related

- [[cost-optimization]] — per-model rate cards
- [[tool-use-function-calling]] — reasoning models often gate tool-call decisions
- external: [Anthropic Extended Thinking](https://docs.anthropic.com/claude/docs/extended-thinking) · [OpenAI o-series](https://openai.com/index/introducing-o3/) · [DeepSeek R1](https://github.com/deepseek-ai/DeepSeek-R1)

## Decision tree

See `content/06-decision-tree.xml`. Routes a task by inferred type and difficulty score to one of {standard, Extended Thinking, o4-mini, o3, DeepSeek R1} with a thinking-budget envelope per node.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/extended-thinking.py`

```python
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
```

### `templates/prompt-reasoning.txt`

```text
You are a careful reasoning assistant. For every task:

1. ANALYZE: Break the problem into parts. Identify what is known, what is unknown, and what assumptions you are making.

2. REASON: Work through each part step by step. Show your intermediate conclusions. If you encounter a contradiction, flag it explicitly.

3. VERIFY: Before giving your final answer, check:
   - Does the answer satisfy all the stated requirements?
   - Are there edge cases or exceptions you haven't considered?
   - Is there a simpler alternative that achieves the same result?

4. ANSWER: Give a clear, direct final answer. Separate it from your reasoning with "FINAL ANSWER:".

Important:
- Do not skip steps. The value is in the explicit reasoning chain.
- Do not express false confidence. If uncertain, say "I'm not certain, but..." and explain why.
- Do not take irreversible actions without explicitly confirming with the user first.
- If the task is ambiguous, state your interpretation before proceeding.

Task: {task}
```

### `templates/reasoning-routing.schema.yaml`

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required: [version, classifier, task_types, eval_evidence, budget_cap, human_gate]
properties:
  version: { type: string, pattern: "^\\d+\\.\\d+\\.\\d+$" }
  classifier:
    type: object
    required: [model, prompt_version, confidence_field]
  task_types:
    type: object
    minProperties: 2
    additionalProperties:
      type: object
      required: [route, thinking_budget, standard_fallback]
      properties:
        route: { type: string, enum: [standard, extended-thinking, o3, o4-mini, deepseek-r1] }
        thinking_budget: { type: integer, minimum: 0, maximum: 131072 }
        standard_fallback:
          type: object
          required: [model, trigger]
  eval_evidence:
    type: object
    required: [set_path, sample_size, reasoning_lift]
    properties:
      sample_size: { type: integer, minimum: 50 }
      reasoning_lift:
        type: object
        additionalProperties: { type: number }
  budget_cap:
    type: object
    required: [monthly_usd, on_cap_hit]
    properties:
      monthly_usd: { type: number, minimum: 0 }
      on_cap_hit: { type: string, enum: [fall-through, fail] }
  human_gate:
    type: object
    required: [enabled, actions, confidence_floor]
    properties:
      enabled: { type: boolean }
      actions: { type: array, items: { type: string } }
      confidence_floor: { type: number, minimum: 0, maximum: 1 }
```

### `templates/_smoke-test.yaml`

```yaml
version: 1.0.0
classifier:
  model: claude-haiku
  prompt_version: cr-classifier-v3
  confidence_field: difficulty_score
task_types:
  code_review_simple:
    route: standard
    thinking_budget: 0
    standard_fallback: {model: claude-sonnet-4-5, trigger: always}
  code_review_hard:
    route: extended-thinking
    thinking_budget: 8192
    standard_fallback: {model: claude-sonnet-4-5, trigger: provider_unhealthy}
eval_evidence:
  set_path: evals/cr-routing-2026-05.jsonl
  sample_size: 78
  reasoning_lift: {code_review_hard: 0.18}
budget_cap:
  monthly_usd: 3500
  on_cap_hit: fall-through
human_gate:
  enabled: true
  actions: [deploy, db-migration]
  confidence_floor: 0.65
```
