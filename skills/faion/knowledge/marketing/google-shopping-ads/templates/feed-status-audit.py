"""
feed_status_audit.py — audit Merchant Center product feed for disapprovals and warnings

Input:
    merchant_id (str or int): Google Merchant Center account ID
    sa_path (str): path to service account JSON credentials file
                   (requires https://www.googleapis.com/auth/content scope)

Output:
    dict with keys:
        disapproved (list): SKUs with disapproved status and their issue details
        warnings (list): SKUs with warning-level issues

Usage:
    from feed_status_audit import audit_feed
    issues = audit_feed("1234567890", "/path/to/service-account.json")
    if issues["disapproved"]:
        print(f"CRITICAL: {len(issues['disapproved'])} products disapproved")
    if issues["warnings"]:
        print(f"WARNING: {len(issues['warnings'])} products have issues")

Requirements:
    pip install google-api-python-client google-auth
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build


def audit_feed(merchant_id: str, sa_path: str) -> dict:
    """Return disapproved and warned products from Merchant Center diagnostics."""
    credentials = service_account.Credentials.from_service_account_file(
        sa_path,
        scopes=["https://www.googleapis.com/auth/content"],
    )
    service = build("content", "v2.1", credentials=credentials)

    issues = {"disapproved": [], "warnings": []}
    request = service.productstatuses().list(
        merchantId=merchant_id,
        maxResults=250,
    )

    while request is not None:
        response = request.execute()
        for product in response.get("resources", []):
            product_id = product.get("productId", "")
            item_issues = product.get("itemLevelIssues", [])
            destination_statuses = product.get("destinationStatuses", [])

            for dest in destination_statuses:
                if dest.get("status") == "disapproved":
                    issues["disapproved"].append({
                        "sku": product_id,
                        "issues": [
                            {
                                "code": i.get("code"),
                                "description": i.get("description"),
                                "servability": i.get("servability"),
                            }
                            for i in item_issues
                        ],
                    })
                    break
            else:
                # No disapproved destination — check for warnings
                if item_issues:
                    issues["warnings"].append({
                        "sku": product_id,
                        "issues": [
                            {
                                "code": i.get("code"),
                                "description": i.get("description"),
                            }
                            for i in item_issues
                            if i.get("servability") != "disapproved"
                        ],
                    })

        request = service.productstatuses().list_next(request, response)

    return issues
