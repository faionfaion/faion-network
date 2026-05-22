<!--
purpose: Canonical vendor-risk assessment skeleton.
consumes: header frontmatter + DPA + subprocessor list + data-flow diagram.
produces: A SOC2 / GDPR-aligned, versioned, owner-signed assessment.
depends-on: ../scripts/validate-vendor-risk-assessment-template.py.
token-budget-impact: ~600 tokens when filled.
-->

---
artefact_id: "<vendor-slug>-risk-assessment"
vendor_name: "<Vendor Inc.>"
owner: "compliance-lead:<person>"
version: "1.0.0"
last_reviewed: "2026-05-22"
risk_rating: "medium"
status: "active"
inputs_used:
  - name: "DPA"
    source: "<vendor-dpa-url>"
  - name: "Subprocessor list"
    source: "<vendor-subprocessor-url>"
---

# Vendor Risk Assessment — <Vendor>

## Data scope

<What customer data / PII / credentials the vendor processes>

## DPA reference

- URL: <link>
- Last reviewed: <ISO date>

## Subprocessors

<list, each with sub-vendor name + DPA link>

## Data residency

<region(s), with citation to vendor SOC2 / contract clause>

## Encryption at rest

<yes/no + algorithm + key management notes>

## Retention

<days; cite policy>

## Breach notification SLA

<hours; cite contract>

## Risk rating + rationale

<low|medium|high|critical> — <2-3 sentences citing the inputs above>

## Decisions / Actions / Next review

- <decision 1>
- Next review: <ISO date, ≤90 days>
