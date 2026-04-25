# Agent Integration — Stakeholder Engagement (PM)

## When to use
- Project kickoff for any cross-functional initiative with >5 named parties (sponsor, end users, regulators, vendors) — engagement plan must precede planning.
- Programs where political risk is significant: M&A integration, reorgs, vendor consolidation, regulated rollouts.
- Multi-stakeholder transformation programs (cloud migration, ERP, M365 / Workday) with sponsors, champions, blockers, and external auditors.
- Public-facing programs (government, NGO, infrastructure) with citizen / community stakeholders that exceed normal corporate scope.
- Pre-RFP / vendor-selection efforts where the buying committee has hidden influencers (security, procurement, legal).
- Pairing with `communications-management/` (executable form of the engagement plan), `stakeholder-register/`, `stakeholder-engagement-advanced/`, `change-control/`, `risk-register/`, and BA `stakeholder-analysis/`.

## When NOT to use
- Solo founders / very small teams (<5 stakeholders) — direct conversation beats matrix overhead.
- One-off internal hotfixes / refactors with no business stakeholder change — RACI alone is enough.
- Anonymous open-source community projects — power/interest axes are meaningless without identity; use governance patterns instead.
- Crisis / incident response — incident command structure replaces engagement plan; do not retrofit during P0.
- When stakeholder identification is the unsolved problem — do `business-analyst/stakeholder-analysis/` first to get a register, then engagement.

## Where it fails / limitations
- Power/Interest 2x2 flattens multi-dimensional politics (urgency, legitimacy, salience). Mitchell-Agle-Wood overlay is needed for serious political risk.
- Static analysis goes stale fast (2–6 weeks in dynamic orgs); a register that is not refreshed is wrong, not just old.
- Self-reported attitude is unreliable — people say "supportive" in workshops and undermine in private. Triangulate against behaviour.
- Hidden stakeholders (works councils, security, procurement, downstream consumers) are systematically missed unless seeded with org-chart context.
- LLMs invent plausible-sounding personas that do not exist in the target organisation; outputs must validate against directory data.
- Cross-cultural blindness: high-context cultures (JP, KR, parts of EU/MEA) route influence through indirect networks the matrix does not represent.
- Engagement strategies that treat all "Manage Closely" stakeholders the same fail — a CFO and a regulator demand opposite tone, cadence, and content.
- Stakeholder fatigue: well-meant high-touch engagement burns goodwill if asks exceed the recipient's tolerance.

## Agentic workflow
Treat the stakeholder register and engagement plan as one structured artifact in git: `stakeholders/register.yaml` (one entry per stakeholder with influence/impact/attitude/quadrant/strategy/cadence/owner/last_engaged) plus a generated `engagement-plan.md`. A subagent maintains the register, proposes patches when new evidence arrives (kickoff transcripts, calendar invites, Slack sentiment), and emits a weekly engagement digest. The engagement plan never auto-sends to executives; it drafts, humans deliver. Pair with `communications-management/plan.yaml` so cadence in one is reflected in the other.

### Recommended subagents
- `faion-sdd-executor-agent` — drives engagement as SDD tasks: TASK_register_baseline, TASK_engagement_plan, TASK_cadence_setup, TASK_quarterly_refresh.
- A custom `register-curator-agent` (model: sonnet per README "Analyze and assess"): ingests org chart, kickoff transcripts, RFP, contract; emits patch with new/changed entries; never overwrites.
- A custom `attitude-triangulator-agent` (model: sonnet): cross-references self-reported attitude against meeting attendance, Slack/email sentiment, response time, escalations; flags drift between stated and observed.
- A custom `engagement-planner-agent` (model: sonnet): converts register quadrants into a Step-5 engagement table (cadence, channel, owner, content) with override rationale required for non-default cadence.
- A custom `salience-scorer-agent` (model: opus per README "Strategic decision"): applies Mitchell-Agle-Wood (power × legitimacy × urgency) on top of the matrix; identifies "definitive" stakeholders requiring daily attention.
- A custom `engagement-sentiment-agent` (model: sonnet): listens to feedback channels (Slack, email, NPS) and updates `attitude` column with evidence trail.
- `password-scrubber-agent` — runs over engagement docs before commit; the register frequently leaks salaries, customer names, candid commentary.

### Prompt pattern
Two stages: discovery → classification → engagement strategy.

```
You are the register-curator agent. Inputs:
1. Kickoff transcript / charter / RFP.
2. Org-chart export (names, titles, reporting lines).
3. Existing register (may be empty).

For each named or implied party, emit STRICT JSON patch:
{ "action": "add|update",
  "id": "S-NN",
  "name": "...",
  "category": "Sponsor|User|Customer|Team|Regulator|Supplier|Influencer",
  "power": "H|M|L",
  "interest": "H|M|L",
  "attitude": "+|0|-|unknown",
  "quadrant": "Manage Closely|Keep Satisfied|Keep Informed|Monitor",
  "evidence": ["quote or org-chart line"],
  "cadence": "daily|weekly|biweekly|monthly|quarterly|release",
  "channel": "1:1|email|digest|meeting|portal",
  "owner": "<role>",
  "rationale": "<= 2 sentences" }

Rules: do not invent people. attitude defaults to "unknown" without evidence.
quadrant must follow power x interest unless override rationale provided.
Flag hidden stakeholders (legal, infosec, works council, procurement,
downstream consumers) in suggested_to_verify.
```

Engagement plan prompt: `Render Step-5 engagement table from the register. Default cadence: HH=Manage Closely (weekly 1:1), HL=Keep Satisfied (biweekly summary), LH=Keep Informed (monthly digest), LL=Monitor (release notes). Override only with explicit rationale.`

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + `git log -- stakeholders/` | Native history of relationship changes; replaces hand-rolled engagement history | preinstalled |
| `yq` | Read/patch register YAML in pipelines | `apt install yq` / `brew install yq` |
| `jq` | Aggregate JSON exports from CRM/HR systems | `apt install jq` |
| `graphviz` (`dot`) | Render influence/impact graph + relationship network | `apt install graphviz` |
| `mermaid-cli` (`mmdc`) | Generate the 2x2 quadrant chart from YAML as PNG/SVG | `npm i -g @mermaid-js/mermaid-cli` |
| `pandoc` | Convert register and engagement plan to PDF/DOCX for sponsor review | https://pandoc.org |
| `pre-commit` | Block commits to attitude/quadrant changes without `evidence:` | https://pre-commit.com |
| `csvkit` | Slice exported register CSVs (from Jira/Confluence) for offline analysis | `pip install csvkit` |
| `gh` / `glab` | Mirror engagement actions as issues; CODEOWNERS gates sponsor sign-off on register changes | https://cli.github.com / https://gitlab.com/gitlab-org/cli |
| `op` (1Password CLI) | Pull sensitive contact info into the register without committing it | https://developer.1password.com/docs/cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Microsoft Graph (Entra ID) | SaaS | REST/Graph | Source of truth for internal org chart, reporting lines, group membership; required to seed register without inventing. |
| Workday HCM / Personio / BambooHR | SaaS | REST | Authoritative for level, span of control, manager — useful for influence inference. |
| Salesforce | SaaS | REST + Bulk API | Authoritative for external (customer) stakeholders. |
| HubSpot | SaaS | REST | Lighter SMB CRM; webhooks drive attitude triggers. |
| Notion / Confluence | SaaS | REST | Common register host; weak typing — schema-validate before commit. |
| Jira / Linear | SaaS | REST/GraphQL | Stakeholder = issue with custom fields (less ideal but common). |
| Smaply / UXPressia | SaaS | Limited API | Persona/journey tools; visual artifact, weak agent automation. |
| StakeholderMap.com / SmartDraw / Lucidchart | SaaS | Export-only | Treat as artifact target, not agent target. |
| Polarion / Jama | SaaS / on-prem | REST/OSLC | Enterprise RM with stakeholder modules; over-kill outside regulated domains. |
| Mural / Miro / FigJam | SaaS | REST | Workshop canvas for matrix exercises; agents can post sticky notes via API. |
| Slack / MS Teams | SaaS | REST + Events | Source for behavioural signal; use with consent. |
| SurveyMonkey / Typeform / Qualtrics | SaaS | REST | Periodic stakeholder pulse surveys feeding attitude triangulation. |
| Calendly / SavvyCal | SaaS | REST | Meeting load monitor for high-touch stakeholders (avoid burnout). |

## Templates & scripts
The README provides Stakeholder Register, Engagement Health Check, and matrix walkthrough. Inline below: a script that reads `stakeholders/register.yaml` and lists stakeholders overdue for engagement.

```python
#!/usr/bin/env python3
"""engagement_due.py — flag stakeholders past their engagement cadence."""
from __future__ import annotations
import datetime as dt
import pathlib
import sys
import yaml

CADENCE_DAYS = {
    "daily": 1, "weekly": 7, "biweekly": 14,
    "monthly": 30, "quarterly": 90, "release": 60,
}

def main(path: str = "stakeholders/register.yaml") -> int:
    data = yaml.safe_load(pathlib.Path(path).read_text())
    today = dt.date.today()
    due: list[str] = []
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
    if due:
        sys.stdout.write("\n".join(due) + "\n")
        return 1
    sys.stdout.write("All engagements current.\n")
    return 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```

Run weekly via cron / GitHub Actions; failure opens an engagement-debt issue assigned to the PM.

## Best practices
- Store the register in git (YAML), not a wiki — diffs become engagement history; CODEOWNERS gate sponsor sign-off on attitude changes.
- Require an `evidence:` field on every attitude assertion (quote, transcript line, ticket link). No evidence → `attitude: unknown`.
- Refresh quarterly minimum, monthly for volatile contexts (post-merger, leadership change, regulator activity).
- Triangulate self-reported attitude with at least one behavioural signal (attendance, Slack sentiment, response time, escalations).
- Apply the Mitchell-Agle-Wood salience overlay for political risk — flag "definitive" (power × legitimacy × urgency) stakeholders for daily attention.
- Tie cadence to quadrant by default: Manage Closely = weekly, Keep Satisfied = biweekly, Keep Informed = monthly, Monitor = release-only. Override only with rationale.
- One canonical register. If Workday or Salesforce holds source data, mirror nightly into the register; do not maintain two truths.
- Always include a "hidden stakeholders" review: legal, infosec, procurement, works council/union, accessibility, downstream API consumers.
- Treat the register as confidential — `password-scrubber-agent` plus a private repo, not a wiki page.
- Pair stakeholder weight with `requirements-prioritization` so high-influence support amplifies a requirement's score.
- Engagement plan is a living document with explicit ownership per stakeholder; rotate owners only on transition.
- Calendar audits prevent burnout — if any stakeholder appears in >3 weekly meetings, consolidate.

## AI-agent gotchas
- Agents invent people. Always seed with a real org chart export and reject any name not in the source list unless flagged `suggested_to_verify`.
- LLMs over-classify everyone as "supportive" by default — politeness bias. Force a 4-way enum (`+/0/-/unknown`) with `unknown` default and require evidence for `+/-`.
- Stakeholder data is regulated PII (GDPR Art. 9 if attitude implies political opinion or health). Never send the register to a third-party model without DPA; prefer self-hosted or zero-retention Anthropic.
- Bulk reclassification is dangerous — cap agent edits to N stakeholders per run (e.g., 5) and require human review on the diff.
- Stakeholder vs. persona conflation: stakeholder = real named human/role with decision power; persona = synthesized archetype. Keep them in separate files.
- Influence ≠ seniority. A CFO's EA may have more influence on calendar decisions than the CFO. Force the agent to consider gatekeepers, not just titles.
- Auto-send is forbidden to executives, regulators, customers, board. Agent drafts; sponsor or PM approves and sends.
- Long-context drift: registers >50 stakeholders blow context. Page by category (Internal/External/Regulator) and operate on slices.
- Cross-cultural miscoding: agents trained on Western norms misread consensus cultures. Add a `cultural_context` system prompt for international initiatives.
- Sentiment-from-Slack is inherently lossy and easily misclassified; never act on a single message.
- Calendar privacy: pulling executive calendars to detect engagement load requires explicit consent in many jurisdictions.
- Human-in-the-loop checkpoints (mandatory): adding a stakeholder, changing attitude, escalating to sponsor, dropping a stakeholder from active engagement.
- Avoid "satisfaction theatre" — agents schedule extra meetings to look engaged; this burns trust faster than under-engagement.

## References
- PMI PMBOK 7e — Stakeholder Performance Domain.
- PMI PMBOK 6e — Stakeholder Management Knowledge Area (still useful for templates and processes).
- Mendelow, A. (1991) — Power-Interest grid (the matrix this methodology uses).
- Mitchell, Agle & Wood (1997) "Toward a Theory of Stakeholder Identification and Salience" — Academy of Management Review.
- Freeman, R. E. "Strategic Management: A Stakeholder Approach" — foundational text.
- Bourne, L. "Stakeholder Relationship Management" — practitioner guidance, including the Stakeholder Circle methodology.
- ISO 21500 / 21502 — project management stakeholder engagement guidance.
- Maister, Green & Galford "The Trusted Advisor" — relationship dynamics with senior stakeholders.
- Sibling methodologies: `communications-management/`, `stakeholder-register/`, `stakeholder-engagement-advanced/`, `change-control/`, BA `stakeholder-analysis/`, `requirements-prioritization/`.
