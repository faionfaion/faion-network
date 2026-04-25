# Agent Integration — Communications Management

## When to use
- Standing up a new project where stakeholder count is >5 and you need a written who/what/when/how matrix before kickoff.
- Distributed / async-first teams where missed updates are the dominant failure mode and signal-to-noise ratio matters more than meeting frequency.
- Regulated programs (SOX, HIPAA, GDPR, MDR) where regulator-facing communications must be traceable, dated, and signed off.
- Recovery of "drowning in Slack/email" situations: build the communications matrix to consolidate channels and kill duplicate updates.
- Multi-vendor / system integrator engagements with formal status cadences and escalation paths required by contract.
- Pairing with `stakeholder-engagement/` (the matrix is the executable form of the engagement plan), `risk-management/` (risk-review cadence), `change-control/` (CR communication), and `lessons-learned/` (close-out report cadence).

## When NOT to use
- Solo founders or 2–3-person startups pre-PMF — the matrix overhead exceeds value; a single Slack channel + weekly investor email is enough.
- Crisis / incident response — runbooks and on-call rotations replace this; do not retrofit a comms plan during P0.
- One-off internal hackathons or short spikes (<2 weeks) — agree on channel verbally, skip the artifact.
- When stakeholders refuse to be classified or the political situation is too fluid to commit to a cadence — wait, do interview rounds first.

## Where it fails / limitations
- Plans go stale within 4–8 weeks; orgs reorg, vendors swap PMs, sponsors rotate. A static plan committed once and never refreshed becomes wrong, not just old.
- "Push" channels (email, status reports) are routinely ignored — recipients report being informed while having read nothing. The plan does not measure consumption.
- Time-zone fan-out is rarely modelled: a "weekly status call Tue 10:00" excludes APAC silently. The matrix needs explicit timezone columns or 2 cadences.
- Communication overload (the README's #1 mistake) is not detected by the plan itself; you need an out-of-band signal (calendar load, message volume, sentiment).
- Cross-cultural mismatch: high-context cultures (JP, KR, parts of EU) read indirect communication that LLMs and Western templates collapse to "neutral".
- Decisions communicated only verbally vanish — the plan must enforce a written artifact (decision log, ADR) per decision, not just a meeting.

## Agentic workflow
Treat the comms plan as a structured YAML file (`comms/plan.yaml`) with one entry per stakeholder × channel and one entry per recurring event. A subagent generates status drafts, meeting agendas, and decision-log entries from project artifacts (Jira/Linear queries, git log, CI status) and emits them as PRs against the project repo for human approval before send. Never let an agent auto-deliver to executives, regulators, or external customers — drafts only. Pair with `stakeholder-engagement/register.yaml` so cadence is derived from the quadrant (Manage Closely → weekly, Keep Informed → monthly digest).

### Recommended subagents
- `faion-sdd-executor-agent` — drives the comms plan as SDD tasks: TASK_comms_plan, TASK_status_report_draft, TASK_meeting_notes_capture. Each emits a commit + execution report.
- `password-scrubber-agent` — runs over status drafts before send; status reports are a top leak path for credentials, internal URLs, salary data, customer names.
- A custom `status-report-agent` (model: haiku per README Agent Selection): pulls Jira/Linear/git data, fills the README's status-report template, posts as a draft PR.
- A custom `meeting-notes-agent` (model: haiku): consumes meeting transcript (Otter, Granola, Fathom), emits structured notes + action items + decision log entries per the README template.
- A custom `comms-plan-curator-agent` (model: sonnet): reconciles the comms plan against the stakeholder register weekly; flags missing cadences, dead channels, abandoned recipients.
- A custom `escalation-router-agent` (model: sonnet): when an issue lands with `severity:high`, looks up the README escalation table and proposes recipient + channel + draft message.

### Prompt pattern
Two-stage: extract → render.

```
You are the status-report agent. Inputs: project name, week_start date, list of
closed Jira/Linear issues, current open risks (from risks/register.yaml),
budget snapshot (from EVM), schedule snapshot.

Emit STRICT MARKDOWN matching the README "Weekly Status Report" template.
Rules:
- Summary <= 2 sentences. Lead with overall status (GREEN/YELLOW/RED).
- "Progress This Week" only contains items with state=Done in this week.
- "Risks/Issues" cites risk IDs from the register, not free-text.
- Schedule/Budget/Scope numbers must come from inputs — never invent.
- If a number is missing, render "N/A" and add a TODO line.
```

Meeting-notes prompt: `Given the transcript and the README "Meeting Notes" template, emit notes. Every action item must have owner + due date or be flagged "OWNER_MISSING". Every decision goes into decisions/YYYY-MM-DD.md as a separate ADR-style entry.`

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + `git log` | Source of truth for "what shipped this week" feeding the status report | preinstalled |
| `gh` (GitHub CLI) / `glab` (GitLab CLI) | Pull issue/PR state into status drafts; comment status updates on issues | https://cli.github.com / https://gitlab.com/gitlab-org/cli |
| `jira-cli` (`ankitpokhrel/jira-cli`) | Query Jira via JQL for status sections | https://github.com/ankitpokhrel/jira-cli |
| `linear-cli` / Linear API + `curl` | Fetch Linear issues by team/project for status drafts | https://developers.linear.app |
| `slack` CLI / `slackdump` | Post pre-approved digests to channels; pull thread history for sentiment triangulation | https://api.slack.com/automation/cli |
| `mscli` / `m365-cli` | MS Teams + Outlook scheduling and message posting | https://pnp.github.io/cli-microsoft365/ |
| `pandoc` | Convert markdown status reports to PDF/HTML for execs and steering committee | https://pandoc.org |
| `mermaid-cli` (`mmdc`) | Generate Gantt / cadence visualizations embedded in status reports | `npm i -g @mermaid-js/mermaid-cli` |
| `taskwarrior` / `dstask` | Personal action-item tracker for action-item follow-up between meetings | https://taskwarrior.org |
| `pre-commit` | Block commits to `comms/plan.yaml` that change cadence without rationale | https://pre-commit.com |
| `yq` / `jq` | Read and patch the plan YAML / aggregate JSON exports | `apt install yq jq` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Slack | SaaS | REST + Events API | Primary async channel; bots can post but should not auto-send to leadership. Use approval workflow. |
| Microsoft Teams | SaaS | Graph API | Enterprise default; Teams + Outlook + Planner integration. Adaptive cards for status. |
| Email (SMTP / Gmail / Outlook) | SaaS | SMTP / Graph / Gmail API | Formal channel; agents draft, human sends. DKIM/SPF check before automation. |
| Jira | SaaS | REST v3 + JQL | Status data source; @mention notifications drive action-item flow. |
| Linear | SaaS | GraphQL | Lightweight equivalent; cycle reports auto-summarize work. |
| Asana | SaaS | REST API | Status updates per portfolio; built-in weekly status feature with API access. |
| Confluence / Notion | SaaS | REST API | Pull-channel home for status reports and meeting notes; weak typing — schema-validate first. |
| Google Workspace (Docs/Calendar/Meet) | SaaS | Google APIs | Doc-first orgs; agents can create agendas in Docs and Meet events. |
| Zoom / Google Meet / Teams Meetings | SaaS | REST / Graph | Meeting orchestration + recording; pair with transcription service. |
| Otter / Fathom / Granola / Fireflies | SaaS | REST / Webhooks | Auto-transcription + AI summary; drives meeting-notes-agent. |
| Loom | SaaS | REST API | Async video updates substitute for some recurring meetings. |
| Statushero / Range / Friday | SaaS | REST API | Async standup tools that replace daily standups for distributed teams. |
| Mattermost / Rocket.Chat / Zulip | OSS | REST API | Self-hosted equivalents to Slack; required for regulated/airgapped environments. |
| BCC Mail Manager / Mailchimp / Customer.io | SaaS | REST API | Bulk stakeholder digests (investors, beta users) when count >50. |

## Templates & scripts
The README provides Communication Plan, Meeting Notes, and Weekly Status Report templates. Inline below: a script that ingests `comms/plan.yaml` and prints stakeholders missing an update this week.

```python
#!/usr/bin/env python3
"""comms_audit.py — list stakeholders due an update this week."""
from __future__ import annotations
import datetime as dt
import pathlib
import sys
import yaml

CADENCE_DAYS = {"daily": 1, "weekly": 7, "biweekly": 14, "monthly": 30, "quarterly": 90}

def main(plan_path: str = "comms/plan.yaml") -> int:
    plan = yaml.safe_load(pathlib.Path(plan_path).read_text())
    today = dt.date.today()
    overdue: list[str] = []
    for entry in plan.get("communications", []):
        last = entry.get("last_sent")
        if last is None:
            overdue.append(f"{entry['stakeholder']} — never sent")
            continue
        last_date = dt.date.fromisoformat(str(last))
        gap = (today - last_date).days
        max_gap = CADENCE_DAYS.get(entry.get("frequency", "weekly"), 7)
        if gap > max_gap:
            overdue.append(
                f"{entry['stakeholder']} ({entry['frequency']}): {gap}d since {last_date}"
            )
    if overdue:
        sys.stdout.write("OVERDUE COMMUNICATIONS:\n  " + "\n  ".join(overdue) + "\n")
        return 1
    sys.stdout.write("All communications current.\n")
    return 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```

Wire into a daily cron / GitHub Action so the PM gets a Monday-morning audit issue.

## Best practices
- Store `comms/plan.yaml` in the project repo, not a wiki — diffs become the cadence-change history; CODEOWNERS gates sponsor sign-off on adding/removing recipients.
- Every recurring meeting must have an agenda template committed to the repo; agendas without inputs auto-cancel via a calendar bot.
- Decisions never live in chat. Pin a decision log (`decisions/YYYY-MM-DD-slug.md`) and reference it from chat — chat history is not searchable enough to be a system of record.
- Status report colour (GREEN/YELLOW/RED) must come from quantitative thresholds in the plan (e.g., schedule slip <5d = GREEN, 5–14d = YELLOW, >14d = RED), not PM mood.
- Limit recurring meetings to <10% of any role's calendar; review every quarter and kill any meeting where >20% of attendees would not opt in voluntarily.
- Match channel to confidentiality: legal/HR/security never on Slack public channels. Encode allowed channels per topic in the plan.
- Time-zone the cadence: any global meeting rotates time across quarters or splits into 2 sessions. Encode TZ + acceptable hours per stakeholder.
- Translate for executives: 1 page max, lead with the ask/decision, no jargon, numbers come first. Preserve detail in an appendix link.
- Pair the comms plan with `risk-management` so risk-trigger thresholds drive escalation messages automatically.
- Weekly automatic audit (`comms_audit.py`) opens an issue when any stakeholder is overdue — the plan only works if it self-monitors.

## AI-agent gotchas
- Agents auto-confabulate progress. Force every status section to cite issue IDs / commit SHAs; reject reports that claim "X completed" without a linked artifact.
- LLMs default to over-positive tone; set status colour from numeric inputs only, and require RED/YELLOW reasoning to cite the breaching metric.
- Meeting transcripts are PII (voice + identifiable speech) and often contain confidential customer data. Never send to a third-party model without DPA; prefer self-hosted Whisper / on-prem Otter Enterprise / zero-retention Anthropic.
- Action items hallucinate owners — agents pick the most-mentioned name. Force owner extraction from the transcript with explicit confirmation phrases ("I'll take that", "<name> will…"), else flag `OWNER_MISSING`.
- Auto-send is forbidden to: executives, regulators, customers, legal, board. Agent prepares the message; a human reviews and sends. Encode this in the plan as `auto_send: false` per recipient.
- Long meetings (>60 min) blow context windows; chunk transcripts by agenda topic, summarize per chunk, then stitch — do not feed 90-min raw transcripts to a single prompt.
- Translation: agents flatten cultural register. Leave Ukrainian/Japanese/Spanish executive comms to humans or to a translator-specialized model with explicit register instructions.
- Slack/Teams emoji and reaction signals are missed by text-only ingest; if sentiment matters, capture reactions explicitly.
- Bulk digest pitfalls: when an agent generates 50 personalized investor updates, a single hallucination becomes a reputational incident. Cap bulk per run, force human spot-check on N samples.
- Context-window leakage: status drafts often pull from many private docs. Scrub PII, customer names, and credentials before any third-party model call.
- Human-in-the-loop checkpoints (mandatory): adding/removing a stakeholder from the plan, changing cadence on `Manage Closely` recipients, sending the first message in a new channel, escalation to sponsor.

## References
- PMI PMBOK 7e — Stakeholder Performance Domain, Communications.
- PMI PMBOK 6e — Communications Management Knowledge Area (still useful for templates and types).
- ISO 21500 / ISO 21502 — communications guidance for project management.
- Maister, Green & Galford "The Trusted Advisor" — written-comm principles for executive audiences.
- "The Phoenix Project" / "The DevOps Handbook" — comms cadence in fast-flow orgs.
- Sibling methodologies: `stakeholder-engagement/`, `risk-management/`, `change-control/`, `lessons-learned/`.
- Slack/Teams bot frameworks: https://api.slack.com / https://learn.microsoft.com/graph/teams-concept-overview
