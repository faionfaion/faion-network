# AI-Powered PM Tools 2026

## Summary

A 2026 survey of AI-augmented PM platforms: Jira+Rovo (enterprise), Monday.com (work management), ClickUp Brain (all-in-one), Wrike (ML risk prediction), Forecast App (resource matching), and Motion/Epicflow (scheduling). Covers each platform's AI capabilities, API agent-friendliness, and the DORA 2025 AI productivity paradox: AI tools boost individual output metrics while organizational delivery metrics stay flat because bottlenecks shift to review, integration, and deployment.

## Why

Choosing a PM platform's AI features requires understanding what is API-accessible versus UI-only. Jira Rovo agents, ClickUp Autopilot, and Monday Agent Factory are not portable — adopting them creates vendor lock-in. The DORA 2025 paradox means tracking individual issue velocity is insufficient; teams must measure end-to-end flow time to detect shifted bottlenecks. Claude subagents interacting via REST/GraphQL APIs are the portable alternative.

## When To Use

- Evaluating which AI-powered PM platform fits the team's needs
- Integrating Claude subagents with an existing PM tool for issue creation, WBS generation, or status reporting
- Setting up automated risk prediction or bottleneck detection workflows
- Generating work breakdown structures from project briefs via PM tool AI or Claude
- Automating meeting notes → task creation pipelines

## When NOT To Use

- Teams with fewer than 3 people where PM platform overhead exceeds coordination benefit
- Pure engineering execution tracking where Linear or GitHub Issues is sufficient
- When PM tool AI features require vendor-specific models conflicting with data governance policies
- Critical path management in construction or hardware — nPlan is specialized; generic AI PM tools do not understand physical dependencies

## Content

| File | What's inside |
|------|---------------|
| `content/01-platform-survey.xml` | Tool comparison table, Jira AI/Rovo features, Monday.com AI, ClickUp Brain features and pricing |
| `content/02-agent-integration.xml` | Agentic workflow patterns, API compatibility table, WBS generation prompt, Jira issue creation script |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-wbs.xml` | XML prompt for agent to generate a work breakdown structure from a project brief |
| `templates/create-jira-issues.sh` | Bash script to create Jira issues from a JSON WBS output |
