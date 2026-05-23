# Feature Flag Cleanup Discipline

## Summary

**One-sentence:** Discipline for retiring feature flags after rollout: every flag carries an expiry, an owner, and a removal PR plan; produces a cleanup ticket per flag with a kill-by date and a verified-removed checkbox.

**One-paragraph:** Discipline for retiring feature flags after rollout: every flag carries an expiry, an owner, and a removal PR plan; produces a cleanup ticket per flag with a kill-by date and a verified-removed checkbox. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Codebases where post-launch 'flag still on for safety' became 'flag still on forever'.
- Solo founders who add flags during rollout and never come back.
- Migration projects (Rails 6→7, Vue 2→3) where transitional flags pile up.
- Audit prep (SOC2, ISO27001) where un-retired flags look like governance gaps.

## Applies If (ALL must hold)

- Project uses feature flags (LaunchDarkly, ConfigCat, env vars, in-code constants) for ≥3 active toggles.
- Flag debt has been observed (a flag older than its planned rollout window still in code).
- Operator can merge cleanup PRs without blocking on a release train.
- A single named owner exists per flag.

## Skip If (ANY kills it)

- Flags are intentional kill-switches with no expiry (e.g. emergency-disable for an external dep) — those use different discipline.
- Project has <3 flags — cleanup process overhead exceeds value.
- Org has a centralised flag-platform that already enforces expiries — duplicate process.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, ids, dashboard snapshots | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/` parent context | vocabulary, neighbouring methodologies |
| [[ci-quality-gate-design]] | upstream context this methodology builds on |
| [[hidden-tech-debt-trace]] | sibling discipline cited in decision tree |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-feature-flag-cleanup-discipline-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-feature-flag-cleanup-discipline.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-feature-flag-cleanup-discipline.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[ci-quality-gate-design]]
- [[hidden-tech-debt-trace]]
- [[dep-bump-batching-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
