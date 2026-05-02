---
name: deploy-static-site-github-pages
description: Push an index.html to a public GitHub repo and publish it live at https://<user>.github.io/<repo>/ in under 5 minutes — no server, no cost.
tier: free
group: hosting-infra
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a static website served publicly at `https://<your-username>.github.io/<your-repo>/` directly from a GitHub repository — free, no server required, and updating with every `git push`.

## Prerequisites

- A GitHub account (free signup at https://github.com/join).
- Git installed locally (`git --version` should return a version number; download at https://git-scm.com/downloads if not present).
- An `index.html` file on your local machine (even a single-line `<h1>Hello</h1>` is enough to start).
- The repository must be **public** — GitHub Pages is only available on public repos on the free plan.

## Steps

1. Sign in at https://github.com and click the "+" icon in the top-right corner, then "New repository".

2. Fill in the repository name (for example `my-site`), set visibility to **Public**, leave "Initialize this repository with a README" unchecked, and click "Create repository".

3. Open your terminal. Navigate to the folder containing your `index.html`:

   ```bash
   cd ~/projects/my-site
   ```

4. Initialize a local Git repo, add your files, and push to GitHub (replace `your-username` and `my-site` with your values):

   ```bash
   git init
   git add index.html
   git commit -m "first commit"
   git branch -M main
   git remote add origin https://github.com/your-username/my-site.git
   git push -u origin main
   ```

   If you already have a local Git repo tracking a different remote, skip `git init` and `git remote add`; just run `git push`.

5. On GitHub, open your repository page and click **Settings** (the gear icon in the top navigation row, not the global account settings).

6. In the left sidebar under "Code and automation", click **Pages**.

7. Under "Build and deployment" → "Source", select **Deploy from a branch**.

8. Under "Branch", choose `main` (or `master` if that is your default branch) and leave the folder as `/ (root)`. Click **Save**.

9. GitHub starts building the site. A blue banner appears: "GitHub Pages source saved." Wait 30–60 seconds, then refresh the Pages settings page — it will show a green banner with your live URL:

   ```
   Your site is live at https://your-username.github.io/my-site/
   ```

10. Open that URL in a browser to confirm the page loads.

## Verify

Run the following command, replacing the URL with your actual Pages URL:

```bash
curl -sI https://your-username.github.io/my-site/ | head -1
```

The response must be `HTTP/2 200`. If you see `404`, the site is not yet built or the branch/folder setting is wrong — revisit Step 7–8.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Settings → Pages shows no "Branch" dropdown | Repo is private | Go to Settings → General → scroll to "Danger Zone" → change visibility to Public, then return to Pages |
| Green banner never appears after 5+ minutes | No `index.html` at repo root or Pages source set to wrong folder | Confirm `index.html` is committed to `main` root (not a subfolder); re-check "Branch" folder setting is `/ (root)` |
| URL returns 404 after going live | GitHub Pages serves from the repo root, but `index.html` is inside a subfolder | Move `index.html` to the repo root: `git mv subdir/index.html index.html && git commit -m "move index to root" && git push` |
| Push fails: "remote: Repository not found" | Remote URL has a typo or wrong username | Run `git remote -v` to check; fix with `git remote set-url origin https://github.com/correct-username/my-site.git` |
| Page loads but shows raw HTML source instead of rendered page | File extension wrong (e.g. `index.htm` instead of `index.html`) | Rename: `git mv index.htm index.html && git commit -m "fix filename" && git push` |

## Next

- Point a custom domain at your GitHub Pages site using Cloudflare — see the `buy-domain-namecheap-cloudflare` playbook to register a domain first.
- Automate updates: every `git push origin main` triggers a new Pages build, so your site always reflects the latest commit.
- Upgrade to Vercel for server-side rendering, preview deployments, and environment variables — see the `deploy-to-vercel-free` playbook.

## References

- [knowledge/free/dev/devtools-developer/github-repo-bootstrap](../../../knowledge/free/dev/devtools-developer/github-repo-bootstrap) — the repo creation steps (visibility, branch name, remote setup) in this playbook directly follow the bootstrap sequence: public visibility gate, `main` as default branch, and `git push -u origin main` to establish tracking, all sourced from this methodology.
