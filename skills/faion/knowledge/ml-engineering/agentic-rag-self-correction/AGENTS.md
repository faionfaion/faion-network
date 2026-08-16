# Agentic RAG — Self-Correction Loop

## Summary

**One-sentence:** Generates an answer, runs a faithfulness verifier (different model) against retrieved chunks, regenerates with feedback up to a hard cap, escalates if ungrounded claims persist.

**One-paragraph:** Generators hallucinate even on grounded RAG context. This methodology wraps any RAG agent with a self-correction loop: generate → verify faithfulness against the same retrieved chunks via a DIFFERENT model → if &gt;2 ungrounded claims, regenerate with feedback. Cap at `max_corrections` (default 2). On cap reached without verified answer, escalate to human review with full iteration trace.

**Ефективно для:**

- RAG features де hallucination > 3% — потрібен safety net.
- Mandatory verifier (different model than generator) — break confirmation bias.
- Trace всі iterations для post-mortem.
- Hard cap на корекції — uncapped loops drift.
- Bridge with `[[agentic-rag-iterative-retrieval]]` — verifier is the gate.

## Applies If (ALL must hold)

- Hallucination rate &gt;3% on baseline RAG eval.
- Verifier model available distinct from generator.
- Cost budget allows N × verifier calls per query.
- Audit-trace pipeline downstream.

## Skip If (ANY kills it)

- Hallucination rate &lt;1% (overhead exceeds gain).
- Only one model available (no distinct verifier).
- Strict latency &lt;2s SLA — self-correct adds 1–3s.
- No audit-trace consumer.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Generator model client | provider client | platform |
| Verifier model client (different from generator) | provider client | platform |
| Faithfulness prompt template | text | service repo |
| Audit log writer | python | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[agentic-rag-iterative-retrieval]]` | Companion methodology — verifier gates iterative loop. |
| `[[prompt-pr-review-checklist]]` | Per-prompt-PR review of the faithfulness prompt. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 2 rules + run/skip terminals | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for self-correction-config | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with detector + repair | ~700 |
| `content/04-procedure.xml` | essential | 5-step: pick verifier → generate → verify → regenerate → escalate | ~700 |
| `content/06-decision-tree.xml` | essential | Routes hallucination rate + verifier availability to self-correct vs vanilla | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `faithfulness-verifier` | sonnet | Different from generator (rule r1); reasoning fits sonnet. |
| `regenerate-with-feedback` | opus | Generator stays on opus. |

## Templates

| File | Purpose |
|------|---------|
| `templates/self_correction_loop.py` | SelfCorrectionLoop class. |
| `templates/self-correction-config.json` | Config skeleton. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agentic-rag-self-correction.py` | Validate self-correction-config | Pre-commit + CI |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[agentic-rag-iterative-retrieval]]
- [[agentic-rag-query-decomposition]]
- [[rag-bench-harness-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on baseline hallucination rate + verifier availability + latency budget. Walk before wiring.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/self_correction_loop.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class SelfCorrectionConfig:
    max_corrections: int = 2
    generator_model: str = "opus"
    verifier_model: str = "sonnet"
    max_ungrounded_claims: int = 2
    audit_trace: bool = True


@dataclass
class SelfCorrectionLoop:
    config: SelfCorrectionConfig
    generate: Callable[[str, list[dict], list[str] | None], str]
    verify: Callable[[str, list[dict]], dict]  # returns {"ungrounded": int, "feedback": list[str]}
    audit_log: Callable[[dict], None]

    def __post_init__(self) -> None:
        # rule r1: distinct verifier
        if self.config.verifier_model == self.config.generator_model:
            raise ValueError("verifier_model must differ from generator_model (rule r1)")
        # rule r2: cap + audit
        if self.config.max_corrections > 3:
            raise ValueError("max_corrections cap is 3 (rule r2)")
        if not self.config.audit_trace:
            raise ValueError("audit_trace must be true (rule r2)")

    def run(self, query: str, chunks: list[dict]) -> dict[str, Any]:
        trace: list[dict] = []
        feedback: list[str] | None = None
        for i in range(self.config.max_corrections + 1):
            answer = self.generate(query, chunks, feedback)
            verdict = self.verify(answer, chunks)
            trace.append({"iter": i, "answer": answer, "verdict": verdict})
            if verdict["ungrounded"] <= self.config.max_ungrounded_claims:
                self.audit_log({"query": query, "trace": trace, "result": "verified"})
                return {"answer": answer, "needs_human_review": False, "trace": trace}
            feedback = verdict.get("feedback", [])
        # cap reached
        self.audit_log({"query": query, "trace": trace, "result": "escalated"})
        return {"answer": None, "needs_human_review": True, "trace": trace}
```

### `templates/self-correction-config.json`

```json
{
  "max_corrections": 2,
  "generator_model": "opus",
  "verifier_model": "sonnet",
  "max_ungrounded_claims": 2,
  "audit_trace": true
}
```
