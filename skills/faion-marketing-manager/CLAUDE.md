# Marketing Manager Orchestrator

> **Entry Point:** Invoked via [/faion-net](../faion-net/CLAUDE.md) or directly as `/faion-marketing-manager`

## Overview

Pure orchestrator that coordinates all marketing activities by routing to specialized sub-skills. Contains NO methodologies - all execution happens in sub-skills.

**Architecture:** Pure Orchestrator | **Sub-Skills:** 7 | **Total Methodologies:** 85+

## Sub-Skills

| Sub-Skill | Purpose | Methods | Status |
|-----------|---------|---------|--------|
| [faion-gtm-strategist](../faion-gtm-strategist/) | GTM, launches, positioning, pricing, partnerships | 26 | Ready |
| [faion-content-marketer](../faion-content-marketer/) | Content, copywriting, SEO, email, social, video/podcast | 16+30 | Ready |
| [faion-growth-marketer](../faion-growth-marketer/) | Analytics, experiments, A/B testing, AARRR, retention | 30 | Ready |
| [faion-conversion-optimizer](../faion-conversion-optimizer/) | Landing pages, CRO, funnels, PLG, onboarding | 13 | Ready |
| [faion-ppc-manager](../faion-ppc-manager/) | Paid advertising (Google, Meta, LinkedIn) | External | Ready |
| [faion-seo-manager](../faion-seo-manager/) | Technical SEO, AEO, Core Web Vitals | External | Ready |
| [faion-smm-manager](../faion-smm-manager/) | Social media management and growth | External | Ready |

## Routing Guide

| Task Type | Route To |
|-----------|----------|
| Product launch, GTM strategy, positioning, pricing | faion-gtm-strategist |
| Content creation, email campaigns, social posts, video | faion-content-marketer |
| Analytics, growth experiments, AARRR, retention | faion-growth-marketer |
| Landing pages, CRO, funnels, PLG, onboarding | faion-conversion-optimizer |
| Paid advertising campaigns (Google, Meta, LinkedIn) | faion-ppc-manager |
| Technical SEO, AEO, search optimization | faion-seo-manager |
| Social media management, community building | faion-smm-manager |

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Pure orchestrator routing logic |
| CLAUDE.md | This file - navigation and overview |

**No methodologies in this directory** - all methodologies exist in sub-skill directories.

## Workflow Examples

### Product Launch
```
1. GTM strategy (faion-gtm-strategist)
2. Launch content (faion-content-marketer)
3. Landing page (faion-conversion-optimizer)
4. Metrics tracking (faion-growth-marketer)
5. Paid campaigns (faion-ppc-manager)
```

### Content Marketing Program
```
1. Content strategy (faion-content-marketer)
2. Technical SEO (faion-seo-manager)
3. Content metrics (faion-growth-marketer)
4. Social distribution (faion-smm-manager)
```

### Growth Optimization
```
1. AARRR analysis (faion-growth-marketer)
2. Funnel optimization (faion-conversion-optimizer)
3. Growth content (faion-content-marketer)
4. Paid scaling (faion-ppc-manager)
```

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-net](../faion-net/CLAUDE.md) | Parent orchestrator |
| [faion-researcher](../faion-researcher/) | Market research, competitor analysis |
| [faion-product-manager](../faion-product-manager/) | Product positioning, roadmap |
| [faion-ux-ui-designer](../faion-ux-ui-designer/) | Design for marketing |

---

*Marketing Orchestrator v2.1 | Pure Orchestrator | 7 Sub-Skills | 85+ Methodologies*
