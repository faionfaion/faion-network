# Google Shopping Ads

**Core API:** [google-ads-basics.md](google-ads-basics.md) | [google-ads-optimization.md](google-ads-optimization.md) | [google-ads-reporting.md](google-ads-reporting.md)

## Campaign Type: SHOPPING

Product listing ads for e-commerce.

## Prerequisites

Before creating Shopping campaigns, you need:
1. Google Merchant Center account
2. Product feed uploaded to Merchant Center
3. Link Merchant Center to Google Ads account

## Create Shopping Campaign

```python
def create_shopping_campaign(client, customer_id, budget_micros, merchant_id):
    """Create a Shopping campaign.

    Args:
        merchant_id: Google Merchant Center ID
    """
    campaign_service = client.get_service("CampaignService")

    # Budget
    budget_resource = create_campaign_budget(client, customer_id, budget_micros)

    # Campaign
    operation = client.get_type("CampaignOperation")
    campaign = operation.create
    campaign.name = f"Shopping Campaign {uuid.uuid4()}"
    campaign.campaign_budget = budget_resource
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.SHOPPING
    )
    campaign.status = client.enums.CampaignStatusEnum.PAUSED

    # Shopping settings
    campaign.shopping_setting.merchant_id = merchant_id
    campaign.shopping_setting.sales_country = "US"
    campaign.shopping_setting.campaign_priority = 0  # 0 (Low), 1 (Medium), 2 (High)

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
| SHOPPING_PRODUCT_ADS | Standard Shopping ads |
| SHOPPING_SHOWCASE_ADS | Showcase Shopping ads (multiple products) |

## Create Product Ad Group

```python
def create_product_ad_group(client, customer_id, campaign_id, name):
    """Create ad group for Shopping campaign."""
    ad_group_service = client.get_service("AdGroupService")

    operation = client.get_type("AdGroupOperation")
    ad_group = operation.create
    ad_group.name = name
    ad_group.campaign = f"customers/{customer_id}/campaigns/{campaign_id}"
    ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
    ad_group.type_ = client.enums.AdGroupTypeEnum.SHOPPING_PRODUCT_ADS

    # Default CPC bid
    ad_group.cpc_bid_micros = 1000000  # $1.00

    response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Product Partitions (Product Groups)

```python
def create_product_partition(client, customer_id, ad_group_id, dimension_type, value=None):
    """Create product partition for targeting.

    Args:
        dimension_type: CATEGORY, BRAND, CHANNEL, CHANNEL_EXCLUSIVITY, CONDITION, etc.
        value: Dimension value (e.g., "Electronics" for CATEGORY)
    """
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    operation = client.get_type("AdGroupCriterionOperation")
    criterion = operation.create
    criterion.ad_group = f"customers/{customer_id}/adGroups/{ad_group_id}"
    criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED

    # Product partition
    partition = criterion.listing_group
    partition.type_ = client.enums.ListingGroupTypeEnum.UNIT

    # Set dimension
    if dimension_type == "BRAND":
        partition.case_value.product_brand.value = value
    elif dimension_type == "CATEGORY":
        partition.case_value.product_category_level1.value = value
    elif dimension_type == "CONDITION":
        partition.case_value.product_condition.condition = getattr(
            client.enums.ProductConditionEnum,
            value.upper()
        )
    # Add more dimension types as needed

    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Shopping Product Ads

Shopping ads are automatically created from product feed. No manual ad creation needed.

## Product Performance Report

```python
def get_shopping_product_report(client, customer_id, campaign_id, start_date, end_date):
    """Get performance by product."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            shopping_performance_view.resource_name,
            segments.product_item_id,
            segments.product_title,
            segments.product_brand,
            segments.product_category_level1,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value
        FROM shopping_performance_view
        WHERE campaign.id = {campaign_id}
        AND segments.date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY metrics.cost_micros DESC
        LIMIT 100
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    products = []
    for row in response:
        products.append({
            "item_id": row.segments.product_item_id,
            "title": row.segments.product_title,
            "brand": row.segments.product_brand,
            "category": row.segments.product_category_level1,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "ctr": row.metrics.ctr,
            "cost": row.metrics.cost_micros / 1_000_000,
            "conversions": row.metrics.conversions,
            "revenue": row.metrics.conversions_value
        })

    return products
```

## Merchant Center Integration

### Check Merchant Center Status

```python
def check_merchant_center_link(client, customer_id):
    """Check Merchant Center account link status."""
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            merchant_center_link.id,
            merchant_center_link.merchant_center_account_name,
            merchant_center_link.status
        FROM merchant_center_link
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    links = []
    for row in response:
        links.append({
            "id": row.merchant_center_link.id,
            "name": row.merchant_center_link.merchant_center_account_name,
            "status": row.merchant_center_link.status.name
        })

    return links
```

## Best Practices

1. **Feed Quality**
   - Use high-quality product images
   - Provide accurate, detailed titles
   - Include all required attributes (brand, GTIN, price)
   - Update inventory regularly

2. **Campaign Structure**
   - Create separate campaigns by product category
   - Use campaign priority for inventory overlap
   - Implement negative keywords at campaign level

3. **Bidding**
   - Start with manual CPC, transition to Target ROAS
   - Adjust bids by product performance
   - Use bid adjustments for devices and locations

4. **Optimization**
   - Review search terms report weekly
   - Add negative keywords for irrelevant searches
   - Exclude low-performing products
   - Test different product image variants

---

*Part of faion-ppc-manager skill*

## Sources

- [Shopping Campaigns Overview](https://support.google.com/google-ads/answer/2454022)
- [Google Merchant Center](https://support.google.com/merchants/answer/188493)
- [Product Data Specification](https://support.google.com/merchants/answer/7052112)
- [Shopping Ads Best Practices](https://support.google.com/google-ads/answer/6275294)
