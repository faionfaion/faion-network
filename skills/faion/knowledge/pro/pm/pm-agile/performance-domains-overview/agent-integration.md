# Agent Integration — Performance Domains Overview (PMBOK 7)

## When to use
- Initial project health scan: rapidly identify which of the 8 domains is weakest.
- Onboarding a PM/agent into an existing project — gives a structured 8-axis mental model.
- Quarterly project audit / steering committee preparation.
- Choosing which methodology to load next (each domain points at concrete sub-methodologies).

## When NOT to use
- Single-sprint feature work — too high-level; use Scrum ceremonies directly.
- Pure waterfall regulated projects with prescribed templates (use PMBOK 6 process groups instead).
- Personal/solo projects without stakeholders or external delivery commitments.

## Where it fails / limitations
- The 8 domains overlap heavily; teams waste time arguing where an issue "belongs."
- Domain colors (green/yellow/red) collapse multi-dimensional reality into a bumper sticker.
- Lacks prescribed cadence — easy to do the assessment once and never repeat.
- Doesn't say which domain to fix first when several are red.

## Agentic workflow
Use a Claude subagent to score each domain from project artifacts (status reports, retros, risk register, sprint logs) and emit a one-page assessment. Run this monthly (or after major milestones). The agent only proposes scores — humans decide priority actions.

### Recommended subagents
- `faion-pm-agent` — drives the 8-domain scan and surfaces the weakest domain.
- `faion-sdd-executor-agent` — converts assessment "priority actions" into SDD tasks.
- General-purpose Claude subagent — pulls evidence from source docs into the assessment.

### Prompt pattern
```
Read <retros, status reports, risk register>. Score each of the
8 PMBOK 7 performance domains green/yellow/red, with one
evidence quote per domain. Identify the single domain that, if
improved, unblocks the most others — and explain why.
```

```
For domain <X>, list the 3 PMBOK methodologies most likely to
shift it from yellow to green, ranked by expected impact and
ordered by dependency (do A before B).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Pull issue/PR data for Project Work + Delivery domains | `brew install gh` |
| `jq` | Slice JSON exports of risks, sprints, milestones | `brew install jq` |
| `pandoc` | Render the 1-page assessment to PDF for stakeholders | `brew install pandoc` |
| `mdcat` / `glow` | Render markdown assessments in terminal | `brew install glow` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira | SaaS | REST API | Source data for Planning, Project Work, Measurement |
| Linear | SaaS | GraphQL | Source data for Delivery + Team domains |
| Confluence / Notion | SaaS | API | Hosts the assessment dashboard |
| Productboard | SaaS | API | Stakeholder + Delivery alignment |
| Gainsight | SaaS | API | Stakeholder satisfaction signals |

## Templates & scripts
See `templates.md` for the Performance Domain Assessment table. Inline assessment skeleton generator:

```bash
#!/usr/bin/env bash
# pd-assessment.sh — emit a fresh assessment skeleton.
project="${1:?project name}"
cat <<MD
# Performance Domain Assessment: $project
**Date:** $(date +%F)

| Domain | Health | Key Issues | Actions |
|--------|--------|------------|---------|
| Stakeholder | | | |
| Team | | | |
| Development Approach | | | |
| Planning | | | |
| Project Work | | | |
| Delivery | | | |
| Measurement | | | |
| Uncertainty | | | |

## Weakest domain
<name> — because <evidence>.

## Priority actions (ranked)
1.
2.
3.
MD
```

## Best practices
- Assess all 8 domains in a single sitting; partial assessments are misleading.
- Anchor each color rating with a quoted artifact (retro line, incident, missed milestone) — no vibes.
- Run the assessment on a fixed cadence (monthly) AND on triggers (incident, scope change, leadership change).
- Never publish more than 3 priority actions; teams cannot work on more in parallel.
- Track domain health over time as a sparkline — direction matters more than absolute level.

## AI-agent gotchas
- Agents over-rate "Team" and "Stakeholder" green because retros are usually polite — counterweight with attrition / NPS data.
- Don't let a single agent both score AND prescribe actions in one pass; bias compounds. Split into two prompts.
- Force evidence-per-cell; without it, the agent produces a beige consensus assessment.
- Watch for stale data: assessments must declare the time window of evidence consulted.
- Domain interactions table is high-value; agents tend to forget cross-domain cause/effect — prompt for it explicitly.

## References
- PMI PMBOK Guide 7th Edition — "Project Performance Domains."
- PMI Standard for Project Management (2021).
- Disciplined Agile Delivery (DAD) framework — overlaps on domain decomposition.
