---
name: faion-google-ads-optimization
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Google Ads API - Optimization

**Communication: User's language. Docs/code: English.**

## Purpose

Provides patterns and guidance for Google Ads bidding strategies, conversion tracking, and Google Analytics integration.

## 3-Layer Architecture

```
Layer 1: Domain Skills (faion-marketing-manager) - orchestrator
    |
Layer 2: Agents (faion-ads-agent) - executor
    |
Layer 3: Technical Skills (this) - tool
```

---

# Section 1: Bidding Strategies

## Strategy Types

| Strategy | Type | Best For |
|----------|------|----------|
| Manual CPC | Manual | Full control |
| Enhanced CPC | Semi-auto | Manual + conversions boost |
| Maximize Clicks | Automated | Traffic focus |
| Maximize Conversions | Automated | Conversion focus |
| Target CPA | Automated | Cost per acquisition goal |
| Target ROAS | Automated | Return on ad spend goal |
| Maximize Conversion Value | Automated | Revenue optimization |

## Create Portfolio Bidding Strategy

```python
def create_target_cpa_strategy(client, customer_id, name, target_cpa_micros):
    """Create a Target CPA portfolio bidding strategy."""
    bidding_strategy_service = client.get_service("BiddingStrategyService")

    operation = client.get_type("BiddingStrategyOperation")
    strategy = operation.create
    strategy.name = name
    strategy.type_ = client.enums.BiddingStrategyTypeEnum.TARGET_CPA
    strategy.target_cpa.target_cpa_micros = target_cpa_micros

    # Optional: set CPC bid ceiling
    strategy.target_cpa.cpc_bid_ceiling_micros = target_cpa_micros * 2

    response = bidding_strategy_service.mutate_bidding_strategies(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Apply Bidding Strategy to Campaign

```python
def set_campaign_bidding_strategy(client, customer_id, campaign_id, strategy_resource):
    """Apply a portfolio bidding strategy to a campaign."""
    campaign_service = client.get_service("CampaignService")

    operation = client.get_type("CampaignOperation")
    campaign = operation.update
    campaign.resource_name = f"customers/{customer_id}/campaigns/{campaign_id}"
    campaign.bidding_strategy = strategy_resource

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

## Bid Adjustments

```python
def set_device_bid_adjustment(client, customer_id, campaign_id, device, modifier):
    """Set bid adjustment for a device type.

    Args:
        device: MOBILE, DESKTOP, TABLET
        modifier: Bid modifier (1.0 = no change, 1.2 = +20%, 0.8 = -20%)
    """
    campaign_criterion_service = client.get_service("CampaignCriterionService")

    operation = client.get_type("CampaignCriterionOperation")
    criterion = operation.create
    criterion.campaign = f"customers/{customer_id}/campaigns/{campaign_id}"
    criterion.device.type_ = getattr(
        client.enums.DeviceEnum, device.upper()
    )
    criterion.bid_modifier = modifier

    response = campaign_criterion_service.mutate_campaign_criteria(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

---

# Section 2: Conversion Tracking

## Conversion Action Types

| Type | Description |
|------|-------------|
| WEBSITE | Website actions (purchases, signups) |
| APP_INSTALL | Mobile app installs |
| APP_IN_APP_PURCHASE | In-app purchases |
| CALL_FROM_ADS | Calls from ads |
| STORE_VISIT | Physical store visits |
| UPLOAD | Offline conversions |

## Create Conversion Action

```python
def create_conversion_action(client, customer_id, name, category, value=None):
    """Create a conversion action for tracking.

    Args:
        category: PURCHASE, SIGNUP, LEAD, PAGE_VIEW, etc.
        value: Default conversion value (optional)
    """
    conversion_action_service = client.get_service("ConversionActionService")

    operation = client.get_type("ConversionActionOperation")
    action = operation.create
    action.name = name
    action.category = getattr(
        client.enums.ConversionActionCategoryEnum,
        category.upper()
    )
    action.type_ = client.enums.ConversionActionTypeEnum.WEBPAGE
    action.status = client.enums.ConversionActionStatusEnum.ENABLED

    # Counting
    action.counting_type = (
        client.enums.ConversionActionCountingTypeEnum.ONE_PER_CLICK
    )

    # Attribution
    action.attribution_model_settings.attribution_model = (
        client.enums.AttributionModelEnum.GOOGLE_ADS_LAST_CLICK
    )
    action.attribution_model_settings.data_driven_model_status = (
        client.enums.DataDrivenModelStatusEnum.UNKNOWN
    )

    # Value
    if value:
        action.value_settings.default_value = value
        action.value_settings.always_use_default_value = False

    # Click-through window (days)
    action.click_through_lookback_window_days = 30

    response = conversion_action_service.mutate_conversion_actions(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Get Conversion Tag

```python
def get_conversion_tag(client, customer_id, conversion_action_id):
    """Get the tracking tag for a conversion action."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            conversion_action.id,
            conversion_action.name,
            conversion_action.tag_snippets
        FROM conversion_action
        WHERE conversion_action.id = {conversion_action_id}
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    for row in response:
        return row.conversion_action.tag_snippets
```

## Upload Offline Conversions

```python
def upload_offline_conversions(client, customer_id, conversions):
    """Upload offline conversions.

    Args:
        conversions: List of dicts with gclid, conversion_action,
                     conversion_date_time, conversion_value
    """
    conversion_upload_service = client.get_service("ConversionUploadService")

    click_conversions = []
    for conv in conversions:
        click_conversion = client.get_type("ClickConversion")
        click_conversion.gclid = conv["gclid"]
        click_conversion.conversion_action = (
            f"customers/{customer_id}/conversionActions/{conv['conversion_action_id']}"
        )
        click_conversion.conversion_date_time = conv["conversion_date_time"]
        click_conversion.conversion_value = conv.get("conversion_value", 0)
        click_conversion.currency_code = conv.get("currency", "USD")

        click_conversions.append(click_conversion)

    request = client.get_type("UploadClickConversionsRequest")
    request.customer_id = customer_id
    request.conversions = click_conversions
    request.partial_failure = True

    response = conversion_upload_service.upload_click_conversions(
        request=request
    )

    return response
```

---

# Section 3: Google Analytics Integration

## Link Google Analytics 4

```python
def create_ga4_link(client, customer_id, ga4_property_id):
    """Link Google Ads to Google Analytics 4 property."""
    google_ads_link_service = client.get_service("GoogleAdsLinkService")

    # Note: GA4 linking is typically done through GA4 Admin API
    # Google Ads API reads existing links

    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            customer.id,
            customer_manager_link.manager_customer,
            customer_manager_link.status
        FROM customer_manager_link
    """

    # Actual GA4 linking requires Google Analytics Admin API
    pass
```

## Import GA4 Conversions

GA4 conversions can be imported to Google Ads through the Google Ads UI or Admin API.

Steps:
1. In GA4, mark events as conversions
2. In Google Ads, go to Tools → Conversions
3. Click + New conversion action → Import → Google Analytics 4 properties
4. Select the conversions to import

## Query Imported Conversions

```python
def get_analytics_conversions(client, customer_id, date_range):
    """Get conversion data including imported GA4 conversions."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            campaign.name,
            segments.conversion_action,
            segments.conversion_action_category,
            metrics.conversions,
            metrics.conversions_value
        FROM campaign
        WHERE segments.date BETWEEN '{date_range[0]}' AND '{date_range[1]}'
        AND metrics.conversions > 0
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    conversions = []
    for row in response:
        conversions.append({
            "campaign": row.campaign.name,
            "action": row.segments.conversion_action,
            "category": row.segments.conversion_action_category.name,
            "conversions": row.metrics.conversions,
            "value": row.metrics.conversions_value
        })

    return conversions
```

---

*faion-google-ads-optimization v1.0*
*Technical Skill (Layer 3)*
*Part of: faion-google-ads-skill*

## Sources

- [Google Ads Bidding Strategies](https://support.google.com/google-ads/answer/2472725)
- [Smart Bidding Guide](https://support.google.com/google-ads/answer/7065882)
- [Conversion Tracking Setup](https://support.google.com/google-ads/answer/1722022)
- [GA4 Integration Guide](https://support.google.com/google-ads/answer/10502623)
