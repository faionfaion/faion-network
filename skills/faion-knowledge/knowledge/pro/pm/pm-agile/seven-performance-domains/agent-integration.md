# Agent Integration — Seven Performance Domains (PMBOK 8)

## When to use
- Greenfield PMO design where you'd otherwise default to PMBOK 6 process groups; PMBOK 8 domains are more fit-for-purpose for hybrid delivery.
- Project audits / health checks — domains give a structured rubric (one section per domain).
- Tailoring conversations: "which domains apply to this project, with what intensity?"
- PM certification alignment (PMP exam content outline since 2023+ leans on these domains).
- Coaching new PMs to think in outcomes (Value, Stakeholders, Risk) rather than artifact production.

## When NOT to use
- Deep technical execution decisions — domains are PM-level abstractions, not engineering rubrics.
- Pure agile teams who already use Scrum + product OKRs and don't need a separate domain map.
- Teams committed to PMBOK 6 (process groups) under a regulator's mandate — switching wholesale costs more than it returns.
- Day-to-day sprint operations — domains live at portfolio / program tempo, not stand-up tempo.

## Where it fails / limitations
- Brief / generic by design — agents need concrete prompts to make outputs actionable.
- "Quality integrated everywhere" sounds nice but in practice means quality gets nobody's attention; teams must pin it to a domain owner.
- Communications absorbed into Stakeholders means comms plans get under-invested; bring them back explicitly.
- Procurement moved to appendix → vendors / contractors fall through the cracks unless an explicit owner is named.
- "Sustainability" emphasis without local metrics is greenwashing; require domain checklists with measurable items.
- Domains overlap (Resources ↔ Schedule ↔ Finance) — risk of double-counting work in dashboards.

## Agentic workflow
A health-check agent ingests a project's docs (charter, plan, risk register, status reports) and produces a per-domain RAG status (Red/Amber/Green) with evidence quotes. A planning agent generates a tailored "domain intensity" matrix per project — which domains need full treatment, which can be light. A reviewer agent checks every status report or deliverable against the domain rubric and flags gaps (e.g., "no Stakeholders section in last 4 status reports").

### Recommended subagents
- `domain-health-checker` — scores each of the 7 domains on a project corpus and outputs RAG with citations.
- `tailoring-advisor` — recommends which domains to apply heavily vs. lightly, given project type.
- `domain-rubric-linter` — verifies status reports / deliverables cover all required domains.
- `value-delivery-coach` — surfaces "output vs. outcome" misalignments (work shipped vs. value realized).

### Prompt pattern
```
You are domain-health-checker. Inputs: list of project documents (path + content).
For each of the 7 domains (Governance, Scope, Schedule, Finance, Stakeholders, Resources, Risk),
output: status (R/A/G), 2-3 evidence quotes with source path, top recommendation.
Do not invent evidence. If a domain is not addressed in the corpus, say "not addressed".
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pandoc` | Convert mixed corpus (PDF, DOCX, MD) into agent-readable text | https://pandoc.org |
| `ripgrep` (`rg`) | Fast keyword scan for domain coverage in repos | https://github.com/BurntSushi/ripgrep |
| `gh` CLI | Pull issues / discussions / project boards into one corpus | https://cli.github.com |
| `yq` | Lint a "domains.yaml" status file in CI | https://github.com/mikefarah/yq |
| `pmbox` (community) | Lightweight CLI for PMBOK templates | https://github.com/topics/pmbok |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Confluence | SaaS | Yes — REST | Status report templates per domain; agent can scaffold pages. |
| Notion | SaaS | Yes — REST | Database with one row per project, columns per domain status. |
| ServiceNow SPM | SaaS | Yes — REST | Enterprise PPM with domain-aware fields. |
| Smartsheet | SaaS | Yes — REST | Portfolio rollup with R/A/G per domain. |
| Power BI / Looker | SaaS | Yes — REST | Domain-level portfolio dashboards. |
| Asana / monday.com | SaaS | Yes — REST | Lighter-weight portfolio views; map domains to custom fields. |

## Templates & scripts
The README is the entire content (no separate templates). Inline domain checklist YAML (drop in `templates/domains.yaml`):

```yaml
domains:
  governance: { status: G, owner: pm,        evidence: charter.md#authority }
  scope:      { status: A, owner: po,        evidence: spec.md, gap: "AC missing for 3 stories" }
  schedule:   { status: G, owner: pm,        evidence: roadmap.md }
  finance:    { status: A, owner: sponsor,   evidence: budget.xlsx, gap: "Q3 forecast stale" }
  stakeholders:{ status: G, owner: pm,       evidence: stakeholder-register.md }
  resources:  { status: R, owner: line_mgr,  evidence: capacity.md, gap: "1 senior eng departed" }
  risk:       { status: G, owner: pm,        evidence: risk-register.md }
value_delivery:
  outputs_shipped: 12
  outcomes_realized: 7
  value_realization_rate: 0.58
sustainability_metrics:
  - co2_per_user_session_kg: 0.012
  - inclusive_a11y_score: AA
```

## Best practices
- Force every status report to have a section per domain — even one line each. Missing sections become the early warning.
- Pair "Value Delivery" tracking with shipped output tracking; a 100% delivery rate with 30% value rate is the most common trap.
- When tailoring, drop a domain with deliberate documentation; never silently. "We're not tracking Finance because budget is fixed annual" is fine; ignoring it is not.
- Run a "domain owner" RACI: each of the 7 domains has one accountable person, even if the same person owns multiple.
- For agile/hybrid programs, map ceremonies → domains (PI Planning → Schedule + Resources, Demos → Stakeholders + Value).
- Re-score domain RAG monthly minimum; the value of the framework is the trend line, not the snapshot.

## AI-agent gotchas
- Agents over-classify everything as Green if not given calibration examples; provide one explicit Red exemplar in the prompt.
- "Quality" mentions tend to scatter across all 7 domains, making it invisible — explicitly ask the agent to surface quality-related findings as a cross-cutting section.
- Sustainability gets hand-waved; require numeric metrics or "not applicable, justification: ..." with a reason.
- LLMs invent PMBOK 7 vocabulary in PMBOK 8 contexts (and vice versa); pin the version in system prompt.
- Stakeholder domain tempts agents into people-name name-dropping without consent — anonymize roles in shared outputs.
- Long corpora cause domain conflation; chunk by domain (one inference per domain) for higher signal.

## References
- PMI PMBOK Guide, 8th edition (2025) — Performance Domains
- PMI Standard for Project Management, 2nd edition
- https://www.pmi.org/pmbok-guide-standards
- https://www.pmi.org/disciplined-agile — adjacent frame for tailoring
- https://www.scrum.org/resources/blog/scrum-and-pmbok — overlap/conflict mapping
