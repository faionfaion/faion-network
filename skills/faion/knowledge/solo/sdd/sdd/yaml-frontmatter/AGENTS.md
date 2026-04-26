# YAML Frontmatter Standards

## Summary

YAML frontmatter is a metadata block (`---` delimited) at the top of Markdown/MDX files that provides structured, machine-readable data about the document. Every SDD document must include frontmatter with typed fields (type, version, status, created) following the project's canonical schema defined in constitution.md.

## Why

Frontmatter enables programmatic filtering, routing, and validation of SDD documents — agents can query status, find blocked features, and sort by recency without reading document bodies. Without a schema, field names drift (`created_at` vs `created`, `WIP` vs `draft`) and validation breaks. Version numbers unquoted as YAML scalars silently parse as floats, corrupting `1.0.0` to `1.0`.

## When To Use

- Generating any new SDD document (spec, design, task, roadmap, constitution)
- Integrating docs with a static site generator (Astro, Hugo, MkDocs) that reads frontmatter
- Setting up CI validation to enforce consistent metadata across `.aidocs/`
- Writing a script or agent tool that filters or routes documents by status or priority

## When NOT To Use

- `AGENTS.md`, `CLAUDE.md`, `README.md` files — these have no lifecycle metadata by convention
- Configuration files using YAML as their primary format (use `.env` or proper config files)
- Deeply nested hierarchical data — frontmatter handles flat/shallow metadata; complex relations belong in the document body

## Content

| File | What's inside |
|------|---------------|
| `content/01-schema.xml` | Required fields per doc type, valid enum values, quoting rules |
| `content/02-validation.xml` | Common YAML pitfalls, validation commands, CI integration rules |

## Templates

| File | Purpose |
|------|---------|
| `templates/sdd-frontmatter.yaml` | Copy-paste blocks for all SDD document types |
| `templates/validate-frontmatter.py` | Python script to validate required fields and enum values |
