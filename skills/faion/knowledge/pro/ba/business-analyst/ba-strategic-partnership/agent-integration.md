# Agent Integration — BA Strategic Partnership and Innovation Leadership

## When to use
- Quarterly BA self-assessment: agent reads sprint logs, Jira/Linear exports, decision logs and produces a "Strategic BA Impact" report (initiatives led, opportunities identified, value quantified).
- Opportunity scouting on a backlog dump: agent re-frames stated requirements as outcomes and surfaces upstream business problems the BA missed.
- Pre-steering-committee prep: agent drafts business cases (problem, value hypothesis, leading indicators, kill criteria) from raw stakeholder notes.
- Responsible-AI requirements review: agent cross-checks a feature spec against fairness/transparency/accountability/privacy/oversight criteria and flags gaps.
- Coaching loop for junior BAs: agent contrasts their requirement docs against "strategic BA" rubric (outcome vs feature, enterprise vs project, partner vs order-taker).

## When NOT to use
- Hard-skill BA artifacts (BPMN diagrams, use-case decomposition, traceability matrices) — use `business-process-analysis`, `use-case-modeling`, `requirements-lifecycle` methodologies instead.
- Stakeholder politics, executive influencing, in-person workshops — agent can prep, not execute.
- One-off tactical tickets — overhead of "strategic framing" is wasted on bug fixes or copy changes.
- Regulated procurement / contract negotiation — keep humans accountable, agent only drafts.

## Where it fails / limitations
- Topic is a stance/posture, not a procedure; without org-specific inputs (OKRs, P&L, customer interviews) the agent produces generic "be more strategic" platitudes.
- "Innovation" outputs degrade into LLM-cliché lists (AI! automation! data!) unless grounded in actual constraints and evidence.
- Value quantification ($) is hallucination-prone — agent must cite the numbers' provenance or mark them as assumptions.
- Responsible-AI criteria are jurisdiction-dependent (EU AI Act, NIST AI RMF, ISO/IEC 42001); a generic checklist will miss locale-specific obligations.
- "Strategic partner" status is earned through trust and track record; an agent cannot manufacture it, only support the human BA who builds it.

## Agentic workflow
Use a two-pass diverge/converge pattern. Pass 1 (diverge): a `researcher`-style subagent ingests org artifacts (OKRs, roadmap, customer feedback, support tickets) and produces a long opportunity list with raw evidence links. Pass 2 (converge): a `business-analyst` framing subagent scores each opportunity against strategic-BA competencies (business acumen, value, enterprise scope, responsible-AI fit) and emits a ranked shortlist with business cases. A human BA reviews and selects what to champion. The faion-brainstorm skill provides the diverge/converge skeleton; faion-improver handles the recurring quarterly rhythm.

### Recommended subagents
- `faion-brainstorm` — diverge/converge/review for opportunity ideation against business outcomes.
- `faion-improver` — quarterly self-audit loop: investigate state, find gaps, propose strategic moves, log results.
- `faion-sdd-executor-agent` — turn approved opportunities into SDD spec → design → tasks once green-lit.
- A custom `ba-strategic-framer` subagent (Sonnet) — re-frames requirement docs as outcome statements; flags "order-taker" language.
- `password-scrubber-agent` — scrub stakeholder notes / customer transcripts before they enter the agent loop.

### Prompt pattern
```
ROLE: Strategic Business Analyst.
INPUTS: <OKR file>, <last-quarter delivery log>, <top-10 customer complaints>.
TASK: Produce <=10 opportunities. For each: (1) outcome (KPI delta), (2) evidence trail (cite line numbers), (3) value hypothesis with assumptions flagged, (4) leading indicator, (5) kill criterion, (6) responsible-AI risks if AI/automation involved.
ANTI-PATTERNS: feature lists, generic "drive innovation" phrases, unsourced dollar amounts.
OUTPUT: structured JSON matching schema in templates section.
```

```
ROLE: BA coach. Compare INPUT requirement doc against strategic-BA rubric.
For each section emit: stance (order-taker | strategic-partner), evidence quote, rewrite suggestion. Score 0-5 on: outcome-orientation, enterprise scope, value quantification, responsible-AI coverage.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `linear-cli` / `gh` / `jira-cli` | Pull backlog and outcomes for opportunity mining | `npm i -g @linear/cli`; `gh` via package manager; `pip install jira-cli` |
| `pandoc` | Convert stakeholder docs / interview transcripts to clean markdown for agent ingest | `apt install pandoc` |
| `dvc` / `git-lfs` | Version evidence artifacts (data exports, transcripts) cited in business cases | `pip install dvc` |
| `whisper.cpp` / `faster-whisper` | Transcribe stakeholder interviews locally before agent processing | github.com/ggerganov/whisper.cpp |
| `aichat` / `llm` (Simon Willison) | Quick CLI chains for opportunity-list re-ranking | `pip install llm` |
| `csvkit` / `duckdb` | Quantify opportunity value from raw CSV exports | `pip install csvkit duckdb` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes (REST + GraphQL API, webhooks) | Outcomes, projects, cycle reviews |
| Productboard | SaaS | Partial (Public API, no streaming) | Opportunity capture + insights linking |
| Aha! | SaaS | Yes (REST API) | Strategy → goals → initiatives → features |
| Jira + Atlassian Intelligence | SaaS | Yes (REST + Forge) | Outcome roadmaps, AI summaries |
| Mural / Miro | SaaS | Limited (REST API; agents struggle with spatial canvases) | Workshop facilitation by humans, agent post-processing |
| Dovetail | SaaS | Yes (API) | Customer research repository — feed agent for opportunity mining |
| Glean / Hebbia | SaaS (enterprise search) | Yes (API) | Cross-system evidence retrieval for business cases |
| OpenProject | OSS | Yes (REST API) | Self-host alternative for BA artifacts |
| n8n / Temporal | OSS | Yes | Orchestrate quarterly review pipelines (faion-net runs n8n on port 5678) |
| Holistic AI / Credo AI | SaaS | Yes (API) | Responsible-AI governance evidence for spec reviews |

## Templates & scripts

See `templates.md` (currently empty — extend with the impact assessment template inlined in `README.md`).

Inline helper: opportunity-list re-ranker. Reads a markdown opportunity dump on stdin, emits ranked JSON with strategic-BA scores. Drop into `~/bin/ba-rank-opps`.

```bash
#!/usr/bin/env bash
# ba-rank-opps — rank BA opportunities via LLM CLI against strategic rubric.
# Usage: cat opportunities.md | ba-rank-opps > ranked.json
set -euo pipefail
: "${MODEL:=claude-opus-4-7}"
RUBRIC='Score 0-5 on: outcome_orientation, enterprise_scope,
value_quantification, evidence_strength, responsible_ai_coverage.
Reject any item lacking evidence trail or kill criterion.
Output strict JSON: {ranked:[{title,scores,total,reject_reason?}]}.'
INPUT=$(cat)
llm -m "$MODEL" --no-stream <<EOF
You are a strategic BA reviewer. Rubric: $RUBRIC
OPPORTUNITIES:
$INPUT
Return JSON only.
EOF
```

Pair with a guard: any opportunity scoring <3 on `evidence_strength` is auto-rejected before reaching humans.

### Opportunity JSON schema (canonical)

```json
{
  "title": "string",
  "outcome": {
    "kpi": "string",
    "current": "number",
    "target": "number",
    "horizon_months": "integer"
  },
  "evidence": [
    {"source": "string (file/URL)", "quote": "string", "locator": "string"}
  ],
  "value_hypothesis": {
    "amount_usd": "number|null",
    "value_method": "top_down|bottom_up|analogous|parametric|qualitative",
    "assumptions": ["string"]
  },
  "leading_indicator": "string",
  "kill_criterion": "string",
  "responsible_ai": {
    "applicable": "boolean",
    "frameworks": ["EU_AI_Act|NIST_AI_RMF|ISO_42001|none"],
    "controls": ["string"]
  },
  "scores": {
    "outcome_orientation": 0,
    "enterprise_scope": 0,
    "value_quantification": 0,
    "evidence_strength": 0,
    "responsible_ai_coverage": 0
  }
}
```

### Workflow diagram

OKRs + tickets + interviews → scrub PII → diverge (researcher subagent) → raw opportunities → converge (BA framer) → ranked JSON → human BA review → steering committee → SDD spec/design (faion-sdd-executor-agent) → quarterly retro (faion-improver) → memory update.

## Best practices
- Always demand an evidence trail (file path + line range or URL + quote) for every claim; agents fabricate confidently otherwise.
- Separate "outcome" (KPI delta) from "output" (feature) in the schema — forces the model out of feature-list mode.
- Keep a kill-criterion field mandatory; without it, "innovation" lists become wish lists.
- Run the strategic-BA rubric as a second-pass scorer, not as part of the generation prompt — judging-while-generating dilutes both.
- Version stakeholder evidence (DVC / git-lfs) so business cases remain auditable when challenged 6 months later.
- For responsible-AI sections, point the agent at the specific framework in scope (EU AI Act Annex III, NIST AI RMF GOVERN/MAP/MEASURE/MANAGE) — generic prompts produce generic outputs.
- Schedule the loop quarterly via cron + faion-improver; one-shot runs miss compounding value.
- Treat agent output as a draft for the human BA's executive narrative, never the narrative itself — strategic credibility is non-delegable.

## AI-agent gotchas
- Hallucinated dollar values: agent will produce confident "$2.3M annual savings" with no source. Mitigation: schema requires `value_method` (top-down / bottom-up / analogous / parametric) and `assumptions[]`.
- "Strategic" buzzword soup: outputs collapse to generic phrases ("drive transformation", "leverage AI"). Mitigation: ban a stoplist in the system prompt; reject responses containing them.
- Confirmation bias on stated requirements: if the BA's old docs are in context, agent rationalizes them rather than challenging. Mitigation: red-team pass with a separate subagent instructed to invert assumptions.
- Responsible-AI checkbox theater: agent ticks all five pillars (fairness/transparency/accountability/privacy/oversight) without specifics. Mitigation: each pillar must reference a concrete control (e.g., "demographic parity threshold 0.05", "model card field X").
- Privacy leakage: stakeholder transcripts often contain PII / commercial-sensitive data. Mitigation: run `password-scrubber-agent` (and a PII scrubber) before any LLM call; prefer local Whisper for transcription.
- Cross-tier model drift: this methodology lives in `pro/`; readers may be on `solo/` tier without access to enterprise tooling. Keep prompts portable (CLI + flat-file inputs) so the workflow degrades gracefully.
- Human-in-the-loop checkpoints: (1) before any opportunity reaches a steering committee, (2) before any AI-related opportunity is greenlit, (3) before value claims appear in board materials. Never auto-publish.

## References
- IIBA, BABOK Guide v3 — chapters on Strategy Analysis and Solution Evaluation.
- IIBA Global Business Analysis Trends 2025/2026 reports — strategic-partner positioning data.
- NIST AI Risk Management Framework (AI RMF 1.0) — GOVERN/MAP/MEASURE/MANAGE controls.
- EU AI Act (Regulation 2024/1689) — Annex III high-risk obligations relevant to BA-led specs.
- ISO/IEC 42001:2023 — AI management system requirements.
- Teresa Torres, "Continuous Discovery Habits" — opportunity solution trees.
- Marty Cagan, "Transformed" — outcome-driven product/BA partnership patterns.
- Anthropic Claude Code subagents docs — `https://docs.anthropic.com/en/docs/claude-code/sub-agents`.
