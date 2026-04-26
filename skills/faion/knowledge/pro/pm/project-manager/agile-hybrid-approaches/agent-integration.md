# Agent Integration — Agile and Hybrid Approaches

## When to use
- Choosing a delivery mode (predictive / agile / hybrid) at project kick-off, given a known mix of contract type, requirement clarity, and stakeholder availability.
- Re-evaluating mid-flight when symptoms appear (waterfall slipping repeatedly → switch core build to Scrum; Scrum failing on fixed-price compliance → wrap in phase gates).
- Designing a tailored hybrid for fixed-price clients (Water-Scrum-Fall, agile-discovery-then-predictive-build, predictive-governance-over-agile-execution).
- Authoring the Development Approach section of a PMBoK 8 plan.
- Coaching a team transitioning from one approach to another with explicit ceremony / artefact mappings.

## When NOT to use
- Tiny projects (< 4 weeks, single team, well-scoped) where any methodology overhead beats the work itself; do a checklist.
- Mandated-by-contract approaches (DoD waterfall, FDA validated software, banking with locked phase gates) where you have no degrees of freedom.
- Pure operations / BAU work with no defined start/end — Kanban + SLAs, not project methodology.
- Research-heavy / pre-PMF startups where "approach" is "do whatever the founder thinks today".

## Where it fails / limitations
- Agile-in-name-only is the most common failure: daily standups + waterfall plan = no benefit, doubled overhead.
- Water-Scrum-Fall caps the agile benefit: the build is iterative but plan and deploy phases are rigid, so total cycle time is still long.
- Fixed-price + agile only works with a "scope envelope" contract; LLMs miss this nuance and recommend agile to fixed-price clients without warning.
- Hybrid governance creates two reporting cadences (sprint review + phase gate) that both consume PM time; not free.
- Scrum at scale (SAFe, LeSS, Nexus) is its own beast and is *not* a generic hybrid; agents conflate them.
- Kanban WIP limits get violated under deadline pressure; methodology guidance does not enforce them — needs tooling.
- "Choose by team experience" advice creates a chicken-and-egg: junior teams default to predictive but never learn agile.

## Agentic workflow
The agent is a methodology selector + tailor. Phase 1: a `methodology-selector` reads a project context YAML (requirement clarity, stakeholder availability, contract type, team experience, risk tolerance, regulator presence) and returns a recommended approach with rationale. Phase 2: a `methodology-tailor` produces the concrete artefact list (charter / backlog / sprints / gates) and ceremony cadence. Human review between phases. Re-run on every steering committee that changes the inputs.

### Recommended subagents
- `methodology-selector` (define inline) — input: project-context.yaml; output: chosen approach + decision matrix score per option.
- `methodology-tailor` (define inline) — input: chosen approach + team size; output: artefact list + ceremony calendar.
- `faion-feature-executor` — once a sprint plan exists, executes the work-breakdown sequentially with gates.
- `faion-brainstorm` — for novel hybrids when the standard three options do not fit.

### Prompt pattern
```
Score the project on each axis (1-5):
- requirement_clarity, stakeholder_engagement, risk_tolerance,
  team_agility, contract_flexibility, regulatory_burden.

Recommend ONE of: [predictive, scrum, kanban, scrumban,
  water-scrum-fall, predictive-governance-over-agile, agile-discovery-then-predictive].

Output JSON:
{ "scores": {...},
  "recommendation": "...",
  "rationale": ["...", "..."],
  "ceremonies": [{"name":"...", "cadence":"weekly"}],
  "artefacts": ["...", "..."],
  "risks_of_recommendation": ["..."],
  "fall_back": "..." }
Constraints:
- Cite at least one risk if recommending agile on a fixed-price contract.
- Never recommend "pure scrum" if regulatory_burden >= 4.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira-cli` | Drive Scrum / Kanban boards programmatically | https://github.com/ankitpokhrel/jira-cli |
| `linear` CLI / API | Modern engineering-team agile board | https://developers.linear.app/ |
| `gh project` | GitHub Projects v2 (Kanban / sprint) | https://cli.github.com/manual/gh_project |
| `azure-boards` (`az boards`) | Azure DevOps Scrum/CMMI/Agile templates | https://learn.microsoft.com/cli/azure/boards |
| `mermaid-cli` | Render approach-decision diagrams | https://github.com/mermaid-js/mermaid-cli |
| `sprintly` / custom | Sprint metrics (velocity, burndown) export | n/a |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira (Cloud / Data Center) | SaaS / on-prem | Yes — REST + JQL | Scrum, Kanban, Scrumban, scaled (Advanced Roadmaps) |
| Linear | SaaS | Yes — GraphQL | Engineering-first agile, cycles + projects |
| Azure DevOps | SaaS / on-prem | Yes — REST | Multiple process templates incl. CMMI for hybrid |
| Asana | SaaS | Yes — REST | Hybrid via Portfolios + Sprints |
| ClickUp | SaaS | Yes — REST | Sprint folders + Gantt for hybrid |
| Targetprocess | SaaS | Yes — REST | SAFe / LeSS hybrid scaling |
| Monday.com | SaaS | Yes — GraphQL | Mixed boards (timeline + sprint) |
| Atlassian Confluence + Jira | SaaS | Yes — REST | Phase-gate docs alongside agile board |

## Templates & scripts
See `templates.md` for sprint-planning + Kanban-board templates. Inline approach-scoring helper (Python, ≤50 lines):

```python
#!/usr/bin/env python3
"""Score a project against agile vs predictive vs hybrid."""
import json, sys
WEIGHTS = {
    "requirement_clarity":   {"predictive": +1, "agile": -1, "hybrid":  0},
    "stakeholder_engagement":{"predictive": -1, "agile": +1, "hybrid":  0},
    "risk_tolerance":        {"predictive": -1, "agile": +1, "hybrid":  0},
    "team_agility":          {"predictive": -1, "agile": +1, "hybrid":  0},
    "contract_flexibility":  {"predictive": -1, "agile": +1, "hybrid": +0.5},
    "regulatory_burden":     {"predictive": +1, "agile": -1, "hybrid":  0},
}
def score(ctx):
    out = {"predictive": 0.0, "agile": 0.0, "hybrid": 0.0}
    for axis, val in ctx.items():
        # val on 1-5 scale, normalise to -1..+1
        n = (val - 3) / 2
        for mode, w in WEIGHTS[axis].items():
            out[mode] += n * w
    return out
def recommend(ctx):
    s = score(ctx)
    pick = max(s, key=s.get)
    return {"scores": s, "recommendation": pick}
if __name__ == "__main__":
    print(json.dumps(recommend(json.load(open(sys.argv[1]))), indent=2))
```

## Best practices
- Pick the smallest approach that solves the symptom; do not adopt SAFe to fix a one-team velocity problem.
- Make the choice explicit and dated in the project charter; write down the trigger that would force a re-evaluation.
- For hybrids, pick *one* primary cadence (sprint OR gate) and make the other an overlay; running both at equal weight burns out the PM.
- Translate ceremonies, not labels: a "sprint review" with no demo is just a status meeting.
- For fixed-price agile, write a scope-envelope contract: range of stories, change-budget, exit clauses.
- Track approach-fit metrics: lead time, velocity stability, change-request rate per sprint, defect-escape; if they trend wrong, revisit.
- Solopreneur: default to personal Kanban with WIP=3; only graduate to Scrum once you have ≥ 2 collaborators.

## AI-agent gotchas
- LLMs default to "agile" for almost any prompt; bias toward agile is heavy in training data. Force balanced scoring.
- Agents conflate Scrum, SAFe, and "agile" — pin a fixed vocabulary.
- "Hybrid" is used as a hand-wave; agents should always name a specific pattern (Water-Scrum-Fall, agile-discovery-then-predictive, etc.).
- Agents recommend daily standups for solo work — guard with team-size threshold.
- Compliance / regulator constraints are dropped silently; require explicit input field and reject "pure agile" when burden ≥ 4.
- "Fixed price + agile" gets recommended without a scope-envelope warning; force a risks-of-recommendation field.
- For approach changes, agents skip the transition cost (training, tool migration); always include a transition-cost section.
- Sprint length defaults to 2 weeks regardless of context; for distributed / regulated teams, 3-4 weeks is often better.

## References
- Scrum Guide (current): https://scrumguides.org/scrum-guide.html
- Kanban Guide: https://kanbanguides.org/
- SAFe (Scaled Agile Framework): https://scaledagileframework.com/
- LeSS (Large-Scale Scrum): https://less.works/
- PMI — Agile Practice Guide: https://www.pmi.org/pmbok-guide-standards/practice-guides/agile
- Disciplined Agile (DA): https://www.pmi.org/disciplined-agile
- Mike Cohn — "Succeeding with Agile" + agileatlas.org articles
- Manifesto for Agile Software Development: https://agilemanifesto.org/
