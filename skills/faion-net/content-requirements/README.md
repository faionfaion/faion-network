# Content Requirements Document

## Overview

This document defines content standards for faion-network articles covering 605 methodologies across 18 domain skills. All content targets Claude Code users and AI-assisted development practitioners.

---

## 1. Article Levels (Tiers)

### Level 1: Introduction (L1)

| Attribute | Specification |
|-----------|---------------|
| Word Count | 800-1,200 words |
| Audience | Beginners, first-time users |
| Purpose | Overview, awareness, orientation |
| Reading Time | 4-6 minutes |
| Token Est. | ~8k-15k generation |

**Content Focus:**
- What is this methodology/concept?
- Why does it matter?
- When to use it?
- Key benefits (3-5 points)
- Next steps / related resources

**Title Formats:**
- "What is [Methodology]? A Beginner's Guide"
- "Introduction to [Concept] for Claude Code Users"
- "[Methodology] Explained: Getting Started"

**Required Sections:**
1. Introduction (100-150 words)
2. What is [Topic]? (200-300 words)
3. Key Benefits (150-200 words)
4. When to Use (150-200 words)
5. Getting Started (100-150 words)
6. Conclusion + Next Steps (100-150 words)

---

### Level 2: Practical Guide (L2)

| Attribute | Specification |
|-----------|---------------|
| Word Count | 1,500-2,500 words |
| Audience | Intermediate users with basic knowledge |
| Purpose | How-to implementation, practical application |
| Reading Time | 8-12 minutes |
| Token Est. | ~15k-30k generation |

**Content Focus:**
- Step-by-step implementation
- Real code examples
- Common patterns and anti-patterns
- Troubleshooting tips
- Best practices

**Title Formats:**
- "How to [Action] with [Methodology]"
- "[Methodology] in Practice: A Step-by-Step Guide"
- "Implementing [Concept]: Practical Examples"

**Required Sections:**
1. Introduction + Prerequisites (150-200 words)
2. Concept Overview (200-300 words)
3. Step-by-Step Implementation (600-1000 words)
   - Step 1: [Action]
   - Step 2: [Action]
   - Step 3: [Action]
4. Code Examples (300-500 words with code blocks)
5. Common Mistakes to Avoid (200-300 words)
6. Best Practices (150-250 words)
7. Conclusion + Further Reading (100-150 words)

---

### Level 3: Deep Dive (L3)

| Attribute | Specification |
|-----------|---------------|
| Word Count | 3,000-5,000 words |
| Audience | Advanced users, specialists |
| Purpose | Comprehensive understanding, expert guidance |
| Reading Time | 15-25 minutes |
| Token Est. | ~30k-60k generation |

**Content Focus:**
- In-depth analysis of methodology
- Multiple implementation approaches
- Performance considerations
- Edge cases and advanced patterns
- Integration strategies
- Comparison with alternatives

**Title Formats:**
- "The Complete Guide to [Methodology]"
- "Mastering [Concept]: Advanced Techniques"
- "[Methodology] Deep Dive: From Basics to Expert"

**Required Sections:**
1. Executive Summary (150-200 words)
2. Introduction + Context (300-400 words)
3. Foundational Concepts (400-600 words)
4. Core Implementation (800-1200 words)
   - Approach A
   - Approach B
   - Approach comparison
5. Advanced Patterns (600-800 words)
6. Performance & Optimization (300-500 words)
7. Real-World Case Studies (400-600 words)
8. Integration Strategies (300-400 words)
9. Troubleshooting Guide (200-300 words)
10. Conclusion + Resources (150-200 words)

---

### Level 4: Pillar Page (L4)

| Attribute | Specification |
|-----------|---------------|
| Word Count | 5,000-10,000 words |
| Audience | All levels (comprehensive reference) |
| Purpose | Authoritative resource, SEO pillar, link hub |
| Reading Time | 25-50 minutes |
| Token Est. | ~60k-120k generation |

**Content Focus:**
- Definitive guide on topic cluster
- Links to all related L1-L3 articles
- Covers full methodology lifecycle
- Industry context and trends
- Comprehensive FAQ
- Glossary of terms

**Title Formats:**
- "The Ultimate Guide to [Topic Cluster]"
- "[Methodology]: Everything You Need to Know"
- "Complete [Domain] Handbook for [Year]"

**Required Sections:**
1. Table of Contents (auto-generated)
2. Executive Summary (200-300 words)
3. Introduction + Industry Context (400-500 words)
4. Fundamentals Section (1000-1500 words)
   - Core concepts
   - Terminology
   - Historical context
5. Methodology Deep Dives (2000-3000 words)
   - Sub-topic A (link to L2/L3)
   - Sub-topic B (link to L2/L3)
   - Sub-topic C (link to L2/L3)
6. Implementation Framework (800-1200 words)
7. Tools & Technologies (500-800 words)
8. Best Practices Summary (400-600 words)
9. Common Challenges & Solutions (400-600 words)
10. Future Trends (300-400 words)
11. FAQ Section (500-800 words, 10-15 questions)
12. Glossary (200-400 words)
13. Resources & Further Reading (200-300 words)

---

## 2. Content Standards

### 2.1 Writing Style

| Guideline | Description |
|-----------|-------------|
| Tone | Professional, accessible, actionable |
| Voice | Active voice preferred (80%+) |
| Person | Second person ("you") for instructions |
| Sentences | 15-25 words average, max 40 words |
| Paragraphs | 3-5 sentences, single topic focus |
| Jargon | Define on first use, include in glossary |

### 2.2 Formatting Standards

**Headings:**
- H1: Article title only (1 per article)
- H2: Major sections
- H3: Sub-sections
- H4: Minor points (use sparingly)

**Lists:**
- Bullet lists for 3+ unordered items
- Numbered lists for sequential steps
- Max 7 items per list (chunk if more)

**Tables:**
- Use for comparisons, specifications, matrices
- Always include header row
- Keep under 6 columns for readability

**Code Blocks:**
- Always specify language
- Include comments for complex logic
- Max 50 lines per block (split if longer)
- Provide context before code

### 2.3 SEO Requirements

**Title:**
- 50-60 characters
- Include primary keyword
- Action-oriented when possible

**Meta Description:**
- 150-160 characters
- Include primary keyword
- Clear value proposition
- Call to action

**Keywords:**
- 1 primary keyword (in title, H1, first paragraph)
- 2-3 secondary keywords (in H2s, naturally distributed)
- 5-10 related terms (throughout content)

**Keyword Density:**
- Primary: 1-2% (10-20 occurrences per 1000 words)
- Secondary: 0.5-1% each
- Avoid keyword stuffing

**URL Structure:**
- Lowercase
- Hyphens for spaces
- Include primary keyword
- Max 60 characters
- Pattern: `/blog/[category]/[slug]`

### 2.4 Internal Linking

| Content Level | Min Internal Links |
|---------------|-------------------|
| L1 | 3-5 links |
| L2 | 5-8 links |
| L3 | 8-12 links |
| L4 | 15-25 links |

**Link Placement:**
- First mention of related topic
- "Related articles" section
- Contextual in-content links
- Anchor text = descriptive (not "click here")

**Link Strategy:**
- L4 pillar links to multiple L2/L3
- L2/L3 link up to L4 pillar
- L1 links to L2 practical guides
- Cross-cluster linking for related topics

### 2.5 Visual Requirements

| Content Level | Images | Diagrams | Code Samples |
|---------------|--------|----------|--------------|
| L1 | 1-2 | 0-1 | 0-1 |
| L2 | 2-4 | 1-2 | 2-4 |
| L3 | 3-5 | 2-3 | 4-8 |
| L4 | 5-10 | 3-5 | 5-10 |

**Image Standards:**
- Alt text required (descriptive, include keyword)
- WebP format preferred
- Max width: 1200px
- Compressed (<200KB)
- Descriptive filename: `methodology-name-diagram.webp`

**Diagram Types:**
- Flowcharts for processes
- Architecture diagrams for systems
- Comparison matrices for alternatives
- Timeline for evolution/roadmaps

**Code Sample Standards:**
- Working, tested code
- Comments explaining key parts
- Copy button enabled
- Syntax highlighting
- Context before/after

### 2.6 Quality Checklist

**Pre-Publication:**
- [ ] Title includes primary keyword (50-60 chars)
- [ ] Meta description written (150-160 chars)
- [ ] All required sections present for level
- [ ] Word count within range for level
- [ ] Minimum internal links added
- [ ] All images have alt text
- [ ] Code samples tested
- [ ] Grammar and spell check passed
- [ ] Reading level appropriate (Grade 8-12)
- [ ] Mobile preview checked

**Technical:**
- [ ] URL follows pattern
- [ ] Schema markup added (Article/HowTo)
- [ ] Open Graph tags set
- [ ] Canonical URL set
- [ ] No broken links

**SEO:**
- [ ] Primary keyword in title
- [ ] Primary keyword in first 100 words
- [ ] Keywords in H2 headings
- [ ] Keyword density 1-2%
- [ ] No duplicate content

---

## 3. Audience Segments

### 3.1 Claude Code Beginners

**Profile:**
- New to Claude Code (<1 month)
- Basic programming knowledge
- Learning AI-assisted development
- Looking for quick wins

**Content Preferences:**
- L1 introduction articles
- Step-by-step tutorials
- Video supplements
- Glossary/terminology guides

**Topics of Interest:**
- Getting started with Claude Code
- Basic prompting techniques
- Setting up development environment
- Understanding CLAUDE.md
- Simple automation tasks

**Tone & Style:**
- Encouraging, patient
- No assumed knowledge
- Plenty of examples
- Quick wins emphasized

---

### 3.2 Intermediate Developers

**Profile:**
- 1-6 months Claude Code experience
- Comfortable with basic features
- Building production workflows
- Exploring advanced features

**Content Preferences:**
- L2 practical guides
- L3 deep dives for specific topics
- Best practices articles
- Comparison articles

**Topics of Interest:**
- Custom skills creation
- MCP server integration
- Advanced prompting
- Workflow optimization
- Testing strategies
- API integrations (LLMs, RAG)

**Tone & Style:**
- Assume basic knowledge
- Focus on efficiency
- Include tradeoffs
- Real-world scenarios

---

### 3.3 Senior Developers / Architects

**Profile:**
- 6+ months AI-assisted dev experience
- Team leadership responsibilities
- Architecting AI workflows
- Evaluating tools and approaches

**Content Preferences:**
- L3 deep dives
- L4 pillar pages
- Architecture guides
- Performance optimization
- Enterprise patterns

**Topics of Interest:**
- Multi-agent architectures
- Enterprise deployment
- Security & compliance
- Cost optimization
- Team workflow design
- Custom framework development

**Tone & Style:**
- Technical depth expected
- Show don't tell
- Include metrics/data
- Discuss tradeoffs explicitly

---

### 3.4 Tech Leads / Project Managers

**Profile:**
- Managing teams using AI tools
- Evaluating ROI of AI adoption
- Setting processes and standards
- Non-coding but technical background

**Content Preferences:**
- L1 overviews for new topics
- L4 comprehensive guides
- Strategy articles
- Case studies with metrics

**Topics of Interest:**
- AI adoption strategy
- Team productivity metrics
- Process integration
- Risk management
- Cost-benefit analysis
- Training programs

**Tone & Style:**
- Business impact focus
- Clear recommendations
- Include decision frameworks
- Metrics and outcomes

---

## 4. Content Taxonomy

### 4.1 Primary Categories

| Category | Description | Target Skills |
|----------|-------------|---------------|
| Development | Coding, APIs, testing | software-developer, devops |
| AI/ML | LLMs, RAG, embeddings | ml-engineer, claude-code |
| Product | MVP, roadmaps, analytics | product-manager, researcher |
| Project | PM tools, risk, agile | project-manager, ba |
| Design | UX research, accessibility | ux-ui-designer |
| Marketing | SEO, content, growth | marketing-manager, seo, smm, ppc |
| Strategy | Architecture, decisions | software-architect, sdd |
| Communication | Stakeholders, feedback | communicator, hr-recruiter |

### 4.2 Topic Clusters

Each L4 pillar page anchors a topic cluster containing related L1-L3 articles.

**Cluster Structure:**
```
L4 Pillar
├── L3 Deep Dive A
│   ├── L2 How-To A1
│   └── L2 How-To A2
├── L3 Deep Dive B
│   └── L2 How-To B1
└── L1 Overview C
```

### 4.3 Content Tags

**Topic Tags:**
- claude-code, ai-development, llm, rag, mcp
- python, typescript, react, api
- devops, docker, kubernetes, ci-cd
- ux, accessibility, usability
- seo, content-marketing, growth
- agile, scrum, project-management

**Skill Tags:**
- One tag per source skill (e.g., faion-software-developer)

**Level Tags:**
- beginner, intermediate, advanced, reference

---

## 5. Article Frontmatter Template

```yaml
---
title: "Article Title Here"
slug: "article-slug-here"
description: "Meta description 150-160 characters with primary keyword."
level: L2  # L1, L2, L3, L4
category: development
tags:
  - claude-code
  - python
  - api
skill: faion-software-developer
methodologies:
  - api-rest-design.md
  - api-error-handling.md
keywords:
  primary: "rest api design"
  secondary:
    - "api best practices"
    - "claude code api"
author: faion-network
publishDate: 2026-01-24
lastUpdated: 2026-01-24
readingTime: 10  # minutes
wordCount: 2000
---
```

---

## 6. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-24 | Initial document creation |

---

*faion-network content-requirements v1.0*
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement methodology | haiku | Pattern application and configuration |
| Review implementation | sonnet | Code analysis and verification |
| Design strategy | opus | Complex decision-making |

