# Max Turns Circuit Breaker

## Summary

**One-sentence:** Sets a max_turns on every agent run, catches MaxTurnsExceeded as a structured fallback, and emits a circuit-breaker-spec.

**One-paragraph:** Tool-calling agents fail by silently consuming budget — no exception, just N more turns. The only deterministic stop is a hard max_turns cap, paired with a structured catch that hands the partial trajectory to a cheap recovery model. This methodology turns an agent profile into a circuit-breaker-spec.

**Ефективно для:** solopreneur whose agent occasionally loops for 50 turns and burns $5 per failure.

## Applies If (ALL must hold)

- Agent calls ≥1 tool that returns text (not terminal).
- Failure mode 'silent loop' is observed or plausible.
- Recovery story exists (cheap model summarises trajectory).
- Budget per turn is bounded.
- Caller (web UI / API) can render a fallback message.

## Skip If (ANY kills it)

- Single LLM call — no loop possible.
- Strict deterministic chain — no tools, no looping.
- No fallback path — better to crash than swallow.
- Notebook scratch — manual cancellation OK.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `agent-profile.yaml` | agent_kind (react|coding|retrieval), per_turn_cost_usd, recovery_model, latency_budget_ms | author |
| `Agent entrypoint` | module symbol | code |
| `Cheap recovery model handle` | e.g. haiku | config |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[langchain-production-patterns]] | Pairs with retries and fallbacks. |
| [[manifest-then-fetch]] | Long tool outputs are a turn-multiplier. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Rules for max_turns range (5-10 retrieval, 15-20 coding), catch + recovery, no-500-bubble. | ~1000 |
| `content/02-output-contract.xml` | essential | circuit-breaker-spec schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | No cap, cap too high, no catch, recovery uses same expensive model. | ~700 |
| `content/04-procedure.xml` | recommended | 5-step wiring procedure. | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Profile parsing | haiku | Mechanical. |
| Decision drafting | sonnet | Tradeoffs require sound reasoning. |
| Code/config emission | sonnet | Mechanical but must compile. |
| Failure-mode cross-check | opus | Catches subtle gaps. |

## Templates

| File | Purpose |
|---|---|
| `templates/circuit-breaker-spec.md.j2` | Output. |
| `templates/circuit-breaker-spec.md` | Output. Generated from `templates/circuit-breaker-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/breaker.py` | Working max_turns + catch. |
| `templates/_smoke-test.yaml` | Minimum. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-max-turns-circuit-breaker.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[langchain-production-patterns]]
- [[manifest-then-fetch]]
- [[llamaindex-production-gotchas]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on agent_kind (retrieval → 5-10; coding → 15-20; planning → 10-15), then on per-turn-cost (high → smaller cap), recovery is always haiku-class. Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/breaker.py`

```python
"""Reference artefact for max-turns-circuit-breaker. Self-test only verifies the scaffold compiles."""
from __future__ import annotations


def build(decision: dict):
    """Build the runtime object from a validated decision-record."""
    if not isinstance(decision, dict):
        raise TypeError("decision must be dict from validated decision-record")
    return decision  # placeholder: real implementations wire here


def _self_test() -> int:
    out = build({"slug": "max-turns-circuit-breaker", "version": "2.0.0"})
    return 0 if out["slug"] == "max-turns-circuit-breaker" else 1


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        raise SystemExit(_self_test())
    if "--help" in sys.argv:
        print(__doc__)
```

### `templates/_smoke-test.yaml`

```yaml
agent_kind: low
per_turn_cost_usd: low
```
