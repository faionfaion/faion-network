# Quality Gates & Confidence Checks

## Summary

Six sequential quality gate levels (L1-L6) prevent defects from propagating through SDD phases. Each gate has a minimum confidence threshold that blocks progression when not met: L1 syntax/format (95%), L2 unit tests (90%), L3 integration tests (85%), L4 code review (80%), L5 staging (85%), L6 production (90%). Confidence score = Automated_Pass × 0.4 + Coverage × 0.2 + Risk_Mitigation × 0.2 + Traceability × 0.2. LLM-generated code enters the L1→L2 validation pipeline immediately after generation; failures trigger targeted re-prompt loops capped at 3 attempts before human escalation.

## Why

"Shift left" — catching issues at L1 costs orders of magnitude less than catching them at L5. LLMs produce syntactically valid code that still fails at runtime (hallucinated APIs, wrong function signatures). L1 gates (100% automated) provide instant feedback on linting and type errors. L2 unit tests (100% automated) catch logic errors cheaply. L4 human review focuses on what AI misses: business logic, security context, and architectural consistency. Without hard-block enforcement at L1/L2, teams accumulate technical debt that defeats the purpose of SDD.

## When To Use

- Before any phase transition in the SDD workflow — confidence check gates progression
- After LLM-generated code is produced — run L1 and L2 before human review
- Setting up CI/CD for an LLM-assisted project — quality gates are the automated enforcement layer
- When using LLM-as-judge to evaluate AI output before integration
- When change failure rate spikes — tighten gate enforcement (soft block → hard block)

## When NOT To Use

- Trivial configuration changes — full L1-L6 wastes time
- Exploratory prototypes that will be discarded — gate overhead exceeds learning value
- When gate tooling is not set up (no linter config, no test suite) — set up tooling first
- L5/L6 for local development — these are deployment gates, not development gates

## Content

| File | What's inside |
|------|---------------|
| `content/01-gate-levels.xml` | L1-L6 definitions, checks per level, confidence thresholds, automation percentages |
| `content/02-confidence.xml` | Confidence score formula, LLM validation pipeline, LLM-as-judge pattern, CI/CD integration |

## Templates

| File | Purpose |
|------|---------|
| `templates/quality-gates.yml` | GitHub Actions workflow implementing L1-L4 gates for Node.js and Python |
| `templates/calculate-confidence.py` | Python dataclass-based confidence score calculator with Gate enum |
| `templates/gate-report.md` | Markdown quality gate report template with per-gate status tables |
| `templates/run-gates.sh` | Shell script running L1-L2 gates locally for Python projects |
