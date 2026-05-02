---
name: model-routing-cheap-vs-strong
description: Build a two-stage complexity classifier that routes prompts to Haiku, Sonnet, or Opus to cut inference costs ~6x without degrading quality.
tier: geek
group: cost-optimization
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working `ModelRouter` class that classifies every incoming prompt and dispatches it to `claude-haiku-4-5-20251001` (simple lookups), `claude-sonnet-4-6` (moderate reasoning), or `claude-opus-4-7` (complex reasoning). The classifier uses a fast regex/keyword pass first and falls back to a lightweight LLM call only when ambiguous. At a 70/25/5 split this routing cuts average inference cost roughly 6x versus always calling Opus, with no change to the caller API.

## Prerequisites

- Python 3.11+, `anthropic>=1.30.0`, `pydantic>=2.0` installed.
- An `ANTHROPIC_API_KEY` in the environment.
- Baseline familiarity with the Anthropic Python SDK (messages API, streaming).
- Optional: a query log (CSV or JSONL) of past prompts to calibrate thresholds.

## Steps

1. Install dependencies into your project virtualenv:

   ```bash
   pip install "anthropic>=1.30.0" "pydantic>=2.0"
   ```

2. Create `router/classifier.py` with the keyword-first classifier:

   ```python
   """Two-stage prompt complexity classifier.

   Stage 1: regex/keyword heuristics (zero LLM cost).
   Stage 2: LLM-based fallback for ambiguous prompts (Haiku, fast + cheap).
   """

   from __future__ import annotations

   import re
   from enum import Enum

   import anthropic
   from pydantic import BaseModel

   # ---------------------------------------------------------------------------
   # Tier definition
   # ---------------------------------------------------------------------------

   class Tier(str, Enum):
       CHEAP  = "claude-haiku-4-5-20251001"
       MID    = "claude-sonnet-4-6"
       STRONG = "claude-opus-4-7"


   # ---------------------------------------------------------------------------
   # Stage 1: heuristic rules (zero cost, <0.1 ms)
   # ---------------------------------------------------------------------------

   _CHEAP_PATTERNS: list[re.Pattern[str]] = [
       re.compile(r"\btranslat(e|ion)\b", re.I),
       re.compile(r"\bsummariz(e|ation)\b.*\bin\s+\d+\s+word", re.I),
       re.compile(r"\bspell[\s-]?check\b", re.I),
       re.compile(r"\bformat\s+(as\s+)?(json|yaml|csv|markdown)\b", re.I),
       re.compile(r"\bwhat\s+is\s+the\s+(capital|population|currency)\b", re.I),
       re.compile(r"\bconvert\s+\d+", re.I),
       re.compile(r"\blist\s+(the\s+)?\d+\s+\w+\b", re.I),
       re.compile(r"^(yes|no|true|false)[?.!]?\s*$", re.I),
   ]

   _STRONG_PATTERNS: list[re.Pattern[str]] = [
       re.compile(r"\b(architect|design|strategy)\s+(a|an|the)\s+\w+\s+system\b", re.I),
       re.compile(r"\bcompare\s+and\s+contrast\b.*\bpros\s+and\s+cons\b", re.I | re.S),
       re.compile(r"\bwrite\s+(a\s+)?(research\s+paper|thesis|dissertation)\b", re.I),
       re.compile(r"\bsecurity\s+(audit|review|pentest)\b", re.I),
       re.compile(r"\brefactor\s+(the\s+)?(entire|whole|full)\b", re.I),
       re.compile(r"\bmulti.?step\s+(reasoning|analysis|plan)\b", re.I),
       re.compile(r"\b(formal\s+proof|mathematical\s+derivation)\b", re.I),
   ]


   def _heuristic_tier(prompt: str) -> Tier | None:
       """Return a tier if heuristics are confident, else None (→ LLM fallback)."""
       for pat in _STRONG_PATTERNS:
           if pat.search(prompt):
               return Tier.STRONG
       for pat in _CHEAP_PATTERNS:
           if pat.search(prompt):
               return Tier.CHEAP
       word_count = len(prompt.split())
       if word_count <= 12:
           return Tier.CHEAP
       if word_count >= 300:
           return Tier.STRONG
       return None  # ambiguous → stage 2


   # ---------------------------------------------------------------------------
   # Stage 2: LLM-based fallback (Haiku, ~0.3 cents per classification)
   # ---------------------------------------------------------------------------

   _CLASSIFY_SYSTEM = """You are a prompt complexity classifier.
   Given a user prompt, reply with EXACTLY one word: CHEAP, MID, or STRONG.

   CHEAP  — simple lookup, format conversion, one-step fact retrieval.
   MID    — requires reasoning, multi-step logic, code generation.
   STRONG — deep analysis, architecture design, long-form research, security audit.

   Reply with one word only. No explanation."""


   class _ClassifyResponse(BaseModel):
       tier: Tier


   def llm_classify(prompt: str, client: anthropic.Anthropic) -> Tier:
       """Call Haiku to classify prompt complexity. Fast and cheap."""
       msg = client.messages.create(
           model=Tier.CHEAP.value,
           max_tokens=5,
           system=_CLASSIFY_SYSTEM,
           messages=[{"role": "user", "content": prompt[:2000]}],
       )
       raw = msg.content[0].text.strip().upper()
       mapping = {"CHEAP": Tier.CHEAP, "MID": Tier.MID, "STRONG": Tier.STRONG}
       return mapping.get(raw, Tier.MID)  # safe default: Sonnet


   # ---------------------------------------------------------------------------
   # Public API
   # ---------------------------------------------------------------------------

   def classify_prompt(prompt: str, client: anthropic.Anthropic) -> Tier:
       """Classify prompt tier. Uses heuristics first, LLM fallback if ambiguous."""
       tier = _heuristic_tier(prompt)
       if tier is not None:
           return tier
       return llm_classify(prompt, client)
   ```

3. Create `router/router.py` — the `ModelRouter` that wraps the classifier and dispatches:

   ```python
   """ModelRouter: classify → dispatch to the right Claude model."""

   from __future__ import annotations

   from dataclasses import dataclass, field

   import anthropic

   from .classifier import Tier, classify_prompt


   @dataclass
   class RoutingStats:
       cheap: int = 0
       mid: int = 0
       strong: int = 0

       def record(self, tier: Tier) -> None:
           if tier == Tier.CHEAP:
               self.cheap += 1
           elif tier == Tier.MID:
               self.mid += 1
           else:
               self.strong += 1

       @property
       def total(self) -> int:
           return self.cheap + self.mid + self.strong

       def cost_ratio(self) -> float:
           """Approx cost vs always-Opus (Haiku=1x, Sonnet=5x, Opus=15x relative)."""
           if self.total == 0:
               return 0.0
           weighted = self.cheap * 1 + self.mid * 5 + self.strong * 15
           opus_baseline = self.total * 15
           return weighted / opus_baseline


   class ModelRouter:
       """Route prompts to Haiku / Sonnet / Opus based on complexity.

       Usage:
           router = ModelRouter()
           response = router.complete("What is the capital of France?")
           print(response.content[0].text)
       """

       def __init__(
           self,
           api_key: str | None = None,
           force_tier: Tier | None = None,
       ) -> None:
           self._client = anthropic.Anthropic(api_key=api_key)
           self._force = force_tier
           self.stats = RoutingStats()

       def complete(
           self,
           prompt: str,
           *,
           system: str = "",
           max_tokens: int = 1024,
           **kwargs,
       ) -> anthropic.types.Message:
           tier = self._force or classify_prompt(prompt, self._client)
           self.stats.record(tier)
           messages: list[dict] = [{"role": "user", "content": prompt}]
           create_kwargs = dict(
               model=tier.value,
               max_tokens=max_tokens,
               messages=messages,
               **kwargs,
           )
           if system:
               create_kwargs["system"] = system
           return self._client.messages.create(**create_kwargs)

       def cost_savings_report(self) -> str:
           ratio = self.stats.cost_ratio()
           savings_pct = round((1 - ratio) * 100, 1)
           return (
               f"Routed {self.stats.total} calls: "
               f"Haiku={self.stats.cheap} Sonnet={self.stats.mid} Opus={self.stats.strong} | "
               f"Cost ratio vs all-Opus: {ratio:.2f} ({savings_pct}% cheaper)"
           )
   ```

4. Create `router/__init__.py` to expose the public API:

   ```python
   from .classifier import Tier, classify_prompt
   from .router import ModelRouter, RoutingStats

   __all__ = ["ModelRouter", "RoutingStats", "Tier", "classify_prompt"]
   ```

5. Integrate the router into your application entry point:

   ```python
   from router import ModelRouter

   router = ModelRouter()

   queries = [
       "Translate 'hello' to Spanish.",
       "Write a Python function that sorts a list of dicts by a nested key.",
       "Design a multi-tenant SaaS auth system supporting SAML SSO and RBAC.",
   ]

   for q in queries:
       response = router.complete(q)
       print(f"Q: {q[:60]}")
       print(f"A: {response.content[0].text[:120]}")
       print()

   print(router.cost_savings_report())
   ```

6. Calibrate thresholds with your own query log. Run a one-time audit to measure accuracy:

   ```python
   import csv
   from router import ModelRouter, Tier

   # CSV with columns: prompt, expected_tier (CHEAP/MID/STRONG)
   router = ModelRouter()
   correct = 0
   total = 0

   with open("query-audit.csv") as fh:
       for row in csv.DictReader(fh):
           predicted = router._client and __import__("router.classifier", fromlist=["classify_prompt"]).classify_prompt(
               row["prompt"], router._client
           )
           if predicted.name == row["expected_tier"]:
               correct += 1
           total += 1

   print(f"Accuracy: {correct}/{total} = {correct/total:.1%}")
   ```

   Add or tighten patterns in `_CHEAP_PATTERNS` / `_STRONG_PATTERNS` until accuracy exceeds 90% on your corpus before deploying.

## Verify

Run the integration smoke test:

```python
python - <<'EOF'
from router import ModelRouter, Tier
router = ModelRouter()

# Cheap: one-step fact
r1 = router.complete("What is the capital of Germany?")
assert r1.model == Tier.CHEAP.value, f"Expected Haiku, got {r1.model}"

# Mid: code generation (falls through to LLM classify)
r2 = router.complete(
    "Write a Python function that parses an ISO 8601 duration string "
    "into a timedelta object, handling weeks correctly."
)
assert r2.model in (Tier.MID.value, Tier.STRONG.value), f"Expected Sonnet+, got {r2.model}"

print(router.cost_savings_report())
print("OK")
EOF
```

Expected output ends with `OK` and a routing report like:
`Routed 2 calls: Haiku=1 Sonnet=1 Opus=0 | Cost ratio vs all-Opus: 0.20 (80.0% cheaper)`

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| LLM fallback returns `MID` for clearly cheap prompts | Classifier prompt is too ambiguous or Haiku returns `mid` casing | Add a `.upper()` normalisation (already in code); also broaden `_CHEAP_PATTERNS` |
| `assert r1.model == Tier.CHEAP.value` fails | Heuristic missed a simple prompt | Add a regex to `_CHEAP_PATTERNS` matching that prompt shape |
| Cost ratio does not improve after routing | Traffic skew: most prompts land in `STRONG` | Audit with `cost_savings_report()`; split complex tasks into smaller sub-prompts before routing |
| `anthropic.RateLimitError` on LLM fallback | Haiku classify calls are hitting rate limits | Cache classify results by prompt hash using `functools.lru_cache` or Redis TTL=1h |
| Stage-2 latency hurts P95 response time | Every ambiguous prompt pays a round-trip to Haiku | Pre-warm the classifier cache with your 1000 most frequent prompts at startup |

## Next

- Add prompt caching (`cache_control: {"type": "ephemeral"}`) to system prompts on the Sonnet and Opus paths to cut costs further — see [`claude-api-basics`](../../../knowledge/geek/ai/llm-integration/claude-api-basics).
- Extend routing to a streaming path using `client.messages.stream()` so callers get tokens immediately without buffering.
- Log tier decisions to your analytics pipeline and set up a weekly accuracy review to retrain heuristics as your query distribution shifts.

## References

- [knowledge/geek/ai/llm-integration/llm-classifier-design](../../../knowledge/geek/ai/llm-integration/llm-classifier-design) — provides the two-stage cascade pattern (heuristic → LLM fallback) that underpins Steps 2 and 3 of this playbook.
- [knowledge/geek/ai/llm-integration/claude-api-integration](../../../knowledge/geek/ai/llm-integration/claude-api-integration) — covers `anthropic.Anthropic` client init, `messages.create` kwargs, and model ID conventions used throughout the router implementation.
- [knowledge/geek/ai/llm-integration/structured-output-patterns](../../../knowledge/geek/ai/llm-integration/structured-output-patterns) — justifies the single-word response schema used in the LLM classify call (Step 2) to keep token usage and parsing overhead minimal.
