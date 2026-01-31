# Google Performance Max (PMax)

**Core API:** [google-ads-basics.md](google-ads-basics.md) | [google-ads-optimization.md](google-ads-optimization.md) | [google-ads-reporting.md](google-ads-reporting.md)

## Campaign Type: PERFORMANCE_MAX

AI-optimized campaigns across all Google inventory (Search, Display, YouTube, Gmail, Discover, Maps).

## Overview

Performance Max uses Google's AI to optimize across channels automatically. Requires:
- Conversion tracking setup
- Asset groups (images, videos, headlines, descriptions)
- Audience signals (optional but recommended)

## Create Performance Max Campaign

```python
def create_performance_max_campaign(client, customer_id, budget_micros):
    """Create a Performance Max campaign."""
    campaign_service = client.get_service("CampaignService")

    # Budget
    budget_resource = create_campaign_budget(client, customer_id, budget_micros)

    # Campaign
    operation = client.get_type("CampaignOperation")
    campaign = operation.create
    campaign.name = f"PMax Campaign {uuid.uuid4()}"
    campaign.campaign_budget = budget_resource
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX
    )
    campaign.status = client.enums.CampaignStatusEnum.PAUSED

    # PMax requires Maximize Conversions or Maximize Conversion Value
    campaign.maximize_conversions.target_cpa_micros = 0  # Let Google optimize

    # Alternative: Target ROAS
    # campaign.maximize_conversion_value.target_roas = 3.5  # 350% ROAS

    # URL expansion (recommended: enabled)
    campaign.url_expansion_opt_out = False

    # Start/end dates
    campaign.start_date = "2026-02-01"
    campaign.end_date = "2026-12-31"

    response = campaign_service.mutate_campaigns(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Asset Groups

Asset groups contain all creative assets for PMax campaigns.

```python
def create_asset_group(client, customer_id, campaign_id, assets):
    """Create asset group for Performance Max campaign.

    Args:
        assets: Dict with headlines, descriptions, images, videos, etc.
    """
    asset_group_service = client.get_service("AssetGroupService")

    operation = client.get_type("AssetGroupOperation")
    asset_group = operation.create
    asset_group.campaign = f"customers/{customer_id}/campaigns/{campaign_id}"
    asset_group.name = f"Asset Group {uuid.uuid4()}"
    asset_group.status = client.enums.AssetGroupStatusEnum.ENABLED

    # Final URLs (required)
    asset_group.final_urls.append(assets["final_url"])

    # Path fields (optional, displayed in URL)
    if "path1" in assets:
        asset_group.path1 = assets["path1"]
    if "path2" in assets:
        asset_group.path2 = assets["path2"]

    response = asset_group_service.mutate_asset_groups(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Add Assets to Asset Group

```python
def add_asset_group_assets(client, customer_id, asset_group_resource, assets):
    """Add text, image, and video assets to asset group.

    Args:
        assets: Dict with:
            - headlines: List of text (3-5 required, max 30 chars)
            - long_headlines: List of text (1-5 required, max 90 chars)
            - descriptions: List of text (2-5 required, max 90 chars)
            - images: List of asset resource names
            - videos: List of YouTube video IDs (optional)
            - business_name: String (required)
    """
    asset_group_asset_service = client.get_service("AssetGroupAssetService")

    operations = []

    # Headlines
    for headline in assets["headlines"]:
        headline_asset = create_text_asset(client, customer_id, headline)
        operations.append(
            create_asset_group_asset_operation(
                client,
                asset_group_resource,
                headline_asset,
                client.enums.AssetFieldTypeEnum.HEADLINE
            )
        )

    # Long headlines
    for long_headline in assets["long_headlines"]:
        long_headline_asset = create_text_asset(client, customer_id, long_headline)
        operations.append(
            create_asset_group_asset_operation(
                client,
                asset_group_resource,
                long_headline_asset,
                client.enums.AssetFieldTypeEnum.LONG_HEADLINE
            )
        )

    # Descriptions
    for description in assets["descriptions"]:
        desc_asset = create_text_asset(client, customer_id, description)
        operations.append(
            create_asset_group_asset_operation(
                client,
                asset_group_resource,
                desc_asset,
                client.enums.AssetFieldTypeEnum.DESCRIPTION
            )
        )

    # Images (use existing asset resource names)
    for image_resource in assets["images"]:
        operations.append(
            create_asset_group_asset_operation(
                client,
                asset_group_resource,
                image_resource,
                client.enums.AssetFieldTypeEnum.MARKETING_IMAGE
            )
        )

    # Business name
    business_name_asset = create_text_asset(
        client,
        customer_id,
        assets["business_name"]
    )
    operations.append(
        create_asset_group_asset_operation(
            client,
            asset_group_resource,
            business_name_asset,
            client.enums.AssetFieldTypeEnum.BUSINESS_NAME
        )
    )

    response = asset_group_asset_service.mutate_asset_group_assets(
        customer_id=customer_id,
        operations=operations
    )

    return [r.resource_name for r in response.results]


def create_asset_group_asset_operation(
    client,
    asset_group_resource,
    asset_resource,
    field_type
):
    """Helper to create asset group asset operation."""
    operation = client.get_type("AssetGroupAssetOperation")
    asset_group_asset = operation.create
    asset_group_asset.asset_group = asset_group_resource
    asset_group_asset.asset = asset_resource
    asset_group_asset.field_type = field_type

    return operation


def create_text_asset(client, customer_id, text):
    """Create text asset."""
    asset_service = client.get_service("AssetService")

    operation = client.get_type("AssetOperation")
    asset = operation.create
    asset.type_ = client.enums.AssetTypeEnum.TEXT
    asset.text_asset.text = text

    response = asset_service.mutate_assets(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Audience Signals

Provide audience signals to guide Google's AI.

```python
def add_audience_signals(client, customer_id, asset_group_resource, signals):
    """Add audience signals to asset group.

    Args:
        signals: Dict with:
            - demographics: List of age/gender criteria
            - interests: List of affinity/in-market audience IDs
            - remarketing: List of user list IDs
    """
    asset_group_signal_service = client.get_service("AssetGroupSignalService")

    operation = client.get_type("AssetGroupSignalOperation")
    signal = operation.create
    signal.asset_group = asset_group_resource

    # Add audience (combine all signals)
    audience = signal.audience

    # User interests
    if "interests" in signals:
        for interest_id in signals["interests"]:
            user_interest = client.get_type("UserInterestInfo")
            user_interest.user_interest_category = (
                f"customers/{customer_id}/userInterests/{interest_id}"
            )
            audience.user_interests.append(user_interest)

    # User lists (remarketing)
    if "remarketing" in signals:
        for list_id in signals["remarketing"]:
            user_list = client.get_type("UserListInfo")
            user_list.user_list = (
                f"customers/{customer_id}/userLists/{list_id}"
            )
            audience.user_lists.append(user_list)

    response = asset_group_signal_service.mutate_asset_group_signals(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Performance Reporting

```python
def get_pmax_performance(client, customer_id, campaign_id, start_date, end_date):
    """Get Performance Max campaign metrics by channel."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            campaign.name,
            segments.conversion_action_category,
            segments.asset_interaction_target.asset,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value
        FROM campaign
        WHERE campaign.id = {campaign_id}
        AND segments.date BETWEEN '{start_date}' AND '{end_date}'
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    results = []
    for row in response:
        results.append({
            "campaign": row.campaign.name,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "cost": row.metrics.cost_micros / 1_000_000,
            "conversions": row.metrics.conversions,
            "conv_value": row.metrics.conversions_value
        })

    return results
```

## Best Practices

1. **Asset Requirements**
   - Provide maximum variety (5 headlines, 5 long headlines, 4+ descriptions)
   - Use high-quality images (at least 3-5 different images)
   - Add videos for YouTube placements
   - Test different messaging angles

2. **Audience Signals**
   - Start with broad signals, refine based on performance
   - Include remarketing lists
   - Add converting customer lists
   - Use similar audiences

3. **Bidding**
   - Start with Maximize Conversions without target CPA
   - After 30+ conversions, switch to Target CPA or Target ROAS
   - Allow 4-6 weeks for learning phase

4. **Optimization**
   - Review asset performance report weekly
   - Replace low-performing assets
   - Add new asset variations regularly
   - Monitor placement exclusions

5. **Budget**
   - PMax needs sufficient budget for learning (3x target CPA minimum)
   - Don't pause/restart frequently (disrupts learning)
   - Allocate budget across multiple asset groups for testing

---

*Part of faion-ppc-manager skill*

## Sources

- [Performance Max Campaigns](https://support.google.com/google-ads/answer/10724817)
- [Performance Max Best Practices](https://support.google.com/google-ads/answer/11513956)
- [Asset Groups Guide](https://support.google.com/google-ads/answer/11004764)
- [Performance Max Audience Signals](https://support.google.com/google-ads/answer/11221673)
