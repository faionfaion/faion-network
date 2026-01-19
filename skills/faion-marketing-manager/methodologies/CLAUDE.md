# Methodologies Folder

## Overview

Contains 74 marketing methodologies organized into growth metrics (root level), paid advertising, marketing growth channels, and business operations. Each methodology follows a consistent structure: Metadata, Problem, Framework, Templates, Examples, Implementation Checklist, Common Mistakes, Tools, and Related Methodologies.

## Structure

```
methodologies/
├── M-GRO-*.md           # Growth metrics and frameworks (12 files)
├── ads/                 # Paid advertising methodologies (16 files)
├── growth/              # Marketing channels and tactics (32 files)
├── operations/          # Business and operations (14 files)
└── [empty subfolders]   # Reserved for future organization
    ├── analytics/
    ├── content-marketing/
    ├── conversion-optimization/
    ├── email-marketing/
    ├── gtm/
    ├── landing-page/
    ├── paid-ads/
    ├── seo/
    └── social-media/
```

## Subfolders

| Folder | Description | Files |
|--------|-------------|-------|
| [ads/](ads/) | Meta, Google, LinkedIn, Twitter ads; analytics setup; attribution; retargeting | 16 |
| [growth/](growth/) | GTM, landing pages, content, SEO, email, social media, launches | 32 |
| [operations/](operations/) | Pricing, subscriptions, churn, legal, financial, hiring, automation | 14 |

## Root Level Files (M-GRO-*)

Growth metrics and experimentation methodologies:

| File | ID | Description |
|------|----|-------------|
| M-GRO-001_aarrr_pirate_metrics.md | M-GRO-001 | AARRR funnel framework for measuring the complete customer journey |
| M-GRO-002_north_star_metric.md | M-GRO-002 | Defining the single metric that captures core customer value |
| M-GRO-003_growth_loops.md | M-GRO-003 | Self-reinforcing growth mechanisms (viral, content, paid, sales) |
| M-GRO-004_ab_testing_framework.md | M-GRO-004 | Systematic A/B testing methodology for experiments |
| M-GRO-005_multivariate_testing.md | M-GRO-005 | Testing multiple variables simultaneously |
| M-GRO-006_statistical_significance.md | M-GRO-006 | Ensuring experiment results are valid and reliable |
| M-GRO-007_cohort_analysis.md | M-GRO-007 | Analyzing user behavior by time-based groups |
| M-GRO-008_funnel_optimization.md | M-GRO-008 | Improving conversion at each funnel stage |
| M-GRO-009_viral_coefficient.md | M-GRO-009 | Measuring and improving product virality (K-factor) |
| M-GRO-010_product_led_growth.md | M-GRO-010 | Growth strategy driven by product experience |
| M-GRO-011_activation_rate.md | M-GRO-011 | Optimizing time-to-first-value and activation |
| M-GRO-012_retention_loops.md | M-GRO-012 | Building mechanisms to keep users returning |

## Methodology Structure

Each methodology file follows this structure:

```markdown
# M-XXX-NNN: Title

## Metadata
| Field | Value |
|-------|-------|
| ID | M-XXX-NNN |
| Name | Methodology Name |
| Category | Category |
| Difficulty | Beginner/Intermediate/Advanced |
| Agent | faion-*-agent |
| Related | M-XXX-NNN, M-XXX-NNN |

## Problem
[What problem this solves]

## Framework
[Step-by-step approach]

## Templates
[Ready-to-use templates]

## Examples
[Real-world examples]

## Implementation Checklist
[Action items]

## Common Mistakes
[What to avoid]

## Tools
[Recommended tools]

## Related Methodologies
[Links to related M-* files]
```

## ID Conventions

| Prefix | Category | Range |
|--------|----------|-------|
| M-GRO | Growth Metrics | 001-012 |
| M-ADS | Paid Advertising | 001-016 |
| M-MKT | Marketing Tactics | 001-032 |
| M-OPS | Operations | 001-014 |

## Agent Assignments

| Agent | Methodologies |
|-------|---------------|
| faion-growth-agent | M-GRO-*, M-OPS-* |
| faion-ads-agent | M-ADS-* |
| faion-content-agent | M-MKT-001, M-MKT-003, M-MKT-004 |
| faion-landing-designer-agent | M-MKT-002 |
| faion-email-agent | M-MKT-005, M-MKT-030 |
| faion-social-agent | M-MKT-006, M-MKT-014, M-MKT-015 |

---

*74 Methodologies | 4 Categories | 6 Agents*
