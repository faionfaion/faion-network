# HealthTech FHIR BA Pack

## Summary

**One-sentence:** Produces a HealthTech BA pack — FHIR resources (Patient, Encounter, Observation, Condition), HIPAA/GDPR overlap matrix, IRB/consent workflow, and audit-trail spec — so clinical features ship without a post-launch privacy incident.

**One-paragraph:** Produces a HealthTech BA pack — FHIR resources (Patient, Encounter, Observation, Condition), HIPAA/GDPR overlap matrix, IRB/consent workflow, and audit-trail spec — so clinical features ship without a post-launch privacy incident. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** business analysts on US-HIPAA, EU-GDPR, or NHS engagements who must shape clinical features against FHIR R4/R5 resources, BAA boundaries, consent capture, and immutable audit trails before code is written.

## Applies If (ALL must hold)

- The feature reads, writes or transmits identifiable health data: PHI under HIPAA, special-category data under GDPR Art. 9, or NHS patient data.
- The FHIR release (R4 or R5) and the implementation guide in force (US Core, UK Core, or the customer's profile) are known, so element paths and bindings can be fixed.
- An architecture diagram or service inventory exists, so every boundary a record crosses and every third-party processor can be enumerated.
- The contracts register (BAAs, Art. 28 agreements) and the consent texts are accessible, and an IRB or ethics approval exists for any research use.
- A privacy or compliance officer is named to review the pack before code is written.

## Skip If (ANY kills it)

- No identifiable health data is in scope (wellness content, de-identified aggregates only, or a marketing site); use the ordinary privacy BA pack instead.
- The organisation already holds a current, signed pack for this exact feature (FHIR map, flow table, processor list, consent model, audit spec); update it rather than producing a second one.
- The feature is a pure EHR pass-through where the EHR vendor owns the FHIR mapping, consent and audit trail and no data lands in your own stores.
- No privacy officer will engage; the pack cannot be reviewed and the work belongs upstream with the compliance function.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Feature data model and screen inventory | ERD, migrations or field list | engineering / product |
| FHIR release and implementation guide | R4 or R5; US Core / UK Core / named profile with version | integration lead |
| Architecture diagram with vendors and environments | diagram or service inventory | engineering |
| Contracts register with BAA / Art. 28 status | list with signed dates and PDFs | legal / procurement |
| Consent texts and IRB approval | versioned consent text; protocol number and approval letter | clinical lead / IRB |
| Store and log inventory with encryption settings | list of databases, backups, indexes, logs, queues | SRE |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: FHIR resource mapping, terminology bindings, minimum-necessary flow table, BAA / Art. 28 per processor, HIPAA-GDPR matrix rows, FHIR Consent with IRB reference, append-only six-year audit trail, encryption in transit and at rest | ~2350 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for the pack: element_map with FHIR resource, path and terminology binding, data_flows with de-identification forced on analytics and training, processors with BAA status forced to blocking without agreement, five-row overlap matrix when both regimes apply, FHIR Consent records with IRB, audit trail six fields / append-only / six years, encryption per store and hop; valid and invalid examples | ~7000 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with detector + repair | ~900 |
| `content/04-procedure.xml` | recommended | 9 steps: FHIR element map, terminology bindings, PHI flow table, processors and agreements, overlap matrix, consent and IRB, audit trail, encryption inventory, validate and file | ~2050 |
| `content/05-examples.xml` | recommended | Complete remote blood-pressure monitoring pack with notes on every non-obvious value, plus a symptom-checker pack breaking six rules and what the validator and privacy officer say | ~3600 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Parse inputs + check preconditions | haiku | Mechanical schema parse. |
| Author the artefact body | sonnet | Bounded synthesis from typed inputs. |
| Review for compliance + cross-cutting impact | opus | Cross-input judgement when stakes are high. |
| Outcome-review synthesis at cadence | opus | Did the artefact change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | Markdown skeleton of the artefact with all required sections. |
| `templates/skeleton.md` | Markdown skeleton of the artefact with all required sections. Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum-viable filled JSON instance, parseable by the validator. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-healthtech-fhir-ba-pack.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
