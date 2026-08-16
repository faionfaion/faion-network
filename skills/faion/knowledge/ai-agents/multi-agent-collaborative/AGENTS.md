# Collaborative Agents with Shared Workspace

## Summary

**One-sentence:** Generates the implementation scaffold for a shared-workspace collaborative multi-agent pattern with capped iterations, independent synthesizer, and per-run token budget.

**One-paragraph:** Each agent in the group produces an initial contribution, then iteratively reads and builds on others' contributions recorded in a shared append-only workspace. After a hard-capped number of iterations a separate coordinator (different agent + ideally different model family) synthesizes the best elements from all contributions in a single call. This methodology ships the `CollaborativeGroup` Python class, the iteration prompt template, and a budget guard so the N×M call pattern cannot silently blow up cost.

**Ефективно для:** солопрейнера на креативних завданнях (strategy, design, narrative), де потрібна різноманітність точок зору, а одна модель збігається на власному prior.

## Applies If (ALL must hold)

- Creative or strategy work where genuinely diverse perspectives improve quality.
- Problem has no single correct answer; coverage matters more than convergence speed.
- Hard iteration cap and per-run token budget are acceptable (you can afford N×M LLM calls).
- Quality bar tolerates extra latency (5x-20x a single-agent call).
- Synthesizer can be an independent agent from the contributors.

## Skip If (ANY kills it)

- Latency budget < 30 s — collaborative pattern is the slowest of the multi-agent shapes.
- Task has a single correct answer — agents converge to the same answer (echo chamber) regardless of iteration count.
- Token budget is rigid (< 20k) — N×M call pattern blows budget faster than any other.
- Deterministic pipeline preferred — sequential is simpler and cheaper.
- Need fine-grained shared mutable state — workspace is append-only by design.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Validated multi-agent spec | YAML with `pattern: collaborative` | `multi-agent-basics` |
| Agent roster + system prompts | list of `{name, role, model, system_prompt}` | spec |
| Per-run token budget | int | `spec.budget.total_tokens` |
| Iteration cap | int (default 5) | spec |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/multi-agent-basics` | Upstream spec this implementation consumes. |
| `geek/ai/ai-agents/schema-version-pinning` | Workspace entries carry `schema_version` for evolvability. |
| `geek/ai/ai-agents/role-specialized-models` | Synthesizer should be on a different model family than contributors. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: capped iterations, budget guard after each round, independent synthesizer, append-only workspace, structured JSON contributions | ~750 |
| `content/02-output-contract.xml` | essential | JSON Schema for the `CollaborativeGroup` config + workspace entry shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: synthesizer-is-contributor, prompt inflation, no budget guard, all-same-model echo, race condition on workspace | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure: configure → run initial brainstorm → iterate (with budget check) → synthesize → emit trace | ~700 |
| `content/06-decision-tree.xml` | essential | Pick collaborative vs hierarchical vs debate based on convergence-needed vs coverage-needed | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Per-iteration contribution | sonnet | Reliable structured ideation; cheap enough for N×M calls. |
| Synthesizer | opus (or different family) | Final synthesis needs strongest reasoning; different family breaks echo. |
| Budget audit per iteration | haiku | Numeric check; not generative. |

## Templates

| File | Purpose |
|------|---------|
| `templates/collaborative_group.py` | Reference `CollaborativeGroup` class with shared workspace, iteration loop, budget guard, and independent synthesizer. |
| `templates/iteration-prompt.txt` | Per-round prompt showing agent its own last contribution + others' latest only (no full history) to prevent prompt inflation. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-agent-collaborative.py` | Validates a collaborative-group config against the contract (iteration cap, budget guard wired, synthesizer != contributor, structured workspace entries). | Pre-merge of any collaborative-pattern PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[multi-agent-basics]] — upstream spec.
- [[multi-agent-hierarchical]] — alternative when convergence > coverage.
- [[multi-agent-conversational]] — alternative for open-ended free-turn shape.
- [[role-specialized-models]] — pick synthesizer model.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides whether collaborative is the right pattern. Pick it when the task is open-ended with no single correct answer (creative/strategy/design); pick hierarchical when convergence + auditability matter more than coverage; pick debate when adversarial verification dominates. Run it before instantiating the class to avoid wrong-pattern cost.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/collaborative_group.py`

```python
"""Inject your own llm_client conforming to the LLMClient Protocol."""
from __future__ import annotations

import dataclasses
import datetime as dt
import json
from typing import Protocol


class LLMClient(Protocol):
    def generate(self, *, model: str, system: str, user: str) -> dict:  # returns {"text": str, "tokens_used": int}
        ...


@dataclasses.dataclass
class Contributor:
    name: str
    model: str
    system_prompt: str


@dataclasses.dataclass
class Synthesizer:
    name: str
    model: str


class CollaborativeGroup:
    """Append-only workspace + capped iterations + independent synthesizer."""

    def __init__(
        self,
        contributors: list[Contributor],
        synthesizer: Synthesizer,
        llm: LLMClient,
        max_iterations: int = 5,
        token_budget: int = 30_000,
    ) -> None:
        names = [c.name for c in contributors]
        if synthesizer.name in names:
            raise ValueError(f"synthesizer.name {synthesizer.name!r} must not be a contributor (rule r3)")
        if max_iterations < 1 or max_iterations > 10:
            raise ValueError("max_iterations must be in [1, 10] (rule r2)")
        if len(contributors) < 2:
            raise ValueError("need >=2 contributors")
        self.contributors = contributors
        self.synthesizer = synthesizer
        self.llm = llm
        self.max_iterations = max_iterations
        self.token_budget = token_budget
        self.workspace: list[dict] = []
        self.used = 0

    def _append(self, agent: str, iteration: int, content: str) -> None:
        self.workspace.append({
            "schema_version": "v1",
            "agent": agent,
            "iteration": iteration,
            "content": content,
            "ts": dt.datetime.utcnow().isoformat() + "Z",
        })

    def _latest_others(self, exclude: str) -> dict:
        latest: dict[str, dict] = {}
        for entry in self.workspace:
            if entry["agent"] != exclude:
                latest[entry["agent"]] = entry
        return latest

    def _budget_left(self) -> bool:
        return self.used < int(0.9 * self.token_budget)

    def run(self, task: str) -> dict:
        # Iteration 0 — initial brainstorm
        for c in self.contributors:
            if not self._budget_left():
                break
            r = self.llm.generate(model=c.model, system=c.system_prompt, user=f"Task: {task}\nProvide your initial idea.")
            self._append(c.name, 0, r["text"])
            self.used += r["tokens_used"]

        # Iterations 1..max
        aborted = False
        for it in range(1, self.max_iterations + 1):
            for c in self.contributors:
                if not self._budget_left():
                    aborted = True
                    break
                others = self._latest_others(c.name)
                # Latest-only context, capped serialization width
                others_view = json.dumps({k: v["content"][:600] for k, v in others.items()})[:3000]
                own_last = next((e for e in reversed(self.workspace) if e["agent"] == c.name), None)
                prompt = (
                    f"Task: {task}\n"
                    f"Your previous idea:\n{own_last['content'] if own_last else '(none yet)'}\n\n"
                    f"Others' latest:\n{others_view}\n\n"
                    "Build on these. Output strict JSON {idea, rationale, risk}."
                )
                r = self.llm.generate(model=c.model, system=c.system_prompt, user=prompt)
                self._append(c.name, it, r["text"])
                self.used += r["tokens_used"]
            if aborted:
                break

        # Synthesis — all latest entries, single call
        latest_per_agent = self._latest_others(exclude="")
        synth_user = json.dumps({k: v["content"] for k, v in latest_per_agent.items()})
        r = self.llm.generate(
            model=self.synthesizer.model,
            system="You are an independent synthesizer; merge best elements from all contributions.",
            user=f"Task: {task}\nContributions: {synth_user}\nReturn the best synthesized result.",
        )
        self.used += r["tokens_used"]

        return {
            "task": task,
            "workspace": self.workspace,
            "final_result": r["text"],
            "used_tokens": self.used,
            "aborted_early": aborted,
        }
```

### `templates/iteration-prompt.txt`

```text
Task:
{{TASK}}

Your previous idea (iteration {{LAST_ITERATION}}):
{{OWN_PREVIOUS_CONTENT}}

Other team members' LATEST ideas (one per agent):
{{OTHERS_LATEST_JSON}}

Build on these. Incorporate the strongest points from others; surface a counterpoint where you genuinely disagree.

Output STRICT JSON, no prose, no code fences:
{
  "idea": "<one-paragraph contribution>",
  "rationale": "<why this is the strongest direction>",
  "risk": "<one concrete failure mode>",
  "builds_on": ["<agent_name_1>", "<agent_name_2>"]
}
```
