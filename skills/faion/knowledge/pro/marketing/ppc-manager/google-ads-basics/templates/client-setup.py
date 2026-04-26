"""Google Ads API client initialization patterns.

Option 1: Load from google-ads.yaml (recommended for local dev).
Option 2: Load from dict (recommended for production / env-var injection).
Option 3: Service account for domain-wide delegation.
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Option 1: From YAML config file
client = GoogleAdsClient.load_from_storage("google-ads.yaml")

# Option 2: From dict (inject via environment variables)
credentials = {
    "developer_token": os.environ["GOOGLE_ADS_DEVELOPER_TOKEN"],
    "client_id": os.environ["GOOGLE_ADS_CLIENT_ID"],
    "client_secret": os.environ["GOOGLE_ADS_CLIENT_SECRET"],
    "refresh_token": os.environ["GOOGLE_ADS_REFRESH_TOKEN"],
    "login_customer_id": os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),  # Optional MCC
    "use_proto_plus": True,
}
client = GoogleAdsClient.load_from_dict(credentials)

# Option 3: Service account (server-to-server, domain-wide delegation)
service_account_credentials = {
    "developer_token": "DEVELOPER_TOKEN",
    "json_key_file_path": "service-account.json",
    "impersonated_email": "user@domain.com",
    "login_customer_id": "MANAGER_ID",
}
client = GoogleAdsClient.load_from_dict(service_account_credentials)
