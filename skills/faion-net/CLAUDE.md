# Faion Network Orchestrator Skill

**Entry Point:** `/faion-net`

Universal orchestrator for end-to-end software project lifecycle. From idea to production, from research to marketing.

## CRITICAL: How This Skill Works

**This is an orchestrator skill.** It does NOT contain methodologies itself. Instead, it routes to domain skills using the **Skill tool**.

```
/faion-net invoked → Analyze user task → Use Skill tool → Domain skill loads → Execute
```

**You MUST use the Skill tool to invoke domain skills. Markdown links do NOT load skills.**

## Skill Routing

| User Intent | Action |
|-------------|--------|
| Research, market, competitors | `Skill(faion-researcher)` |
| Architecture, system design | `Skill(faion-software-architect)` |
| Product planning, roadmaps | `Skill(faion-product-manager)` |
| Writing code, APIs | `Skill(faion-software-developer)` |
| Infrastructure, CI/CD | `Skill(faion-devops-engineer)` |
| AI/ML, LLM APIs, RAG | `Skill(faion-ml-engineer)` |
| Marketing, GTM, SEO | `Skill(faion-marketing-manager)` |
| UX/UI, usability | `Skill(faion-ux-ui-designer)` |
| Project management | `Skill(faion-project-manager)` |
| Business analysis | `Skill(faion-business-analyst)` |
| SDD workflow | `Skill(faion-sdd)` |
| Task execution | `Skill(faion-feature-executor)` |

## Example Flow

```
User: "Research competitors for my SaaS"

1. Intent: Market research
2. Action: Use Skill tool with skill: "faion-researcher"
3. Result: faion-researcher loads with 32 methodologies
4. Execute: Full competitor analysis using loaded methodologies
```

## Statistics

| Metric | Count |
|--------|-------|
| Domain Skills | 46 |
| Agents | 60+ |
| Methodologies | 605 |

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Full routing logic and skill catalog |
| [methodologies-catalog.md](methodologies-catalog.md) | All 605 methodologies |

---

*Faion Network v2.2 - Skill Tool Integration*
