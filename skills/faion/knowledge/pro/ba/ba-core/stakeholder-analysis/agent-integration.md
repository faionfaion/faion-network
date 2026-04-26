# Agent Integration — Stakeholder Analysis (ba-core, fundamentals)

This file is the **ba-core / fundamentals** angle on stakeholder analysis: definitions, classical frameworks (Mendelow power-interest, Mitchell-Agle-Wood salience, RACI/RASCI/DACI), and BABOK alignment. For the agentic-tooling perspective (CLIs, services, register-as-YAML pipeline), see `pro/ba/business-analyst/stakeholder-analysis/agent-integration.md` — do not duplicate.

## When to use

- Establishing the *vocabulary* for an initiative — "stakeholder", "salience", "engagement level", "responsibility" — before a single interview happens; without shared definitions, downstream artifacts disagree.
- Translating BABOK Knowledge Area 1 ("Plan Stakeholder Engagement", task 3.2) into an actual deliverable on a regulated or audited program.
- Onboarding a new BA / agent to an existing program: read the register *and* read the framework definitions so classifications are reproducible.
- Choosing between RACI, RASCI, DACI, RAPID for a specific decision class — the wrong responsibility model causes more friction than missing one entirely.
- Disambiguating "stakeholder" from "user", "persona", "actor" (use-case sense), and "customer" — these conflate constantly in Notion/Confluence pages and break traceability.
- Programs where regulators or auditors will read the artifact (SOX, MDR, ISO 13485, GDPR Art. 35 DPIA): definitions must match the standard's vocabulary verbatim.

## When NOT to use

- Solo / pre-PMF work where ceremony exceeds value — use direct customer discovery and skip formal frameworks.
- Pure code refactor with zero business-stakeholder change — RACI on the engineering team is sufficient; no Mendelow grid needed.
- One-shot decisions with a single accountable owner — DACI/RAPID overhead is wasted; a one-line ADR is enough.
- Open-source community projects where identities are pseudonymous — salience axes (power, legitimacy) cannot be measured.

## Where it fails / limitations

- **Mendelow's power-interest grid (1991)** flattens politics to two axes; it is silent on legitimacy and urgency. Use Mitchell-Agle-Wood when those matter.
- **Mitchell-Agle-Wood salience (1997)** is qualitative — the eight types (dormant, discretionary, demanding, dominant, dangerous, dependent, definitive, non-stakeholder) are descriptive, not predictive; they tell you *who* matters, not *what to do next*.
- **RACI** has known pathologies: too many `R`s, more than one `A`, "C-spam" where everyone is consulted. RASCI adds `S` (Support) which is often more useful than another `R`.
- **DACI** vs **RAPID** vs **RACI** are commonly mixed within one org — the same letter (`A`, `I`, `D`) means different things in each. Pick one model per program and document it.
- Stakeholder ≠ persona ≠ actor ≠ user. Conflating them breaks requirements traceability: a persona has no decision authority; an actor (UML) is a role interacting with the system; a stakeholder is a real party with stake.
- Static artifacts go stale within 2–6 weeks in fast-moving orgs; BABOK 3 explicitly calls stakeholder analysis a "continuous activity", not a one-time deliverable.
- Cultural blindness: the frameworks above are Anglo-American; in high-context cultures (JP, KR, parts of EU), influence flows through indirect networks the grid does not capture.

## Agentic workflow

Before any tooling, the agent must establish definitions: what does "stakeholder" mean *on this program*, which responsibility model is in force (RACI / RASCI / DACI / RAPID), which salience model overlays the engagement matrix (Mendelow vs. Mitchell-Agle-Wood). Persist these decisions as a `glossary.md` and `model-choice.md` in the program's BA folder so every later agent invocation reads the same definitions. Drive classification by *evidence*, not by title: an agent that cannot cite a quote, transcript line, or org-chart entry must return `unknown` rather than guess. Pair a discovery agent (proposes additions) with a definitions linter (rejects entries that violate the chosen model — e.g., two accountables in RACI).

### Recommended subagents

- `faion-sdd-executor-agent` — owns `TASK_define_stakeholder_glossary`, `TASK_choose_responsibility_model`, `TASK_baseline_register`, each commits a versioned artifact.
- `password-scrubber-agent` — sweeps stakeholder docs (interview notes, attitude evidence) for leaked credentials/PII before commit; stakeholder docs are the single most common leak channel.
- Custom `definitions-linter-agent` (sonnet): validates the register against the chosen model — RACI: exactly one `A` per row; RASCI: at most one `A`, multiple `S` allowed; DACI: exactly one `D`; flags violations as PR comments.
- Custom `salience-classifier-agent` (sonnet): applies Mitchell-Agle-Wood (power × legitimacy × urgency) to each stakeholder; emits one of the 8 types with citations.
- Custom `babok-mapper-agent` (sonnet): maps the register to BABOK 3 §3.2 deliverables (Stakeholder List, Map, Personas, Roles & Responsibilities) so audits can trace artifacts to standard tasks.

### Prompt pattern

Two-stage: (1) freeze definitions, (2) classify against them.

```
You are the definitions agent. Given the program charter, choose:
- responsibility_model: one of [RACI, RASCI, DACI, RAPID]
- salience_model: one of [Mendelow, Mitchell-Agle-Wood, both]
- stakeholder_definition: verbatim from BABOK 3 §3.2 OR ISO 21502 §4.4

Emit STRICT JSON:
{ "responsibility_model": "...", "salience_model": "...",
  "stakeholder_definition": "...", "rationale": "<=3 sentences",
  "rejected_alternatives": ["..."] }
Rules: no invention; cite the source clause for the definition.
```

```
You are the salience-classifier. For each stakeholder in the register,
apply Mitchell-Agle-Wood:
- power: ability to impose will (H/M/L + evidence)
- legitimacy: socially accepted claim (H/M/L + evidence)
- urgency: time-criticality of claim (H/M/L + evidence)
Emit type: dormant|discretionary|demanding|dominant|dangerous|dependent|definitive|non-stakeholder.
Rule: any axis without evidence => "unknown"; do not infer urgency from tone.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + signed tags | Freeze a definitional snapshot per release (`git tag stakeholders-v1.0`); audit-ready provenance | preinstalled |
| `cspell` / `vale` | Lint stakeholder docs against a glossary so "user" and "stakeholder" are not interchanged | https://cspell.org , https://vale.sh |
| `markdownlint` | Enforce table structure of the RACI / register tables | `npm i -g markdownlint-cli` |
| `pandoc` | Render glossary + register to PDF for sponsor / auditor sign-off | https://pandoc.org |
| `mermaid-cli` (`mmdc`) | Generate Mendelow grid + Mitchell-Agle-Wood Venn from source data | `npm i -g @mermaid-js/mermaid-cli` |
| `csvkit` / `miller` (`mlr`) | Tabular checks on RACI integrity (one `A` per row) | `pip install csvkit` ; `brew install miller` |
| `jq` / `yq` | Schema validation of register entries against the frozen model | `apt install jq yq` |

## Services & apps

| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| IIBA BABOK Online | SaaS (paid) | No public API | Authoritative source for definitions; cite by section number, not URL. |
| PMI Standards+ | SaaS (paid) | No public API | PMBOK 7e Stakeholder Performance Domain — cite for hybrid PM/BA programs. |
| ISO Online Browsing Platform | SaaS | No API | ISO 21502:2020 §4.4 stakeholder engagement; canonical for ISO-aligned programs. |
| OMG SBVR / DMN | OSS spec | N/A | Source of formal vocabulary if the program needs decision-model rigour beyond DACI. |
| Confluence | SaaS | REST API | Common host for the glossary; weak typing — pair with a structured macro. |
| Notion | SaaS | REST API | Database-backed glossary works well; enforce select fields for model enums. |
| Microsoft Graph (AAD) | SaaS | REST | Source of truth for org-chart-derived stakeholder candidates (titles, manager, group). |
| Workday HCM | SaaS | REST + RaaS | Enterprise org-chart for influence inference (level, span of control). |
| Atlassian Jira (Forge) | SaaS | REST + Forge | Custom-field-driven RACI per epic/story; agents drive via JQL. |
| StakeholderMap.com | SaaS | None public | Visual artifact only — do not treat as data store. |

## Templates & scripts

The methodology README ships Stakeholder Register, Stakeholder Profile, and a starter RACI table. The fundamentals deliverable that is missing is a **definitions-frozen** sidecar — a single file every later artifact links back to. Inline below is a 40-line bash linter that rejects RACI tables with more than one `A` per row.

```bash
#!/usr/bin/env bash
# raci-lint.sh — fail if any row has !=1 'A' (Accountable) or 0 'R'.
# Usage: raci-lint.sh path/to/raci.md
set -euo pipefail
file="${1:?path required}"
errors=0
# Extract markdown tables; assume header row contains "Activity" and role columns.
awk '
  /^\| *Activity *\|/ { in_tbl=1; print; next }
  in_tbl && /^\|[- |]+\|$/ { print; next }
  in_tbl && /^\|/ { print; next }
  in_tbl && !/^\|/ { in_tbl=0 }
' "$file" | while IFS= read -r row; do
  # skip header / separator rows
  [[ "$row" =~ Activity ]] && continue
  [[ "$row" =~ ^\|[-\ |]+\|$ ]] && continue
  # split cells, count A and R (case-sensitive single letters)
  cells=$(printf '%s' "$row" | tr '|' '\n' | sed 's/^ *//;s/ *$//')
  a_count=$(printf '%s\n' "$cells" | grep -cxE 'A')
  r_count=$(printf '%s\n' "$cells" | grep -cxE 'R')
  activity=$(printf '%s\n' "$cells" | sed -n '2p')
  if [[ "$a_count" -ne 1 ]]; then
    echo "ERR: '$activity' has $a_count A (must be 1)" >&2
    errors=$((errors+1))
  fi
  if [[ "$r_count" -lt 1 ]]; then
    echo "ERR: '$activity' has 0 R (need >=1)" >&2
    errors=$((errors+1))
  fi
done
exit $(( errors > 0 ? 1 : 0 ))
```

Wire as `pre-commit` hook on any file under `stakeholders/raci/`.

## Best practices

- Freeze definitions before classifying anyone. A `glossary.md` + `model-choice.md` in the program folder is non-negotiable; cite BABOK / ISO / PMBOK section numbers, not blog URLs.
- Use **Mendelow** for engagement cadence (which quadrant → which channel) and **Mitchell-Agle-Wood** for prioritization (definitive > dominant > dangerous > rest). They are complementary, not substitutes.
- Choose **one** responsibility model per program. RACI for steady-state ops; RASCI when "support" roles are common (data ops, infra); DACI for time-boxed decisions; RAPID for cross-functional decisions with split input/agreement.
- Enforce RACI integrity mechanically: exactly one `A` per row, ≥1 `R`, no `R+A` collapse to a single person. Lint in CI.
- Separate stakeholder, persona, and actor artifacts. A stakeholder row never becomes a persona; a persona never gets engagement cadence; an actor (UML) is a system-interaction role with no political weight.
- Salience drift is real: re-run the salience classifier when org events occur (reorg, leadership change, regulatory letter) — not on a calendar.
- Cite the BABOK 3 task you are executing (3.2 Plan Stakeholder Engagement) in the artifact header so audits trace artifact → task → standard.
- Pair power-interest with **legitimacy** check on every "high-power" classification — high power without legitimacy = a bully, not a stakeholder; the engagement strategy is escalation, not accommodation.
- Keep a `non-stakeholders` list explicitly. Documenting *exclusions* prevents repeated re-litigation ("why isn't Marketing on this?").
- Sponsor signs the register baseline. Subsequent diffs require sponsor ack only on attitude or accountability changes, not contact info.

## AI-agent gotchas

- LLMs treat "stakeholder" as a synonym for "user" / "persona" by default; they will silently merge them. Force the chosen `stakeholder_definition` into the system prompt verbatim.
- Agents over-assign `R` and `C` in RACI — every role gets something. Constrain output: max 1 `A`, max 3 `R`, justify each `C` with a one-line rationale.
- Mitchell-Agle-Wood urgency is mis-inferred from message tone. Force the agent to cite a deadline, regulatory date, or contractual SLA — not "they sounded urgent".
- Legitimacy assessment is value-laden; agents trained on Western corp norms will mark unions, works councils, and informal coalitions as "low legitimacy". Override with explicit jurisdictional context (DE works council = statutory, high legitimacy).
- BABOK section citations hallucinate readily — agents invent plausible-looking section numbers (e.g. "BABOK 3 §3.2.4"). Maintain a curated `babok-toc.md` in the repo and constrain the agent to cite only from it.
- Confusion between "Stakeholder Engagement" (BABOK 3 KA 1, task 3.2) and "Stakeholder Collaboration" (KA 2, task 4.x): they reference each other. Pin which task the artifact serves.
- Agents flatten RASCI to RACI when they hit token pressure (drop the `S` column). Detect via column-count assertion in the linter.
- Human-in-the-loop checkpoints (mandatory): freezing definitions, choosing the responsibility model, baselining the register, and any change to `A` (Accountable). Agents draft; humans approve.
- Long-context drift on glossary terms — by stakeholder #40 the agent has subtly redefined "influence". Require the agent to re-emit the definition before each batch of 10 classifications.
- Do not let agents auto-publish the register. Names + attitudes + salience scores are confidential; one Slack-bot leak ends trust.

## References

- IIBA, *BABOK Guide v3* (2015), §3.2 Plan Stakeholder Engagement; §10.43 Stakeholder List, Map, or Personas — https://www.iiba.org/standards-and-resources/babok/
- Mendelow, A. L. (1991) "Environmental Scanning — The Impact of the Stakeholder Concept", Proc. 2nd ICIS — origin of the power-interest grid.
- Mitchell, R., Agle, B., Wood, D. (1997) "Toward a Theory of Stakeholder Identification and Salience", *Academy of Management Review* 22(4) — power × legitimacy × urgency, 8 types.
- Freeman, R. E. (1984) *Strategic Management: A Stakeholder Approach* — foundational definition of "stakeholder".
- PMI, *PMBOK Guide 7e* (2021) — Stakeholder Performance Domain.
- ISO 21502:2020, §4.4 — project stakeholder engagement vocabulary.
- Smith, L. W. (2000) "Stakeholder Analysis: a Pivotal Practice of Successful Projects", PMI symposium — RACI vs. RASCI vs. DACI history.
- Sibling methodology (agentic angle): `pro/ba/business-analyst/stakeholder-analysis/agent-integration.md`.
- Related ba-core methodologies: `ba-planning/`, `elicitation-techniques/`, `requirements-prioritization/`, `ba-governance/`.
