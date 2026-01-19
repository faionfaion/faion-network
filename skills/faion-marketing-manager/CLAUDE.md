# Marketing Manager Skill

## Overview

Marketing domain skill that orchestrates all marketing activities from go-to-market strategy to growth experiments. Covers GTM planning, landing pages, content marketing, SEO/SEM, GEO/AEO, paid ads (Google, Meta, LinkedIn), email marketing, social media, and growth hacking.

**Purpose:** Complete marketing orchestration for startups and digital products.

**Communication:** User's language. Content: target audience language.

## Skill Metadata

| Field | Value |
|-------|-------|
| Name | faion-marketing-manager |
| User-invocable | No |
| Methodologies | 77 total |
| References | 8 technical guides |

## Agents

| Agent | Purpose |
|-------|---------|
| faion-landing-agent | Landing page orchestrator (analyze, copy, design modes) |
| faion-content-agent | Content marketing, SEO |
| faion-email-agent | Email marketing campaigns |
| faion-social-agent | Social media marketing |
| faion-growth-agent | Growth hacking, experiments |
| faion-ads-agent | Paid advertising (Meta, Google, LinkedIn) |

## Directory Structure

```
faion-marketing-manager/
├── SKILL.md                    # Main skill definition
├── CLAUDE.md                   # This file
├── methodologies/              # 77 methodology files
│   ├── M-GRO-*.md             # Growth methodologies (12 files)
│   ├── ads/                   # Paid advertising (16 files)
│   ├── growth/                # Marketing growth (32 files)
│   └── operations/            # Business operations (14 files)
└── references/                 # Technical reference guides (8 files)
```

## Subfolders

| Folder | Description | Files |
|--------|-------------|-------|
| [methodologies/](methodologies/) | All methodology files organized by category | 74 files |
| [methodologies/ads/](methodologies/ads/) | Meta, Google, LinkedIn ads setup and optimization | 16 files |
| [methodologies/growth/](methodologies/growth/) | Marketing channels, GTM, social media, SEO | 32 files |
| [methodologies/operations/](methodologies/operations/) | Pricing, subscriptions, legal, financial planning | 14 files |
| [references/](references/) | Technical API guides and tool references | 8 files |

## Key Files

### Main Skill

| File | Description |
|------|-------------|
| [SKILL.md](SKILL.md) | Complete skill definition with all 72 inline methodologies |

### Growth Methodologies (Root)

| File | Description |
|------|-------------|
| M-GRO-001_aarrr_pirate_metrics.md | AARRR funnel framework (Acquisition, Activation, Retention, Revenue, Referral) |
| M-GRO-002_north_star_metric.md | Single metric that captures core customer value |
| M-GRO-003_growth_loops.md | Self-reinforcing growth mechanisms |
| M-GRO-004_ab_testing_framework.md | Systematic experimentation methodology |
| M-GRO-005_multivariate_testing.md | Testing multiple variables simultaneously |
| M-GRO-006_statistical_significance.md | Ensuring experiment validity |
| M-GRO-007_cohort_analysis.md | Analyzing user groups over time |
| M-GRO-008_funnel_optimization.md | Improving conversion at each stage |
| M-GRO-009_viral_coefficient.md | Measuring and improving virality |
| M-GRO-010_product_led_growth.md | Growth driven by product experience |
| M-GRO-011_activation_rate.md | First-value experience optimization |
| M-GRO-012_retention_loops.md | Mechanisms to keep users returning |

### References

| File | Description | Lines |
|------|-------------|-------|
| [seo.md](references/seo.md) | Technical SEO, AEO, Core Web Vitals | ~560 |
| [seo-2026.md](references/seo-2026.md) | GEO, AEO, Zero-Click, AI Content, Topical Authority | ~250 |
| [google-ads.md](references/google-ads.md) | Google Ads API, Search, Display, Performance Max | ~1470 |
| [meta-ads.md](references/meta-ads.md) | Meta Marketing API for Facebook/Instagram | ~1100 |
| [analytics.md](references/analytics.md) | GA4, Plausible, Mixpanel, PostHog integration | ~1470 |
| [image-generation.md](references/image-generation.md) | DALL-E, Midjourney, FLUX, Stable Diffusion | ~1300 |
| [video-generation.md](references/video-generation.md) | Sora, Runway, Pika, Kling video AI | ~860 |
| [audio-production.md](references/audio-production.md) | TTS, STT, voice cloning, podcast production | ~1300 |

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

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-research-domain-skill | Provides market data for marketing |
| faion-product-domain-skill | Provides product positioning |
| faion-seo-skill | SEO optimization details |
| faion-analytics-skill | Analytics integration |

---

*Marketing Domain Skill v1.0 | 77 Methodologies | 8 Agents*
