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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-outsource-onboarding-one-pager-template.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[freelancer-personal-crm-minimal]]
- [[indie-hacker-tax-and-legal-essentials]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
