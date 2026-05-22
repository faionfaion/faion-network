---
slug: ai-assisted-velocity-anomaly-detection
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Detection protocol for ai assisted velocity anomaly detection — explicit signals, thresholds, and remediation paths so the failure mode is caught before it ships.
content_id: "9e2e894929e813ae"
tags: [ai, detection, pm]
---
# AI Assisted Velocity Anomaly Detection

## Summary

**One-sentence:** Detection protocol for ai assisted velocity anomaly detection — explicit signals, thresholds, and remediation paths so the failure mode is caught before it ships.

**One-paragraph:** Detection protocol for ai assisted velocity anomaly detection — explicit signals, thresholds, and remediation paths so the failure mode is caught before it ships. Geek/pm has 'ai-in-project-management' as an overview but no concrete recipe for hooking an LLM/anomaly model to burndown signals — direct fit for the AI Gantt pain point.

## Applies If (ALL must hold)

- You instrument or audit for the specific failure mode addressed by ai assisted velocity anomaly detection.
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
| `geek/pm/pm-agile/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

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

- parent skill: `geek/pm/pm-agile/`
- peer methodologies: see siblings under `geek/pm/pm-agile/`
- external: industry references cited inline in `content/01-core-rules.xml`
