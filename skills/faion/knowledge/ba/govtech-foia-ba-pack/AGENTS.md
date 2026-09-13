# GovTech FOIA / Records-Retention BA Pack

## Summary

**One-sentence:** Produces a public-sector BA pack — FOIA/records-retention schedule, WCAG AA accessibility audit plan, procurement-clause review log, and comment-period buffer — that closes the design-time gaps that bite GovTech launches.

**One-paragraph:** Produces a public-sector BA pack — FOIA/records-retention schedule, WCAG AA accessibility audit plan, procurement-clause review log, and comment-period buffer — that closes the design-time gaps that bite GovTech launches. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** business analysts on US-federal, US-state, UK, EU-member, or CA-federal/provincial engagements who must surface FOIA, records-retention, accessibility (Section 508 / EN 301 549), and procurement clauses before a public-sector launch turns into a legal incident.

## Applies If (ALL must hold)

- The system is operated by or for a public body subject to access-to-information and records law (US federal or state, UK, EU institution, Canadian federal or provincial).
- The data model exists at least as an ERD or migration set, so record classes and fields can be enumerated and tagged.
- The agency's records officer and its Chief FOIA Officer / FOI officer (or delegate) are identified and available to sign the schedule and the export paths.
- The contract or solicitation text is in hand, so clauses can be logged against design decisions while the design is still cheap to change.
- A launch date is proposed, so the public-notice buffer can be tested against it.

## Skip If (ANY kills it)

- The system is private-sector with no public-body operator; use the ordinary privacy and accessibility methodologies instead.
- The agency already has a signed, current retention schedule, export runbook, exemption map and accessibility plan covering this exact system; update that pack rather than producing a second one.
- The system stores no records at all (a stateless static site with no forms, uploads, logs or messaging) and has no public-facing flow to audit.
- No records officer exists or will engage; the pack cannot be approved and the work belongs upstream with the agency's records-management function.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Data model with stores and fields | ERD, migrations or schema dump | engineering repo |
| Schedule authority for the jurisdiction | NARA GRS / agency schedule, Public Records Act 1958 body schedule, state or provincial archives schedule (PDF or URL) | agency records officer |
| Statutory access-request clock | working days per statute (5 U.S.C. §552(a)(6)(A)(i); FOIA 2000 s.10; Reg. 1049/2001; Access to Information Act) | agency counsel / FOI officer |
| Contract, solicitation and framework clauses | PDF or clause register | procurement |
| Public-facing page and flow inventory | list with URLs | product / design |
| Proposed launch date and notice regime | date plus PRA / APA / consultation determination | programme manager |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: retention schedule per record class, export within statutory clock, exempt fields tagged, ephemeral channels captured, WCAG AA launch gate, clause review log, public-notice buffer, named officers | ~2450 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for the pack: record_classes with finite retention and schedule item, data_stores with export path and lead time capped at the 20-day clock for us-federal / uk, exemption_map, staff_channels, WCAG AA audit with launch gate, seven-topic clause log, public_notice buffer >= 90, both officers; valid and invalid examples | ~6200 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with detector + repair | ~900 |
| `content/04-procedure.xml` | recommended | 9 steps: record classes and schedule, export path per store, exemption map, staff channels, accessibility plan, clause log, notice buffer, officer signatures, validate and file | ~2200 |
| `content/05-examples.xml` | recommended | Complete state benefits portal pack with notes on every non-obvious value, plus a federal grants pack breaking four rules and what the validator and reviewer say | ~3150 |
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
| `scripts/validate-govtech-foia-ba-pack.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
