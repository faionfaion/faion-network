# Agent Integration — Stakeholder Register

## When to use
- Foundational artifact for any project with >5 stakeholders; precedes the engagement plan and the communications plan.
- Programs that span departments, organizations, or jurisdictions where "who has authority over what" is not obvious.
- Pre-RFP / vendor selection where the buying committee needs to be enumerated, including hidden influencers (security, procurement, FinOps).
- Post-merger or post-reorg projects where lines of authority are still being redrawn.
- Compliance-driven projects (privacy, security, data residency) requiring a documented record of consulted stakeholders.
- Pair with `stakeholder-engagement/`, `stakeholder-engagement-advanced/`, `communications-management/`, `change-control/`, BA `stakeholder-analysis/`.

## When NOT to use
- Solo founders / one-person projects.
- Single-team product squads where everyone is in one Slack channel — a `MAINTAINERS.md` is enough.
- Throwaway internal scripts or hotfixes with no business stakeholder.
- Anonymous OSS communities — names and roles are missing by design.
- Crisis response where roles are pre-assigned by the incident command structure.

## Where it fails / limitations
- Registers go stale fast; an unrefreshed register is wrong, not just old.
- Hidden stakeholders (works councils, infosec, procurement, downstream consumers) are systematically missed unless seeded with org-chart context.
- Registers without behavioural triangulation rely on self-report, which is unreliable for attitude and influence.
- Influence ≠ seniority; the gatekeepers (EAs, schedulers, infosec PMs) often outrank their nominal role.
- Power/Interest 2x2 (Mendelow) flattens politics; for high-stakes programs add Mitchell-Agle-Wood salience overlay.
- LLMs invent plausible names from titles; without grounding in directory data the register is fiction.
- Confidentiality risk: registers contain PII, candid commentary, salaries, and sometimes regulated PII (GDPR Art. 9 if attitude implies political opinion or health).
- "Comprehensive" registers (>200 entries) become unusable; engagement focus dilutes.

## Agentic workflow
The register is one canonical YAML in git: `stakeholders/register.yaml`. Each entry has id, name, role, organization, category, power, interest, impact, attitude, quadrant, cadence, owner, contact_ref (1Password key), evidence[], last_engaged, hidden_flag. A subagent ingests authoritative directory exports (Entra ID, Workday, Salesforce) plus narrative inputs (kickoff transcript, RFP) and proposes register patches. Two human approvers (PM + sponsor) sign off on attitude/power changes. The register is the source for engagement-plan generation; it does not double as comms plan or RACI.

### Recommended subagents
- `faion-sdd-executor-agent` — drives register tasks (TASK_register_baseline, TASK_quarterly_refresh, TASK_hidden_stakeholders_review).
- Custom `register-curator-agent` (sonnet) — ingests directory + narrative; emits add/update patches with evidence fields; never overwrites without `update` action.
- Custom `directory-loader-agent` (haiku) — pulls org-chart slice (Entra Graph / Workday) into a typed roster used as ground truth for name/role validation.
- Custom `hidden-stakeholder-agent` (sonnet) — runs a checklist (legal, infosec, procurement, accessibility, works council, FinOps, downstream consumers, competitors) and proposes additions.
- Custom `attitude-evidence-agent` (sonnet) — for any `+/-` attitude assertion, requires and stores at least one quote / message / behaviour log line.
- Custom `salience-scorer-agent` (opus) — applies Mitchell-Agle-Wood (power × legitimacy × urgency) for political-risk overlay.
- `password-scrubber-agent` — runs over the register before commit; salaries, customer names, candid commentary leak easily.

### Prompt pattern
```
You are register-curator. Inputs: org_chart.json (authoritative names+titles),
existing register.yaml, narrative_sources[] (kickoff, charter, RFP).
For each named or implied party, emit STRICT JSON patch:
{ "action": "add|update|deprecate",
  "id": "S-NN", "name": "...", "role": "...", "organization": "...",
  "category": "Sponsor|User|Customer|Team|Regulator|Supplier|Influencer",
  "power": "H|M|L", "interest": "H|M|L", "impact": "H|M|L",
  "attitude": "+|0|-|unknown",
  "quadrant": "Manage Closely|Keep Satisfied|Keep Informed|Monitor",
  "evidence": ["org_chart.json:line_N or quote"],
  "hidden_flag": true|false,
  "rationale": "<= 2 sentences" }
Rules: name MUST appear in org_chart.json or narrative_sources. attitude
defaults to "unknown" without behavioural or quoted evidence.
Cap patches per run: 10. Flag low-confidence as "suggested_to_verify".
```

Hidden-stakeholder prompt: `Walk this checklist (legal, infosec, procurement, FinOps, accessibility, works council/union, downstream API consumers, regulators, customer success) and propose additions; cite the trigger from inputs.`

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + `git log -- stakeholders/` | Native history of relationship changes | preinstalled |
| `yq` | Patch register YAML | `apt install yq` |
| `jq` | Reduce JSON exports from HRIS / IdP | `apt install jq` |
| `csvkit` | Slice exported registers from Confluence/Jira | `pip install csvkit` |
| `mermaid-cli` (`mmdc`) | Generate the 2x2 quadrant chart from YAML | `npm i -g @mermaid-js/mermaid-cli` |
| `graphviz` (`dot`) | Influence/relationship network graph | `apt install graphviz` |
| `pre-commit` | Block attitude/power changes without `evidence:` | https://pre-commit.com |
| `op` (1Password CLI) | Store contact info out-of-band; reference by op:// URL | https://developer.1password.com/docs/cli |
| `gpg` / `age` | Encrypt the register at rest if repo is shared | https://age-encryption.org |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Microsoft Graph (Entra ID / Azure AD) | SaaS | REST/Graph | Source of truth for internal directory; must seed register. |
| Workday HCM / Personio / BambooHR / HiBob | SaaS | REST | Authoritative role/level/manager. |
| Salesforce | SaaS | REST + Bulk | Authoritative external customer/partner stakeholders. |
| HubSpot | SaaS | REST | SMB CRM equivalent. |
| Notion / Confluence / SharePoint | SaaS | REST | Common register host; weak typing — schema-validate before commit. |
| Jira / Linear / Azure DevOps | SaaS | REST | Stakeholder-as-issue with custom fields (less ideal but common). |
| Smaply / UXPressia | SaaS | Limited API | Persona/journey tools — visual artifact only. |
| Lucidchart / SmartDraw / StakeholderMap.com | SaaS | Export-only | Visual artifact target, not agent target. |
| Maptio / TeamMate / OrgVue | SaaS | REST | Org-design tools that complement registers. |
| Slack / MS Teams | SaaS | REST + Events | Behavioural signal source for attitude triangulation (with consent). |

## Templates & scripts
README provides Stakeholder Register and Individual Stakeholder Profile templates. Inline below: a 30-line script that audits register completeness and flags missing evidence.

```python
#!/usr/bin/env python3
"""register_audit.py — audit register completeness and evidence coverage."""
import json, sys, yaml, pathlib

REQUIRED = ["name", "role", "category", "power", "interest", "owner"]

def main(path: str = "stakeholders/register.yaml") -> int:
    data = yaml.safe_load(pathlib.Path(path).read_text())
    issues = []
    for s in data.get("stakeholders", []):
        sid = s.get("id", "?")
        for f in REQUIRED:
            if not s.get(f):
                issues.append(f"{sid}: missing {f}")
        att = s.get("attitude", "unknown")
        if att in {"+", "-"} and not s.get("evidence"):
            issues.append(f"{sid}: attitude={att} without evidence")
        if s.get("power") == "H" and not s.get("cadence"):
            issues.append(f"{sid}: high-power without cadence")
    print(json.dumps({"issues": issues, "count": len(issues)}, indent=2))
    return 1 if issues else 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```

Run via pre-commit; failure blocks merge until evidence is added or attitude is downgraded to `unknown`.

## Best practices
- Store the register in git (YAML), never in a wiki — diffs become history; CODEOWNERS gate sponsor sign-off on attitude / power changes.
- Require an `evidence:` field on every attitude or power assertion (quote, transcript line, ticket link, log line). No evidence → `unknown`.
- Refresh quarterly minimum; monthly during high-volatility periods (post-merger, leadership change, regulator activity).
- Triangulate self-reported attitude with at least one behavioural signal (attendance, response time, escalations, sentiment).
- One canonical register; if Workday or Salesforce holds source data, mirror nightly into the register, do not maintain two truths.
- "Hidden stakeholders" review is a recurring task: legal, infosec, procurement, FinOps, accessibility, works council, downstream consumers, regulators.
- Contact info via 1Password / secrets manager — reference by `op://` key, not inline.
- Mitchell-Agle-Wood salience overlay for any program with regulator or political risk.
- Cap register size; if >50 entries, partition by category and operate on slices.
- Treat the register as confidential — private repo, scrubber pre-commit, encrypted at rest if shared broadly.

## AI-agent gotchas
- Agents invent people. Always ground name validation in an authoritative directory; reject any name absent from source.
- LLMs default to "supportive" attitude (politeness bias). Force a 4-way enum with `unknown` default and require evidence for `+/-`.
- Stakeholder data is regulated PII; never send the register to a third-party LLM without DPA; prefer self-hosted or zero-retention Anthropic.
- Bulk reclassification is dangerous; cap agent edits per run and require human review on diff.
- Stakeholder vs. persona conflation: stakeholder = real named human/role with decision power; persona = synthesized archetype. Separate files.
- Influence inference from titles alone misses gatekeepers (EAs, infosec, procurement); force the agent to enumerate gatekeepers explicitly.
- Long-context drift: registers >50 stakeholders blow the prompt; page by category.
- Cross-cultural miscoding — agents trained on Western norms misread consensus cultures. Add `cultural_context` system prompt for international initiatives.
- Sentiment-from-Slack is lossy; never act on a single message.
- Attribute leakage: do not include candid commentary in machine-readable fields — use a separate `notes_private` file with stricter ACL.
- Human-in-the-loop checkpoints (mandatory): adding a stakeholder, attitude change, deprecation, sharing register outside immediate team, salience overlay decisions.

## References
- PMI PMBOK 7e — Stakeholder Performance Domain.
- PMI PMBOK 6e — Stakeholder Management Knowledge Area (templates, processes).
- Mendelow, A. (1991) — Power-Interest grid.
- Mitchell, Agle & Wood (1997) "Toward a Theory of Stakeholder Identification and Salience" — Academy of Management Review.
- Freeman, R. E. — "Strategic Management: A Stakeholder Approach".
- Bourne, L. — "Stakeholder Relationship Management" (Stakeholder Circle).
- ISO 21500 / 21502 — stakeholder identification and engagement guidance.
- IIBA BABOK v3 — Stakeholder Analysis tasks.
- Sibling methodologies: `stakeholder-engagement/`, `stakeholder-engagement-advanced/`, `communications-management/`, `change-control/`, BA `stakeholder-analysis/`.
