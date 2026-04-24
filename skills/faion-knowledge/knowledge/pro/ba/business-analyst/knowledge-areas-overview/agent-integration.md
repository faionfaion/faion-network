# Agent Integration — BA Knowledge Areas Overview (BABOK)

This methodology is an **index/overview**, not a single technique. It maps the six BABOK knowledge areas (Planning, Elicitation, Lifecycle, Strategy, Analysis & Design, Solution Evaluation) and tells the agent which sub-methodology to load next. Use it as a router, not a deliverable producer.

## When to use

- Project kickoff: BA has no plan yet, needs to choose which knowledge areas apply.
- Scoping a BA effort for a new feature/epic — pick which of the 6 areas the work touches.
- Audit: validate that an in-flight project covers all required BA knowledge areas (gap-check).
- Onboarding a new BA or AI agent into a domain it has not touched — load this first to get the map.
- Routing inside a multi-agent BA pipeline: decide whether the next sub-agent is `ba-planning`, `elicitation-techniques`, `requirements-traceability`, `strategy-analysis`, `requirements-documentation`, or `solution-assessment`.

## When NOT to use

- You already know which technique is needed (e.g. "write user stories") — load `user-story-mapping` directly, skip the overview.
- Small/single-feature task with one stakeholder and known scope — overhead exceeds value.
- Pure software design (no business requirements) — use software-architect skills instead.
- Agile teams that already operate from a backlog with clear DoR/DoD — BABOK formalism adds friction without gain.
- Certification study — this file is operational, not exam prep.

## Where it fails / limitations

- **BABOK is descriptive, not prescriptive** — overview lists tasks but does not order them; agents that follow it linearly produce waterfall artifacts even on agile projects.
- **Heavy on documents, light on automation** — outputs (BA approach, governance plan, traceability matrix) are document-shaped; LLMs over-produce prose with no consumer.
- **Knowledge areas overlap** — Elicitation/Analysis/Lifecycle bleed into each other; agents that strictly partition activities miss feedback loops.
- **No tool guidance** — BABOK is tool-agnostic; agent must inject its own toolchain (Jira, Confluence, BPMN editors).
- **Perspective layer is vague** — Agile/BI/IT/Architecture/BPM perspectives shift task interpretation but the overview does not show how; LLMs default to IT-perspective regardless.

## Agentic workflow

Treat the overview as a **dispatch table**. The orchestrator agent reads `README.md`, classifies the user's request into one of the six knowledge areas (or several), then delegates to the matching sub-methodology under `business-analyst/`, `ba-core/`, or `ba-modeling/`. Use the "BA Coverage Checklist" template (in `templates.md`) as the shared state object across sub-agents — each sub-agent updates its row when done.

For greenfield projects, walk areas top-to-bottom (Planning → Elicitation → Strategy → Analysis → Lifecycle → Evaluation). For change requests, jump straight to Lifecycle + Analysis. For post-launch, jump to Evaluation.

### Recommended subagents

- `faion-sdd-executor-agent` — drives the BA plan as an SDD spec; treat each knowledge area as a task with its own AC.
- `password-scrubber-agent` — sanitizes elicitation transcripts and stakeholder docs before they enter the requirements repo.
- A custom `ba-router-agent` (define inline; see prompt pattern below) — single-shot classifier that picks the next knowledge area.
- For sub-area execution, route to the agents implied by the related-methodology lists (e.g. `requirements-traceability`, `business-process-analysis`, `use-case-modeling`).

### Prompt pattern

Router (one-shot classification):
```
You are a BA router. Given the user request, output a JSON array of BABOK
knowledge areas in execution order, drawn from:
[planning, elicitation, lifecycle, strategy, analysis-design, evaluation].
For each area, name the sub-methodology slug to load next.
Request: <user-text>
```

Coverage audit (gap analysis):
```
Read business-analyst/knowledge-areas-overview/README.md and the project
artifacts at <path>. For each of the 6 knowledge areas, mark Covered/Partial/
Missing and cite evidence (file + line). Output the BA Coverage Checklist
table from templates.md, fully populated.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `acli` (Atlassian CLI) | Jira/Confluence requirements + traceability | https://developer.atlassian.com/cloud/acli/ |
| `gh` | GitHub Issues as lightweight requirements store | https://cli.github.com/ |
| `notion-cli` (community) | Notion databases for stakeholder lists, BA approach | `npm i -g @notionhq/client` + scripts |
| `bpmn-to-image` | Render BPMN XML to PNG/SVG for review | `npm i -g bpmn-to-image` |
| `pandoc` | Convert BA deliverables between md/docx/pdf | https://pandoc.org/ |
| `mermaid-cli` (`mmdc`) | Generate process/state diagrams from text | `npm i -g @mermaid-js/mermaid-cli` |
| `yq` / `jq` | Manipulate requirements stored as YAML/JSON | distro pkg / `brew install` |
| `marp-cli` | Stakeholder-engagement decks from md | `npm i -g @marp-team/marp-cli` |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira (Cloud) | SaaS | Yes — REST v3 + acli | Requirements lifecycle, traceability via issue links |
| Confluence | SaaS | Yes — REST | BA approach, stakeholder register, governance docs |
| Azure DevOps | SaaS | Yes — `az boards` | Work items as requirements, queries for traceability |
| Notion | SaaS | Yes — official API | Stakeholder DB, perspectives matrix, knowledge-area board |
| Linear | SaaS | Yes — GraphQL | Lightweight backlog; weak for formal BABOK artifacts |
| GitHub Projects | SaaS | Yes — GraphQL | Free option; map issues to knowledge areas via labels |
| Camunda Modeler / bpmn.io | OSS | Partial — XML editable by agents | Process modeling for areas 4 & 5 |
| Lucid / draw.io | SaaS / OSS | Partial — drawio XML scriptable | Diagrams; agents prefer mermaid for git-native flow |
| Miro | SaaS | Limited — REST exists but UX-centric | Workshop boards; agents struggle with spatial output |
| ReqIF tools (Polarion, Doors) | SaaS | Limited | Heavy enterprise; only relevant for regulated domains |

## Templates & scripts

`templates.md` already ships the **BA Coverage Checklist** and **BA Plan**. Below is a router script that classifies a request and prints the next knowledge area + sub-methodology slug — drop-in for orchestrator agents.

```bash
#!/usr/bin/env bash
# ba-route.sh — classify a BA request into BABOK knowledge area(s)
# Usage: ba-route.sh "user request text"
# Requires: anthropic API key in $ANTHROPIC_API_KEY
set -euo pipefail
REQ="${1:?request text required}"
PROMPT=$(cat <<EOF
Classify the following BA request into BABOK knowledge areas.
Output JSON: [{"area":"<slug>","methodology":"<slug>","why":"<1-line>"}]
Areas: planning, elicitation, lifecycle, strategy, analysis-design, evaluation.
Methodologies (pick one per area):
  planning -> ba-planning, stakeholder-analysis
  elicitation -> elicitation-techniques
  lifecycle -> requirements-traceability, requirements-lifecycle, requirements-prioritization
  strategy -> strategy-analysis
  analysis-design -> requirements-documentation, business-process-analysis,
    use-case-modeling, user-story-mapping, acceptance-criteria,
    requirements-validation, decision-analysis, data-analysis, interface-analysis
  evaluation -> solution-assessment
Request: $REQ
EOF
)
curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d "$(jq -n --arg p "$PROMPT" '{
    model:"claude-opus-4-5",
    max_tokens:1024,
    messages:[{role:"user",content:$p}]
  }')" | jq -r '.content[0].text'
```

## Best practices

- Cache the routing decision: classify once at project start, store as `ba-plan.yaml`, do not re-classify per task.
- Keep the BA Coverage Checklist in version control beside the code — agents diff it across commits to detect drift.
- For agile projects, collapse Planning + Strategy into a single Sprint 0 deliverable; the overview's linear flow is wrong for iterative teams.
- Map each knowledge area to a label in the issue tracker (`ba:planning`, `ba:elicitation`, …) so traceability falls out of normal workflow.
- Pair the overview with **one** perspective (Agile / BI / IT / Architecture / BPM) explicitly stated up front — leaving it implicit produces inconsistent output across agents.
- When auditing, treat "Partial" as the default unless the agent finds artifact + sign-off; LLMs over-credit half-done work.
- Use opus for gap analysis and routing, sonnet for area-specific work, haiku for template-fill — matches the README's Agent Selection table.

## AI-agent gotchas

- **Document inflation**: agents asked to "produce BA deliverables" generate a 30-page approach document for a 2-week feature; cap output by knowledge area (e.g. Planning ≤ 1 page for sprints ≤ 2 weeks).
- **Hallucinated stakeholders**: in Elicitation, LLMs invent personas and quote them as sources; require a stakeholder register file as input, refuse to proceed without it.
- **Traceability drift**: agents update requirements but forget to update the matrix; enforce a hook that fails commits touching `requirements/*.md` without a matching `traceability.yaml` change.
- **Perspective bias**: without explicit perspective, models default to IT — they will produce system requirements when the user wanted process improvements.
- **Knowledge-area conflation**: agents merge Analysis & Design with Solution Evaluation, treating "validate requirements" and "measure solution" as the same step. Keep them in separate prompts/contexts.
- **Checkpoint requirement**: human review is mandatory between Strategy → Analysis (scope lock) and Analysis → Build (requirements baseline). Encode as explicit pause states in the orchestrator.
- **Source confusion**: BABOK v3 wording differs from v2; agents trained on mixed corpora produce hybrid task names. Pin the version in the system prompt.

## References

- BABOK Guide v3.0 (IIBA, 2015) — canonical source for the 6 knowledge areas.
- IIBA Agile Extension to BABOK v2 — for agile-perspective adaptation.
- `business-analyst/CLAUDE.md` — sibling routing index in this repo.
- Sibling methodologies: `ba-planning`, `stakeholder-analysis`, `elicitation-techniques`, `requirements-traceability`, `requirements-lifecycle`, `requirements-prioritization`, `strategy-analysis`, `requirements-documentation`, `business-process-analysis`, `use-case-modeling`, `user-story-mapping`, `acceptance-criteria`, `requirements-validation`, `decision-analysis`, `interface-analysis`, `solution-assessment`.
- Atlassian acli docs: https://developer.atlassian.com/cloud/acli/
- bpmn.io modeler: https://bpmn.io/toolkit/bpmn-js/
