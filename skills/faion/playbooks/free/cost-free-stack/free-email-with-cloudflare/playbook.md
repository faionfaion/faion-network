---
name: free-email-with-cloudflare
description: Set up a professional email address on your own domain for free using Cloudflare Email Routing, forwarding to an existing Gmail inbox.
tier: free
group: cost-free-stack
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have `hi@yourdomain.com` (or any address you choose) forwarding to your existing Gmail account, with SPF and DMARC records in place so inbound mail passes spam checks — all at zero cost, using Cloudflare Email Routing.

## Prerequisites

- A domain already on Cloudflare nameservers (Cloudflare shows it as **Active** in your dashboard). If your domain is still on a registrar's nameservers, point it to Cloudflare first.
- A Cloudflare account with access to that domain (free plan is sufficient).
- A Gmail address you actively use — this is the destination inbox.
- No prior email setup on this domain (no existing MX records). If you have MX records from another provider, remove them first.

## Steps

### Step 1 — Open Email Routing in the Cloudflare dashboard

1. Sign in at https://dash.cloudflare.com.
2. Click your domain name in the account list.
3. In the left sidebar, click **Email** → **Email Routing**.
4. Click **Get started** (or **Enable Email Routing** if the button says that).

Cloudflare opens a three-step wizard: Routing addresses → Custom addresses → DNS records.

### Step 2 — Add a destination address (your Gmail)

1. On the **Routing addresses** step, type your Gmail address in the **Destination email** field (e.g., `yourname@gmail.com`).
2. Click **Send verification email**.
3. Open Gmail and look for a message from Cloudflare with subject **"Verify your email address"**. Click the **Verify email address** button in that message.
4. Return to the Cloudflare tab. The address should now show a green **Verified** badge. Click **Next**.

### Step 3 — Create a custom address

1. On the **Custom addresses** step, type the local part you want — for example, `hi` — in the first field. The field to the right shows `@yourdomain.com`.
2. In the **Action** dropdown, select **Send to an email**.
3. In the **Destination** field, select the Gmail address you just verified.
4. Click **Save** to add the rule.
5. Click **Next**.

You now have `hi@yourdomain.com` → `yourname@gmail.com` configured.

### Step 4 — Apply the DNS records Cloudflare recommends

1. On the **DNS records** step, Cloudflare lists the MX, SPF, and DMARC records it needs. The list typically looks like:

   | Type | Name | Value |
   |------|------|-------|
   | MX | `yourdomain.com` | `route1.mx.cloudflare.net` (priority 67) |
   | MX | `yourdomain.com` | `route2.mx.cloudflare.net` (priority 28) |
   | MX | `yourdomain.com` | `route3.mx.cloudflare.net` (priority 96) |
   | TXT | `yourdomain.com` | `v=spf1 include:_spf.mx.cloudflare.net ~all` |
   | TXT | `_dmarc.yourdomain.com` | `v=DMARC1; p=none` |

2. Click **Add records automatically**. Cloudflare creates all listed records in your DNS zone.
3. Click **Finish**.

The Email Routing overview page now shows **Email Routing: Enabled** and lists your `hi@yourdomain.com` rule.

### Step 5 — Send a test email

1. Open a separate email client (e.g., your phone's Mail app, a second Gmail account, or any service).
2. Send a plain-text email to `hi@yourdomain.com` with any subject.
3. Wait up to 60 seconds and check your Gmail inbox.

The message should arrive with the original sender in the **From** field and `hi@yourdomain.com` shown as the recipient.

## Verify

In Gmail, open the forwarded test message and click **More** (the three-dot menu) → **Show original**. Confirm all three of the following in the raw headers:

- `Received-SPF: pass` — SPF record resolved correctly.
- `Authentication-Results: ... dmarc=pass` — DMARC policy evaluated.
- `To: hi@yourdomain.com` — the envelope address matches your custom address.

If all three appear, email routing is working and your domain's mail authentication records are valid.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Test email never arrives in Gmail | Forwarding rule saved but destination address not verified | In Cloudflare → Email → Email Routing → **Destination addresses**, check that Gmail shows **Verified**. Resend the verification email if needed. |
| Gmail marks the forwarded email as spam | SPF/DMARC records not yet propagated | Check Cloudflare DNS tab — MX and TXT records must show no orange proxy cloud (DNS-only). Wait 5 minutes and re-test. |
| Cloudflare shows **DNS conflict** warning | Existing MX records from a previous provider still present | Go to Cloudflare DNS tab, delete the old MX records, then re-apply the Cloudflare Email Routing records from the wizard. |
| `Route not found` bounce reply | Rule was saved without a destination or destination was unverified at save time | Delete the rule in Email Routing → **Routing rules**, re-add it, and confirm the destination address badge is green before saving. |
| Cannot find **Email Routing** in sidebar | Domain is on a Business or Enterprise plan where the UI layout differs | Look under **Email** in the left sidebar; if absent, go to https://dash.cloudflare.com/?to=/:account/:zone/email/routing directly. |

## Next

- Add a **catch-all** rule: in Email Routing → **Routing rules**, click **Catch-all address** → **Send to an email** → select your Gmail. This ensures mail sent to any address on your domain (`contact@`, `support@`, etc.) reaches you during early launch.
- Configure **Send as** in Gmail (Settings → Accounts and Import → Send mail as → Add another email address) so you can reply from `hi@yourdomain.com` directly inside Gmail. This requires an SMTP relay such as Brevo (free up to 300 emails/day).
- Once you have consistent sending volume, upgrade the DMARC policy from `p=none` to `p=quarantine` by editing the `_dmarc` TXT record value to `v=DMARC1; p=quarantine; rua=mailto:hi@yourdomain.com`.

## References

- [knowledge/free/dev/devtools-developer/github-repo-bootstrap](../../../knowledge/free/dev/devtools-developer/github-repo-bootstrap) — the DNS record verification pattern from this methodology (confirming records propagate before treating setup as complete) directly informs the Verify step, where raw headers confirm SPF/DMARC pass rather than trusting the UI alone.
