---
name: landing-page-essentials
description: Write and ship a one-page site that converts visitors into signups using a 7-block structure and concrete copy formulas.
tier: free
group: marketing-fundamentals
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a live one-page site with a single primary CTA — built on the 7-block structure (Hero, Problem, Solution + Features, Social Proof, CTA, FAQ, Footer) — that turns cold traffic into email signups or trial starts without paid ads or a navigation menu.

## Prerequisites

- A confirmed problem hypothesis (at least two real customer conversations; see `mom-test-customer-interview`).
- A one-sentence positioning statement or a draft of who you help and what outcome you deliver (see `positioning-basics`).
- A free account on a static hosting platform: https://vercel.com (free tier) or https://pages.github.com.
- A form or signup endpoint: https://app.mailerlite.com (free up to 1,000 subscribers) or a Stripe Payment Link for paid signups.
- A text editor (VS Code is fine) and basic HTML/CSS ability, OR a no-code page builder account: https://carrd.co ($0 plan allows one site).

## Steps

### Block 1 — Hero: state the single outcome

1. Write your headline using the Before/After/Bridge formula:
   - **Before:** describe the reader's world right now (the pain state).
   - **After:** describe the world after your product works.
   - **Bridge:** name your product as the mechanism that moves them.
   - Example for a VAT compliance tool for Etsy sellers: "Etsy sellers in the EU spend 3–6 hours per quarter guessing which VAT rates apply to digital goods. VATwise calculates the correct rate for every sale automatically — so you file in under 10 minutes."
2. Write a sub-headline (one sentence, ≤20 words) that names the target persona and the primary benefit: "For Etsy sellers shipping digital downloads to EU buyers."
3. Add a single primary CTA button. Label it with an outcome verb, not a generic one: "Calculate my VAT now" beats "Get started". Point the button at your signup form or Stripe link. **No navigation menu on the page.**
4. Add one hero visual: a product screenshot, a before/after data comparison, or a 3-second screen recording (GIF). No stock photos of people shaking hands.

### Block 2 — Problem: make the pain legible

5. Write 2–3 sentences using the Problem-Agitate-Solution (PAS) opening, stopping before the solution: describe the exact situation where the pain occurs, then twist the knife by naming the downstream consequence. Example: "EU VAT rules for digital goods change every year. Miss a rate update and you owe back-tax plus penalties. Most Etsy sellers discover the error at tax time — when it's too expensive to fix."
6. Keep this block to 3–5 lines. No bullet points here — flowing prose reads as empathy, not a feature list.

### Block 3 — Solution + three features

7. Introduce your product with one sentence that positions it as the direct answer to the problem stated above: "VATwise reads your Etsy order export, looks up the current VAT rate for each buyer's country, and generates a ready-to-submit report."
8. List exactly three features as outcome-led bullet points. Format: **Feature name** — what it does for the user, not how it works technically.
   - **Live rate database** — always reflects the latest EU digital-goods VAT rates, updated within 24 hours of any change.
   - **One-click Etsy import** — paste your order CSV and VATwise parses buyer location automatically; no manual entry.
   - **Filing-ready PDF** — download a report formatted for OSS (One Stop Shop) VAT returns, accepted by all EU tax authorities.
9. Do not list more than three features. More features at this stage signal uncertainty about your value prop.

### Block 4 — Social proof

10. Add at least one piece of proof. In order of preference:
    - A direct quote from a paying customer with their first name, shop name, and country: "I used to dread VAT season. Now I run VATwise on the last day of the quarter and I'm done in 8 minutes. — Lena K., LenaDesigns, Netherlands."
    - A concrete usage number: "47 Etsy sellers used VATwise to file Q1 2025 VAT returns without a single penalty."
    - A media mention or indie newsletter feature with the outlet name.
    - If you have none yet, a brief founder note works: "I'm Ruslan, I ran an Etsy shop for 3 years and got a VAT penalty in 2023. I built VATwise so no one else has to learn this the hard way."
11. Display social proof directly beneath the Solution block — before the main CTA — because visitors scan top-to-bottom and trust must precede the ask.

### Block 5 — Primary CTA (repeated)

12. Repeat the exact same CTA button from the Hero, same label, same destination. Place it immediately after social proof. This is not a new offer — it is a second chance for visitors who scrolled past the first button.

### Block 6 — FAQ (handle the top three objections)

13. Identify the three objections that killed deals in your early customer calls (see your `first-10-customers` call notes). Write one FAQ entry per objection. Format each as a direct question the buyer would actually type, followed by a 2–4 sentence answer that resolves the doubt without hedging.
    - Example Q: "Does VATwise work if I sell in both the EU and the US?" A: "Yes. VATwise processes EU transactions and ignores non-EU orders automatically. US sales are not subject to EU VAT — VATwise will mark them as exempt in your report."
    - Example Q: "What if the VAT rules change after I buy?" A: "Your subscription includes all rate updates. We email you within 48 hours of any change to EU digital-goods rates."
    - Example Q: "I only sell 10–20 items a month. Is it worth it?" A: "The EU OSS filing threshold is €10,000/year across all EU countries. If you're above that — and many Etsy sellers are after a few years — you are legally required to file. VATwise pays for itself in the first quarter you avoid a late-filing fee."
14. Keep the FAQ block to three entries. Move anything else to a help doc linked from the footer.

### Block 7 — Footer

15. Add a footer with: your product name, a one-line description, a link to your privacy policy (required for any email capture — use https://termly.io to generate one free), and a contact email. No social media icons unless your product category expects them (most SaaS categories do not).
16. Do not add a blog, pricing page link, or "About" page at this stage. Every link is an exit ramp. Keep the visitor on the conversion path.

### Publish

17. If using Carrd: create a new site at https://app.carrd.co, choose the "Landing Page" template, replace every text block with your copy from Steps 1–16, connect your form element to MailerLite or your Stripe link, publish under a `.carrd.co` subdomain or your own domain.
18. If writing HTML: create `index.html` with your 7 blocks, push to a GitHub repo, connect the repo to Vercel at https://vercel.com/new, deploy. Use a `<meta name="viewport" content="width=device-width, initial-scale=1">` tag so the page is readable on mobile.
19. Set up basic analytics by adding the PostHog snippet (see `free-analytics-posthog`) before the closing `</body>` tag. You need to know where visitors drop off to improve conversion.

## Verify

Open the live URL in an incognito browser window. Run through this checklist in order:

1. The headline passes the "5-second test": cover the rest of the page and ask a stranger what the product does and who it's for. They should answer correctly within 5 seconds.
2. The CTA button is visible without scrolling on a 375 px wide screen (iPhone SE). Check with browser DevTools → Toggle device toolbar → set width to 375.
3. Submit the signup form with a test email address. Confirm the email lands in your MailerLite subscriber list (or the Stripe test charge completes if using a payment link).
4. Run `curl -s -o /dev/null -w "%{http_code}" https://your-domain.com` — returns `200`.
5. Open https://pagespeed.web.dev and paste your URL. Mobile performance score ≥ 70 (Carrd and Vercel static sites typically score 85+).

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Visitors land but bounce in under 10 seconds (PostHog session replay shows immediate exit) | Hero headline does not match the ad or link that brought them (traffic-message mismatch) | Open PostHog → Recordings and watch 5 sessions. Check the referrer. If traffic is organic, the headline may be too vague; if paid, align ad copy to headline word-for-word. |
| Signup form submits but no subscriber appears in MailerLite | Form action URL or API key is wrong | In MailerLite → Forms → your form → Settings, copy the embed code again. The `action` attribute must match exactly. Test with a real email, not a `+test` alias — some form providers strip them. |
| Page loads slowly on mobile (PageSpeed < 70) | Hero image is an uncompressed PNG over 500 KB | Compress the image at https://squoosh.app (target < 80 KB for a hero image at 1200 px wide). Use WebP format. |
| CTA button is invisible on mobile | Button colour has low contrast against the background | Check contrast at https://webaim.org/resources/contrastchecker. Minimum ratio 4.5:1 for normal text. Use a high-contrast button colour (dark background + white text, or bright accent). |
| Visitors read the FAQ but still don't convert | FAQ answers hedge ("it depends", "usually", "in most cases") | Rewrite each answer as a direct statement that fully resolves the doubt. Hedged answers are worse than no FAQ — they amplify uncertainty. |
| Domain shows Vercel's default page instead of your site | DNS not propagated or Vercel project not linked to the domain | In Vercel dashboard → your project → Settings → Domains, add your domain and copy the provided A record or CNAME. Allow up to 24 hours for DNS propagation. Run `dig +short A your-domain.com` to confirm it points at Vercel's IP. |

## Next

- [positioning-basics](../positioning-basics/playbook.md) — tighten the Hero headline further by stress-testing your positioning statement against three competing alternatives.
- [first-10-customers](../first-10-customers/playbook.md) — if you haven't sourced your first paying users yet, do that before investing in conversion optimisation; low traffic makes A/B data meaningless.
- `free-analytics-posthog` — instrument the page with session recording and funnel analysis to identify which block loses the most visitors.

## References

- [knowledge/free/marketing/marketing-manager](../../../knowledge/free/marketing/marketing-manager) — the orchestrator's routing logic places landing-page work under faion-conversion-optimizer, not faion-content-marketer; this playbook applies that routing decision by structuring the page around a single conversion path (no menu, single CTA) rather than content engagement, which is the conversion-first stance the routing table prescribes.
