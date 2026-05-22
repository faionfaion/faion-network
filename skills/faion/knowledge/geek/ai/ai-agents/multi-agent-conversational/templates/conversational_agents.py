#!/usr/bin/env python3
# purpose: AutoGen-style conversational multi-agent runner with sliding window + dual termination + budget audit.
# consumes: agents list, termination_phrase, max_turns, window_size, token_budget, llm_client.
# produces: conversation trace + final extraction.
# depends-on: any LLM client with `generate(model, system, user) -> {text, tokens_used}`.
# token-budget-impact: bounded by min(max_turns × per_turn_cost, token_budget); honor self.token_budget hard cap.
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
