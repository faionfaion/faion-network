# Contractor Management

## Summary

A four-phase operational framework for managing hired contractors after the contract is signed: onboard with documentation and tool access, establish async communication rhythm (daily/weekly/monthly), assign tasks with explicit scope and examples, and evaluate performance monthly using an SBI-R (Situation-Behavior-Impact-Request) feedback structure.

## Why

Contractors fail silently: without a documented onboarding kit, clear quality standards, and structured feedback, quality drifts and scope creeps — but the manager doesn't discover it until a deadline is missed. Front-loading documentation and structured check-ins reduces rework and miscommunication, which is the primary cost driver in contractor engagements.

## When To Use

- Onboarding a new contractor: build doc pack, provision tooling, schedule check-in cadence
- Aggregating weekly/monthly status across multiple contractors
- Drafting structured SBI-R feedback from observed work output
- Performance evaluation cycles: synthesize a review from logged tasks and quality signals
- Standardizing communication rhythm for an async, multi-timezone contractor roster

## When NOT To Use

- Pre-hire screening and sourcing — use `ops-contractor-basics`
- Conflict resolution or termination conversations — human-only; agents can prep facts but not deliver
- Performance issues that may signal worker misclassification — escalate to legal first
- Managing W-2 employees — different feedback frameworks (1:1s, OKRs, comp reviews)

## Content

| File | What's inside |
|------|---------------|
| `content/01-onboarding-and-rhythm.xml` | Onboarding checklist, essential documentation template, communication rhythm table |
| `content/02-tasks-and-feedback.xml` | Good vs. bad task specification, SBI-R feedback framework, common issues and root causes |
| `content/03-evaluation-and-gotchas.xml` | Contractor evaluation rubric, agentic workflow notes, AI-agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/onboarding-doc.md` | Contractor onboarding document: business context, role, tools, working norms, quality standards |
| `templates/weekly-checkin.md` | Weekly check-in: completed, in-progress, blockers, next-week focus, hours logged |
| `templates/evaluation.md` | Contractor review: 5-area rubric (quality, communication, reliability, speed, proactiveness) + decision |
| `templates/slack-digest.py` | Pull contractor Slack thread history for weekly status digests |
