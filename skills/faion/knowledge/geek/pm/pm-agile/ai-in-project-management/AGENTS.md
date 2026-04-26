# AI in Project Management

## Summary

Framework for applying AI to project risk scoring, schedule variance analysis, resource capacity forecasting, and stakeholder digest generation. Anchor: PMBOK 8 AI Appendix + DORA 2025 Productivity Paradox — AI boosts individual task velocity but organizational throughput stays flat until bottlenecks in review/deploy are addressed.

## Why

AI PM tools adoption reached 47-54% across risk, task automation, and scheduling (PMI 2024). The integration pattern that works: AI as observation and synthesis layer (data aggregation, anomaly surfacing, report generation) with human-initiated action triggers. The pattern that fails: AI as autonomous decision layer for budget reallocations and deadline changes without audit trail.

## When To Use

- Risk register needs automated scoring across sprint data (staleness, dependent-task count, owner response rate)
- Stakeholder reports require synthesis from multiple sources (Jira, GitHub, budget sheets)
- Schedule variance must run continuously, not just at milestones
- Resource allocation decisions need capacity forecasting across 3+ team members
- Post-mortems need pattern extraction from historical project data

## When NOT To Use

- Projects with fewer than 3 people: overhead exceeds benefit
- Decisions carrying legal/contractual weight: require full human sign-off with audit trail
- Teams without baseline PM tooling (Jira/Linear/GitHub): AI has nothing to feed on
- Highly political one-off decisions where stakeholder dynamics dominate data signals

## Content

| File | What's inside |
|------|---------------|
| `content/01-ai-applications.xml` | AI adoption rates by PM area; productivity paradox; implementation approach; industry results |
| `content/02-agent-workflow.xml` | Subagent patterns for PM digest and risk scoring; prompt patterns; CLI tools; gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/risk-score.py` | Python script: score risk items Low/Medium/High from JSON risk register |
| `templates/pm-digest-prompt.txt` | Prompt for project status digest from sprint JSON data |
