---
name: github-actions-cicd
description: Add a three-job GitHub Actions workflow (lint, test, deploy) to a Node or Python project and ship it on every push to main.
tier: solo
group: automation
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a `.github/workflows/ci.yml` that runs lint and tests on every pull request and deploys your app automatically on every push to `main` — using either `actions/deploy-pages` for static sites or rsync-over-SSH for VPS targets. No manual deploys. A failing test blocks the merge.

## Prerequisites

- A GitHub repository with your project code (Node.js or Python).
- For **Node**: `package.json` with a `test` script (`npm test`) and a lint script (`npm run lint`). Node 20+ recommended.
- For **Python**: `requirements.txt` (or `pyproject.toml`) and a `pytest` test suite (`pytest tests/`). Python 3.11+ recommended.
- For **VPS deploy target**: SSH access to your server, a dedicated deploy keypair (see `vps-first-deploy`), and rsync installed on the server.
- For **GitHub Pages target**: the repo's GitHub Pages settings set to deploy from a branch or Actions (Settings → Pages → Source → GitHub Actions).
- GitHub repository secrets configured (see Step 1 below).

## Steps

### Store secrets in GitHub

1. In your repository, go to **Settings → Secrets and variables → Actions → New repository secret** and add:

   | Secret name | Value |
   |-------------|-------|
   | `DEPLOY_KEY` | Private key of your deploy keypair (the full PEM text, `-----BEGIN OPENSSH PRIVATE KEY-----` … `-----END OPENSSH PRIVATE KEY-----`) |
   | `DEPLOY_HOST` | Server hostname or IP, e.g. `46.225.58.119` |
   | `DEPLOY_USER` | SSH user on the server, e.g. `deploy` |
   | `DEPLOY_PORT` | SSH port, e.g. `22` (or `22022` if non-standard) |

   For GitHub Pages deployments you do not need `DEPLOY_KEY` — GitHub Actions uses the built-in `GITHUB_TOKEN`.

### Create the workflow file

2. Create `.github/workflows/ci.yml` in your repository root. Choose the variant for your stack.

   **Node.js project (lint → test → deploy to GitHub Pages):**

   ```yaml
   name: CI/CD

   on:
     push:
       branches: [main]
     pull_request:
       branches: [main]

   jobs:
     lint:
       runs-on: ubuntu-24.04
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-node@v4
           with:
             node-version: 20
             cache: npm
         - run: npm ci
         - run: npm run lint

     test:
       needs: lint
       runs-on: ubuntu-24.04
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-node@v4
           with:
             node-version: 20
             cache: npm
         - run: npm ci
         - run: npm test

     deploy:
       needs: test
       runs-on: ubuntu-24.04
       if: github.ref == 'refs/heads/main' && github.event_name == 'push'
       permissions:
         pages: write
         id-token: write
       environment:
         name: github-pages
         url: ${{ steps.deployment.outputs.page_url }}
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-node@v4
           with:
             node-version: 20
             cache: npm
         - run: npm ci
         - run: npm run build
         - uses: actions/upload-pages-artifact@v3
           with:
             path: dist
         - id: deployment
           uses: actions/deploy-pages@v4
   ```

   **Python project (lint → test → deploy to VPS via rsync):**

   ```yaml
   name: CI/CD

   on:
     push:
       branches: [main]
     pull_request:
       branches: [main]

   jobs:
     lint:
       runs-on: ubuntu-24.04
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: "3.11"
         - run: pip install ruff
         - run: ruff check .
         - run: ruff format --check .

     test:
       needs: lint
       runs-on: ubuntu-24.04
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: "3.11"
         - run: pip install -r requirements.txt
         - run: pytest tests/ -v

     deploy:
       needs: test
       runs-on: ubuntu-24.04
       if: github.ref == 'refs/heads/main' && github.event_name == 'push'
       steps:
         - uses: actions/checkout@v4
         - name: Write deploy SSH key
           run: |
             mkdir -p ~/.ssh
             echo "${{ secrets.DEPLOY_KEY }}" > ~/.ssh/deploy_key
             chmod 600 ~/.ssh/deploy_key
             ssh-keyscan -p ${{ secrets.DEPLOY_PORT }} ${{ secrets.DEPLOY_HOST }} >> ~/.ssh/known_hosts
         - name: Rsync files to server
           run: |
             rsync -avz --delete \
               --exclude .git \
               --exclude __pycache__ \
               --exclude .venv \
               -e "ssh -i ~/.ssh/deploy_key -p ${{ secrets.DEPLOY_PORT }}" \
               ./ ${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }}:/home/${{ secrets.DEPLOY_USER }}/myapp/
         - name: Restart service
           run: |
             ssh -i ~/.ssh/deploy_key \
               -p ${{ secrets.DEPLOY_PORT }} \
               ${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }} \
               "sudo systemctl restart myapp"
   ```

### Commit and push the workflow

3. Stage and commit the new workflow file:

   ```bash
   git add .github/workflows/ci.yml
   git commit -m "ci: add lint/test/deploy pipeline"
   git push origin main
   ```

4. Open the **Actions** tab in your GitHub repository. You should see a new workflow run triggered automatically. Wait for all three jobs to show green checkmarks.

### Verify the deploy key is authorized on the server (VPS target only)

5. On your server, append the **public** half of your deploy keypair to the `deploy` user's authorized keys:

   ```bash
   echo "ssh-ed25519 AAAA... deploy@github-actions" >> /home/deploy/.ssh/authorized_keys
   chmod 600 /home/deploy/.ssh/authorized_keys
   ```

   The private half (`DEPLOY_KEY` secret) stays in GitHub — never on the server.

### Protect main with a branch rule (optional but recommended)

6. In **Settings → Branches → Add rule**, set **Branch name pattern** to `main`, enable **Require status checks to pass before merging**, and select `lint` and `test` as required checks. This blocks direct pushes that skip CI.

## Verify

After a successful push to `main`, check that the deploy job ran and the correct revision is live:

**GitHub Pages:**
```bash
curl -sI https://<your-github-username>.github.io/<repo-name>/ | head -3
```
Expect `HTTP/2 200`. Also confirm the Actions tab shows the `deploy-pages` step completed without error.

**VPS rsync:**
```bash
ssh -i ~/.ssh/deploy_key -p 22 deploy@46.225.58.119 \
  "git -C /home/deploy/myapp log --oneline -1 2>/dev/null || ls -lt /home/deploy/myapp | head -5"
```
The output should reflect the commit you just pushed. Also run `sudo systemctl status myapp` on the server to confirm the service is `active (running)`.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `lint` job fails with `ESLint couldn't find a configuration file` | No `.eslintrc` or `eslint.config.js` in repo | Add a minimal ESLint config or remove the lint step until one exists; see `code-style-and-prettier` playbook |
| `test` job fails with `Cannot find module` | `npm ci` uses `package-lock.json` — lock file is missing or stale | Run `npm install` locally, commit `package-lock.json`, push again |
| `deploy` job shows `Permission denied (publickey)` | `DEPLOY_KEY` secret value has trailing whitespace or is missing the final newline | Re-copy the private key to the secret, including the last newline; verify with `wc -c ~/.ssh/deploy_key` locally |
| `rsync` exits 23 (partial transfer) | Target directory `/home/deploy/myapp/` does not exist on server | `ssh deploy@<host> "mkdir -p /home/deploy/myapp"` once, then re-run the workflow |
| `deploy-pages` fails with `Resource not accessible by integration` | GitHub Pages not enabled or `permissions` block missing from workflow | Enable Pages in repo Settings → Pages → Source → GitHub Actions; confirm the `permissions: pages: write` block is present in the `deploy` job |
| Jobs run on PRs but deploy triggers on PRs too | Missing `if: github.event_name == 'push'` guard | Add the `if:` condition to the `deploy` job (see Step 2 — it is already included in the templates above) |
| `pytest` fails with `ModuleNotFoundError` | App dependencies not installed before running tests | Confirm `pip install -r requirements.txt` runs before `pytest` in the `test` job |

## Next

- Add caching for Python dependencies to speed up the `test` job: replace `pip install -r requirements.txt` with the `actions/cache` action keyed on the hash of `requirements.txt`.
- Wire up `env-management-secrets` to inject per-environment `.env` values into the deploy job without committing secrets to the repo.
- Upgrade to matrix testing: add a `strategy.matrix.python-version: ["3.11", "3.12"]` block to the `test` job to gate on multiple runtimes.

## References

- [knowledge/solo/dev/automation-tooling/cd-basics](../../../knowledge/solo/dev/automation-tooling/cd-basics) — the three-job pipeline shape (lint → test → deploy) and the `needs:` dependency chain used in this playbook follow the CD basics job-sequencing pattern directly.
- [knowledge/solo/dev/automation-tooling/cd-pipelines](../../../knowledge/solo/dev/automation-tooling/cd-pipelines) — the `if: github.ref == 'refs/heads/main'` guard and the secrets-injection pattern (`${{ secrets.DEPLOY_KEY }}`) are drawn from the CD pipeline secrets-and-gates section of this methodology.
- [knowledge/solo/dev/automation-tooling/trunk-based-ci-gates](../../../knowledge/solo/dev/automation-tooling/trunk-based-ci-gates) — the branch protection rule in Step 6 (requiring `lint` and `test` checks to pass before merge) implements the CI gate pattern this methodology prescribes for trunk-based development.
