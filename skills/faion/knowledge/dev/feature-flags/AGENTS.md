# Feature Flags

## Summary

**One-sentence:** Gate incomplete or experimental code behind runtime flags so deploy is decoupled from release, with explicit ownership and a documented lifecycle.

**One-paragraph:** Feature flags gate incomplete or experimental code behind runtime toggles, decoupling deployment from release. Every flag has an owner, an expiry date, a lifecycle (off → canary → rollout → on → cleanup), and a removal PR queued. Flags ship in a central registry; their evaluation is pure (no side effects); kill-switches are mandatory for risky changes. Output is the flag registry plus the code patterns for evaluation + cleanup.

**Ефективно для:**

- Trunk-based development without long-lived branches.
- Progressive rollouts (canary 1% → 10% → 50% → 100%).
- A/B experiments wired to analytics.
- Kill-switches for risky integrations or third-party dependencies.

## Applies If (ALL must hold)

- Continuous delivery culture: deploys ship hourly to daily.
- Risk-tier or experiment-tier features need progressive exposure.
- Codebase can carry runtime flag evaluations cheaply (web/mobile/backend, not embedded).
- Engineering owns flag lifecycle (creation + cleanup), not just product.

## Skip If (ANY kills it)

- Single-tenant or on-prem deploys where there is no central runtime to flip flags.
- Hardware/firmware where flag evaluation costs cycle budget.
- Embedded systems with no remote config channel.
- Tiny app where deploy is the release — flags add overhead without payoff.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Flag platform chosen (LaunchDarkly, Statsig, GrowthBook, in-house) + version | config | platform |
| Flag registry location (file path or service URL) | URL/path | platform |
| Owner-and-expiry policy | ADR | tech-lead |
| Analytics integration for variant assignment | endpoint | data |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[trunk-based-dev-principles]] | Flags enable trunk-based shipping of incomplete work. |
| [[logging-patterns]] | Flag evaluations are logged for observability. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (owner + expiry, pure evaluation, central registry, kill-switch for risky, cleanup PR queued, no nested flags >2) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for flag entry + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: register → wire → roll out → monitor → cleanup | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `flag_registry_entry` | sonnet | Mechanical: owner + expiry + variants + targeting. |
| `evaluation_wiring` | sonnet | Add evaluation calls + analytics integration. |
| `cleanup_pr_queue` | sonnet | Stub the removal PR when the flag is created. |

## Templates

| File | Purpose |
|------|---------|
| `templates/flag-registry.json` | Flag registry schema with owner, expiry, variants, targeting |
| `templates/flag-manager.py` | Python flag manager wrapping evaluation + logging |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-feature-flags.py` | Validate flag registry entries against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[trunk-based-dev-principles]]
- [[logging-patterns]]
- [[ab-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps deploy cadence, exposure-risk, and platform maturity to a rule from `01-core-rules.xml`, telling the agent whether to wire a flag or skip when the runtime can't carry it. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/flag-registry.json`

```json
{
  "new_checkout": {
    "type": "release",
    "owner": "payments-team",
    "description": "New checkout flow replacing legacy cart UI",
    "created": "2026-01-15",
    "expected_cleanup": "2026-02-15",
    "status": "rolling_out",
    "rollout_percentage": 50
  },
  "new_search": {
    "type": "experiment",
    "owner": "search-team",
    "description": "ML-powered search vs rule-based baseline",
    "created": "2026-02-01",
    "expected_cleanup": "2026-03-15",
    "status": "active",
    "rollout_percentage": 25
  },
  "maintenance_mode": {
    "type": "ops",
    "owner": "platform-team",
    "description": "Redirect all traffic to maintenance page",
    "created": "2025-06-01",
    "expected_cleanup": null,
    "status": "permanent"
  },
  "disable_payments": {
    "type": "kill_switch",
    "owner": "platform-team",
    "description": "Emergency kill switch for payment processing",
    "created": "2025-01-01",
    "expected_cleanup": null,
    "status": "permanent"
  }
}
```

### `templates/flag-manager.py`

```python
"""FeatureFlagManager — env overrides, group/user lists, percentage bucketing."""
import hashlib
import json
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class FlagType(Enum):
    RELEASE = "release"
    EXPERIMENT = "experiment"
    OPS = "ops"
    PERMISSION = "permission"
    KILL_SWITCH = "kill_switch"


@dataclass
class FeatureFlag:
    name: str
    flag_type: FlagType
    default: bool = False
    description: str = ""
    owner: str = ""


@dataclass
class RolloutConfig:
    percentage: int = 0          # 0-100
    user_ids: set[str] = field(default_factory=set)
    groups: set[str] = field(default_factory=set)


class FeatureFlagManager:
    def __init__(self):
        self._flags: dict[str, FeatureFlag] = {}
        self._rollouts: dict[str, RolloutConfig] = {}
        self._overrides: dict[str, bool] = {}
        self._load_overrides()

    def _load_overrides(self):
        for key, value in os.environ.items():
            if key.startswith("FF_"):
                self._overrides[key[3:].lower()] = value.lower() in ("true", "1", "yes")
        config_path = os.getenv("FEATURE_FLAGS_CONFIG")
        if config_path and os.path.exists(config_path):
            with open(config_path) as f:
                self._overrides.update(json.load(f))

    def register(self, flag: FeatureFlag) -> None:
        self._flags[flag.name] = flag

    def set_rollout(self, flag_name: str, config: RolloutConfig) -> None:
        self._rollouts[flag_name] = config

    def is_enabled(
        self,
        flag_name: str,
        user_id: Optional[str] = None,
        groups: Optional[set[str]] = None,
    ) -> bool:
        if flag_name in self._overrides:
            return self._overrides[flag_name]
        flag = self._flags.get(flag_name)
        if not flag:
            return False
        rollout = self._rollouts.get(flag_name)
        if not rollout:
            return flag.default
        if user_id and user_id in rollout.user_ids:
            return True
        if groups and rollout.groups & groups:
            return True
        if rollout.percentage > 0 and user_id:
            key = f"{flag_name}:{user_id}"
            bucket = int(hashlib.md5(key.encode()).hexdigest(), 16) % 100
            return bucket < rollout.percentage
        return flag.default


feature_flags = FeatureFlagManager()
```
