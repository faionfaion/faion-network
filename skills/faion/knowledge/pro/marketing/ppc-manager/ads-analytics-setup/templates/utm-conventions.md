<!-- purpose: legacy template for ads-analytics-setup — utm-conventions -->
<!-- consumes: per AGENTS.md Prerequisites -->
<!-- produces: artefact per content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml, content/06-decision-tree.xml -->
<!-- token-budget-impact: ~400-1200 tokens when loaded as context -->

# UTM Naming Conventions

Rules: lowercase only, underscores not spaces, consistent across all tools.

## utm_source (traffic origin)

| Value | Platform |
|-------|----------|
| google | Google Ads |
| meta | Facebook / Instagram |
| linkedin | LinkedIn Ads |
| twitter | Twitter / X |
| email | Email campaigns |
| affiliate | Affiliate traffic |
| partner | Partner referrals |

## utm_medium (channel type)

| Value | When to Use |
|-------|-------------|
| cpc | Paid search |
| paid_social | Paid social media |
| email | Email campaigns |
| organic_social | Organic social posts |
| referral | Referral traffic |
| display | Display/banner ads |
| video | Video ads |

## utm_campaign (initiative + description + date)

Format: `[initiative]_[description]_[date]`

Examples:
- launch_spring_sale_2026q1
- retention_winback_apr2026
- acquisition_demo_request_2026

## utm_content (ad variation identifier)

Format: `[type]_[description]_[version]`

Examples:
- video_testimonial_v2
- image_product_hero_v1
- text_social_proof_v3

## utm_term (keyword — paid search only)

Use the actual keyword. Set automatically by Google Ads via {keyword} ValueTrack parameter.

## Implementation

```javascript
// utm-constants.js — export from here, never hardcode inline
export const UTM_SOURCES = {
  google: "google",
  meta: "meta",
  linkedin: "linkedin",
  email: "email",
};

export const UTM_MEDIUMS = {
  cpc: "cpc",
  paidSocial: "paid_social",
  email: "email",
};
```
