#!/bin/bash
# Create a Facebook Ads ad set with targeting and optimization configuration.
# Requires campaign_id from create-campaign.sh output.
# Budget in CENTS: 5000 = $50.00

curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/adsets" \
  -H "Authorization: Bearer {access-token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "[Targeting]_[Placement]_[Budget]",
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
      "facebook_positions": ["feed"]
    },
    "start_time": "2026-01-01T00:00:00-0800",
    "promoted_object": {
      "pixel_id": "{pixel-id}",
      "custom_event_type": "PURCHASE"
    }
  }'

# Response: {"id": "ADSET_ID"}
