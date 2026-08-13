# Feature Flag Rollout and Targeting

## Summary

**One-sentence:** Deterministic per-user bucketing for gradual rollouts: hash(flag+user) %100 < rollout_percent; per-attribute targeting (country, plan, role) sits on top.

**One-paragraph:** Deterministic per-user bucketing for gradual rollouts: hash(flag+user) %100 < rollout_percent; per-attribute targeting (country, plan, role) sits on top. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Need gradual rollout of a flag from 0% to 100% with reproducible per-user state.
- Need targeted exposure (beta cohort, country, plan, role) before global rollout.
- Flag manager is already in place (see feature-flags-core-implementation).
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Need gradual rollout of a flag from 0% to 100% with reproducible per-user state.
- Need targeted exposure (beta cohort, country, plan, role) before global rollout.
- Flag manager is already in place (see feature-flags-core-implementation).

## Skip If (ANY kills it)

- Flag is operational kill-switch only — gradual rollout has no value, just on/off.
- Anonymous traffic with no stable identifier — hash bucketing has nothing to anchor on.
- Managed flag SDK already provides bucketing — use it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| FeatureFlagManager | Python class | feature-flags-core-implementation |
| Stable user id source | auth context or session id | auth |
| Targeting attribute table | country/plan/role per user | user store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[feature-flags-core-implementation]] | manager + flag registry sits beneath rollout logic |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `bucketing-impl` | sonnet | Hash + percent gate. |
| `targeting-rules` | sonnet | Per-attribute matching. |
| `ramp-runner` | haiku | Script that ramps the percent value. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rollout.py` | Deterministic per-user bucketing with rollout_percent + targeting attrs |
| `templates/ramp.sh` | Ramp helper: bump rollout_percent in steps, wait for guardrails between |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-feature-flags-rollout-targeting.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[feature-flags-core-implementation]]
- [[feature-flags-types-lifecycle]]
- [[ab-testing-basics]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is this flag a gradual/targeted rollout AND is there a stable user id?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rollout.py`

```python
# faion_header_json: {"__faion_header__":{"purpose":"Deterministic per-user bucketing with rollout_percent + targeting attrs","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#deterministic-per-user","token_budget_impact":"~150 tokens when loaded"}}
import hashlib


def in_rollout(flag_name: str, user_id: str, rollout_percent: int) -> bool:
    raw = f"{flag_name}:{user_id}".encode()
    bucket = int(hashlib.sha256(raw).hexdigest(), 16) % 100
    return bucket < rollout_percent


def targeted(targeting: dict, attrs: dict) -> bool:
    for key, allowed in targeting.items():
        if attrs.get(key) not in allowed:
            return False
    return True
```

### `templates/ramp.sh`

```bash
# faion_header_json: {"__faion_header__":{"purpose":"Ramp helper: bump rollout_percent in steps, wait for guardrails between","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#deterministic-per-user","token_budget_impact":"~150 tokens when loaded"}}
set -euo pipefail
FLAG="$1"; shift
STEPS=("$@")
for pct in "${STEPS[@]}"; do
  echo "Ramping $FLAG to $pct%"
  # caller wires this to their flag-service / config-edit method
  curl -fsS -X PATCH "https://flags.internal/flags/$FLAG" -d "{\"rollout_percent\":$pct}"
  sleep 600
done
```
