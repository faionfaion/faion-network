<!--
purpose: Canonical skeleton for the `healthtech-fhir-ba-pack` artefact — one section per rule in content/01-core-rules.xml.
consumes: Feature data model, architecture diagram, contracts register, consent texts, IRB approval, log and store inventory.
produces: A committed pack at .product/healthtech-fhir-ba-pack/<feature>.md plus its JSON form validated by scripts/validate-healthtech-fhir-ba-pack.py.
depends-on: templates/header.yaml, content/02-output-contract.xml, scripts/validate-healthtech-fhir-ba-pack.py.
token-budget-impact: ~1500 tokens to fill end-to-end.
-->
---
version: 0.1.0
feature_name: <feature_name>
fhir_version: <fhir_version>
profile: <profile>
privacy_officer: <privacy_officer>
---

# Feature and regimes

- feature_name: <feature_name>
- regimes: hipaa true | false; gdpr true | false; nhs true | false
- fhir_version: <fhir_version> (R4 | R5)
- profile: <profile> (US Core, UK Core, or the customer's named profile)

# FHIR element map

One row per clinical element (r-clinical-elements-map-to-fhir-resources). Coded elements carry a standard binding (r-coded-terminology-bindings).

| Clinical element | Resource | Element path | Coded | Code system | System URI | Value set |
|---|---|---|---|---|---|---|
| <systolic blood pressure> | Observation | Observation.component.value[x] | true | LOINC | http://loinc.org | 8480-6 |
| <diagnosis> | Condition | Condition.code | true | SNOMED CT | http://snomed.info/sct | <code> |

# PHI data flows

One row per boundary crossed (r-phi-minimum-necessary-per-flow). Analytics and model-training rows are safe-harbor or expert-determination with the method named.

| From | To | PHI elements crossing | Purpose | De-identification | Method | Excluded at boundary |
|---|---|---|---|---|---|---|
| <service> | <service or vendor> | <element paths> | treatment | none | — | <element paths> |
| <service> | <analytics store> | <element paths> | analytics | safe-harbor | <18 identifier classes stripped; job name> | <element paths> |

# Processors

Every third party touching PHI (r-baa-or-dpa-per-processor). PHI in scope without a signed BAA is blocking.

| Processor | Service kind | PHI in scope | BAA signed | Signed on | Art. 28 signed | Evidence | Status |
|---|---|---|---|---|---|---|---|
| <vendor> | cloud-host | true | true | YYYY-MM-DD | true | <URL> | cleared |

# HIPAA-GDPR overlap matrix

Required when hipaa and gdpr are both true (r-hipaa-gdpr-overlap-matrix-minimum-rows). Five mandatory rows.

| Row | HIPAA position | GDPR position | Design decision | Stricter clock honoured |
|---|---|---|---|---|
| lawful_basis | <45 CFR §164.506 permitted use> | <Art. 6 + Art. 9(2)(h)> | <decision> | <clock> |
| breach_notification_clock | <60 days, §164.404> | <72 hours, Art. 33> | <decision> | 72 hours |
| individual_access | <30 days, §164.524> | <one month, Art. 15> | <decision> | 30 days |
| retention_and_deletion | <six years, §164.316(b)(2)> | <erasure, Art. 17> | <decision> | <clock> |
| cross_border_transfer | <no restriction> | <Chapter V> | <decision> | <clock> |

# Consent model

- model: fhir-consent | equivalent-record
- research_use: true | false
- irb: protocol_number <IRB-...>; approval_date YYYY-MM-DD; waiver_of_consent true | false; committee <name>

| Kind | Scope | Provisions (action / data category / purpose) | Period | Text version | Capture (timestamp field, channel) |
|---|---|---|---|---|---|
| treatment | <scope> | permit / <category> / treatment | <start>–<end> | <version> | Consent.dateTime, mobile |
| research | <scope> | permit / <category> / research; deny / <category> / research | <start>–<end> | <version> | Consent.dateTime, mobile |

# Audit trail

- model: fhir-auditevent | equivalent-schema
- fields: actor, subject_id, action, timestamp, source_system, purpose
- append_only: true
- application_roles_with_update_or_delete: none
- retention_years: <6 or more>
- per_patient_query: true
- storage: <where and which index makes per-patient query possible>

# Encryption inventory

| Store | Kind | Encrypted at rest | Key management separated | Status |
|---|---|---|---|---|
| <store> | database | true | true | cleared |
| <backup bucket> | backup | true | true | cleared |

| Hop from | Hop to | TLS minimum |
|---|---|---|
| <service> | <service> | 1.2 |

# Blocking findings

- <processor without agreement, unencrypted store, identified-PHI analytics flow; or "none">
