# Agent Integration — Stakeholder Engagement (PMBoK)

## When to use
- Project kickoff for any cross-functional initiative with >5 named parties (sponsor, end users, regulators, vendors); engagement plan precedes detailed planning.
- Programs with high political risk: M&A integration, reorgs, vendor consolidation, regulated rollouts (HIPAA, SOX, GDPR, MiFID).
- Public-sector and infrastructure programs with citizen / community / NGO stakeholders outside the corporate boundary.
- Pre-RFP / vendor selection where the buying committee has hidden influencers (security, procurement, legal, FinOps).
- Multi-stakeholder transformation programs (cloud migration, ERP, M365 / Workday, SAP S/4) with sponsors, champions, blockers, and external auditors.
- Pair with `stakeholder-register/`, `stakeholder-engagement-advanced/`, `communications-management/`, `change-control/`, and BA `stakeholder-analysis/`.

## When NOT to use
- Solo founders or teams under 5 stakeholders — direct conversation beats matrix overhead.
- One-off internal hotfixes or refactors with no business stakeholder change — RACI is enough.
- Anonymous open-source community projects — power/interest axes are meaningless without identity.
- Crisis / incident response — incident command structure replaces engagement plan; do not retrofit during a P0.
- When stakeholder identification is the unsolved problem — run BA `stakeholder-analysis/` first to populate the register.

## Where it fails / limitations
- The 2x2 Power/Interest grid (Mendelow) flattens multi-dimensional politics; Mitchell-Agle-Wood salience overlay is needed for high-stakes programs.
- Static analysis goes stale fast — 2 to 6 weeks in dynamic orgs; an unrefreshed register is wrong, not just old.
- Self-reported attitude is unreliable; people say "supportive" in workshops and undermine in private. Triangulate against behaviour.
- Hidden stakeholders (works councils, security, procurement, downstream consumers, FinOps, accessibility) are systematically missed without org-chart seeding.
- LLMs invent plausible-sounding personas; outputs must validate against directory data.
- Cross-cultural blindness — high-context cultures (JP, KR, parts of EU/MEA) route influence through indirect networks the matrix does not represent.
- "Manage Closely" is not one strategy — a CFO and a regulator demand opposite tone, cadence, and content; uniform handling fails both.
- Stakeholder fatigue — well-meant high-touch engagement burns goodwill if asks exceed tolerance.

## Agentic workflow
Treat the engagement plan as a structured artifact in git: `stakeholders/register.yaml` (one entry per stakeholder with influence, impact, attitude, quadrant, strategy, cadence, owner, last_engaged, evidence) plus a generated `engagement-plan.md`. A subagent maintains the register, proposes patches when new evidence arrives (kickoff transcripts, calendar invites, Slack signals, NPS surveys), and emits a weekly engagement digest. The plan never auto-sends to executives — agents draft, humans deliver. Pair with `communications-management/plan.yaml` so cadence in one is reflected in the other.

### Recommended subagents
- `faion-sdd-executor-agent` — drives engagement as SDD tasks: TASK_register_baseline, TASK_engagement_plan, TASK_cadence_setup, TASK_quarterly_refresh.
- Custom `register-curator-agent` (sonnet) — ingests org chart, kickoff transcripts, RFP, contract; emits patches; never overwrites.
- Custom `attitude-triangulator-agent` (sonnet) — cross-references self-reported attitude against meeting attendance, response time, escalation count.
- Custom `engagement-planner-agent` (sonnet) — converts register quadrants into Step-5 engagement table (cadence, channel, owner, content) with override rationale required for non-default cadence.
- Custom `salience-scorer-agent` (opus) — applies Mitchell-Agle-Wood (power x legitimacy x urgency) on top of the matrix; identifies "definitive" stakeholders requiring daily attention.
- `password-scrubber-agent` — runs over engagement docs before commit; the register frequently leaks salaries, candid commentary, customer names.

### Prompt pattern
Two-stage discovery → classification → engagement strategy.

```
You are register-curator. Inputs: kickoff transcript, org-chart export, existing register.
For each named or implied party, emit STRICT JSON patch:
{ "action": "add|update", "id": "S-NN", "name": "...",
  "category": "Sponsor|User|Customer|Team|Regulator|Supplier|Influencer",
  "power": "H|M|L", "interest": "H|M|L",
  "attitude": "+|0|-|unknown",
  "quadrant": "Manage Closely|Keep Satisfied|Keep Informed|Monitor",
  "evidence": ["quote or org-chart line"],
  "cadence": "daily|weekly|biweekly|monthly|quarterly|release",
  "channel": "1:1|email|digest|meeting|portal",
  "owner": "<role>", "rationale": "<= 2 sentences" }
Rules: never invent people. attitude defaults to "unknown" without evidence.
```

Engagement plan prompt: `Render Step-5 table from register. Default cadence: HH=Manage Closely (weekly 1:1), HL=Keep Satisfied (biweekly summary), LH=Keep Informed (monthly digest), LL=Monitor (release notes). Override only with explicit rationale.`

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + `git log -- stakeholders/` | Native history of relationship changes | preinstalled |
| `yq` | Read/patch register YAML in pipelines | `apt install yq` / `brew install yq` |
| `jq` | Aggregate JSON exports from CRM/HR systems | `apt install jq` |
| `graphviz` (`dot`) | Render influence/impact graph + relationship network | `apt install graphviz` |
| `mermaid-cli` (`mmdc`) | Generate the 2x2 quadrant chart from YAML | `npm i -g @mermaid-js/mermaid-cli` |
| `pandoc` | Convert plan to PDF/DOCX for sponsor review | https://pandoc.org |
| `pre-commit` | Block attitude/quadrant changes without `evidence:` | https://pre-commit.com |
| `gh` / `glab` | Mirror engagement actions as issues; CODEOWNERS gates sponsor sign-off | https://cli.github.com |
| `op` (1Password CLI) | Pull sensitive contact info into the register without committing it | https://developer.1password.com/docs/cli |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Microsoft Graph (Entra ID) | SaaS | REST/Graph | Source of truth for internal org chart, reporting lines, group membership; required to seed register without inventing. |
| Workday HCM / Personio / BambooHR | SaaS | REST | Authoritative for level, span of control, manager — useful for influence inference. |
| Salesforce | SaaS | REST + Bulk API | Authoritative for external (customer) stakeholders. |
| HubSpot | SaaS | REST | Lighter SMB CRM; webhooks drive attitude triggers. |
| Notion / Confluence | SaaS | REST | Common register host; weak typing — schema-validate before commit. |
| Jira / Linear | SaaS | REST/GraphQL | Stakeholder = issue with custom fields (less ideal but common). |
| Smaply / UXPressia | SaaS | Limited API | Persona/journey tools; visual artifact only. |
| StakeholderMap.com / Lucidchart / SmartDraw | SaaS | Export-only | Treat as artifact target, not agent target. |
| Mural / Miro / FigJam | SaaS | REST | Workshop canvas for matrix exercises; agents can post sticky notes via API. |
| Slack / MS Teams | SaaS | REST + Events | Source for behavioural signal; use with consent. |
| Qualtrics / Typeform / SurveyMonkey | SaaS | REST | Periodic stakeholder pulse surveys feeding attitude triangulation. |

## Templates & scripts
The README provides Stakeholder Register and Engagement Health Check. Inline below: a 25-line script that reads `stakeholders/register.yaml` and lists stakeholders overdue for engagement.

```python
#!/usr/bin/env python3
"""engagement_due.py — flag stakeholders past their engagement cadence."""
import datetime as dt, pathlib, sys, yaml

CADENCE_DAYS = {"daily": 1, "weekly": 7, "biweekly": 14,
                "monthly": 30, "quarterly": 90, "release": 60}

def main(path: str = "stakeholders/register.yaml") -> int:
    data = yaml.safe_load(pathlib.Path(path).read_text())
    today, due = dt.date.today(), []
    for s in data.get("stakeholders", []):
        cadence = s.get("cadence", "monthly")
        last = s.get("last_engaged")
        max_gap = CADENCE_DAYS.get(cadence, 30)
        if last is None:
            due.append(f"{s['id']} {s['name']:<25} never engaged ({cadence})")
            continue
        gap = (today - dt.date.fromisoformat(str(last))).days
        if gap > max_gap:
            due.append(f"{s['id']} {s['name']:<25} {gap}d > {max_gap}d ({cadence})")
    sys.stdout.write("\n".join(due) + "\n" if due else "All current.\n")
    return 1 if due else 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```

## Best practices
- Store the register in git (YAML), not a wiki — diffs become engagement history; CODEOWNERS gate sponsor sign-off on attitude changes.
- Require an `evidence:` field on every attitude assertion (quote, transcript line, ticket link). No evidence → `attitude: unknown`.
- Refresh quarterly minimum, monthly for volatile contexts (post-merger, leadership change, regulator activity).
- Triangulate self-reported attitude with at least one behavioural signal (attendance, sentiment, response time, escalations).
- Apply the Mitchell-Agle-Wood salience overlay for political risk — flag "definitive" stakeholders for daily attention.
- Tie cadence to quadrant by default; override only with explicit rationale.
- One canonical register — if Workday or Salesforce holds source data, mirror nightly; do not maintain two truths.
- Always run a "hidden stakeholders" review (legal, infosec, procurement, works council/union, accessibility, downstream consumers).
- Calendar audits prevent burnout — if any stakeholder appears in >3 weekly meetings, consolidate.

## AI-agent gotchas
- Agents invent people; seed with a real org chart export and reject any name not in the source list unless flagged `suggested_to_verify`.
- LLMs over-classify everyone as "supportive" by default (politeness bias). Force a 4-way enum (`+/0/-/unknown`) with `unknown` default.
- Stakeholder data is regulated PII (GDPR Art. 9 if attitude implies political opinion or health). Never send the register to a third-party model without DPA.
- Bulk reclassification is dangerous — cap agent edits to N stakeholders per run (e.g., 5) and require human review on the diff.
- Stakeholder vs. persona conflation: stakeholder = real named human/role with decision power; persona = synthesized archetype. Separate files.
- Influence ≠ seniority. A CFO's EA may have more influence on calendar decisions than the CFO; force the agent to consider gatekeepers.
- Auto-send is forbidden to executives, regulators, customers, and board. Agent drafts; PM or sponsor approves.
- Sentiment from Slack is lossy and easily misclassified; never act on a single message.
- Cross-cultural miscoding — agents trained on Western norms misread consensus cultures. Add a `cultural_context` system prompt for international initiatives.
- Human-in-the-loop checkpoints (mandatory): adding a stakeholder, changing attitude, escalating to sponsor, dropping a stakeholder from active engagement.

## References
- PMI PMBOK 7e — Stakeholder Performance Domain.
- PMI PMBOK 6e — Stakeholder Management Knowledge Area (templates and processes).
- Mendelow, A. (1991) — Power-Interest grid (the matrix this methodology uses).
- Mitchell, Agle & Wood (1997) "Toward a Theory of Stakeholder Identification and Salience" — Academy of Management Review.
- Freeman, R. E. — "Strategic Management: A Stakeholder Approach".
- Bourne, L. — "Stakeholder Relationship Management" (Stakeholder Circle methodology).
- ISO 21500 / 21502 — project management stakeholder engagement guidance.
- Sibling methodologies: `stakeholder-register/`, `stakeholder-engagement-advanced/`, `communications-management/`, `change-control/`, BA `stakeholder-analysis/`.
