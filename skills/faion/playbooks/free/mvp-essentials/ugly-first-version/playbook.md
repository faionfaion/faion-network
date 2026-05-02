---
name: ugly-first-version
description: Ship a deliberately unpolished v1 in 3-7 days using a fixed "ugly budget", default browser styles, and a single landing-page link to reach 5-10 real users fast.
tier: free
group: mvp-essentials
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working product behind a public URL, a log of reactions from 5-10 real users, and clear evidence of whether the core interaction is worth polishing — all before spending a single hour on visual design.

## Prerequisites

- A scoped feature list of ≤5 items (see `mvp-scope-cutting` if you have more).
- A working local build of any web app (Python/Django, Node/Express, Rails, or similar).
- A domain or a free subdomain you control (e.g., `myapp.railway.app`, `myproject.vercel.app`).
- A place to post one link publicly — your personal Twitter/X account, a relevant Discord server, a Reddit community, or a newsletter with ≥50 subscribers.
- No prior design experience required. The entire point is to skip it.

## Steps

### Step 1 — Lock the ugly budget

Open a plain text file named `V1-CONTRACT.md` at your project root. Write exactly three lines:

```
Ship date: <date 3-7 days from today>
Design budget: 0 hours
Color palette: max 3 colors (black, white, one accent)
```

Treat this file as a commitment. If you feel the urge to open Figma or adjust spacing, re-read it. The budget is not negotiable during v1.

### Step 2 — Set the minimum UI baseline

Remove any custom CSS files from your project. Add a single stylesheet tag pointing to a classless CSS reset that applies readable default styles with zero custom work:

```html
<link rel="stylesheet" href="https://unpkg.com/sakura.css/css/sakura.css">
```

This gives you readable typography, sensible margins, and a neutral background in one line. You are now done with design.

If sakura.css conflicts with your framework, use `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">` instead — both are classless and require zero configuration.

### Step 3 — Pick one accent color and stop

Open your browser's DevTools color picker, or go to https://coolors.co/generate and hit the spacebar once. Take the first color that is not white, black, or grey. Add it as a single CSS variable:

```css
:root { --accent: #4361ee; }
```

Use `--accent` only for the primary button and active states. Use it nowhere else. You now have your 3-color palette: black text, white background, one accent.

### Step 4 — Build only the core loop

The core loop is: a user arrives → does one thing → sees a result. For **TaskFlow** (a freelancer task tracker): user adds a task, sees it in a list, marks it done. Build exactly that. Implement no profile page, no settings, no onboarding wizard, no empty-state illustration. If a feature is not in your V1-CONTRACT.md feature list, delete the code or comment it out with `# TODO v2:`.

### Step 5 — Deploy behind a single public URL

Push to a free hosting provider that gives you a live URL in under 10 minutes:

- **Railway:** `railway up` from your project root → `https://myapp.railway.app`
- **Render:** connect your GitHub repo at https://render.com → auto-deploy on push
- **Vercel:** `npx vercel --prod` from a Next.js or static project root

Write the live URL into `V1-CONTRACT.md`:

```
Live URL: https://taskflow-v1.railway.app
```

Do not buy a custom domain yet. Do not set up a CDN. A plain URL is sufficient.

### Step 6 — Write a one-sentence landing page intro

Replace your homepage `<h1>` with one sentence that names the user and the problem:

```
TaskFlow lets freelancers track tasks without leaving their browser tab.
```

Add a single call-to-action button labeled "Try it now" that links to the core loop. Do not add a features list, testimonials section, or pricing table. The page should be navigable in under 10 seconds.

### Step 7 — Post the link and log reactions

Post the URL in one or two places where your target user lives. For TaskFlow: a freelancer subreddit (`r/freelance`, `r/digitalnomad`) or a relevant Discord community. Write one line in `V1-CONTRACT.md` for each of the first 5-10 people who respond:

```
User #1 (Reddit r/freelance): "where is the due date field?" — feature gap
User #2 (Discord): signed up, used it for 10 minutes, said "good enough" — positive signal
User #3 (Reddit r/freelance): "I already use Notion" — wrong audience
```

Log raw reactions, not your interpretation. You need 5 entries before moving to any polish work.

## Verify

After completing Step 7, run this check:

```bash
grep -c "^User #" V1-CONTRACT.md
```

The number must be ≥ 5. If it is less than 5, the v1 is not done — you are still in the user-collection phase. Do not touch CSS, spacing, or color until this check passes.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "I need to fix just this one layout issue before posting" | Design anxiety hijacking the ugly budget | Re-read V1-CONTRACT.md. The budget is 0 design hours. Post the link now, log the layout complaint as User #N feedback if anyone mentions it. |
| No responses after 48 hours | Wrong community or wrong framing | Try a different community. Rewrite your one-sentence intro to name the pain point more specifically. Do not redesign the product. |
| Hosting deploy fails | Missing environment variable or build command misconfigured | Check the platform's build logs. For Railway: set env vars in the dashboard under Variables. For Render: set them under Environment. These are config issues, not design issues — fix and redeploy. |
| Classless CSS breaks an existing component | Framework-generated class names conflicting with reset | Switch from sakura.css to water.css (different default specificity). If still broken, remove the reset and add only `body { font-family: system-ui; max-width: 48rem; margin: 0 auto; padding: 1rem; }` directly. |
| Users ask for a feature you cut | Scope was correct | Log the request in V1-CONTRACT.md as a future signal. Do not build it now. Five identical requests = validated need for v2. |

## Next

- `mvp-scope-cutting` — if your core loop still feels too big, apply the must-have/cut algorithm to get to ≤5 items before returning here.
- After 5+ user reactions: decide whether to polish or pivot based on the log — polish only if ≥3 users completed the core loop without confusion.
- For the next iteration: move custom domain, error tracking, and analytics into a v1.1 scope (not before).

## References

- [knowledge/free/dev/code-quality/tech-debt-basics](../../../knowledge/free/dev/code-quality/tech-debt-basics) — the deliberate-prudent quadrant from Fowler's framework is the exact classification for an ugly v1: you knowingly skip design quality to gain shipping speed, log it in V1-CONTRACT.md, and schedule the payoff after user validation rather than before.
