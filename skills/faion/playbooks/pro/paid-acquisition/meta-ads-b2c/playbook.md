---
name: meta-ads-b2c
description: Structure a Meta Ads Sales campaign with a 1% Lookalike audience, 5 ad variants, CAPI integration, and a 3x ROAS scale trigger.
tier: pro
group: paid-acquisition
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a live Meta Ads account structure — one Sales campaign, one Ad Set targeting a 1% Lookalike audience built from purchasers, and five creative variants (3 video + 2 image) — with Conversions API (CAPI) sending server-side purchase events. Daily budget is $50. When a duplicated Ad Set reaches 3x ROAS over a 7-day window, you scale by duplicating that Ad Set at the same daily budget rather than raising the bid.

## Prerequisites

- A Meta Business Manager account at https://business.facebook.com with a verified ad account.
- A Facebook Pixel installed on the purchase confirmation page, firing a `Purchase` event with `value` and `currency` parameters. Verify with the Meta Pixel Helper Chrome extension.
- A Custom Audience of ≥1,000 purchasers (uploaded customer list or pixel-based). Meta requires this to generate a Lookalike.
- Access to your server or tag manager to add the CAPI endpoint (Node.js, Python, or server-side GTM).
- A Meta Marketing API access token with `ads_management` + `ads_read` permissions (generate via https://developers.facebook.com/tools/explorer/).
- Five pieces of creative ready: 3 short-form videos (15–30s, 9:16 or 1:1, H.264 MP4, ≥720p) and 2 static images (1080×1080 or 1200×628, JPEG/PNG, text <20% of frame).
- Facebook Business Manager admin role on the ad account.

## Steps

1. **Create the Lookalike Audience** from your purchaser base.

   Open https://www.facebook.com/adsmanager/audiences, click "Create Audience" → "Lookalike Audience". Under "Source", select your purchaser Custom Audience. Set Country/Region to your target market (e.g. United States). Set audience size to **1%** (highest similarity to your seed). Click "Create Audience" and wait 1–2 hours for Meta to populate it (~2M people for a US 1%).

2. **Set up Conversions API (CAPI)** to send server-side `Purchase` events.

   Install the official Meta Business SDK for your language:

   ```bash
   # Python
   pip install facebook-business

   # Node.js
   npm install facebook-nodejs-business-sdk
   ```

   Add a CAPI call in your order-confirmation handler. Replace `<PIXEL_ID>` and `<ACCESS_TOKEN>` with your values:

   ```python
   from facebook_business.adobjects.serverside.action_source import ActionSource
   from facebook_business.adobjects.serverside.event import Event
   from facebook_business.adobjects.serverside.event_request import EventRequest
   from facebook_business.adobjects.serverside.user_data import UserData
   from facebook_business.adobjects.serverside.custom_data import CustomData
   from facebook_business.api import FacebookAdsApi
   import hashlib, time

   FacebookAdsApi.init(access_token="<ACCESS_TOKEN>")
   PIXEL_ID = "<PIXEL_ID>"

   def send_purchase_event(email: str, order_value: float, currency: str, order_id: str, client_ip: str, user_agent: str, fbclid: str | None = None):
       user_data = UserData(
           email=hashlib.sha256(email.lower().encode()).hexdigest(),
           client_ip_address=client_ip,
           client_user_agent=user_agent,
           fbc=f"fb.1.{int(time.time()*1000)}.{fbclid}" if fbclid else None,
       )
       custom_data = CustomData(value=order_value, currency=currency, order_id=order_id)
       event = Event(
           event_name="Purchase",
           event_time=int(time.time()),
           user_data=user_data,
           custom_data=custom_data,
           action_source=ActionSource.WEBSITE,
       )
       EventRequest(PIXEL_ID, events=[event]).execute()
   ```

   Enable **deduplication**: pass the same `event_id` in both the browser Pixel `fbq('track', 'Purchase', {...}, {eventID: order_id})` call and the CAPI `event_id` field. Meta will deduplicate and not double-count the conversion.

3. **Create the Campaign** in Ads Manager.

   Go to https://www.facebook.com/adsmanager, click "Create". Set:
   - **Objective:** Sales (optimised for conversions, not traffic)
   - **Campaign name:** `[SLS] <Product> — Lookalike Scale`
   - **Budget type:** Campaign Budget Optimisation (CBO) — OFF for this structure; we use Ad Set–level budget
   - **Special ad categories:** None (unless financial services or housing)
   - **A/B test:** Off

   Click "Next".

4. **Configure the Ad Set** targeting.

   - **Ad Set name:** `[LAL-1pct] Purchasers — $50/day`
   - **Conversion location:** Website
   - **Performance goal:** Maximise number of conversions
   - **Conversion event:** Purchase (confirm the pixel shows ≥50 events in last 7 days; otherwise the event is "learning limited")
   - **Budget:** Daily — $50
   - **Schedule:** Ongoing
   - **Audience:** Under "Custom Audiences", select the 1% Lookalike you created in Step 1. Remove all interest/behaviour targeting — Lookalike + broad works better than stacking interests.
   - **Age/Gender:** All ages 18+, All genders (narrow only if your data confirms a strong skew)
   - **Placements:** Advantage+ Placements (automatic) — do NOT manually restrict to Feed only; Meta's algorithm allocates across Reels, Stories, and Feed based on ROAS

   Click "Next".

5. **Upload the five creative variants** as separate ads.

   Create each ad individually within the same Ad Set so Meta's system tests them fairly:

   - **Ad 1 — Video hook (problem-first):** 15–30s video opening with the pain point in the first 3 seconds. Headline: "Still struggling with [problem]?" Primary text: 2–3 sentences max. CTA button: "Shop Now".
   - **Ad 2 — Video social proof:** Testimonial or UGC clip, 20–30s. Headline: "[Customer name] saved [outcome]." CTA: "Learn More" → product page.
   - **Ad 3 — Video product demo:** Screen recording or hands-on product demo, 15–20s. Headline: "Here's how it works." CTA: "Shop Now".
   - **Ad 4 — Image lifestyle:** Single 1080×1080 lifestyle photo with product in use. Headline ≤27 chars. Primary text ≤125 chars (Meta truncates beyond this on mobile). CTA: "Shop Now".
   - **Ad 5 — Image offer:** 1200×628 or 1080×1080 graphic showing the offer (e.g. "Free shipping on orders over $40"). Primary text states the offer. CTA: "Get Offer".

   For each ad, confirm the destination URL includes UTM parameters:
   `?utm_source=facebook&utm_medium=paid&utm_campaign=lal-purchasers-1pct&utm_content=<ad-slug>`

6. **Publish** and confirm delivery.

   Click "Publish". In the Ads Manager overview, verify the Ad Set status shows "Active" (not "In Review" or "Error"). Allow 24–72 hours for Meta's learning phase (50 purchase events required to exit learning). During learning, do not edit budgets, audiences, or creatives.

7. **Monitor ROAS and apply the scale rule** after day 7.

   In Ads Manager, set the date range to "Last 7 days". Add the column "Purchase ROAS" (Customize Columns → search "ROAS"). Check the Ad Set–level ROAS:

   - **ROAS ≥ 3x:** Duplicate the Ad Set (right-click → Duplicate). Keep all settings identical. Set the duplicate's start date to today. Do NOT increase the original Ad Set's budget — horizontal duplication prevents the algorithm from resetting its learning. Label the duplicate `[LAL-1pct] Purchasers — $50/day — Scale-01`.
   - **ROAS 2–3x:** Wait another 7 days; the campaign is profitable but not at threshold.
   - **ROAS < 2x:** Review the lowest-performing ads (sort by Cost per Purchase), pause the two worst creatives, and replace with two new variants. Do not touch the budget.

## Verify

Confirm the pipeline is working end-to-end with these three checks:

**1. CAPI receiving events:**

```bash
curl -s "https://graph.facebook.com/v19.0/<PIXEL_ID>/events?access_token=<ACCESS_TOKEN>" \
  | python3 -m json.tool | grep '"event_count"'
```

Returns a non-zero `event_count` for the current day. If 0, your server-side call is not firing — add logging around `EventRequest.execute()` and check for API errors.

**2. Deduplication working:**

In Meta Events Manager (https://business.facebook.com/events_manager), open your Pixel, click "Test Events". Trigger a purchase on your site. Under "Received Events", the Purchase event should appear once with source "Browser + Server" and dedup status "Deduplicated". If it shows twice, your `event_id` values differ between browser and server.

**3. Ad delivery confirmed:**

In Ads Manager with date = "Today", the Ad Set column "Impressions" should show >0 within 6 hours of going live. If still 0 after 24h, check: (a) payment method on file, (b) ads not stuck in review, (c) audience size shown as ≥1,000.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Ad Set stuck in "Learning Limited" | Fewer than 50 purchase events per week | Lower the conversion event to "Add to Cart" (more frequent) while scaling spend; switch back to Purchase once volume exceeds 50/week |
| CAPI returns `(#200) Must be admin` error | Access token lacks `ads_management` scope | Regenerate token in Graph API Explorer with `ads_management` + `business_management` permissions; re-test with `curl` |
| Lookalike audience shows "Too Small" | Seed Custom Audience has fewer than 100 people | Upload a larger customer list (CSV with hashed emails); Meta requires ≥100 matched rows to generate a Lookalike |
| High CPM (>$40) despite Advantage+ placements | Creative fatigue or audience saturation | Check Frequency column — if Frequency >3 on a 7-day basis, duplicate the Ad Set with a 2% Lookalike to expand reach; retire high-frequency creatives |
| ROAS looks inflated in Ads Manager vs. your backend | View-through attribution counting non-incremental sales | Change attribution window in Ad Set settings to "Click 1-day, View 0-day" for a conservative read closer to last-click; reconcile with Shopify/Stripe revenue for the same period |
| Duplicate Ad Set resets to Learning phase | Meta treats each Ad Set as a new learner | Expected behaviour — let it run 7 days; do not edit the duplicate during learning |
| Purchase events firing on page reload | Pixel fires on every load, not once per order | Wrap the browser `fbq('track', 'Purchase')` call in a condition that checks a server-set cookie or a one-time token to prevent re-fire on refresh |

## Next

- [meta-ads-retargeting](../meta-ads-retargeting/playbook.md) — build a retargeting Ad Set targeting 95% video viewers and Add-to-Cart events from the traffic this campaign generates.
- Apply the same Lookalike + CAPI structure to Google Performance Max using the audience signals methodology under `pro/marketing/ppc-manager/google-pmax`.
- Once you have 3+ duplicated Ad Sets each hitting 3x ROAS, introduce Creative Testing systematically — see `pro/marketing/ppc-manager/ads-ab-testing-ads` for a structured rotation framework.

## References

- [knowledge/pro/marketing/ppc-manager/ads-meta-campaign-setup](../../../knowledge/pro/marketing/ppc-manager/ads-meta-campaign-setup) — defines the Campaign → Ad Set → Ad hierarchy and the Sales objective configuration used in Steps 3 and 4 of this playbook.
- [knowledge/pro/marketing/ppc-manager/ads-meta-targeting](../../../knowledge/pro/marketing/ppc-manager/ads-meta-targeting) — covers Lookalike Audience seed requirements and the 1% similarity setting that drives Step 1's audience build.
- [knowledge/pro/marketing/ppc-manager/ads-conversion-tracking](../../../knowledge/pro/marketing/ppc-manager/ads-conversion-tracking) — provides the CAPI deduplication pattern (matching `event_id` between browser Pixel and server-side call) implemented in Step 2.
- [knowledge/pro/marketing/ppc-manager/ads-budget-optimization](../../../knowledge/pro/marketing/ppc-manager/ads-budget-optimization) — explains why horizontal Ad Set duplication at a fixed budget outperforms vertical budget increases when scaling past the 3x ROAS threshold in Step 7.
- [knowledge/pro/marketing/growth-marketer/conversion-tracking](../../../knowledge/pro/marketing/growth-marketer/conversion-tracking) — backs the reconciliation step in Troubleshooting: cross-referencing Ads Manager ROAS against backend revenue to detect view-through attribution inflation.
