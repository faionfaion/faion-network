# Agent Integration — Stakeholder Engagement (Advanced)

## When to use
- Stakeholder Register exists but the project is missing champions, has dormant supporters, or active resisters.
- Pre-launch and change-management work where adoption depends on department heads.
- Long projects (>6 months) where engagement levels drift; quarterly re-assessment needed.
- Coalition-building for portfolio shifts (M&A, reorg, platform migration).
- Public-facing launches where end users are Unaware and need to be moved to Supportive.

## When NOT to use
- One-off small tasks with no organisational politics.
- Adversarial negotiations (procurement, legal disputes) — engagement implies collaboration; use negotiation playbooks instead.
- Crisis comms — different discipline (incident comms, PR), different cadence and tone.

## Where it fails / limitations
- Levels (Unaware → Resistant → Neutral → Supportive → Leading) are not strictly linear; a Leading stakeholder can drop to Resistant if betrayed once.
- Engagement Plans get written and never executed — without rituals (1:1 cadence, status emails) they decay.
- Optimism bias: PMs over-report Supportive. Use behavioural evidence (attendance, response time, public statements) not vibes.
- Hidden stakeholders (auditors, regulators, end users) get neglected because they don't show up; explicit search needed.
- Cultural variance: "Resistance" looks different across cultures (silence vs. open disagreement); single rubric misclassifies.

## Agentic workflow
A subagent reads the Stakeholder Register + recent communications log + meeting minutes to assess current engagement levels with evidence quotes, identifies gaps to desired levels, and drafts engagement activities per stakeholder. Pair with a meeting-prep helper that produces pre-/post-meeting briefs. Engagement classification must be evidence-based — refuse to upgrade a stakeholder to Supportive without a quoted positive signal. Human-in-loop for tactic selection because politics is contextual; agent proposes, human chooses.

### Recommended subagents
- `faion-pm-agent` — produces engagement plan, weekly drift report.
- `faion-business-analyst` — links engagement signals to requirement risk (resistant SME = requirement gap).
- `faion-improver` — periodic audit: which stakeholders haven't been touched in N weeks vs. their target cadence.
- A communications subagent (custom) — drafts personalised stakeholder updates from the project status report.

### Prompt pattern
```
Input: stakeholders.yaml, comms_log_30d.md, meeting_minutes_30d.md
Output: engagement_assessment.yaml — for each stakeholder:
{current_level, evidence_quotes[], desired_level, gap, drift_30d}.
Rule: each level upgrade needs >=1 quoted positive signal; downgrades need a negative one.
```

```
For meeting with {stakeholder_id} on {date}:
produce prep_sheet (their concerns, motivations, last interaction,
desired outcome, key messages, anticipated objections, asks).
End with a single-paragraph "what good looks like" outcome statement.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh api` | Pull GitHub PR review patterns to gauge engagement of technical stakeholders | https://cli.github.com |
| `slack-cli` / Slack API | Sample channel activity per stakeholder | https://api.slack.com |
| `jira-cli` | Look at comment frequency on tickets owned/watched by stakeholder | https://github.com/ankitpokhrel/jira-cli |
| `gcalcli` | Schedule and track 1:1 cadence | https://github.com/insanum/gcalcli |
| `pandoc` | Render engagement plan → PDF for sponsor review | https://pandoc.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Salesforce / HubSpot CRM | SaaS | Yes — REST API | Use Activity History as engagement signal |
| Gainsight / Catalyst | SaaS | Yes — REST API | Customer success engagement scoring |
| Microsoft Viva / Workplace Analytics | SaaS | Limited (privacy gates) | Meeting time per stakeholder pair |
| Notion / Airtable | SaaS | Yes — REST API | Engagement plan + tracking log |
| LinkedIn Sales Navigator | SaaS | Limited (TOS-restrictive) | External-stakeholder activity; manual only |
| Loomly / Status Hero | SaaS | Yes — REST API | Auto-distribute status updates per cadence |
| Mailchimp / Customer.io | SaaS | Yes — REST API | Templated updates to "Keep Informed" cohort |
| Zoom / MS Teams API | SaaS | Yes | Pull meeting attendance/duration as engagement evidence |

## Templates & scripts
See `templates.md` for engagement plan and meeting-prep formats. Inline drift detector (≤50 lines):

```python
# engagement_drift.py — flags stalled stakeholders
import yaml, sys
from datetime import date, timedelta

THRESH = {"manage-closely": 7, "keep-satisfied": 14,
          "keep-informed": 14, "monitor": 30}  # days

def main(reg_path, log_path):
    register = yaml.safe_load(open(reg_path))
    touches = yaml.safe_load(open(log_path))  # [{stakeholder_id, date}]
    last = {}
    for t in touches:
        d = date.fromisoformat(t["date"])
        last[t["stakeholder_id"]] = max(last.get(t["stakeholder_id"], d), d)

    today = date.today()
    for s in register:
        sid = s["id"]
        max_gap = THRESH.get(s.get("quadrant", "monitor"), 30)
        gap = (today - last.get(sid, today - timedelta(days=999))).days
        if gap > max_gap:
            print(f"[DRIFT] {sid} {s['name']} q={s['quadrant']} gap={gap}d (>{max_gap}d)")
            print(f"        suggested action: {s.get('comms', {}).get('channel', '1:1')}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
```

## Best practices
- Build relationships before you need them — first ask should not be a favour.
- Pre-meeting prep ≥ 15 min. Personalise: reference the stakeholder's last public statement or initiative.
- Engage resistors face-to-face, not by email — written tone amplifies friction.
- Recognition compounds: public credit for Supportive stakeholders converts them to Leading.
- Cadence per quadrant: Manage-Closely weekly, Keep-Satisfied bi-weekly, Keep-Informed weekly broadcast, Monitor monthly summary.
- Track engagement-level history as a time series — trend lines reveal drift the snapshot can't.
- Pair with Risk Register: a Resistant high-influence stakeholder is a top-tier project risk.

## AI-agent gotchas
- Polite-tone bias: agents up-rate engagement on courteous emails. Require explicit positive evidence ("agreed to sponsor", "publicly endorsed").
- Translation/cultural cues missed: passive-voice criticism reads as Neutral to LLMs but is Resistant in many cultures. Have human reviewer per region.
- Auto-generated personalised messages can feel canned; require the agent to surface context bullets, not write the email body.
- Meeting-prep agent will pad with generic talking points; force max-3 messages and 1 ask.
- Do not let agents propose moving Resistant directly to Leading — the Resistant→Neutral hop must be earned with a concrete commitment.
- Privacy: engagement levels are sensitive; never let an agent share level-classification with the stakeholder themselves.

## References
- PMBOK Guide 7th Edition — Stakeholder Performance Domain.
- "Stakeholder Theory" — R. Edward Freeman.
- "Influence: The Psychology of Persuasion" — Robert Cialdini (engagement tactics).
- "Crucial Conversations" — Patterson, Grenny, McMillan, Switzler (resistant-stakeholder dialogue).
- Bourne L., "Stakeholder Engagement" (Stakeholder Circle methodology).
