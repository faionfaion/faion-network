---
slug: utm-taxonomy-discipline
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "5822288a2a59308e"
summary: "Utm Taxonomy Discipline: produces a versioned, owner-signed artefact that closes the gap 'role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization'."
tags: [utm-taxonomy-discipline, marketing, solo]
---
# Utm Taxonomy Discipline

## Summary

**One-sentence:** Utm Taxonomy Discipline: produces a versioned, owner-signed artefact that closes the gap 'role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization'.

**One-paragraph:** Addresses the gap surfaced by 'role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization': Basic but missing. A consistent UTM taxonomy (source/medium/campaign/content/term conventions + naming rules + registry) is the foundation of all attribution. Without it, no downstream analysis works. Faion has analytics-setup methodologies but no naming-discipline methodology. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a utm taxonomy discipline artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working utm taxonomy discipline artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/marketing` | parent domain group — provides operating context for Utm Taxonomy Discipline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules grounded in the cited gap | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/utm-taxonomy-discipline.json` | JSON schema for the Utm Taxonomy Discipline output contract |
| `templates/utm-taxonomy-discipline.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-utm-taxonomy-discipline.py` | Enforce Utm Taxonomy Discipline output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/marketing/`
- upstream playbook: `role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization`
- solo/marketing/role-growth-marketing
