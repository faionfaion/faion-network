# faion-researcher Skill

> **Entry Point:** Invoked via [/faion-net](../faion-net/CLAUDE.md) or directly as `/faion-researcher`

## When to Use

- Generate and validate business ideas
- Market research (TAM/SAM/SOM)
- Analyze competitors and find gaps
- Build user personas and understand pain points
- Research pricing strategies
- Validate problem-solution fit
- Evaluate niche viability
- Generate project/product names

## Overview

Research orchestrator skill that coordinates 2 specialized sub-skills for comprehensive product/startup research.

**Sub-Skills:** 2 | **Total Methodologies:** 43 | **Agents:** 2

---

## Sub-Skills

### faion-market-researcher
Market & business intelligence: TAM/SAM/SOM, competitors, pricing, trends, niche evaluation, business models, idea generation.

**Files:** 22 | [View](../faion-market-researcher/CLAUDE.md)

### faion-user-researcher
User research & validation: personas, interviews, JTBD, pain points, problem validation, value prop, surveys.

**Files:** 21 | [View](../faion-user-researcher/CLAUDE.md)

---

## Research Modes

| Mode | Output | Sub-Skill |
|------|--------|-----------|
| ideas | idea-candidates.md | market-researcher |
| market | market-research.md | market-researcher |
| competitors | competitive-analysis.md | market-researcher |
| pricing | pricing-research.md | market-researcher |
| niche | niche-evaluation.md | market-researcher |
| personas | user-personas.md | user-researcher |
| pains | pain-points.md | user-researcher |
| validate | problem-validation.md | user-researcher |
| names | name-candidates.md | market-researcher |

---

## Agents

<<<<<<< HEAD
```
faion-researcher/
├── SKILL.md                    # Full skill specification
├── CLAUDE.md                   # This file
├── methodologies-detail.md     # Full methodology templates (~1500 lines)
├── *.md                        # 32 methodologies (semantic naming)
└── ref-*.md                    # Reference materials (AI tools, best practices)
```

---

## Key Workflows

### Idea Discovery
```
Gather Context → Generate Ideas → User Selection → Pain Research → Niche Evaluation → Present Results
```

### Product Research
```
Parse project → Read constitution.md → Select modules → Run agents sequentially → Write summary
```

### Project Naming
```
Gather Concept → Generate 15-20 Names → User Selection → Check Domains → Present Results → Update constitution
```
=======
| Agent | Purpose |
|-------|---------|
| faion-research-agent | Research orchestrator with 9 modes |
| faion-domain-checker-agent | Domain availability verification |
>>>>>>> claude

---

## Output Files

All outputs go to `.aidocs/product_docs/`:

| Module | Output File | Sub-Skill |
|--------|-------------|-----------|
| Market Research | market-research.md | market-researcher |
| Competitors | competitive-analysis.md | market-researcher |
| Pricing | pricing-research.md | market-researcher |
| Personas | user-personas.md | user-researcher |
| Validation | problem-validation.md | user-researcher |
| Summary | executive-summary.md | Both |

---

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Orchestrator specification |
| [methodologies-index.md](methodologies-index.md) | Index to all methodologies |
| [workflows.md](workflows.md) | Research workflows |
| [frameworks.md](frameworks.md) | Core frameworks (7 Ps, JTBD, TAM/SAM/SOM) |
| [agent-invocation.md](agent-invocation.md) | Agent usage guide |

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-net](../faion-net/CLAUDE.md) | Parent orchestrator |
| [faion-market-researcher](../faion-market-researcher/CLAUDE.md) | Sub-skill (market focus) |
| [faion-user-researcher](../faion-user-researcher/CLAUDE.md) | Sub-skill (user focus) |
| [faion-sdd](../faion-sdd/CLAUDE.md) | Uses research outputs for specs |
| [faion-product-manager](../faion-product-manager/CLAUDE.md) | Uses research for decisions |
| [faion-marketing-manager](../faion-marketing-manager/CLAUDE.md) | Uses research for GTM |

---

*faion-researcher v2.0*
*Orchestrator with 2 sub-skills (43 methodologies total)*
