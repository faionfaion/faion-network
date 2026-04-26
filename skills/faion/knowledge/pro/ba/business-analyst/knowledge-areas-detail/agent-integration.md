# Agent Integration — BA Knowledge Areas (BABOK)

This file is an index-level integration guide. It does not duplicate per-methodology agent files (those live next to each named methodology under `business-analyst/`, `ba-core/`, `ba-modeling/`). Use this file to pick which KA — and which downstream methodology — an agent should run.

## When to use

- Starting a new BA engagement and need to scope which KAs apply.
- Routing a vague stakeholder request ("we need requirements") to the correct KA + methodology.
- Building a multi-step agentic pipeline that crosses several KAs (e.g. elicit → model → validate → trace).
- Auditing an existing BA artefact set for KA coverage gaps before a release gate.

## When NOT to use

- You already know the methodology (e.g. "write user stories"). Go straight to that methodology's `agent-integration.md`.
- Pure product discovery work with no formal requirements artefacts — use `product-manager/continuous-discovery` instead.
- Pure UX research — use `pro/ux/ux-researcher/` skills.
- One-off ad-hoc questions that don't produce a tracked artefact.

## Where it fails / limitations

- BABOK is artefact-heavy. LLMs over-produce structure (10-page docs for a 3-feature MVP). Force scope before generation.
- KA-3 (Lifecycle) requires a system of record (Jira/Linear/ADO). An agent without write access can only emit drafts; traceability matrices stay stale unless wired to the issue tracker.
- KA-4 (Strategy) needs ground truth about current state (org chart, KPIs, capability map). LLMs hallucinate plausible-but-wrong baselines without a document source.
- KA-6 (Solution Evaluation) needs telemetry. No metrics → agent invents metrics. Block this branch unless an analytics datasource is attached.
- The 6-KA framing is BABOK v3 (waterfall-leaning). For pure agile/discovery, prefer `pm-agile/` + `product-manager/` skills.

## Agentic workflow

Treat the 6 KAs as a routing tree, not a sequential pipeline. A planner agent classifies the inbound request into one or more KAs, then dispatches per-KA subagents in parallel where dependencies allow. Always commit the KA classification to a memory file before dispatch — downstream agents read it instead of re-classifying. End every run with a KA-3 trace pass so artefacts stay linked.

Default sequencing for a greenfield engagement: `KA-1 → KA-4 → KA-2 → KA-5 (model) → KA-3 (prioritize+approve) → KA-5 (design) → build → KA-6`.

### Recommended subagents

- `faion-sdd-executor-agent` — drives the artefact lifecycle once requirements are approved (KA-3 → build).
- `faion-brainstorm` skill — KA-2 elicitation simulation (multi-persona stakeholders) and KA-4 future-state divergence.
- `faion-feature-executor` — KA-5 design definition once requirements pass verification.
- Inline planner agent (no dedicated subagent yet) — owns KA classification and dispatch. Implement as a single Claude call returning JSON `{ka: [...], methodologies: [...], blockers: [...]}`.
- `faion-improver` — KA-6 retrospective loop after solution ships.

### Prompt pattern

KA classification (planner):

```
You are a BABOK KA router. Input: a stakeholder request.
Output JSON only: {primary_ka: "KA-N", secondary_kas: ["KA-M", ...],
methodologies: ["slug-1", ...], missing_inputs: ["..."]}.
Rules: never invent KAs outside KA-1..KA-6. If telemetry is required
(KA-6) and not provided, list it under missing_inputs and stop.
```

KA-2 elicitation simulation (when humans are unavailable for a workshop dry-run):

```
Simulate a 4-person stakeholder workshop on <topic>. Personas: <list>.
For each persona output: stated needs, hidden needs, objections, success
criteria. Flag every claim that requires real-stakeholder confirmation.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Issue/PR sync for KA-3 traceability | `brew install gh` / cli.github.com |
| `jira-cli` (ankitpokhrel) | Issue CRUD + JQL traceability queries | github.com/ankitpokhrel/jira-cli |
| `linear-cli` | Linear issue ops (KA-3 lifecycle) | npm `@linear/cli` |
| `pandoc` | Convert markdown requirements ↔ docx for stakeholder review | pandoc.org |
| `bpmn-to-image` | Render BPMN XML for KA-5 process models | npm `bpmn-to-image` |
| `mermaid-cli` | Render mermaid (use cases, swimlanes) headlessly | npm `@mermaid-js/mermaid-cli` |
| `plantuml` (jar) | Use-case + class diagrams for KA-5 | plantuml.com |
| `dbt` (optional) | KA-6 metric definitions if warehouse-backed | getdbt.com |

## Services & apps

| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Jira | SaaS | Yes (REST + MCP) | Best for KA-3 traceability matrices via JQL. |
| Linear | SaaS | Yes (GraphQL) | Faster API, weaker custom fields → harder for full BABOK trace. |
| Azure DevOps | SaaS | Yes (REST) | Native requirements/test/work-item links → strongest KA-3 fit out of the box. |
| Confluence | SaaS | Partial | Storage for KA-1/KA-4 narrative artefacts; agent writes pages via REST. |
| Notion | SaaS | Yes (REST) | Lightweight alternative to Confluence; weaker for formal traceability. |
| Lucidchart / Miro | SaaS | Limited | API exists but diagram fidelity loss; prefer text-first (mermaid/PlantUML/BPMN XML) and import. |
| Camunda Modeler | OSS desktop | No (GUI) | Use `bpmn-js` headlessly or `camunda-platform-rest` instead. |
| Signavio | SaaS | Yes | Process intelligence + KA-6 process-mining feeds. |
| Celonis | SaaS | Yes | KA-6 process mining, agent reads via API for variance reports. |
| Aha! | SaaS | Yes | Strategy (KA-4) + roadmap, REST API. |

## Templates & scripts

The methodology folder has empty `checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md`. Per-methodology files for KA-mapped methodologies (e.g. `business-analyst/ba-planning`, `ba-modeling/use-case-modeling`) hold the real templates. This index keeps one routing snippet:

```bash
#!/usr/bin/env bash
# ba-route.sh — classify a request into BABOK KAs, list candidate methodologies.
# Usage: echo "we need to figure out why churn is up" | ba-route.sh
set -euo pipefail
REQ="$(cat)"
KB="skills/faion/knowledge/pro/ba"
claude -p "You are a BABOK KA router. Read the request and respond with JSON \
only: {primary_ka,secondary_kas[],methodologies[],missing_inputs[]}. \
Allowed KAs: KA-1..KA-6. Allowed methodologies: $(ls $KB/business-analyst $KB/ba-core $KB/ba-modeling 2>/dev/null | sort -u | paste -sd, -). \
Request: $REQ" --output-format json | jq -r '.result'
```

Wire the JSON output into your task graph; one job per `methodologies[]` entry, blockers from `missing_inputs[]` raised before dispatch.

## Best practices

- Classify before generating. Skipping the KA-routing step makes agents draft KA-5 specs when the actual gap is KA-1 stakeholder mapping.
- Persist the classification (`.aidocs/ba-routing.json`) so re-runs converge instead of reclassifying.
- For KA-3, never let an agent both author and approve a requirement in the same run — split into `author` and `reviewer` agents with different prompts.
- KA-2 + KA-5 should always emit machine-readable artefacts (JSON requirement objects, BPMN XML, Gherkin) alongside the human prose. Prose-only output breaks downstream traceability.
- Use the BABOK competency table (analytical/behavioural/business/communication/interaction) as a tag set for prompt routing — e.g. tasks tagged `interaction:facilitation` go to the `faion-brainstorm` skill rather than a solo agent.
- Cap each KA artefact to a hard line budget (KA-1 plan ≤ 200 lines, KA-4 strategy ≤ 300, KA-5 spec ≤ 500 per epic). Without caps LLMs balloon docs.

## AI-agent gotchas

- LLMs default to KA-5 (modelling) on any input. Fight this — most real failures are KA-1 (no stakeholder map) or KA-3 (no traceability). Make the planner explicitly score all 6 KAs.
- Agents will fabricate "industry standard" KPIs in KA-6. Require a citation or a datasource path for every metric; reject otherwise.
- BABOK terminology collides with agile terminology (e.g. "requirement" vs "story", "stakeholder" vs "persona"). Pin a glossary in the agent's system prompt — drift causes traceability errors when artefacts cross teams.
- Verification (KA-5) ≠ Validation (KA-5). Two separate tasks. Don't let one prompt produce both — they require different mental modes (quality vs business fit) and a single pass usually does neither well.
- Multi-agent runs across KAs duplicate stakeholder lists. Centralise stakeholder register in one file referenced by all KA agents — never let each agent maintain its own copy.
- KA-3 traceability matrices require stable IDs. If your agent assigns IDs at generation time, they renumber on every run. Use content-hash IDs (e.g. `REQ-<sha1[:8]>`) or pull IDs from the issue tracker before drafting.

## References

- BABOK Guide v3 (IIBA, 2015) — canonical source for the 6 KAs.
- IIBA Agile Extension v2 — bridges KA framing to scrum/SAFe contexts.
- `skills/faion/knowledge/pro/ba/business-analyst/` — per-methodology agent integrations.
- `skills/faion/knowledge/pro/ba/ba-core/` — 21 core BA methodologies.
- `skills/faion/knowledge/pro/ba/ba-modeling/` — 7 modelling methodologies.
- BABOK Techniques chapter (Ch. 10) — taxonomy used to map KA tasks → techniques → methodologies.
