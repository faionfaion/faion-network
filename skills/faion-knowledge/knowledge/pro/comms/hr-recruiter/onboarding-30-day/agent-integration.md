# Agent Integration — 30-Day Onboarding Phase

## When to use
- Generating role-specific 30-day plans (engineer, sales, support, etc.) from an existing universal template + role competency model.
- Producing pre-boarding and Day 1 packets: welcome email, equipment checklist, first-week calendar invites, links to required docs.
- Tracking onboarding completion across new hires via HRIS / LMS APIs and surfacing "behind plan" cases to managers.
- Drafting personalized check-in agendas (Day 7, 14, 30) for managers and buddies based on hire's progress.
- Synthesizing 30-day survey responses across cohorts to identify systemic onboarding issues and propose template improvements.

## When NOT to use
- Companies under 20 employees where onboarding is bespoke per hire — the agent's structure becomes overhead.
- Senior executives (VP/CXO) — their onboarding is high-touch, stakeholder-mapping driven, and template-resistant.
- Contract / contingent workers with <30 day engagements — the universal plan exceeds their tenure.
- Companies in an active reorg / RIF — onboarding plans constructed during chaos give false structure; pause and resume after stabilization.

## Where it fails / limitations
- LLMs cargo-cult generic onboarding tasks ("review company values", "set up 1:1s") that don't reflect actual workflow tools or team structure; without ingesting team-specific runbooks, output is generic.
- Calendar invites for week 1 require timezone awareness and conflict checking; agents auto-scheduling without read access to calendars produce overlapping events.
- Privacy: onboarding plans surface manager names, team rosters, project codenames — must respect access controls.
- Buddy assignments require matching availability, seniority, and personality; agents using only org-chart data produce mismatched pairs.
- Cultural variance: onboarding norms in DE/JP/UA/US differ (probation periods, formality, tooling); a single template misfires across geos.
- Feedback collection at Day 7/14/30 fatigues fast if overly long; agents tend to over-engineer surveys.

## Agentic workflow
A new-hire trigger (ATS "Hired" event or HRIS "Started" status) fires the onboarding agent. It pulls the role's universal 30-day template + team-specific addendum, customizes per hire (manager name, buddy, pre-assigned project), creates Notion/Confluence onboarding doc, schedules calendar invites for week 1, and posts a Slack DM thread with Day 1 checklist. A scheduled agent runs daily to check progress (LMS completion, 1:1 attendance) and flags lag to the manager. Day 7/14/30 check-in agents send a short survey, summarize results, and prep talking points for the manager 1:1.

### Recommended subagents
- `faion-onboarding-agent` (referenced in README) — primary orchestrator.
- `faion-recruiter-agent` — handoff from offer-accepted to pre-boarding.
- A custom `lms-tracker` agent (sonnet, scheduled daily) — pulls completion data, posts Slack alert if stale.
- `faion-improver` — quarterly template improvement from cohort feedback.
- `faion-sdd-execution` — for technical-role onboarding tasks (dev env, first PR).

### Prompt pattern
```
Generate 30-day onboarding plan for <role> at <team>. Inputs:
- universal template (this methodology)
- team runbook <runbook.md>
- manager <name>, buddy <name>
- start date <YYYY-MM-DD>, timezone <tz>
Customize: replace generic placeholders with actual links, names,
project codenames. Add 5 role-specific learning tasks. Create week 1
calendar block list (no overlaps, working hours only).
Output: onboarding-doc.md + calendar.ics.
```

```
Day 7 check-in for <new_hire>. Pull from <slack-activity> + <lms-status>
+ <git-activity>. Draft a 30-min 1:1 agenda with manager. Highlight:
- completed items
- blocked items + suspected cause
- suggested probing questions
- escalation flags (if behind plan).
≤200 words. No corporate jargon.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` CLI | Provision repo access for engineers | https://cli.github.com |
| `op` | Pull HRIS / LMS API tokens | https://developer.1password.com/docs/cli |
| `icalendar` Python lib | Generate `.ics` calendar invites | `pip install icalendar` |
| `pandoc` | Convert onboarding doc MD → DOCX/PDF for offline | OS package |
| `jq` | Parse HRIS/LMS API responses | OS package |
| `slack-cli` / `slack-sdk` | Post Day 1 thread, schedule reminders | `pip install slack-sdk` |
| `csvkit` | Cohort survey analysis | `pip install csvkit` |
| `notion-sdk-py` / Confluence API | Create onboarding pages programmatically | `pip install notion-client` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| BambooHR / Rippling / Workday | SaaS HRIS | Yes | Onboarding workflows, document signing via API. |
| Sapling (Kallidus) / Hibob | SaaS | Yes | Dedicated onboarding modules; webhook events. |
| WorkBright | SaaS | Yes | I-9 / forms automation. |
| Lessonly / 360Learning / WorkRamp | SaaS LMS | Yes | Course completion APIs. |
| Notion / Confluence / Slite | SaaS | Yes | Onboarding doc hub; agent generates from template. |
| 15Five / Lattice / Culture Amp | SaaS | Yes | Check-in surveys, automated cadence. |
| Asana / Monday / Trello | SaaS | Yes | Day 1–30 task boards. |
| Donut (Slack app) | SaaS | Partial | Buddy matching; agent triggers but matching is opaque. |
| Microsoft Viva Learning | SaaS | Yes | Compliance + role training in Teams. |
| Okta / Azure AD | SaaS IdP | Partial | Provision SSO + group memberships; high-permission ops require human approval. |

## Templates & scripts
See `templates.md` for universal 30-day plan, role-specific examples, and check-in schedule. Inline new-hire bootstrap script:

```bash
#!/usr/bin/env bash
# bootstrap-newhire.sh - run on offer-accepted webhook
set -euo pipefail
NAME="${1:?name}"; ROLE="${2:?role}"; START="${3:?YYYY-MM-DD}"; MGR="${4:?manager}"
SLUG=$(echo "$NAME" | tr '[:upper:] ' '[:lower:]-')
mkdir -p "onboarding/$SLUG"
claude -p "Generate 30-day plan for $NAME ($ROLE) starting $START, manager $MGR. \
  Use methodology template; output Markdown." > "onboarding/$SLUG/plan.md"
gh issue create --title "Onboarding: $NAME ($ROLE)" \
  --label "onboarding" --assignee "$MGR" \
  --body-file "onboarding/$SLUG/plan.md"
echo "Created onboarding/$SLUG/plan.md and GH issue"
```

## Best practices
- Pre-boarding (offer-accepted → start date) is when 20% of new hires churn; build a 2-week pre-start touchpoint cadence.
- Day 1: working laptop, accounts, lunch with team, NO heavy training — first impressions stick.
- Document onboarding in the same place new hires will work daily (Notion/Confluence), not in HR-only tools.
- Buddy ≠ manager; pick a peer who started 6–12 months ago and remembers the pain points.
- Set ONE meaningful Day 30 milestone (first PR, first sales call, first ticket resolved); avoids "completed all training" theater.
- Survey at Day 14 and Day 30 with ≤5 questions; long surveys get <40% response.
- Capture systemic issues across cohorts; one new hire's complaint is anecdote, three is a pattern.

## AI-agent gotchas
- Generic-task injection: "review company values" without pointing to a specific page is busywork; force template links to existing docs or fail loudly if missing.
- Calendar conflicts: agents auto-schedule without reading existing calendars produce double-bookings; always check `freebusy` before invite.
- Buddy matching: don't autoassign; surface 3 candidates and let the manager pick.
- Surveys via agent risk fatigue; agent must rate-limit and not send if previous survey unanswered.
- Privacy: onboarding plans contain manager-only info (project codenames, customer lists); agents must enforce visibility boundaries.
- Localization: US "celebrate Day 1" energy lands awkwardly in DE/JP/UA contexts; tone-adapt per locale.
- Human-in-loop checkpoint: any provisioning step (SSO group, repo write access, payroll); agents draft requests, humans approve.
- Data residency: HRIS data crossing borders into agent prompts may violate GDPR / data-protection rules; check before sending personal data to LLM.
- Stale templates: agents reuse last quarter's links / Slack channels that were archived; build a "link health check" pre-pass.
- Agents over-promise on Day 30 milestones; calibrate against actual median ramp from cohort data, not aspirational goals.

## References
- Michael Watkins, "The First 90 Days"
- SHRM: "Onboarding New Employees: Maximizing Success" — https://www.shrm.org/topics-tools/tools/toolkits/onboarding-new-employees
- Gallup: "The Power of Great Onboarding"
- Brandon Hall Group onboarding research
- BambooHR Onboarding Guide: https://www.bamboohr.com/resources/guides/onboarding
- Workable 30-60-90 Day Plan: https://resources.workable.com/tutorial/30-60-90-day-plan
- Bauer & Erdogan, "Organizational Socialization" (research synthesis)
- Buffer, GitLab, HashiCorp public onboarding handbooks (open patterns)
