# Risk Register

## Summary

**One-sentence:** Structured log of threats and opportunities scored by P×I; named owner; observable trigger; Accept entries require contingency; ≥1 opportunity per 10 threats; reviewed weekly.

**One-paragraph:** Structured log of identified threats and opportunities, each scored by probability × impact (1-25 scale), assigned a response strategy (Avoid/Transfer/Mitigate/Accept for threats; Exploit/Share/Enhance/Accept for opportunities), and owned by a named individual. Every Accept entry requires a contingency_amount or contingency_plan. Trigger must be an observable signal. Calibrate the impact scale with a project-specific reference. Include at least one opportunity per ten threats. Register is reviewed weekly; archived after each stage gate.

**Ефективно для:**

- Standing up the uncertainty domain at project kickoff
- Weekly risk review cycles (diffing register against issue tracker and schedule)
- Pre-gate and steering-committee snapshots (top-N risks with response status)
- Vendor / supplier onboarding (category=External)

## Applies If (ALL must hold)

- Standing up the uncertainty domain at project kickoff
- Weekly risk review cycles
- Pre-gate and steering-committee snapshots (top-N risks with response status)
- Vendor / supplier onboarding (category=External, contract clauses as triggers)
- Any milestone where 'what could kill this?' deserves a written answer

## Skip If (ANY kills it)

- Pure-Scrum teams already tracking risks as backlog impediments
- Tasks under 1 week with a single owner
- Pre-discovery R&D where uncertainty is the work — use a learning log
- Risks already covered by a separate risk system (GDPR, security)

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Project artefacts | Markdown | charter, WBS, stakeholder register |
| Impact scale reference | YAML | calibrated project-specific (e.g. H impact = >$50k or >1 month delay) |
| Risk categories | list | Technical / External / Organizational / PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[risk-management]] | Process around the register (identify, plan, monitor) |
| [[stakeholder-register]] | Owner role names come from stakeholder analysis |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules: exactly-one-named-owner, trigger-observable, accept-requires-contingency, score-integrity, opportunity-quota | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `identify-phase-1` | sonnet | Categorised brainstorm from project artefacts with quoted sources |
| `score-phase-2` | sonnet | P×I assignment with rationale per rating + strategy |
| `heatmap-render` | haiku | Mechanical aggregation |

## Templates

| File | Purpose |
|------|---------|
| `templates/risk-register.md` | Register table: ID, description, category, P, I, score, strategy, response, owner, status |
| `templates/risk-card.md` | Single risk deep-dive card with trigger, contingency, and ownership fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-register.py` | Validate risk YAML: score integrity, Accept+contingency rule, heatmap output | Pre-commit; weekly review |
| `scripts/validate-risk-register.py` | Lint register against opportunity quota + named-owner + trigger-observable rules | CI on register changes |

## Related

- parent skill: `pro/pm/project-manager/`
- [[risk-management]]
- [[stakeholder-register]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
