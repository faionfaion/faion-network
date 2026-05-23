# Android Keystore and Signing

## Summary

**One-sentence:** Produces a signing config: keystore policy, Play App Signing decision, upload-key handling, debug-key separation.

**One-paragraph:** Produces a signing config: keystore policy, Play App Signing decision, upload-key handling, debug-key separation. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Прийняття рішення Play App Signing vs self-managed і документація рішення з owner.
- Конфіг для CI з reproducible signed builds.
- Відокремлення debug.keystore від upload key — щоб не зливати в Slack.

## Applies If (ALL must hold)

- Shipping an Android app via the Play Store or a managed enterprise channel.
- Migrating from legacy app-signed builds to Play App Signing.
- CI must produce reproducible signed builds.

## Skip If (ANY kills it)

- Pure web app or PWA — no Android signing surface.
- iOS-only roadmap.
- Internal-only enterprise rollout via MDM with a different signing flow.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Play Console access | credential | release manager |
| Keystore secret store | vault path | platform / security |
| CI signing config | yaml / script | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[app-store-and-play-store-release]] | Signing is one stage of the release pipeline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 4-step procedure with input/action/output per step | 1000 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-skeleton` | haiku | Mechanical template emission |
| `wire-feature-logic` | sonnet | Per-feature judgment with bounded inputs |
| `audit-output` | sonnet | Verify rules in 01-core-rules.xml hold |

## Templates

| File | Purpose |
|------|---------|
| `templates/signing-config.gradle.kts` | Gradle Kotlin DSL signing config skeleton with build-type separation |
| `templates/signing-policy.md` | Markdown policy + decision record for the signing approach |
| `templates/_smoke-test.gradle.kts` | Minimum-viable filled-in signing config |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-android-keystore-and-signing.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[app-store-and-play-store-release]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
