# Agent Integration — Stakeholder Analysis

## When to use

- Kickoff of any cross-functional initiative where >5 named parties touch the change (sponsor, SMEs, end users, regulator, vendor) and you need to decide whom to interview first.
- Migration / replacement projects where end-user resistance is the dominant risk and you need to map influence vs. impact before scoping.
- Regulated programs (HIPAA, GDPR, SOX, MDR) — the regulator is a stakeholder and missing them in Step 1 invalidates downstream artifacts.
- M&A and reorg work where the political map is unstable; rerun the matrix every 2–4 weeks.
- Pairing with `elicitation-techniques/` to drive interview ordering, with `requirements-prioritization/` to weight requirement scores by stakeholder influence, and with `business-process-analysis/` to find process owners.
- Pre-RFP / vendor-selection work where the buying committee has hidden influencers (security, procurement, legal).

## When NOT to use

- Solo founder pre-PMF with <3 people involved — overhead exceeds value; skip to direct customer interviews via `continuous-discovery`.
- Strictly internal engineering refactors with no business stakeholder change — `RACI` alone is enough.
- Public open-source projects with anonymous community contributors — the influence/impact axis is meaningless when identity is unknown; use `governance` patterns instead.
- One-off bug fixes or hotfixes — stakeholder map will be stale before the deploy completes.

## Where it fails / limitations

- The 2x2 influence/impact matrix flattens multi-dimensional politics — power, urgency, and legitimacy (Mitchell-Agle-Wood salience) are collapsed into one axis and important nuance is lost.
- Stakeholder lists drift fast (2–6 weeks in fast-moving orgs); a static register goes stale and becomes wrong, not just old. README mistake #5 is the dominant real-world failure.
- Hidden stakeholders (works councils, legal, infosec, procurement, downstream consumers of an API) are systematically missed — agents will not invent them unless given org-chart context.
- Self-reported attitude is unreliable — people say "supportive" in workshops and undermine in private. The matrix only works if attitude is triangulated against behaviour.
- LLM hallucinates plausible-sounding personas ("VP of Product Excellence") that do not exist in the target org; outputs must be validated against an actual directory / org chart.
- Cultures vary: in high-context cultures (JP, KR) influence flows through indirect networks the matrix does not represent.

## Agentic workflow

Treat the stakeholder register as a single YAML/Markdown file (`stakeholders/register.yaml`) with one entry per stakeholder containing influence (H/M/L), impact (H/M/L), attitude (+/0/-), category, engagement_strategy, last_updated. A subagent ingests an org chart, kickoff transcript, or RFP and proposes additions/changes as a structured patch — never overwrites the register directly. Each transition (added, attitude shift, escalated) is committed with a one-line rationale so `git log -- stakeholders/` becomes the relationship history. Pair the register with the matrix as a generated artifact (`make stakeholder-matrix`) so the picture is always rebuilt from source.

### Recommended subagents

- `faion-sdd-executor-agent` — drives stakeholder analysis as an SDD task: TASK_stakeholder_register, TASK_engagement_plan, TASK_matrix_refresh. Each emits a commit + execution report.
- `password-scrubber-agent` — runs over interview notes / transcripts before commit, since stakeholder docs are the single most common place secrets leak (pasted credentials, internal URLs, salary data).
- A custom `stakeholder-discovery-agent` (model: sonnet, per README Agent Selection table): owns Step 1 — ingests org chart + kickoff transcript, emits candidate list with category and rationale.
- A custom `stakeholder-attitude-agent` (model: sonnet): triangulates self-reported attitude against transcripts/Slack/emails, flags drift between stated and observed support.
- A custom `engagement-planner-agent` (model: sonnet): turns the matrix into a per-stakeholder engagement plan (cadence, channel, owner) — output is the table in Step 5 of README.
- A custom `conflict-mediator-agent` (model: opus): activated when two stakeholders' needs collide; produces position summary, common ground, trade-offs, escalation recommendation per README "Stakeholder Conflicts".

### Prompt pattern

Two-stage: discovery → classification.

```
You are the stakeholder-discovery agent. Inputs:
1. Org chart snippet (names, titles, reporting lines).
2. Kickoff transcript / charter.
3. Existing register (may be empty).

For each named or implied party, emit STRICT JSON:
{ "id": "S-NN", "name": "...", "role": "...", "category": "Customer|EndUser|Sponsor|DomainSME|ImplementationSME|Tester|Regulator|Supplier",
  "influence": "H|M|L", "impact": "H|M|L", "attitude": "+|0|-|unknown",
  "evidence": ["quote or org-chart line"], "engagement": "Manage Closely|Keep Satisfied|Keep Informed|Monitor",
  "rationale": "<=2 sentences" }

Rules: do not invent people. If attitude is not directly evidenced, return "unknown".
Flag potential hidden stakeholders (legal, infosec, works council, procurement,
downstream API consumers) in a separate `suggested_to_verify` list.
```

Engagement-plan prompt: `Given the register below, produce the Step-5 engagement table.
Quadrant mapping: HH=Manage Closely (weekly 1:1), HL=Keep Satisfied (biweekly summary), LH=Keep Informed (monthly digest), LL=Monitor (release notes only). Override only with explicit rationale.`

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + `git log -- stakeholders/` | Native history of relationship changes; replaces hand-rolled "Engagement History" table | preinstalled |
| `yq` | Read/update register YAML in pipelines (`yq '.stakeholders[] \| select(.influence=="H")'`) | `brew install yq` / `apt install yq` |
| `jq` | Aggregate JSON exports from CRMs into the register schema | `apt install jq` |
| `graphviz` (`dot`) | Render the influence/impact matrix and relationship graph from YAML | `apt install graphviz` |
| `mermaid-cli` (`mmdc`) | Generate the 2x2 matrix as PNG/SVG from a Mermaid quadrant chart | `npm i -g @mermaid-js/mermaid-cli` |
| `pandoc` | Convert the register to per-stakeholder profile PDFs for sponsor review | https://pandoc.org |
| `gh issue` / `gh pr` + CODEOWNERS | Mirror engagement actions as issues; require sponsor approval for register changes | https://cli.github.com |
| `pre-commit` | Block commits where attitude was changed without an `evidence:` field | https://pre-commit.com |
| `csvkit` | Slice exported register CSVs (from Jira/Confluence) for offline analysis | `pip install csvkit` |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Salesforce | SaaS | REST + Bulk API | Authoritative for external (customer) stakeholders; agents drive via `sf data` CLI. |
| HubSpot | SaaS | REST API | Lighter-weight CRM for SMB; good webhooks for attitude-change triggers. |
| Microsoft Graph (AAD) | SaaS | REST/Graph API | Source of truth for internal org chart, reporting lines, group membership. Use for hidden-stakeholder discovery. |
| Workday HCM | SaaS | REST + RaaS | Enterprise org-chart source; useful for influence inference (span of control, level). |
| BambooHR / Personio | SaaS | REST API | SMB org-chart sources; simpler than Workday. |
| Notion | SaaS | REST API | Common register host; weak typing on enums (attitude, influence) — validate via schema. |
| Confluence | SaaS | REST API | Free-text drift is high; pair with a structured macro or custom property. |
| Jira | SaaS | REST v3 + JQL | Stakeholder = issue with custom fields; workflow can model attitude transitions. |
| Linear | SaaS | GraphQL | Lightweight; one issue per stakeholder, labels for category, custom field for influence. |
| Smaply / UXPressia | SaaS | Limited API | Persona/journey tools — good for visual artifact, weak for agent automation. |
| StakeholderMap.com | SaaS | None public | Visual matrix tool; export-only — treat as artifact target, not agent target. |
| Polarion / Jama | SaaS/on-prem | REST/OSLC | Enterprise RM with built-in stakeholder modules; over-kill outside regulated domains. |
| Mural / Miro | SaaS | REST API | Collaborative matrix workshop canvas; agents post sticky notes via API. |
| Slack / MS Teams | SaaS | REST + Events API | Source for attitude triangulation — sentiment in stakeholder DMs/threads. |

## Templates & scripts

The README already provides Stakeholder Register, Stakeholder Profile, and RACI templates. Inline below is a Python script that validates a YAML register, computes the quadrant for each stakeholder, and emits a Mermaid quadrant chart.

```python
#!/usr/bin/env python3
"""stakeholder_matrix.py — validate register and emit Mermaid quadrant chart."""
from __future__ import annotations
import sys, pathlib, yaml

LEVELS = {"H": 0.85, "M": 0.55, "L": 0.20}
QUADRANT = {
    ("H","H"): "Manage Closely",
    ("H","L"): "Keep Satisfied",
    ("L","H"): "Keep Informed",
    ("L","L"): "Monitor",
}

def quad(infl: str, impact: str) -> str:
    i = "H" if infl == "H" else "L"
    p = "H" if impact == "H" else "L"
    return QUADRANT[(i, p)]

def main(path: str = "stakeholders/register.yaml") -> int:
    data = yaml.safe_load(pathlib.Path(path).read_text())
    errors: list[str] = []
    print("quadrantChart")
    print("    title Influence vs Impact")
    print("    x-axis Low Impact --> High Impact")
    print("    y-axis Low Influence --> High Influence")
    print("    quadrant-1 Manage Closely")
    print("    quadrant-2 Keep Satisfied")
    print("    quadrant-3 Monitor")
    print("    quadrant-4 Keep Informed")
    for s in data.get("stakeholders", []):
        infl, imp = s.get("influence"), s.get("impact")
        if infl not in LEVELS or imp not in LEVELS:
            errors.append(f"{s.get('id')}: bad influence/impact {infl}/{imp}")
            continue
        x, y = LEVELS[imp], LEVELS[infl]
        label = f"{s['id']} {s['name']}"
        print(f'    "{label}": [{x:.2f}, {y:.2f}]')
        s["quadrant"] = quad(infl, imp)
    if errors:
        print("\nERRORS:", *errors, sep="\n", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```

Wire it into `pre-commit` or a `make stakeholder-matrix` target so the chart is rebuilt on every register change.

## Best practices

- Store the register as YAML in git, not in a wiki — diffs become the engagement history, `git blame` shows who reclassified whom, and CODEOWNERS gates sponsor sign-off on attitude changes.
- Require an `evidence:` field on every attitude assertion (quote, transcript line, ticket link). No evidence → attitude is `unknown`, not `0`.
- Refresh quarterly at minimum, monthly for volatile orgs (post-merger, leadership change). Set a calendar trigger that opens an issue assigned to the BA.
- Triangulate self-reported attitude with at least one behavioural signal (meeting attendance, Slack sentiment, response time, sponsor escalations).
- Apply the Mitchell-Agle-Wood salience overlay (power × legitimacy × urgency) on top of the influence/impact matrix when politics matter — flag "definitive" stakeholders (all three) for daily attention.
- Tie engagement cadence to quadrant by default: Manage Closely = weekly, Keep Satisfied = biweekly, Keep Informed = monthly, Monitor = release-only. Override only with rationale.
- One canonical register. If Salesforce/Workday hold the data, mirror nightly into the git register; do not maintain two truths.
- Always include a "hidden stakeholders" review step: legal, infosec, procurement, works council/union, accessibility, downstream API consumers. README mistake #1 (missing stakeholders) is the dominant failure mode.
- Never publish names + attitudes outside the BA and sponsor. Treat the register as confidential — `password-scrubber-agent` plus a private repo, not a wiki page.
- Pair stakeholder weight with `requirements-prioritization` (e.g., MoSCoW or weighted shortest job first) so high-influence support amplifies a requirement's score.

## AI-agent gotchas

- Agents invent people. Always seed with a real org chart export (Microsoft Graph / Workday) and reject any name not in the source list unless flagged `suggested_to_verify`.
- LLMs over-classify everyone as "supportive" by default — politeness bias. Force a 4-way enum (`+/0/-/unknown`) with `unknown` as the default, and require evidence for `+` or `-`.
- Stakeholder data is regulated PII in many jurisdictions (GDPR Art. 9 if attitude implies political opinion or health). Never send the register to a third-party model without a DPA; prefer self-hosted or Anthropic with zero-retention.
- Bulk reclassification is dangerous. Cap agent actions to N stakeholders per run (e.g., 5) and force human review on the diff. A runaway agent flipping 50 stakeholders to "Resistant" is reputationally toxic.
- LLMs conflate stakeholder with persona — stakeholder = real named human/role with decision power; persona = synthesized archetype for design. Keep them in separate files; a persona never gets a row in the register.
- Influence is not seniority. The CFO's EA may have more influence on calendar decisions than the CFO. Force the agent to consider gatekeepers, not just titles.
- Human-in-the-loop checkpoints (mandatory): adding a new stakeholder, changing attitude, escalating to sponsor. Agent prepares the patch; sponsor or BA approves the merge.
- Long-context drift: when a register exceeds ~50 stakeholders, agents lose track of who is who. Page by category and operate on slices, not the full register.
- Cross-cultural blindness: agents trained on Western corp norms will miscategorize collectivist cultures (consensus = high influence even at low rank). Add a `cultural_context` system prompt for international initiatives.
- Do not let agents auto-send communications. Engagement plans are human-executed; agents draft, never deliver, especially to executives and regulators.

## References

- IIBA BABOK Guide v3, ch. 3 "Business Analysis Planning and Monitoring" / "Stakeholder Engagement" — https://www.iiba.org/standards-and-resources/babok/
- Mitchell, Agle & Wood (1997) "Toward a Theory of Stakeholder Identification and Salience" — Academy of Management Review.
- Mendelow, A. (1991) Power-Interest grid (the matrix this methodology uses) — Proceedings of the Second International Conference on Information Systems.
- PMI PMBOK 7e — Stakeholder Performance Domain.
- ISO 21500 / ISO 21502 — Project management, stakeholder engagement guidance.
- Sibling methodologies in this repo: `elicitation-techniques/`, `requirements-prioritization/`, `business-process-analysis/`, `ba-strategic-partnership/`, `ba-planning/`.
