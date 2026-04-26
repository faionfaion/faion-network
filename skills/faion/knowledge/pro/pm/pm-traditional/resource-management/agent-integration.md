# Agent Integration — Resource Management (PMBoK)

## When to use
- Multi-team programs sharing scarce specialists (security, ML, SRE, designers) where allocation conflicts cause schedule slips.
- Agency / consulting environments billing by utilization with hard hourly budgets.
- Programs spanning external contractors with rate cards, MSAs, and statement-of-work linkage to deliverables.
- Capacity planning across quarters when demand forecasts must align with hiring and contractor pipelines.
- Workforce planning during reorgs or post-merger integration where role mapping is non-trivial.
- Pair with `procurement-management/`, `cost-estimation/`, `scope-management/`, `schedule-development/`, `risk-management/`.

## When NOT to use
- Stable single-team product squad with one tech lead doing capacity by feel — kanban WIP limits are sufficient.
- Solopreneurs — calendar blocking covers it; resource matrices waste time.
- Pre-PMF startups optimizing for learning velocity — 100% of one engineer beats 60% of three.
- Pure agile teams with stable sized backlogs — let the team self-organize within a fixed capacity.
- Fixed-bid contracts where resource visibility is internal-only and not a deliverable.

## Where it fails / limitations
- Static resource plans go stale within 2-4 weeks; allocation matrices need continuous reconciliation against actuals.
- "100% allocation" is a planning fiction; real available time is 60-70% after meetings, ramp, support, time off.
- Skill matrices assume binary skill presence; reality is gradient (junior → senior, T-shaped, language-specific).
- Resource leveling algorithms optimize for math, not morale — the same person reassigned three times in two months will burn out or quit.
- LLMs proposing reassignments invent skills that people don't have or skip recent calendar conflicts.
- Cross-functional reporting lines (matrix orgs) make "the manager" unclear; allocation requires negotiating with multiple managers per resource.
- Resource leveling collides with critical-chain buffer management; mixing the two creates double counting.
- Privacy/PII risks: skill matrices, performance ratings, and rate cards are sensitive; dumping into a wiki is non-compliant in many jurisdictions.

## Agentic workflow
Resources are a typed `resources/roster.yaml` (one entry per named resource: role, skills with levels, hours per week, calendar URL, manager, cost rate, vacation, location/timezone) plus `resources/allocations.yaml` (resource_id → activity_id → hours per week). A capacity-planning subagent reconciles allocations against schedule and roster, flags overloads, suggests level-loading swaps, and emits a utilization report. A skill-matching subagent reads requirement → suggests candidates from roster with skill-fit scores and current load. Both never auto-assign — they emit recommendations that the resource manager and individuals confirm.

### Recommended subagents
- `faion-sdd-executor-agent` — drives capacity planning as SDD tasks (TASK_roster_baseline, TASK_quarterly_capacity, TASK_skill_matrix_refresh).
- Custom `capacity-planner-agent` (sonnet) — reads schedule + roster + allocations; emits weekly utilization with overload/underload flags and suggested rebalancing.
- Custom `skill-matcher-agent` (sonnet) — given activity skill requirements + roster, ranks candidates by fit, current load, cost, location/timezone overlap.
- Custom `vacation-impact-agent` (sonnet) — computes critical-path impact of planned PTO; flags conflicts before approval.
- Custom `contractor-onboarding-agent` (haiku) — drives the procurement → onboarding → access provisioning checklist for new contractors.
- Custom `attrition-risk-agent` (opus) — combines tenure, role mobility, sentiment signals (anonymous survey deltas, scope churn) to flag retention risk; output is a 1:1 prompt, not a personnel decision.
- `password-scrubber-agent` — runs over roster/allocation files; rate cards and skill ratings are sensitive.

### Prompt pattern
```
You are skill-matcher. Inputs: activity {id, skills_required[{skill, level}],
start, end, hours}, roster.yaml, allocations.yaml.
For each candidate emit STRICT JSON:
{ "resource_id": "...",
  "skill_fit": 0.0-1.0,
  "available_hours": <number>,
  "current_overlap": <hours/wk>,
  "rate": <currency>,
  "tz_overlap_hours": <number>,
  "concerns": ["..."],
  "recommend": "primary|backup|no" }
Rules: do not invent skills. Cap recommendations to top 5.
"primary" requires skill_fit >= 0.8 AND available_hours >= required.
```

Capacity prompt: `Given allocations.yaml + roster.yaml, compute per-resource per-week utilization. Flag any resource at >85% as RED and propose a swap from <70% utilized resources with overlapping skills.`

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + `git log -- resources/` | History of allocation decisions | preinstalled |
| `yq` | Patch roster/allocations YAML | `apt install yq` |
| `jq` | Reduce JSON exports from HRIS / PSA tools | `apt install jq` |
| `pandas` (Python) | Capacity math, pivot by week / role / skill | `pip install pandas` |
| `mermaid-cli` (`mmdc`) | Render Gantt + resource histogram | `npm i -g @mermaid-js/mermaid-cli` |
| `holidays` (pip) | Country-specific public holidays for capacity adjustment | `pip install holidays` |
| `pre-commit` | Block allocation edits without rationale and manager approval reference | https://pre-commit.com |
| `op` (1Password CLI) | Store rate cards out-of-band | https://developer.1password.com/docs/cli |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Float / Resource Guru / Runn | SaaS | REST | Lightweight resource scheduling; agent-friendly APIs. |
| Forecast / Harvest Forecast | SaaS | REST | Capacity planning + time tracking integration. |
| Mosaic / Saviom / Hub Planner | SaaS | REST | Mid-market PSA with skill matrix support. |
| Mavenlink / Kantata / Replicon | SaaS | REST | Enterprise PSA; deep but slow integration. |
| Workday / Oracle HCM / SAP SuccessFactors | SaaS | REST | Authoritative HCM data; integrate read-only. |
| BambooHR / Personio / HiBob | SaaS | REST | SMB HRIS; useful for mid-size programs. |
| Lattice / 15Five / Culture Amp | SaaS | REST | Skill / performance signals (use with consent). |
| Jira Plans / Tempo / Advanced Roadmaps | SaaS | REST | Allocation against Jira capacity in engineering orgs. |
| Microsoft Project / Planner / Loop | SaaS | REST + Graph | Common in regulated enterprises. |
| Calendly / Google Calendar / MS Calendar | SaaS | REST | Real-time availability; required for calibration. |

## Templates & scripts
README provides Resource Plan and Resource Request templates. Inline below: a script that flags resource overloads from `roster.yaml` + `allocations.yaml`.

```python
#!/usr/bin/env python3
"""capacity_check.py — find overloaded resources per ISO week."""
from collections import defaultdict
import sys, yaml, pathlib

def main(roster: str, allocations: str, threshold: float = 0.85) -> int:
    R = {r["id"]: r for r in yaml.safe_load(pathlib.Path(roster).read_text())["resources"]}
    A = yaml.safe_load(pathlib.Path(allocations).read_text())["allocations"]
    load: dict = defaultdict(lambda: defaultdict(float))
    for a in A:
        for week, hours in a["weeks"].items():
            load[a["resource_id"]][week] += hours
    over = []
    for rid, weeks in load.items():
        capacity = R[rid]["hours_per_week"]
        for week, hours in weeks.items():
            ratio = hours / capacity
            if ratio > threshold:
                over.append((rid, week, round(ratio, 2)))
    for rid, week, ratio in sorted(over):
        sys.stdout.write(f"{rid} {week} {ratio*100:.0f}%\n")
    return 1 if over else 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```

## Best practices
- Plan to 70% utilization, not 100%; reserve 30% for meetings, support, learning, and unplanned work.
- Skill matrix entries are dated and self-asserted with peer endorsement; refresh quarterly.
- Cross-train pairs for any single point of failure (one person knowing one critical system → escalate to staffing risk).
- Allocation in git, not spreadsheets — diffs explain "why this changed", spreadsheets erase history.
- Time-zone overlap matters more than raw hours for collaboration-heavy work; surface tz_overlap_hours in matching.
- Vacation calendars are inputs to the schedule, not afterthoughts; lock in PTO before milestone commitments.
- Rate cards live in 1Password / secure store, not in the repo; reference by ID only.
- Use peak-trough leveling: move non-critical-path work into trough weeks.
- Track "ramp time" explicitly — a new joiner is 30-50% productive for 4-8 weeks; under-counting ramp creates the next milestone slip.
- Couple resource decisions to procurement and cost forecasts; a contractor decision affects budget and margin, not just capacity.

## AI-agent gotchas
- Agents over-allocate top performers; force a hard cap at 85% utilization in the prompt and refuse plans that exceed it.
- LLMs invent skills based on title (called "Senior" → assumed expert). Force skill assertions to come from `roster.yaml` only.
- Vacation, holidays, and capacity-impacting events (parental leave, on-call rotation) are routinely missed; explicitly inject these into the prompt.
- Privacy: roster + rate cards are PII / commercially sensitive; require DPA when using third-party LLMs and never auto-publish reports outside the resource-management owner.
- Agents conflate availability with willingness — the calendar may be open, but the person may be over-asked; HITL needed before assignment.
- Resource leveling that ignores morale produces "thrash" reassignments; cap reassignments per resource per quarter.
- Contractor allocation needs procurement linkage; agent must refuse to allocate beyond signed SOW hours.
- Skill matching by embedding similarity is shallow; require explicit skill keys and levels, not free-text matching.
- Auto-replan after every change creates churn; batch capacity replans to a weekly cadence.
- Human-in-the-loop checkpoints (mandatory): adding a new resource, changing an allocation, terminating an engagement, escalating attrition risk, sharing roster outside the immediate program.

## References
- PMI PMBOK 7e — Team Performance Domain.
- PMI PMBOK 6e — Project Resource Management Knowledge Area.
- DeMarco, T. & Lister, T. — "Peopleware" (productivity, environment, attrition).
- Goldratt, E. — "Critical Chain" (resource buffers, multitasking penalty).
- Brooks, F. — "The Mythical Man-Month" (adding people to a late project).
- ISO 21500 / 21502 — resource management guidance.
- Drucker, P. — "Managing Oneself" (utilization vs. effectiveness).
- Sibling methodologies: `procurement-management/`, `cost-estimation/`, `scope-management/`, `schedule-development/`, `risk-management/`.
