# Researcher

> **Entry point:** `/faion-net` — invoke for automatic routing.

Research orchestrator: market research, competitor analysis, user research, personas, validation, pricing.

## Sub-Skills

| Skill | Focus | Methodologies |
|-------|-------|---------------|
| [faion-market-researcher](../faion-market-researcher/CLAUDE.md) | TAM/SAM/SOM, competitors, pricing, trends | 18 |
| [faion-user-researcher](../faion-user-researcher/CLAUDE.md) | Personas, interviews, JTBD, pain points | 12 |

**Total:** 30+ methodologies

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

## Agents

| Agent | Purpose |
|-------|---------|
| faion-research-agent | Research orchestrator with 9 modes |
| faion-domain-checker-agent | Domain availability verification |

## Output Files

All outputs go to `.aidocs/product_docs/`:

| Module | Output File |
|--------|-------------|
| Market Research | market-research.md |
| Competitors | competitive-analysis.md |
| Pricing | pricing-research.md |
| Personas | user-personas.md |
| Validation | problem-validation.md |
| Summary | executive-summary.md |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-market-researcher](../faion-market-researcher/CLAUDE.md) | Sub-skill (market focus) |
| [faion-user-researcher](../faion-user-researcher/CLAUDE.md) | Sub-skill (user focus) |
| [faion-sdd](../faion-sdd/CLAUDE.md) | Uses research outputs for specs |
| [faion-product-manager](../faion-product-manager/CLAUDE.md) | Uses research for decisions |
| [faion-marketing-manager](../faion-marketing-manager/CLAUDE.md) | Uses research for GTM |
