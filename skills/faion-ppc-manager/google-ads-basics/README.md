---
name: faion-google-ads-basics
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Google Ads API - Basics

**Communication: User's language. Docs/code: English.**

## Purpose

Provides patterns and guidance for Google Ads API authentication, account structure, and basic campaign management operations.

## 3-Layer Architecture

```
Layer 1: Domain Skills (faion-marketing-manager) - orchestrator
    |
Layer 2: Agents (faion-ads-agent) - executor
    |
Layer 3: Technical Skills (this) - tool
```

## Campaign Type-Specific Guides

| Guide | Content |
|-------|---------|
| [google-search-ads.md](google-search-ads.md) | Search campaigns, keywords, ad groups, quality score |
| [google-display-ads.md](google-display-ads.md) | Display campaigns, targeting, responsive ads, placements |
| [google-shopping-ads.md](google-shopping-ads.md) | Shopping campaigns, product feeds, Merchant Center |
| [google-pmax.md](google-pmax.md) | Performance Max campaigns, asset groups, audience signals |

---

# Section 1: Authentication

## Overview

Google Ads API uses OAuth 2.0 for authentication with additional developer tokens for API access.

## Authentication Components

| Component | Purpose | Required |
|-----------|---------|----------|
| Developer Token | API access identifier | Yes |
| OAuth 2.0 Client ID | Application identifier | Yes |
| OAuth 2.0 Client Secret | Application secret | Yes |
| Refresh Token | Long-lived token for access | Yes |
| Login Customer ID | Manager account ID (MCC) | For MCC |

## Authentication Flow

```
1. Create Google Cloud Project
   |
2. Enable Google Ads API
   |
3. Create OAuth 2.0 credentials
   |
4. Get Developer Token (ads.google.com)
   |
5. Generate Refresh Token
   |
6. Configure client library
```

## Developer Token Levels

| Level | Daily Requests | Requirements |
|-------|----------------|--------------|
| Test Account | Unlimited (test) | Apply in Google Ads UI |
| Basic Access | 15,000 | Approved application |
| Standard Access | 10,000 per customer | Company verification |

## Python Authentication Setup

```python
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Option 1: From YAML config file
client = GoogleAdsClient.load_from_storage("google-ads.yaml")

# Option 2: From dict
credentials = {
    "developer_token": "YOUR_DEVELOPER_TOKEN",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "refresh_token": "YOUR_REFRESH_TOKEN",
    "login_customer_id": "YOUR_MANAGER_ID",  # Optional, for MCC
    "use_proto_plus": True
}
client = GoogleAdsClient.load_from_dict(credentials)
```

## google-ads.yaml Template

```yaml
developer_token: "DEVELOPER_TOKEN"
client_id: "CLIENT_ID.apps.googleusercontent.com"
client_secret: "CLIENT_SECRET"
refresh_token: "REFRESH_TOKEN"
login_customer_id: "MANAGER_ACCOUNT_ID"  # Without dashes
use_proto_plus: True
```

## Service Account Authentication (Server-to-Server)

```python
from google.ads.googleads.client import GoogleAdsClient

# For domain-wide delegation
credentials = {
    "developer_token": "DEVELOPER_TOKEN",
    "json_key_file_path": "service-account.json",
    "impersonated_email": "user@domain.com",
    "login_customer_id": "MANAGER_ID"
}
client = GoogleAdsClient.load_from_dict(credentials)
```

## Security Best Practices

- Store credentials in environment variables or secrets manager
- Never commit credentials to version control
- Use separate credentials for test/production
- Rotate refresh tokens periodically
- Implement least-privilege access

---

# Section 2: Account Structure

## Hierarchy

```
Manager Account (MCC)
|
+-- Customer Account 1
|   |
|   +-- Campaign A
|   |   +-- Ad Group 1
|   |   |   +-- Ads
|   |   |   +-- Keywords
|   |   +-- Ad Group 2
|   |
|   +-- Campaign B
|
+-- Customer Account 2
```

## Resource Types

| Resource | Description | Parent |
|----------|-------------|--------|
| Customer | Ad account | Manager (optional) |
| Campaign | Budget, targeting settings | Customer |
| Ad Group | Ads and keywords container | Campaign |
| Ad | Creative content | Ad Group |
| Keyword | Search targeting | Ad Group |
| Extension | Additional ad info | Campaign/Ad Group |

## Customer Management

```python
def list_accessible_customers(client):
    """List all customers accessible by the authenticated user."""
    customer_service = client.get_service("CustomerService")

    accessible_customers = customer_service.list_accessible_customers()

    for resource_name in accessible_customers.resource_names:
        customer_id = resource_name.split("/")[-1]
        print(f"Customer ID: {customer_id}")

def get_customer_details(client, customer_id):
    """Get details for a specific customer."""
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            customer.id,
            customer.descriptive_name,
            customer.currency_code,
            customer.time_zone,
            customer.auto_tagging_enabled
        FROM customer
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    for row in response:
        customer = row.customer
        return {
            "id": customer.id,
            "name": customer.descriptive_name,
            "currency": customer.currency_code,
            "timezone": customer.time_zone,
            "auto_tagging": customer.auto_tagging_enabled
        }
```

---

# Section 3: Campaign Management

## Campaign Types

| Type | Code | Best For | Guide |
|------|------|----------|-------|
| Search | SEARCH | Text ads on search results | [google-search-ads.md](google-search-ads.md) |
| Display | DISPLAY_NETWORK | Banner ads across websites | [google-display-ads.md](google-display-ads.md) |
| Shopping | SHOPPING | Product listings | [google-shopping-ads.md](google-shopping-ads.md) |
| Performance Max | PERFORMANCE_MAX | AI-optimized cross-channel | [google-pmax.md](google-pmax.md) |
| Video | VIDEO | YouTube ads | (See Video Ads docs) |
| App | MULTI_CHANNEL | App installs/engagement | (See App Campaigns docs) |
| Demand Gen | DEMAND_GEN | Discovery feeds | (See Demand Gen docs) |

## Update Campaign

```python
def update_campaign_status(client, customer_id, campaign_id, new_status):
    """Update campaign status (ENABLED, PAUSED, REMOVED)."""
    campaign_service = client.get_service("CampaignService")

    operation = client.get_type("CampaignOperation")
    campaign = operation.update
    campaign.resource_name = f"customers/{customer_id}/campaigns/{campaign_id}"
    campaign.status = getattr(
        client.enums.CampaignStatusEnum,
        new_status.upper()
    )

    # Set update mask
    client.copy_from(
        operation.update_mask,
        protobuf_helpers.field_mask(None, campaign._pb)
    )

    response = campaign_service.mutate_campaigns(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## List Campaigns

```python
def list_campaigns(client, customer_id):
    """List all campaigns with key metrics."""
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            campaign_budget.amount_micros,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions
        FROM campaign
        WHERE campaign.status != 'REMOVED'
        ORDER BY campaign.name
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    campaigns = []
    for row in response:
        campaigns.append({
            "id": row.campaign.id,
            "name": row.campaign.name,
            "status": row.campaign.status.name,
            "type": row.campaign.advertising_channel_type.name,
            "budget": row.campaign_budget.amount_micros / 1_000_000,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "cost": row.metrics.cost_micros / 1_000_000,
            "conversions": row.metrics.conversions
        })

    return campaigns
```

---

# Quick Reference

## Location IDs (Common)

| Country | ID |
|---------|-----|
| United States | 2840 |
| United Kingdom | 2826 |
| Canada | 2124 |
| Australia | 2036 |
| Germany | 2276 |
| France | 2250 |

## Language IDs (Common)

| Language | ID |
|----------|-----|
| English | 1000 |
| Spanish | 1003 |
| French | 1002 |
| German | 1001 |
| Portuguese | 1014 |

---

*faion-google-ads-basics v1.0*
*Technical Skill (Layer 3)*
*Part of: faion-google-ads-skill*

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement methodology | haiku | Pattern application and configuration |
| Review implementation | sonnet | Code analysis and verification |
| Design strategy | opus | Complex decision-making |

## Sources

- [Google Ads API Documentation](https://developers.google.com/google-ads/api/docs/start)
- [OAuth 2.0 for Google APIs](https://developers.google.com/identity/protocols/oauth2)
- [Google Ads API Client Libraries](https://developers.google.com/google-ads/api/docs/client-libs)
- [Google Ads Help Center](https://support.google.com/google-ads)
