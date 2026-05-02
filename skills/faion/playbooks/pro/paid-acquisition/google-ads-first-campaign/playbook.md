---
name: google-ads-first-campaign
description: Build a Search campaign from scratch — account to live ads — with conversion tracking and a clear path to smart bidding.
tier: pro
group: paid-acquisition
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a live Google Search campaign with one ad group per persona, RSAs with 15 headlines and 4 descriptions, sitelink extensions, and a `purchase` conversion action firing via `gtag.js` — ready to accumulate the 30 conversions needed to unlock Maximize Conversions smart bidding.

## Prerequisites

- A Google Ads account (MCC or standalone) linked to a billing method.
- A live website where the `gtag.js` global snippet is already installed in `<head>`.
- Google Tag Manager or direct HTML access to add the event snippet to your thank-you / order-confirmation page.
- At minimum one defined persona with a clear search intent (e.g., "SMB owner searching for invoice software").
- A $30/day budget allocated and approved.
- Keyword research completed: 20–50 seed keywords per persona grouped by intent.

## Steps

1. **Create the campaign.** In Google Ads UI go to Campaigns → New campaign → Sales. Choose Search, deselect Display Network expansion, deselect Search Network partners. Name it after the persona: `search-smb-invoice-buyers`. Set location, language, and daily budget to `$30`. Bidding: Manual CPC, enable Enhanced CPC. Leave campaign PAUSED until Step 7.

2. **Structure ad groups by single intent.** Create one ad group per search intent cluster, not per product. ≤10 keywords each. Example for the SMB-invoice persona:
   - `ag-invoice-software-smb` — `invoice software for small business`, `online invoicing tool`, `billing software smb` (broad match + exact)
   - `ag-invoice-free-trial` — `invoice software free trial`, `try invoicing app free`, `free invoice maker online`
   Keep each group to one theme so Quality Score stays high and ad relevance is tight.

3. **Write RSA ads (one per ad group minimum).** Each RSA needs 3–15 headlines and 2–4 descriptions. Aim for the full 15/4 to maximize Google's rotation pool.
   - Headlines: include keyword in at least 3, brand name in 1, unique value props (e.g., `Send Invoice in 60 Seconds`, `No Monthly Fee`, `Trusted by 8,000 Freelancers`). Pin Headline 1 to the keyword-rich variant.
   - Descriptions: two benefit-led, one objection-handler, one CTA. Example: `Create, send, and track invoices from any device. Free 14-day trial — no card required.`
   - Character limits: headlines 30 chars, descriptions 90 chars.

4. **Add sitelink extensions.** At campaign level add 4 sitelinks covering key landing pages:
   - `How It Works` → `/how-it-works`
   - `Pricing` → `/pricing`
   - `Customer Stories` → `/customers`
   - `Start Free Trial` → `/signup`
   Each sitelink needs a 2-line description (35 chars each). Sitelinks raise CTR by 10–20% on brand and navigational queries.

5. **Implement conversion tracking via gtag.js.** In Google Ads → Tools → Conversions → New conversion → Website. Choose action category `Purchase`. Note the `AW-XXXXXXXXX/YYYy...` conversion ID and label. Add the event snippet to your order-confirmation page immediately after the global gtag snippet:

   ```html
   <!-- Place after gtag.js global snippet, on order-confirmation page only -->
   <script>
     gtag('event', 'conversion', {
       'send_to': 'AW-XXXXXXXXX/YYYy...',
       'value': orderTotal,           // dynamic; pull from your order object
       'currency': 'USD',
       'transaction_id': orderId      // deduplication key
     });
   </script>
   ```

   Set `Count` to `One` (not Every) for purchase actions to avoid counting refreshes as repeat conversions. Attribution model: Data-driven (if account is new, use Last click temporarily).

6. **Verify the conversion tag fires.** Install the Chrome extension **Tag Assistant Legacy** (or use Tag Assistant Companion). Complete a test purchase (or trigger the confirmation page with a dummy order). In Tag Assistant confirm a green `AW-XXXXXXXXX` hit with status `Conversion recorded`. Also check Google Ads → Conversions → the new action shows `Recording conversions` (not `Unverified`) within 24 h.

7. **Enable the campaign.** Set campaign status to ENABLED. Set ad group default CPC bids manually: start at 1.5× your break-even CPC. Formula: `Break-even CPC = (avg order value × target ROAS margin) / expected CVR`. For a $50 avg order, 20% margin, 2% CVR: `$50 × 0.20 / 0.02 = $500 max CPA`, so start CPC at $2–4 and adjust after week 1 data.

8. **Monitor for the first 7 days.** Check daily: impression share, avg CPC, CTR, conversion rate. Pause keywords with CTR <0.5% after 100+ impressions. Add negatives from the Search Terms report — especially broad-match bleed (irrelevant job searches, competitor names you don't want to pay for).

9. **Switch to Maximize Conversions after 30 conversions.** Once the campaign accumulates ≥30 conversions in the past 30-day window, go to Campaign Settings → Bidding → Switch to Maximize Conversions. Optionally set a Target CPA once you have 50+ conversions and a stable CPA trend. Do not switch bidding strategy during a learning period reset (e.g., right after adding new ad groups).

## Verify

In Google Ads, navigate to Campaigns → your campaign → Conversions column. Run the following check:

1. Conversions column shows a non-zero value after a test purchase.
2. Campaign status is `Eligible` (not `Limited by budget` on day 1 — if it is, the $30/day is too low for the keyword CPCs; raise budget or narrow geo).
3. In Google Ads UI → Tools → Conversions → the `purchase` action shows status `Recording conversions`.

CLI verification (if you have the Google Ads API CLI or `gaql` tool):

```bash
gaql "SELECT campaign.name, metrics.conversions, metrics.clicks FROM campaign WHERE campaign.name = 'search-smb-invoice-buyers' AND segments.date DURING LAST_7_DAYS"
```

Expected: `conversions > 0` after a verified test purchase.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Conversion action shows `Unverified` after 24 h | Tag not firing on confirmation page | Open Tag Assistant on the confirmation URL; check for JS errors; confirm `send_to` value matches exactly `AW-XXXXXXXXX/YYYy...` (copy-paste from Ads UI, not typed) |
| Ads not serving after campaign is ENABLED | Ad strength `Poor` or disapproved ads | Open Ads → check policy status; RSA needs ≥3 headlines to serve; add more headlines if strength is below `Good` |
| CTR < 0.5% after 200 impressions | Low ad relevance or wrong match type | Check Search Terms report; headlines may not contain the keyword; switch top keywords to exact match |
| `Limited by budget` from day 1 | $30/day too low for keyword CPCs | Narrow geo (city vs. country), reduce ad group count, or raise budget; alternatively lower max CPC bids by 30% |
| Smart bidding switch resets campaign performance | Learning period restart | Expected — allow 2 weeks after the switch before comparing CPA; do not change bids or add/remove keywords during this window |
| Sitelinks not showing | Account too new or Quality Score too low | Sitelinks require Ad Rank threshold; improve headline relevance and landing page speed (Core Web Vitals) |

## Next

- Run the `google-ads-optimization` playbook to tune match types and negative keyword lists after 4 weeks of data.
- Set up a linked Google Analytics 4 property and import GA4 conversions as a secondary source to cross-validate gtag.js data.
- Once CPA is stable for 60 days, expand to Performance Max (`google-pmax` methodology) to capture display + shopping intent.

## References

- [knowledge/pro/marketing/ppc-manager/ads-google-campaign-setup](../../../knowledge/pro/marketing/ppc-manager/ads-google-campaign-setup) — account → campaign → ad group → RSA hierarchy used directly in Steps 1–4; ad group theme isolation and keyword count limits come from this methodology.
- [knowledge/pro/marketing/ppc-manager/ads-conversion-tracking](../../../knowledge/pro/marketing/ppc-manager/ads-conversion-tracking) — gtag.js purchase event snippet, `send_to` format, `Count: One` deduplication, and Data-driven attribution model referenced in Step 5 and the Verify section.
- [knowledge/pro/marketing/ppc-manager/ads-budget-optimization](../../../knowledge/pro/marketing/ppc-manager/ads-budget-optimization) — break-even CPC formula and the 30-conversion threshold for switching from Manual CPC to Maximize Conversions in Steps 7 and 9.
- [knowledge/pro/marketing/ppc-manager/ads-google-keywords](../../../knowledge/pro/marketing/ppc-manager/ads-google-keywords) — single-intent ad group structure and the ≤10 keyword per group rule applied in Step 2.
