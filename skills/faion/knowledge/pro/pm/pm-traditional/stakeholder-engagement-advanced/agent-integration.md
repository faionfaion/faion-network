# Agent Integration — Stakeholder Engagement (Advanced)

## When to use
- Cross-functional / cross-org programs with >10 stakeholders and material political risk.
- Change initiatives (transformations, M&A integration, ERP rollouts) where adoption hinges on advocacy.
- Regulated programs where named approvers must be tracked through engagement levels.
- Long-running programs (>6 months) where attitudes drift and need monitoring.

## When NOT to use
- Small co-located teams where lunch and standups already provide the engagement.
- Pure-internal tools with single sponsor — overhead exceeds benefit.
- One-off launches with <4 stakeholders.
- Crisis recovery where speed dominates relationship calibration.

## Where it fails / limitations
- "Engagement level" labels (Resistant→Leading) are subjective; without calibration two PMs rate the same person differently.
- The matrix encourages PMs to optimize labels, not relationships.
- Documenting strategies for individuals can leak and damage trust if the artefact is mishandled.
- Engagement plans go stale fast; without weekly maintenance the data lies.
- Cultural mismatch — tactics like "give visible roles" backfire in low-individualism cultures.

## Agentic workflow
A subagent is well-suited to: ingest meeting notes / Slack / email signals, extract per-stakeholder sentiment cues, propose engagement-level updates, draft personalized meeting prep sheets, and flag warning signs (skipped meetings, delayed responses). Humans own the actual conversations and the political judgment. Treat all stakeholder data as confidential — keep the agent's working set local and avoid sending personal assessments to third-party logs.

### Recommended subagents
- `faion-pm-agent` — owns engagement plan; drafts strategies, updates the matrix.
- `faion-communicator` agent (knowledge/solo/comms/communicator) — drafts tailored messages per stakeholder voice.
- `faion-business-analyst` (ba-core) — strong for power/interest grid mapping and stakeholder-needs analysis.

### Prompt pattern
```
Given the stakeholder register + last 14 days of project artefacts (meeting
notes, status emails, Slack), output JSON:
[{stakeholder_id, signals: [...], suggested_level: U|R|N|S|L,
  confidence: low|med|high, rationale, recommended_next_step}]
Only update level when confidence != low. Cite source quote per signal.
```

```
Draft meeting prep for stakeholder <id>: their stated concerns, prior
positions, our two objectives, three message options ranked by
likelihood-of-acceptance, anticipated objections + responses.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` / `jira-cli` | Stakeholder log as private issues with `stakeholder` label | vendor docs |
| `mermaid-cli` | Power/interest grid as `quadrantChart` | https://mermaid.js.org |
| `vault` (HashiCorp) | Encrypt the engagement plan at rest | https://www.vaultproject.io |
| `sops` | Mozilla SOPS for git-tracked encrypted plans | https://github.com/getsops/sops |
| `pandoc` | Render plan to PDF for sponsor review | https://pandoc.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| HubSpot CRM | SaaS | Yes — REST API | Track interactions, sentiment, contact cadence. |
| Salesforce | Enterprise SaaS | Yes — REST API | Heavyweight; for enterprise sponsor-mapping. |
| Affinity / Streak | SaaS | Yes — REST API | Relationship-intelligence flavour. |
| Notion stakeholder DB | SaaS | Yes — REST API | Best for solo/SDD; agent-friendly. |
| Miro/Lucid power-interest grid | SaaS | Limited | Visualization only. |
| Microsoft Viva Glint / Pulse | Enterprise SaaS | Yes — Graph API | Sentiment surveys at scale. |
| Loomio | OSS | Limited | Decision-engagement, not 1:1 tracking. |

## Templates & scripts
See `templates.md` for the engagement plan and meeting prep sheet. Helper to compute level deltas between two snapshots:

```python
# engagement_diff.py — diff two YAML stakeholder snapshots, list movement.
import sys, yaml
ord_ = {"U":0,"R":1,"N":2,"S":3,"L":4}
old = {s["id"]: s for s in yaml.safe_load(open(sys.argv[1]))}
new = {s["id"]: s for s in yaml.safe_load(open(sys.argv[2]))}
for sid, s in new.items():
    o = old.get(sid)
    if not o:
        print(f"NEW {sid} -> {s['level']}")
    elif s["level"] != o["level"]:
        delta = ord_[s["level"]] - ord_[o["level"]]
        arrow = "↑" if delta > 0 else "↓"
        print(f"{arrow} {sid}: {o['level']} -> {s['level']} ({s.get('rationale','')})")
for sid in old.keys() - new.keys():
    print(f"REMOVED {sid}")
```

## Best practices
- Never share the engagement matrix with stakeholders themselves; it is a working PM artefact.
- Pair every "desired level" with a behavioral indicator (e.g. "Sales Director quotes the project in QBR") so progress is observable.
- Schedule low-effort touchpoints with Supportive stakeholders; relationship maintenance prevents regression.
- For Resistant stakeholders, document concerns in their own words before designing strategy.
- Keep a 30-day rolling engagement-trend chart to spot drift early.
- Pre-mortem politically risky decisions with a "stakeholder reaction" column before announcing.

## AI-agent gotchas
- Stakeholder data is sensitive PII-adjacent; do not pass it to third-party LLMs without encryption and DPA.
- LLMs over-detect "resistance" from neutral language and over-detect "support" from politeness; require multi-signal corroboration.
- Agents will draft suspiciously-similar engagement strategies for everyone — force per-person motivations as input.
- Don't let the agent autonomously send messages to stakeholders; always human-review the wording.
- Token budget: send only the active stakeholders + last N interactions; full history is wasteful and risky.
- Human-in-loop checkpoints: (1) every level change, (2) every drafted message before send, (3) any "warning sign" auto-flag before escalation.

## References
- PMI, *PMBOK Guide* 7th ed., Stakeholder Performance Domain.
- Mendelow, A., "Stakeholder Mapping" (1991) — power/interest grid.
- D. Bourne, *Stakeholder Relationship Management* (2009).
- J. Kotter, *Leading Change* (1996) — coalition-building patterns.
