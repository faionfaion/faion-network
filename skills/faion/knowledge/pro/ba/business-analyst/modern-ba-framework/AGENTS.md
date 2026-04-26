# Modern BA Framework

## Summary

A meta-framework for applying the six BABOK Knowledge Areas to modern delivery contexts: agile, AI/ML, cloud-native, platform engineering, and process-mining. The deliverable for an agent is not "do BA" but a routing decision — a `ba-approach.json` that picks methodologies per KA, declares delivery perspective (Agile/BI/IT/BizArch/BPM/Data-Product/AI-Product), maps per-task model tiers, and requires human PO sign-off before execution. The framework also maps team competencies against ECBA/CCBA/CBAP/AAC/CBDA/CPOA and SFIA v9.

## Why

BABOK was published in 2015. Without a modern interpretation layer, agents default to waterfall-shaped artifacts (BRD/SRS/RTM) even on agile projects, miss AI/ML-specific concerns (prompt versioning, eval traceability, model selection), and apply a single Agile perspective when the work actually spans Business Architecture and BPM. The framework forces explicit perspective declaration and maps each KA to a concrete sibling methodology, preventing KAs with no executable output.

## When To Use

- Onboarding a new BA or PO: agent reads project context and emits a tailored BA approach that selects methodologies per KA and perspective.
- Migration audits: shifting from waterfall BABOK artifacts to agile/lean BA equivalents.
- Certification-aligned skill assessment: scoring a team against BABOK certifications and SFIA v9.
- Multi-perspective discovery: work spanning Agile + BI + Business Architecture simultaneously.
- Model selection routing: assigning haiku/sonnet/opus per task type (format → haiku, AC → sonnet, gap analysis → opus).

## When NOT To Use

- A specific BA task is already scoped — load the concrete sibling methodology directly (acceptance-criteria, elicitation-techniques, business-process-analysis).
- Pure non-BA work (code refactor, infra hardening) — the framework manufactures BA scaffolding nobody asked for.
- Solo founders with no enterprise team — the routing value collapses to a single perspective.
- Greenfield product discovery before stakeholders or a problem statement exist — use continuous-discovery first.

## Content

| File | What's inside |
|------|---------------|
| `content/01-modern-application.xml` | BABOK KA modern application table, updated perspectives (including Data-Product, AI-Product), competency-based framework with modern skills added per category. |
| `content/02-integration.xml` | Framework integration table (SAFe, DevOps, Design Thinking, Lean Startup, Data Mesh); certification alignment 2025-2026; agentic workflow and prompt patterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ba-approach.json` | Starter BA Approach JSON: perspectives, KA include/rationale, methodologies, model routing, human sign-off flag. |
| `templates/ba-approach-init.sh` | Script scaffolding a `ba-approach.json` for a feature under `.aidocs/<feature>/`. |
