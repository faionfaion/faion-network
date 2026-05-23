# Proposal From Discovery Template

## Summary

**One-sentence:** A one-page three-option proposal template fed directly from discovery-call notes, with fixed sections, evidence anchors, a named owner, and a published outcome-review cadence.

**One-paragraph:** Solo technical freelancers lose inbound deals on slow proposal turnaround. The upstream `discovery-call-structure` methodology produces verbatim pain notes but stops there; this methodology converts those notes into a committed one-page artefact with three offers (light / standard / outcome-based), each anchored to an evidence link, owned by a named person, and reviewed against close-rate at the next iteration. Mechanism: rule-bound output contract + per-application evidence + outcome review. Primary output: a versioned, owned, evidence-anchored proposal document the freelancer can send within the same client-cycle as the discovery call.

**Ефективно для:**

- Одного фрілансера, що закриває inbound-ліди в межах одного циклу спілкування.
- Конвертації нотаток discovery-call у три ціновані опції на одну сторінку.
- Регулярного outcome-review: чи проп з шаблону справді закриває угоди частіше.
- Командного контролю якості — фіксована форма + іменований власник + версія.

## Applies If (ALL must hold)

- The freelancer runs the inbound-to-signed-retainer loop on a recurring cadence (≥1/month).
- Upstream `discovery-call-structure` notes (verbatim pain + budget signal) are available.
- The freelancer owns the artefact (or escalates ownership to a named person).
- The team has a version-controlled or wiki-style space where the artefact lives.

## Skip If (ANY kills it)

- One-off deal with no recurrence — write a single doc, not a versioned artefact.
- Fewer than 3 inbound proposals per year — review cadence costs more than it returns.
- Procurement-led RFP that mandates a different shape — fill the RFP's template instead.
- No named owner is available — defer until ownership is resolved.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Discovery-call notes | Markdown / transcript | upstream `discovery-call-structure` |
| Rate card | JSON / sheet | freelancer's pricing doc |
| Three offer scaffolds | YAML | this methodology's `templates/skeleton.md` |
| Repository / wiki path | URL | team knowledge space |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/rate-raise-conversation-script` | Anchors pricing language for the outcome-based option. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions; artefact lives in SDD space. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: fixed shape, evidence anchors, named owner, version+last_reviewed, outcome review | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure: notes → scaffold → fill → review → commit | ~800 |
| `content/05-examples.xml` | essential | One worked proposal end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Mechanical fill from header + section list. |
| `populate-evidence-fields` | sonnet | Per-section judgment: pick the right evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change close-rate? |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Canonical section list with `not_applicable: <reason>` markers per section. |
| `templates/header.yaml` | Frontmatter schema: owner, version, last_reviewed, evidence_root. |
| `templates/proposal-from-discovery-template.json` | JSON schema for the output contract. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-proposal-from-discovery-template.py` | Validate a filled artefact against the schema in `02-output-contract.xml`. | Pre-commit; before sending to client. |

## Related

- [[rate-raise-conversation-script]]
- [[single-page-case-study-generation]]
- [[retainer-pricing-methodology]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (inbound count, has_discovery_notes, named_owner_present, recurrence_per_year) to a rule from `01-core-rules.xml`. Use it whenever an inbound lead lands and you have to decide between filling the proposal template, deferring (no owner), or writing a one-off email.

