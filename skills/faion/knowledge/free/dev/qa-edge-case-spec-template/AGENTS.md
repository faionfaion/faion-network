---
slug: qa-edge-case-spec-template
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a Given/When/Then edge-case test-data spec linked to the originating incident, with named owner, evidence anchors, and a next-review date.
content_id: "6310c6abbd0ea3e9"
complexity: light
produces: spec
est_tokens: 3400
tags: [qa, edge-case, test-data, given-when-then, regression]
---
# QA Edge Case Spec Template

## Summary

**One-sentence:** Pins a Given/When/Then edge-case spec to a fixed shape so test-data setup for tricky scenarios becomes a reviewable artefact, not folklore.

**One-paragraph:** Produces a versioned, owned, evidence-anchored Given/When/Then spec for a tricky edge case, linked to the originating incident (Sentry issue, customer ticket, post-mortem) and committed to the team's knowledge space. Fixed section list — practitioners fill, never invent. Carries `version`, `owner`, `last_reviewed`, evidence links, and an explicit "decisions / actions / next-review" block.

**Ефективно для:** QA інженера після інциденту — закриває петлю між багом і запіненим регресійним тестом.

## Applies If (ALL must hold)

- An incident, ticket, or post-mortem produced a tricky-scenario edge case worth pinning.
- The team has a recurring need to reproduce that scenario (≥ 3 expected hits per year).
- There is a named owner accountable for refreshing the artefact.
- The team uses a version-controlled or wiki-style space where the artefact will live.
- The trigger event is observable (Sentry alert, ticket, threshold, schedule).

## Skip If (ANY kills it)

- One-shot work with no recurrence — write a single test, not a versioned artefact.
- Team has < 3 instances per year — review cadence costs more than it returns.
- Regulated context that mandates a different spec format (use the regulator's template).
- No named owner is available — defer until ownership is resolved; anonymous artefacts rot.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Originating incident link | URL | Sentry / Jira / GitHub Issue |
| Reproduction steps | text | post-mortem or QA notes |
| Test environment fixture set | code | `tests/fixtures/` or factory module |
| Named owner | role + person | team roster |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/regression-test-first-bugfix-workflow` | Defines the bug → test → fix flow this spec slots into. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions; artefact lives in the team's SDD space. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: fixed shape, evidence anchors, owner+version, fill budget ≤30 min, decisions/actions block | ~1000 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, self-check checklist | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |
| `content/05-examples.xml` | medium | One full filled spec for a real-shaped edge case | ~500 |
| `content/06-decision-tree.xml` | essential | When to write a full spec vs an inline test comment | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list, low cost. |
| `populate-evidence-fields` | sonnet | Per-section judgment: select correct evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the pinned spec change downstream behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Canonical section list with `not_applicable: <reason>` markers per section. |
| `templates/header.yaml` | Frontmatter schema: owner, version, last_reviewed, evidence_root, incident_url. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-edge-case-spec-template.py` | Validate that filled artefact matches the canonical schema, carries evidence links, owner, and not-stale `last_reviewed`. | Pre-merge and weekly staleness scan. |

## Related

- [[regression-test-first-bugfix-workflow]] — outer flow this spec is the inner artefact of.
- [[django-pytest]] — common runner the resulting test plugs into.
- [[api-testing]] — sibling spec format for API-shaped edge cases.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides whether the case warrants a full pinned spec (≥3 expected hits/year, named owner, evidence ≥1) or a smaller pytest comment + `pytest.mark.regression`. Use it the moment the QA engineer hits a tricky scenario in triage — before they start typing the spec.
