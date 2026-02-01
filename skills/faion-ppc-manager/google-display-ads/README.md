# Google Display Ads

**Core API:** [google-ads-basics.md](google-ads-basics.md) | [google-ads-optimization.md](google-ads-optimization.md) | [google-ads-reporting.md](google-ads-reporting.md)

## Campaign Type: DISPLAY_NETWORK

Banner ads across Google Display Network (websites, apps, YouTube).

## Create Display Campaign

```python
def create_display_campaign(client, customer_id, budget_micros):
    """Create a Display campaign."""
    campaign_service = client.get_service("CampaignService")

    # Budget (reuse budget creation from search)
    budget_resource = create_campaign_budget(client, customer_id, budget_micros)

    # Campaign
    operation = client.get_type("CampaignOperation")
    campaign = operation.create
    campaign.name = f"Display Campaign {uuid.uuid4()}"
    campaign.campaign_budget = budget_resource
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.DISPLAY
    )
    campaign.status = client.enums.CampaignStatusEnum.PAUSED

    # Network settings (Display Network only)
    campaign.network_settings.target_google_search = False
    campaign.network_settings.target_search_network = False
    campaign.network_settings.target_partner_search_network = False
    campaign.network_settings.target_content_network = True

    # Bidding strategy
    campaign.manual_cpc.enhanced_cpc_enabled = True

    response = campaign_service.mutate_campaigns(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Ad Group Types

| Type | Description |
|------|-------------|
| DISPLAY_STANDARD | Standard display ads |
| DISPLAY_UPLOAD_ADS | Uploaded image/HTML5 ads |

## Targeting Options

Display campaigns support multiple targeting methods:

| Targeting Type | Description |
|----------------|-------------|
| Contextual | Target by keywords, topics, or placements |
| Audience | Target specific user groups (custom, affinity, in-market) |
| Demographics | Age, gender, parental status, household income |
| Remarketing | Show ads to previous site visitors |

### Add Contextual Targeting

```python
def add_keyword_targeting(client, customer_id, ad_group_id, keywords):
    """Add keyword targeting to display ad group."""
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    operations = []
    for keyword in keywords:
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.create
        criterion.ad_group = f"customers/{customer_id}/adGroups/{ad_group_id}"
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        criterion.keyword.text = keyword
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD

        operations.append(operation)

    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=operations
    )

    return [r.resource_name for r in response.results]
```

### Add Placement Targeting

```python
def add_placement_targeting(client, customer_id, ad_group_id, placements):
    """Add placement targeting (specific websites/apps).

    Args:
        placements: List of URLs (e.g., ["example.com", "youtube.com"])
    """
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    operations = []
    for url in placements:
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.create
        criterion.ad_group = f"customers/{customer_id}/adGroups/{ad_group_id}"
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        criterion.placement.url = url

        operations.append(operation)

    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=operations
    )

    return [r.resource_name for r in response.results]
```

### Add Audience Targeting

```python
def add_audience_targeting(client, customer_id, ad_group_id, audience_id):
    """Add audience targeting to ad group.

    Args:
        audience_id: User list or audience segment ID
    """
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    operation = client.get_type("AdGroupCriterionOperation")
    criterion = operation.create
    criterion.ad_group = f"customers/{customer_id}/adGroups/{ad_group_id}"
    criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
    criterion.user_list.user_list = (
        f"customers/{customer_id}/userLists/{audience_id}"
    )

    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Responsive Display Ads

```python
def create_responsive_display_ad(client, customer_id, ad_group_id, assets):
    """Create a responsive display ad.

    Args:
        assets: Dict with headlines, descriptions, images, logos
    """
    ad_group_ad_service = client.get_service("AdGroupAdService")

    operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = operation.create
    ad_group_ad.ad_group = f"customers/{customer_id}/adGroups/{ad_group_id}"
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED

    # Responsive display ad
    responsive_ad = ad_group_ad.ad.responsive_display_ad

    # Headlines (1-5 required)
    for headline in assets["headlines"]:
        headline_asset = client.get_type("AdTextAsset")
        headline_asset.text = headline
        responsive_ad.headlines.append(headline_asset)

    # Long headline (required)
    responsive_ad.long_headline.text = assets["long_headline"]

    # Descriptions (1-5 required)
    for desc in assets["descriptions"]:
        desc_asset = client.get_type("AdTextAsset")
        desc_asset.text = desc
        responsive_ad.descriptions.append(desc_asset)

    # Business name (required)
    responsive_ad.business_name = assets["business_name"]

    # Images (1-15, at least 1 required)
    for image_resource in assets["images"]:
        image_asset = client.get_type("AdImageAsset")
        image_asset.asset = image_resource
        responsive_ad.marketing_images.append(image_asset)

    # Logos (optional, 1-5)
    if "logos" in assets:
        for logo_resource in assets["logos"]:
            logo_asset = client.get_type("AdImageAsset")
            logo_asset.asset = logo_resource
            responsive_ad.logo_images.append(logo_asset)

    # Final URLs
    ad_group_ad.ad.final_urls.append(assets["final_url"])

    response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Upload Image Assets

```python
def upload_image_asset(client, customer_id, image_url, name):
    """Upload image asset for display ads.

    Args:
        image_url: Public URL of the image
        name: Asset name
    """
    asset_service = client.get_service("AssetService")

    operation = client.get_type("AssetOperation")
    asset = operation.create
    asset.type_ = client.enums.AssetTypeEnum.IMAGE
    asset.name = name
    asset.image_asset.data = requests.get(image_url).content

    response = asset_service.mutate_assets(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Performance Report

```python
def get_display_performance(client, customer_id, campaign_id, start_date, end_date):
    """Get display campaign performance by placement."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            detail_placement_view.display_name,
            detail_placement_view.placement_type,
            detail_placement_view.target_url,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.cost_micros,
            metrics.conversions
        FROM detail_placement_view
        WHERE campaign.id = {campaign_id}
        AND segments.date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY metrics.impressions DESC
        LIMIT 100
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    placements = []
    for row in response:
        placements.append({
            "name": row.detail_placement_view.display_name,
            "type": row.detail_placement_view.placement_type.name,
            "url": row.detail_placement_view.target_url,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "ctr": row.metrics.ctr,
            "cost": row.metrics.cost_micros / 1_000_000,
            "conversions": row.metrics.conversions
        })

    return placements
```

---

*Part of faion-ppc-manager skill*

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement methodology | haiku | Pattern application and configuration |
| Review implementation | sonnet | Code analysis and verification |
| Design strategy | opus | Complex decision-making |

## Sources

- [Google Display Network Overview](https://support.google.com/google-ads/answer/2404190)
- [Responsive Display Ads](https://support.google.com/google-ads/answer/7005917)
- [Display Campaign Targeting](https://support.google.com/google-ads/answer/2497941)
