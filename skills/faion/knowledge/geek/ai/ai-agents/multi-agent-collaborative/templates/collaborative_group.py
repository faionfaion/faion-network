#!/usr/bin/env python3
# purpose: Reference CollaborativeGroup for shared-workspace multi-agent ideation with capped iterations + budget guard.
# consumes: contributors[{name, model, system_prompt}], synthesizer{name, model}, token budget, max_iterations.
# produces: synthesized final_result + full workspace audit trail (append-only).
# depends-on: any LLM client that exposes `generate(model, system, user) -> {text, tokens_used}`; here typed as Protocol.
# token-budget-impact: N contributors × (1 + max_iterations) + 1 synthesis call; honor self.token_budget hard cap.
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
