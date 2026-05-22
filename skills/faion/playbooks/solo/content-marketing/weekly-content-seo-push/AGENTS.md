---
slug: weekly-content-seo-push
tier: solo
group: content-marketing
persona: P1
goal: TBD
complexity: light
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Empty content slot → 1 indexed asset live each week (blog / changelog / doc).
content_id: 38a3350faa3a7940
methodology_refs:
  - growth-seo-fundamentals
  - seo-basics
  - seo-techniques
  - topical-authority
  - growth-content-marketing
  - growth-copywriting-fundamentals
  - zero-click-search-adaptation
  - search-everywhere-optimization
  - growth-hacker-news-launch
  - growth-indiehackers-strategy
---

# Weekly content and SEO atomic push

**Playbook slug:** `weekly-content-seo-push`  
**Tier:** solo  
**Complexity:** light  
**Persona:** P1 — Solo SaaS Builder

## Intent

Empty content slot → 1 indexed asset live each week (blog / changelog / doc).

## Scope

Solo founder ships one indexed asset per week (blog post, changelog, doc page): topic chosen against keyword + ICP, draft generated with AI then human-edited, on-page SEO complete, shared on 2 channels. Exit artifact is indexable URL + 2 shares.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a single-operator SaaS founder. It assumes no team, no SRE rotation, no co-founder. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill — solo founders drift fastest where stages don't end cleanly.

### Non-goals

- Long-tail SEO campaigns — separate quarterly
- Paid distribution — organic only here

### Prerequisites

- Blog/docs infrastructure live (sitemap, indexable)
- Keyword + ICP shortlist exists

## Success criteria

The playbook is done when:
- 1 asset published per week with on-page SEO complete
- Asset shared on 2 channels (Reddit / IH / HN / X / LinkedIn)
- Asset indexed within 7 days (Search Console)
- Internal link added from 1 existing page

## Stages

### Stage 1: Pick topic

**Intent:** Pick a topic that hits keyword + ICP at once.

**Tasks:**
- Scan keyword shortlist
- Pick topic with monthly volume + low difficulty
- Tag ICP segment

**Methodologies in chain:**
- `growth-seo-fundamentals` → `solo/marketing/seo-manager/growth-seo-fundamentals`
- `seo-basics` → `solo/marketing/seo-manager/seo-basics`
- `seo-techniques` → `solo/marketing/seo-manager/seo-techniques`
- `topical-authority` → `solo/marketing/seo-manager/topical-authority`

**Outputs:**
- Topic brief

**Decision gate:**
> Advance when topic has keyword + ICP fit. Refuse generic 'just write something'.

### Stage 2: Draft

**Intent:** AI draft + human edit. Voice matters more than length.

**Tasks:**
- Generate AI draft from brief
- Human-edit for voice
- Add concrete examples + screenshots

**Methodologies in chain:**
- `growth-content-marketing` → `solo/marketing/content-marketer/growth-content-marketing`
- `growth-copywriting-fundamentals` → `solo/marketing/content-marketer/growth-copywriting-fundamentals`

**Outputs:**
- Draft v1

**Decision gate:**
> Advance when voice reads as human + concrete. Stay if it sounds AI-generic.

### Stage 3: Optimise

**Intent:** On-page SEO + zero-click adaptation.

**Tasks:**
- Title + meta + H1 + URL slug
- Internal links + structured data
- Adapt for zero-click answer extraction

**Methodologies in chain:**
- `zero-click-search-adaptation` → `solo/marketing/seo-manager/zero-click-search-adaptation`
- `search-everywhere-optimization` → `solo/marketing/content-marketer/search-everywhere-optimization`

**Outputs:**
- Published asset

**Decision gate:**
> Advance when on-page checklist complete. Refuse to publish without title/meta.

### Stage 4: Share

**Intent:** Distribute on 2 channels matching topic.

**Tasks:**
- Pick 2 channels matching ICP
- Post with native angle (not link-drop)
- Engage with first 5 replies

**Methodologies in chain:**
- `growth-hacker-news-launch` → `solo/marketing/gtm-strategist/growth-hacker-news-launch`
- `growth-indiehackers-strategy` → `solo/marketing/gtm-strategist/growth-indiehackers-strategy`

**Outputs:**
- 2 channel posts

**Decision gate:**
> Required output: 2 distribution posts. Without distribution, indexing is the only chance.

## Common pitfalls

- Publishing without distribution — indexing alone doesn't move needle solo-scale
- AI-generic drafts — readers detect tone instantly, refuse to share

## Quality checklist (self-review)

- Could I share this with my ICP without cringing at AI-tells?
- Did the post get indexed within 7 days, or is something broken in the sitemap?

## Related playbooks

- `monthly-competitor-scan`
- `sunday-roadmap-ritual`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **solo-content-calendar-template** (tier `solo`, blocks stage 1) — Pick-topic stage needs ready-to-fill content calendar
- **on-page-seo-checklist-2026** (tier `solo`, blocks stage 3) — Optimise stage needs 2026-current on-page SEO checklist

## CLI usage

```
faion get-content weekly-content-seo-push --format md       # human-readable rendering
faion get-content weekly-content-seo-push --format context  # agent-optimised context bundle
faion get-content weekly-content-seo-push --format json     # raw structured form
```
