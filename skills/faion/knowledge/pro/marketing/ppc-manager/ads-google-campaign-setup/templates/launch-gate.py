"""
launch_gate.py — pre-flight checks for a Google Ads campaign before enabling

Input:
    client: GoogleAdsClient instance
    customer_id (str): account ID (no hyphens)
    campaign_id (int): campaign to validate

Output:
    dict with keys:
        ok (bool): True if all checks pass
        issues (list[str]): list of issue descriptions

Usage:
    from launch_gate import can_enable
    result = can_enable(client, "1234567890", 9876543210)
    if not result["ok"]:
        raise ValueError(f"Pre-launch gate failed: {result['issues']}")
"""


def can_enable(client, customer_id: str, campaign_id: int) -> dict:
    """Run pre-flight checks; return ok=True only if all checks pass."""
    ga = client.get_service("GoogleAdsService")
    rows = list(ga.search(customer_id=customer_id, query=f"""
        SELECT
            ad_group.id,
            ad_group_ad.ad.id,
            ad_group_ad.ad.responsive_search_ad.headlines,
            campaign.network_settings.target_content_network,
            campaign.network_settings.target_partner_search_network,
            campaign_budget.amount_micros
        FROM ad_group_ad
        WHERE campaign.id = {campaign_id}
    """))

    issues = []

    if not rows:
        issues.append("no ads found in campaign")
        return {"ok": False, "issues": issues}

    # Network settings check
    if any(r.campaign.network_settings.target_content_network for r in rows):
        issues.append("Display Network is enabled — disable for Search-only campaign")
    if any(r.campaign.network_settings.target_partner_search_network for r in rows):
        issues.append("Search Partners is enabled — disable if not intentional")

    # Budget sanity check ($1/day minimum = 1,000,000 micros)
    budget_micros = rows[0].campaign_budget.amount_micros
    if budget_micros < 1_000_000:
        issues.append(
            f"budget is {budget_micros} micros (${budget_micros / 1_000_000:.6f}/day) "
            "— likely a micros unit error; expected dollars * 1,000,000"
        )

    # RSA headline check (minimum 3 headlines per ad)
    for r in rows:
        headlines = r.ad_group_ad.ad.responsive_search_ad.headlines
        if len(headlines) < 3:
            issues.append(
                f"ad {r.ad_group_ad.ad.id} has only {len(headlines)} headline(s); minimum 3 required"
            )

    return {"ok": len(issues) == 0, "issues": issues}
