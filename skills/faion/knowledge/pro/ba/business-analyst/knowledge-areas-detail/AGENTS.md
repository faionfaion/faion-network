# BA Knowledge Areas Detail

## Summary

Detailed reference for all six BABOK Knowledge Areas (KA-1 through KA-6): per-KA task table, key outputs, linked methodologies, and the canonical workflow sequence for greenfield engagements and change requests. This is a routing and reference index — it does not replace per-methodology folders. Use it to select KAs, sequence subagents, and audit artifact coverage.

## Why

BABOK knowledge areas overlap and can be applied in multiple sequences. Without a concrete task-level reference, agents default to KA-5 (modeling) on any input, missing stakeholder mapping (KA-1), strategy alignment (KA-4), and traceability maintenance (KA-3). This detail file provides the KA dispatch table and typical sequencing that prevents those defaults.

## When To Use

- Starting a new BA engagement: scope which KAs apply and in what order.
- Routing a vague stakeholder request to the correct KA and downstream methodology.
- Building a multi-step agentic pipeline crossing several KAs (elicit → model → validate → trace).
- Auditing an existing BA artifact set for KA coverage gaps before a release gate.

## When NOT To Use

- You already know the methodology — go straight to that methodology's folder.
- Pure product discovery with no formal requirements artifacts — use `product-manager/continuous-discovery`.
- Pure UX research — use `pro/ux/ux-researcher/` skills.
- One-off ad-hoc questions that produce no tracked artifact.

## Content

| File | What's inside |
|------|---------------|
| `content/01-knowledge-areas.xml` | KA-1 through KA-6: purpose, task table with outputs, linked methodologies, and key techniques. |
| `content/02-workflow.xml` | KA relationships, typical BA workflow sequence, underlying competencies across all KAs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ba-route.sh` | Bash script classifying a BA request into KAs and listing candidate methodologies via Claude API. |
