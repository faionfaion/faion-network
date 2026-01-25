# Business Analyst Skill

> **Entry Point:** Invoked via [/faion-net](../faion-net/CLAUDE.md) or directly as `/faion-business-analyst`

## When to Use

- Planning BA approach and stakeholder analysis
- Requirements elicitation (interviews, workshops, documentation review)
- Requirements lifecycle management and traceability
- Strategy analysis (current/future state, gap analysis)
- Use case modeling and user story mapping
- Business process analysis (BPMN)
- Solution evaluation and assessment

## Overview

BA orchestrator with 2 sub-skills, 28 methodologies across 6 Knowledge Areas.

**Agent:** faion-ba-agent

<<<<<<< HEAD
## Quick Decision: What BA Task?

| If you need to... | Use Knowledge Area | Key Methodology |
|-------------------|-------------------|-----------------|
| Plan BA approach, stakeholders | KA-1 Planning | ba-planning, stakeholder-analysis |
| Gather requirements | KA-2 Elicitation | elicitation-techniques |
| Track/prioritize requirements | KA-3 Lifecycle | requirements-traceability, requirements-prioritization |
| Analyze current/future state | KA-4 Strategy | strategy-analysis |
| Model/document requirements | KA-5 Analysis | use-case-modeling, user-story-mapping |
| Evaluate solution | KA-6 Evaluation | solution-assessment |

**Full decision trees:** See [SKILL.md](SKILL.md#decision-trees)

## Directory Structure

```
faion-business-analyst/
├── SKILL.md                          # Main skill
├── CLAUDE.md                         # Navigation (this file)
├── ref-CLAUDE.md                     # References overview
├── ba-planning.md
├── stakeholder-analysis.md
├── elicitation-techniques.md
├── requirements-documentation.md
├── requirements-traceability.md
├── strategy-analysis.md
├── requirements-lifecycle.md
├── solution-assessment.md
├── business-process-analysis.md
├── data-analysis.md
├── decision-analysis.md
├── use-case-modeling.md
├── user-story-mapping.md
├── acceptance-criteria.md
├── requirements-validation.md
├── requirements-prioritization.md
├── interface-analysis.md
├── knowledge-areas-overview.md
├── methodologies-detail.md           # Governance, risk, change templates
├── ai-enabled-business-analysis.md
├── agile-ba-frameworks.md
├── process-mining-automation.md
├── data-driven-requirements.md
├── modern-ba-framework.md
├── ba-strategic-partnership.md
└── ba-trends-summary.md
=======
---

## Architecture

```
faion-business-analyst (orchestrator)
├── faion-ba-core (21 methodologies)
│   └── Planning, Elicitation, Lifecycle, Strategy, Evaluation
└── faion-ba-modeling (7 methodologies)
    └── Use Cases, User Stories, BPMN, ERD, Decision Tables
>>>>>>> claude
```

---

<<<<<<< HEAD
| File | Description | Lines |
|------|-------------|-------|
| SKILL.md | Main skill: decision trees, 6 KAs, methodology table | ~370 |
| methodologies-detail.md | Detailed templates: governance, risk, change | ~450 |
| *.md (26 files) | Individual methodology files | ~250 each |

## 6 Knowledge Areas Summary

| # | Knowledge Area | Focus | Key Outputs |
|---|----------------|-------|-------------|
| 1 | BA Planning & Monitoring | Approach, stakeholders, governance | BA approach, stakeholder map |
| 2 | Elicitation & Collaboration | Gather and confirm information | Elicitation results |
| 3 | Requirements Lifecycle | Trace, maintain, prioritize, approve | Traced/approved requirements |
| 4 | Strategy Analysis | Current/future state, risks, change | Change strategy |
| 5 | Requirements Analysis & Design | Model, verify, validate, recommend | Solution recommendation |
| 6 | Solution Evaluation | Measure, assess, improve | Value improvement recommendations |
=======
## Quick Decision

| If you need... | Sub-Skill | Key Methodology |
|----------------|-----------|-----------------|
| Plan BA approach | ba-core | ba-planning, stakeholder-analysis |
| Gather requirements | ba-core | elicitation-techniques |
| Track requirements | ba-core | requirements-traceability |
| Analyze state | ba-core | strategy-analysis |
| Model requirements | ba-modeling | use-case-modeling, user-story-mapping |
| Evaluate solution | ba-core | solution-assessment |

---
>>>>>>> claude

## Sub-Skills

<<<<<<< HEAD
### Core (KA-1 to KA-3)

| Methodology | When to Use |
|-------------|-------------|
| ba-planning | Define BA approach |
| stakeholder-analysis | Map stakeholders |
| elicitation-techniques | Gather requirements |
| requirements-traceability | Track relationships |
| requirements-prioritization | Rank requirements |
| requirements-lifecycle | Manage over time |

### Analysis (KA-4 to KA-5)

| Methodology | When to Use |
|-------------|-------------|
| strategy-analysis | Current/future state |
| use-case-modeling | User-system interactions |
| user-story-mapping | Agile requirements |
| business-process-analysis | Process flows (BPMN) |
| data-analysis | Data requirements |
| decision-analysis | Business rules |
| interface-analysis | System interfaces |
| acceptance-criteria | Done criteria (BDD) |
| requirements-validation | Validate vs goals |
| requirements-documentation | Formal documentation |

### Evaluation (KA-6)

| Methodology | When to Use |
|-------------|-------------|
| solution-assessment | Evaluate performance |

## Modern BA (2025-2026)

| Topic | File |
|-------|------|
| AI-Enabled BA | ai-enabled-business-analysis.md |
| Agile BA | agile-ba-frameworks.md |
| Process Mining | process-mining-automation.md |
| Data-Driven Requirements | data-driven-requirements.md |
| Modern BA Framework | modern-ba-framework.md |
=======
### faion-ba-core (21 methodologies)

Planning, elicitation, requirements lifecycle, strategy analysis, solution evaluation, modern practices.

**Location:** [faion-ba-core/](faion-ba-core/)
>>>>>>> claude

### faion-ba-modeling (7 methodologies)

<<<<<<< HEAD
```
# Via faion-ba-agent for methodology execution
# Called from faion-net or faion-sdd orchestrators
```
=======
Use cases, user stories, BPMN, ERD, decision tables, interfaces, acceptance criteria.
>>>>>>> claude

**Location:** [faion-ba-modeling/](faion-ba-modeling/)

<<<<<<< HEAD
- Business Analysis Framework Guide (BABOK)
- BA industry standards
- Certifications: ECBA, CCBA, CBAP, AAC
=======
---

## 6 Knowledge Areas

| # | Knowledge Area | Focus | Sub-Skill |
|---|----------------|-------|-----------|
| 1 | BA Planning & Monitoring | Approach, stakeholders | ba-core |
| 2 | Elicitation & Collaboration | Gather information | ba-core |
| 3 | Requirements Lifecycle | Trace, maintain, prioritize | ba-core |
| 4 | Strategy Analysis | Current/future state, gaps | ba-core |
| 5 | Requirements Analysis & Design | Model, verify, validate | ba-modeling |
| 6 | Solution Evaluation | Measure, assess, improve | ba-core |

**Detailed overview:** [knowledge-areas-detail.md](knowledge-areas-detail.md)

---

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Main orchestrator |
| [knowledge-areas-detail.md](knowledge-areas-detail.md) | 6 KAs overview |
| [ref-CLAUDE.md](ref-CLAUDE.md) | References overview |
| [faion-ba-core/](faion-ba-core/) | Core BA sub-skill |
| [faion-ba-modeling/](faion-ba-modeling/) | Modeling sub-skill |

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-net](../faion-net/CLAUDE.md) | Parent orchestrator |
| [faion-product-manager](../faion-product-manager/CLAUDE.md) | Provides product vision |
| [faion-project-manager](../faion-project-manager/CLAUDE.md) | Uses requirements for scope |
| [faion-sdd](../faion-sdd/CLAUDE.md) | Transforms requirements into specs |
| [faion-software-architect](../faion-software-architect/CLAUDE.md) | Uses requirements for architecture |
>>>>>>> claude
