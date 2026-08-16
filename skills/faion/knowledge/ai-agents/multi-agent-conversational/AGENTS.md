# AutoGen-Style Conversational Multi-Agent Pattern

## Summary

**One-sentence:** Generates an AutoGen-style conversational multi-agent runner with capped sliding-window context, dual termination (phrase + max_turns), and per-turn budget audit.

**One-paragraph:** Two or more agents take sequential turns in a free-form conversation. Each agent receives a sliding window of recent turns (default last 3) plus the previous message, produces a reply, and the loop continues until a termination phrase appears or `max_turns` is reached. The pattern matches the AutoGen GroupChat / v0.4 event-driven core for tasks where the approach cannot be decomposed upfront — interactive debugging, negotiation, Socratic verification. This methodology ships a `ConversationalAgents` class with both guards wired and a per-turn token audit.

**Ефективно для:** інженера, який запускає інтерактивний дебаг / Socratic-перевірку — конверсація замість заздалегідь зафіксованого пайплайну.

## Applies If (ALL must hold)

- Dynamic task where approach cannot be decomposed upfront (debugging, negotiation, Socratic).
- Adversarial verification — one agent proposes, another critiques, conversation converges.
- Open-ended exploration where the conversation path itself is the output.
- Agents need to negotiate a shared understanding before acting.
- A semantic termination signal can be defined (phrase, JSON flag, or output-shape check).

## Skip If (ANY kills it)

- Task has a known sequential pipeline — use `sequential` or `hierarchical` instead.
- Production audit requires structured per-step decision logs — conversational turns are harder to parse.
- Latency budget tight — free-form runs always risk hitting `max_turns`.
- Agents need shared mutable state beyond message history — use `collaborative` workspace pattern.
- Two agents on identical model + identical system prompt — degenerates to monologue.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Validated multi-agent spec | YAML with `pattern: conversational` | `multi-agent-basics` |
| Agent roster (≥2) | list of `{name, model, system_prompt}` | spec |
| `termination_phrase` | string (e.g. `"TASK COMPLETE"`) | spec.termination |
| `max_turns` | int (≤30) | spec.termination |
| Per-turn token budget | int | spec.budget |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/multi-agent-basics` | Upstream spec. |
| `geek/ai/ai-agents/schema-version-pinning` | Turn entries carry `schema_version`. |
| `geek/ai/ai-agents/record-replay-debugging` | Conversation traces feed into record/replay. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: dual termination, sliding window cap, termination check on output, per-turn budget audit, distinct identities | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for `ConversationalAgents` config + turn entry shape | ~650 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: missing phrase, missing max_turns, full-history prompt, identical agents, no budget audit | ~700 |
| `content/04-procedure.xml` | medium | 5-step build: config → start → turn loop with checks → emit trace → final extraction | ~700 |
| `content/06-decision-tree.xml` | essential | Pick conversational vs sequential vs hierarchical from decomposability and audit needs | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Per-turn response | sonnet | Reliable structured turn generation. |
| Critique role (adversarial) | opus or different family | Stronger reasoning to surface objections; different family breaks echo. |
| Termination detector | haiku | Cheap string + shape check on each output. |

## Templates

| File | Purpose |
|------|---------|
| `templates/conversational_agents.py` | Reference runner with sliding window, dual termination, per-turn audit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-agent-conversational.py` | Validates a conversational config (dual termination present, max_turns ≤30, sliding window cap set, distinct identities). | Pre-merge of any conversational-pattern PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[multi-agent-basics]] — upstream spec.
- [[multi-agent-hierarchical]] — alternative when you have a plan.
- [[multi-agent-collaborative]] — alternative for parallel ideation.
- [[record-replay-debugging]] — replay conversational traces deterministically.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides whether conversational beats sequential/hierarchical: pick conversational when the path is unknowable upfront AND audit can tolerate prose turns. Otherwise pick sequential (known DAG) or hierarchical (manager + workers). Run it before scaffolding to avoid wrong-pattern cost.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/conversational_agents.py`

```python
from __future__ import annotations

import dataclasses
import datetime as dt
import json
from typing import Protocol


class LLMClient(Protocol):
    def generate(self, *, model: str, system: str, user: str) -> dict:
        ...


@dataclasses.dataclass
class Agent:
    name: str
    model: str
    system_prompt: str


class ConversationalAgents:
    def __init__(
        self,
        agents: list[Agent],
        llm: LLMClient,
        termination_phrase: str,
        max_turns: int = 12,
        window_size: int = 3,
        token_budget: int = 20_000,
    ) -> None:
        if len(agents) < 2:
            raise ValueError("need >=2 agents")
        if len({a.name for a in agents}) != len(agents):
            raise ValueError("agent names must be unique")
        if len({a.system_prompt for a in agents}) != len(agents):
            raise ValueError("agent system_prompts must be distinct (rule r5)")
        if not termination_phrase or len(termination_phrase) < 3:
            raise ValueError("termination_phrase required, >=3 chars (rule r1)")
        if not (2 <= max_turns <= 30):
            raise ValueError("max_turns must be in [2,30] (rule r2)")
        if not (1 <= window_size <= 8):
            raise ValueError("window_size must be in [1,8] (rule r3)")
        self.agents = agents
        self.llm = llm
        self.term = termination_phrase
        self.max_turns = max_turns
        self.window = window_size
        self.token_budget = token_budget

    def run(self, initial_message: str) -> dict:
        log: list[dict] = [{
            "schema_version": "v1", "speaker": "user", "content": initial_message,
            "ts": dt.datetime.utcnow().isoformat() + "Z",
        }]
        used = 0
        exit_reason = "max_turns"
        for turn in range(1, self.max_turns + 1):
            speaker = self.agents[(turn - 1) % len(self.agents)]
            window = log[-self.window :]
            user_payload = "\n".join(f"[{e['speaker']}] {e['content']}" for e in window)
            user_payload += f"\n\nReply as {speaker.name}. End with '{self.term}' when the task is solved."
            r = self.llm.generate(model=speaker.model, system=speaker.system_prompt, user=user_payload)
            log.append({
                "schema_version": "v1", "speaker": speaker.name,
                "content": r["text"], "tokens_used": r["tokens_used"],
                "ts": dt.datetime.utcnow().isoformat() + "Z",
            })
            used += r["tokens_used"]
            if self.term in r["text"]:
                exit_reason = "phrase"
                break
            if used >= int(0.9 * self.token_budget):
                exit_reason = "budget"
                break

        final = None
        if exit_reason == "phrase":
            tail = log[-1]["content"]
            final = tail.split(self.term, 1)[0].strip()
        else:
            final = log[-1]["content"]

        return {
            "log": log, "used_tokens": used, "exit_reason": exit_reason,
            "aborted_early": exit_reason == "budget", "final_result": final,
        }


if __name__ == "__main__":
    # smoke shape — caller injects a real LLMClient.
    print(json.dumps({"hint": "import ConversationalAgents and inject llm"}, indent=2))
```
