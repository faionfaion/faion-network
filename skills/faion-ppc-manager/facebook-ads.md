---
name: faion-facebook-ads-skill
user-invocable: false
description: ""
---

# Facebook Ads API Guide

**Complete reference for Facebook advertising via Meta Marketing API (2025-2026)**

---

## Quick Reference

| Area | Key Elements |
|------|--------------|
| **Campaign Structure** | Ad Account > Campaign > Ad Set > Ad > Creative |
| **Objectives** | Awareness, Traffic, Engagement, Leads, Sales |
| **Placements** | Feed, Stories, Right Column, Marketplace, Reels, Search |
| **Budget** | Daily/lifetime, CBO, bid strategies |
| **Creative** | Images, Videos, Carousels, Dynamic Creative |

---

## Campaign Management

### Campaign Objectives (v20.0+)

| Objective | Code | Use Case |
|-----------|------|----------|
| **Awareness** | `OUTCOME_AWARENESS` | Brand reach, video views |
| **Traffic** | `OUTCOME_TRAFFIC` | Website visits |
| **Engagement** | `OUTCOME_ENGAGEMENT` | Post engagement, page likes |
| **Leads** | `OUTCOME_LEADS` | Lead forms, instant forms |
| **App Promotion** | `OUTCOME_APP_PROMOTION` | App installs |
| **Sales** | `OUTCOME_SALES` | Conversions, catalog sales |

### Create Campaign

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/campaigns" \
  -H "Authorization: Bearer {access-token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Summer Sale 2026",
    "objective": "OUTCOME_SALES",
    "status": "PAUSED",
    "special_ad_categories": [],
    "buying_type": "AUCTION"
  }'
```

**Response:**
```json
{
  "id": "23849857358"
}
```

### Campaign Budget Optimization (CBO)

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/campaigns" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "CBO Campaign",
    "objective": "OUTCOME_SALES",
    "status": "PAUSED",
    "daily_budget": 10000,
    "bid_strategy": "LOWEST_COST_WITHOUT_CAP"
  }'
```

**Note:** Budget is in cents (10000 = $100.00)

### Update Campaign

```bash
curl -X POST "https://graph.facebook.com/v20.0/{campaign-id}" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Updated Campaign Name",
    "status": "ACTIVE"
  }'
```

### Campaign Status Values

| Status | Meaning |
|--------|---------|
| `ACTIVE` | Running and delivering |
| `PAUSED` | Manually paused |
| `DELETED` | Soft-deleted (recoverable) |
| `ARCHIVED` | Completed, read-only |

---

## Ad Set Management

### Create Ad Set

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/adsets" \
  -H "Authorization: Bearer {access-token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "US 25-54 Lookalike",
    "campaign_id": "{campaign-id}",
    "billing_event": "IMPRESSIONS",
    "optimization_goal": "OFFSITE_CONVERSIONS",
    "daily_budget": 5000,
    "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
    "status": "PAUSED",
    "targeting": {
      "geo_locations": {
        "countries": ["US"]
      },
      "age_min": 25,
      "age_max": 54,
      "genders": [1, 2],
      "publisher_platforms": ["facebook"],
      "facebook_positions": ["feed", "right_hand_column"]
    },
    "start_time": "2026-01-20T00:00:00-0800",
    "end_time": "2026-02-20T23:59:59-0800",
    "promoted_object": {
      "pixel_id": "{pixel-id}",
      "custom_event_type": "PURCHASE"
    }
  }'
```

### Bid Strategies

| Strategy | Code | Description |
|----------|------|-------------|
| **Lowest Cost** | `LOWEST_COST_WITHOUT_CAP` | Maximize results within budget |
| **Cost Cap** | `COST_CAP` | Control cost per result |
| **Bid Cap** | `LOWEST_COST_WITH_BID_CAP` | Maximum bid per auction |
| **ROAS** | `LOWEST_COST_WITH_MIN_ROAS` | Minimum return on ad spend |

### Optimization Goals

| Goal | Code | Best For |
|------|------|----------|
| Conversions | `OFFSITE_CONVERSIONS` | Website sales/leads |
| Link Clicks | `LINK_CLICKS` | Traffic campaigns |
| Impressions | `IMPRESSIONS` | Reach/awareness |
| Landing Page Views | `LANDING_PAGE_VIEWS` | Quality traffic |
| Lead Generation | `LEAD_GENERATION` | Lead forms |

### Facebook Placement Options

```json
{
  "targeting": {
    "publisher_platforms": ["facebook"],
    "facebook_positions": [
      "feed",
      "right_hand_column",
      "instant_article",
      "marketplace",
      "video_feeds",
      "story",
      "search",
      "instream_video",
      "facebook_reels"
    ]
  }
}
```

---

## Ad Creative

### Create Image Ad

```bash
# 1. Upload image
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/adimages" \
  -H "Authorization: Bearer {access-token}" \
  -F "filename=@image.jpg"

# Response: {"images": {"image.jpg": {"hash": "abc123..."}}}

# 2. Create creative
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/adcreatives" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Summer Sale Creative",
    "object_story_spec": {
      "page_id": "{page-id}",
      "link_data": {
        "image_hash": "abc123...",
        "link": "https://example.com/sale",
        "message": "Shop our biggest sale of the year!",
        "name": "Summer Sale - Up to 50% Off",
        "description": "Limited time offer on all products",
        "call_to_action": {
          "type": "SHOP_NOW",
          "value": {
            "link": "https://example.com/sale"
          }
        }
      }
    }
  }'
```

### Create Video Ad

```bash
# 1. Upload video (async)
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/advideos" \
  -H "Authorization: Bearer {access-token}" \
  -F "source=@video.mp4" \
  -F "title=Product Demo"

# 2. Check upload status
curl -X GET "https://graph.facebook.com/v20.0/{video-id}?fields=status"

# 3. Create creative (after status = ready)
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/adcreatives" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Video Ad Creative",
    "object_story_spec": {
      "page_id": "{page-id}",
      "video_data": {
        "video_id": "{video-id}",
        "title": "Product Demo",
        "message": "See our product in action!",
        "call_to_action": {
          "type": "LEARN_MORE",
          "value": {"link": "https://example.com"}
        }
      }
    }
  }'
```

### Call to Action Types

| Type | Best For |
|------|----------|
| `SHOP_NOW` | E-commerce |
| `LEARN_MORE` | Information |
| `SIGN_UP` | Lead generation |
| `BOOK_NOW` | Appointments |
| `DOWNLOAD` | Apps |
| `GET_OFFER` | Promotions |
| `GET_QUOTE` | Services |
| `CONTACT_US` | Direct contact |
| `SUBSCRIBE` | Newsletters |
| `APPLY_NOW` | Applications |

### Image Specifications

| Placement | Recommended Size | Ratio |
|-----------|------------------|-------|
| Feed | 1080x1080px | 1:1 |
| Stories | 1080x1920px | 9:16 |
| Right Column | 1200x628px | 1.91:1 |
| Carousel | 1080x1080px | 1:1 |

### Video Specifications

| Spec | Requirement |
|------|-------------|
| Format | MP4, MOV |
| Max size | 4GB |
| Max length | 240 min (Feed), 15s (Stories) |
| Min resolution | 720p |
| Aspect ratio | 1:1, 4:5, 9:16, 16:9 |

---

## Ad Creation

### Create Ad

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/ads" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Summer Sale Ad v1",
    "adset_id": "{adset-id}",
    "creative": {"creative_id": "{creative-id}"},
    "status": "PAUSED",
    "tracking_specs": [
      {
        "action.type": ["offsite_conversion"],
        "fb_pixel": ["{pixel-id}"]
      }
    ]
  }'
```

### Dynamic Creative

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/adsets" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Dynamic Creative Ad Set",
    "campaign_id": "{campaign-id}",
    "optimization_goal": "OFFSITE_CONVERSIONS",
    "billing_event": "IMPRESSIONS",
    "daily_budget": 5000,
    "status": "PAUSED",
    "targeting": {...},
    "is_dynamic_creative": true
  }'

# Create ad with asset feed
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/ads" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Dynamic Creative Ad",
    "adset_id": "{adset-id}",
    "status": "PAUSED",
    "creative": {
      "creative_id": "{creative-id}"
    },
    "asset_feed_spec": {
      "images": [
        {"hash": "hash1"},
        {"hash": "hash2"},
        {"hash": "hash3"}
      ],
      "titles": [
        {"text": "Title Option 1"},
        {"text": "Title Option 2"}
      ],
      "bodies": [
        {"text": "Body text option 1"},
        {"text": "Body text option 2"}
      ],
      "call_to_action_types": ["SHOP_NOW", "LEARN_MORE"]
    }
  }'
```

---

## Best Practices

### Naming Conventions

```
Campaign: [Objective]_[Audience]_[Date]
Ad Set: [Targeting]_[Placement]_[Budget]
Ad: [Creative Type]_[Version]_[Date]

Example:
Campaign: Sales_Lookalike-US-1%_2026-01
Ad Set: LAL-US-1%_FB-Feed_$50d
Ad: Video-15s_v1_2026-01-20
```

### Common Workflows

**1. Launch New Campaign**

```
1. Create Campaign (objective, budget)
2. Create Ad Set (targeting, optimization)
3. Upload Media (images/videos)
4. Create Creative
5. Create Ad (link creative to ad set)
6. Review → Set to ACTIVE
```

**2. A/B Testing**

```
1. Create Campaign
2. Create 2+ Ad Sets with one variable different:
   - Different audiences
   - Different placements
   - Different bid strategies
3. Equal budgets, run 7+ days
4. Analyze with breakdown reports
5. Scale winner, pause losers
```

**3. Retargeting Funnel**

```
1. Cold audience (prospecting)
   → Website visitors (7 days)
   → Product viewers (14 days)
   → Cart abandoners (7 days)
   → Purchasers (exclude)

2. Different messaging per stage
3. Frequency caps to prevent fatigue
```

---

## Sources

- [Meta Marketing API Documentation](https://developers.facebook.com/docs/marketing-apis/)
- [Graph API Reference](https://developers.facebook.com/docs/graph-api/)
- [Facebook Business Help Center](https://www.facebook.com/business/help/)
