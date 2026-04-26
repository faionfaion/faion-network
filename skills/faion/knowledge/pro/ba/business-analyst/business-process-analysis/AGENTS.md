# Business Process Analysis

## Summary

A five-stage methodology for documenting how work actually flows through an organization (current state), classifying each step as value-adding, business-necessary, or non-value-adding, and designing a measurable future state. At enterprise scale (M&A, ERP rollout, digital transformation), a portfolio agent maintains the process inventory while per-process agents apply the 5-stage loop against APQC PCF or SCOR reference frameworks.

## Why

Processes trapped in tribal knowledge produce inconsistent execution and hide inefficiencies. Quantifying NVA percentage before redesigning separates evidence-based improvement from gut-feel reorganizations. The `nva_minutes_per_year × feasibility` composite score prioritizes which processes to deep-model vs. document narratively only, preventing portfolio bloat.

## When To Use

- M&A integration requiring a Day-1/Day-100/target-state process comparison across two organizations' inventories.
- ERP/CRM/HCM rollout (SAP S/4HANA, Oracle Fusion, Workday) — gap-fit analysis against vendor reference processes.
- Digital transformation programme: 100-500 processes scored on maturity, automation readiness, and customer impact.
- Pre-IPO/pre-acquisition due diligence (SOX 404, ISO 9001) requiring auditor-grade process narratives with control points.
- Shared-services/GBS design consolidating multiple business units into one process model.

## When NOT To Use

- Single-team local workflow — use the `ba-modeling/business-process-analysis` variant; enterprise governance overhead is unjustified.
- Greenfield startup with no installed process estate — jump to use-case modeling or user-story-mapping.
- Pure customer-experience redesign — use customer-journey-mapping; BPA is a downstream consequence.
- Single broken process instance requiring root-cause analysis — use 5-whys/fishbone instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-process-stages.xml` | Five-stage BPA loop: identify, document, analyze (value/time/cost/quality/pain), design future state, validate. |
| `content/02-enterprise-scale.xml` | Portfolio-agent pattern, BPMN governance, reference-framework alignment, M&A and ERP-rollout specializations, anti-patterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/process-documentation.md` | Current-state process doc: overview, scope, actors, steps, business rules, exceptions, metrics. |
| `templates/process-analysis.md` | Analysis artifact: value classification, pain points, bottlenecks, improvement opportunities, future-state summary. |
| `templates/rank-portfolio.py` | Script: scorecard.csv → ranked.csv (top automation/redesign candidates by NVA × feasibility). |
