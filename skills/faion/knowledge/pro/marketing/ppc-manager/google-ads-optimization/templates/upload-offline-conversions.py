"""
Upload offline conversions to Google Ads matched by gclid.

Input:  client (GoogleAdsClient), customer_id (str),
        conversions (list of dicts):
          - gclid (str)
          - conversion_action_id (str)
          - conversion_date_time (str, format: '2026-01-15 14:30:00+00:00')
          - conversion_value (float, optional)
          - currency (str, default 'USD')

Output: UploadClickConversionsResponse (partial_failure enabled)

Note:   Must upload within 90 days of the original click — older gclids are rejected.
"""


def upload_offline_conversions(client, customer_id, conversions):
    service = client.get_service("ConversionUploadService")

    click_conversions = []
    for conv in conversions:
        click_conversion = client.get_type("ClickConversion")
        click_conversion.gclid = conv["gclid"]
        click_conversion.conversion_action = (
            f"customers/{customer_id}/conversionActions/{conv['conversion_action_id']}"
        )
        click_conversion.conversion_date_time = conv["conversion_date_time"]
        click_conversion.conversion_value = conv.get("conversion_value", 0.0)
        click_conversion.currency_code = conv.get("currency", "USD")
        click_conversions.append(click_conversion)

    request = client.get_type("UploadClickConversionsRequest")
    request.customer_id = customer_id
    request.conversions = click_conversions
    request.partial_failure = True  # do not abort batch on single failure

    return service.upload_click_conversions(request=request)
