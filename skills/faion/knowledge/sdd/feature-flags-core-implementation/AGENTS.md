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
| `templates/_smoke-test.py` | Minimum viable filled-in artefact for sanity-checking the schema. |

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
