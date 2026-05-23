# Solo Testimonial Extraction Script

## Summary

**One-sentence:** Generates a 3-question testimonial outreach + a structured Testimonial JSON (hesitation, outcome, anti-recommendation) consumable by case-study templates.

**One-paragraph:** Sean D'Souza and Joanna Wiebe documented a 3-question structure that flips testimonial extraction from 'write something nice' to a guided interview: (1) what was the hesitation before buying, (2) what happened that made it worth it, (3) who would you NOT recommend this to. The third question disarms generic praise and produces specific, credible language. Output: a `Testimonial` JSON with hesitation, outcome, anti-recommendation, consent flag, and 90-day follow-up reminder.

**Ефективно для:**

- Recently closed engagement that delivered a measurable outcome.
- Building social proof for a Solo product's landing page.
- Recording credible quotes for case studies without ghostwriting.
- Standardising the 90-day post-engagement testimonial harvest.

## Applies If (ALL must hold)

- Engagement closed ≤14 days OR customer hit a measurable milestone.
- Customer has been billed and paid (no free / trial users).
- Customer is reachable by email or DM.
- Operator needs case-study or social-proof content this quarter.

## Skip If (ANY kills it)

- Engagement was rocky or NPS &lt;7 — pulling a testimonial forces a lie.
- Customer is under NDA / corporate gag — request anonymous case study instead.
- Customer asked NOT to be public — respect immediately.
- &gt;90 days since milestone — memory decay; testimonial becomes vague.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Outcome metric | specific (revenue / time saved / bug fixed) with number | operator |
| Relationship history | first name + prior thread + last touchpoint | CRM |
| Case-study template | downstream consumer of the JSON | marketing |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[solo-support-sla-template]] | happy ticket → testimonial pipeline |
| [[business-storytelling]] | downstream — testimonial fits Pixar case study |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routes by observable signal to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `outreach-draft` | haiku | Template fill. |
| `response-parse` | sonnet | Quote extraction with bounded judgment. |
| `display-variants` | sonnet | 3 lengths (full / mid / short). |

## Templates

| File | Purpose |
|------|---------|
| `templates/outreach-email.md` | 3-question testimonial outreach skeleton |
| `templates/testimonial.json` | Output JSON skeleton with consent fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-testimonial-extraction-script.py` | Validate solo-testimonial-extraction-script artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[solo-support-sla-template]]
- [[business-storytelling]]
- [[storytelling]]

## Decision tree

See `content/06-decision-tree.xml`. Gates on NPS, recency, and consent; failure at any gate halts. Otherwise emits a complete Testimonial JSON.
