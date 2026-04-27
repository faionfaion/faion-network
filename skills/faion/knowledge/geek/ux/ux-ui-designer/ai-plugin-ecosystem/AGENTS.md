# AI Plugin Ecosystem (Figma)

## Summary

Methodology for evaluating, adopting, and using AI plugins in Figma (Magician, Automator, Content Reel, Stark, Diagram, Similayer) — covering plugin selection criteria, workflow integration, agent-friendly pre/post-processing patterns, and the hard constraint that Figma plugins run only in the browser sandbox and cannot be invoked headlessly by agents.

## Why

Figma's plugin ecosystem accelerates repetitive design tasks but lacks a stable external API surface. Agents cannot invoke plugins directly — they can only pre-process inputs (generate data files, configuration scripts) and post-process outputs (analyze Figma JSON exports). Understanding which tasks are agent-automatable versus plugin-only prevents wasted engineering effort.

## When To Use

- Evaluating which Figma AI plugins to adopt for a specific team workflow
- Automating repetitive design tasks: bulk renaming, content population, icon generation
- Generating a plugin adoption policy with accessibility and brand guardrails
- Auditing design files for missing content, broken links, or accessibility violations at scale

## When NOT To Use

- Final production asset export — AI plugin outputs require human QA before handoff
- Design system creation — plugins assist but cannot own system architecture decisions
- Small one-off tasks where plugin setup time exceeds manual effort (fewer than ~20 components)
- Contexts where plugin API access to external services raises data privacy concerns

## Content

| File | What's inside |
|------|---------------|
| `content/01-plugin-inventory.xml` | Top Figma AI plugins, capabilities, agent-friendliness, limitations |
| `content/02-agentic-workflow.xml` | What agents can/cannot do with plugins, prompt patterns, tools and services |

## Templates

| File | Purpose |
|------|---------|
| `templates/content-reel-data.py` | Generate Content Reel-compatible JSON data file from name/email lists |
| `templates/prompt-plugin-evaluation.txt` | Prompt for scored plugin adoption matrix |
