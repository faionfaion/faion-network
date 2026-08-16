# Prompt Basics

## Summary

**One-sentence:** Pins prompt templates as code constants (PromptTemplate dataclass with system+user_template+examples) so prompt diffs are reviewable and silent regressions on model upgrades surface in CI.

**One-paragraph:** Core prompt engineering patterns: zero-shot, few-shot, chain-of-thought, self-consistency, ReAct. The PromptTemplate dataclass encapsulates system prompt, user template with variables, and optional few-shot examples. Core rule: store templates as code constants (not runtime strings) — this enables git diff and catches regressions when model versions update.

**Ефективно для:** AI/ML інженера, що автоматизує LLM-pipeline — закриває петлю між prompt design і deterministic, version-controlled call site.

## Applies If (ALL must hold)

- Any pipeline step requiring consistent, parseable LLM output.
- Before investing in fine-tuning — prompt engineering resolves most output consistency issues.
- Agent inner-loop outputs are unreliable or hallucinating.
- Setting up few-shot examples to teach a model a new output schema.
- Encoding role, constraints, and output format into a reusable PromptTemplate.

## Skip If (ANY kills it)

- Task complexity genuinely requires multi-step reasoning — use Chain-of-Thought or ReAct instead.
- Output schema must be guaranteed — use Structured Outputs with Pydantic.
- Token budget is the bottleneck — elaborate system prompts eat context; prefer short system + structured output.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task description | spec | upstream agent / human |
| Output format target | enum | downstream consumer schema |
| Few-shot examples | list[dict] | curated golden set |
| Model id | string | pipeline config |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/openai-chat-completions` | The PromptTemplate renders messages consumed by the SDK call. |
| `geek/ai/llm-integration/prompt-techniques` | Advanced patterns (CoT, ReAct) layered on top of PromptTemplate. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: code-constant templates, few-shot 3–5, explicit format, no injection, last-example weight | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for one rendered messages array; valid + invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair: drift, injection, runtime concat, vague task, no system | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure: define role+constraints → write user_template → add few-shot → render → call → diff | ~600 |
| `content/06-decision-tree.xml` | essential | Picks zero-shot vs few-shot vs CoT by task complexity and ambiguity | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-template` | sonnet | Per-task prompt authorship; balance precision with brevity. |
| `lint-template` | haiku | Mechanical check for placeholder usage and injection vectors. |
| `prompt-eval` | opus | Cross-call A/B and regression detection on prompt changes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-template.py` | PromptTemplate dataclass with system + user_template + few-shot examples and render() helper. |
| `templates/build-system.py` | build_system() builder composing role + constraints + output_format. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prompt-basics.py` | Validate a rendered-messages JSON record matches the output contract. | Post-render in pipeline; CI on every prompt change. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[prompt-techniques]] — advanced patterns (CoT, self-consistency, ReAct).
- [[openai-chat-completions]] — downstream consumer of rendered messages.
- [[structured-output-basics]] — when prompts alone cannot enforce schema.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks (a) zero-shot vs few-shot by task ambiguity (≥2 valid outputs per input → few-shot), (b) inline vs CoT by reasoning depth (≥3 steps → CoT), and (c) injection-safe rendering when any field comes from user input. Use it before authoring any new template.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/prompt-template.py`

```python
"""
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class PromptTemplate:
    system: str
    user_template: str
    examples: List[Dict[str, str]] = field(default_factory=list)
    version: str = "v1"

    def render(self, **kwargs) -> List[Dict[str, str]]:
        """Render the template into a messages array ready for any OpenAI-compatible API."""
        msgs: List[Dict[str, str]] = [{"role": "system", "content": self.system}]
        for ex in self.examples:
            msgs.append({"role": "user", "content": ex["input"]})
            msgs.append({"role": "assistant", "content": ex["output"]})
        msgs.append({"role": "user", "content": self.user_template.format(**kwargs)})
        return msgs


# Example: zero-shot extraction
EXTRACT_JSON = PromptTemplate(
    system="Extract the requested fields. Return only valid JSON, no prose.",
    user_template='Text: {text}\n\nReturn: {{"sentiment": str, "topics": [str]}}',
    version="extract-v1",
)
```

### `templates/build-system.py`

```python
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
```
