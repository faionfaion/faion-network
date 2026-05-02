---
name: free-analytics-posthog
description: Add product analytics to any website with PostHog free tier — track page views, capture custom events, and verify data in the live-events feed.
tier: free
group: cost-free-stack
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have PostHog running on your site, capturing page views automatically and one custom event (`signup_clicked`) fired from a button click handler, visible in real time in the PostHog live-events feed — all within the free tier limit of 1 million events per month.

## Prerequisites

- A website you control that serves HTML (static site, Gatsby, Next.js, plain HTML — all work).
- Access to edit the HTML `<head>` of your site (or the equivalent layout file).
- A PostHog account (free signup at https://app.posthog.com — no credit card required for the free tier).
- Basic familiarity with HTML and JavaScript (you know what a `<script>` tag is and how to add an `onclick` handler).

## Steps

### Step 1 — Sign up and create a project

1. Open https://app.posthog.com/signup and create an account with your email.
2. On first login, PostHog asks you to create a project. Name it after your product (e.g., `TaskApp`). Select the **EU Cloud** or **US Cloud** region — this choice is permanent, so pick the region closest to your users.
3. PostHog lands you on the **Getting Started** page. Keep this tab open.

### Step 2 — Copy the JavaScript snippet

1. In the PostHog dashboard, go to **Settings → Project → JavaScript Snippet**.
2. Copy the full snippet. It looks like this (your `YOUR_PROJECT_API_KEY` will be a real key):

```html
<script>
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a=u.__SV=[],u.push(["$set_once",{}]),u._i.push([i,s,a]),["capture","identify","alias","on","once","off","reset","onFeatureFlags","reloadFeatureFlags","addGroup","group","updateEarlyAccessFeatureEnrollment","getActiveMatchingSurveys","renderSurvey","canRenderSurvey","getNextSurveyStep","identify","setPersonProperties","group","resetGroups","setPersonPropertiesForFlags","resetPersonPropertiesForFlags","setGroupPropertiesForFlags","resetGroupPropertiesForFlags","onSessionId","getSessionId","getSessionReplayUrl","getDecideData","init","reset","capture","register","register_once","unregister","identify","createPersonProfile","opt_in_capturing","opt_out_capturing","has_opted_in_capturing","has_opted_out_capturing","clear_opt_in_out_capturing","debug"].forEach(function(t){g(u,t)}),void 0)}(document,window.posthog||[]);
  posthog.init('YOUR_PROJECT_API_KEY', {api_host: 'https://eu.i.posthog.com'})
</script>
```

The snippet PostHog provides is already pre-filled with your real API key and correct `api_host`. Do not hand-edit the key.

### Step 3 — Paste the snippet before `</head>`

Open your site's HTML layout file and paste the snippet as the **last element before `</head>`**.

**Plain HTML site** (`index.html`):

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>TaskApp</title>
  <!-- other head content -->

  <script>
    !function(t,e){ /* ... full PostHog snippet ... */ }
    posthog.init('YOUR_PROJECT_API_KEY', {api_host: 'https://eu.i.posthog.com'})
  </script>
</head>
<body>
  <!-- page content -->
</body>
</html>
```

**Gatsby** (`src/html.js` — run `gatsby build && cp .cache/default-html.js src/html.js` first if the file does not exist):

```jsx
// src/html.js  — add the posthog script inside <head>
<script
  dangerouslySetInnerHTML={{
    __html: `
      !function(t,e){ /* ... full PostHog snippet ... */ }
      posthog.init('YOUR_PROJECT_API_KEY', {api_host: 'https://eu.i.posthog.com'})
    `,
  }}
/>
```

**Next.js** (`app/layout.tsx`):

```tsx
// app/layout.tsx
import Script from 'next/script'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <Script id="posthog" strategy="afterInteractive">{`
          !function(t,e){ /* ... full PostHog snippet ... */ }
          posthog.init('YOUR_PROJECT_API_KEY', {api_host: 'https://eu.i.posthog.com'})
        `}</Script>
      </head>
      <body>{children}</body>
    </html>
  )
}
```

### Step 4 — Capture a custom event from a click handler

Find your sign-up button (or any CTA button) in the HTML and add an `onclick` handler that calls `posthog.capture`:

```html
<!-- Before -->
<button>Start for free</button>

<!-- After -->
<button onclick="posthog.capture('signup_clicked', { location: 'hero' })">
  Start for free
</button>
```

The second argument is an optional properties object. Add any properties that are useful for your analysis — `location`, `plan`, `source`, etc. PostHog stores them as event properties you can filter on.

If you are using React, attach the handler in JSX:

```tsx
<button
  onClick={() => posthog.capture('signup_clicked', { location: 'hero' })}
>
  Start for free
</button>
```

### Step 5 — Deploy and open the live-events feed

1. Deploy your site (push to GitHub Pages, run `gatsby build && deploy`, `next build`, etc.).
2. In the PostHog dashboard, click **Activity → Live Events** in the left sidebar.
3. Open your live site in another browser tab.
4. Click the **Start for free** button.

Within 5–10 seconds you should see two events appear in the live feed:
- `$pageview` — fired automatically by the PostHog snippet on page load.
- `signup_clicked` — fired by your click handler.

## Verify

Open the PostHog **Activity → Live Events** feed. Load your site and click the button. Within 10 seconds, confirm:

1. A `$pageview` event appears with your page URL as `$current_url`.
2. A `signup_clicked` event appears with `location: hero` (or whichever property you set) in the event detail panel.

If both events appear, PostHog is correctly installed and capturing data.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| No events appear in live feed after 30s | Snippet not loading — likely placed after `</head>` or inside a `defer`ed script | Move the snippet to immediately before `</head>`; check browser DevTools → Network for a request to `eu.i.posthog.com` or `us.i.posthog.com` |
| `posthog is not defined` JS error on click | Snippet loads after the click handler fires (e.g., `async`/`defer` on the snippet) | Remove `async`/`defer` from the PostHog `<script>` tag, or wrap `posthog.capture` in a guard: `if (window.posthog) posthog.capture(...)` |
| Events appear in live feed but not in **Insights** | Ingestion delay — PostHog processes live events instantly but Insights queries run on the batch pipeline | Wait 1–2 minutes; refresh the Insights chart |
| `$pageview` fires but custom event does not | `onclick` attribute typo or JSX `onClick` not wired up | Open DevTools Console, type `posthog.capture('test')`, check live feed; if that works, the issue is in the button wiring |
| Free tier quota warning at <1M events/mo | Autocapture is enabled and capturing every click/input by default | Disable autocapture in the init call: `posthog.init('KEY', {api_host: '...', autocapture: false})` — you keep manual `posthog.capture` calls |

## Next

- Enable **Session Replay** (free up to 5k sessions/mo) — PostHog dashboard → Session Replay → Enable. No code change required; the snippet already instruments the page.
- Add `posthog.identify('user-123', { email: 'user@taskapp.com' })` after a successful login to tie events to known users.
- Once you have 100+ `signup_clicked` events, build a **Funnel** in PostHog Insights: `$pageview` → `signup_clicked` → `$pageview` on the `/dashboard` route to measure conversion.

## References

- [knowledge/free/dev/javascript-developer/javascript-modern](../../../knowledge/free/dev/javascript-developer/javascript-modern) — the modern JS standards this playbook follows when writing the click-handler snippet: named event properties as plain object literals, no `var`, browser ES2022+ assumed, matching the same runtime constraints PostHog's own snippet targets.
