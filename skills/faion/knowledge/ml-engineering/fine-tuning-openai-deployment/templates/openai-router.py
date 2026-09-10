"""
purpose: Router that splits traffic between base and fine-tune by percentage.
consumes: see AGENTS.md ## Prerequisites
produces: playbook-step
depends-on: content/02-output-contract.xml schema for fine-tuning-openai-deployment
token-budget-impact: ≤500 tokens to fill
"""
# Usage:
#   export OPENAI_API_KEY=...            # read by the openai client
#   export MODEL_REGISTRY_PATH=infra/model-id-registry.yaml
#   router = ModelRouter()
#   reply = router.chat(messages, sticky_key=user_id)
# Ramp = edit rollout.pct in the registry and commit; the router re-reads on
# mtime change. Rollback = pct: 0. No model_id is ever written in this file.
# Requires: pip install openai>=1.0 pyyaml

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from pathlib import Path

import yaml
from openai import OpenAI, OpenAIError

log = logging.getLogger("model-router")


class ModelRouter:
    def __init__(self, registry_path: str | None = None, client: OpenAI | None = None) -> None:
        self.path = Path(registry_path or os.environ["MODEL_REGISTRY_PATH"])
        self.client = client or OpenAI()
        self._mtime = 0.0
        self._reload()

    # r5-model-id-version-controlled: model IDs come from the registry file only.
    def _reload(self) -> None:
        mtime = self.path.stat().st_mtime
        if mtime == self._mtime:
            return
        reg = yaml.safe_load(self.path.read_text(encoding="utf-8"))
        entry = reg["models"][reg["active"]]
        gate = entry.get("eval_gate", {})
        pct = int(entry.get("rollout", {}).get("pct", 0))
        # r1-eval-gate-required: an un-gated entry is served at 0% no matter what pct says.
        if pct > 0 and gate.get("passed") is not True:
            log.error("registry entry %s has no passed eval gate; forcing pct=0", reg["active"])
            pct = 0
        self.base_model = reg["base_model"]
        self.ft_model = entry["model_id"]
        self.pct = pct
        self.cost_ratio_threshold = float(entry.get("cost_watch", {}).get("ratio_threshold", 2.0))
        self._mtime = mtime
        log.info("router loaded: ft=%s pct=%d base=%s", self.ft_model, self.pct, self.base_model)

    def choose_arm(self, sticky_key: str | None) -> str:
        """Deterministic per sticky_key so one user sees one model during a ramp step."""
        self._reload()
        if self.pct <= 0:
            return "base"
        if self.pct >= 100:
            return "ft"
        seed = sticky_key or os.urandom(8).hex()
        bucket = int(hashlib.sha1(seed.encode()).hexdigest(), 16) % 100
        return "ft" if bucket < self.pct else "base"

    def chat(self, messages: list[dict], sticky_key: str | None = None, **kwargs) -> str:
        arm = self.choose_arm(sticky_key)
        try:
            return self._call(arm, messages, **kwargs)
        except OpenAIError as exc:
            if arm == "ft" and self.pct < 100:  # fail open: a broken fine-tune never drops traffic
                log.warning("ft arm failed (%s); retrying on base", exc)
                return self._call("base", messages, **kwargs)
            raise

    def _call(self, arm: str, messages: list[dict], **kwargs) -> str:
        model = self.ft_model if arm == "ft" else self.base_model
        started = time.perf_counter()
        try:
            resp = self.client.chat.completions.create(model=model, messages=messages, **kwargs)
        except OpenAIError as exc:
            self._emit(arm, model, started, error=type(exc).__name__)
            raise
        usage = resp.usage
        self._emit(arm, model, started, prompt_tokens=usage.prompt_tokens, completion_tokens=usage.completion_tokens)
        return resp.choices[0].message.content or ""

    # r3-cost-watch + r4-rollback-signal: one structured line per request feeds the
    # dashboard that computes p95 latency, error rate and cost ratio per arm.
    def _emit(self, arm: str, model: str, started: float, **fields) -> None:
        record = {"event": "llm_request", "arm": arm, "model": model,
                  "latency_ms": round((time.perf_counter() - started) * 1000, 1),
                  "rollout_pct": self.pct, **fields}
        log.info(json.dumps(record))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    router = ModelRouter()
    print(router.chat([{"role": "user", "content": "ping"}], sticky_key="smoke-test", max_tokens=8))
