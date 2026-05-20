---
slug: gov-license-compliance-scan
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Every release pipeline runs an automated license scan against an explicit allowlist.
content_id: "45fd1c644873945c"
tags: [governance, license-compliance, sbom, supply-chain, eu-cra]
---
# License Compliance as a Build-Blocking Gate

## Summary

**One-sentence:** Every release pipeline runs an automated license scan against an explicit allowlist.

**One-paragraph:** Every release pipeline runs an automated license scan against an explicit allowlist. Free OSS-shipped projects use GitHub's `licensee` for source detection; commercial SaaS or shipped binaries use FOSSA (or Black Duck / ScanCode) to produce an SPDX/CycloneDX SBOM and a deny/flag/approve decision per dependency. Copyleft licenses (GPL, AGPL, SSPL) introduced into proprietary builds block the pipeline; the agent regenerates the `NOTICE` / `THIRD_PARTY.md` attribution file on every dependency change. License scanning runs on PR, not just on release.

## Applies If (ALL must hold)

- Any product distributed externally — SaaS, downloadable, OSS published — where license obligations attach.
- Enterprise procurement contexts where customers ask for an SBOM and a license attestation.
- Repos where AI agents add dependencies autonomously; the agent is the new "developer who didn't read the license".
- Products subject to EU CRA (anything sold in the EU after Sep 2026) or US federal procurement (EO 14028 SBOM mandate).

## Skip If (ANY kills it)

- Internal-only tools that never leave the org boundary — no redistribution, no obligation.
- Hobby projects with zero compliance bar (still good hygiene if free; skip if it slows you down).
- Vendored read-only mirrors — license obligations follow the upstream redistribution, not the mirror.
- Pure data repos with no compiled artifact — apply data-license review instead.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/sdlc-ai/sdlc-ai/`
