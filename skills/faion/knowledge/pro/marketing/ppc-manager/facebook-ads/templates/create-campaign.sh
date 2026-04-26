#!/bin/bash
# Create a Facebook Ads campaign via Meta Marketing API v20.
# Budget values are in CENTS: 10000 = $100.00
# Always create campaigns as PAUSED; activate after reviewing ad sets.

curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/campaigns" \
  -H "Authorization: Bearer {access-token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "[Objective]_[Audience]_[YYYY-MM]",
    "objective": "OUTCOME_SALES",
    "status": "PAUSED",
    "special_ad_categories": [],
    "buying_type": "AUCTION",
    "daily_budget": 10000,
    "bid_strategy": "LOWEST_COST_WITHOUT_CAP"
  }'

# Response: {"id": "CAMPAIGN_ID"}
