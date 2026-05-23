# App Store and Play Store Release

## Summary

**One-sentence:** Cross-store release playbook step: prepare metadata, screenshots, review notes, staged rollout, post-release watch.

**One-paragraph:** Cross-store release playbook step: prepare metadata, screenshots, review notes, staged rollout, post-release watch. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Cross-store release зі staged rollout (1% → 10% → 50% → 100%) і rollback criteria.
- Pre-flight review checklist для мінімізації reviewer rejection.
- Post-release watch: crash rate, store rating, support ticket spike.

## Applies If (ALL must hold)

- Shipping a mobile app to App Store or Play Store (or both).
- Need staged rollout with rollback criteria.
- Reviewer rejection risk must be minimized via pre-flight checks.

## Skip If (ANY kills it)

- Internal-only enterprise distribution (TestFlight / MDM, not public).
- Web-only product.
- Hotfix-only release where store metadata is unchanged.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| App Store Connect access | credential | release manager |
| Play Console access | credential | release manager |
| Signed build artefacts | ipa / aab | ci |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[android-keystore-and-signing]] | Signed builds are required input to the release step |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output per step | 1000 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template fill, bounded transformation |
| `synthesize-decision` | sonnet | Per-instance judgment; bounded inputs |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/release-playbook-step.md` | Cross-store release step skeleton with per-store checklists |
| `templates/rollout-decision-log.md` | Decision log tracking the staged-rollout gate decisions |
| `templates/_smoke-test.md` | Filled-in playbook for a v2.3.0 release |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-app-store-and-play-store-release.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[android-keystore-and-signing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
