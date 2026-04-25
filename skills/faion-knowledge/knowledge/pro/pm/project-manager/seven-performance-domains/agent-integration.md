# Agent Integration — Seven Performance Domains (PMBoK 8)

## When to use
- Structuring an end-to-end project narrative (charter → closure) around the PMBoK 8 domains rather than legacy process groups, so deliverables map cleanly to a known taxonomy.
- Auditing an existing project plan: walk each of the seven domains and surface gaps (missing finance baseline, no governance forum, no risk owner).
- Building a project status dashboard: one panel per domain, traffic-light per outcome.
- Tailoring methodology selection — domains are stable; processes inside them flex predictive vs agile vs hybrid.
- Onboarding a PM-agent persona: the seven-domain map is the smallest mental model that still covers everything.

## When NOT to use
- Pure-Scrum teams with a Product Owner / Scrum Master that never report to PMI-style governance — Scrum events already cover the domains implicitly; mapping is busywork.
- Tiny solopreneur projects (< 1 week, single deliverable) where governance + finance domains collapse into "did I ship it / did I get paid".
- Standards-bound shops still on PMBoK 6 (process groups + ten knowledge areas); switching narrative mid-project confuses sponsors.
- Domain-driven design conversations — "domain" overloads the term and creates noise.

## Where it fails / limitations
- Domains are descriptive, not generative: knowing "Risk" is a domain does not produce a risk register; it points you at the methodology.
- "Governance replaces Integration Management" is not a 1:1 swap; portfolio-level governance was previously implicit and now leaks into PM scope, surprising old PMP holders.
- "Quality integrated throughout" sounds elegant but hides quality work; agents skip explicit quality plans because the domain is invisible.
- Stakeholder + Communications fusion drops dedicated comms artefacts (comms plan, RACI for messages); teams forget to recreate them.
- Procurement moved to appendix → agents under-emphasize vendor risk on contractor-heavy projects.
- Sustainability is named but unmeasured in PMBoK 8 itself; teams need external frameworks (GHG Protocol, B-Corp) to operationalize.

## Agentic workflow
Use the seven domains as a top-level rubric the agent walks linearly: for each domain, the agent asks "what artefact exists, who owns it, what is the current state?". Output is a markdown matrix (domain × artefact × owner × status × next-action). Re-run weekly; diff drives the status report. Never let the agent invent domain names — pin them to the canonical seven (Governance, Scope, Schedule, Finance, Stakeholders, Resources, Risk).

### Recommended subagents
- `pm-domain-auditor` (define inline) — walks the seven domains against a project workspace and produces a gap matrix.
- `faion-sdd-executor` — when a domain gap becomes a task, drives implementation through quality gates.
- `faion-brainstorm` — when scoping a new domain artefact (e.g. first risk register), use diverge / converge / review to generate the initial list.
- `nero-improve` — feed the gap matrix into the improver loop for periodic remediation.

### Prompt pattern
```
You are a PM domain auditor. Walk the 7 PMBoK 8 domains in fixed order:
[Governance, Scope, Schedule, Finance, Stakeholders, Resources, Risk].

For each domain output:
- artefact_path: relative path or "MISSING"
- owner: name or "UNASSIGNED"
- last_updated: ISO date or "never"
- status: green/amber/red
- next_action: one sentence, imperative

Sources: <list of paths to scan>
Constraints:
- Use ONLY the seven canonical names; do not invent.
- Quality, Communications, Procurement are integrated; flag if missing as sub-items.
- Output JSON object keyed by domain.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Pull issues / PRs as scope + schedule signal | https://cli.github.com/ |
| `jira-cli` | Read epics / stories per domain | https://github.com/ankitpokhrel/jira-cli |
| `linear` CLI / API | Stakeholder + scope sync | https://developers.linear.app/docs/cli |
| `monday-cli` (community) | Resources + risk boards | https://github.com/mondaycom |
| `gitleaks` / `trufflehog` | Governance / sec hygiene per domain audit | https://github.com/gitleaks/gitleaks |
| `notion-sdk` (Python/JS) | Pull domain artefacts from a project workspace | https://developers.notion.com/ |
| `mermaid-cli` | Render domain interaction diagrams | https://github.com/mermaid-js/mermaid-cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira Premium / Advanced Roadmaps | SaaS | Yes — REST + JQL | Scope + Schedule + Resources domains |
| ClickUp | SaaS | Yes — REST | Stakeholders + Resources via Workload view |
| Smartsheet | SaaS | Yes — REST | Governance forums + Finance dashboards |
| Monday.com | SaaS | Yes — GraphQL | Risk + Resources boards |
| Notion / Confluence | SaaS | Yes — REST | Domain charter + status doc per domain |
| Power BI / Looker / Metabase | SaaS / OSS | Partial — SQL APIs | Finance + Measurement dashboards |
| MS Project / Project for the Web | SaaS | Yes — Graph API | Schedule + Resources baseline |
| Asana Portfolios | SaaS | Yes — REST | Governance roll-up across projects |

## Templates & scripts
See `templates.md` for the domain checklist. Inline domain-audit walker (Python, ≤50 lines):

```python
#!/usr/bin/env python3
"""Walk PMBoK 8 domains against a project root; emit JSON gap matrix."""
import json, os, sys
DOMAINS = ["Governance", "Scope", "Schedule", "Finance",
           "Stakeholders", "Resources", "Risk"]
EXPECTED = {
    "Governance":   ["charter.md", "decision-log.md"],
    "Scope":        ["scope.md", "wbs.md"],
    "Schedule":     ["schedule.md", "milestones.md"],
    "Finance":      ["budget.md", "cost-baseline.md"],
    "Stakeholders": ["stakeholder-register.md", "comms-plan.md"],
    "Resources":    ["raci.md", "team-charter.md"],
    "Risk":         ["risk-register.md"],
}
def audit(root):
    out = {}
    for d in DOMAINS:
        items = []
        for f in EXPECTED[d]:
            p = os.path.join(root, f)
            items.append({"file": f, "exists": os.path.isfile(p)})
        present = sum(1 for i in items if i["exists"])
        status = "green" if present == len(items) else \
                 "amber" if present else "red"
        out[d] = {"status": status, "items": items}
    return out
if __name__ == "__main__":
    print(json.dumps(audit(sys.argv[1] if len(sys.argv) > 1 else "."), indent=2))
```

## Best practices
- Treat domains as the project's table of contents; every artefact lives under exactly one domain.
- Pair each domain with a measurable outcome (e.g. Finance → "CPI ≥ 0.95 at every gate"), not just an activity.
- Run the seven-domain audit before every steering committee — drives the status pack automatically.
- When a process feels homeless, default to Governance; do not invent a new domain.
- Map domain gaps to risks: a missing artefact = a risk in the Risk domain.
- For PMBoK 7 → 8 transitions, keep a translation table next to the audit so old PMs do not wave the integration-management flag.
- Track domain coverage as a project KPI (e.g. "7/7 green" by gate 2).

## AI-agent gotchas
- LLMs blur Stakeholders + Communications back into separate domains because PMBoK 6 is heavily represented in training data; pin the canonical seven in the system prompt.
- Agents will silently rename Governance to "Integration Management"; reject any output containing the old name.
- "Quality" is integrated, not a domain — agents keep adding an 8th domain. Validate output length == 7.
- Sustainability creeps into Stakeholders or Risk inconsistently; either keep it under Governance or as an explicit sub-criterion in every domain — pick one and lock it.
- Agents underweight Procurement on vendor-heavy projects because PMBoK 8 demoted it; force a vendor-risk question into the audit.
- Domain status colors drift over time (every artefact "green") — calibrate by sampling 1 in 5 domains for human review.
- Output ordering matters: list domains in fixed sequence so diffs across runs are stable.

## References
- PMI — A Guide to the PMBOK 8th Edition (preview / change papers): https://www.pmi.org/standards/pmbok
- PMI — PMBOK 7 Performance Domains explained: https://www.pmi.org/learning/library/pmbok-guide-7th-edition-performance-domains
- PMI — "What's new in PMBOK 8" (PMI blog / community articles)
- Project Management Institute Code of Ethics & Professional Conduct: https://www.pmi.org/about/ethics/code
- Mike Griffiths — "PMBOK 7th vs 6th Edition" (Leading Answers blog)
- Praxis Framework (alt domain model, useful contrast): https://www.praxisframework.org/
