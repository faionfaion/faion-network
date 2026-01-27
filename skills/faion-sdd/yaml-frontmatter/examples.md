# YAML Frontmatter Examples

Real-world frontmatter examples for various document types.

---

## SDD Documents

### Constitution

```yaml
---
type: constitution
version: "7.8.0"
status: active
created: 2026-01-12
updated: 2026-01-25
author: Ruslan Faion
domain: faion.net
tech_stack:
  frontend: [gatsby, react, typescript, tailwind]
  backend: [django, python, postgresql]
  infrastructure: [docker, nginx, hetzner]
---
```

### Roadmap

```yaml
---
type: roadmap
version: "2.7.0"
status: active
created: 2026-01-12
updated: 2026-01-25
current_phase: MLP
milestones:
  - name: MVP
    status: done
  - name: MLP
    status: in-progress
  - name: Scale
    status: planned
---
```

### Feature Specification (spec.md)

```yaml
---
type: spec
feature_id: "026-knowledge-infrastructure"
version: "1.0.0"
status: todo
priority: P1
created: 2026-01-20
updated: 2026-01-25
depends_on:
  - "024-starter-kits"
  - "025-cli-tool"
success_criteria:
  - Knowledge hub pages functional
  - 50+ guides migrated
  - Search working
---
```

### Design Document (design.md)

```yaml
---
type: design
feature_id: "026-knowledge-infrastructure"
version: "1.0.0"
status: draft
created: 2026-01-22
updated: 2026-01-25
spec_version: "1.0.0"
architecture:
  pattern: static-generation
  framework: gatsby
  data_source: mdx
api_contracts:
  - name: KnowledgeQuery
    type: graphql
---
```

### Implementation Plan (implementation-plan.md)

```yaml
---
type: implementation-plan
feature_id: "026-knowledge-infrastructure"
version: "1.0.0"
status: approved
created: 2026-01-23
updated: 2026-01-25
design_version: "1.0.0"
total_tasks: 8
waves:
  - name: Foundation
    tasks: [1, 2, 3]
  - name: Content
    tasks: [4, 5, 6]
  - name: Polish
    tasks: [7, 8]
---
```

### Task (TASK_001_setup.md)

```yaml
---
type: task
task_id: "TASK_001"
feature_id: "026-knowledge-infrastructure"
status: todo
priority: P0
created: 2026-01-23
depends_on: []
blocks:
  - TASK_002
  - TASK_003
complexity: medium
estimated_tokens: 50000
files_to_change:
  - action: CREATE
    path: src/templates/knowledge.tsx
  - action: MODIFY
    path: gatsby-node.ts
---
```

---

## Methodology Documents

### Basic Methodology

```yaml
---
type: methodology
id: sdd-workflow-overview
title: SDD Workflow Overview
category: SDD
difficulty: beginner
tags:
  - sdd
  - workflow
  - specification
read_time_minutes: 8
---
```

### Advanced Methodology

```yaml
---
type: methodology
id: rag-pipeline-optimization
title: RAG Pipeline Optimization
category: ML Engineering
difficulty: advanced
tags:
  - rag
  - embeddings
  - vector-search
  - llm
read_time_minutes: 25
prerequisites:
  - rag-fundamentals
  - embedding-basics
related:
  - chunking-strategies
  - reranking-techniques
---
```

### Skill Reference

```yaml
---
type: skill-reference
skill_id: faion-ml-engineer
title: ML Engineer Skill Reference
version: "1.0.0"
sub_skills:
  - faion-llm-integration
  - faion-rag-engineer
  - faion-ml-ops
  - faion-ai-agents
  - faion-multimodal-ai
total_methodologies: 80
---
```

---

## Product Documents

### Market Research

```yaml
---
type: product-doc
doc_type: market-research
version: "1.0.0"
status: final
created: 2026-01-15
updated: 2026-01-20
market_size:
  tam: "$50B"
  sam: "$5B"
  som: "$50M"
competitors_analyzed: 12
---
```

### GTM Manifest

```yaml
---
type: gtm-part
part_number: 1
title: Market Analysis
version: "1.0.0"
status: final
created: 2026-01-17
next_part: 2
---
```

### User Persona

```yaml
---
type: product-doc
doc_type: user-persona
version: "1.0.0"
status: final
created: 2026-01-18
persona_name: "Tech Lead Terry"
segment: B2B
pain_points:
  - Team coordination
  - Documentation overhead
  - Knowledge silos
---
```

---

## Content Documents

### Blog Post (MDX)

```yaml
---
type: blog-post
title: "Building RAG Pipelines in 2026"
slug: building-rag-pipelines-2026
description: "A comprehensive guide to modern RAG architecture"
pubDate: 2026-01-25
updatedDate: 2026-01-25
author: Ruslan Faion
tags:
  - rag
  - llm
  - ai
  - tutorial
category: AI Engineering
readingTime: 15
draft: false
featured: true
image:
  src: /images/blog/rag-pipeline.png
  alt: RAG Pipeline Architecture
seo:
  title: "RAG Pipelines Guide 2026 | faion.net"
  description: "Learn to build production RAG systems"
  keywords: [rag, llm, ai, embeddings]
---
```

### Knowledge Guide

```yaml
---
type: knowledge-guide
title: "Prompt Engineering Fundamentals"
slug: prompt-engineering-fundamentals
methodology_id: prompt-engineering
level: beginner
version: "1.0.0"
status: published
created: 2026-01-20
updated: 2026-01-25
author: Ruslan Faion
access: free
tags:
  - prompt-engineering
  - llm
  - beginner
reading_time: 12
prerequisites: []
next_guides:
  - prompt-engineering-intermediate
  - chain-of-thought
---
```

### Landing Page (MDX)

```yaml
---
type: landing-page
slug: starter-kits
title: "Starter Kits | faion.net"
description: "Production-ready project templates"
version: "1.0.0"
status: draft
components:
  - Hero
  - Features
  - Pricing
  - FAQ
  - CTA
seo:
  title: "Starter Kits - Production-Ready Templates"
  description: "Download and deploy in minutes"
  og_image: /images/og/starter-kits.png
---
```

---

## Static Site Generator Examples

### Jekyll Post

```yaml
---
layout: post
title: "Welcome to Jekyll"
date: 2026-01-25 10:30:00 +0200
categories: [blog, jekyll]
tags: [ssg, ruby]
author: admin
permalink: /blog/:year/:month/:title/
image: /assets/images/jekyll-post.jpg
excerpt: "Getting started with Jekyll static site generator"
comments: true
---
```

### Hugo Article

```yaml
---
title: "Hugo Quick Start"
date: 2026-01-25T10:30:00+02:00
draft: false
weight: 10
description: "Learn Hugo basics"
categories:
  - tutorials
tags:
  - hugo
  - ssg
author: "Author Name"
cover:
  image: images/hugo.png
  alt: "Hugo Logo"
  relative: true
ShowToc: true
TocOpen: false
---
```

### Astro Blog Post

```yaml
---
title: "Astro Content Collections"
description: "Type-safe content management"
pubDate: 2026-01-25
updatedDate: 2026-01-25
heroImage: "/blog-placeholder.jpg"
tags: ["astro", "typescript", "content"]
draft: false
---
```

### VitePress Page

```yaml
---
title: API Reference
editLink: true
lastUpdated: true
aside: true
outline: deep
prev:
  text: "Getting Started"
  link: /guide/getting-started
next:
  text: "Configuration"
  link: /guide/configuration
---
```

### Docusaurus Doc

```yaml
---
id: intro
title: Introduction
sidebar_label: Intro
sidebar_position: 1
description: Project introduction
keywords:
  - docs
  - tutorial
tags:
  - Getting started
---
```

---

## API Documentation

### OpenAPI Spec Reference

```yaml
---
type: api-reference
title: "Users API"
version: "1.0.0"
base_path: /api/v1/users
authentication: bearer
rate_limit: 100/minute
endpoints:
  - method: GET
    path: /
    summary: List users
  - method: POST
    path: /
    summary: Create user
  - method: GET
    path: /{id}
    summary: Get user
---
```

---

## Complex Nested Example

```yaml
---
type: feature-bundle
bundle_id: "v2.0-release"
version: "1.0.0"
status: planning
created: 2026-01-25
features:
  - id: "026-knowledge-infrastructure"
    status: in-progress
    completion: 60
  - id: "027-api-v2"
    status: todo
    completion: 0
  - id: "028-mobile-app"
    status: backlog
    completion: 0
metrics:
  target_date: 2026-Q2
  success_criteria:
    - metric: MAU
      target: 10000
    - metric: NPS
      target: 50
team:
  lead: "Ruslan Faion"
  members:
    - role: frontend
      count: 2
    - role: backend
      count: 1
    - role: design
      count: 1
---
```

---

## Minimal Examples

### Absolute Minimum (Not Recommended)

```yaml
---
type: note
---
```

### Recommended Minimum

```yaml
---
type: spec
version: "1.0.0"
status: draft
created: 2026-01-25
---
```

---

## Anti-Patterns (What NOT to Do)

### Invalid YAML

```yaml
---
# BAD: Tab indentation
type:	spec
# BAD: No space after colon
version:1.0.0
# BAD: Unquoted version (parsed as float)
version: 1.0
# BAD: Invalid date format
created: 25-01-2026
# BAD: Comma-separated instead of array
tags: a, b, c
---
```

### Correct Version

```yaml
---
type: spec
version: "1.0.0"
created: 2026-01-25
tags: [a, b, c]
---
```

---

*yaml-frontmatter/examples.md v1.0.0 - 2026-01-25*
