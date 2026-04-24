# YAML Frontmatter Templates

Copy-paste templates for all SDD document types. Replace placeholders in `{CURLY_BRACES}`.

---

## SDD Core Documents

### Constitution Template

```yaml
---
type: constitution
version: "1.0.0"
status: active
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
author: {Author Name}
domain: {project-domain.com}
---
```

### Roadmap Template

```yaml
---
type: roadmap
version: "1.0.0"
status: active
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
---
```

### Feature Specification Template

```yaml
---
type: spec
feature_id: "{NNN}-{feature-name}"
version: "1.0.0"
status: backlog
priority: P1
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
depends_on: []
---
```

### Design Document Template

```yaml
---
type: design
feature_id: "{NNN}-{feature-name}"
version: "1.0.0"
status: draft
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
spec_version: "1.0.0"
---
```

### Implementation Plan Template

```yaml
---
type: implementation-plan
feature_id: "{NNN}-{feature-name}"
version: "1.0.0"
status: draft
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
design_version: "1.0.0"
total_tasks: {N}
---
```

### Task Template

```yaml
---
type: task
task_id: "TASK_{NNN}"
feature_id: "{NNN}-{feature-name}"
status: todo
priority: P1
created: {YYYY-MM-DD}
depends_on: []
blocks: []
complexity: medium
estimated_tokens: 50000
---
```

---

## Methodology Templates

### Basic Methodology

```yaml
---
type: methodology
id: {methodology-id}
title: "{Methodology Title}"
category: {Category}
difficulty: beginner
tags: [{tag1}, {tag2}]
read_time_minutes: {N}
---
```

### Advanced Methodology with Prerequisites

```yaml
---
type: methodology
id: {methodology-id}
title: "{Methodology Title}"
category: {Category}
difficulty: advanced
tags: [{tag1}, {tag2}, {tag3}]
read_time_minutes: {N}
prerequisites:
  - {prereq-methodology-1}
  - {prereq-methodology-2}
related:
  - {related-methodology-1}
  - {related-methodology-2}
---
```

---

## Product Documentation Templates

### Market Research

```yaml
---
type: product-doc
doc_type: market-research
version: "1.0.0"
status: draft
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
---
```

### User Persona

```yaml
---
type: product-doc
doc_type: user-persona
version: "1.0.0"
status: draft
created: {YYYY-MM-DD}
persona_name: "{Persona Name}"
segment: {B2B|B2C}
---
```

### Competitive Analysis

```yaml
---
type: product-doc
doc_type: competitive-analysis
version: "1.0.0"
status: draft
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
competitors_analyzed: {N}
---
```

### GTM Part

```yaml
---
type: gtm-part
part_number: {N}
title: "{Part Title}"
version: "1.0.0"
status: draft
created: {YYYY-MM-DD}
---
```

---

## Content Templates

### Blog Post (MDX)

```yaml
---
type: blog-post
title: "{Post Title}"
slug: {post-slug}
description: "{Brief description for SEO}"
pubDate: {YYYY-MM-DD}
author: {Author Name}
tags: [{tag1}, {tag2}, {tag3}]
category: {Category}
readingTime: {N}
draft: true
featured: false
image:
  src: /images/blog/{image-name}.png
  alt: "{Image description}"
---
```

### Knowledge Guide

```yaml
---
type: knowledge-guide
title: "{Guide Title}"
slug: {guide-slug}
methodology_id: {source-methodology}
level: beginner
version: "1.0.0"
status: draft
created: {YYYY-MM-DD}
author: {Author Name}
access: free
tags: [{tag1}, {tag2}]
reading_time: {N}
---
```

### Landing Page

```yaml
---
type: landing-page
slug: {page-slug}
title: "{Page Title} | {Site Name}"
description: "{Page description for SEO}"
version: "1.0.0"
status: draft
seo:
  title: "{SEO Title}"
  description: "{SEO Description}"
  og_image: /images/og/{image-name}.png
---
```

---

## Static Site Generator Templates

### Jekyll Post

```yaml
---
layout: post
title: "{Post Title}"
date: {YYYY-MM-DD} {HH:MM:SS} {+ZZZZ}
categories: [{category1}, {category2}]
tags: [{tag1}, {tag2}]
author: {author}
excerpt: "{Post excerpt}"
---
```

### Hugo Article

```yaml
---
title: "{Article Title}"
date: {YYYY-MM-DD}T{HH:MM:SS}{+ZZ:ZZ}
draft: true
description: "{Article description}"
categories: [{category}]
tags: [{tag1}, {tag2}]
author: "{Author Name}"
---
```

### Astro Content

```yaml
---
title: "{Content Title}"
description: "{Content description}"
pubDate: {YYYY-MM-DD}
tags: [{tag1}, {tag2}]
draft: true
---
```

### VitePress Page

```yaml
---
title: {Page Title}
editLink: true
lastUpdated: true
outline: deep
---
```

### Docusaurus Doc

```yaml
---
id: {doc-id}
title: {Doc Title}
sidebar_label: {Sidebar Label}
sidebar_position: {N}
description: {Doc description}
---
```

---

## Brief/Onboarding Templates

### Onboarding Brief

```yaml
---
type: brief
brief_type: onboarding
target_role: "{Target Role}"
version: "1.0.0"
status: active
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
language: en
---
```

### Technical Brief

```yaml
---
type: brief
brief_type: technical
target_audience: "{Audience}"
version: "1.0.0"
status: draft
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
---
```

---

## Schema Definition Templates

### Zod Schema (Astro)

```typescript
// src/content.config.ts
import { defineCollection, z } from 'astro:content';

const {collection_name} = defineCollection({
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    draft: z.boolean().default(false),
    tags: z.array(z.string()).default([]),
  }),
});

export const collections = { {collection_name} };
```

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["type", "version", "status", "created"],
  "properties": {
    "type": {
      "type": "string",
      "enum": ["{type1}", "{type2}", "{type3}"]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "status": {
      "type": "string",
      "enum": ["draft", "review", "approved", "active"]
    },
    "created": {
      "type": "string",
      "format": "date"
    }
  }
}
```

### Front Matter CMS Schema

```json
{
  "frontMatter.taxonomy.contentTypes": [
    {
      "name": "{content-type}",
      "pageBundle": false,
      "fields": [
        {
          "title": "Title",
          "name": "title",
          "type": "string",
          "required": true
        },
        {
          "title": "Status",
          "name": "status",
          "type": "choice",
          "choices": ["draft", "published"],
          "default": "draft"
        },
        {
          "title": "Date",
          "name": "date",
          "type": "datetime",
          "default": "{{now}}"
        }
      ]
    }
  ]
}
```

---

## Validation Templates

### GitHub Action for Validation

```yaml
# .github/workflows/validate-frontmatter.yml
name: Validate Frontmatter

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/front-matter-schema@v1
        with:
          files: 'content/**/*.md'
          schema: '.frontmatter-schema.json'
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

for file in $(git diff --cached --name-only | grep '\.md$'); do
  if head -1 "$file" | grep -q '^---$'; then
    # Extract and validate YAML
    sed -n '2,/^---$/p' "$file" | head -n -1 | python -c "import yaml,sys; yaml.safe_load(sys.stdin)" || exit 1
  fi
done
```

---

## Quick Reference Card

| Document | Type Value | Required Fields |
|----------|------------|-----------------|
| Constitution | `constitution` | type, version, status, created, updated, author |
| Roadmap | `roadmap` | type, version, status, created, updated |
| Spec | `spec` | type, feature_id, version, status, priority, created, updated |
| Design | `design` | type, feature_id, version, status, created, updated |
| Impl Plan | `implementation-plan` | type, feature_id, version, status, created, updated |
| Task | `task` | type, task_id, feature_id, status, priority, created |
| Methodology | `methodology` | type, id, title, category, difficulty |
| Product Doc | `product-doc` | type, doc_type, version, status, created |
| Brief | `brief` | type, brief_type, target_role, version, status, created |

---

*yaml-frontmatter/templates.md v1.0.0 - 2026-01-25*
