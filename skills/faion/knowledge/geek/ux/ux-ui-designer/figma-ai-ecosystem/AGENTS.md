# Figma AI Ecosystem

## Summary

Methodology for using Figma's native AI tools (Figma Make for prototype generation, Figma Draw for vector sketching, Figma Sites for static publishing, AI Image Tools for canvas-direct object erase/isolate/expand) — covering capabilities, limits, and agent pre/post-processing workflows. Agents cannot invoke any Figma AI tool directly; they generate optimized prompts and structured briefs that a human pastes into Figma.

## Why

Figma AI tools (Config 2025+) compress the prototype-to-stakeholder-review cycle from days to hours. However, each tool has hard limits: Make prototypes are static, Sites output is not a CMS, AI image expansion fails on complex textures, and all AI features are gated behind paid plans. Knowing which tasks belong to Figma AI vs a Claude agent prevents building workflows that don't exist.

## When To Use

- Generating web app prototypes rapidly from a text brief using Figma Make
- Removing objects or expanding image backgrounds on the Figma canvas without export/re-import
- Publishing a static site from Figma via Figma Sites for early stakeholder review
- Producing vector sketch assets using Figma Draw for illustration-heavy UI components
- Auditing a team's Figma AI feature adoption and identifying workflow gaps

## When NOT To Use

- Production web development — Figma Sites output is for demos and landing pages, not complex apps
- Complex multi-state interactive prototyping requiring custom conditional logic
- Brand-critical image editing where exact pixel control matters — AI image tools are probabilistic
- Figma Draw for precise icon creation — generative output lacks manual vector precision

## Content

| File | What's inside |
|------|---------------|
| `content/01-tools-overview.xml` | Make, Draw, Sites, AI Image Tools — capabilities, limits, plan requirements |
| `content/02-agentic-workflow.xml` | What agents can/cannot do, prompt patterns, tools, services, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/find-image-nodes.py` | Figma REST API script to find raster-fill nodes suitable for AI image tools |
| `templates/prompt-make.txt` | Prompt for generating optimized Figma Make input prompts |
| `templates/prompt-sites-review.txt` | Prompt for reviewing Figma Sites page specs for SEO and static limitations |
