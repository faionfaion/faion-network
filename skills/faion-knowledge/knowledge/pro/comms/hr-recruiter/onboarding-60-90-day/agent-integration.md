# Agent Integration — 60-90 Day Onboarding Phases

## When to use
- A hire has cleared the 30-day learning phase and needs explicit Contribute (31-60) + Execute (61-90) milestones.
- Manager wants a structured second-and-third-month plan separate from the broad 30-60-90 framework.
- Performance review at day 90 must be defensible — phases give the artifact trail (project completion, mentorship, autonomy).
- Internal mobility: the first 30 days were about context, the next 60 about delivery against the new role.
- Sales / CS / engineering roles where ramp quotas or feature ownership land in this exact window.

## When NOT to use
- Hire is still failing day-30 criteria; resolve that first or restart the cycle.
- Roles with multi-quarter ramps (Enterprise AE, surgeon, ML researcher) — extend phases, do not compress.
- Highly autonomous senior hires who define their own deliverables; impose only on entry-level/mid roles.
- Contract/agency placements under 60 days.

## Where it fails / limitations
- "Contributing" defined as activity (meetings attended, PRs opened) rather than outcome (project shipped, deal closed) gives false-positive reviews.
- Generic milestones identical across roles ignore that a Sales 60-day milestone (50% pipeline) is fundamentally unlike an SE one (feature delivered).
- Skipping the day-45 skip-level check leaves the manager as the only signal source — biased and noisy.
- Mentorship asks at day-90 ("help onboard newer hires") fail when there are no newer hires; remove the milestone instead of fudging it.
- The framework assumes a 3-month review cadence. Quarterly hiring spikes break the calendar; plans drift to "whenever".

## Agentic workflow
Use a Claude subagent to monitor weekly 1:1 notes and project tracker updates against the day-31-90 milestones, producing a delta report each Friday and a draft day-60 / day-90 review packet. The agent is most useful at week 5-6 (where slip starts) and week 11 (where review prep starts). The agent does not decide ramp pass/fail — it surfaces evidence and gaps; the manager rules.

### Recommended subagents
- `faion-sdd-executor-agent` — model the 60-90 plan as an SDD task list with quality gates per milestone.
- `nero-sdd-executor-agent` — for internal NERO hires; ties review packets into the mesh's `notifications/` queue.
- Custom `hr-review-agent` (suggested) — sonnet for review summaries and gap analysis; opus only when calibrating across hires; haiku for HRIS field updates.

### Prompt pattern
```
Compare hire X's last 4 weekly 1:1 notes and Linear activity against the
days 31-60 milestones in <plan>. Output: status per milestone (on-track /
slipping / blocked), top 3 risks with cited evidence, recommended day-60
review focus.
```

```
Draft a day-60 review packet: completed milestones with artifacts, partial
milestones with reasons, manager prompts (3 questions), proposed day-90
goals. Cite source lines for every claim.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Pull PR/issue activity for engineering ramps | https://cli.github.com/ |
| `linear-cli` | Read milestone/project status | https://linear.app/docs |
| `slack-cli` | Pull thread context from project channels | https://api.slack.com/automation/cli |
| `pandoc` | Generate review packet PDF | https://pandoc.org/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Lattice | SaaS | Yes (API) | Native 60/90 review templates |
| 15Five | SaaS | Yes (API) | Weekly check-ins → milestone status |
| Culture Amp | SaaS | Yes (API) | Onboarding satisfaction survey at day 90 |
| BambooHR | SaaS | Yes (API) | Stores plan + review outcomes |
| Officevibe / TINYpulse | SaaS | Yes (API) | Pulse signals between formal reviews |
| Notion / Coda | SaaS | Yes (API) | Free-form plan host with database fields |

## Templates & scripts
See `templates.md` and `examples.md` for role-specific 60-90 milestones (engineer, sales rep, marketer). Inline weekly delta script:

```bash
#!/usr/bin/env bash
# weekly-delta.sh — diff this week's commits/issues against milestone list.
# Requires gh + jq + plan.yaml with milestones[].id, .due_week, .verifier
set -euo pipefail
WEEK=$1; PLAN=plan.yaml
gh issue list --assignee "@me" --state all --json number,title,closedAt \
  --jq ".[] | select(.closedAt | startswith(\"$WEEK\"))" > closed.json
yq '.milestones[] | select(.due_week == "'"$WEEK"'")' "$PLAN" > due.yaml
echo "## Week $WEEK delta" 
echo "### Closed"; jq -r '.title' closed.json
echo "### Due"; yq '.id' due.yaml
```

## Best practices
- Re-baseline at the day-30 review: confirm 60-day milestones still match team reality before phase 2 starts.
- Make day-45 a skip-level: the hire's manager has been the only voice; the skip-level catches blind spots.
- Use one verification artifact per milestone: PR merged, deal closed, doc published, demo recorded — never "self-report".
- Allow milestone swaps (not slips): if a project was deprioritized, swap to an equivalent-scope replacement and document why.
- Day-90 review covers next-quarter goals, not just the past 60 days; otherwise the hire enters Q2 with no plan.
- For sales roles, ramp quota at 50-75% of full quota for days 61-90; reset to 100% only at day 91.

## AI-agent gotchas
- Agents conflate "active in meetings" with "contributing"; force the prompt to distinguish presence from outcome.
- Sentiment in 1:1 notes is often muted by the manager; do not let the agent infer "happy" from absence of complaints.
- Sales pipeline data is noisy in the first 60 days (deals not yet stage-correct); cap the agent's confidence on conversion-style metrics.
- LLMs over-recommend mentorship milestones at day 90; only include if there is a confirmed newer hire to mentor.
- Cross-tenant leakage: never mix two hires' contexts in one prompt; per-hire run only.
- 90-day surveys must be optional and anonymous; do not pipe NPS-style scores back into the plan as performance data.
- Agents produce kindly-worded gap reports. For underperformance, surface verbatim manager quotes instead of paraphrase.

## References
- Michael D. Watkins, *The First 90 Days*, HBR Press.
- SHRM, "Performance Management Best Practices" — https://www.shrm.org/
- Indeed Hiring Lab, "90-Day Review Guide" — https://www.indeed.com/hire/c/info/90-day-review
- Gallup, "The Manager–Employee Check-In" — https://www.gallup.com/workplace/
- Lattice, "Designing the 90-Day Review" — https://lattice.com/library
