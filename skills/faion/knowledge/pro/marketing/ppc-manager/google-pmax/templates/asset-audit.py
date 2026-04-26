"""
pmax_asset_audit.py — pull PMax asset performance labels grouped by type

Input:
    client: GoogleAdsClient instance
    customer_id (str): account ID (no hyphens)
    asset_group_resource (str): e.g. "customers/123/assetGroups/456"

Output:
    dict keyed by performance label (BEST, GOOD, LOW, PENDING, UNSPECIFIED)
    each value is a list of {type, text, resource} dicts

Usage:
    from asset_audit import audit_assets
    labels = audit_assets(client, "1234567890", "customers/123/assetGroups/456")
    low_assets = labels.get("LOW", [])
    for asset in low_assets:
        print(f"Replace {asset['type']}: {asset['text'][:50]}")
"""

from google.ads.googleads.client import GoogleAdsClient  # noqa: F401 (type hint)


def audit_assets(client, customer_id: str, asset_group_resource: str) -> dict:
    """Return asset performance labels grouped by label value."""
    ga = client.get_service("GoogleAdsService")
    query = f"""
        SELECT
            asset_group_asset.field_type,
            asset_group_asset.performance_label,
            asset.text_asset.text,
            asset.resource_name
        FROM asset_group_asset
        WHERE asset_group_asset.asset_group = '{asset_group_resource}'
    """
    by_label: dict[str, list] = {
        "BEST": [], "GOOD": [], "LOW": [], "PENDING": [], "UNSPECIFIED": []
    }
    for row in ga.search(customer_id=customer_id, query=query):
        label = row.asset_group_asset.performance_label.name
        by_label.setdefault(label, []).append({
            "type": row.asset_group_asset.field_type.name,
            "text": row.asset.text_asset.text,
            "resource": row.asset.resource_name,
        })
    return by_label
