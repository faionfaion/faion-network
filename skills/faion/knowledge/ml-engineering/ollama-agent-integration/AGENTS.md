# Ollama Agent Integration

## Summary

**One-sentence:** Wires a local Ollama model into a LangChain, LlamaIndex, or custom agent loop with tool calling, structured output, and streaming support.

**One-paragraph:** Wires a local Ollama model into a LangChain, LlamaIndex, or custom agent loop with tool calling, structured output, and streaming support. The methodology assumes the inputs in Prerequisites and produces a `code` artefact validated by `scripts/validate-ollama-agent-integration.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** Developers building privacy-preserving agents that run entirely on local Ollama models without cloud LLM dependencies.

## Applies If (ALL must hold)

- Existing OpenAI-based agent code that needs to run against local models for privacy or cost.
- Any extraction or classification sub-agent where input data must not leave the machine.
- Local test agents in CI pipelines that mock cloud LLM behavior without API costs.
- Agent prototyping before committing to cloud provider pricing.
- Hybrid local/cloud setups where the agent uses the best available endpoint.

## Skip If (ANY kills it)

- Best-quality responses required for complex reasoning — even 70B local models trail frontier cloud models.
- Multilingual tasks across more than 20 languages — local models lag cloud providers significantly.
- Fine-tuned custom behavior needed but GPU for fine-tuning is unavailable.
- Real-time latency requirements on small hardware — CPU inference is 5-20x slower than GPU.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[ollama-python-client]]` | Adjacent context the agent normally already has when this methodology fires. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules with rationale and source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples for the output artefact. | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix. | ~800 |
| `content/04-procedure.xml` | medium | Five-step procedure with decision-gates. | ~700 |
| `content/05-examples.xml` | medium | One end-to-end worked example. | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether the methodology applies, ending in rule refs. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `generate-skeleton` | sonnet | Boilerplate + schema scaffolding. |
| `fill-business-logic` | opus | Domain-judgment-heavy core logic. |
| `lint-and-test` | haiku | Mechanical checks against the contract. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.py` | Minimum-viable filled-in example used by the validator self-test. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ollama-agent-integration.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ollama-python-client]]
- [[ollama-tool-calling]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `ollama-agent-integration` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/_smoke-test.py`

```python
"""ollama-agent-integration smoke-test fixture — minimum viable filled-in instance."""
from __future__ import annotations

SMOKE = {
    "slug": "ollama-agent-integration",
    "version": "1.0.0",
    "date": "2026-05-22",
    "produces": "code",
    "payload": {
        "language": "python",
        "entry_point": "skeleton.py",
        "files": [{"path": "skeleton.py", "purpose": "main module"}],
    },
    "forbidden_seen": [],
}
```
