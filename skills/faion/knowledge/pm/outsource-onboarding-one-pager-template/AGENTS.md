# Outsource Onboarding One-Pager Template

## Summary

**One-sentence:** One-page contractor onboarding template: scope, deliverables, comms cadence, access list, kill-switch — get a hire shipping in 24 hrs.

**One-paragraph:** Pins the contractor onboarding artefact: one page, six named sections (scope / deliverables / comms cadence / access list / payment / kill-switch). Output is a versioned spec the contractor signs before first day; same template reused per hire, evolved per learning.

**Ефективно для:**

- Solo founder hiring contractor #1-5 who keeps spending the first week answering 'how do I…' messages. One page that turns 'first day' into 'first deliverable in 24 hrs'.

## Applies If (ALL must hold)

- Onboarding a contractor / freelancer / async hire
- Hire is part-time (≤30 hrs/week) and remote
- Engagement length ≥2 weeks

## Skip If (ANY kills it)

- Full-time employee — needs full HR onboarding instead
- One-off task <8 hrs total
- Hire already onboarded in prior engagement

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Signed contractor agreement (with NDA + IP clause) | doc | lawyer-reviewed template |
| Scope brief (problem, success criteria, constraints) | doc | founder |
| Tool stack list (repos, design files, channels) | table | stack inventory |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/project-manager/freelancer-personal-crm-minimal` | Peer methodology — onboarded contractor enters the CRM as 'active'. |
| `solo/pm/indie-hacker-tax-and-legal-essentials` | Peer methodology — contract + NDA pattern lives there. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules incl. skip-this-methodology + run-the-checklist | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-outsource-onboarding-one-pager-template` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-outsource-onboarding-one-pager-template` | haiku | Schema check + threshold checks; deterministic. |
| `review-outsource-onboarding-one-pager-template` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/outsource-onboarding-one-pager-template.json` | JSON skeleton conforming to the output contract schema. |
| `templates/outsource-onboarding-one-pager-template.md` | Markdown skeleton for human-readable artefact rendering. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-outsource-onboarding-one-pager-template.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[freelancer-personal-crm-minimal]]
- [[indie-hacker-tax-and-legal-essentials]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/outsource-onboarding-one-pager-template.json`

```json
{
  "artefact_id": "onboard-contractor-x-2026-w22",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "contractor": {
    "name": "designer-x",
    "agreement_signed": "2026-05-22"
  },
  "scope": "Lead designer for /pricing redesign + /home hero refresh; output Figma files + production-ready assets.",
  "deliverables": [
    {
      "id": "d1",
      "what": "/pricing v1 wireframe",
      "due_in_hours": 24
    },
    {
      "id": "d2",
      "what": "/pricing final mocks",
      "due_in_hours": 168
    }
  ],
  "comms_cadence": {
    "daily_standup": "#daily-standup by 11:00",
    "weekly_call": "Friday 14:00 30min"
  },
  "access_list": [
    {
      "tool": "figma",
      "level": "edit"
    },
    {
      "tool": "slack",
      "level": "guest"
    },
    {
      "tool": "github",
      "level": "read"
    }
  ],
  "payment_terms": {
    "rate": 80,
    "currency": "EUR",
    "cycle": "biweekly",
    "via": "wise"
  },
  "kill_switch": {
    "trial_period_weeks": 2,
    "criterion": "first 2 deliverables on time AND figma fidelity",
    "exit_pay_days": 14
  },
  "owner": "@ruslan"
}
```
