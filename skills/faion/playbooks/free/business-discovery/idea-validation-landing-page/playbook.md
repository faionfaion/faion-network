---
name: idea-validation-landing-page
description: Stand up a one-page landing with an email-capture form, push $30 of paid traffic at it, and measure whether real strangers want your unbuilt product.
tier: free
group: business-discovery
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a live single-page site describing your unbuilt product, a working "Get early access" form backed by Tally or Formspree, and a traffic experiment with $30 of paid ads that tells you — within 72 hours — whether strangers care enough to give you their email. Pass threshold: ≥10% email-capture rate on landing-page visitors, or ≥30 collected emails, whichever comes first.

## Prerequisites

- A one-sentence problem statement and a name for your unbuilt product (e.g. "RevisionStack — the revision-feedback hub for freelance designers").
- A hypothesis from at least one customer interview (see [mom-test-customer-interview](../mom-test-customer-interview/playbook.md)).
- Accounts at: Carrd (free plan at https://carrd.co) or Framer (free plan at https://framer.com). Carrd is simpler for non-developers; Framer gives more design control.
- A Tally account (free at https://tally.so) OR a Formspree account (free at https://formspree.io) to host the email-capture form.
- A $30 budget for paid traffic: Twitter/X Ads (https://ads.twitter.com), Reddit Ads (https://ads.reddit.com), or Meta Ads (https://www.facebook.com/adsmanager). Any one of the three is sufficient.
- A UTM-aware link ready (built at https://ga-dev-tools.google/campaign-url-builder/) so you can track which channel sends traffic.
- Optional: a custom domain ($8–12/year on Namecheap); otherwise use the free Carrd/Framer subdomain.

## Steps

1. Write the page copy before touching any tool. In a plain text file, draft four blocks:
   - **Headline** (≤10 words): what it does for the reader. Example: "Stop losing client revision notes across 6 different apps."
   - **Sub-headline** (≤20 words): who it is for + the outcome. Example: "RevisionStack centralises every design revision round so freelancers ship faster and fight less."
   - **Three bullet benefits**: each starts with a verb and names a concrete outcome. Example: "Collect all client feedback in one thread — no more digging through email and Slack." Do not describe features; describe results.
   - **CTA sentence** below the form: "Join 47 designers getting early access." (Start with "Join 0" if you have no list yet; update as signups arrive.)

2. Open https://carrd.co, sign in, click "Build a site", choose "Landing Page". If using Framer, open https://framer.com, click "Start for free", pick "Marketing" → "Landing".

3. Delete every default section except the hero block. You need exactly: headline, sub-headline, bullet benefits, form, and one optional product screenshot or rough wireframe image (skip if nothing exists yet — a plain colour background is fine).

4. Paste your copy from Step 1 into the hero block. Keep font stack and colours minimal — a dark-on-white or white-on-dark single-colour background eliminates design decisions and loads fast.

5. Create the capture form. In Tally: open https://tally.so/dashboard, click "New form", add a single "Email" field and a "Submit" button labelled "Get early access". Copy the embed code. In Formspree: open https://formspree.io, create a new form, copy the `<form action="...">` snippet. Back in Carrd/Framer, add an "Embed" block and paste the form code.

6. Set the form success message to: "You're on the list. We'll email you when RevisionStack opens." (Adjust product name.) Do not redirect to another URL — keep people on the page.

7. Publish the page. In Carrd: click "Publish" → use the free `yourname.carrd.co` subdomain or connect a custom domain. In Framer: click "Publish" → share the generated `.framer.website` URL or connect your domain.

8. Build your UTM tracking link. Go to https://ga-dev-tools.google/campaign-url-builder/, enter:
   - Website URL: your published page URL
   - Campaign Source: `twitter` (or `reddit` / `meta`)
   - Campaign Medium: `paid`
   - Campaign Name: `idea-validation-<your-product-slug>`
   Copy the resulting link — this is what your ad will point to.

9. Set up the paid traffic campaign. Pick one channel and follow the minimum-spend path:

   **Twitter/X Ads** — go to https://ads.twitter.com, click "Create campaign", choose "Website traffic". Set daily budget to $10/day for 3 days. Audience: choose "Interest targeting" → pick 2–3 interests that match your persona (e.g. "Freelancing", "Graphic Design", "Creative software"). Ad copy: your headline from Step 1 + UTM link. No image required for a text ad.

   **Reddit Ads** — go to https://ads.reddit.com, click "Create campaign", goal = "Traffic". Set $10/day for 3 days. Target 2–3 subreddits where your persona hangs out (e.g. r/freelance, r/graphic_design, r/web_design). Ad: headline + sub-headline as body + UTM link. "Link ad" format, no custom creative needed.

   **Meta Ads** — go to https://www.facebook.com/adsmanager, create a "Traffic" campaign, set $10/day, 3-day schedule. Detailed targeting: interests matching your persona (e.g. "Freelancer", "Adobe Creative Cloud", "Graphic design"). Ad creative: a 1200×628px image (create in Canva free at https://canva.com) showing the headline text over a coloured background, plus UTM link in the destination URL field.

10. After spending $30 (or 72 hours, whichever comes first), open your Tally or Formspree dashboard and count collected emails. Open your UTM report (in Twitter/Reddit/Meta analytics) to count landing-page visitors.

11. Calculate: `capture_rate = emails_collected / page_visitors * 100`. Compare against pass thresholds:
    - ≥10% capture rate → demand signal confirmed, move to [mvp-scope-cutting](../../mvp-essentials/mvp-scope-cutting/playbook.md).
    - ≥30 emails (regardless of rate) → list large enough to conduct beta, move forward.
    - &lt;10% and &lt;30 emails → revise headline and benefits (return to Step 1), run a second $30 experiment before concluding.

## Verify

Open your form provider dashboard (Tally: https://tally.so/forms, Formspree: https://formspree.io/forms) and confirm the email count. Then run:

```
curl -s -o /dev/null -w "%{http_code}" https://<your-page-url>
```

Returns `200`. If you see `301` or `302`, the redirect chain is adding latency — check that your custom domain is set to the published URL, not an intermediate redirect.

A passing experiment looks like: 400 visitors, 45 emails = 11.25% capture rate. A failing experiment to revisit: 350 visitors, 28 emails = 8% capture rate — below both thresholds, requiring headline revision before the next ad run.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| 0 emails after $30 spend | Traffic never reached the landing page — UTM link was broken or ad rejected | Open the ad platform's delivery report; if impressions > 0 but clicks = 0, the creative was rejected. Rewrite ad copy removing superlatives ("best", "#1") which trigger rejection. If clicks > 0 but form submissions = 0, the embed is broken — test the Tally/Formspree form URL directly in incognito. |
| Ad account rejected at signup | Platform requires business verification or billing address match | Use a personal credit card matching your registered name. Reddit and Twitter accept individual accounts. Meta may ask for identity verification — submit ID via https://www.facebook.com/help/1735443093393986 |
| Very low CTR on ad (&lt;0.5%) | Headline does not match the audience's vocabulary | Go to the subreddit or Twitter search for your persona's terms. Replace abstract words ("centralise") with the exact words they use in posts ("stop losing", "track all feedback"). |
| Carrd/Framer page not indexable | Not a concern for a 72-hour experiment — search engines won't index it in time anyway | No action needed; all traffic comes from paid links, not organic. |
| Email capture rate is 15% but only 8 emails total | Spend was too low to reach statistical confidence | The signal is promising — run a second $30 experiment on a different channel before deciding. 30 emails from any source is the floor for a meaningful list. |
| Tally form shows "upgrade to collect responses" | Free plan hit 100-response limit | Export current responses, then switch to Formspree free tier (50 submissions/month) for the remainder of the experiment. |

## Next

- [mvp-scope-cutting](../../mvp-essentials/mvp-scope-cutting/playbook.md) — if the experiment passes, cut scope to the single feature that matches the most-cited benefit from your email list.
- [first-10-customers](../../marketing-fundamentals/first-10-customers/playbook.md) — email every person on your list personally before building anything; convert 3–5 of them to paid beta users.
- [niche-selection-framework](../niche-selection-framework/playbook.md) — if signups came from two different personas, use this framework to pick the one segment to build for first.

## References

- [knowledge/free/dev/software-developer/mobile-responsive](../../../knowledge/free/dev/software-developer/mobile-responsive) — the landing page's email-capture rate depends directly on mobile usability: over 60% of Twitter/Reddit paid-ad clicks open on mobile, so applying the single-column, thumb-reachable CTA layout described in this methodology prevents conversion loss before a visitor ever reads the headline.
- [knowledge/free/dev/software-developer/tailwind](../../../knowledge/free/dev/software-developer/tailwind) — if using a static HTML page instead of Carrd/Framer, Tailwind's utility classes (specifically `max-w-xl mx-auto`, `text-4xl font-bold`, and `py-4 px-8`) produce a readable single-column hero in under 20 lines without writing custom CSS, keeping the page build under 30 minutes.
