---
name: buy-domain-namecheap-cloudflare
description: Buy a domain on Namecheap and delegate DNS management to Cloudflare so you can add records, SSL, and proxying from a single dashboard.
tier: free
group: hosting-infra
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will own a registered domain on Namecheap, have it pointing at Cloudflare's nameservers, and have Cloudflare managing the DNS zone — ready for A, CNAME, MX, or TXT records and free SSL on any service you deploy.

## Prerequisites

- A Namecheap account (free signup at https://www.namecheap.com).
- A Cloudflare account (free signup at https://dash.cloudflare.com).
- A credit or debit card for the domain purchase ($8–15/year for `.com`).
- `dig` installed locally (`dig` ships with `bind-utils` on Linux; macOS includes it by default; Windows: use WSL or https://toolbox.googleapps.com/apps/dig/).

## Steps

1. Sign in at https://www.namecheap.com and type your desired domain into the search field on the homepage.

2. Choose an available `.com` (or `.io` / `.dev` if you accept the price difference). Avoid premium domains marked with a "$" badge — they cost $40–$2000+ and are not worth it at this stage.

3. Click "Add to Cart", skip every upsell (WhoisGuard is free and already checked — keep it; everything else uncheck), and complete checkout.

4. After purchase, click "Manage" next to your new domain in the order confirmation, or go to https://ap.www.namecheap.com/domains/list/ and click "Manage" there.

5. Sign in at https://dash.cloudflare.com and click "Add a site".

6. Enter `mydomain.com` (replace with your actual domain), choose the **Free** plan, and click "Continue".

7. Cloudflare scans existing DNS records. Review the list — keep any records that look correct, delete obvious junk. Click "Continue to activation".

8. Cloudflare shows two nameserver hostnames, for example:
   ```
   anita.ns.cloudflare.com
   bob.ns.cloudflare.com
   ```
   Copy both values exactly.

9. Back in Namecheap → Domain → Nameservers section, select "Custom DNS" from the dropdown, paste the two Cloudflare nameservers into the input fields, and click the green checkmark to save.

10. Return to Cloudflare and click "Check nameservers". Propagation takes 5 minutes to 48 hours; Cloudflare emails you when the zone is active. You can also refresh the Cloudflare dashboard — the zone status changes from "Pending" to "Active".

## Verify

Run the following command, replacing `mydomain.com` with your domain:

```
dig +short NS mydomain.com
```

The output must include both Cloudflare nameserver hostnames (e.g. `anita.ns.cloudflare.com.` and `bob.ns.cloudflare.com.`). If it still shows `dns1.registrar-servers.com`, propagation is not complete — wait 30 minutes and retry.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `dig +short NS` returns Namecheap nameservers after 2h | Custom DNS values were not saved | Open Namecheap → Domain List → Manage → Nameservers → Custom DNS; verify both Cloudflare values appear and re-save |
| Cloudflare zone stays "Pending" for >24h | Wrong nameservers entered | In Cloudflare → your domain → DNS → Nameservers, copy the exact values shown and re-enter them in Namecheap Custom DNS |
| Namecheap shows no "Custom DNS" option | Domain is locked or uses PremiumDNS add-on | Disable PremiumDNS in the Namecheap panel, or unlock the domain under the Security tab |
| Domain purchase fails at checkout | Card declined or 3DS step skipped | Try a different payment method or complete 3DS confirmation in the popup; Namecheap also accepts PayPal |
| Cloudflare "Add a site" rejects the domain | Domain not yet propagated in registrar records | Wait 5 minutes after Namecheap purchase confirmation before adding to Cloudflare |

## Next

- Add an A record pointing `mydomain.com` at your server IP in Cloudflare → DNS → Records to route traffic to a VPS or static host.
- Enable "Full (Strict)" SSL/TLS in Cloudflare → SSL/TLS → Overview once your origin server has a valid certificate.
- Explore the `deploy-static-site-github-pages` playbook to publish a site at no cost before pointing your domain at it.

## References

- [knowledge/free/dev/devtools-developer/github-repo-bootstrap](../../../knowledge/free/dev/devtools-developer/github-repo-bootstrap) — the `gh` CLI workflow pattern used here mirrors how Cloudflare and Namecheap UIs expose config state: read current state first, apply minimal changes, verify with a CLI query (`dig`) rather than assuming the UI reflects live DNS.
