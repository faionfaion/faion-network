# Google Search Ads

**Core API:** [google-ads-basics.md](google-ads-basics.md) | [google-ads-optimization.md](google-ads-optimization.md) | [google-ads-reporting.md](google-ads-reporting.md)

## Campaign Type: SEARCH

Text ads on Google search results.

## Create Search Campaign

```python
from google.ads.googleads.client import GoogleAdsClient

def create_search_campaign(client, customer_id, budget_amount_micros):
    """Create a Search campaign with budget."""
    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_service = client.get_service("CampaignService")

    # Create campaign budget
    budget_operation = client.get_type("CampaignBudgetOperation")
    budget = budget_operation.create
    budget.name = f"Campaign Budget {uuid.uuid4()}"
    budget.amount_micros = budget_amount_micros  # e.g., 10000000 = $10
    budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD

    budget_response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id,
        operations=[budget_operation]
    )
    budget_resource_name = budget_response.results[0].resource_name

    # Create campaign
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = f"Search Campaign {uuid.uuid4()}"
    campaign.campaign_budget = budget_resource_name
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.SEARCH
    )
    campaign.status = client.enums.CampaignStatusEnum.PAUSED

    # Network settings
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = True
    campaign.network_settings.target_partner_search_network = False
    campaign.network_settings.target_content_network = False

    # Bidding strategy
    campaign.manual_cpc.enhanced_cpc_enabled = True

    # Start/end dates (YYYY-MM-DD format)
    campaign.start_date = "2026-02-01"
    campaign.end_date = "2026-12-31"

    response = campaign_service.mutate_campaigns(
        customer_id=customer_id,
        operations=[campaign_operation]
    )

    return response.results[0].resource_name
```

## Ad Groups

```python
def create_ad_group(client, customer_id, campaign_id, name, cpc_bid_micros):
    """Create an ad group within a campaign."""
    ad_group_service = client.get_service("AdGroupService")

    operation = client.get_type("AdGroupOperation")
    ad_group = operation.create
    ad_group.name = name
    ad_group.campaign = f"customers/{customer_id}/campaigns/{campaign_id}"
    ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
    ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD

    # Set default CPC bid
    ad_group.cpc_bid_micros = cpc_bid_micros  # e.g., 1000000 = $1.00

    response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Ad Group Types

| Type | Campaign Type | Description |
|------|---------------|-------------|
| SEARCH_STANDARD | Search | Standard search ads |
| SEARCH_DYNAMIC_ADS | Search | Dynamic search ads |

## Update Ad Group Bid

```python
def update_ad_group_bid(client, customer_id, ad_group_id, new_bid_micros):
    """Update ad group CPC bid."""
    ad_group_service = client.get_service("AdGroupService")

    operation = client.get_type("AdGroupOperation")
    ad_group = operation.update
    ad_group.resource_name = (
        f"customers/{customer_id}/adGroups/{ad_group_id}"
    )
    ad_group.cpc_bid_micros = new_bid_micros

    client.copy_from(
        operation.update_mask,
        protobuf_helpers.field_mask(None, ad_group._pb)
    )

    response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id,
        operations=[operation]
    )

    return response.results[0].resource_name
```

## Keyword Management

### Match Types

| Match Type | Symbol | Example Keyword | Matches |
|------------|--------|-----------------|---------|
| Broad | none | shoes | running shoes, buy footwear |
| Phrase | "..." | "running shoes" | best running shoes, running shoes sale |
| Exact | [...] | [running shoes] | running shoes (exact or close) |

### Add Keywords

```python
def add_keywords(client, customer_id, ad_group_id, keywords):
    """Add keywords to an ad group.

    Args:
        keywords: List of dicts with 'text' and 'match_type'
    """
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    operations = []
    for kw in keywords:
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.create
        criterion.ad_group = f"customers/{customer_id}/adGroups/{ad_group_id}"
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED

        # Set keyword
        criterion.keyword.text = kw["text"]
        criterion.keyword.match_type = getattr(
            client.enums.KeywordMatchTypeEnum,
            kw["match_type"].upper()
        )

        # Optional: set bid
        if "bid_micros" in kw:
            criterion.cpc_bid_micros = kw["bid_micros"]

        operations.append(operation)

    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=operations
    )

    return [r.resource_name for r in response.results]
```

### Add Negative Keywords

```python
def add_negative_keywords(client, customer_id, campaign_id, keywords):
    """Add negative keywords at campaign level."""
    campaign_criterion_service = client.get_service("CampaignCriterionService")

    operations = []
    for text in keywords:
        operation = client.get_type("CampaignCriterionOperation")
        criterion = operation.create
        criterion.campaign = f"customers/{customer_id}/campaigns/{campaign_id}"
        criterion.negative = True
        criterion.keyword.text = text
        criterion.keyword.match_type = (
            client.enums.KeywordMatchTypeEnum.BROAD
        )

        operations.append(operation)

    response = campaign_criterion_service.mutate_campaign_criteria(
        customer_id=customer_id,
        operations=operations
    )

    return [r.resource_name for r in response.results]
```

### Keyword Research with Keyword Planner

```python
def get_keyword_ideas(client, customer_id, keywords, location_ids, language_id):
    """Get keyword ideas from Keyword Planner.

    Args:
        keywords: Seed keywords list
        location_ids: Geographic targeting (e.g., ["2840"] for USA)
        language_id: Language code (e.g., "1000" for English)
    """
    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")

    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    request.language = f"languageConstants/{language_id}"

    # Add location targeting
    for loc_id in location_ids:
        request.geo_target_constants.append(
            f"geoTargetConstants/{loc_id}"
        )

    # Seed keywords
    request.keyword_seed.keywords.extend(keywords)

    # Get ideas
    response = keyword_plan_idea_service.generate_keyword_ideas(
        request=request
    )

    ideas = []
    for idea in response:
        ideas.append({
            "keyword": idea.text,
            "avg_monthly_searches": idea.keyword_idea_metrics.avg_monthly_searches,
            "competition": idea.keyword_idea_metrics.competition.name,
            "low_bid_micros": idea.keyword_idea_metrics.low_top_of_page_bid_micros,
            "high_bid_micros": idea.keyword_idea_metrics.high_top_of_page_bid_micros
        })

    return ideas
```

### Quality Score

```python
def get_keyword_quality_scores(client, customer_id, campaign_id):
    """Get quality scores for keywords."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            ad_group_criterion.keyword.text,
            ad_group_criterion.quality_info.quality_score,
            ad_group_criterion.quality_info.creative_quality_score,
            ad_group_criterion.quality_info.search_predicted_ctr,
            ad_group_criterion.quality_info.post_click_quality_score
        FROM keyword_view
        WHERE campaign.id = {campaign_id}
        AND ad_group_criterion.status != 'REMOVED'
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    keywords = []
    for row in response:
        criterion = row.ad_group_criterion
        keywords.append({
            "keyword": criterion.keyword.text,
            "quality_score": criterion.quality_info.quality_score,
            "creative_quality": criterion.quality_info.creative_quality_score.name,
            "expected_ctr": criterion.quality_info.search_predicted_ctr.name,
            "landing_page": criterion.quality_info.post_click_quality_score.name
        })

    return keywords
```

## Search Terms Report

```python
def get_search_terms_report(client, customer_id, campaign_id, start_date, end_date):
    """Get search terms that triggered ads."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            search_term_view.search_term,
            search_term_view.status,
            campaign.name,
            ad_group.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions
        FROM search_term_view
        WHERE campaign.id = {campaign_id}
        AND segments.date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY metrics.impressions DESC
        LIMIT 100
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    terms = []
    for row in response:
        terms.append({
            "search_term": row.search_term_view.search_term,
            "status": row.search_term_view.status.name,
            "campaign": row.campaign.name,
            "ad_group": row.ad_group.name,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "cost": row.metrics.cost_micros / 1_000_000,
            "conversions": row.metrics.conversions
        })

    return terms
```

---

*Part of faion-ppc-manager skill*

## Sources

- [Search Campaign Guide](https://support.google.com/google-ads/answer/1722047)
- [Responsive Search Ads](https://support.google.com/google-ads/answer/7684791)
- [Keyword Match Types](https://support.google.com/google-ads/answer/7478529)
- [Ad Extensions Guide](https://support.google.com/google-ads/answer/2375499)
