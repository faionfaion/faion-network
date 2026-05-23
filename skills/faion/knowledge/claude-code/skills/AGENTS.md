# Creating or Updating Claude Code Skills

## Summary

**One-sentence:** Spec for SKILL.md (frontmatter + body), tool-permission scope, global vs project-specific distinction, name conventions, auto-trigger keyword design.

**One-paragraph:** Claude Code skills are discoverable workflows: SKILL.md + optional reference.md + scripts/. Skills auto-trigger on keywords + appear in the `/` menu. Misuse — single-shot tasks wrapped as skills, missing tool whitelist, project-specific business logic stuffed into faion-network — bloats the skill catalog and erodes trust. This methodology codifies the SKILL.md frontmatter schema, the trigger-keyword rule, the tool-permission discipline, and the global-vs-project decision. Output is a SKILL.md validated by the schema.

**Ефективно для:**

- Reusable workflow, що повинен з'являтися в `/` menu Claude Code.
- Tool permission scoping: read-only research skill = Read+Grep+Glob only.
- Multi-file knowledge bundles (SKILL.md + reference.md + scripts/).
- Global vs project-specific: shared в faion-network, локальний — gitignore.

## Applies If (ALL must hold)

- Complex workflow needs to be discoverable + reusable across sessions.
- Tool permissions must be scoped (read-only research vs full-write deploy).
- Multi-file knowledge bundled together (SKILL.md + supporting refs).

## Skip If (ANY kills it)

- One-time task — use a plain prompt.
- Need slash command with arguments only — use Command.
- Skill already exists in faion-network with minor wording differences — edit the existing one.
- Project-specific business logic that should not be shared cross-project — keep local + gitignore.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workflow spec | Markdown | team |
| Trigger keywords | list of phrases that should auto-invoke | team / use-case |
| Tool whitelist | minimum tools needed | permissions policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[project-docs-convention]] | upstream context required for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: skill-md-required-fields, minimum-tool-whitelist, global-vs-project-decision, reference-md-on-demand, trigger-keywords-test | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for config + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skill-vs-alternative` | sonnet | Decision tree application. |
| `write-skill-md` | sonnet | Light judgment on body length + keywords. |
| `test-trigger-keywords` | haiku | Mechanical 10-phrasing test. |

## Templates

| File | Purpose |
|------|---------|
| `templates/SKILL.md` | SKILL.md skeleton with required frontmatter + body sections |
| `templates/reference.md` | On-demand reference.md template |
| `templates/keyword-test.md` | 10-phrasing keyword test fixture template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-skills.py` | Validate the config artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[agents]]
- [[commands]]
- [[hooks]]
- [[project-docs-convention]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
