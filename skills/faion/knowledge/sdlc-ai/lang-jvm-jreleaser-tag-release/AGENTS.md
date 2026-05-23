# JVM One-Tag Release via JReleaser

## Summary

**One-sentence:** Replace ad-hoc mvn deploy / gradle publish + hand-edited CHANGELOG with a single git tag that triggers JReleaser — staging to Maven Central, signing, changelog generation, GitHub release in one shot.

**One-paragraph:** JVM One-Tag Release via JReleaser produces a config artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- JVM library publisher (Maven Central / GitHub Packages).
- Team where the release ritual is bespoke per engineer and prone to error.
- Multi-module Gradle / Maven build needing coordinated version bump + tag.
- Project where every release must include signed artefacts + changelog.

## Applies If (ALL must hold)

- Repo publishes ≥ 1 artefact to a central registry.
- Maven Central or compatible target is configured.
- GPG signing key + GitHub token available as CI secrets.
- Team accepts conventional-commits → changelog generation.

## Skip If (ANY kills it)

- Repo never publishes externally (internal app only).
- Custom release pipeline already proven over years.
- Team won't adopt conventional commits — JReleaser changelog gets noisy.
- Multi-language release where JVM is one slice — JReleaser is JVM-only.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| jreleaser.yml | committed JReleaser config | release-eng |
| CI secrets | GPG key + Sonatype creds + GH token | platform |
| CHANGELOG generator | JReleaser default or custom config | release-eng |
| Tag convention | vMAJOR.MINOR.PATCH SemVer | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gov-conventional-commits-enforced]] | JReleaser changelog needs conventional commits |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `jreleaser_config_draft` | sonnet | Author the YAML for repo's distribution set. |
| `ci_workflow_draft` | sonnet | Tag-triggered GH Actions workflow. |
| `dry_run_validation` | haiku | `jreleaser config --output` validation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/jreleaser.yml` | JReleaser config for one Maven Central distribution. |
| `templates/release-workflow.yml` | Tag-triggered GH Actions workflow. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-jvm-jreleaser-tag-release.py` | Validate the JReleaser-config artefact. | pre-merge of release config |

## Related

- [[gov-conventional-commits-enforced]]
- [[lint-precommit-floor]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
