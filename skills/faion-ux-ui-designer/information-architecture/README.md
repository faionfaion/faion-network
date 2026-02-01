---
id: ia-templates
name: "Information Architecture - Templates"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Information Architecture - Templates

## Metadata
- **Category:** UX / Design Methods
- **Difficulty:** Intermediate
- **Tags:** #methodology #ux #design #information-architecture #templates
- **Agent:** faion-ux-researcher-agent

---

## Templates

### IA Strategy Document

```markdown
# Information Architecture Strategy

**Project:** [Name]
**Version:** [Number]
**Date:** [Date]

## Overview

**Product type:** [Website / Application / etc.]
**Content volume:** [Approximate pages/items]
**Expected growth:** [How content will grow]

## Research Summary

### User Insights
- Primary user goal: [Goal]
- Secondary goals: [Goals]
- Common mental models: [How users think about content]

### Content Insights
- Total content items: [Number]
- Content types: [Types]
- Relationships: [How content connects]

### Business Requirements
- Priority content: [What's most important]
- Governance: [Who owns what]
- Constraints: [Technical, political]

## Organization Approach

### Primary Scheme
**Scheme:** [Topic / Task / Audience / etc.]
**Rationale:** [Why this approach]

### Category Structure

**Level 1 Categories:**
1. [Category]
   - [Subcategory]
   - [Subcategory]
2. [Category]
   - [Subcategory]
   - [Subcategory]

### Cross-Cutting Tags
- [Tag group 1]: [Tags]
- [Tag group 2]: [Tags]

## Navigation Design

### Global Navigation
[Items that appear everywhere]

### Section Navigation
[How navigation works within sections]

### Contextual Links
[Related content strategy]

## Labeling Guidelines

| Label Type | Guidelines | Examples |
|------------|------------|----------|
| Categories | [Rules] | [Examples] |
| Actions | [Rules] | [Examples] |
| Status | [Rules] | [Examples] |

## Search Strategy

- Primary search: [How it works]
- Filters: [Available filters]
- Facets: [If applicable]

## Scalability Plan

How structure accommodates:
- New content: [Approach]
- New categories: [Approach]
- Content retirement: [Approach]

## Validation Plan

- [ ] Card sorting for categories
- [ ] Tree testing for findability
- [ ] Usability testing for navigation
```

### Sitemap Template

```markdown
# Sitemap: [Site Name]

**Version:** [Number]
**Date:** [Date]

## Legend
- (**) Priority page
- (L) Login required
- (NEW) New in this version

## Site Structure

```
Home (*)
│
├── Products (*)
│   ├── Category A
│   │   ├── Product 1
│   │   └── Product 2
│   └── Category B
│       └── Product 3
│
├── Solutions
│   ├── By Industry
│   │   ├── Healthcare
│   │   └── Finance
│   └── By Size
│       ├── Enterprise
│       └── Small Business
│
├── Resources
│   ├── Blog
│   ├── Guides (*)
│   ├── Webinars
│   └── Case Studies
│
├── Company
│   ├── About
│   ├── Careers
│   ├── Press
│   └── Contact (*)
│
├── Support (*)
│   ├── Help Center
│   ├── Documentation
│   ├── Community
│   └── Contact Support
│
└── Account (L)
    ├── Dashboard
    ├── Settings
    └── Billing
```

## Page Inventory

| Page | URL | Priority | Template | Owner |
|------|-----|----------|----------|-------|
| Home | / | High | Homepage | Marketing |
| Products | /products | High | Listing | Product |
```

### Taxonomy Document

```markdown
# Taxonomy: [Site Name]

## Content Types

| Type | Description | Attributes |
|------|-------------|------------|
| Article | Blog/news content | Title, body, date, author, category |
| Product | Product pages | Name, description, specs, price |
| Help | Support content | Title, body, category, tags |

## Categories

### Primary Categories

| Category | Description | Parent |
|----------|-------------|--------|
| [Category 1] | [What it contains] | None |
| [Subcategory 1a] | [What it contains] | Category 1 |

### Tags

| Tag Group | Tags | Applied To |
|-----------|------|------------|
| Topic | [List of tags] | Articles |
| Feature | [List of tags] | Products |
| Difficulty | Beginner, Intermediate, Advanced | Help |

## Naming Conventions

### Rules
1. Use sentence case
2. Avoid jargon
3. Be specific
4. Keep short (2-4 words)

### Examples

| Bad | Good | Why |
|-----|------|-----|
| Solutions | Marketing Tools | More specific |
| Resources | Guides & Templates | Clearer content |
| Miscellaneous | Never use | Everything needs a home |
```

---

## Examples

### Example 1: E-commerce IA

**Organization scheme:** Task-based (Shop, Learn, Get Help)

```
Shop
├── By Category (Clothing, Electronics, Home)
├── By Brand
└── Sale Items

Learn
├── Buying Guides
├── Style Tips
└── Product Reviews

Get Help
├── Order Status
├── Returns
└── Contact Us
```

### Example 2: SaaS Product IA

**Organization scheme:** User journey (Discover, Build, Grow)

```
Discover
├── Features
├── Solutions
├── Pricing

Build
├── Documentation
├── API Reference
├── Tutorials

Grow
├── Case Studies
├── Best Practices
├── Community
```

---

## Common IA Patterns

### Mega Menu

```
Products ▼
┌─────────────────────────────────────┐
│ Category A    Category B    Featured│
│ ├ Item        ├ Item        [Image] │
│ ├ Item        ├ Item                │
│ └ Item        └ Item        View All│
└─────────────────────────────────────┘
```
Best for: Large sites with many products

### Hub and Spoke

```
      ┌───────┐
      │  Hub  │
      └───┬───┘
    ┌─────┼─────┐
    ▼     ▼     ▼
  Spoke Spoke Spoke
```
Best for: Task-focused applications

### Flat Structure

```
Home → Page → Page → Page
         └── Page
         └── Page
```
Best for: Small sites, marketing pages

---

## Tools

| Tool | Use |
|------|-----|
| **OmniGraffle** | Sitemaps, diagrams |
| **Miro/FigJam** | Collaborative IA work |
| **Whimsical** | Quick sitemaps |
| **Optimal Workshop** | Card sorting, tree testing |
| **Airtable/Notion** | Taxonomy management |

---

## Checklist

Research phase:
- [ ] Content inventory complete
- [ ] User research conducted
- [ ] Business goals documented
- [ ] Mental models understood

Strategy phase:
- [ ] Organization scheme chosen
- [ ] Primary categories defined
- [ ] Taxonomy documented
- [ ] Navigation types identified

Design phase:
- [ ] Sitemap created
- [ ] Labels defined
- [ ] Navigation designed
- [ ] Search strategy planned

Validation phase:
- [ ] Card sorting conducted
- [ ] Tree testing completed
- [ ] Navigation tested
- [ ] Iterations made

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Information architecture strategy | opus | Strategic design: planning complete IA for complex applications |

## Sources

- [IA Deliverables](https://www.nngroup.com/articles/ia-deliverables/) - Nielsen Norman Group
- [Practical Information Architecture](https://alistapart.com/article/thedisciplineofcontentstrategy/) - A List Apart
- [IA Templates and Tools](https://www.usability.gov/how-to-and-tools/methods/information-architecture.html) - Usability.gov
- [Creating IA Documentation](https://www.interaction-design.org/literature/article/information-architecture-deliverables) - IDF guide
- [IA Tools Comparison](https://xd.adobe.com/ideas/process/information-architecture/) - Adobe XD resources
