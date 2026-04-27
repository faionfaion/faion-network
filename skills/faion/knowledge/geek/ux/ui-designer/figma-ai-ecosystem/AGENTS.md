# Figma AI Ecosystem

## Summary

Figma's AI suite — Make (prompt-to-prototype), Draw (vector sketching), Sites (publish direct from Figma), and Image Tools (erase/isolate/expand) — is entirely UI-only with no agent API surface. Agents cannot trigger any of these features programmatically. The practical agent integration surface is the Figma REST API (read file structure, styles, components) and Figma Webhooks API (react to file change events). Agent role: prompt preparation for humans to paste into Figma Make, webhook-triggered audits, and post-publish accessibility/performance validation of Figma Sites output.

## Why

Figma has evolved from a design tool to an end-to-end platform with AI at its core, but all AI features require a human in the Figma UI session. Understanding what the REST and Webhooks APIs do and do not support prevents building automation pipelines that silently fail because they depend on non-existent agent entry points.

## When To Use

- Generating structured prompts for Figma Make that a designer then pastes and executes
- Using Figma Webhooks to trigger downstream agent workflows (spec generation, audit, asset export) on file changes
- Auditing Figma Sites published pages with Lighthouse and axe after a human publishes
- Applying non-destructive image editing (erase, isolate, expand) within Figma — human-operated, agent can post-process exported results
- Evaluating Figma's AI suite before committing to Adobe Firefly or standalone generative tools

## When NOT To Use

- Production-quality code output is required — Figma Make outputs prototype-grade code, not deployable code
- The design system is token-driven and complex — Figma AI tools do not reliably respect custom token systems
- Deterministic, reproducible outputs are required — all Figma AI features are non-deterministic
- The artifact must be version-controlled at code level — Figma files are binary; Sites output is not Git-tracked
- WCAG compliance is required from day one — Figma AI outputs consistently miss accessibility requirements

## Content

| File | What's inside |
|------|---------------|
| `content/01-ai-tools.xml` | Figma AI tool catalog, agent boundary rule, REST and Webhooks API scope |
| `content/02-agent-integration.xml` | Agent workflow, prompt preparation pattern, service catalog, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/figma-make-prompt.txt` | Structured Figma Make prompt template for feature prototypes |
| `templates/audit-figma-sites.sh` | Lighthouse + axe audit script for Figma Sites published pages |
