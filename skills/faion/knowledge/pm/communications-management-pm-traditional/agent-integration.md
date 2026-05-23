# Agent Integration — Communications Management (PM Traditional)

## When to use
- Bootstrapping a project's communication plan from a stakeholder register: deriving a per-stakeholder matrix of needs/format/frequency/owner.
- Designing meeting cadences (daily/weekly/monthly) to minimise meeting load while keeping decisions flowing.
- Generating standardised status report and meeting-notes templates that propagate across project portfolios.
- Auditing existing comms hygiene — too many meetings, missing owners, decisions undocumented, escalation path unclear.
- Routing comms by channel: choosing email vs Slack vs meeting vs wiki for each communication purpose.
- Solopreneur client-comms playbook: weekly update emails + on-demand Loom + monthly milestone review.

## When NOT to use
- Single-stakeholder projects (just you + one customer) — informal communication suffices, the matrix is overkill.
- Crisis / incident response — comms move to incident-management runbook (status page, war room, hourly updates), not the PM matrix.
- High-trust / collocated small teams using ambient awareness; formalising channels can suppress collaboration.
- Sales / marketing / support communications — those are external-comms with their own playbook (CRM, email-marketing, ticketing).

## When NOT to use
- Already-mature org with a working comms cadence; switching to a new template imposes friction with little gain.

## Where it fails / limitations
- Communication matrices grow stale fast: stakeholders change, projects pivot, channels get deprecated. Without a refresh cadence, the doc lies.
- "Frequency × stakeholder × channel" combinatorial blowup: 20 stakeholders × 5 channels = 100 cells most of which are empty noise.
- LLM-generated status reports default to optimism (everything "on track") because pessimistic phrasing is rarer in training data; honesty must be enforced.
- Meeting templates without an enforced agenda owner devolve into status-theatre meetings.
- Escalation paths look clean on paper but break in practice when first-contact is unavailable or out of office; backup paths missing.
- "Push vs pull" framing ignores the real problem: people read 5% of pushed comms and 0% of pulled comms; the methodology lacks engagement metrics.
- Text-channel selection (email vs Slack) is culture-dependent; one-size-fits-all rules cause friction.

## Agentic workflow
The agent generates and maintains the communication artefacts and audits live behaviour. (1) Plan-builder: from stakeholder register → comms matrix + meeting schedule + escalation path. (2) Status-reporter: pulls metrics (sprint velocity, risk count, EVM CPI/SPI) and assembles weekly status report; routes per matrix. (3) Meeting-secretary: ingests transcript / notes, emits decisions log + action items with owners and due dates; pushes to issue tracker. (4) Comms-auditor: scans Slack/email/meeting analytics monthly to flag drift (meeting bloat, missing owners, undocumented decisions). Humans approve narrative, sensitivity calls, and escalation triggers.

### Recommended subagents
- `comms-plan-builder` — input: stakeholder register, output: matrix + meeting cadence + channel rules + escalation path.
- `status-reporter` — input: project metrics + last week's report, output: this-week's status with delta + risks.
- `meeting-secretary` — input: transcript/notes, output: decisions, actions (owner, due, status), open questions.
- `comms-auditor` — input: meeting calendar + Slack stats + email volume, output: anti-pattern flags (meeting overload, missing decision logs, single-point owners).
- `escalation-router` — input: issue + impact + first contact, output: who to notify next + by when.

### Prompt pattern
```
Status report (push channel):
Inputs:
- last_report: <prev week markdown>
- metrics: {sprint_velocity, planned, completed, cpi, spi,
            risk_count_high, blocker_count, scope_changes_open}
- raw_events: [...] (commits, deploys, decisions, escalations)

Output JSON:
{ "headline_status": "green|yellow|red",
  "headline_one_liner": "...",
  "this_week": ["..."],
  "next_week": ["..."],
  "risks_top3": [{name,impact,mitigation,owner}],
  "decisions_needed": [{question,owner,by_date}],
  "metrics_delta": {...} }

Rules:
- Headline must reflect worst metric, not average.
- Reject empty risks list if risk register is non-empty.
- Cite commit / issue IDs as evidence; refuse vague "made progress".
- Length cap 400 words; humans skim.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `slack-cli` (`slacky`) | Post status updates programmatically | https://github.com/slackapi/slack-cli |
| `gh issue` / `gh pr` | Pull commit/PR/issue activity for status | https://cli.github.com/ |
| `jira-cli` | Pull sprint metrics for status | https://github.com/ankitpokhrel/jira-cli |
| `pandoc` | Render status MD → PDF / DOCX for execs | https://pandoc.org/ |
| `mailx` / `msmtp` | Email status from CI | https://marlam.de/msmtp/ |
| `whisper.cpp` / `whisperx` | Transcribe meeting recordings locally | https://github.com/ggerganov/whisper.cpp |
| `meeting-bot` (Read.ai, Otter, Fathom) | Auto-transcribe + summarise meetings | https://www.read.ai/ |
| `mermaid-cli` | Render escalation flowcharts | https://github.com/mermaid-js/mermaid-cli |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Slack | SaaS | Yes — REST + Bolt SDK | Push channel; Workflow Builder for forms |
| Microsoft Teams | SaaS | Yes — Graph API | Enterprise default |
| Email (SES, Postmark, Resend) | SaaS | Yes — REST | Status emails to formal stakeholders |
| Confluence / Notion | SaaS | Yes — REST | Pull channel; meeting notes home |
| Loom / Tella | SaaS | Yes — REST | Async video updates |
| Read.ai / Otter / Fathom | SaaS | Yes — REST | Meeting transcription + summary |
| Linear / Jira | SaaS | Yes — REST | Action item tracking |
| Geekbot / Range | SaaS | Yes — REST | Async standup automation |
| Status hero / Status.team | SaaS | Yes — REST | Project status dashboards |
| PagerDuty / OpsGenie | SaaS | Yes — REST | Escalation routing for incidents |

## Templates & scripts
See `templates.md` for the full plan + status report + meeting notes. Action-extractor (~25 lines):

```python
import re
ACTION_RE = re.compile(
    r"(?:^|\n)\s*(?:[-*]\s*)?\[\s*[\sx]\s*\]\s*(?P<text>.+?)"
    r"(?:\s+@(?P<owner>\w[\w.-]*))?"
    r"(?:\s+(?:by|due)\s+(?P<due>\d{4}-\d{2}-\d{2}))?\s*$",
    re.IGNORECASE | re.MULTILINE)
def extract(notes):
    out = []
    for m in ACTION_RE.finditer(notes):
        out.append({"text": m["text"].strip(),
                    "owner": m["owner"],
                    "due": m["due"],
                    "complete": False})
    return [a for a in out if a["text"]]
```

## Best practices
- Headline-first: every status starts with R/Y/G + one sentence; details below for skimmers.
- Default to async: writing > meeting unless the topic is decision-shaped or ambiguous; meetings are expensive synchronisation.
- Every meeting has an agenda 24h before, an owner, decisions logged, and action items with owner + due date — or it gets cancelled.
- Match channel to message: urgent = call, complex = meeting, status = report, FYI = chat, reference = wiki, formal = email.
- Send status reports on the same day/time every week; predictability builds the ritual.
- Document decisions in a single decision log (ADR-style for tech, lightweight for biz). "Where was this decided?" is a smell.
- Escalation paths must include backup contacts and out-of-office routing; otherwise they fail at the worst time.
- Metric every 4-6 weeks: meeting hours per person, status report read-rate (email open / Slack reactions), action item closure rate. Cull what isn't read.

## AI-agent gotchas
- LLM status reports default to optimism — "good progress, all on track". Force the agent to cite metrics or refuse.
- Action items without owner/due date pile up; require both fields or the agent rejects the meeting note.
- Decision summaries lose dissent: agents collapse "we considered X but chose Y because Z" into "we chose Y". Preserve dissent and rationale.
- Channel auto-routing: agents will email everyone for everything. Route by stakeholder preference recorded in the matrix.
- PII / commercial-in-confidence content leaks via meeting transcripts; run a redactor before posting summaries to broad channels.
- Time-zone confusion: status sent at "9 AM" varies by region; pin UTC + local in scheduled comms.
- Escalation hallucination: agents invent contact names not in the register. Require explicit `escalation.yaml` lookup.
- Status repetition: agents repeat last week's content if metrics didn't change; force them to surface delta or report "no change" explicitly.

## References
- PMI PMBOK Guide 6th Ed., Chapter 10 — Project Communications Management.
- Cal Newport, *A World Without Email* (2021) — async-default culture.
- Atlassian Team Playbook — meeting & status patterns (https://www.atlassian.com/team-playbook).
- "The Art of Meeting Architecture" — Maarten Vanneste.
- Kim Scott, *Radical Candor* — status honesty.
- ISO 21502:2020 — communication competence in project management.
- "Decisions, Decisions" — DACI / RAPID frameworks for decision communication.
