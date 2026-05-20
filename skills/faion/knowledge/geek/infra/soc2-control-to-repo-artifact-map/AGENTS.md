---
slug: soc2-control-to-repo-artifact-map
tier: geek
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "dfcc6e7f0221f461"
summary: One-to-many YAML map from each SOC 2 Trust Service Criterion to concrete repo artifacts (file paths, CI jobs, dashboard URLs) so audit evidence pulls in minutes, not weeks.
---
# Soc2 Control To Repo Artifact Map

## Summary

**One-sentence:** One-to-many YAML map from each SOC 2 Trust Service Criterion (TSC) control to concrete repo artifacts — file paths, CI job names, dashboard URLs — auto-rendered into the auditor evidence binder.

**One-paragraph:** Annual SOC 2 audits stall when evidence lives in a hundred places and is re-discovered every year. This methodology defines a single source-of-truth `soc2-map.yaml` checked into the product repo, mapping every applicable TSC criterion to one or more concrete artifacts (file path, CI job, dashboard link, ticket query, IaC resource). A small renderer turns the map into the auditor's evidence index and detects rot (artifact paths that no longer exist or CI jobs that disappeared). Anchored to "SOC2 / GDPR audit prep (annual)" for the product dev team. Geek tier because it presupposes self-hosted CI, infra-as-code, and a dashboarding stack.

## Applies If (ALL must hold)

- You are preparing for or maintaining a SOC 2 Type II audit (or equivalent: ISO 27001, HIPAA SOC 2-style controls).
- The product is shipped from one or a small set of monorepos / linked repos where artifacts live.
- You have authority to enforce that new controls require a map entry.
- A named consumer exists — auditor, GRC analyst, or compliance bot.

## Skip If (ANY kills it)

- Pre-audit phase with no scoped TSC list yet — first run a scoping workshop; map comes after scope is frozen.
- Artifacts live primarily outside the repo (e.g., paper logs, Notion-only) — fix the artifact-location problem first, then come back.
- One-off snapshot for a tiny startup with <5 controls — overhead does not pay back; a flat checklist is cheaper.

## Prerequisites

- Frozen list of in-scope TSC criteria (Security mandatory; Availability / Confidentiality / Processing Integrity / Privacy optional).
- Read access to CI logs, dashboards, and ticket systems the artifacts point at.
- A storage location for the rendered evidence binder (S3 bucket, doc, git tag) the auditor reads from.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/infra/AGENTS.md` | Parent group context |
| `pro/infra/pci-dss-vendor-evidence-pack` if present | Sibling evidence-collection discipline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules every map enforces | ~900 |

## Related

- parent skill: `geek/infra/`
- triggering activity: `p6-product-dev-team/SOC2 / GDPR audit prep (annual)`
- adjacent: `soc2-evidence-generator-cli` (pro/sdd) — generates per-PR evidence stubs that link into this map.
