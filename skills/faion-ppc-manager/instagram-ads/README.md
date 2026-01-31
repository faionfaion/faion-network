---
name: faion-instagram-ads-skill
user-invocable: false
description: ""
---

# Instagram Ads API Guide

**Complete reference for Instagram advertising via Meta Marketing API (2025-2026)**

---

## Quick Reference

| Area | Key Elements |
|------|--------------|
| **Placements** | Feed, Stories, Explore, Reels, Search |
| **Creative Formats** | Single Image, Video, Carousel, Collection |
| **Aspect Ratios** | 1:1 (Feed), 9:16 (Stories/Reels), 4:5 (Feed) |
| **Objectives** | Awareness, Traffic, Engagement, Leads, Sales |

---

## Instagram Placements

### Available Positions

```json
{
  "targeting": {
    "publisher_platforms": ["instagram"],
    "instagram_positions": [
      "stream",        // Feed
      "story",         // Stories
      "explore",       // Explore tab
      "reels",         // Reels
      "search"         // Search results
    ]
  }
}
```

### Placement Best Practices

| Placement | Format | Best For |
|-----------|--------|----------|
| **Feed** | 1:1, 4:5 images/videos | Product showcases, storytelling |
| **Stories** | 9:16 full-screen | Limited-time offers, immersive content |
| **Explore** | 1:1, 4:5 | Discovery, reaching new audiences |
| **Reels** | 9:16 vertical video | Short-form video, trending content |
| **Search** | 1:1 images | Intent-based targeting |

---

## Creative Specifications

### Image Ads

| Placement | Recommended Size | Ratio | File Size |
|-----------|------------------|-------|-----------|
| Feed | 1080x1080px | 1:1 | Max 30MB |
| Feed (Portrait) | 1080x1350px | 4:5 | Max 30MB |
| Stories | 1080x1920px | 9:16 | Max 30MB |
| Explore | 1080x1080px | 1:1 | Max 30MB |
| Reels | 1080x1920px | 9:16 | Max 30MB |

**Format:** JPG, PNG

### Video Ads

| Placement | Specs | Duration | File Size |
|-----------|-------|----------|-----------|
| Feed | 1080x1080px (1:1) or 1080x1350px (4:5) | 1s - 60min | Max 4GB |
| Stories | 1080x1920px (9:16) | 1s - 15s | Max 4GB |
| Explore | 1080x1080px (1:1) | 1s - 60min | Max 4GB |
| Reels | 1080x1920px (9:16) | 1s - 90s | Max 4GB |

**Format:** MP4, MOV
**Min Resolution:** 720p
**Recommended:** H.264 compression, square pixels, fixed frame rate, stereo AAC audio

### Carousel Ads

| Spec | Requirement |
|------|-------------|
| Cards | 2-10 images/videos |
| Image Size | 1080x1080px (1:1) |
| Video Ratio | 1:1 only |
| File Size | 30MB per image, 4GB per video |
| Duration | 1s - 240min per video |

---

## Ad Set Configuration

### Create Instagram Ad Set

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/adsets" \
  -H "Authorization: Bearer {access-token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Instagram Feed & Stories - US 18-34",
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
      "age_min": 18,
      "age_max": 34,
      "genders": [1, 2],
      "publisher_platforms": ["instagram"],
      "instagram_positions": ["stream", "story", "explore", "reels"]
    },
    "promoted_object": {
      "pixel_id": "{pixel-id}",
      "custom_event_type": "PURCHASE"
    }
  }'
```

### Instagram-Only vs Multi-Platform

**Instagram Only:**
```json
{
  "targeting": {
    "publisher_platforms": ["instagram"],
    "instagram_positions": ["stream", "story"]
  }
}
```

**Instagram + Facebook:**
```json
{
  "targeting": {
    "publisher_platforms": ["facebook", "instagram"],
    "facebook_positions": ["feed", "story"],
    "instagram_positions": ["stream", "story", "reels"]
  }
}
```

---

## Creative Best Practices

### Feed Ads

**Image Guidelines:**
- Use high-quality visuals (1080x1080px or 1080x1350px)
- Minimal text on images (avoid >20% text coverage)
- Clear product shots or lifestyle imagery
- Consistent brand aesthetics

**Video Guidelines:**
- Capture attention in first 3 seconds
- Add captions (85% watch without sound)
- Keep videos under 30 seconds for best performance
- Use square (1:1) or vertical (4:5) format

**Copy Guidelines:**
- Primary text: Up to 125 characters (optimal)
- Headline: Up to 40 characters
- CTA button required
- Use emojis sparingly

### Stories Ads

**Creative Tips:**
- Full-screen vertical format (9:16)
- Design for mobile viewing
- Keep branding at top/bottom (avoid middle swipe area)
- Use interactive elements (polls, questions - via organic Stories)
- Text should be large and readable

**Safe Zones:**
- Top 250px: Reserved for profile info
- Bottom 250px: Reserved for CTA button
- Design content within safe zone (1080x1420px)

### Reels Ads

**Video Best Practices:**
- Vertical 9:16 format only
- 1-90 seconds (15-30s optimal)
- Fast-paced, entertaining content
- Trending audio/music
- Native, authentic look (avoid overly polished)
- Clear hook in first 1-2 seconds

**Technical:**
- Looping videos perform better
- Minimum 500x888px resolution
- H.264 codec, AAC audio
- Add captions for accessibility

---

## Instagram Shopping Ads

### Product Tags in Ads

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/adcreatives" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Shopping Ad Creative",
    "object_story_spec": {
      "instagram_actor_id": "{instagram-business-account-id}",
      "link_data": {
        "image_hash": "abc123...",
        "link": "https://example.com/shop",
        "message": "Shop our latest collection",
        "call_to_action": {
          "type": "SHOP_NOW",
          "value": {"link": "https://example.com/shop"}
        }
      }
    },
    "product_set_id": "{product-catalog-id}"
  }'
```

### Collection Ads

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/adcreatives" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Collection Ad",
    "object_story_spec": {
      "instagram_actor_id": "{instagram-business-account-id}",
      "template_data": {
        "collection_hero_image_hash": "hero_image_hash",
        "collection_thumbnails": [
          {"product_id": "product_1"},
          {"product_id": "product_2"},
          {"product_id": "product_3"},
          {"product_id": "product_4"}
        ],
        "message": "Shop the collection",
        "link": "https://example.com/collection"
      }
    }
  }'
```

---

## Audience Targeting for Instagram

### Demographics

```json
{
  "targeting": {
    "age_min": 18,
    "age_max": 34,
    "genders": [2],
    "geo_locations": {
      "countries": ["US"],
      "cities": [{"key": "2490299", "radius": 10, "distance_unit": "mile"}]
    },
    "publisher_platforms": ["instagram"],
    "instagram_positions": ["stream", "story"]
  }
}
```

### Instagram-Specific Behaviors

```json
{
  "targeting": {
    "behaviors": [
      {"id": "6015559470583", "name": "Instagram Business Profile Followers"}
    ],
    "interests": [
      {"id": "6003139266461", "name": "Fashion"},
      {"id": "6003020834693", "name": "Photography"}
    ]
  }
}
```

---

## Performance Optimization

### Bid Strategies for Instagram

| Strategy | Use Case |
|----------|----------|
| Lowest Cost | Maximize results, unstable performance |
| Cost Cap | Control cost per conversion |
| Bid Cap | Control auction competition |

### Budget Allocation

**Multi-Placement Strategy:**
```
Feed: 40% budget (broad reach)
Stories: 30% budget (engagement)
Reels: 20% budget (discovery)
Explore: 10% budget (new audiences)
```

**Test allocation, then optimize based on:**
- Cost per result
- Conversion rate
- Return on ad spend (ROAS)

---

## Reporting Metrics

### Key Instagram Metrics

```bash
curl -X GET "https://graph.facebook.com/v20.0/{adset-id}/insights?\
fields=spend,impressions,reach,frequency,clicks,cpc,cpm,ctr,\
actions,cost_per_action_type,video_avg_time_watched_actions,\
video_p25_watched_actions,video_p50_watched_actions,\
video_p75_watched_actions,video_p100_watched_actions&\
date_preset=last_7d&\
breakdowns=publisher_platform,platform_position&\
access_token={token}"
```

### Instagram-Specific Breakdown

```bash
curl -X GET "https://graph.facebook.com/v20.0/{campaign-id}/insights?\
fields=spend,impressions,actions&\
date_preset=last_7d&\
filtering=[{'field':'publisher_platform','operator':'IN','value':['instagram']}]&\
breakdowns=platform_position&\
access_token={token}"
```

**Returns data for:**
- `instagram_stream` (Feed)
- `instagram_story` (Stories)
- `instagram_explore` (Explore)
- `instagram_reels` (Reels)

---

## Common Workflows

### 1. Launch Instagram Shopping Campaign

```
1. Connect Instagram Business Account to Business Manager
2. Set up Product Catalog (Facebook Commerce Manager)
3. Create Campaign (objective: OUTCOME_SALES)
4. Create Ad Set (Instagram placements only)
5. Create Shopping Creative (product tags)
6. Enable Instagram Shopping features
7. Review → Activate
```

### 2. Stories + Reels Campaign

```
1. Create Campaign (objective: OUTCOME_AWARENESS or OUTCOME_ENGAGEMENT)
2. Create Ad Set (instagram_positions: ["story", "reels"])
3. Upload vertical videos (9:16, 1080x1920px)
4. Add captions and CTA
5. Test multiple creative variations
6. Monitor video completion rates
7. Optimize for top performers
```

### 3. Multi-Format Testing

```
1. Create 3 Ad Sets:
   - Ad Set A: Feed only (1:1 images)
   - Ad Set B: Stories only (9:16 videos)
   - Ad Set C: Reels only (9:16 short videos)
2. Equal budgets, same audience
3. Run 7 days minimum
4. Compare CPA, ROAS, engagement
5. Scale winning placement
```

---

## Best Practices Summary

### Creative Quality
- High-resolution images (1080px min)
- Vertical video for Stories/Reels
- Captions for sound-off viewing
- Authentic, native-looking content

### Targeting
- Leverage Instagram-specific behaviors
- Test age 18-34 for most products
- Use interest targeting for cold audiences
- Retarget engaged users

### Budget
- Start with $20-50/day minimum
- Test placements separately before combining
- Allocate more to top-performing placements
- Increase budget 20-30% every 3-4 days when scaling

### Testing
- Test 3-5 creative variations
- Run tests minimum 7 days
- Use dynamic creative for automated testing
- Monitor frequency (keep under 3.0)

---

## Sources

- [Meta Marketing API Documentation](https://developers.facebook.com/docs/marketing-apis/)
- [Instagram Advertising Guide](https://business.instagram.com/advertising/)
- [Instagram Creative Best Practices](https://www.facebook.com/business/ads-guide/instagram)
