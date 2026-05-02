---
name: landing-page-from-zero
description: Pick a stack, scaffold the project, write Hero/Problem/Solution/CTA copy, embed a Tally email-capture form, and deploy to Vercel with a custom domain — all in one day.
tier: solo
group: frontend-launch
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a live landing page for your product at `https://yourdomain.com`, with a Hero section, Problem/Solution narrative, a call-to-action, an embedded Tally form collecting visitor emails, deployed to Vercel, and served under a custom domain via a CNAME record.

Real product used as example: **Taska** — a one-person project tracker that emails you a daily digest.

## Prerequisites

- Node.js 20+ installed (`node -v` confirms).
- A Vercel account (free signup at https://vercel.com).
- A domain registered and pointing to Cloudflare DNS (or any registrar where you can add a CNAME).
- A Tally account (free at https://tally.so) — you'll create a one-field email-capture form.
- Git installed and configured with a GitHub/GitLab account.
- npm or pnpm available (`npm -v`).

## Steps

### Step 1 — Choose your stack

Pick one based on your shipping target:

| Stack | When to pick | Scaffold command |
|-------|-------------|------------------|
| **Next.js 14 + Tailwind** | You want React component flexibility and may add server routes later | `npx create-next-app@14 taska-landing --typescript --tailwind --eslint --app` |
| **Astro + Tailwind** | Pure static, fastest build, minimal JS by default | `npm create astro@latest taska-landing -- --template minimal` then `npx astro add tailwind` |
| **Plain HTML + Tailwind CDN** | Zero toolchain, single `index.html`, ship in 30 min | No scaffold — create `index.html` manually (see Step 3) |

This playbook follows **Next.js 14 + Tailwind** as the primary path, with HTML-CDN notes where they diverge.

### Step 2 — Scaffold the Next.js project

```bash
npx create-next-app@14 taska-landing \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --no-src-dir \
  --import-alias "@/*"
cd taska-landing
```

Confirm it boots:

```bash
npm run dev
```

Open `http://localhost:3000` — you should see the default Next.js 14 App Router page. Shut down dev server (`Ctrl+C`) and delete the placeholder content:

```bash
# Remove default placeholder styles and page content
rm app/globals.css  # we will rewrite this
```

Replace `app/globals.css` with:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

html {
  scroll-behavior: smooth;
}
```

### Step 3 — Write the four copy sections

Open `app/page.tsx` and replace its entire content with the four-section layout. The copy pattern is: **Hero → Problem → Solution → CTA**.

```tsx
export default function Home() {
  return (
    <main className="min-h-screen bg-white text-gray-900 font-sans">

      {/* Hero */}
      <section className="max-w-2xl mx-auto px-6 pt-24 pb-16 text-center">
        <h1 className="text-4xl font-bold leading-tight mb-4">
          Stop losing track of what needs doing.
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Taska sends you a 9am email every morning: three tasks, no dashboard, no noise.
        </p>
        <a
          href="#waitlist"
          className="inline-block bg-indigo-600 text-white px-8 py-3 rounded-lg text-lg font-medium hover:bg-indigo-700 transition-colors"
        >
          Join the waitlist
        </a>
      </section>

      {/* Problem */}
      <section className="bg-gray-50 py-16">
        <div className="max-w-2xl mx-auto px-6">
          <h2 className="text-2xl font-bold mb-4">Project trackers are built for teams.</h2>
          <p className="text-gray-600 text-lg">
            Jira, Linear, Notion boards — they assume you have standups, sprints, and a PM.
            If you're solo, you spend more time updating the tracker than shipping.
          </p>
        </div>
      </section>

      {/* Solution */}
      <section className="py-16">
        <div className="max-w-2xl mx-auto px-6">
          <h2 className="text-2xl font-bold mb-4">One email. Three tasks. Done.</h2>
          <ul className="space-y-3 text-gray-600 text-lg list-disc list-inside">
            <li>Add tasks via a dead-simple web form or reply to the email.</li>
            <li>Every morning at 9am: your top three tasks land in your inbox.</li>
            <li>No app to open. No dashboard to maintain. No notifications.</li>
          </ul>
        </div>
      </section>

      {/* CTA — Tally embed */}
      <section id="waitlist" className="bg-indigo-50 py-16">
        <div className="max-w-2xl mx-auto px-6 text-center">
          <h2 className="text-2xl font-bold mb-2">Get early access</h2>
          <p className="text-gray-600 mb-8">
            Join 200+ solopreneurs already on the waitlist.
          </p>
          {/* Tally embed — replace FORM_ID with your actual Tally form ID */}
          <iframe
            data-tally-src="https://tally.so/embed/FORM_ID?alignLeft=1&hideTitle=1&transparentBackground=1"
            loading="lazy"
            width="100%"
            height="120"
            title="Taska waitlist"
            frameBorder={0}
            marginHeight={0}
            marginWidth={0}
            className="mx-auto max-w-md"
          />
          <script async src="https://tally.so/widgets/embed.js" />
        </div>
      </section>

    </main>
  );
}
```

**Plain HTML + Tailwind CDN path:** create a single `index.html`, add `<script src="https://cdn.tailwindcss.com"></script>` in `<head>`, and write the four sections using identical class names. Host on any static server or drag-and-drop to Netlify Drop.

### Step 4 — Create the Tally email-capture form

1. Sign in at https://tally.so.
2. Click **New form → Start from scratch**.
3. Add one field: **Email** (required), label it "Your email".
4. Set submit message: "You're on the list. We'll email you when Taska launches."
5. Click **Publish**, then go to **Share → Embed → Inline**.
6. Copy the form ID from the embed snippet (the hash after `tally.so/embed/`).
7. Replace `FORM_ID` in `app/page.tsx` with the actual ID (e.g., `wQ4aXV`).

Verify the embed locally: `npm run dev`, open `http://localhost:3000#waitlist` — the form must render and accept a test submission.

### Step 5 — Push to GitHub and deploy to Vercel

```bash
git init
git add .
git commit -m "feat: initial landing page"
gh repo create taska-landing --public --source=. --push
```

If you don't have the GitHub CLI, create the repo manually at https://github.com/new, then:

```bash
git remote add origin git@github.com:yourusername/taska-landing.git
git push -u origin main
```

Now deploy:

```bash
npx vercel deploy --prod
```

On first run, Vercel CLI prompts you to link the project (accept defaults). It prints the production URL, e.g. `https://taska-landing.vercel.app`.

### Step 6 — Connect a custom domain via CNAME

1. Open https://vercel.com/dashboard, select the `taska-landing` project.
2. Go to **Settings → Domains → Add**.
3. Enter `taska.yourdomain.com` (or `yourdomain.com` for apex).
4. Vercel shows the CNAME target, e.g. `cname.vercel-dns.com`.
5. In Cloudflare (or your registrar's DNS panel), add:

```
Type:  CNAME
Name:  taska          (for taska.yourdomain.com)
Value: cname.vercel-dns.com
TTL:   Auto (Cloudflare proxied OFF for apex, proxied ON for subdomain is fine)
```

For an apex domain (`yourdomain.com`), use an **A record** pointing to `76.76.21.21` (Vercel's IP) instead of a CNAME, because apex CNAMEs are not supported by all DNS providers.

Wait 2–10 minutes for propagation.

## Verify

Run this single command after DNS propagates:

```bash
curl -sI https://taska.yourdomain.com | head -5
```

Expected:

```
HTTP/2 200
content-type: text/html; charset=utf-8
```

HTTP/2 200 confirms Vercel is serving the page over TLS on your custom domain. Open the URL in a browser, scroll to the waitlist form, submit a test email, and confirm Tally records it in https://tally.so/forms/FORM_ID/submissions.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Vercel shows "Invalid domain configuration" | CNAME not yet propagated or pointing to wrong target | Run `dig +short CNAME taska.yourdomain.com` — it must return `cname.vercel-dns.com`. If blank, wait 10 min or re-save the Cloudflare record with proxy OFF. |
| Tally form shows blank iframe | Script tag inside Next.js `page.tsx` is not executed on server render | Move `<script async src="https://tally.so/widgets/embed.js" />` to `app/layout.tsx` inside `<body>` so it loads once per page. |
| `npx vercel deploy --prod` errors: "No project linked" | Vercel CLI not linked | Run `npx vercel link` in the project directory, select the org and project, then re-run deploy. |
| Build fails with TypeScript error on `frameBorder` | Next.js strict JSX types reject `frameBorder={0}` | Remove `frameBorder={0} marginHeight={0} marginWidth={0}` — they are deprecated HTML attrs; the embed renders fine without them. |
| Domain resolves but shows Vercel 404 | Vercel project was not assigned the domain | Go to Vercel → project → Settings → Domains and confirm `taska.yourdomain.com` is listed and verified (green checkmark). |

## Next

- Add analytics before you announce: use Vercel Analytics (`npm i @vercel/analytics`) or Plausible for privacy-first tracking. Add `<Analytics />` to `app/layout.tsx`.
- Write your first announcement copy using the `growth-copywriting-fundamentals` methodology under `solo/marketing/content-marketer/` — specifically the email subject line and Twitter/X thread patterns.
- Once you have 50+ emails, move to `rest-api-in-one-day` playbook to wire up a real sign-up endpoint with confirmation emails.

## References

- [knowledge/solo/dev/frontend-developer/tailwind](../../../knowledge/solo/dev/frontend-developer/tailwind) — Tailwind utility class patterns and responsive layout conventions used in the Hero/Problem/Solution sections to maintain consistent spacing (`px-6`, `max-w-2xl`, `py-16`) and color scale.
- [knowledge/solo/marketing/content-marketer/growth-copywriting-fundamentals](../../../knowledge/solo/marketing/content-marketer/growth-copywriting-fundamentals) — Problem-agitation-solution copy structure applied directly to the four section headers: Hero headline leads with pain, Problem names the existing broken alternative, Solution presents the mechanism, CTA converts.
