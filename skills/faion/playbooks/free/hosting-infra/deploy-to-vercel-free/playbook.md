---
name: deploy-to-vercel-free
description: Connect a Next.js, Vite, or static GitHub repo to Vercel and get a live https://<name>.vercel.app URL in under 5 minutes — free, no credit card.
tier: free
group: hosting-infra
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a Next.js, Vite, or static HTML project deployed live at `https://<project-name>.vercel.app`, auto-redeploying on every push to your `main` branch, with environment variables configured for an API key.

## Prerequisites

- A GitHub account with the project repository already pushed to it (public or private both work).
- The project must be one of: Next.js, Vite, Create React App, Astro, Hugo, Gatsby, Nuxt, or a plain static folder — Vercel auto-detects all of them.
- An API key you need at runtime (for example `NEXT_PUBLIC_STRIPE_KEY` or `VITE_API_KEY`), stored only in your password manager as `<your-secret>`.
- No payment method required for the Hobby (free) plan.

## Steps

1. Open https://vercel.com and click **Sign Up** in the top-right corner.

2. On the "Create Your Vercel Account" screen, click **Continue with GitHub**. Authorize Vercel to access your GitHub account when prompted.

3. Vercel opens the onboarding dashboard. Click **Add New Project** (or the "+" button in the top navigation row if you already have projects).

4. Under "Import Git Repository", find your repository in the list. If it does not appear, click **Adjust GitHub App Permissions** → select the repo → save, then return to this page.

5. Click **Import** next to your repository name.

6. Vercel shows the "Configure Project" screen. Review the auto-detected settings:
   - **Framework Preset** — Vercel sets this automatically (e.g., "Next.js", "Vite", "Create React App", "Other"). Verify it matches your project; if wrong, open the dropdown and select the correct framework.
   - **Root Directory** — leave as `./` unless your app lives in a subdirectory (e.g., `apps/web`).
   - **Build Command** — pre-filled from the framework preset (e.g., `next build` or `vite build`). Override only if your `package.json` uses a custom script.
   - **Output Directory** — pre-filled (e.g., `.next` for Next.js, `dist` for Vite). Leave as-is unless you changed it.

7. Expand the **Environment Variables** section. For each secret your app needs at build time or runtime:
   - Enter the variable **Name** (e.g., `NEXT_PUBLIC_STRIPE_KEY`).
   - Paste the value from your password manager in the **Value** field (replace `<your-secret>` with the real value here — never commit it to the repo).
   - Leave **Environment** checkboxes at their defaults (Production, Preview, Development all checked).
   - Click **Add**.
   - Repeat for additional variables.

8. Click **Deploy**. Vercel queues a build. A real-time log appears showing install, build, and upload phases.

9. Wait for the build to finish (typically under 60 seconds for a small project). Vercel shows a "Congratulations!" screen with a preview image of your site and the live URL.

10. Click **Visit** or open the URL shown (format: `https://<project-name>.vercel.app`) in your browser.

11. Optional — assign a shorter subdomain: go to your project dashboard → **Settings** → **Domains** → type a name in "Add Domain" (e.g., `myapp.vercel.app` if not already taken) → click **Add**. Vercel updates the assignment immediately.

## Verify

Open your browser console (F12) or run:

```bash
curl -sI https://<project-name>.vercel.app | head -1
```

The response must be `HTTP/2 200`. In the Vercel dashboard under **Deployments**, the latest entry must show a green **Ready** badge — not "Error" or "Building".

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Build log shows `sh: next: command not found` | `next` (or `vite`, etc.) not in `dependencies`, only in `devDependencies`, and `NODE_ENV=production` prunes dev deps | Move the framework package to `dependencies` in `package.json`, commit, push — Vercel rebuilds automatically |
| Framework Preset shows "Other" for a Next.js project | `package.json` missing `"next"` in dependencies, or `next.config.js` absent | Add `next.config.js` (even an empty `module.exports = {}`) and ensure `next` is in `dependencies` |
| Environment variable is `undefined` at runtime in the browser | `VITE_` or `NEXT_PUBLIC_` prefix missing | Client-side env vars require the prefix: `VITE_` for Vite projects, `NEXT_PUBLIC_` for Next.js; rename the variable in Vercel dashboard → Settings → Environment Variables, then redeploy |
| "Import" button not visible for the repo | Vercel GitHub App has no permission for that repo | Click **Adjust GitHub App Permissions** on the Import screen → add the repo → save |
| Deployment URL returns 404 for all routes | Single-page app routing not configured | Add a `vercel.json` at repo root with `{"rewrites": [{"source": "/(.*)", "destination": "/index.html"}]}`, commit, push |
| Custom subdomain `myapp.vercel.app` already taken | Another project owns it | Choose a different name; append a short unique suffix (e.g., `myapp-2026.vercel.app`) |

## Next

- Add a custom domain (e.g., `myapp.com`) instead of `vercel.app` — see the `buy-domain-namecheap-cloudflare` playbook to register a domain first, then add it in Vercel → Settings → Domains.
- Enable preview deployments: every pull request on GitHub automatically gets its own `https://<branch>-<project>.vercel.app` URL — already active by default, no extra steps needed.
- Protect secrets further: use Vercel's **Sensitive** flag (eye icon) when adding environment variables so values are never shown again after saving.

## References

- [knowledge/free/dev/devtools-developer/github-repo-bootstrap](../../../knowledge/free/dev/devtools-developer/github-repo-bootstrap) — the prerequisite repo setup sequence (public/private visibility, default branch name, remote push) that Step 4 and Step 11 rely on: Vercel imports directly from the GitHub repo Vercel's GitHub App can see, so the repo must already be bootstrapped and pushed before this playbook begins.
