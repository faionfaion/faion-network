---
name: newsletter-setup
description: Launch a newsletter from zero — pick a platform, configure DNS auth, write your first 3 issues, embed a signup form, and reach 100 subscribers.
tier: solo
group: content-marketing
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a live newsletter on Beehiiv (free up to 2,500 subscribers), with DKIM/SPF configured on your sending domain, three drafted issues with concrete subject lines and structure, a signup form embedded on your landing page, and a repeatable process that gets you to your first 100 subscribers.

## Prerequisites

- A domain you control (DNS managed in Cloudflare or your registrar).
- A landing page you can edit (any static site, Webflow, Carrd, or similar).
- A list of at least 50 personal contacts you can email directly.
- Accounts: Beehiiv (free tier, no card required), Cloudflare (or registrar DNS access).

## Steps

1. **Create a Beehiiv account** at https://www.beehiiv.com — sign up with your work email, choose the free plan (Launch tier, up to 2,500 subscribers, $0/mo).

2. **Create a publication** — in the Beehiiv dashboard click "New Publication", enter your newsletter name (e.g. `NicheWeekly`), choose a subdomain (`nicheweekly.beehiiv.com`), and pick the `Blog/Creator` template for a clean starting layout.

3. **Connect your sending domain** — go to Settings → Custom Domain, enter your domain (e.g. `mail.mydomain.com`), and copy the three DNS records Beehiiv shows (one CNAME for tracking, two TXT records for DKIM).

4. **Add DNS records in Cloudflare** — log in to https://dash.cloudflare.com, select your domain, open DNS → Records, add each record Beehiiv listed:
   - `Type: CNAME`, `Name: mail`, `Target: tracking.beehiiv.com`, Proxy off (DNS only).
   - Two `TXT` records with the exact values from Beehiiv (they start with `v=DKIM1; k=rsa; p=...`).

5. **Add SPF to your root domain** — if your domain has no SPF record yet, add:
   ```
   Type: TXT  Name: @  Content: v=spf1 include:beehiiv.com ~all
   ```
   If an SPF record already exists, append `include:beehiiv.com` before the `~all` or `-all` terminator.

6. **Verify DNS in Beehiiv** — return to Settings → Custom Domain and click "Verify DNS". Wait up to 30 minutes if propagation is still running; Beehiiv will show a green checkmark when DKIM and SPF pass.

7. **Write Issue 1 — The Welcome Issue**
   - Subject: `Welcome — here is what you will get every week`
   - Hook (2 sentences): state who this newsletter is for and the one transformation it delivers.
   - Value: bullet list of 3 things readers will learn or get in future issues.
   - CTA: "Reply and tell me your biggest challenge with [topic]." (replies warm up your sender reputation.)

8. **Write Issue 2 — The Flagship How-To**
   - Subject: `How I [achieved specific result] in [timeframe] (step-by-step)`
   - Hook: open with the problem or mistake that led to the result.
   - Value: numbered steps, real numbers or screenshots, one concrete takeaway per step.
   - CTA: "Forward this to one person who would find it useful."

9. **Write Issue 3 — The Curated Roundup**
   - Subject: `5 [topic] resources worth your time this week`
   - Hook: one sentence on why you curated these (your filter criterion).
   - Value: five links, each with a 1-sentence reason it matters.
   - CTA: Link to your signup page with "Know someone who should read this? Send them here: [signup URL]".

10. **Schedule Issues 1–3** — in Beehiiv set Issue 1 to send immediately on launch day, Issue 2 seven days later, Issue 3 fourteen days later. Use the same send time (e.g. 09:00 local) for consistency.

11. **Embed a signup form on your landing page** — in Beehiiv go to Grow → Embed Form, copy the HTML snippet, and paste it into your landing page's hero section or a dedicated `/subscribe` page. Test the form by subscribing with a secondary email.

12. **Hand-invite 50 personal contacts** — draft a short personal email (not a newsletter, a plain-text message):
    ```
    Subject: Quick ask — would you read this?

    Hi [Name],

    I just launched a newsletter about [topic]. You came to mind because [specific reason].

    One click to subscribe: [signup URL]

    If it is not for you, no worries at all.

    [Your name]
    ```
    Send individually (not BCC) to 50 people you know. Personal emails get 40–60% open rates; blast emails get 20%.

13. **Post in 3 niche communities** — identify the top subreddits or Slack groups for your topic (e.g. `r/SideProject`, `r/Entrepreneur`, a relevant Slack group). Post a value-first comment or thread (answer a real question, then mention the newsletter as a resource at the end — do not post a raw signup link or you will be banned). Do this on days 1, 3, and 7 post-launch.

14. **Set up a referral prompt in Issue 3** — Beehiiv has a built-in referral widget (Grow → Referral Program). Enable it, set the reward to "Shoutout in next issue" (zero cost), and add the widget block to Issue 3 above the footer.

## Verify

Send yourself a test issue from Beehiiv and run it through https://www.mail-tester.com (paste the provided email address as recipient, send the test, then check your score). A passing result shows:

- Score ≥ 8/10.
- SPF: pass.
- DKIM: pass.
- DMARC: pass or neutral (Beehiiv sets a DMARC policy automatically; verify with `dig TXT _dmarc.mydomain.com`).

If all four pass, your newsletter infrastructure is correctly configured.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Beehiiv DNS verification stays red after 30 minutes | CNAME or TXT records not saved, or Cloudflare proxy is ON for the CNAME | Open Cloudflare DNS panel, confirm all three records exist exactly as Beehiiv specified; set the CNAME to "DNS only" (grey cloud, not orange) |
| mail-tester DKIM fail even after DNS verification passed | Multiple DKIM TXT records with the same selector | Run `dig TXT beehiiv._domainkey.mydomain.com` — if you see two conflicting records, delete the old one in Cloudflare |
| SPF "permerror: too many DNS lookups" | Existing SPF chain already has 10 `include:` entries | Flatten the SPF record using https://dmarcanalyzer.com/spf/spf-record-flattener/ before adding `include:beehiiv.com` |
| Personal invite emails bounce or go to spam | Sending from a free Gmail/Yahoo address with no SPF | Send from your custom-domain address (e.g. `hello@mydomain.com`) — set up Google Workspace Starter ($6/mo) or use Cloudflare Email Routing to a Gmail and reply from that alias |
| Community posts removed by moderators | Raw signup links violate sub/group rules | Lead with genuine value (answer a question or share analysis), mention the newsletter only as a secondary resource; check sidebar rules before posting |

## Next

- Once you reach 100 subscribers, run a **reader survey** (Typeform free tier) to find the single topic they want most — use results to plan the next 4 issues.
- At 500 subscribers, consider upgrading to Beehiiv Scale ($39/mo) to unlock the ad network and paid subscriptions.
- Pair with the content-marketer methodology on growth loops to set up a systematic content-repurposing pipeline (turn each issue into a Twitter/X thread + LinkedIn post).

## References

- [knowledge/solo/marketing/content-marketer/growth-email-marketing](../../../knowledge/solo/marketing/content-marketer/growth-email-marketing) — sender-reputation mechanics (SPF/DKIM/DMARC) and deliverability warm-up sequence back Steps 3–6 of this playbook directly
- [knowledge/solo/marketing/content-marketer/growth-newsletter-growth](../../../knowledge/solo/marketing/content-marketer/growth-newsletter-growth) — referral-loop and community-seeding tactics that inform the hand-invite and subreddit posting steps (Steps 12–14)
- [knowledge/solo/marketing/content-marketer/growth-content-marketing](../../../knowledge/solo/marketing/content-marketer/growth-content-marketing) — hook/value/CTA issue structure used as the template for all three draft issues in Steps 7–9
