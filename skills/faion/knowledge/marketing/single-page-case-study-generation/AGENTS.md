# Single Page Case Study Generation

## Summary

**One-sentence:** A one-page case-study template tuned for service engagements (not SaaS feature launches) with six required slots — problem, approach, outcome, numbers, pull-quote, NDA-safe fallback — so every finished freelance project becomes a reusable sales asset within a week of delivery.

**One-paragraph:** Every finished engagement is a sales asset, but freelancers never write it up because there is no template. The case-study mentions in product/product-lifecycle are SaaS-feature-launch flavor, not service-engagement flavor. This methodology codifies the six required slots, the NDA-redaction fallback (so confidential clients still produce a usable anonymous case), and a one-week-from-delivery deadline so the write-up happens while results and quotes are still fresh.

**Ефективно для:**

- Закритого freelance-проекту: 7 днів на драфт, 14 на публікацію.
- NDA-fallback версія: industry + size + role без імен.
- Шість обов'язкових слотів (problem/approach/outcome/numbers/quote/NDA).
- Outcome-review: чи кейс справді конвертує prospects на discovery-call.

## Applies If (ALL must hold)

- The engagement is delivered and paid within the last 30 days, and the client contact is reachable for a quote and permission.
- At least one quantitative outcome has a baseline and a final value readable from a system the freelancer can export (Stripe, server logs, GA4, calendar, P&L, ticket tracker).
- The client will agree in writing to a named study or to an anonymised one (industry, size band, context, quoted role).
- The study will be used as a sales asset with a discovery-call booking link that can carry a tracking parameter.
- The freelancer can store the evidence exports and the permission message privately for as long as the study is published.

## Skip If (ANY kills it)

- The engagement produced no measurable outcome with a baseline: log it in one line; a study on adjectives is not written.
- Delivery was more than 30 days ago with no draft: log as missed and add the 7-day draft task to the next delivery checklist.
- The client has refused both the named and the anonymised version in writing: one-line internal log only.
- What is needed is a SaaS feature-launch case study with product analytics, not a service-engagement page.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Delivery record | final delivery date and paid invoice | invoicing tool |
| Evidence exports | baseline and final values with their measurement window from Stripe, server logs, GA4, calendar, P&L or ticket tracker | the client's systems, exported and stored privately |
| Publication permission | written agreement to the named or anonymised version | client contact, by email or message |
| Verbatim quote | one sentence from a named contact with written permission to publish | client contact, by email or message |
| Discovery-call link | booking URL with a UTM or tracking parameter | freelancer's site or scheduling tool |
| `templates/single-page-case-study-generation.md.j2`, `templates/single-page-case-study-generation.json` | one-page skeleton; the contract schema | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/proposal-from-discovery-template` | Upstream artefact template that anchors this methodology's recurring loop. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions; artefact lives in the team's SDD space. |

## Content (load on demand)
| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: six slots on one page, numbers as baseline/final/delta, evidence source named and kept, verbatim quote with written permission, NDA fallback never dropped, 7-day draft / 14-day publish, outcome-first headline, single tracked CTA | 2550 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the case-study report: named or anonymised version, delivery, draft and publish-or-park dates in the 7- and 14-day windows, outcome-first title with a number, six slots with sentence counts, numbers as baseline, final, delta, unit, window and source system, verbatim quote with permission, anonymisation block, evidence in inputs_used, one tracked CTA, 90-day review; valid and invalid reports; 8 forbidden patterns | 4750 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with description + reason + repair | 950 |
| `content/04-procedure.xml` | essential | 8 steps: confirm a defensible number inside the window, export and store the evidence, get the version and the quote in writing, draft the six slots within 7 days, write the outcome-first title, fit one page, add one tracked CTA, publish or park within 14 days, validate and schedule the review | 1650 |
| `content/05-examples.xml` | recommended | Complete report for a fintech checkout-latency engagement (named version, 5 and 12 days after delivery, 62 percent headline, two sourced numbers, VP quote with email permission, 310 words, one UTM-tracked CTA, review at 90 days) with a note per value, plus a service-first write-up five months late and what the validator prints | 2000 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule; read before drafting. | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list, low cost. |
| `populate-evidence-fields` | sonnet | Per-section judgment: select correct evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change behaviour at the next iteration? |

## Templates

| File | Purpose |
|------|---------|
| `templates/single-page-case-study-generation.md.j2` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/single-page-case-study-generation.md` | Markdown skeleton (5-line header) for the artefact body. Generated from `templates/single-page-case-study-generation.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/single-page-case-study-generation.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-single-page-case-study-generation.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- upstream playbook: `p3-technical-freelancer/Productize a recurring engagement into a fixed-scope offer`
- parent skill: `pro/marketing/`
- related methodology: `pro/marketing/testimonial-capture-microsurvey`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.
