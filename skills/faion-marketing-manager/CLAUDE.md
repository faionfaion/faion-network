# Marketing Manager Orchestrator

> **Entry Point:** Invoked via [/faion-net](../faion-net/CLAUDE.md) or directly as `/faion-marketing-manager`

## Overview

Marketing orchestrator that coordinates 4 specialized sub-skills for all marketing activities.

**Architecture:** Orchestrator | **Sub-Skills:** 4 | **Total Methodologies:** 82

## Sub-Skills

| Sub-Skill | Purpose | Methods | Status |
|-----------|---------|---------|--------|
| [faion-gtm-strategist](../faion-gtm-strategist/) | GTM, launches, positioning, pricing | 26 | Ready |
| [faion-content-marketer](../faion-content-marketer/) | Content, copywriting, SEO, email, social | 16+30 | Ready |
| [faion-growth-marketer](../faion-growth-marketer/) | Analytics, experiments, A/B testing, AARRR | 30 | Ready |
| [faion-conversion-optimizer](../faion-conversion-optimizer/) | Landing pages, CRO, funnels, PLG | 13 | Ready |

<<<<<<< HEAD
| Field | Value |
|-------|-------|
| Name | faion-marketing-manager |
| User-invocable | No |
| Methodologies | 86 total |
| References | 9 technical guides |
=======
## When to Use
>>>>>>> claude

| Task Type | Route To |
|-----------|----------|
| Product launch, GTM strategy | faion-gtm-strategist |
| Content creation, email, social | faion-content-marketer |
| Analytics, growth experiments | faion-growth-marketer |
| Landing pages, CRO, funnels | faion-conversion-optimizer |

## Files

<<<<<<< HEAD
## Directory Structure

```
faion-marketing-manager/
├── SKILL.md                    # Main skill (decision trees, category summaries)
├── CLAUDE.md                   # This file
├── methodologies/              # 77 methodology files
│   ├── *.md                   # Growth metrics (20 files)
│   ├── ads/                   # Paid advertising (16 files)
│   ├── growth/                # Marketing growth (35 files)
│   └── operations/            # Business operations (14 files)
└── references/                 # Technical reference guides (9 files)
    └── methodologies-detail.md # Detailed frameworks (72 inline methodologies)
```

## Key Files

### Main Skill

| File | Description | Lines |
|------|-------------|-------|
| [SKILL.md](SKILL.md) | Decision trees, methodology categories, workflows | ~500 |

### References

| File | Description | Lines |
|------|-------------|-------|
| [methodologies-detail.md](references/methodologies-detail.md) | Detailed methodology frameworks (GTM, Landing, Content, Email, Ads, Social, Growth) | ~1200 |
| [seo.md](references/seo.md) | Technical SEO, AEO, Core Web Vitals | ~560 |
| [seo-2026.md](references/seo-2026.md) | GEO, AEO, Zero-Click, AI Content, Topical Authority | ~250 |
| [google-ads.md](references/google-ads.md) | Google Ads API, Search, Display, Performance Max | ~1470 |
| [meta-ads.md](references/meta-ads.md) | Meta Marketing API for Facebook/Instagram | ~1100 |
| [analytics.md](references/analytics.md) | GA4, Plausible, Mixpanel, PostHog integration | ~1470 |
| [image-generation.md](references/image-generation.md) | DALL-E, Midjourney, FLUX, Stable Diffusion | ~1300 |
| [video-generation.md](references/video-generation.md) | Sora, Runway, Pika, Kling video AI | ~860 |
| [audio-production.md](references/audio-production.md) | TTS, STT, voice cloning, podcast production | ~1300 |

**Total reference material:** ~9,500 lines

## Decision Trees (in SKILL.md)

SKILL.md contains 5 decision trees for methodology selection:

1. **Main Decision Tree** - What marketing goal? (Launch, Acquire, Convert, Retain, Grow, Analyze)
2. **Channel Selection** - B2B, B2C, Developers, Local audiences
3. **Content Type Selection** - By funnel stage (TOFU, MOFU, BOFU, Retention)
4. **Landing Page Optimization** - By conversion problem
5. **Email Strategy** - By subscriber type

## Methodology Categories (in SKILL.md)

| Category | Count | When to Use |
|----------|-------|-------------|
| GTM Strategy | 12 | Launching product, entering market |
| Landing Page | 12 | Creating/optimizing landing pages |
| Content Marketing | 12 | Building organic traffic, SEO |
| Email Marketing | 12 | Lead nurturing, retention |
| Paid Advertising | 12 | Quick acquisition, scaling |
| Social Media | 6 | Brand awareness, community |
| Growth & Operations | 6 | Scaling, experimentation |
| Modern SEO & AI | 14 | SEO 2026+, AI content, GEO/AEO |

## Subfolders

| Folder | Description | Files |
|--------|-------------|-------|
| [methodologies/](methodologies/) | All methodology files organized by category | 77 files |
| [methodologies/ads/](methodologies/ads/) | Meta, Google, LinkedIn ads setup and optimization | 16 files |
| [methodologies/growth/](methodologies/growth/) | Marketing channels, GTM, social media, SEO | 35 files |
| [methodologies/operations/](methodologies/operations/) | Pricing, subscriptions, legal, financial planning | 14 files |
| [references/](references/) | Technical API guides and tool references | 9 files |

## Workflows

### 1. GTM Manifest Creation

```
Read product research -> AskUserQuestion (sales model, timeline) -> Generate 12 sections -> Combine into gtm-manifest-full.md
```

### 2. Landing Page Creation

```
Discovery -> Copy (AIDA/PAS) -> Design -> Implementation -> Analysis
```

### 3. Content Marketing

```
Keyword Research -> Content Plan -> Creation -> Optimization -> Distribution
```

### 4. Growth Experiments

```
Hypothesis -> Experiment Design -> Run -> Analyze -> Learn -> Iterate
```
=======
| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Orchestrator routing logic |
| [workflows.md](workflows.md) | Cross-skill workflows |
| [methodologies-index.md](methodologies-index.md) | Complete methodology index |
| [quick-reference.md](quick-reference.md) | Quick reference tables |
| references/ | Shared technical references (analytics, ads, SEO) |
>>>>>>> claude

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-net](../faion-net/CLAUDE.md) | Parent orchestrator |
| [faion-ppc-manager](../faion-ppc-manager/) | Paid advertising specialist |
| [faion-seo-manager](../faion-seo-manager/) | SEO specialist |
| [faion-smm-manager](../faion-smm-manager/) | Social media specialist |

---

<<<<<<< HEAD
*Marketing Domain Skill v1.1 | 86 Methodologies | 6 Agents*
=======
*Marketing Orchestrator v2.0 | 4 Sub-Skills | 82 Methodologies*
>>>>>>> claude
