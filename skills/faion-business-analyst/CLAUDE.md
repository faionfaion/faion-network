# Business Analyst Skill

## Overview

BA Domain Skill based on IIBA BABOK v3 (Guide to Business Analysis Body of Knowledge). Orchestrates business analysis activities across 6 Knowledge Areas with 24 methodologies.

**Agent:** `faion-ba-agent`

## Purpose

Enable professional business analysis following IIBA standards:
- Requirements engineering and lifecycle management
- Stakeholder analysis and engagement
- Process modeling and data analysis
- Strategy analysis and solution evaluation
- Use cases, user stories, and acceptance criteria

## Directory Structure

```
faion-business-analyst/
|-- SKILL.md              # Main skill definition with embedded methodologies
|-- CLAUDE.md             # This navigation file
|-- methodologies/        # 24 methodology files (M-BA-001 to M-BA-024)
|   |-- CLAUDE.md         # Methodology folder overview
|   |-- M-BA-001_ba_planning.md
|   |-- M-BA-002_stakeholder_analysis.md
|   |-- ... (16 more files)
|-- references/           # Best practices and research
    |-- CLAUDE.md         # References folder overview
    |-- best-practices-2026.md
```

## Key Files

| File | Description |
|------|-------------|
| SKILL.md | Complete skill definition: 6 Knowledge Areas, 24 methodologies (M-BA-001 to M-BA-024) |
| methodologies/ | Individual methodology files with detailed frameworks and templates |
| references/ | Modern BA practices 2025-2026: AI integration, agile BA, process mining |

## BABOK Knowledge Areas

| # | Knowledge Area | Methodologies |
|---|----------------|---------------|
| 1 | BA Planning and Monitoring | M-BA-001, M-BA-002, M-BA-003 |
| 2 | Elicitation and Collaboration | M-BA-004, M-BA-005, M-BA-006 |
| 3 | Requirements Lifecycle Management | M-BA-007, M-BA-008 |
| 4 | Strategy Analysis | M-BA-011, M-BA-012, M-BA-013, M-BA-014 |
| 5 | Requirements Analysis and Design Definition | M-BA-015, M-BA-016, M-BA-017 |
| 6 | Solution Evaluation | M-BA-018 |

## Methodology Quick Reference

| ID | Name | Category |
|----|------|----------|
| M-BA-001 | BA Planning | Planning |
| M-BA-002 | Stakeholder Analysis | Planning |
| M-BA-003 | Elicitation Techniques | Elicitation |
| M-BA-004 | Requirements Documentation | Analysis |
| M-BA-005 | Requirements Traceability | Lifecycle |
| M-BA-006 | Strategy Analysis | Strategy |
| M-BA-007 | Requirements Lifecycle | Lifecycle |
| M-BA-008 | Solution Assessment | Evaluation |
| M-BA-009 | Business Process Analysis | Analysis |
| M-BA-010 | Data Analysis | Analysis |
| M-BA-011 | Decision Analysis | Analysis |
| M-BA-012 | Use Case Modeling | Analysis |
| M-BA-013 | User Story Mapping | Analysis |
| M-BA-014 | Acceptance Criteria | Analysis |
| M-BA-015 | Requirements Validation | Lifecycle |
| M-BA-016 | Requirements Prioritization | Lifecycle |
| M-BA-017 | Interface Analysis | Analysis |
| M-BA-018 | Knowledge Areas Overview | Framework |

## Modern Practices (references/)

Additional methodologies for 2025-2026:

| ID | Name | Focus |
|----|------|-------|
| M-BA-019 | AI-Enabled BA | GenAI, agentic AI, AI TRiSM |
| M-BA-020 | Agile BA in Scrum/SAFe | Scaled frameworks |
| M-BA-021 | Process Mining | RPA, intelligent automation |
| M-BA-022 | Data-Driven Requirements | Analytics, evidence-based |
| M-BA-023 | BABOK v3 Modern Application | Framework updates |
| M-BA-024 | BA Strategic Partnership | Innovation leadership |

## Usage

```
# Use via faion-ba-agent for BABOK methodology execution
# Called from faion-net or faion-sdd orchestrators
```

## References

- BABOK Guide v3 (IIBA)
- IIBA Business Analysis Standards
- IIBA Certifications: ECBA, CCBA, CBAP, IIBA-AAC
