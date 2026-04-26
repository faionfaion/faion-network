# Learning Speed as Competitive Moat

## Summary

When AI lets anyone clone product features in weeks, the durable competitive advantage is how
quickly an org notices changes, updates its beliefs, and ships different answers. This is
operationalized as a versioned `beliefs.yaml` updated by a daily/weekly agent pipeline: a
signal-collector ingests market, customer, and analytics signals; a classifier tags each signal
against current beliefs; a synthesizer diffs the beliefs weekly; a strategy-reviewer proposes
roadmap changes. Humans own two gates: kill/keep decisions and any belief change affecting
pricing or positioning.

## Why

Feature parity is no longer a moat — AI can replicate a UI in days. The real moat is learning
velocity: `(Signals Noticed × Update Speed × Execution Quality) / Time`. Orgs that run weekly
strategy reviews instead of quarterly, and that log decisions with predictions and check-back
dates, compound their advantage while competitors are still debating last quarter's roadmap.
Decision logs graded quarterly on prediction accuracy are the forcing function.

## When To Use

- AI-replicable product surface where feature parity is reachable in weeks (most B2B SaaS,
  content tools, vertical AI wrappers)
- Org with 3+ teams where signal latency is measured in weeks, not days
- Strategy reviews are quarterly but competitor/customer behavior changes weekly
- Post-PMF stage where the bottleneck is "what do we ship next" not "does anyone want this"
- Board, GTM, or fundraising narrative needs a defensible operational moat beyond a feature list

## When NOT To Use

- Pre-PMF / 1–5 person team — a single founder's speed beats any process; "rituals" become theater
- Truly defensible moats already in place (network effects, regulated licenses, hardware, dataset
  lock-in) — focus there, not on meta-process
- Markets with 6–12 month sales cycles (defense, medical devices) — weekly updates produce noise
- Teams that will not act on signals — an Insight Repository without a decision owner is a graveyard
- Burned-out teams — adding weekly rituals on top of broken delivery makes velocity worse

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Learning-velocity formula, signal collection, belief-update model, rituals |
| `content/02-agent-usage.xml` | Belief-update pipeline, subagents, prompt patterns, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/belief_update.py` | Weekly belief-update loop: loads events.ndjson, calls Claude, writes beliefs.yaml |
