# Agent Integration — Onboarding

How to drive the onboarding bundle (preboarding, day-one, 30-day, 60-90 day, buddy program, manager guide, feedback loop, remote onboarding) with Claude subagents and HRIS / collab tooling. Pairs with `README.md`, `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.

## When to use

- Standing up a repeatable onboarding program for the first time, or replacing a tribal-knowledge handoff.
- Hiring at a velocity (>= 1 hire / week) where ad-hoc onboarding is producing inconsistent ramp.
- Rolling out remote-first onboarding where Day-1 in-office rituals do not translate.
- After a 90-day-retention dip or new-hire eNPS drop — needs a refresh on the program, not just on managers.
- M&A integrations where two onboarding cultures need to merge into one without homogenizing.

## When NOT to use

- Hires of 1-2 per year — write a checklist, do not build a program; the maintenance burden won't pay back.
- C-suite / executive onboarding — bespoke, board-driven, doesn't fit a framework.
- Contractor / agency placements with < 90 days expected tenure — focus on access provisioning + safety, skip culture.
- Crisis backfills where the new hire is replacing a critical departure — onboarding is collapsed into knowledge transfer; treat separately.

## Where it fails / limitations

- 30-60-90 plans default to "learn / contribute / execute" but the verbs are too generic to gate progress.
- Buddy programs degrade silently when buddies stop checking in; agents can monitor but can't repair the relationship.
- Documentation-as-onboarding fails — new hires don't read it; an agent piping docs is a worse experience, not better.
- Cultural transmission resists templating: values, unwritten rules, "how we disagree", "when to escalate" are invisible to a checklist.
- Compliance training overload (security, harassment, GDPR, SOC 2) crowds out role learning in week 1; agents that schedule everything to Day 1 destroy the experience.
- Auto-generated 30-60-90 goals miss the manager's real expectations and become aspirational fiction.

## Agentic workflow

Drive onboarding as a six-stage pipeline owned by a `faion-onboarding-agent` (specialization of `faion-recruiter-agent`). Stage 1 (preboarding, sonnet) — between offer-acceptance and Day 1: equipment ticket, account provisioning kickoff, welcome packet, schedule generation. Stage 2 (Day 1 plan, sonnet) — generates a personalized agenda from the role + manager preferences. Stage 3 (30-60-90 draft, opus) — combines the JD, level expectations, and team's current quarter goals into a *draft* plan; manager edits before sending. Stage 4 (cadence reminders, haiku) — nudges manager + buddy + new hire on milestone check-ins. Stage 5 (feedback collection, sonnet) — runs week-1 pulse, day-30, day-60, day-90 surveys; codes free-text. Stage 6 (program-level analytics, opus) — quarterly cohort review, attrition, ramp metrics. Mandatory human-in-loop on every plan personalization and survey deployment.

### Recommended subagents

- `faion-onboarding-agent` — primary, owns the full lifecycle.
- `faion-recruiter-agent` — handoff at offer-acceptance; passes candidate context.
- `faion-employer-brand-agent` — drafts welcome content consistent with EVP.
- `general-purpose` reviewer (sonnet) — tone check on welcome / Day-1 communications, especially across language and culture.

### Prompt pattern

30-60-90 draft:
```
You are drafting a 30-60-90 plan per skills/faion/knowledge/pro/comms/hr-recruiter/onboarding/README.md.
Role: <title>, level: <IC3/M1/...>. Team's current quarter OKRs: <pasted>. Manager's stated success criteria for this hire (3 bullets): <pasted>. Hire's relevant background: <pasted>.
Output: 3 phases × 3 sections (learn / build / deliver). Each goal must be observable, time-bound to the phase, and tied to either an OKR, an artefact, or a relationship. No verbs like "understand" or "be familiar with". Mark each goal "M" (manager-set) so manager can edit before sending.
```

Day-90 retrospective:
```
Inputs: week-1 pulse, day-30 survey, day-60 check-in notes, day-90 survey, manager's 90-day review notes (attached). Produce: (1) themes by sentiment, (2) hire-stated blockers and which were resolved, (3) manager-stated competence ramp delta, (4) program-improvement recommendations applicable to next cohort. Quote verbatim. Do not infer manager opinions from hire surveys.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Version-control onboarding kits | cli.github.com |
| BambooHR API | HRIS data + onboarding tasks | documentation.bamboohr.com/reference |
| Rippling API | Equipment, accounts, and HRIS unified | developer.rippling.com |
| Workday Studio / REST | Enterprise HRIS, complex but agent-drivable | community.workday.com |
| Okta / Azure AD CLI | SSO/account provisioning | developer.okta.com |
| Jamf / Kandji / Mosyle | MDM for laptop preboarding | developer.jamf.com |
| Slack API + workflow builder | Buddy DMs, pulse polls | api.slack.com |
| Notion / Coda API | Living onboarding playbook + 30-60-90 plans | developers.notion.com |
| `pandas` + `pyreadstat` | Survey analysis | pypi |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| BambooHR | SaaS HRIS | Yes (REST) | SMB default; onboarding tasks are first-class. |
| Rippling | SaaS HRIS+IT+Finance | Yes (REST) | Best end-to-end provisioning for agents. |
| HiBob | SaaS HRIS | Yes (REST) | Strong onboarding workflows; clean API. |
| Sapling / Kallidus Sapling | SaaS | Yes (REST) | Onboarding-specialist; webhook-rich. |
| WorkBright | SaaS | Yes (REST) | Strong on I-9 / paperwork compliance. |
| Workday | SaaS HRIS (enterprise) | Partial | Heavy auth, rate limits. |
| Lattice / 15Five | SaaS | Yes (REST) | 30-60-90 + check-ins built-in. |
| Donut (Slack app) | SaaS | Yes (Slack workflow) | Buddy pairing automation. |
| Loom | SaaS | Yes (REST) | Async culture and welcome videos. |
| Notion / Confluence | SaaS | Yes (REST) | New-hire wiki, often the de-facto onboarding hub. |
| Okta / Azure AD / JumpCloud | SaaS IDP | Yes (REST/SCIM) | Provisioning automation. |
| Jamf / Kandji | SaaS MDM | Yes (REST) | Pre-shipped, zero-touch laptops. |
| Greenhouse Onboarding | SaaS | Yes (REST) | Bridges ATS → onboarding without re-keying. |

## Templates & scripts

See `templates.md` for: 30-day plan template, day-1 agenda, manager guide, buddy guide, surveys. Worked examples in `examples.md` and `onboarding-30-day/`, `onboarding-60-90-day/` sibling methodologies.

Inline helper — preboarding readiness gate (run 5 days before start; block start if anything red):

```python
# preboard_gate.py — verify readiness before Day 1
import sys, json, datetime as dt

CHECKS = [
    ("offer_signed",         lambda d: d.get("offer_signed_at")),
    ("equipment_shipped",    lambda d: d.get("equipment_tracking")),
    ("accounts_provisioned", lambda d: d.get("okta_user") and d.get("email")),
    ("manager_assigned",     lambda d: d.get("manager_id")),
    ("buddy_assigned",       lambda d: d.get("buddy_id")),
    ("day1_scheduled",       lambda d: d.get("calendar_url")),
    ("welcome_email_sent",   lambda d: d.get("welcome_sent_at")),
]

def gate(d):
    start = dt.date.fromisoformat(d["start_date"])
    days_left = (start - dt.date.today()).days
    rows = [{"check": name, "ok": bool(fn(d))} for name, fn in CHECKS]
    blocked = [r["check"] for r in rows if not r["ok"]]
    return {"start_date": d["start_date"], "days_left": days_left,
            "rows": rows, "status": "GREEN" if not blocked else "RED",
            "blocking": blocked}

if __name__ == "__main__":
    json.dump(gate(json.load(sys.stdin)), sys.stdout, indent=2)
```

Pipe HRIS new-hire JSON in. Status RED at T-5 → escalate to People Ops; do not let the agent send the welcome email until GREEN.

## Best practices

- Move every compliance / paperwork task to preboarding. Day 1 is for human connection, not e-signatures.
- Manager + buddy are the only two roles that materially predict 90-day retention; protect their time, not the program's.
- Buddy must be peer-level, not the manager's chosen favorite — different reporting line, similar seniority.
- 30-60-90 goals must be observable artefacts: shipped feature, written doc, signed-off review, customer call. Never "be familiar with...".
- Survey at week 1 (4 questions max), day 30, day 60, day 90; rising attrition shows up in week-1 pulse first.
- Do not announce "the official end of onboarding" at day 90. Real onboarding ends at the first time the new hire teaches someone else.
- For remote: ship laptop pre-imaged; default Day 1 to async + one 90-min synchronous welcome; avoid back-to-back video.
- Compliance training: spread across days 5-30, not Day 1. Track completion, not score-as-evidence-of-learning.
- Localize day-1 logistics (timezone, holidays, language) — global default templates produce poor experiences in non-HQ regions.

## AI-agent gotchas

- Agents will generate 30-60-90 goals from the JD without team OKRs — the plan looks coherent but is disconnected from real work.
- LLM tone in welcome emails over-uses corporate uplift language; force a manager pre-send review.
- "Personalization" by an agent often means inserting the candidate's name 6 times; not personalization. Pull from intake form for genuine personalization (preferred name, pronouns, language).
- Pulse-survey free-text analysis from agents systematically under-weights minority concerns (small N gets summarized away). Always show raw quotes alongside themes.
- Auto-DMs from a "buddy bot" replace, not augment, the buddy. Block; the buddy is the human relationship, not a Slack workflow.
- Calendar-conflict detection: agents will book Day 1 over team standups. Always read the team calendar first.
- Compliance content is jurisdiction-specific (US harassment training is not EU GDPR training). Agents that auto-bundle modules without locale checks create legal exposure.
- Mandatory human-in-loop: (1) every 30-60-90 plan before sharing with hire, (2) any survey question added to a recurring template, (3) any HRIS-mutating action, (4) buddy + manager assignment.

## References

- SHRM — "Onboarding New Employees" toolkit (shrm.org).
- BambooHR — "The Definitive Guide to Onboarding".
- Bauer, T. — "Onboarding New Employees: Maximizing Success" (SHRM Foundation).
- Gallup — "State of the American Workplace" (drivers of new-hire engagement).
- HBR — "How to Onboard a New Employee Virtually" (Watkins, 2020).
- Internal: `skills/faion/knowledge/pro/comms/hr-recruiter/recruiting-process/agent-integration.md`.
- Internal: `skills/faion/knowledge/pro/comms/hr-recruiter/recruitment-funnel-optimization/agent-integration.md` (90-day retention as funnel terminal).
- Internal: `skills/faion/knowledge/pro/comms/hr-recruiter/retention-compliance/agent-integration.md`.
