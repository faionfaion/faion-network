---
slug: supply-chain-risk-checklist-spike
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "89fa19c2f2789673"
summary: A 7-signal checklist for evaluating a library before adoption (license, maintainer count, last release, CVE history, GitHub star vs npm-download ratio, transitive depth, vendor lock-in) producing a numeric risk score.
tags: [supply-chain, dependency-risk, library-evaluation, security, SBOM]
---

# Supply Chain Risk Checklist Spike

## Summary

**One-sentence:** A 7-signal checklist for evaluating a library before adoption (license, maintainer count, last release, CVE history, GitHub star vs npm-download ratio, transitive depth, vendor lock-in) producing a numeric risk score.

**One-paragraph:** After log4shell (CVE-2021-44228), event-stream (2018 npm hijack), and the xz-utils backdoor (CVE-2024-3094), library evaluation cannot be reduced to "is it popular?". This methodology walks a 7-signal checklist using `npm audit`, `pip-audit`, `osv.dev`, `socket.dev`, GitHub API, and Snyk Open Source Advisor as data sources, scores each on 0-3 (low/med/high/critical risk), and emits a `LibraryRiskReport`. Output: numeric risk score (0-21), traffic-light decision (green ≤ 6, yellow 7-12, red ≥ 13), and a remediation suggestion (fork, pin, replace).

## Applies If (ALL must hold)

- evaluating a new library / framework / SDK before adoption OR auditing an existing dependency
- the library will be on the production code path OR build path
- you can run network calls (osv.dev, GitHub API) from the eval machine
- there is at least 30min available — this is a spike, not a glance

## Skip If (ANY kills it)

- the library is a transitive dep you do not directly import — evaluate the direct parent instead
- this is a one-off script (e.g. data migration) that will be deleted next week
- the library is officially blessed by your platform (e.g. AWS SDK on AWS Lambda) and substitution costs &gt; risk
- you have already evaluated this library in the last 90 days

## Prerequisites

- library name + ecosystem (npm, PyPI, crates.io, Maven, RubyGems, Go modules)
- API access to osv.dev (public) and GitHub (token recommended for rate limits)
- access to `npm audit` / `pip-audit` / `cargo audit` for the local dependency
- list of permissive licenses your project accepts (MIT, Apache-2.0, BSD)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer/dependency-audit` | Periodic-audit upstream — uses this checklist for spot-checks |
| `geek/sdlc-ai/sca-supply-chain-analysis` | SCA tooling integration that consumes this report |
| `pro/dev/software-developer/fork-vs-fix-decision-rule` | Chosen when this checklist returns RED + critical dependency |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 7-signal coverage, fresh data, license closed list, transitive depth, no-stars-without-downloads | ~1000 |
| `content/02-output-contract.xml` | essential | `LibraryRiskReport` schema with scores, decision, remediation | ~700 |
| `content/03-failure-modes.xml` | essential | 6 modes: stars-as-quality, missing CVE check, license confusion | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cve_lookup_osv` | haiku | API call + parse |
| `maintainer_count_github` | haiku | GitHub API mechanical |
| `license_classification` | sonnet | SPDX matching with edge cases |
| `risk_score_synthesis` | sonnet | Aggregation rule application |
| `remediation_suggestion` | opus | Cross-signal reasoning (fork vs pin vs replace) |

## Templates

| File | Purpose |
|------|---------|
| `templates/library-risk-report.json` | Output schema |
| `templates/license-allowlist.yaml` | Operator's accepted licenses |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/evaluate-library.sh` | Driver: fetch all 7 signals, emit report | Pre-adoption spike |
| `scripts/quarterly-rescore.py` | Re-run scoring on all production deps | Quarterly cadence |

## Related

- parent skill: `solo/dev/software-developer/`
- peer methodologies: `dependency-audit`, `fork-vs-fix-decision-rule`
- external: [OSV (Google open vulnerability DB)](https://osv.dev/) · [Socket — npm/PyPI supply-chain](https://socket.dev/) · [Snyk Open Source Advisor](https://snyk.io/advisor/) · [OpenSSF Scorecard](https://github.com/ossf/scorecard) · [Sonatype State of the Software Supply Chain 2023](https://www.sonatype.com/state-of-the-software-supply-chain/introduction)
