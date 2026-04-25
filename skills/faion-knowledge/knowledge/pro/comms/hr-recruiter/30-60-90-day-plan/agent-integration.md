# Agent Integration — 30-60-90 Day Plan

## When to use
- New hire ramp-up plans for any role with measurable deliverables (engineer, sales rep, PM, marketer).
- Internal transfers and promotions where role scope changes substantially.
- Re-orgs where teams or leaders need a structured first quarter against new mandates.
- Interim/fractional executives needing a public artifact for stakeholders by day 30.
- Drafting role-specific milestones during offer/interview close to set explicit expectations.

## When NOT to use
- Hourly/shift roles where competency comes from training scripts, not project ownership.
- Sub-30-day contracts or short bursts where the framework's three-phase cadence does not fit.
- Roles where outcomes depend wholly on team output (use OKRs at team level instead).
- Highly regulated apprenticeships with externally mandated curriculum (medical residency, etc.).

## Where it fails / limitations
- Treating the plan as a checklist instead of a living document; drift after week 2 is the norm without manager re-baselining.
- One-size template across functions: a Sales 90-day differs structurally from an Engineering 90-day (pipeline build vs. code ownership).
- No leading indicators in week 1-2 — managers discover misalignment at the day-30 review when it is already late.
- Confusing learning (days 1-30) with execution (days 61-90); pushing delivery into the learn phase causes early burnout and bad code.
- Plans written by HR alone, without the hiring manager and the new hire collaborating, become checkboxes nobody reads.

## Agentic workflow
A Claude subagent can draft the role-specific 30-60-90 plan from a job description plus a few constraints (team size, tech stack, current goals), then keep it alive by ingesting weekly 1:1 notes and adjusting milestones. The agent is best as a drafting and reconciliation tool: it produces the document, suggests adjustments after each check-in, and flags risk (e.g. "no project owned by day 45" → escalate). Keep humans in the loop for the day-30/60/90 review verdicts — the agent prepares the brief, the manager makes the call.

### Recommended subagents
- `faion-sdd-executor-agent` — generate the plan as an SDD-style spec with phases, success criteria, dependencies; reuse if the plan is treated as a deliverable with quality gates.
- `nero-sdd-executor-agent` — same role inside NERO's mesh when the plan is for an internal hire; logs check-ins to `actions/` and `notifications/`.
- Custom `hr-onboarding-agent` (not yet in repo) — wrap the JD parser, role template selector, and check-in summarizer; use sonnet for plan drafting and review interpretation, opus for cross-role calibration, haiku for HRIS field updates.

### Prompt pattern
```
Given JD <attached>, team context <attached>, and constraints (remote-first,
3 engineers, ship target <feature>), draft a 30-60-90 plan in markdown using
the Watkins phases (learn / contribute / execute). Output: phase tables,
weekly checkpoints, role-specific milestones, success criteria per phase.
Flag any milestone you cannot ground in the JD.
```

```
Here are the day-30 review notes for <hire>. Compare against the plan,
identify gaps, propose 3 revisions to the day-60 milestones with rationale.
Do not invent metrics — cite the relevant 1:1 quotes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Read/write hire onboarding issues, project boards | https://cli.github.com/ |
| `linear-cli` (community) | Sync milestones to Linear projects | https://github.com/linear/linear |
| `notion-cli` (community wrappers) | Push plan into a Notion onboarding hub | https://developers.notion.com/ |
| `pandoc` | Convert plan markdown to PDF/DOCX for offer packet | https://pandoc.org/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| BambooHR | SaaS | Yes (REST API) | Store plan, check-in dates, performance review links |
| Lattice | SaaS | Yes (API + webhooks) | Native 30/60/90 templates and review cycles |
| 15Five | SaaS | Yes (API) | Weekly check-ins map cleanly to plan milestones |
| Notion | SaaS | Yes (API) | Most flexible host; pair with database for status |
| Asana / Monday | SaaS | Yes (API) | Track plan as a project with subtasks |
| HiBob | SaaS | Yes (API) | EU-friendly HRIS with onboarding workflows |

## Templates & scripts
See `templates.md` and `examples.md` in this directory for the universal plan and role-specific variants. Inline helper to derive a draft scaffold from a JD:

```bash
#!/usr/bin/env bash
# draft-30-60-90.sh — given a JD file and role slug, scaffold the plan.
# Usage: ./draft-30-60-90.sh engineer jd.md > plan.md
set -euo pipefail
ROLE=$1; JD=$2
cat <<MD
# 30-60-90 Plan — $ROLE
> Source JD: $JD

## Days 1-30 — Learn
- [ ] Environment + access provisioned (day 1)
- [ ] Shadow 3 cross-functional partners
- [ ] Read top-5 docs flagged by manager
- [ ] Day-30 check-in: write 1-pager observations

## Days 31-60 — Contribute
- [ ] Own first scoped project end-to-end
- [ ] Active in 2 ceremonies/week
- [ ] Day-60 review: deliver project, propose 1 improvement

## Days 61-90 — Execute
- [ ] Independent ownership of medium-scope work
- [ ] Mentor next hire on setup
- [ ] Day-90 review: performance + dev plan
MD
```

## Best practices
- Co-author the plan with the hire on day 1; ownership = adherence.
- Anchor each phase to one outcome the team already cares about (a release, a quota slice, a launch) — avoid synthetic milestones.
- Pair each milestone with a verification artifact (PR, deal, doc, demo) the manager can point to in review.
- Run the day-30 review at day 25 to leave slack for course correction before the formal check.
- Calibrate across hires: pull last quarter's plans into one doc and remove anything that did not predict success.
- Keep the plan in the same tool the team uses daily (Notion/Linear/Asana). Plans in HRIS-only docs go stale.

## AI-agent gotchas
- LLMs hallucinate role-specific milestones if the JD is thin; require the agent to cite the JD line for each milestone or mark it `(synthetic — confirm)`.
- Day-30 reviews need human verdicts. Never auto-issue a "passed/failed" status from the agent; produce a brief, manager decides.
- Plans are sensitive HR artifacts — strip PII (full name, comp, visa status) before sending to any external LLM endpoint; route via the agent's structured output schema.
- Agents drafting for new domains (e.g. clinical roles) without ground truth produce generic plans. Gate behind a domain-template library; refuse if no template matches.
- Check-in summarizers can soften bad signals. Keep direct quotes in the brief; do not let the agent paraphrase risk language.
- Cross-role contamination: feeding an SE plan into the agent and asking for a Sales plan often retains engineering-flavored milestones. Reset context per role.

## References
- Michael D. Watkins, *The First 90 Days*, Harvard Business Review Press, 2013.
- SHRM, "Onboarding New Employees: Maximizing Success" — https://www.shrm.org/topics-tools/tools/toolkits/onboarding-new-employees
- Workable, "30-60-90 Day Plan Template" — https://resources.workable.com/tutorial/30-60-90-day-plan
- Lattice, "How to Build a 30-60-90 Day Plan" — https://lattice.com/library/how-to-write-a-30-60-90-day-plan
- Reforge, "Onboarding for Performance" — https://www.reforge.com/
