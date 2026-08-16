# Chain of Thought

## Summary

**One-sentence:** Chain-of-Thought prompting + extended thinking + self-consistency: when to use each, how to wire them, and how to keep CoT from leaking to the user.

**One-paragraph:** CoT elicits intermediate reasoning steps before final answers, improving multi-step accuracy. This methodology covers zero-shot CoT (prompt-only), few-shot CoT (with worked examples), extended-thinking modes (Claude / OpenAI o-series), and self-consistency sampling (vote across N reasonings). Includes practical guardrails: hide CoT from end-user, cap reasoning length, prevent the model leaking the system prompt as part of its «thinking».

**Ефективно для:** ML eng + prompt engineers, що бачать «модель дає поверхневі відповіді на 5-step problems» і потребують структурованого CoT-апгрейду.

## Applies If (ALL must hold)

- task requires multi-step reasoning (math, planning, logic)
- single-shot accuracy is the bottleneck
- you can afford 2-3x more output tokens
- you can hide CoT from end-user
- extended-thinking mode is available on the chosen model

## Skip If (ANY kills it)

- task is single-step (lookup, simple classification)
- latency / cost budget can't afford the extra tokens
- you need raw answer only and can't filter CoT
- model doesn't support CoT well (some sub-3B local models)

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case brief | text | Author / owner |
| Tier-manifest entry | JSON | `skills/tier-manifest.json` |
| Eval / fixture data (when applicable) | jsonl | Repo `tests/fixtures/` |
| Named approver | role:person | Org RACI |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/semantic-xml-content` | Authoring shape for `content/*.xml`. |
| `geek/ai/ml-engineer/ai-agent-patterns` | Pattern catalogue for agent loops referenced from this methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with statement + rationale + source | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for produces=code + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure with input / action / output / decision-gate | ~700 |
| `content/05-examples.xml` | medium | End-to-end worked example | ~500 |
| `content/06-decision-tree.xml` | essential | Root question + branches with `when` observables → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-step` | sonnet | Standard reasoning over the procedure / scoring axes. |
| `author-output` | sonnet | Produces the artefact in the shape `produces=code`. |
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-chain-of-thought.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-zero-shot.txt` | Zero-shot CoT prompt template |
| `templates/self-consistency.py` | Sample N + majority-vote helper |
| `templates/extended-thinking.py` | Claude / o-series extended-thinking call helper |
| `templates/strip-cot.py` | CoT-stripping helper for output filtering |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-chain-of-thought.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
- [[agents-production-deployment]] — production gates this methodology feeds into.
- external: rule rationales cite the sources in `content/01-core-rules.xml`.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-hide-cot`, `r2-bounded-thinking`, `r3-self-consistency-for-stakes`, `r4-cot-validated`, `r5-prompt-versioned` from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/prompt-zero-shot.txt`

```text
# Prompt Zero Shot
# Prompt skeleton for chain-of-thought.

SYSTEM: You are applying methodology `chain-of-thought`. Honour every rule in content/01-core-rules.xml.
USER: <task input>
ASSISTANT (expected shape): <see content/02-output-contract.xml>
```

### `templates/self-consistency.py`

```python
"""Skeleton for the `chain-of-thought` template `self-consistency.py` — fill the placeholders."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Skeleton:
    slug: str = "chain-of-thought"
    version: str = "1.1.0"
    owner: str = "role:person"
    approver: str = "role:person"

    def render(self) -> dict:
        return {
            "slug": self.slug,
            "version": self.version,
            "owner": self.owner,
            "approver": self.approver,
        }


if __name__ == "__main__":
    import json
    import sys
    sys.stdout.write(json.dumps(Skeleton().render(), indent=2) + "\n")
```

### `templates/extended-thinking.py`

```python
"""Skeleton for the `chain-of-thought` template `extended-thinking.py` — fill the placeholders."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Skeleton:
    slug: str = "chain-of-thought"
    version: str = "1.1.0"
    owner: str = "role:person"
    approver: str = "role:person"

    def render(self) -> dict:
        return {
            "slug": self.slug,
            "version": self.version,
            "owner": self.owner,
            "approver": self.approver,
        }


if __name__ == "__main__":
    import json
    import sys
    sys.stdout.write(json.dumps(Skeleton().render(), indent=2) + "\n")
```

### `templates/strip-cot.py`

```python
"""Skeleton for the `chain-of-thought` template `strip-cot.py` — fill the placeholders."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Skeleton:
    slug: str = "chain-of-thought"
    version: str = "1.1.0"
    owner: str = "role:person"
    approver: str = "role:person"

    def render(self) -> dict:
        return {
            "slug": self.slug,
            "version": self.version,
            "owner": self.owner,
            "approver": self.approver,
        }


if __name__ == "__main__":
    import json
    import sys
    sys.stdout.write(json.dumps(Skeleton().render(), indent=2) + "\n")
```
