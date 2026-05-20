---
slug: email-preflight-checklist
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "a9d558fbf9799c19"
summary: Email Preflight Checklist delivers a concrete, testable methodology that turns the recurring task of 'Lifecycle email send + post-send analytics (per send)' into an auditable artefact, addressing the gap: growth-email-marketing covers theory but no concrete pre-send checklist — U
tags: [marketing, solo, checklist, methodology]
---
# Email Preflight Checklist

## Summary

**One-sentence:** Email Preflight Checklist delivers a concrete, testable methodology that turns the recurring task of 'Lifecycle email send + post-send analytics (per send)' into an auditable artefact, addressing the gap: growth-email-marketing covers theory but no concrete pre-send checklist — UTM, alt-text, plain-text, suppression list, spam-score. Solo marketers leak revenue here every send.

**One-paragraph:** growth-email-marketing covers theory but no concrete pre-send checklist — UTM, alt-text, plain-text, suppression list, spam-score. Solo marketers leak revenue here every send. Email Preflight Checklist closes this gap with a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. The methodology is anchored to the triggering work 'Lifecycle email send + post-send analytics (per send)' (role-growth-marketing, solo tier). It produces a structured artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'Lifecycle email send + post-send analytics (per send)' (role: role-growth-marketing) is in your current workload at least once per cycle.
- You have authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the artefact — human reviewer OR downstream agent.
- An auditable source-of-truth is available for the inputs the methodology needs.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer — artefact will be orphaned regardless of quality.
- Cannot access the input source-of-truth (system down, access denied) — paraphrased substitutes are worse than skipping.

## Prerequisites

- Read access to the systems / dashboards / docs that feed the methodology's inputs.
- A storage location for the produced artefact (git repo, doc, ticket) where the consumer can read it.
- Prior cycle's artefact (if any) accessible for carry-forward and trend comparison.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
| `solo/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `email_preflight_checklist_template_fill` | haiku | Template fill, no judgment |
| `email_preflight_checklist_evidence_check` | sonnet | Bounded comparison + judgment |
| `email_preflight_checklist_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `solo/marketing/` (see neighbouring methodologies)
- triggering activity: `role-growth-marketing/Lifecycle email send + post-send analytics (per send)`
- external: industry references cited inline in `content/01-core-rules.xml`
