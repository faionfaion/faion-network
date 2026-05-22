---
slug: traceability-auto-maintenance
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "2f766bc83892524e"
summary: Keeps the requirements traceability matrix live as the backlog churns — tracker-API ingest, link-drift detection, weekly reconciliation, AI-assisted broken-link repair — so the matrix stays useful past sprint 4.
tags: [traceability, requirements, ba, jira, ai-assisted-ba]
---

# Traceability Auto Maintenance

## Summary

**One-sentence:** Keeps the requirements traceability matrix live as the backlog churns — tracker-API ingest, link-drift detection, weekly reconciliation, AI-assisted broken-link repair — so the matrix stays useful past sprint 4.

**One-paragraph:** Static traceability matrices die within 4 sprints because tickets get renamed, deleted, merged, or split, while the matrix lives in a different document. This methodology binds the matrix to a tracker (Jira / Linear / GitHub Issues) via API ingest, runs a weekly link-drift detector (compares matrix references to current tracker state), and routes broken links through an AI-assisted repair queue (LLM proposes the most likely replacement, BA approves). Output: `TraceabilityReport` with link-health metrics + auto-generated repair PRs against the matrix file.

## Applies If (ALL must hold)

- BA maintains a requirements traceability matrix (CSV, ReqIF, Confluence, Notion DB)
- backlog lives in a tracker with REST/GraphQL API (Jira, Linear, GitHub, Azure DevOps)
- AI assistance is permitted on requirements artifacts (some regulated orgs forbid)
- matrix has ≥ 50 requirement rows with ≥ 1 link each (smaller doesn't need automation)

## Skip If (ANY kills it)

- requirements live entirely inside the tracker (no separate matrix) — use tracker's own coverage report
- tracker has no stable IDs (e.g. unscoped spreadsheet) — fix tracker discipline first
- regulated environment forbids LLM access to requirements — use the human-only `requirements-traceability` parent
- &lt; 50 rows — manual maintenance is cheaper than automation

## Prerequisites

- tracker API credentials (read + comment scope minimum)
- matrix file under source control OR API access
- canonical link types (e.g. "implements", "verified-by", "depends-on")
- weekly review slot for BA to approve repair queue

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/ba-core/requirements-traceability` | Defines matrix structure this methodology maintains |
| `pro/ba/business-analyst/ai-assisted-requirements-discovery` | Provides the LLM context for repair suggestions |
| `pro/pm/pm-traditional/change-management` | Consumes traceability impact analysis when backlog churns |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: API source-of-truth, drift detection cadence, AI-as-suggester not actor, link-type discipline, audit log | ~1000 |
| `content/02-output-contract.xml` | essential | `TraceabilityReport` + repair-suggestion schema | ~700 |
| `content/03-failure-modes.xml` | essential | 6 modes: stale cache, wrong repair, link-type collapse, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tracker_api_ingest` | haiku | API call + parse |
| `drift_detection_diff` | haiku | Set-diff |
| `repair_candidate_search` | sonnet | Semantic + textual matching |
| `impact_analysis_for_BA` | opus | Cross-requirement reasoning |
| `repair_PR_assembly` | sonnet | File-edit + commit |

## Templates

| File | Purpose |
|------|---------|
| `templates/traceability-report.json` | Output schema |
| `templates/repair-suggestion.json` | Per-link repair record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/drift-detect.py` | Weekly drift detection vs tracker | Cron Mon 09:00 |
| `scripts/repair-queue.py` | Run LLM repair suggestions over broken links | After drift-detect |

## Related

- parent skill: `pro/ba/business-analyst/`
- peer methodologies: `requirements-traceability`, `ai-assisted-requirements-discovery`
- external: [ISO/IEC/IEEE 29148:2018 requirements engineering](https://www.iso.org/standard/72089.html) · [INCOSE Guide for Writing Requirements](https://www.incose.org/) · [Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/) · [Karl Wiegers — Software Requirements (3rd ed.)](https://www.processimpact.com/)
