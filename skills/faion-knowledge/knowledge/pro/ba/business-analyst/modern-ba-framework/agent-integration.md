# Agent Integration — Modern BA Framework (BABOK + BA Standard 2025)

This methodology is a *meta-framework*: it tells you how to map the six BABOK Knowledge Areas onto modern delivery contexts (agile, AI/ML, cloud, platform, process-mining). The deliverable for an LLM agent is not "do BA" — it is a **routing decision** ("for this work, which methodologies apply, in which order, with which competencies") plus a competency-gap report. Drive it as a planner-style subagent that reads work context once, picks the right downstream methodologies, and sequences them.

## When to use

- Onboarding a new BA / PO to a project: the agent reads project context (repo, tickets, stakeholder list) and emits a tailored "BA approach" that picks methodologies from the 6 KAs based on Agile / BI / IT / BizArch / BPM perspective.
- Migration audits: shifting an enterprise from waterfall BABOK artifacts (BRD/SRS/RTM) to agile/lean BA — agent maps each existing artifact to its modern equivalent (story map, opportunity tree, decision log).
- Certification-aligned skill assessment: scoring a team against ECBA/CCBA/CBAP/AAC/CBDA/CPOA competencies, producing a gap matrix vs. SFIA v9.
- Multi-perspective discovery: when a workstream touches Agile + BI + Bus.Architecture simultaneously (e.g. an internal AI platform), the framework's perspective dimension forces the agent to pick the right BA techniques per perspective rather than defaulting to one.
- Tooling / model selection: routing per-task to haiku / sonnet / opus based on the README's Agent Selection table (mechanical formatting → haiku, gap analysis → opus).

## When NOT to use

- A specific BA task is already scoped (write AC, run elicitation workshop, build a BPMN). Skip the meta-framework — load the concrete sibling methodology directly (`acceptance-criteria`, `elicitation-techniques`, `business-process-analysis`).
- Pure non-BA work (pure code refactor, infra hardening). The framework will manufacture BA scaffolding nobody asked for.
- Solo founders with no enterprise / hybrid team — most "modern application" tables collapse to a single perspective and the routing value is near zero.
- Greenfield product discovery where you don't yet know stakeholders or a problem statement. Use `continuous-discovery` / `opportunity-solution-trees` first; come back to this for governance.

## Where it fails / limitations

- **Not executable.** README is descriptive (tables of "modern application"); there are no procedures, inputs, outputs, or acceptance tests. An agent applying it without sibling methodologies produces hand-wavy plans.
- **Empty companion files.** `checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md` are empty in this repo — the agent cannot draw structured prompts/templates from the methodology itself; it must synthesize from siblings.
- **Static perspective list.** Five BABOK perspectives miss data-product, AI-product-ownership, and platform-engineering perspectives now common in 2025-2026. The agent must extend the table or risk routing AI/ML work into a stale Agile/BI bucket.
- **Certification-to-real-skill drift.** ECBA/CCBA/CBAP signal coverage, not capability with LLMs, RAG, prompt design, or evals. Don't treat the cert table as a hiring filter for AI-era BA.
- **No KPI surface.** Framework gives no measurable output — easy to declare "modernized" without proving anything changed in cycle time, defect rate, or stakeholder NPS.
- **Recency risk.** "BA Standard (2025)" wording will go stale; the agent must check current IIBA publications before quoting versions to humans.

## Agentic workflow

Run a **planner subagent** that takes a work brief + repo context and emits a BA Approach JSON: `{perspective[], knowledge_areas[], methodologies[], competencies_needed[], model_routing{}}`. The planner does not execute BA work — it routes. A second pass (executor) loads each chosen sibling methodology (`stakeholder-analysis`, `requirements-validation`, etc.) and runs the actual analysis. State lives in `.aidocs/<feature>/ba-approach.md` and is re-read on every sprint or milestone for drift detection. Human PO/BA approves the approach before any execution starts; otherwise the agent will self-justify a default plan.

### Recommended subagents

- `faion-brainstorm` — Diverge across perspectives (Agile vs. BI vs. BizArch lens) before converging on one approach; reduces the LLM tendency to default to "Agile" for everything.
- `faion-feature-executor` — Consumes the BA Approach plan and runs each KA's chosen methodology in order, with quality gates between KAs (Strategy → Requirements → Design → Evaluation).
- `faion-sdd-executor-agent` — When the work is delivery-bound, wraps the BA approach inside an SDD feature (`spec.md`, `design.md`, `test-plan.md`) so requirements get traced into code.
- `faion-improver` — Periodic audit of BA Approach drift: compares plan vs. actual artifacts, flags KAs that were skipped.
- General `Task` subagent — One per KA, with that KA's sibling methodology files passed as system context.
- Routing per task (per README's Agent Selection): mechanical formatting → haiku, AC writing / requirements analysis → sonnet, gap analysis / BPMN architecture → opus.

### Prompt pattern

Planner pass:

```
Inputs: <project-brief>, <stakeholder-list>, <repo-tree>, <existing-tickets>.
Pick: 1-3 BABOK perspectives (Agile, BI, IT, BizArch, BPM, +Data-Product, +AI-Product).
For each KA (BAP&M, E&C, RLM, SA, RA&D, SE) decide INCLUDE/SKIP with one-sentence rationale.
For each INCLUDE'd KA, name 1-2 sibling methodologies from .../business-analyst/.
Emit JSON to .aidocs/<feature>/ba-approach.json. Halt for human PO sign-off.
```

Competency-gap pass:

```
Inputs: team roster + skill self-assessments, BA approach JSON.
For each competency (Analytical, Behavioral, BizKnowledge, Communication, Interaction, Tools&Tech) score Have / Need / Gap.
Map gaps to ECBA/CCBA/CBAP/AAC/CBDA/CPOA training tracks and SFIA v9 levels.
Emit competency-gap.md with ranked hiring/training recommendations.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `iiba-babok` (no official CLI) — fetch from IIBA member portal | Authoritative BABOK / BA Standard text | https://www.iiba.org/standards-and-resources/babok/ |
| `acli` / `jira-cli` | Pull tickets to feed planner with real project context | https://developer.atlassian.com/cloud/acli ; https://github.com/ankitpokhrel/jira-cli |
| `gh` + `gh project` | Read GitHub Issues / Projects v2 backlog as input | https://cli.github.com |
| `glow` / `mdcat` | Render the BA Approach markdown for human review | https://github.com/charmbracelet/glow |
| `mermaid-cli` (`mmdc`) | Render KA dependency / perspective diagrams from generated mermaid | `npm i -g @mermaid-js/mermaid-cli` |
| `pandoc` | Convert ba-approach.md → DOCX/PDF for non-technical stakeholders | `apt install pandoc` |
| `yq` / `jq` | Validate / transform the BA Approach JSON in CI | `apt install yq jq` |
| `pre-commit` | Reject commits to `.aidocs/<feature>/` lacking required KA sections | https://pre-commit.com |
| `sfia-mapper` (community Python) | Map competencies to SFIA v9 levels | https://sfia-online.org/en |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| IIBA KnowledgeHub | SaaS (paid) | No public API | Source of truth for BABOK/BA Standard; agent must rely on cached PDFs. |
| Jira / Jira Align | SaaS | Yes (REST + acli) | Ingest backlog & SAFe portfolio for the planner. |
| Linear | SaaS | Yes (GraphQL SDK) | Smaller teams; cycles map to KA cadence. |
| Azure DevOps | SaaS | Yes (`az boards`) | Common in regulated enterprises adopting modern BA. |
| Lucid / Miro | SaaS | Partial (Miro REST OK; Lucid limited) | For perspective workshops; agent posts artifacts back. |
| Confluence / Notion | SaaS | Yes (REST) | Persist BA Approach + competency-gap docs as canonical. |
| Camunda / Signavio | SaaS/OSS | Yes (REST + BPMN XML) | BPM perspective execution surface. |
| Power BI / Tableau / Metabase | SaaS / OSS | Partial | BI-perspective deliverables; agent emits dataset specs not visuals. |
| Workday Skills Cloud / Gloat | SaaS | API gated | Competency-gap inputs in large enterprises. |
| LinkedIn Learning / Coursera | SaaS | Yes (limited API) | Auto-route certification gap → course list. |
| GitHub Projects v2 | SaaS | Yes (`gh project`, GraphQL) | Lightweight backlog source for solopreneur context. |
| n8n / Airflow | OSS | Yes | Schedule planner re-runs on sprint cadence. |

## Templates & scripts

Inline planner skeleton (≤50 lines, bash + jq), drops a starter `ba-approach.json` for a feature:

```bash
#!/usr/bin/env bash
# ba-approach-init.sh — scaffold a Modern BA Framework approach for a feature
set -euo pipefail
FEATURE="${1:?usage: ba-approach-init.sh <feature-slug>}"
DIR=".aidocs/${FEATURE}"
mkdir -p "$DIR"
cat > "$DIR/ba-approach.json" <<'JSON'
{
  "perspectives": [],
  "knowledge_areas": {
    "ba_planning_monitoring":    {"include": null, "methodologies": [], "rationale": ""},
    "elicitation_collaboration": {"include": null, "methodologies": [], "rationale": ""},
    "requirements_lifecycle":    {"include": null, "methodologies": [], "rationale": ""},
    "strategy_analysis":         {"include": null, "methodologies": [], "rationale": ""},
    "requirements_analysis_design": {"include": null, "methodologies": [], "rationale": ""},
    "solution_evaluation":       {"include": null, "methodologies": [], "rationale": ""}
  },
  "competencies_needed": [],
  "model_routing": {
    "format_requirements": "haiku",
    "write_acceptance_criteria": "sonnet",
    "validate_with_stakeholders": "sonnet",
    "gap_analysis": "opus",
    "bpmn_modeling": "opus"
  },
  "human_signoff_required": true
}
JSON
echo "Initialized $DIR/ba-approach.json — fill perspectives + KA decisions, then commit."
```

Sibling methodologies (load on demand): `ba-planning`, `stakeholder-analysis`, `elicitation-techniques`, `requirements-lifecycle`, `requirements-validation`, `strategy-analysis`, `business-process-analysis`, `use-case-modeling`, `acceptance-criteria`, `solution-assessment`.

## Best practices

- Treat the framework as a **router**, not a deliverable. Output is `ba-approach.json`, not "a BA report".
- Force perspective declaration up front. Default-Agile routing hides BizArch and BPM concerns until late.
- Persist the approach under `.aidocs/<feature>/` and diff it sprint-over-sprint to catch silent scope shifts.
- Map every INCLUDE'd KA to at least one *executable* sibling methodology — a KA without a methodology is theatre.
- Score competencies against SFIA v9 *and* certification curricula separately; certs ≠ skills.
- Re-run the planner whenever stakeholders, perspective, or delivery model changes (e.g., team adopts SAFe, or product pivots to data-product).
- Cache IIBA PDFs locally; the agent must not invent BABOK clause numbers under hallucination pressure.

## AI-agent gotchas

- LLMs over-fit to the **Agile** perspective. Force a structured perspective-selection step or you'll never see BizArch / BPM picks.
- The model often confabulates IIBA version numbers. Pin a fact-source file (cached BABOK ToC + BA Standard ToC) and require citations.
- Agent Selection table in README is *advisory*. Cost regressions happen when the planner downgrades opus → sonnet for "gap analysis"; lock model per task in the JSON.
- Human-in-the-loop checkpoint is **mandatory** between planner and executor. Auto-execution skips the only place a real PO/BA can correct perspective bias.
- Competency-gap output is sensitive PII when it names individuals. Run `password-scrubber-agent` and remove names before persisting outside private repos.
- Don't let the agent edit the README's tables; it tends to "modernize" them every run, churning git history. Confine edits to `agent-integration.md` and `.aidocs/<feature>/`.
- Certification recommendations leak vendor bias (IIBA-only). Cross-reference PMI-PBA, BCS, and Scrum.org product-owner tracks before presenting to the user.

## References

- IIBA — BABOK Guide v3 + Business Analysis Standard (2025): https://www.iiba.org/standards-and-resources/babok/
- IIBA Agile Extension to BABOK v2: https://www.iiba.org/professional-development/knowledge-centre/agile-extension/
- SFIA v9 framework: https://sfia-online.org/en/sfia-9
- SAFe 6.0 BA / Product Owner roles: https://scaledagileframework.com
- Teresa Torres — Continuous Discovery Habits (opportunity-solution trees, complementary to BABOK Strategy Analysis)
- Marty Cagan — Inspired / Empowered (modern product BA blend with PO competencies)
- IIBA Certifications: ECBA, CCBA, CBAP, AAC, CBDA, CPOA — https://www.iiba.org/business-analysis-certifications/
