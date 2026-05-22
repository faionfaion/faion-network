---
slug: agency-decline-templates
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Reusable template for agency decline templates that codifies the structure, named fields, and decision points so each new instance ships in minutes instead of being re-invented.
content_id: "2f09102bedaa4313"
tags: [agency, marketing, template]
---
# Agency Decline Templates

## Summary

**One-sentence:** Reusable template for agency decline templates that codifies the structure, named fields, and decision points so each new instance ships in minutes instead of being re-invented.

**One-paragraph:** Reusable template for agency decline templates that codifies the structure, named fields, and decision points so each new instance ships in minutes instead of being re-invented. Bad-fit-lead decline is a high-leverage moment and there is no methodology for graceful 'no' templates that protect positioning and seed referrals.

## Applies If (ALL must hold)

- You are starting a new instance of the artefact addressed by agency decline templates (kickoff, contract, brief, deck).
- The instance has a named owner and a target review date.
- Filled fields will be read by humans outside the author's team (clients, contractors, executives).
- Sensitive data (contract terms, salary, IP) is captured but redacted before broad sharing.

## Skip If (ANY kills it)

- First instance ever, no comparable past work — write freeform, extract a template after.
- One-off bespoke artefact (M&A doc, lawsuit, novel R&D) — template constrains the wrong axes.
- Localized cultural or regulatory context the template does not encode — start from local norms.

## Prerequisites

- Empty instance of the artefact created and named (filename, doc ID).
- Required input metadata reachable (parties, dates, scope, budget).
- Reviewer identified with deadline acknowledged.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | The 4 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `structural_fill` | haiku | Slot in known fields from inputs |
| `ambiguity_resolution` | sonnet | Resolve open fields against context |
| `stakeholder_voice` | opus | Write narrative sections coherent with strategy |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `solo/marketing/content-marketer/`
- peer methodologies: see siblings under `solo/marketing/content-marketer/`
- external: industry references cited inline in `content/01-core-rules.xml`
