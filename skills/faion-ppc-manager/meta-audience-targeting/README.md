---
name: faion-meta-audience-targeting-skill
user-invocable: false
description: ""
---

# Meta Audience Targeting Guide

**Complete reference for audience targeting across Facebook & Instagram (2025-2026)**

---

## Quick Reference

| Type | Use Case | Min Size | Match Rate |
|------|----------|----------|------------|
| **Demographics** | Basic targeting | 1,000 | N/A |
| **Interests** | Cold audiences | 1,000 | N/A |
| **Custom Audiences** | Retargeting | 100 | 50-80% |
| **Lookalike Audiences** | Scale winners | 100 source | High |
| **Special Ad Categories** | Housing, Credit, Employment | N/A | Restricted |

---

## Demographic Targeting

### Geographic Locations

```json
{
  "targeting": {
    "geo_locations": {
      "countries": ["US", "CA", "GB"],
      "regions": [{"key": "4081"}],
      "cities": [{"key": "2421836", "radius": 25, "distance_unit": "mile"}],
      "zips": [{"key": "US:90210"}]
    }
  }
}
```

**Location Types:**
- **Countries:** ISO 2-letter codes
- **Regions:** State/province IDs
- **Cities:** City IDs with radius targeting
- **Zips:** Postal code targeting

### Age and Gender

```json
{
  "targeting": {
    "age_min": 25,
    "age_max": 54,
    "genders": [1, 2]
  }
}
```

**Gender Codes:**
- `1` = Male
- `2` = Female
- Omit for all genders

**Age Range:** 18-65+ (min 18 required)

### Languages and Locales

```json
{
  "targeting": {
    "locales": [6, 24]
  }
}
```

**Common Locale IDs:**
- `6` = English (US)
- `24` = English (UK)
- `28` = Spanish (Spain)
- `46` = French (France)

### Device Targeting

```json
{
  "targeting": {
    "user_os": ["iOS", "Android"],
    "user_device": ["iPhone", "Samsung Galaxy S"],
    "wireless_carrier": ["Verizon", "AT&T"]
  }
}
```

---

## Interest and Behavior Targeting

### Interest Targeting

```json
{
  "targeting": {
    "interests": [
      {"id": "6003139266461", "name": "Entrepreneurship"},
      {"id": "6003107902433", "name": "Small business"},
      {"id": "6003020834693", "name": "Photography"}
    ]
  }
}
```

**Find Interest IDs:**
```bash
curl -X GET "https://graph.facebook.com/v20.0/search?\
type=adinterest&\
q=entrepreneurship&\
limit=100&\
access_token={token}"
```

**Response:**
```json
{
  "data": [
    {
      "id": "6003139266461",
      "name": "Entrepreneurship",
      "audience_size_lower_bound": 140000000,
      "audience_size_upper_bound": 150000000
    }
  ]
}
```

### Behavior Targeting

```json
{
  "targeting": {
    "behaviors": [
      {"id": "6002714895372", "name": "Engaged Shoppers"},
      {"id": "6015559470583", "name": "Frequent Travelers"}
    ]
  }
}
```

**Popular Behaviors:**
- Online shoppers
- Purchase behavior (by product category)
- Travel behavior
- Device usage
- Digital activities

---

## Custom Audiences

### Website Custom Audiences

**Create from Pixel Events:**
```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/customaudiences" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Website Visitors 30 Days",
    "subtype": "WEBSITE",
    "rule": {
      "inclusions": {
        "operator": "or",
        "rules": [
          {
            "event_sources": [{"id": "{pixel-id}", "type": "pixel"}],
            "retention_seconds": 2592000,
            "filter": {
              "operator": "and",
              "filters": [
                {"field": "url", "operator": "i_contains", "value": "/products"}
              ]
            }
          }
        ]
      }
    }
  }'
```

**Common Website Audiences:**
- All website visitors (180 days)
- Specific page visitors (30/60/90 days)
- Add to cart without purchase (14 days)
- Product viewers (30 days)
- Purchasers (exclude from prospecting)

### Customer List Audiences

**Create from Email/Phone:**
```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/customaudiences" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Email Subscribers 2026",
    "subtype": "CUSTOM",
    "description": "Newsletter subscribers",
    "customer_file_source": "USER_PROVIDED_ONLY"
  }'
```

**Add Users (Hashed):**
```bash
curl -X POST "https://graph.facebook.com/v20.0/{audience-id}/users" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "payload": {
      "schema": ["EMAIL", "FN", "LN", "PHONE", "CT", "ST", "ZIP", "COUNTRY"],
      "data": [
        [
          "sha256(email@example.com)",
          "sha256(john)",
          "sha256(doe)",
          "sha256(1234567890)",
          "sha256(new york)",
          "sha256(ny)",
          "sha256(10001)",
          "sha256(us)"
        ]
      ]
    }
  }'
```

**Important:**
- All PII must be SHA256 hashed
- More data fields = better match rate
- Minimum 100 matched users to activate
- Typical match rate: 50-80%

### Engagement Custom Audiences

**Facebook/Instagram Engagers:**
```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/customaudiences" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "FB Page Engagers - 365 Days",
    "subtype": "ENGAGEMENT",
    "rule": {
      "inclusions": {
        "operator": "or",
        "rules": [
          {
            "event_sources": [{"id": "{page-id}", "type": "page"}],
            "retention_seconds": 31536000,
            "filter": {
              "operator": "or",
              "filters": [
                {"operator": "engaged"},
                {"operator": "visited"}
              ]
            }
          }
        ]
      }
    }
  }'
```

**Engagement Types:**
- Facebook Page engagers
- Instagram Business Profile engagers
- Video viewers (25%, 50%, 75%, 95%)
- Lead form openers
- Event responders

### App Activity Custom Audiences

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/customaudiences" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "App Users - Last 30 Days",
    "subtype": "APP",
    "rule": {
      "inclusions": {
        "operator": "or",
        "rules": [
          {
            "event_sources": [{"id": "{app-id}", "type": "app"}],
            "retention_seconds": 2592000,
            "filter": {
              "operator": "and",
              "filters": [
                {"field": "event", "operator": "eq", "value": "fb_mobile_purchase"}
              ]
            }
          }
        ]
      }
    }
  }'
```

---

## Lookalike Audiences

### Create Lookalike

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/customaudiences" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Lookalike US 1% - Purchasers",
    "subtype": "LOOKALIKE",
    "origin_audience_id": "{source-audience-id}",
    "lookalike_spec": {
      "type": "similarity",
      "country": "US",
      "ratio": 0.01
    }
  }'
```

### Lookalike Sizing

| Size | Reach | Quality | Use Case |
|------|-------|---------|----------|
| 1% | Smallest | Highest | Testing, high-value products |
| 2-3% | Medium | Good | Scaling proven campaigns |
| 5-10% | Largest | Lower | Mass market, awareness |

**Best Practices:**
- Source audience: Min 100, ideally 1,000+ users
- Use high-value customers (purchasers, not just visitors)
- Test multiple sizes (1%, 3%, 5%)
- Create country-specific lookalikes
- Update source audience monthly

### Multi-Country Lookalikes

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/customaudiences" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Lookalike 1% - US, CA, GB",
    "subtype": "LOOKALIKE",
    "origin_audience_id": "{source-audience-id}",
    "lookalike_spec": [
      {"type": "similarity", "country": "US", "ratio": 0.01},
      {"type": "similarity", "country": "CA", "ratio": 0.01},
      {"type": "similarity", "country": "GB", "ratio": 0.01}
    ]
  }'
```

---

## Exclusion Targeting

### Exclude Custom Audiences

```json
{
  "targeting": {
    "custom_audiences": [
      {"id": "{prospecting-audience-id}"}
    ],
    "exclusions": {
      "custom_audiences": [
        {"id": "{purchasers-audience-id}"},
        {"id": "{existing-customers-id}"}
      ]
    }
  }
}
```

**Common Exclusions:**
- Existing customers (prevent ad fatigue)
- Recent purchasers (respect recency)
- High-frequency users (>5 impressions/week)
- Employees and internal users
- Competitors (if identifiable)

### Exclude Connections

```json
{
  "targeting": {
    "excluded_connections": [
      {"id": "{page-id}"}
    ]
  }
}
```

**Exclude:**
- People who like your Page
- People who like specific Pages
- Friends of people who like your Page

---

## Advanced Targeting

### Layered Targeting (AND Logic)

```json
{
  "targeting": {
    "geo_locations": {"countries": ["US"]},
    "age_min": 25,
    "age_max": 45,
    "interests": [
      {"id": "6003139266461", "name": "Entrepreneurship"}
    ],
    "behaviors": [
      {"id": "6002714895372", "name": "Engaged Shoppers"}
    ],
    "custom_audiences": [
      {"id": "{website-visitors-id}"}
    ]
  }
}
```

**Result:** Users who match ALL conditions

### Flexible Targeting (OR Logic)

```json
{
  "targeting": {
    "flexible_spec": [
      {
        "interests": [
          {"id": "6003139266461", "name": "Entrepreneurship"},
          {"id": "6003107902433", "name": "Small business"}
        ]
      }
    ]
  }
}
```

**Result:** Users who match ANY interest

### Narrow Targeting (AND within OR)

```json
{
  "targeting": {
    "flexible_spec": [
      {
        "interests": [{"id": "6003139266461"}]
      },
      {
        "interests": [{"id": "6003107902433"}],
        "behaviors": [{"id": "6002714895372"}]
      }
    ]
  }
}
```

**Result:** (Interest A) OR (Interest B AND Behavior C)

---

## Audience Insights

### Get Audience Size Estimate

```bash
curl -X GET "https://graph.facebook.com/v20.0/act_{ad-account-id}/reachestimate?\
targeting_spec={targeting-json}&\
optimization_goal=OFFSITE_CONVERSIONS&\
access_token={token}"
```

**Response:**
```json
{
  "estimate_ready": true,
  "users_lower_bound": 500000,
  "users_upper_bound": 600000,
  "estimate_dau": 50000
}
```

**Audience Size Guidelines:**
- Too small (<1,000): Limited delivery
- Small (1K-10K): Good for niche targeting
- Medium (10K-500K): Optimal range
- Large (500K-5M): Broad targeting
- Too large (>10M): Consider narrowing

---

## Special Ad Categories

### Restricted Targeting

**Housing, Employment, Credit:**
```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/campaigns" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Housing Campaign",
    "objective": "OUTCOME_LEADS",
    "special_ad_categories": ["HOUSING"],
    "status": "PAUSED"
  }'
```

**Restrictions:**
- No age targeting (automatically 18-65+)
- No gender targeting
- Limited location radius (15+ miles)
- No exclusions based on demographics
- No custom/lookalike audiences based on demographics

---

## Best Practices

### Audience Structure

**Prospecting:**
```
Cold Audiences (0-3% lookalike, broad interests)
↓
Warm Audiences (website visitors, engagers)
↓
Hot Audiences (cart abandoners, product viewers)
```

**Exclusion Strategy:**
```
All campaigns exclude purchasers (last 180 days)
Retargeting excludes top-funnel audiences
```

### Testing Strategy

1. **Broad vs Narrow:**
   - Test broad (interest only) vs narrow (interest + behavior)
   - Run 7 days, compare CPA/ROAS

2. **Lookalike Sizes:**
   - Test 1%, 3%, 5% simultaneously
   - Equal budgets, same creative
   - Scale winner after statistical significance

3. **Audience Stacking:**
   - Test single interest vs multiple interests
   - Test exclusions on/off
   - Monitor audience overlap

### Naming Conventions

```
Audience: [Type]_[Source]_[Timeframe]_[Size]

Examples:
WCA_AllVisitors_30d_50k
CRM_Purchasers_90d_10k
LAL_US_1%_Purchasers_500k
Interest_Entrepreneurship_5M
Engagement_VideoViewers-75%_30d_20k
```

---

## Common Workflows

### 1. Full-Funnel Audience Setup

```
1. Create WCA: All visitors (180d)
2. Create WCA: Product viewers (30d)
3. Create WCA: Cart abandoners (14d)
4. Create WCA: Purchasers (180d)
5. Create LAL: 1%, 3%, 5% from purchasers
6. Configure exclusions (purchasers excluded from all)
```

### 2. Interest Research

```
1. Use Graph API to search interests
2. Check audience size (aim for 500K-5M)
3. Test 3-5 related interests separately
4. Combine top performers
5. Create lookalike from converters
```

### 3. Retargeting Ladder

```
Day 1-7: All visitors → Awareness ads
Day 7-14: Product viewers → Product-specific ads
Day 14-30: Cart abandoners → Discount/urgency ads
Day 30+: Re-engage with new products
```

---

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement methodology | haiku | Pattern application and configuration |
| Review implementation | sonnet | Code analysis and verification |
| Design strategy | opus | Complex decision-making |

## Sources

- [Meta Marketing API - Targeting](https://developers.facebook.com/docs/marketing-api/audiences/reference/targeting/)
- [Custom Audiences Documentation](https://developers.facebook.com/docs/marketing-api/audiences/reference/custom-audience/)
- [Lookalike Audiences Guide](https://www.facebook.com/business/help/164749007013531)
- [Special Ad Categories](https://www.facebook.com/business/help/298000447747885)
