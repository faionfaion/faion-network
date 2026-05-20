---
slug: ai-orphan-link-detection
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Detection protocol for ai orphan link detection — explicit signals, thresholds, and remediation paths so the failure mode is caught before it ships.
content_id: "7d8a17cde2e47b5c"
tags: [ai, detection, sdlc-ai]
---
# AI Orphan Link Detection

## Summary

**One-sentence:** Detection protocol for ai orphan link detection — explicit signals, thresholds, and remediation paths so the failure mode is caught before it ships.

**One-paragraph:** Detection protocol for ai orphan link detection — explicit signals, thresholds, and remediation paths so the failure mode is caught before it ships. Traceability decays. A geek-tier methodology using LLM + graph traversal to detect orphan requirements, broken stories, and trace gaps in Jira/ADO export — a USP for the geek tier.

## Applies If (ALL must hold)

- You instrument or audit for the specific failure mode addressed by ai orphan link detection.
- Signals are observable in code, logs, or artefacts you control.
- Each detection has a remediation path — detection without repair is theater.
- False-positive rate budget is set before deploying the detector.

## Skip If (ANY kills it)

- Detectors with no remediation path — alarm fatigue without action is worse than silence.
- Hypothetical failure modes never observed in production data.
- Costs of false positive > cost of missed failure (e.g., halting prod on flaky signal).

## Prerequisites

- Signal source instrumented (log line, metric, lint rule, scanner).
- Channel for alerts agreed (Slack, PagerDuty, dashboard).
- Remediation playbook or runbook ready for each detector firing.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | The 4 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `signal_capture` | haiku | Pattern matcher, no judgment |
| `severity_assignment` | sonnet | Anchored severity per detector hit |
| `policy_synthesis` | opus | When detectors accumulate, propose root-cause fix |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `geek/sdlc-ai/`
- peer methodologies: see siblings under `geek/sdlc-ai/`
- external: industry references cited inline in `content/01-core-rules.xml`
