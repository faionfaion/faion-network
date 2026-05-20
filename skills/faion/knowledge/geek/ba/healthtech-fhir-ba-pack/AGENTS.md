---
slug: healthtech-fhir-ba-pack
tier: geek
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: FHIR resources (Patient, Encounter, Observation, Condition), HIPAA/GDPR overlap, IRB/consent flows, audit-trail requirements — the HealthTech vertical pack the corpus lacks.
content_id: "856493a66c147273"
tags: [healthtech-fhir-ba-pack, ba, geek]
---

# HealthTech FHIR BA Pack

## Summary

**One-sentence:** FHIR resources (Patient, Encounter, Observation, Condition), HIPAA/GDPR overlap, IRB/consent flows, audit-trail requirements — the HealthTech vertical pack the corpus lacks.

**One-paragraph:** HealthTech engagements need FHIR familiarity, HIPAA/GDPR overlap, IRB/consent, audit-trail. None of this is in faion. Output: FHIR resource map + compliance checklist + consent flow + audit-log spec.

## Applies If (ALL must hold)

- BA on a HealthTech engagement
- scope includes patient data, clinical records, or healthcare provider workflow
- client jurisdiction subjects them to HIPAA, GDPR-Health, or equivalent

## Skip If (ANY kills it)

- consumer wellness app with no clinical record
- B2B health-IT-tooling for non-clinical staff (HR, scheduling)
- client has dedicated HealthTech BA team — augment, don't duplicate

## Prerequisites

- list of patient-data fields needed
- client's existing EMR / EHR + integration scope
- HIPAA Business Associate Agreement or GDPR Data Processing Agreement reviewed

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent skill — provides operating context for this methodology |
| `pro/ba/business-analyst` | peer methodology — produces inputs or consumes outputs |
| `pro/sec/data-classification` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `pro/ba/business-analyst/`
- peer methodology: `pro/ba/business-analyst`
- peer methodology: `pro/sec/data-classification`
- external: https://www.hl7.org/fhir/ (HL7 FHIR R5); https://www.hhs.gov/hipaa/ (HHS HIPAA); https://gdpr.eu/article-9-special-categories-of-data/
