# Agent Integration — Modern BA Framework (ba-core fundamentals & selection)

This is the *fundamentals* angle: what the major BA reference frameworks actually are (BABOK v3 + BA Standard 2025, IREB CPRE, PMI-PBA / Business Analysis for Practitioners, BCS Diploma, SAFe Business Analyst, Agile Extension to BABOK), and how an LLM agent picks ONE primary framework for a given engagement before doing any actual analysis. Sibling `business-analyst/modern-ba-framework/agent-integration.md` covers the *routing* angle (mapping KAs onto modern delivery contexts); this file covers *selection* — choose the framework, calibrate vocabulary, then route.

## When to use

- Onboarding a BA / agent into an unfamiliar org and the company "BA standard" is unclear or contested. Pick a primary framework before writing artifacts.
- Procurement / RFP responses that name a specific standard (BABOK v3, IREB, CMMI-DEV PA:RD) — the agent must align deliverable vocabulary exactly to win evaluation points.
- Regulated industries (pharma GxP, banking BCBS 239, automotive ASPICE) where requirements-engineering is auditable. IREB CPRE-aligned artifacts pass audit; loose user stories often do not.
- Multi-vendor programs where each vendor uses a different BA dialect — agent normalizes everything to one canonical framework's terms.
- Hybrid agile/waterfall portfolios. The Agile Extension to BABOK v2 + BABOK v3 combo is the standard "bridge"; the agent must know which clause maps to which Scrum/SAFe ceremony.
- Building an internal BA training curriculum or competency matrix — must anchor on a published framework's syllabus (IIBA, IREB, PMI, BCS).

## When NOT to use

- The team already has a working BA practice and a known reference (e.g. "we follow IIBA + Scrum"). Forcing a re-selection is rework theatre.
- Solo founder / 1-2 person product. No framework will improve outcomes vs. continuous discovery + plain user stories. Use `solo/product/product-planning` instead.
- Pure UX or growth work; BA frameworks under-specify research and experimentation. Use `pro/ux/ux-researcher` and `pro/marketing/conversion-optimizer`.
- One-shot tactical analysis (a single ticket clarification). Loading a meta-framework wastes tokens; load the specific sibling methodology directly.
- Org explicitly anti-IIBA (some product-led companies treat BABOK as bureaucratic). Pick `Agile Extension` or skip to product-discovery methodologies.

## Where it fails / limitations

- **Vocabulary churn.** "BA Standard (2025)" partially supersedes parts of BABOK v3 (2015). The README in this folder mixes both eras; an agent quoting the file verbatim will conflate concepts. Always cross-check against current IIBA publications.
- **No selection rubric.** README enumerates frameworks but gives no decision criteria for picking one. Agent must supply the rubric (regulation, contract, team maturity, delivery model) externally.
- **Certification ≠ skill.** ECBA/CCBA/CBAP measure exam pass rate, not analyst quality with LLM tools, RAG, or evals. Treat the cert table in README as procurement signaling, not capability.
- **"Modern application" tables are descriptive.** No procedures, no acceptance tests, no inputs/outputs. Agents that treat them as instructions produce hand-wavy plans.
- **Empty companion files.** `checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md` are zero bytes — selection logic must be supplied by `agent-integration.md` (this file) until the methodology is filled.
- **IIBA-centric.** The README does not mention IREB CPRE-FL/AL, BCS, PMI-PBA, or SWEBOK at depth; an agent that defaults to BABOK in a non-IIBA shop creates friction.
- **Static perspective list.** Five BABOK perspectives miss data-product, AI-product-ownership, platform-engineering — common in 2025-2026.

## Agentic workflow

Run a **selector subagent** that takes org context (industry, regulation, team size, delivery model, existing standards, contract obligations) and emits a `ba-framework-decision.md`: chosen primary framework, secondary/extension frameworks, rationale, vocabulary glossary, and a deviations log. This decision is *upstream* of the routing planner described in the business-analyst sibling — selection picks the rulebook, then routing picks the plays. Persist the decision under `.aidocs/<feature>/ba-framework-decision.md` and require a human PO/BA sign-off; the file becomes the single source of truth that downstream methodologies (stakeholder-analysis, requirements-lifecycle, etc.) read for terminology.

### Recommended subagents

- `faion-brainstorm` — Diverge across candidate frameworks (BABOK v3, IREB CPRE, PMI-PBA, BCS, SAFe BA, Agile Extension) before converging on one. Forces the agent off its default-IIBA prior.
- `faion-feature-executor` — After selection, executes the routing planner from sibling `business-analyst/modern-ba-framework`; the chosen framework's vocabulary is passed as context to every executor step.
- `faion-sdd-executor-agent` — Wraps BA artifacts (requirements, validation, traceability) inside the SDD `spec.md` / `design.md` / `test-plan.md` lifecycle so the framework choice survives into delivery.
- `faion-improver` — Periodic audit: compares produced artifacts vs. chosen framework's required deliverables; flags drift (e.g. team chose IREB but produces only loose stories with no glossary).
- General `Task` subagent — One per candidate framework, summarizes that framework's mandatory artifacts and audit hooks; outputs feed the selector's converge step.
- Routing per task: framework-comparison tables → haiku, decision rationale prose → sonnet, regulatory mapping (GxP/ASPICE/BCBS) → opus.

### Prompt pattern

Selector pass:

```
Inputs: industry, regulation_set[], team_size, delivery_model, contract_clauses[],
        existing_standards[], stakeholder_count, audit_required (bool).
Candidates: BABOK_v3, BA_Standard_2025, IREB_CPRE, PMI_PBA, BCS_Diploma,
            SAFe_BA, Agile_Extension_BABOK_v2, SWEBOK_v4_KA_Requirements.
Score each on: regulatory_fit, team_maturity_fit, vocab_overlap_with_existing,
              tooling_support, certification_availability, agile_friendliness.
Pick ONE primary + up to 2 extensions. Produce vocabulary glossary
(BA term -> chosen-framework term -> sibling-methodology slug).
Emit ba-framework-decision.md. Halt for human sign-off.
```

Audit pass (after delivery):

```
Inputs: ba-framework-decision.md, list of produced artifacts in .aidocs/<feature>/.
For each mandatory deliverable in chosen framework, check presence + quality.
Emit framework-conformance.md with PASS/FAIL per artifact and remediation.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| IIBA member portal (no CLI) | Authoritative BABOK v3 + BA Standard 2025 PDFs | https://www.iiba.org/standards-and-resources/babok/ |
| IREB downloads | CPRE Foundation/Advanced syllabi (free PDFs) | https://www.ireb.org/en/downloads |
| PMI Standards | Business Analysis for Practitioners (PMI-PBA reference) | https://www.pmi.org/standards |
| BCS specifications | BCS Diploma in BA syllabi | https://www.bcs.org/qualifications-and-certifications/certifications-for-business/business-analysis/ |
| SWEBOK v4 | KA: Software Requirements (IEEE) | https://www.computer.org/education/bodies-of-knowledge/software-engineering |
| `gh` + `gh project` | Pull GitHub Issues/Projects to feed selector with current artifact inventory | https://cli.github.com |
| `jira-cli` / `acli` | Same for Jira / Jira Align portfolios | https://github.com/ankitpokhrel/jira-cli |
| `pandoc` | Render `ba-framework-decision.md` to DOCX/PDF for procurement/audit | `apt install pandoc` |
| `mermaid-cli` (`mmdc`) | Diagram framework coverage matrix | `npm i -g @mermaid-js/mermaid-cli` |
| `yq` / `jq` | Validate the decision JSON (if you also emit machine form) | `apt install yq jq` |
| `pre-commit` | Reject `.aidocs/<feature>/` commits missing `ba-framework-decision.md` | https://pre-commit.com |
| `glow` / `mdcat` | Terminal render decision doc for human review | https://github.com/charmbracelet/glow |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| IIBA KnowledgeHub | SaaS (paid) | No public API | Cache PDFs locally; agent reads from cache to avoid hallucinating clause numbers. |
| IREB exam portal | SaaS | No API | Download CPRE syllabi PDFs; treat as ground truth for IREB vocabulary. |
| Jira / Jira Align | SaaS | Yes (REST + acli) | Inventory existing artifacts as selector input; tag stories with chosen framework's term. |
| Linear | SaaS | Yes (GraphQL) | Lighter-weight backlog source for solopreneur / small-team selection runs. |
| Azure DevOps | SaaS | Yes (`az boards`) | Common in BCBS/ASPICE shops; query existing work-item types to detect implicit framework. |
| Confluence / Notion | SaaS | Yes (REST) | Persist `ba-framework-decision.md` and glossary as canonical org doc. |
| Polarion / Jama Connect | SaaS | Yes (REST) | Regulated-industry RM tools; presence implies IREB/ASPICE-style framework already in play. |
| DOORS Next | SaaS | Yes (OSLC) | Banking/aerospace; same signal as Polarion. |
| Camunda / Signavio | SaaS/OSS | Yes (REST + BPMN) | If org runs BPM heavily, BABOK BPM perspective + BPMN tooling is a strong selection signal. |
| LinkedIn Learning / Coursera | SaaS | Limited API | Map cert gap → curriculum once framework is chosen. |
| GitHub Projects v2 | SaaS | Yes (GraphQL) | Lightweight inventory for small teams; agent infers de-facto framework from issue templates. |
| n8n / Airflow | OSS | Yes | Schedule audit pass on sprint cadence; alerts when conformance drops. |

## Templates & scripts

Inline framework-selector skeleton (≤50 lines, bash + jq) — drops a starter `ba-framework-decision.json` for a feature. Fill it in interactively or via a planner LLM call:

```bash
#!/usr/bin/env bash
# ba-framework-select.sh — scaffold a primary-framework decision for a feature
set -euo pipefail
FEATURE="${1:?usage: ba-framework-select.sh <feature-slug>}"
DIR=".aidocs/${FEATURE}"
mkdir -p "$DIR"
cat > "$DIR/ba-framework-decision.json" <<'JSON'
{
  "context": {
    "industry": "",
    "regulation_set": [],
    "team_size": 0,
    "delivery_model": "",
    "contract_clauses": [],
    "existing_standards": [],
    "audit_required": false
  },
  "candidates_scored": {
    "BABOK_v3":              {"regulatory_fit": 0, "agile_fit": 0, "vocab_overlap": 0, "total": 0},
    "BA_Standard_2025":      {"regulatory_fit": 0, "agile_fit": 0, "vocab_overlap": 0, "total": 0},
    "IREB_CPRE":             {"regulatory_fit": 0, "agile_fit": 0, "vocab_overlap": 0, "total": 0},
    "PMI_PBA":               {"regulatory_fit": 0, "agile_fit": 0, "vocab_overlap": 0, "total": 0},
    "BCS_Diploma":           {"regulatory_fit": 0, "agile_fit": 0, "vocab_overlap": 0, "total": 0},
    "SAFe_BA":               {"regulatory_fit": 0, "agile_fit": 0, "vocab_overlap": 0, "total": 0},
    "Agile_Extension_BABOK": {"regulatory_fit": 0, "agile_fit": 0, "vocab_overlap": 0, "total": 0},
    "SWEBOK_v4_Reqs":        {"regulatory_fit": 0, "agile_fit": 0, "vocab_overlap": 0, "total": 0}
  },
  "primary": "",
  "extensions": [],
  "rationale": "",
  "glossary": {},
  "deviations": [],
  "human_signoff_required": true
}
JSON
echo "Initialized $DIR/ba-framework-decision.json — fill scores, pick primary, commit."
```

Sibling methodologies (load on demand once primary framework is chosen): `ba-planning`, `ba-governance`, `stakeholder-analysis`, `elicitation-techniques`, `requirements-lifecycle`, `requirements-validation`, `requirements-traceability`, `strategy-basics`, `strategy-methods`, `solution-assessment`, `agile-ba-frameworks`.

## Best practices

- Pick **one primary framework**, list extensions explicitly. Two co-equal primaries always cause vocabulary thrash and audit ambiguity.
- Build a vocabulary glossary mapping the chosen framework's terms to the org's existing terms before any artifact is produced; persist as `glossary.md` next to the decision file.
- In regulated settings, score `regulatory_fit` first and let it veto agile-friendly frameworks. SAFe BA is a poor fit for ASPICE / BCBS 239 audits.
- Cache PDFs of BABOK v3, BA Standard 2025, IREB CPRE-FL/AL, PMI-PBA into a read-only fact-source; force the agent to cite from the cache, not from training data.
- Treat the IIBA cert ladder (ECBA → CCBA → CBAP, plus AAC/CBDA/CPOA) as procurement signaling — it satisfies RFP scorecards but does not predict LLM-era BA performance.
- Record deviations from the chosen framework in a `deviations[]` log with rationale; never silently drop a mandatory artifact.
- Re-run the selector when one of these changes: regulation set, contract, primary delivery model (waterfall ↔ agile ↔ hybrid), or M&A integration. Otherwise the decision survives across sprints.
- Pair this decision with the routing planner from sibling `business-analyst/modern-ba-framework`. Selection without routing produces a vocabulary doc nobody uses.

## AI-agent gotchas

- LLMs default to **BABOK** because it is the most-tokenized BA reference in training data. Force structured candidate scoring or you'll never see IREB / PMI-PBA / BCS picked.
- Models confabulate clause numbers, KA boundaries, and IIBA version dates. Pin a fact-source file (cached BABOK ToC + BA Standard ToC + IREB CPRE syllabi) and require citations.
- "BA Standard (2025)" wording in the README will go stale; agent must check current IIBA publication titles before quoting versions to humans.
- The Agent Selection table at the bottom of the README is *advisory*. Cost regressions appear when the planner downgrades opus → sonnet for "gap analysis" or regulatory mapping; lock the model per task in the decision JSON.
- Human-in-the-loop checkpoint is **mandatory** between selection and routing. Auto-execution skips the only place a real PO/BA can correct framework bias (especially the default-BABOK pull).
- Vocabulary glossary is sensitive: in M&A or vendor contexts it can leak commercial terms. Run `password-scrubber-agent` and tag the doc as confidential before persisting outside private repos.
- Don't let the agent edit the README's tables; it tends to "modernize" them every run, churning git history. Confine edits to `agent-integration.md` and `.aidocs/<feature>/`.
- Certification recommendations leak vendor bias (IIBA-only). Cross-reference IREB, PMI-PBA, BCS, and Scrum.org product-owner tracks before presenting to the user.
- Don't quote CMMI-DEV process areas as "framework" peers without flagging that CMMI is a maturity model, not a BA reference; mixing the two confuses procurement.

## References

- IIBA — BABOK Guide v3 + Business Analysis Standard (2025): https://www.iiba.org/standards-and-resources/babok/
- IIBA Agile Extension to BABOK v2: https://www.iiba.org/professional-development/knowledge-centre/agile-extension/
- IREB — CPRE Foundation Level + Advanced Level syllabi: https://www.ireb.org/en/downloads
- PMI — Business Analysis for Practitioners (PMI-PBA reference): https://www.pmi.org/standards
- BCS — Diploma in Business Analysis: https://www.bcs.org/qualifications-and-certifications/certifications-for-business/business-analysis/
- SWEBOK v4 — KA: Software Requirements (IEEE): https://www.computer.org/education/bodies-of-knowledge/software-engineering
- SAFe — Business Analyst / Product Owner role descriptions: https://scaledagileframework.com
- SFIA v9 framework: https://sfia-online.org/en/sfia-9
- IIBA Certifications: ECBA, CCBA, CBAP, AAC, CBDA, CPOA — https://www.iiba.org/business-analysis-certifications/
- Sibling routing-angle file: `../../business-analyst/modern-ba-framework/agent-integration.md`
