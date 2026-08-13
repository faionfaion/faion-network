# Feature Flag Core Implementation

## Summary

**One-sentence:** Implements FeatureFlagManager registering typed FeatureFlag dataclasses, loading from FF_* env + JSON config, exposing is_enabled(flag_name, user_id) as the single call site.

**One-paragraph:** Implements FeatureFlagManager registering typed FeatureFlag dataclasses, loading from FF_* env + JSON config, exposing is_enabled(flag_name, user_id) as the single call site. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Need an in-process feature flag layer without taking on a managed flag service.
- Stack is Python; typed flag definitions live in code and version with the repo.
- Decorator or middleware integration points are required for HTTP/CLI surfaces.
- Output produces `code` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Need an in-process feature flag layer without taking on a managed flag service.
- Stack is Python; typed flag definitions live in code and version with the repo.
- Decorator or middleware integration points are required for HTTP/CLI surfaces.

## Skip If (ANY kills it)

- Using OpenFeature / LaunchDarkly / GrowthBook / Statsig SDK — let the SDK be the call site.
- Project has <3 flags ever — boolean if/else is cheaper.
- Flag flips must be hot-reloadable from a UI without redeploy — use a managed service.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Python project root | src/ | team |
| Config dir | config/ or .config/ | team |
| Env var loader | settings.py / pydantic-settings | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[feature-flags-types-lifecycle]] | flag taxonomy + lifecycle policy upstream |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-manager` | sonnet | Class skeleton + registration. |
| `decorator-impl` | haiku | Mechanical decorator wrapper. |
| `env-loader` | haiku | FF_* prefix parsing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/feature_flag_manager.py` | FeatureFlagManager: typed flag registry + env/file loader + is_enabled API |
| `templates/decorator.py` | @feature(name) decorator gating a function on flag state |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-feature-flags-core-implementation.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[feature-flags-types-lifecycle]]
- [[feature-flags-rollout-targeting]]
- [[feature-flags-services-testing]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are you on a managed flag SDK already?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/feature_flag_manager.py`

```python
# faion_header_json: {"__faion_header__":{"purpose":"FeatureFlagManager: typed flag registry + env/file loader + is_enabled API","consumes":"see content/02-output-contract.xml","produces":"code","depends_on":"content/01-core-rules.xml#typed-flag-registration","token_budget_impact":"~150 tokens when loaded"}}
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class FeatureFlag:
    name: str
    description: str
    default: bool = False
    rollout_percent: int = 0
    targeting: dict = field(default_factory=dict)


class FeatureFlagManager:
    def __init__(self) -> None:
        self._flags: dict[str, FeatureFlag] = {}
        self._overrides: dict[str, bool] = {}

    def register(self, flag: FeatureFlag) -> None:
        self._flags[flag.name] = flag

    def load_env(self, prefix: str = "FF_") -> None:
        for k, v in os.environ.items():
            if not k.startswith(prefix):
                continue
            name = k.removeprefix(prefix).lower().replace("_", "-")
            self._overrides[name] = v.lower() in ("1", "true", "yes")

    def load_file(self, path: Path) -> None:
        if not path.is_file():
            return
        data = json.loads(path.read_text())
        for name, value in data.items():
            self._overrides[name] = bool(value)

    def is_enabled(self, name: str, user_id: str | None = None) -> bool:
        if name in self._overrides:
            return self._overrides[name]
        flag = self._flags.get(name)
        if flag is None:
            return False
        return flag.default
```

### `templates/decorator.py`

```python
# faion_header_json: {"__faion_header__":{"purpose":"@feature(name) decorator gating a function on flag state","consumes":"see content/02-output-contract.xml","produces":"code","depends_on":"content/01-core-rules.xml#typed-flag-registration","token_budget_impact":"~150 tokens when loaded"}}
from functools import wraps
from typing import Callable


def feature(name: str, manager):
    def deco(fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not manager.is_enabled(name):
                raise PermissionError(f"feature {name} disabled")
            return fn(*args, **kwargs)
        return wrapper
    return deco
```
