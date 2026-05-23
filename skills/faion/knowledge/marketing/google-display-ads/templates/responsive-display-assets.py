"""Asset dict structure for create_responsive_display_ad().

Pass this dict as the `assets` argument.
Image and logo resource_names come from upload_image_asset() calls.
"""

assets = {
    # Headlines: 1-5, max 30 chars each
    "headlines": [
        "Headline Option 1",
        "Headline Option 2",
        "Headline Option 3",
    ],

    # Long headline: exactly 1, max 90 chars
    "long_headline": "Full-length headline describing the main value proposition",

    # Descriptions: 1-5, max 90 chars each
    "descriptions": [
        "Description explaining the key benefit in detail.",
        "Alternative description with a different angle.",
    ],

    # Business name: required
    "business_name": "Company Name",

    # Marketing images: 1-15 resource_names from upload_image_asset()
    "images": [
        "customers/{customer_id}/assets/{asset_id_1}",
        "customers/{customer_id}/assets/{asset_id_2}",
    ],

    # Logo images: 0-5 (optional)
    "logos": [
        "customers/{customer_id}/assets/{logo_asset_id}",
    ],

    # Destination URL
    "final_url": "https://example.com/landing-page",
}
