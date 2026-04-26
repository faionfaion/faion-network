# Agent Integration — Methodologies Summary (Product Manager)

## Nature of this entry

`methodologies-summary` is **not a methodology** — it is the index/quick-reference
for the 33 methodologies inside `pro/product/product-manager/`. It contains only
`README.md` (table of contents + selection guide); `checklist.md`,
`templates.md`, `examples.md`, `llm-prompts.md` are intentionally empty.

The 5-file research pattern (CLI tools, services, scripts, gotchas) does not apply
to a router document. A subagent does not "execute" a summary — it reads it to
choose which real methodology to load next.

## Agentic role: routing only

Use this file as the **first read** when an agent enters product-manager scope
without a specific methodology pinned. Flow:

```
PM task arrives → Read methodologies-summary/README.md
              → Match task to row in "Quick Selection Guide"
              → Read knowledge/pro/product/product-manager/<picked>/README.md
              → Load that methodology's agent-integration.md (if present)
              → Execute
```

### Recommended subagents

- `faion-pm-agent` — owns mvp-scoping, product-discovery, business-model-research routes
- `faion-mvp-scope-analyzer-agent` — invoked from `mvp-scoping` row
- `faion-mlp-agent` — invoked from `mlp-planning` row
- `faion-market-researcher-agent` — invoked from problem-validation, value-proposition-design, niche-evaluation rows
- `faion-persona-builder-agent` — invoked from `jobs-to-be-done` row

### Prompt pattern (router)

```
Task: <PM task>
Step 1: Read pro/product/product-manager/methodologies-summary/README.md
Step 2: Pick ONE row from Quick Selection Guide
Step 3: Read that methodology's README.md and apply
Return: methodology slug + chosen agent
```

## When to use this file

- Cold start: agent has PM task, no methodology pre-selected
- Task triage: deciding between RICE vs MoSCoW, MVP vs MLP, roadmap vs OKR

## When NOT to use

- Methodology already chosen → skip summary, go straight to that folder
- Cross-skill work (BA, PM-agile, project-manager) → use respective skill's own router
- Execution / templates → look in the methodology's own files, never here

## Limitations

- README is hand-curated — drifts when methodologies are added/removed; verify the
  folder list against `ls pro/product/product-manager/` before trusting it.
- "Quick Selection Guide" maps tasks to methodologies but not to agents; agent
  selection must be cross-referenced in each methodology's own
  `agent-integration.md`.
- No CLI tools, services, or scripts apply at this level — those belong to
  individual methodologies.

## References

- Parent skill: `pro/product/product-manager/SKILL.md`
- Sibling routers: `solo/product/product-planning/`, `solo/product/product-operations/`
- Research brief: `skills/faion/.research/BRIEF.md`
