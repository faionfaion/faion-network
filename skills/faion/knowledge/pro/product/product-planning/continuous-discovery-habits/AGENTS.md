# Continuous Discovery Habits

## Summary

Teresa Torres' framework: a product trio (PM + Design Lead + Tech Lead) runs weekly customer
touchpoints and maps all signals into an Opportunity Solution Tree (OST). Every node is classified
as outcome, opportunity, solution, or assumption test. Opportunities are scored on reach × frequency
× severity × addressability. Selected opportunities spawn falsifiable assumption tests before any
build. Discovery output traces to delivery via `opp_id` in SDD specs and PR titles.

## Why

Discovery as a one-time project kickoff produces roadmaps that miss user reality within weeks.
A weekly cadence — at least one customer touchpoint per week — keeps the team continuously
calibrated. The OST makes opportunity-to-solution tracing explicit and forces rejection of
solution-shaped feature requests at intake. Without continuous discovery, shipped features
frequently don't move the Outcome, and the team has no structured diagnosis path.

## When To Use

- Active product with paying users where weekly discovery output must convert into roadmap moves
- Quarterly OKR cycle where each Outcome must trace to opportunities, then to assumption tests
- Backlog grooming: rejecting feature requests disguised as solutions and recasting as opportunities
- Roadmap negotiation where the OST provides a defensible structure for "why not feature X"
- Solo/small-team where agents fill discovery gaps by mining tickets, analytics, and sales calls
- Post-launch when shipped features aren't moving the Outcome — to diagnose the broken assumption

## When NOT To Use

- Pre-PMF or zero-user products — no signal volume to support a weekly cadence; use
  customer-development or problem-validation first
- Crisis triage (active outage, churn cliff, security incident) — pause discovery, resume after
- Hardware / regulated medical / enterprise sales with 6–18 month cycles — adapt to monthly windows
- Stakeholder culture demanding validation from a single interview — pick a different framework
- Pure platform/infra teams whose users are other engineers — adapt with DX telemetry instead

## Content

| File | What's inside |
|------|---------------|
| `content/01-ost-model.xml` | OST structure, weekly cadence, scoring model, anti-patterns |
| `content/02-agent-usage.xml` | Planning-lens pipeline, subagent table, prompt pattern, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/ost-schema.json` | OST node schema: type, parent, evidence, score, status, linked specs |
| `templates/spec-opp-link.yml` | GitHub Actions check: blocks PR merge if SDD spec lacks opp_id |
