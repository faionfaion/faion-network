# Agent Integration — YAML Frontmatter Standards

## When to use
- Any time an agent generates a new SDD document (spec, design, task, roadmap) — frontmatter is required
- When building a script or tool that reads, filters, or routes SDD documents by metadata (status, priority, type)
- When integrating SDD docs with a static site generator (Astro, Hugo, MkDocs) that parses frontmatter
- When setting up CI validation to enforce consistent metadata across all documents in `.aidocs/`

## When NOT to use
- Plain README files with no lifecycle metadata (AGENTS.md, CLAUDE.md — these have no frontmatter by convention)
- Configuration files masquerading as Markdown — use proper config formats (TOML, JSON, YAML) instead
- Deeply nested hierarchical data — frontmatter works for flat/shallow metadata; complex relationships belong in document body

## Where it fails / limitations
- YAML syntax is fragile: a single tab, unquoted colon, or unescaped special char silently corrupts the entire frontmatter block in some parsers
- `gray-matter` (JS) and `python-frontmatter` (Python) behave differently on edge cases (e.g., multi-line values, boolean coercion) — test both if your pipeline uses both
- LLMs frequently omit required fields or use incorrect date formats (`25-04-2026` instead of `2026-04-25`); validation must be automated
- Version fields as unquoted numbers (`version: 1.0`) are parsed as floats in YAML; always quote: `version: "1.0.0"`
- Frontmatter schemas drift across projects without centralized enforcement; the `status` field alone has been seen as `draft`, `Draft`, `WIP`, `in-review` in the same repo

## Agentic workflow
An agent generating any SDD document must read the project's constitution.md (or this methodology) for the canonical frontmatter schema, then populate all required fields before writing the document body. A validation step — either inline or as a separate CI job — parses the frontmatter and checks required fields, value enums, and date format. Failed validation blocks the pre-commit hook, not the agent, so agents must validate locally before committing.

### Recommended subagents
- Any tier — frontmatter generation is mechanical; Haiku is sufficient if the schema is provided explicitly in the prompt
- CI bot / pre-commit hook — automated validation is more reliable than a second agent for this task

### Prompt pattern
```
Generate frontmatter for a new spec.md with these values:
- type: spec
- feature_id: "042-auth-refactor"
- version: "1.0.0"
- status: draft
- priority: P1
- created: 2026-04-25
- author: ruslan

Output only the frontmatter block (between --- delimiters), then start the document body.
```

```
Validate this frontmatter against SDD standards.
Required fields: type, version, status, created.
Valid status values: draft, review, approved, superseded.
Date format: YYYY-MM-DD.
Version format: semver quoted string.
Report every violation with field name and fix.
---
[paste frontmatter here]
---
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `yq` | Parse, query, and validate YAML frontmatter from CLI | `brew install yq` / [docs](https://mikefarah.gitbook.io/yq/) |
| `front-matter-schema` | GitHub Action: validate frontmatter against JSON Schema in CI | `uses: hashicorp/front-matter-schema@v1` / [docs](https://github.com/hashicorp/front-matter-schema) |
| `markdownlint-cli2` | Catches malformed frontmatter delimiters and formatting issues | `npm i -g markdownlint-cli2` / [docs](https://github.com/DavidAnson/markdownlint-cli2) |
| `python-frontmatter` | Parse frontmatter in Python scripts/agents | `pip install python-frontmatter` / [PyPI](https://pypi.org/project/python-frontmatter/) |
| `gray-matter` | Parse frontmatter in Node.js scripts/agents | `npm i gray-matter` / [docs](https://github.com/jonschlinkert/gray-matter) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Astro Content Collections | OSS framework | Yes — Zod schema | Type-safe frontmatter validation at build time; ideal for SDD portals |
| Front Matter CMS | OSS VS Code ext | Partial | GUI for frontmatter editing; agents cannot drive VS Code extensions |
| Hugo | OSS SSG | Yes — file-based | Reads YAML/TOML/JSON frontmatter; agent writes files, Hugo builds |
| MkDocs + Material | OSS | Yes — file-based | Reads frontmatter for nav, tags; CI-friendly |
| GitHub Actions | SaaS CI | Yes | `front-matter-schema` action validates on PR; blocks merge on failure |

## Templates & scripts
See `templates.md` for complete frontmatter blocks per SDD document type.

Frontmatter validation script (Python, validates required fields and enum values):
```python
#!/usr/bin/env python3
"""Validate YAML frontmatter in SDD documents."""
import sys
import frontmatter

REQUIRED = {"type", "version", "status", "created"}
VALID_STATUS = {"draft", "review", "approved", "superseded"}
VALID_TYPES = {"spec", "design", "task", "roadmap", "constitution", "implementation-plan"}

def validate(path: str) -> list[str]:
    post = frontmatter.load(path)
    meta = post.metadata
    errors = []
    for field in REQUIRED:
        if field not in meta:
            errors.append(f"MISSING required field: {field}")
    if "status" in meta and meta["status"] not in VALID_STATUS:
        errors.append(f"INVALID status '{meta['status']}', must be one of {VALID_STATUS}")
    if "type" in meta and meta["type"] not in VALID_TYPES:
        errors.append(f"INVALID type '{meta['type']}', must be one of {VALID_TYPES}")
    if "version" in meta and not isinstance(meta["version"], str):
        errors.append("version must be a quoted string (e.g., \"1.0.0\")")
    return errors

if __name__ == "__main__":
    for path in sys.argv[1:]:
        errs = validate(path)
        if errs:
            print(f"{path}:"); [print(f"  - {e}") for e in errs]; sys.exit(1)
    print("OK")
```

## Best practices
- Define a canonical frontmatter schema in constitution.md once per project; all agents and humans reference the same schema
- Always quote version numbers and IDs in YAML: `version: "1.0.0"`, `feature_id: "042-slug"` — bare numbers are float-coerced
- Use ISO 8601 dates (`YYYY-MM-DD`) — LLMs default to locale-specific formats without explicit instruction
- Keep frontmatter shallow: max 2 levels of nesting; anything deeper belongs in the document body as structured tables
- Run frontmatter validation as a pre-commit hook so agents cannot commit invalid documents; use `yq` or the Python script above
- Add `updated: YYYY-MM-DD` to every document an agent touches — enables sorting by recency without reading file mtimes

## AI-agent gotchas
- LLMs frequently output frontmatter with trailing spaces on field lines — YAML parsers accept these but schema validators may reject them
- When an agent generates a document with a code fence in the body (```` ``` ````), some parsers mis-detect the second `---` in YAML comments as a frontmatter close delimiter — test with your parser
- Agents asked to "update the status field" sometimes regenerate the entire frontmatter block, erasing `created` and other fields set by earlier agents — instruct agents to patch only the target field using `yq`
- `python-frontmatter` preserves insertion order; `gray-matter` does not guarantee order — do not rely on field ordering for parsing logic
- Zod validation errors in Astro content collections produce build failures, not runtime errors — agent-generated content must be validated before committing to repos that build on push

## References
- [Using Frontmatter in Markdown](https://www.markdownlang.com/advanced/frontmatter.html)
- [gray-matter on GitHub](https://github.com/jonschlinkert/gray-matter)
- [python-frontmatter on PyPI](https://pypi.org/project/python-frontmatter/)
- [Astro Content Collections + Zod](https://docs.astro.build/en/guides/content-collections/)
- [hashicorp/front-matter-schema GitHub Action](https://github.com/hashicorp/front-matter-schema)
- [yq YAML processor](https://mikefarah.gitbook.io/yq/)
- [SSW Rules: Frontmatter Best Practices](https://www.ssw.com.au/rules/best-practices-for-frontmatter-in-markdown)
