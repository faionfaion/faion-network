# Supply Chain Risk Checklist Spike

## Summary

**One-sentence:** 7-signal library risk report (license, maintainer count, last release, CVE history, stars-to-downloads, transitive depth, vendor lock-in) producing an aggregate score and a green/yellow/red verdict.

**One-paragraph:** After log4shell, event-stream, and xz-utils, library evaluation cannot reduce to 'is it popular?'. This methodology walks a 7-signal checklist using osv.dev, the registry API, GitHub stars vs downloads, and SBOM data; scores each signal 0-3; aggregates to a 0-21 score with green (<=6) / yellow (7-12) / red (>=13) verdict; emits a remediation suggestion (adopt / pin / fork / decline). Data must be fresh within 24h; SSPL/BUSL/custom licenses always score 3.

**Ефективно для:**

- Перед adoption нової бібліотеки на production code path.
- Quarterly rescore критичних залежностей.
- Інцидент supply-chain (event-stream / xz / tj-actions) - re-audit affected deps.
- Custom license bumped - оцінити legal/SaaS impact.
- Transitive bloat - оцінити блокучу важкість.

## Applies If (ALL must hold)

- Evaluating a new library / framework / SDK before adoption OR auditing an existing dependency.
- The library will be on the production code path OR build path.
- Network access to osv.dev + GitHub API is available.
- At least 30 minutes is available - this is a spike, not a glance.

## Skip If (ANY kills it)

- Library is a transitive dep you do not directly import (evaluate parent instead).
- Throwaway script that will be deleted next week.
- Platform-blessed SDK (AWS SDK on Lambda) where substitution costs > risk.
- Library was evaluated within the last 90 days and nothing changed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Library name + ecosystem | npm / PyPI / crates.io / Maven / RubyGems / Go | engineering |
| License allowlist | operator-accepted SPDX list | legal |
| GitHub token | personal access token for rate limits | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[security-testing]] | consumer of this report; library risk feeds into release security pass. |
| [[openapi-specification]] | API surface consumers consider before adopting a transitive library risk. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: 7-signal coverage, data fresh 24h, license closed list, transitive depth cap, stars without downloads, decision record, remediation explicit | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: fetch signals, score, aggregate, verdict, remediation | ~900 |
| `content/05-examples.xml` | essential | Worked example: xz-utils retro evaluation | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cve_lookup_osv` | haiku | API call + parse. |
| `maintainer_count_github` | haiku | GitHub API mechanical. |
| `license_classification` | sonnet | SPDX matching with edge cases. |
| `risk_score_synthesis` | sonnet | Aggregation rule application. |
| `remediation_suggestion` | opus | Cross-signal reasoning (fork vs pin vs replace). |

## Templates

| File | Purpose |
|------|---------|
| `templates/library-risk-report.json` | JSON skeleton for the 7-signal library risk report. |
| `templates/license-allowlist.yaml` | Operator-accepted SPDX license allowlist. |
| `templates/_smoke-test.json` | Minimum viable library risk report for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-supply-chain-risk-checklist-spike.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[security-testing]]
- [[openapi-specification]]
- [[performance-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - signal coverage, data freshness, license class, aggregate band - onto a rule from `content/01-core-rules.xml`. Use it before any adoption: it catches stars-only-eval and stale-CVE-data upstream.
