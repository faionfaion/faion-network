# Quality Management

## Summary

A three-process framework (Plan Quality → Manage Quality → Control Quality) applied as code-driven gates: DoD checked per PR by an automated validator, defect metrics aggregated weekly by a collector agent, and severity classified by a triager with human confirmation. Quality is built in, not tested in — prevention over detection is the operative principle (Deming).

## Why

Rework consumes 20-40% of project time when quality is an afterthought. Defects found in production cost 10-100x more to fix than defects found at code review. A machine-readable DoD (`quality/dod.yaml`) versioned in the repo and enforced by CI makes "done" unambiguous and prevents checklist drift.

## When To Use

- Setting Definition of Done across a multi-team or multi-repo product
- Defect-escape rate climbing or production incidents recurring on the same surfaces
- Codebase has no quality dashboard and PM/PO cannot answer whether the trend is improving
- Pre-release hardening: agent-driven quality audit before a major launch
- Compliance kickoff (SOC2, ISO 9001) where evidence trail must be reproducible

## When NOT To Use

- One-person prototype before product-market fit — quality gates slow validation loops
- Spike or research code marked throwaway — formal QC inflates effort 2-3x
- When the team rejects DoD as ceremony — fix the trust issue first, then introduce gates
- For aesthetic UX polish — use design review, not quality management process

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Three quality processes, quality concepts, metrics taxonomy (product/process/perception) |
| `content/02-workflow.xml` | Agentic DoD-validator and metric-collector pipeline, prompt patterns, AI-agent gotchas |
| `content/03-tools-and-references.xml` | CLI tools, SaaS services, best practices, references |

## Templates

| File | Purpose |
|------|---------|
| `templates/dod.yaml` | Machine-readable Definition of Done with must/should items and scope tags |
| `templates/dod-validator.py` | PR gate script: tests, coverage, lint, secrets scan |
| `templates/defect-report.md` | Defect report template with severity, steps, environment, root cause |
| `templates/quality-checklist.md` | Pre-ship quality checklist (code, testing, performance, security, accessibility) |
