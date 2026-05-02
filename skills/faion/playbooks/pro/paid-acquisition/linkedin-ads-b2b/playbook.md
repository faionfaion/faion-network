---
name: linkedin-ads-b2b
description: Run LinkedIn Sponsored Content campaigns targeting B2B ICPs by job title, company size, and industry to generate MQLs via Lead Gen Forms.
tier: pro
group: paid-acquisition
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a live LinkedIn Campaign Manager setup with Sponsored Content ads targeting "VP Engineering" personas at SaaS companies sized 201-1000, a Lead Gen Form capturing MQL data, a CRM webhook routing form fills to your SDR queue, and a follow-up SLA of 24 hours enforced by your CRM.

## Prerequisites

- A LinkedIn Campaign Manager account with at least one ad account (billing credit card attached).
- LinkedIn Insight Tag installed on your website (verify at Campaign Manager → Account Assets → Insight Tag).
- A CRM that accepts webhook POSTs (HubSpot, Salesforce, Pipedrive, or equivalent).
- Minimum daily budget of $50 committed for ≥14 days ($700 minimum test run).
- Your ICP defined: job title(s), seniority level, company size range, industry.
- A 1200×627 px image asset for the ad creative (professional quality, no text overlay over 20% of image area).
- An SDR or AE assigned to follow up on inbound leads within 24 hours.

## Steps

1. Sign in to Campaign Manager at https://www.linkedin.com/campaignmanager/ and select your ad account.

2. Click **Create campaign** → choose objective **Lead Generation** (not Website Visits — Lead Gen Forms require this objective).

3. Name the campaign using the pattern `[ICP]-[Offer]-[Date]`, for example `VP-Eng-SaaS201-DemoRequest-2026-05`. This makes performance segmentation readable at a glance.

4. Set the audience targeting:
   - **Job Title**: add exact titles — `VP of Engineering`, `VP Engineering`, `Head of Engineering`. Use the "OR" connector between title variants.
   - **Company Size**: select `201-500` and `501-1000` (two separate facets, both checked).
   - **Industry**: select `Computer Software`, `Internet`, `Information Technology and Services`. Exclude `Staffing and Recruiting` and `Higher Education` to reduce noise.
   - **Geography**: set to your target region (e.g., United States).
   - Verify **Forecasted results** shows at least 20,000 matched members. If under 20,000, broaden industry or add seniority level `Director` to the title list.

5. Enable **Audience Expansion** — OFF. Keep targeting precise for the first 14 days.

6. Select ad format: **Single Image Ad**.

7. Set budget:
   - **Daily budget**: $50 minimum. Use $75/day if your target CPL is under $60.
   - **Start date**: today. **End date**: leave open (manual pause).
   - **Bid strategy**: **Manual CPC** for the first 14 days. Set manual bid at $8-10 (middle of the $5-15 typical CPC range). Do NOT use Maximum Delivery until you have 50+ form fills.

8. Create the Lead Gen Form:
   - Go to **Campaign Assets → Lead Gen Forms → Create form**.
   - Form name: `Demo-Request-VPEng-2026`.
   - Headline (≤60 chars): `Request a product demo`.
   - Details (≤160 chars): `See how [Product] helps engineering teams ship faster. 15-minute demo, no sales pitch.`
   - Fields to collect: **First Name**, **Last Name**, **Email**, **Job Title**, **Company Name**, **Company Size** (all pre-filled from LinkedIn profile).
   - Add one custom question: `What is your biggest engineering bottleneck right now?` (open text — improves lead quality signal).
   - Privacy policy URL: your company's privacy policy page.
   - Confirmation message: `Thanks — your SDR will reach out within 24 hours.`

9. Create the Sponsored Content ad:
   - Click **Create ad** → **Single Image Ad**.
   - Introductory text (≤150 chars visible): `VP Engineering at a 200-1000 person SaaS — does your team lose sprint velocity to infra fires?`
   - Headline (≤70 chars): `Cut engineering downtime by 40%. See how.`
   - Description (≤100 chars): `Join 300+ SaaS engineering teams using [Product].`
   - CTA button: **Request Demo**.
   - Upload your 1200×627 image.
   - Attach the Lead Gen Form created in step 8.

10. Set up the CRM webhook for form-fill routing:
    - In Campaign Manager → **Account Assets → Lead Gen Form Responses** → select your form → **Connect to CRM or Zapier/Make**.
    - If using native integration (HubSpot or Marketo): follow the OAuth connection wizard and map LinkedIn form fields to CRM contact properties.
    - If using webhook (Zapier or Make): copy the Lead Gen Forms webhook URL from Campaign Manager → paste it as the trigger endpoint in Zapier/Make → map fields to your CRM's contact create endpoint.
    - In your CRM, create an automated task: assign a follow-up call/email to the owning SDR with due date = today + 24 hours, triggered on new contact creation from LinkedIn source.

11. Launch: click **Review** → verify targeting summary, daily budget, and Lead Gen Form are correct → click **Launch campaign**.

12. Set a calendar reminder for **Day 15**: switch bid strategy from Manual CPC to **Maximum Delivery** once you have ≥50 form fills accumulated.

13. Add audience exclusions to prevent wasting spend on existing customers:
    - Go to **Campaign → Audience → Exclusions → Upload a list**.
    - Export current customers (email list) from your CRM and upload as a LinkedIn Matched Audience.
    - Apply the exclusion after the list is processed (typically 24-48 hours).

## Verify

Open Campaign Manager → select your campaign → click **Performance**.

Run this check 48 hours after launch (LinkedIn metrics stabilize after 24-48 hours):

- **Impressions** > 0 (confirms targeting matched audience and billing is active).
- **CTR** ≥ 0.3% (below this, creative needs revision — see Troubleshooting).
- **Lead Gen Form opens** > 0 (confirms the CTA is rendering the form, not a broken link).
- **Lead Gen Form completion rate** ≥ 10% (below this, form is too long or privacy policy URL is broken).

In your CRM: confirm at least one test lead record exists with `source = LinkedIn` and the SDR follow-up task was created with the correct due date.

To test the webhook end-to-end before going live: in Campaign Manager → Lead Gen Forms → your form → **Download leads as CSV** → manually POST one row to your webhook URL using curl:

```bash
curl -X POST https://hooks.yourcrm.com/linkedin \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"Lead","email":"test+linkedin@yourcompany.com","job_title":"VP Engineering","company_name":"TestCo","company_size":"501-1000"}'
```

Confirm the CRM creates a contact and assigns the SDR task.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Campaign status "In Review" for >24h | Creative review queue backlog or policy flag | Check Campaign Manager notifications; if flagged, remove text overlay from image that exceeds 20% area limit; resubmit |
| CTR below 0.3% after 1,000 impressions | Ad copy not role-specific, or image lacks contrast | Rewrite intro text to open with the ICP's specific pain; swap image; test 2 variants (A/B via duplicate ad) |
| Lead form completion rate below 10% | Too many custom questions, or privacy policy URL returns 404 | Remove all custom questions except one; verify privacy policy URL loads in incognito |
| CPL above $150 after 3+ days | Audience too narrow causing frequency saturation, or bid too low | Check frequency metric — if above 3, expand industry list or add seniority `Director`; raise manual CPC bid to $12 |
| CRM not receiving leads | Webhook URL misconfigured or Lead Gen Form not connected | In Campaign Manager → Lead Gen Forms → verify CRM integration status shows "Connected"; re-run the curl test from the Verify section |
| Forecasted audience below 20,000 | Over-targeting on all three dimensions simultaneously | Relax one dimension: remove the company size filter (add it back as a negative — exclude `1-10` and `10-50` instead) |
| "Learning" status persisting past day 14 | Not enough conversions to exit learning phase | Confirm budget is ≥$50/day; if leads are coming in but algorithm still shows learning, wait for 50 cumulative form fills before switching to Maximum Delivery |
| LinkedIn API OAuth token expired (for automated reporting) | 60-day token lifetime; no refresh triggered | Implement proactive token refresh at day 50; never rely on 401 errors to trigger refresh mid-run |

## Next

- [google-ads-first-campaign](../google-ads-first-campaign/playbook.md) — add Google Search as a second paid channel once LinkedIn CPL is below target and CRM attribution is confirmed.
- [ltv-cac-attribution](../ltv-cac-attribution/playbook.md) — build the LTV:CAC dashboard to validate whether LinkedIn MQLs convert to pipeline at the ratio required for profitability.
- Review the `knowledge/pro/marketing/ppc-manager/ads-linkedin-ads` bidding-progression rules at day 14 to decide whether to switch to Maximum Delivery or Cost Cap bidding.

## References

- [knowledge/pro/marketing/ppc-manager/ads-linkedin-ads](../../../knowledge/pro/marketing/ppc-manager/ads-linkedin-ads) — targeting facet definitions (Job Title, Company Size, Industry), Lead Gen Form field pre-fill behavior, CPM/CPC cost ranges ($30-80 CPM, $5-15 CPC), and the bidding-progression rule (Manual CPC for 14 days then Maximum Delivery after 50+ form fills) that underpins Steps 7 and 12.
- [knowledge/pro/marketing/ppc-manager/growth-paid-acquisition](../../../knowledge/pro/marketing/ppc-manager/growth-paid-acquisition) — LTV:CAC 3:1 minimum gate and the test-and-scale rule that sets the $50/day minimum and the 14-day evaluation window before scaling budget.
