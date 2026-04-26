# Agent Integration — BA Methodologies Detail (Index Reference)

This file is an index/detail reference grouping 12 BA frameworks (governance,
communication, elicitation prep, requirements maintenance, change impact,
current/future state, risk, change strategy, requirements architecture,
solution options, solution limitations) plus the BABOK 50-technique table.
The agent guidance below applies to driving the **whole detail catalog** —
selecting which framework to apply, chaining them, and feeding outputs between
them. For deep guidance on a specific framework, defer to its sibling
methodology folder (e.g. `risk-assessment/`, `business-process-analysis/`,
`solution-assessment/`, `decision-analysis/`).

## When to use

- Project kickoff: need to pick *which* BA frameworks to run for this
  initiative (not all 12 apply to every project).
- Mid-project routing: a stakeholder asks an ambiguous question
  ("can we do X?") and you need to map it to the right BABOK technique
  before drafting a deliverable.
- Audit / handover: producing a BA artifact inventory showing which
  frameworks were applied, which outputs exist, and what's missing.
- Training a new analyst (or agent) on the catalog of techniques and when
  each one fits.

## When NOT to use

- For a single, well-scoped deliverable with a known framework — go directly
  to the dedicated methodology folder; don't route through this index.
- Lightweight startup / single-feature work — the 12-framework set assumes
  enterprise / multi-stakeholder context. For a 2-person team building one
  feature, use `user-story-mapping/` + `acceptance-criteria/` and skip the
  rest.
- Pure agile teams that already have story mapping + backlog grooming —
  governance, change control, and requirements architecture frameworks
  often duplicate Scrum/Kanban ceremonies.

## Where it fails / limitations

- **Index, not deep guidance.** Each of the 12 frameworks here is summarized
  in 30-80 lines. Real execution needs sibling methodology folders or BABOK
  v3 itself.
- **No tooling specifics.** Templates are markdown skeletons; they don't tell
  you how to feed them into Jira, Confluence, Azure DevOps, or a backlog tool.
- **Static templates** — risk matrix, scoring rubric, etc. are illustrative.
  Real projects need calibrated weights from stakeholders, which the index
  can't supply.
- **No traceability across frameworks.** The index doesn't show how
  governance decisions feed change-impact analysis, which feeds risk
  analysis, which feeds change strategy. Agents must build that chain
  themselves.
- **BABOK 50-technique table is a lookup, not a tutorial.** Use it for
  recall, not for learning.

## Agentic workflow

Treat this index as a **router**: a Claude subagent reads the methodology
catalog, classifies the user's request into 1-3 frameworks, then loads the
sibling methodology folders for execution. The Agent Selection table at the
bottom of `README.md` already specifies model tiers (haiku for formatting,
sonnet for elicitation/validation, opus for gap analysis and BPMN).

A typical chain: **classifier (sonnet)** → routes to → **executor (sonnet
or opus per table)** → produces deliverable using sibling folder template →
**reviewer (sonnet)** → checks against BABOK technique completeness criteria.

For multi-framework engagements (e.g. discovery phase covering current state
+ future state + gap + risk), run them sequentially with each output piped
into the next as JSON context, not as raw markdown.

### Recommended subagents

- `faion-sdd-executor-agent` — drives any multi-step BA deliverable through
  spec → design → test-plan → implementation phases; works for BA when the
  "implementation" is a written artifact (e.g. requirements baseline).
- Custom `ba-classifier` (sonnet) — single-shot prompt that maps a user
  question to one of the 12 frameworks + a BABOK technique number.
  Build from the `Technique Selection Guide` table in section 3 of the
  README.
- Custom `ba-reviewer` (sonnet) — validates a BA deliverable against the
  acceptance criteria implied by its template (every column filled, every
  risk has owner+response, every option scored, etc.).

### Prompt pattern

Classifier:
```
You are a BA technique classifier. Given the user request below, return JSON:
{"frameworks": ["<one of the 12>", ...], "babok_techniques": [<numbers>],
 "rationale": "<one sentence>"}.
Frameworks: governance, communication-planning, elicitation-prep,
requirements-maintenance, change-impact, current-state, future-state,
risk-analysis, change-strategy, requirements-architecture, solution-options,
solution-limitations.
Request: """<user input>"""
```

Executor (per framework, after classification):
```
Apply the <framework> template from
knowledge/pro/ba/business-analyst/methodologies-detail/README.md section
<N>. Use the user-provided context below. Fill every column; mark unknowns
explicitly as TBD with a question for the human. Output the completed
markdown table only.
Context: """<context>"""
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pandoc` | Convert BA markdown deliverables to docx/pdf for sponsor sign-off | `apt install pandoc` · pandoc.org |
| `jq` | Pipe classifier JSON output into executor prompts | `apt install jq` |
| `mermaid-cli` (`mmdc`) | Render BPMN/flowcharts from frameworks 6, 9, 10 | `npm i -g @mermaid-js/mermaid-cli` |
| `glow` | Terminal preview of generated markdown deliverables | github.com/charmbracelet/glow |
| `csvkit` | Convert risk register / scoring matrices CSV ⇄ markdown | `pip install csvkit` |
| `gh` | Create issues from change requests (framework 5) | cli.github.com |
| `markdownlint-cli2` | Pre-commit lint on BA deliverables | `npm i -g markdownlint-cli2` |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira / Jira Align | SaaS | Yes — REST + MCP | Backlog mgmt (#2), prioritization (#33), item tracking (#26), change requests |
| Confluence | SaaS | Yes — REST | Publish requirements baseline, governance docs, communication plans |
| Azure DevOps | SaaS | Yes — REST + MCP | Same as Jira; better for traceability matrices |
| Lucidchart / draw.io | SaaS / OSS | Partial — diagram XML | Requirements architecture (#10), data flow diagrams (#13) |
| Miro / Mural | SaaS | Limited — board API | Affinity diagrams, brainstorming (#5), workshops (#50) |
| Aha! / ProductBoard | SaaS | Yes — REST | Strategy analysis (frameworks 6-9), opportunity scoring |
| Camunda Modeler | OSS | Yes — BPMN XML | BPMN process modeling (#35), can be parsed/generated by agents |
| Signavio (SAP) | SaaS | Yes — REST | Enterprise process mining + modeling |
| Celonis | SaaS | Yes — REST | Process mining feeds current-state framework (#6) |
| draw.io desktop | OSS | Yes — XML files | Local diagramming, agent-editable |
| Modern Requirements (MR4DevOps) | SaaS | Partial | Use-case modeling (#47) inside Azure DevOps |
| ReqView / Polarion | Commercial | Partial | Heavy traceability + baselines for regulated industries |

## Templates & scripts

This index already contains 12 markdown table templates (one per framework).
Below is a small router script that uses the classifier prompt above to
select frameworks for a given user request and emit a checklist of
deliverables to produce.

```bash
#!/usr/bin/env bash
# ba-route.sh — classify a BA request → emit deliverable checklist
# Usage: ba-route.sh "We need to evaluate three vendor solutions"
set -euo pipefail
REQ="${1:?usage: ba-route.sh \"<request>\"}"
DETAIL_DIR="$(dirname "$0")"
PROMPT=$(cat <<EOF
You are a BA technique classifier. Return ONLY JSON:
{"frameworks":[...],"babok_techniques":[...],"rationale":"..."}.
Frameworks: governance, communication-planning, elicitation-prep,
requirements-maintenance, change-impact, current-state, future-state,
risk-analysis, change-strategy, requirements-architecture, solution-options,
solution-limitations.
Request: """$REQ"""
EOF
)
JSON=$(claude -p "$PROMPT" --output-format json | jq -r '.result')
echo "$JSON" | jq -r '.frameworks[]' | while read -r fw; do
  echo "- [ ] $fw → see $DETAIL_DIR/README.md (search anchor: $fw)"
done
echo "BABOK techniques: $(echo "$JSON" | jq -r '.babok_techniques | join(", ")')"
echo "Rationale: $(echo "$JSON" | jq -r '.rationale')"
```

For sibling-folder execution prompts, templates, and examples specific to
each of the 12 frameworks, see the corresponding methodology directory
(many already have their own `agent-integration.md` — see CHANGELOG entries
for `risk-assessment`, `solution-assessment`, `business-process-analysis`,
`decision-analysis`, etc.).

## Best practices

- **Always run the classifier first.** Don't let an executor agent guess
  which framework to apply — that's where hallucinated deliverables come
  from. The classifier is cheap (one sonnet call) and cuts rework.
- **Keep framework outputs in separate files.** A "BA deliverable" with
  governance + communication + risk + change-strategy in one document is
  unreviewable. Split per framework, link via index.
- **Fill `Owner` columns before submitting.** Every template has
  ownership/responsibility columns. Agents consistently leave them blank,
  which makes the artifact useless for audit.
- **Calibrate scoring weights with humans.** The 25/20/20/20/15 default in
  the Solution Options template is illustrative; ask the sponsor for their
  weights before the agent applies them — otherwise the recommendation is
  garbage-in-garbage-out.
- **Tie risks to requirements.** Cross-reference risk-register IDs (R-001)
  to requirement IDs (FR-001) in framework 8 + framework 10 outputs;
  agents skip this step by default.
- **Version the baseline.** Framework 4 (Requirements Maintenance) only
  works if you actually tag baselines. Use git tags
  (`baseline/2026-Q2-r1`) on the deliverable repo.

## AI-agent gotchas

- **Hallucinated stakeholder names.** Agents fill the
  `Audience Matrix` and `Decision Authority Matrix` with plausible-sounding
  but invented role names ("Steering Committee", "Product Council") that
  don't exist in the org. Require human review of any row containing a
  named role or committee.
- **Score inflation.** When asked to fill the Solution Options scoring
  matrix, agents tend to score every option 3-4 to "stay neutral",
  destroying the discriminating power. Force the prompt to use the full
  1-5 range and justify each score in one sentence.
- **Fake risk probabilities.** P/I scores are guessed, not derived. Make
  the agent attach an `evidence` column (incident history, expert
  judgment, similar project, none) and reject rows with `evidence: none`
  for high-impact risks.
- **Template fill without context.** An agent will happily produce a
  current-state SWOT for a company it knows nothing about. Require a
  context-loading step (document analysis, transcript ingest) before any
  current/future-state framework runs.
- **Loss of traceability across hops.** When chaining
  current-state → future-state → gap → strategy, agents drop IDs between
  steps. Force structured JSON intermediates that preserve the
  capability/requirement IDs.
- **Premature recommendation.** The Solution Options template ends with a
  Recommendation field. Agents fill it before showing scores to the
  human. Configure the prompt to return `"recommendation": "PENDING_HUMAN_REVIEW"`
  by default; only flip to a real recommendation after explicit go-ahead.
- **BABOK 50-technique table misuse.** Agents will pick technique #5
  (Brainstorming) for everything. Constrain selection to ≤3 techniques
  per request and require justification per technique.

## References

- BABOK Guide v3 — IIBA, 2015 (Sections 4-9 map to frameworks 1-12 here).
- IIBA Agile Extension to BABOK v2.
- BPMN 2.0 spec — omg.org/spec/BPMN/2.0
- "Software Requirements" — Karl Wiegers, 3rd ed (governance, change
  control, requirements maintenance).
- "User Story Mapping" — Jeff Patton (complement to framework 7).
- "Business Analysis Techniques: 99 Essential Tools" — Cadle, Paul,
  Turner.
- Sibling methodology folders in this skill: `risk-assessment/`,
  `solution-assessment/`, `business-process-analysis/`,
  `decision-analysis/`, `requirements-lifecycle/`,
  `requirements-validation/`, `ba-planning/`, `user-story-mapping/`,
  `data-driven-requirements/` — each has its own `agent-integration.md`.
