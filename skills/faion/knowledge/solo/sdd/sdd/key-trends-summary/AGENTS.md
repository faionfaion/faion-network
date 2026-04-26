# Key Trends Summary 2025-2026

## Summary

Orientation reference covering six major shifts relevant to SDD practitioners: (1) SDD becoming the dominant paradigm for AI-assisted development (intent → spec → plan → execute → review); (2) docs-as-code and LLM-optimized documentation; (3) ADRs as standard practice at AWS, Google Cloud, and Microsoft Azure; (4) LLM-first workflows (context packing, spec-first, agentic MCP); (5) platform engineering growth (45% → 80% of large orgs by 2026); (6) OpenTelemetry as the #2 CNCF project for observability. Load at the start of architectural planning sessions, not per-task.

## Why

The bottleneck has shifted from implementation to specification — LLMs generate code at scale, but quality specifications remain a human-centric skill. Adoption metrics: 65% of developers use AI tools weekly, 25% of YC W25 codebases are 95%+ AI-generated, MCP has become the standard protocol for agent-tool interaction. Teams that treat specs as programming interfaces for AI agents ship faster with lower defect rates than teams that rely on narrative requirements.

## When To Use

- When an agent needs to orient itself on current SDD, observability, and platform tooling before advising on architecture
- When a human asks what tools to use for SDD/documentation in 2025-2026
- As a context document before quarterly roadmap sessions
- When evaluating whether to adopt a new tool (Kiro, Tessl, MCP, etc.)

## When NOT To Use

- As a replacement for methodology-specific docs — use dedicated methodology folders for actionable guidance
- For time-sensitive tool decisions — this is a snapshot; verify market share data currency before committing
- For domains not covered here (the doc covers SDD, ADRs, living docs, platform engineering, observability)
- When the agent already has current context from a more specific source

## Content

| File | What's inside |
|------|---------------|
| `content/01-sdd-and-docs.xml` | SDD core workflow and effectiveness table; living documentation and docs-as-code patterns; developer portal landscape |
| `content/02-adrs-and-llm-workflows.xml` | ADR lifecycle, storage pattern, best practices; LLM-first adoption metrics and workflow patterns; agentic MCP standard |
| `content/03-platform-observability.xml` | Platform engineering trajectory; portal vs platform distinction; OpenTelemetry three pillars + profiling |

## Templates

none
