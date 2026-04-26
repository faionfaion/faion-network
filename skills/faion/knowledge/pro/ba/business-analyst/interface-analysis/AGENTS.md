# Interface Analysis

## Summary

Identifies and documents all boundaries and connections between a solution and external systems, users, hardware, and communication channels, then specifies data elements, protocols, frequency, volume, security, and error handling for each. At enterprise scale, a portfolio-level integration landscape register (one row per source-target pair, with criticality tier, sensitivity classification, and owner) precedes per-interface specification and feeds SOC2/ISO 27001/GDPR Art. 30 compliance evidence.

## Why

Systems built in isolation fail at integration time. Interface requirements discovered during development are the most expensive to fix (late-change cost). At enterprise scale, undocumented "shadow integrations" — Zapier recipes, manual SFTP scripts, Excel macros — are the single most common source of audit findings and security incidents. An active-traffic reality check (90 days no traffic → retirement candidate; traffic without a register entry → governance violation) keeps the register honest.

## When To Use

- Pre-discovery for an enterprise-wide programme (ERP migration, M&A, core-system replacement) requiring a portfolio-level interface inventory.
- Drafting an integration target operating model: which team owns which interface, approval process, single source of truth.
- Building a cross-system traceability matrix (capability → process → system → interface) to scope SOWs and impact analyses.
- API contract governance: naming, versioning, deprecation, SLA, security baseline standards for all internal/external interfaces.
- Vendor/partner onboarding with 20+ interfaces requiring a criticality-rated register with renewal dates.
- Producing IT general controls evidence (SOC2, ISO 27001, GDPR Art. 30) listing every system-to-system data flow with PII classification.

## When NOT To Use

- Single feature with one external API call — use the per-interface spec in ba-modeling/interface-analysis.
- Greenfield startup with fewer than five systems — a one-page integration diagram is enough.
- Pure technical refactor (bumping protobuf version) where business capability mapping adds no decision value.
- Organisation lacks a system-of-record for applications (no APM/CMDB) — build that first.

## Content

| File | What's inside |
|------|---------------|
| `content/01-interface-types.xml` | Four interface types, five-step analysis procedure, data element specification, behavior definition, validation checklist. |
| `content/02-enterprise-landscape.xml` | Portfolio-level landscape register, shadow-IT discovery, agentic workflow (4-pass pattern), governance rules, anti-patterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/interface-specification.md` | Per-interface spec: overview, connected systems, data spec, technical spec, operational spec, error handling, security. |
| `templates/interface-catalog.md` | Interface catalog summary table with diagram placeholder and links to per-interface specs. |
| `templates/landscape-register.md` | Portfolio landscape register table (IF-ID, Source, Target, Channel, Criticality, Sensitivity, Owner, SLA, Standard?). |
| `templates/landscape-merge.sh` | Script: merge CMDB export + gateway dump → starter register.csv for BA enrichment. |
