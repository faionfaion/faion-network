# Agent Integration — Performance Domains Overview

## When to use
- Onboarding a new project: triage which of the 8 PMBOK7 domains need active management on this engagement.
- Periodic project health checks where you score each domain green/yellow/red and decide where to spend management attention.
- Tailoring an engagement: deciding which methodologies (RACI, EVM, risk register, communication plan) to instantiate vs skip based on domain weight.
- Mapping legacy-PMBOK6 process documentation onto the PMBOK7 outcome-based view during cert prep or audit.
- Routing a multi-methodology agent: a router that picks the right detailed methodology (scope-management, schedule-development, EVM, etc.) given a project question.

## When NOT to use
- Single-task work where a checklist suffices; the framework adds overhead without changing decisions.
- Pure scrum teams for whom Scrum Guide already defines roles, ceremonies and metrics — domains and Scrum aren't contradictory but redundant overlay creates confusion.
- Operations / BAU work that is not a project (no defined start/end, no unique outcome).
- Low-stakes internal work where domain assessment cost > project cost.

## Where it fails / limitations
- "Outcomes not processes" sounds clean but PMBOK7 still ships ~50 process artefacts in the Standard for Project Management; agents trained on PMBOK6 mix the two.
- Domain interactions are described qualitatively; an agent cannot quantitatively trade Stakeholder vs Measurement attention without a separate decision model.
- Performance Domains are auditing primitives, not delivery primitives — you cannot "do" the Stakeholder Domain, only do stakeholder engagement and assess against the domain.
- Many real LLM outputs collapse the 8 domains back into the old 5 process groups (Initiate / Plan / Execute / M&C / Close); this is a regression.
- The framework intentionally avoids prescribing tools — agents tend to invent processes to fill the gap, drifting back to PMBOK6.
- 2026 cert weights shift Business Environment from 8% to 26% (see `pm-certification-changes-2026`); training data still reflects old weights.

## Agentic workflow
Use the overview as a **router and assessment harness**, not as an executable methodology. A `domain-router` agent reads the user's project question, classifies it into one or more of the 8 domains, and dispatches to the detailed methodology agents (scope-management, EVM, risk-management, etc.). A separate `domain-assessor` agent scores each domain green/yellow/red weekly using objective inputs (sprint metrics, risk register count, stakeholder satisfaction survey) and surfaces the weakest two domains to the human PM. Humans own the strategic call on where to invest attention.

### Recommended subagents
- `domain-router` — classify input → 1-3 of {stakeholder, team, dev-approach, planning, project-work, delivery, measurement, uncertainty}; emit confidence + rationale.
- `domain-assessor` — input: project artefacts, output: per-domain RAG status with cited evidence.
- `tailoring-advisor` — input: project context (size, risk, regulated?) → which detailed methodologies to enable.
- `faion-pm-agent` (existing skill router) — already routes to detailed PM methodologies.

### Prompt pattern
```
System: You are the PMBOK7 Performance Domains classifier.
Domains: stakeholder, team, dev-approach, planning, project-work,
         delivery, measurement, uncertainty.

Input: <project question or status item>
Output JSON:
{ "primary_domain": "<one>",
  "secondary_domains": ["<...>"],
  "rationale": "<one sentence>",
  "recommended_methodologies": ["scope-management", ...],
  "confidence": 0.0-1.0 }

If the input is operational (not project work), return
{"out_of_scope": true, "reason": "..."}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh project` / `jira-cli` | Pull project artefacts that feed domain assessment | https://cli.github.com/ , https://github.com/ankitpokhrel/jira-cli |
| `pandas` / `duckdb` | Aggregate cross-domain metrics (sprint velocity, EVM, risk count) into a single dashboard | https://duckdb.org/ |
| `mermaid-cli` | Render the 8-domain interaction map for status reports | https://github.com/mermaid-js/mermaid-cli |
| `gpt-cli` / `claude` | Run the router agent locally over a backlog of items | n/a |
| `streamlit` | Build a domain RAG dashboard from CSV/JSON | https://streamlit.io/ |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Smartsheet PMO | SaaS | Yes — REST | Domain-tagged work portfolio |
| Monday.com | SaaS | Yes — GraphQL | Custom statuses for domain RAG |
| Notion / Confluence | SaaS | Yes — REST | Where the PMBOK7 tailoring doc lives |
| Asana Portfolios | SaaS | Yes — REST | Cross-project domain rollup |
| Jira + Atlas | SaaS | Yes — REST | Atlas gives portfolio-level domain status |
| ClickUp Goals | SaaS | Yes — REST | Tie outcomes to delivery domain |
| OnePager Pro | SaaS | Limited | One-page exec status by domain |
| ProjectManager.com | SaaS | Yes — REST | PMBOK-aligned PMO tooling |

## Templates & scripts
See `templates.md` for the Performance Domain Assessment table (8 rows × 3 columns: health/issues/actions). Domain router can be ~25 lines:

```python
DOMAINS = ["stakeholder","team","dev-approach","planning",
           "project-work","delivery","measurement","uncertainty"]
def classify(question, llm):
    schema = {"primary_domain": "", "secondary_domains": [], "confidence": 0}
    prompt = f"Classify into PMBOK7 domain(s): {DOMAINS}\nQ: {question}"
    return llm.json(prompt, schema=schema)
```

## Best practices
- Re-assess domains at every project gate (kickoff, mid-point, pre-launch, close), not weekly — weekly drives status-theatre.
- Start every status report with the two weakest domains; do not rotate through all 8 — focus drives action.
- Map your existing artefacts (RACI, risk register, EVM dashboard) onto domains explicitly so the framework augments, not replaces, your toolkit.
- When tailoring, drop entire domains, not partial methodologies. "Light EVM" is usually fake EVM. Either commit or skip.
- The Uncertainty domain is most often under-resourced; require an active risk register or downgrade to red.
- Use the domain interaction matrix (e.g., poor Stakeholder → Team + Delivery suffer) as the leading indicator; do not wait for downstream domains to slip.

## AI-agent gotchas
- Domain naming is not stable: "Project Work" is sometimes labelled "Execution"; agents trained on draft PMBOK7 use both. Pin canonical names in the prompt.
- LLMs collapse "Development Approach" into "Methodology" and lose the distinction between hybrid/iterative/incremental — feed the table explicitly.
- Asking an LLM "is this domain healthy?" without inputs returns generic prose. Always feed evidence (artefact links, metrics) and require citations.
- The framework is principle-based; agents over-rotate to checklists. Bias prompts toward "what outcome is at risk?" not "did we follow process?"
- 2026 exam alignment shifts weights toward Business Environment (Value Delivery, Governance, Sustainability); agents using pre-2026 training will under-emphasise these.
- Cross-domain double-counting: the same status item often hits Stakeholder + Communication + Delivery; require the router to pick a primary and list secondaries explicitly.
- Domains are NOT phases. Agents that emit "Stakeholder phase complete" need correction.

## References
- PMI, *PMBOK Guide* 7th Ed. (2021), Section 2 — Project Performance Domains.
- PMI, *The Standard for Project Management* (bundled with 7th Ed.) — principles + value delivery system.
- PMI Practice Standard for Tailoring (in development).
- Disciplined Agile (PMI) — tailoring goals and decision tables.
- 2026 PMP Exam Content Outline (Q3 2025 update).
- Mind the Product, "PMBOK7 for product managers" (2022).
