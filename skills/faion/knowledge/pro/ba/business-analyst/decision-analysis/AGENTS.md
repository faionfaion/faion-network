# Decision Analysis

## Summary

A six-step structured evaluation framework: define the decision, generate options (including do-nothing), elicit weighted criteria individually per stakeholder then reconcile high-variance weights, route scoring by domain expertise (Security scores Security criteria, Finance scores Cost), run sensitivity analysis (±20% on weights), and produce a Decision Analysis Document that traces every criterion to a requirements catalog entry. The BA owns the process; agents own the artifacts.

## Why

Without a structured framework, decisions are made by the loudest voice and the rationale evaporates. Auditors returning 12 months later ask "why this option?" — the Decision Analysis Document is the answer. Criteria traced to requirements prevent the "we evaluated on features the business never asked for" failure mode. Individual weight elicitation before group reconciliation prevents anchor bias from dominant stakeholders.

## When To Use

- Enterprise vendor/platform/package selection (CRM, ERP, ITSM, IdP) with 3+ candidates and 5-7 stakeholder groups.
- Build-vs-buy-vs-extend evaluations where Finance, Architecture, Security, and Operations each weight criteria differently.
- Approval-gate decisions in regulated environments (banking, healthcare, gov) where auditors require documented rationale.
- Investment/portfolio prioritization where the same matrix template is reused across N initiatives.
- Solution evaluation at the end of a BA cycle (BABOK KA 7) comparing candidates against elicited requirements.
- Steering committee deadlock where members are arguing intuitions rather than criteria.

## When NOT To Use

- Decisions inside one team's autonomy (npm package choice, CI runner version) — use a 5-line ADR.
- Pure financial decisions with quantifiable cash flows — use NPV/IRR/payback, not 1-5 scoring.
- Strategic direction questions ("should we enter market X?") — use scenario planning / BABOK KA 6 strategy analysis.
- When the decision-maker has already decided and asked the BA for cover — a retrofitted matrix is theater.
- Early discovery with high uncertainty — lock weights too early creates false rigor; use opportunity-solution trees.

## Content

| File | What's inside |
|------|---------------|
| `content/01-decision-steps.xml` | Six-step procedure, criteria types and weighting, scoring scale, sensitivity analysis, documentation requirements. |
| `content/02-enterprise-workflow.xml` | Five-phase multi-stakeholder workflow, traceability to requirements, recommended subagents, prompt patterns, AI gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-analysis-document.md` | Full Decision Analysis Document: context, options, criteria+weights, evaluation matrix, analysis, recommendation, approval. |
| `templates/decision-matrix.md` | Simple decision matrix for fast evaluations (3-5 options, ≤7 criteria). |
| `templates/weight-reconcile.py` | Script: aggregate per-stakeholder weight CSVs, compute mean/σ, flag dissent (σ > 0.05 or range > 0.20). |
