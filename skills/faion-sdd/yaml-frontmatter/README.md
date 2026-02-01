# YAML Frontmatter Standards

> **Entry point:** `/faion-net` - invoke for automatic routing.

Standard for metadata in all SDD documentation and content files.

---

## Overview

YAML frontmatter is a metadata block at the beginning of Markdown/MDX files, enclosed by triple-dashed lines (`---`). It provides structured data about the document that can be parsed programmatically.

```yaml
---
type: spec
version: "1.0.0"
status: draft
created: 2026-01-25
---

# Document Title

Content starts here...
```

---

## Why Frontmatter?

| Benefit | Description |
|---------|-------------|
| **Machine-readable** | Parseable by tools, SSGs, and LLMs |
| **Separation of concerns** | Metadata separate from content |
| **Validation** | Schema validation ensures consistency |
| **Queryable** | Filter/sort documents by metadata |
| **Type-safe** | TypeScript types via Zod schemas |
| **SSG integration** | Native support in Jekyll, Hugo, Astro, etc. |

---

## Supported Formats

| Format | Delimiters | Use Case |
|--------|------------|----------|
| **YAML** | `---` | Default, most portable |
| **TOML** | `+++` | Hugo preference |
| **JSON** | `{` `}` | Programmatic generation |

**Recommendation:** Use YAML for maximum portability across tools.

---

## Static Site Generator Support

### Jekyll

First major SSG with frontmatter support. Processes any file with YAML frontmatter.

```yaml
---
layout: post
title: "My Post"
date: 2026-01-25
categories: [tech, ai]
---
```

[Jekyll Front Matter Docs](https://jekyllrb.com/docs/front-matter/)

### Hugo

Supports YAML, TOML, and JSON. Has powerful cascade frontmatter for inherited values.

```yaml
---
title: "My Post"
date: 2026-01-25
draft: false
taxonomies:
  tags: ["ai", "sdd"]
---
```

[Hugo Front Matter Docs](https://gohugo.io/content-management/front-matter/)

### Astro

Modern approach with Zod schema validation and TypeScript integration.

```yaml
---
title: "My Post"
description: "Post description"
pubDate: 2026-01-25
tags: ["ai", "sdd"]
---
```

[Astro Content Collections](https://docs.astro.build/en/guides/content-collections/)

### VitePress

Markdown-based docs with frontmatter support via gray-matter.

```yaml
---
title: "Page Title"
editLink: true
lastUpdated: true
---
```

[VitePress Frontmatter](https://vitepress.dev/guide/frontmatter)

### MDX

Frontmatter in MDX files works like Markdown, accessible via exports.

```jsx
---
title: "Component Doc"
status: "stable"
---

# {frontmatter.title}
```

---

## Parsing Libraries

### JavaScript/Node.js

| Library | Downloads/week | Features |
|---------|----------------|----------|
| **gray-matter** | 9M+ | YAML/TOML/JSON, excerpts, custom delimiters |
| **front-matter** | 1M+ | Simple, YAML only |
| **@github-docs/frontmatter** | - | Schema validation with revalidator |

**gray-matter** (recommended):
```javascript
import matter from 'gray-matter';

const { data, content } = matter(fileContents);
console.log(data.title);  // frontmatter
console.log(content);     // markdown body
```

[gray-matter on GitHub](https://github.com/jonschlinkert/gray-matter)

### Python

| Library | Features |
|---------|----------|
| **python-frontmatter** | YAML/JSON/TOML, handlers, post objects |

```python
import frontmatter

post = frontmatter.load('article.md')
print(post['title'])    # frontmatter
print(post.content)     # markdown body
```

[python-frontmatter on PyPI](https://pypi.org/project/python-frontmatter/)

### Custom Parser (Simple)

**Python:**
```python
import yaml
import re

def parse_frontmatter(content: str) -> tuple[dict, str]:
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1)), match.group(2)
    return {}, content
```

**JavaScript:**
```javascript
function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (match) {
    return { data: jsyaml.load(match[1]), content: match[2] };
  }
  return { data: {}, content };
}
```

---

## Schema Validation

### Zod (TypeScript/Astro)

Astro's content collections use Zod for type-safe frontmatter validation.

```typescript
// src/content.config.ts
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  schema: z.object({
    title: z.string().max(100),
    description: z.string().optional(),
    pubDate: z.coerce.date(),
    draft: z.boolean().default(false),
    tags: z.array(z.string()).default([]),
  }),
});

export const collections = { blog };
```

[Zod Documentation](https://zod.dev/)

### JSON Schema

For validation in any language using JSON Schema.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["type", "version", "status"],
  "properties": {
    "type": { "enum": ["spec", "design", "task"] },
    "version": { "pattern": "^\\d+\\.\\d+\\.\\d+$" },
    "status": { "enum": ["draft", "review", "approved"] }
  }
}
```

### GitHub Actions Validation

```yaml
- uses: hashicorp/front-matter-schema@v1
  with:
    files: 'content/**/*.md'
    schema: '.frontmatter-schema.json'
```

[front-matter-schema Action](https://github.com/hashicorp/front-matter-schema)

---

## LLM Usage Tips

### For Claude/GPT/Copilot

1. **Always include frontmatter** when generating documentation
2. **Follow the schema** defined in constitution.md or this file
3. **Use ISO dates** (YYYY-MM-DD) for date fields
4. **Quote strings** that might be misinterpreted (version numbers, IDs)
5. **Keep arrays inline** for short lists: `tags: [ai, sdd, docs]`

### Prompt Patterns

When asking LLMs to generate content with frontmatter:

```
Generate a spec.md for feature X with proper YAML frontmatter including:
- type: spec
- feature_id: "XXX-feature-name"
- version: "1.0.0"
- status: draft
- priority: P1
- created: [today's date]
```

### Validation Prompt

```
Validate this frontmatter against SDD standards:
[paste frontmatter]

Check for:
- Required fields present
- Correct field types
- Valid status/priority values
- Proper date format
```

---

## Best Practices

### Do

- Use YAML for portability
- Quote version numbers: `version: "1.0.0"`
- Use arrays for multiple values: `tags: [a, b, c]`
- Keep frontmatter minimal and focused
- Use meaningful, descriptive key names
- Validate with schemas in production

### Don't

- Don't use tabs (YAML requires spaces)
- Don't put too much data in frontmatter
- Don't use HTML in frontmatter values
- Don't nest deeply (max 2-3 levels)
- Don't hardcode computed values (let tools compute)

---

## SDD Document Types

See [examples.md](examples.md) for complete frontmatter examples for:

| Type | File | Description |
|------|------|-------------|
| constitution | constitution.md | Project standards |
| roadmap | roadmap.md | Feature timeline |
| spec | spec.md | Feature specification |
| design | design.md | Technical design |
| implementation-plan | implementation-plan.md | Task breakdown |
| task | TASK_XXX_*.md | Individual task |
| methodology | *.md in skills/ | Methodology reference |

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Writing specification templates | haiku | Form completion, mechanical setup |
| Reviewing specifications for clarity | sonnet | Language analysis, logical consistency |
| Architecting complex system specs | opus | Holistic design, novel combinations |
## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Step-by-step checklist |
| [examples.md](examples.md) | Real frontmatter examples |
| [templates.md](templates.md) | Copy-paste templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompt patterns |

---

## External Resources

- [Using Frontmatter in Markdown](https://www.markdownlang.com/advanced/frontmatter.html)
- [SSW Rules: Best Practices for Frontmatter](https://www.ssw.com.au/rules/best-practices-for-frontmatter-in-markdown)
- [GitHub Docs: Using YAML Frontmatter](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter)
- [Front Matter CMS](https://frontmatter.codes/)
- [remark-frontmatter plugin](https://github.com/remarkjs/remark-frontmatter)

---

*yaml-frontmatter v1.0.0 - 2026-01-25*
