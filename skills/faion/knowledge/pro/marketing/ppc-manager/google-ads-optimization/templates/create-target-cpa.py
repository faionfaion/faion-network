"""
Create a Target CPA portfolio bidding strategy in Google Ads.

Input:  client (GoogleAdsClient), customer_id (str), name (str),
        target_cpa_micros (int — CPA in micros, e.g. 50000000 = $50)
Output: resource_name (str) of the created strategy
"""


def create_target_cpa_strategy(client, customer_id, name, target_cpa_micros):
    bidding_strategy_service = client.get_service("BiddingStrategyService")

    operation = client.get_type("BiddingStrategyOperation")
    strategy = operation.create
    strategy.name = name
    strategy.type_ = client.enums.BiddingStrategyTypeEnum.TARGET_CPA
    strategy.target_cpa.target_cpa_micros = target_cpa_micros
    # CPC ceiling prevents runaway bids; set to 2x CPA target
    strategy.target_cpa.cpc_bid_ceiling_micros = target_cpa_micros * 2

    response = bidding_strategy_service.mutate_bidding_strategies(
        customer_id=customer_id,
        operations=[operation],
    )
    return response.results[0].resource_name


def apply_strategy_to_campaign(client, customer_id, campaign_id, strategy_resource):
    """Apply an existing portfolio strategy to a campaign."""
    from google.api_core import protobuf_helpers

    campaign_service = client.get_service("CampaignService")
    operation = client.get_type("CampaignOperation")
    campaign = operation.update
    campaign.resource_name = f"customers/{customer_id}/campaigns/{campaign_id}"
    campaign.bidding_strategy = strategy_resource

    client.copy_from(
        operation.update_mask,
        protobuf_helpers.field_mask(None, campaign._pb),
    )
    response = campaign_service.mutate_campaigns(
        customer_id=customer_id,
        operations=[operation],
    )
    return response.results[0].resource_name
