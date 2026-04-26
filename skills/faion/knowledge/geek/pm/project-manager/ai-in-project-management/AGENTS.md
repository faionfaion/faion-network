# AI in Project Management

## Summary

PMBOK 8's first dedicated AI appendix: principles for ethical AI use, AI-assisted decision traceability, and sustainable project delivery. Key finding from DORA 2025 — the AI productivity paradox: AI coding assistants produce 21% more tasks and 98% more PRs at the individual level, but organizational delivery metrics stay flat because bottlenecks shift to review, integration, and deployment. Every AI-assisted PM decision must be logged as "AI-suggested [X] based on [data]; human PM approved/modified/rejected because [reason]".

## Why

PMBOK 8 requires human oversight for AI-assisted decisions — agents cannot autonomously reassign resources, close issues, or change deadlines. The productivity paradox means individual velocity metrics are misleading; end-to-end flow time measurement is required to detect bottleneck shifts. AI risk prediction tools need 3–6 months of historical project data before becoming reliable; deploying them on novel projects produces confident-sounding but unreliable scores.

## When To Use

- Assessing where AI can reduce PM overhead in an existing project workflow
- Implementing PMBOK 8 AI appendix guidance: documenting AI-assisted decisions, establishing human oversight gates
- Detecting bottleneck shifts caused by AI productivity gains that have not translated to org-level delivery improvements
- Building AI-assisted risk identification and probability forecasting into project health monitoring
- Establishing team AI literacy baselines before rolling out AI PM tools

## When NOT To Use

- As justification for removing human PM oversight — PMBOK 8 explicitly requires human control for AI-assisted decisions
- Single-person, short-duration tasks where PM overhead exceeds coordination benefit
- Regulated industries (medical devices, aerospace) without established AI decision documentation in compliance framework
- When the team has not established baseline metrics — AI optimization without baseline measurement cannot demonstrate improvement

## Content

| File | What's inside |
|------|---------------|
| `content/01-pmbok8-ai.xml` | PMBOK 8 AI appendix overview, adoption rates by PM area, implementation approach, industry results |
| `content/02-agent-usage.xml` | Agentic decision-support patterns, risk report prompt, bottleneck detection prompt, DORA metrics script, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-health-report.xml` | XML prompt for agent to generate a project health report with RAG status and risk assessment |
| `templates/dora-deployment-count.sh` | Bash script to count deployments in last 30 days from GitHub releases |
