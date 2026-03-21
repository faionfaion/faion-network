---
name: faion-brainstorm
description: "Multi-agent brainstorming: structured diverge-converge-review cycles for technical and product ideation."
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, WebSearch, WebFetch, AskUserQuestion
---
> **Entry point:** `/faion-brainstorm` — invoke directly or via `/faion-net`.

# Multi-Agent Brainstorm Skill

**Communication: User's language. Code/docs: English.**

## Purpose

Structured multi-agent brainstorming process for generating, evaluating, and prioritizing recommendations. Uses parallel research agents with distinct personas, adversarial reviewers, and evidence-based synthesis.

## Process: Diverge → Converge → Review → Finalize

### Phase 1: DIVERGE (Research Agents)

Launch N research agents (default: 10, max 3 parallel) with **distinct personas**.

**Key principles:**
- Each agent gets a unique focus area/perspective (not identical prompts)
- Agents generate independently (no cross-pollination during divergence)
- Each agent must produce exactly 30 recommendations
- Format: current state → problem → solution → impact

**Persona assignment strategies:**
- **By domain:** frontend, backend, infra, security, UX, cost, etc.
- **By framework:** Six Thinking Hats (facts, emotions, risks, benefits, creativity, process)
- **By lens:** user perspective, developer perspective, business perspective, operations perspective

**Anti-patterns to avoid:**
- Identical prompts → groupthink, redundant output
- Too many agents → diminishing returns (10-12 optimal)
- No persona differentiation → bandwagon bias on popular ideas

### Phase 2: CONVERGE (Synthesis)

A single synthesis pass that:
1. **Deduplicates** — cluster similar recommendations across agents
2. **Counts consensus** — track how many agents independently recommended each item
3. **Ranks by impact** — use explicit criteria: cost savings, effort, risk reduction, user impact
4. **Structures output** — organize into priority tiers (This Week / This Month / This Quarter / Backlog)

**Synthesis document structure:**
```markdown
# [Topic]: Recommendations (Draft)
## Executive Summary (3-5 sentences)
## Tier 1: Critical (do now)
## Tier 2: High (do soon)
## Tier 3: Medium (plan)
## Backlog (defer)
## Architecture Decisions (consensus table)
## Quick Win Execution Order
```

### Phase 3: REVIEW (Adversarial Reviewers)

Launch M review agents (default: 8-10, max 3 parallel) with **adversarial roles**.

**Required reviewer roles:**
1. **Feasibility & Effort** — are estimates realistic? hidden dependencies?
2. **Security** — gaps, risks introduced, minimum viable hardening?
3. **Architecture** — coherence, contradictions, correct ordering?
4. **Solo Dev / DX** — maintenance burden, set-and-forget vs ongoing toil?
5. **Cost-Benefit** — actual monetary impact, ROI ranking?
6. **Missing Perspectives** — what's absent? user features? data? operations?
7. **Domain Expert** — deep dive on the #1 recommendation
8. **Prioritization Synthesis** — final ordering incorporating all reviewer feedback

**Optional roles (based on topic):**
- LLM Cost Optimizer
- UX Quality Reviewer
- Testing Strategy Reviewer
- Compliance/Legal Reviewer

**Anti-patterns to avoid:**
- Generic "review this document" prompts → rubber-stamping
- All reviewers with same perspective → echo chamber
- No adversarial role → blind spots persist

### Phase 4: FINALIZE

Incorporate reviewer feedback into final document:
1. Re-tier recommendations based on reviewer consensus
2. Adjust effort estimates based on feasibility review
3. Add missing items identified by devil's advocate
4. Include cost projections if relevant
5. Mark items for backlog with clear "why defer" rationale

**Final document structure:**
```markdown
# [Topic]: Recommendations (Final)
## Key Insights from Review (table: reviewer → finding)
## THIS WEEK (items + effort + impact)
## THIS MONTH (items)
## THIS QUARTER (items)
## BACKLOG (items + why defer)
## Architecture Decisions (consensus table)
## Cost Projection (if applicable)
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| research_agents | 10 | Number of research agents in Phase 1 |
| review_agents | 8 | Number of review agents in Phase 3 |
| parallel_limit | 3 | Max concurrent agents |
| recs_per_agent | 30 | Recommendations per research agent |
| focus | auto | Topic focus (auto-detected from user prompt) |

## Usage Examples

```
/faion-brainstorm How to improve our deployment pipeline?
/faion-brainstorm 10 recommendations for reducing LLM costs
/faion-brainstorm Technical audit of the authentication system
```

## Evidence Base

- MultiColleagues (ECIS 2025): specialized agent roles produce stronger ideation
- A-MEM (arXiv 2502.12110): tiered memory improves agent coherence
- IBIS-based brainstorming (ACM 2024): prevents premature convergence
- Six Thinking Hats: forces systematic multi-perspective coverage
- Brainwriting: independent generation before sharing prevents anchoring

## Self-Evaluation Criteria

After each brainstorm, evaluate:
1. **Coverage** — did agents cover all relevant perspectives?
2. **Novelty** — any surprising/non-obvious recommendations?
3. **Actionability** — can items be executed immediately?
4. **Bias** — was there groupthink? anchoring? infrastructure bias?
5. **User focus** — are user-facing improvements represented?

## Related Skills

- faion-software-architect (architecture decisions)
- faion-product-planning (feature prioritization)
- faion-researcher (market/competitor research)
