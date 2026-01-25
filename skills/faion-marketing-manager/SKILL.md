---
name: faion-marketing-manager
description: "Marketing orchestrator: GTM, content, growth, conversion optimization."
user-invocable: false
allowed-tools: Read, Write, Edit, Task, WebSearch, AskUserQuestion, TodoWrite, Glob, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Marketing Manager Orchestrator

Coordinates all marketing activities by routing to specialized sub-skills.

## Purpose

Routes marketing tasks to appropriate sub-skill based on domain: GTM strategy, content marketing, growth experiments, or conversion optimization.

## Architecture

| Sub-Skill | Purpose | Methodologies |
|-----------|---------|---------------|
| **faion-gtm-strategist** | GTM, launches, positioning, pricing, partnerships, customer success | 26 |
| **faion-content-marketer** | Content, copywriting, SEO, email, social, video/podcast, AI tools | 16 + 30 refs |
| **faion-growth-marketer** | Analytics, experiments, A/B testing, AARRR, retention, viral loops | 30 |
| **faion-conversion-optimizer** | Landing pages, CRO, funnels, PLG, onboarding | 13 |

**Total:** 82 methodologies + 30 media references

## Decision Tree

| If you need... | Route to | Example Methodologies |
|---------------|----------|----------------------|
| **GTM & Launch** | faion-gtm-strategist | GTM strategy, Product Hunt, positioning, pricing |
| **Content Creation** | faion-content-marketer | Content strategy, copywriting, email, social, video |
| **Growth & Analytics** | faion-growth-marketer | AARRR, A/B testing, retention, viral loops, analytics |
| **Conversion** | faion-conversion-optimizer | Landing pages, CRO, funnels, PLG, onboarding |
| **Paid Ads** | faion-ppc-manager | Google Ads, Meta Ads, LinkedIn Ads (separate skill) |
| **SEO Technical** | faion-seo-manager | Technical SEO, AEO, Core Web Vitals (separate skill) |
| **Social Media Mgmt** | faion-smm-manager | Twitter, LinkedIn, Instagram growth (separate skill) |

## Routing Examples

### Launch Scenario
```
Product Launch
├─→ faion-gtm-strategist (GTM strategy, positioning, launch plan)
├─→ faion-content-marketer (launch content, email campaign, press release)
├─→ faion-conversion-optimizer (landing page, free trial)
└─→ faion-growth-marketer (metrics tracking, experiments)
```

### Content Scenario
```
Content Marketing
├─→ faion-content-marketer (content strategy, SEO, copywriting)
├─→ faion-growth-marketer (content metrics, A/B testing)
└─→ faion-seo-manager (technical SEO, Core Web Vitals)
```

### Growth Scenario
```
Growth Optimization
├─→ faion-growth-marketer (AARRR framework, experiments, analytics)
├─→ faion-conversion-optimizer (funnel optimization, PLG)
└─→ faion-content-marketer (growth content, email)
```

## Execution Pattern

1. **Analyze** task intent and domain
2. **Route** to appropriate sub-skill(s)
3. **Invoke** sub-skill(s) using Skill tool
4. **Coordinate** if multiple sub-skills needed
5. **Report** results to user

## Quick Reference

| Marketing Goal | Primary Sub-Skill | Secondary Sub-Skills |
|----------------|-------------------|---------------------|
| Launch product | gtm-strategist | content-marketer, conversion-optimizer |
| Acquire users | content-marketer | growth-marketer, ppc-manager |
| Optimize conversion | conversion-optimizer | growth-marketer |
| Scale growth | growth-marketer | ppc-manager, content-marketer |
| Build brand | content-marketer | gtm-strategist, smm-manager |
| Retain users | growth-marketer | content-marketer |
| Partnerships | gtm-strategist | content-marketer |

## Related Skills (External)

- faion-ppc-manager (paid advertising)
- faion-seo-manager (technical SEO, AEO)
- faion-smm-manager (social media management)
- faion-researcher (market research)
- faion-product-manager (product positioning)
- faion-ux-ui-designer (design for marketing)

## References

Shared reference files remain in faion-marketing-manager/references/:
- analytics.md (GA4, Plausible, Mixpanel)
- google-ads.md, meta-ads.md (PPC technical refs)
- seo.md (SEO/AEO technical)

---

*Marketing Manager Orchestrator v2.0*
*4 Sub-Skills | 82 Methodologies | 30 Media References*
