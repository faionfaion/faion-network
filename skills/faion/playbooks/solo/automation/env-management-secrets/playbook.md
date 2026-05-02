---
name: env-management-secrets
description: Graduate from a single .env file to per-environment dotenv files, encrypted secrets via sops+age, GitHub Actions secrets, and 1Password CLI for local dev.
tier: solo
group: automation
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a per-environment secrets layout (`.env.development`, `.env.staging`, `.env.production`), production secrets encrypted in-repo with `sops` + `age` (no plaintext keys ever committed), GitHub Actions wired to the same secrets via repository secrets, and 1Password CLI loading local dev keys on demand — so the only file you ever put in `.gitignore` is your `age` private key.

## Prerequisites

- Basic `.env` + `.gitignore` hygiene already in place (see `dotenv-secrets-management`).
- Git repo hosted on GitHub (public or private).
- `age` installed: https://github.com/FiloSottile/age/releases (macOS: `brew install age`; Ubuntu: `sudo apt install age`).
- `sops` v3.9+ installed: https://github.com/getsops/sops/releases (macOS: `brew install sops`; Ubuntu: download binary from releases page).
- GitHub CLI (`gh`) installed and authenticated: https://cli.github.com.
- 1Password desktop app + CLI (`op`) installed and unlocked at least once: https://developer.1password.com/docs/cli/get-started.

## Steps

### Set up the per-environment file layout

1. Create three environment files in your project root:

   ```bash
   touch .env.development .env.staging .env.production
   ```

2. Add all three to `.gitignore` (they will be replaced by encrypted versions later):

   ```
   .env
   .env.*
   !.env.example
   !.env.*.enc
   ```

3. Populate `.env.development` with real local dev values:

   ```
   DATABASE_URL=postgresql://myapp:devpassword@localhost:5432/myapp_dev
   OPENAI_API_KEY=sk-proj-devkeyhere
   STRIPE_SECRET_KEY=sk_test_yourtestkey
   APP_ENV=development
   ```

4. Create `.env.example` listing every key with placeholder values — commit this file:

   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   OPENAI_API_KEY=<openai-api-key>
   STRIPE_SECRET_KEY=<stripe-secret-key>
   APP_ENV=development
   ```

   ```bash
   git add .env.example
   git commit -m "chore: add .env.example with all required keys"
   ```

### Generate an age keypair for secret encryption

5. Generate a new age identity:

   ```bash
   age-keygen -o ~/.config/sops/age/keys.txt
   ```

   This prints your public key, e.g.: `age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p`

6. Add your private key file to `.gitignore` and keep it only on your machine:

   ```
   # age private key — NEVER commit this
   keys.txt
   ```

   Back up `~/.config/sops/age/keys.txt` to 1Password: open 1Password → create a new Secure Note item named `age-key-myapp` → paste the full file contents.

### Create a .sops.yaml configuration

7. Create `.sops.yaml` in your project root — this tells `sops` which key to use for which file:

   ```yaml
   creation_rules:
     - path_regex: \.env\.production\.enc$
       age: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p
     - path_regex: \.env\.staging\.enc$
       age: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p
   ```

   Replace the `age1...` value with your actual public key from Step 5. Commit `.sops.yaml`:

   ```bash
   git add .sops.yaml
   git commit -m "chore: add .sops.yaml with age encryption rules"
   ```

### Encrypt the production and staging env files

8. Encrypt `.env.production`:

   ```bash
   sops --encrypt .env.production > .env.production.enc
   ```

9. Encrypt `.env.staging`:

   ```bash
   sops --encrypt .env.staging > .env.staging.enc
   ```

10. Commit the encrypted files — these are safe to store in Git:

    ```bash
    git add .env.production.enc .env.staging.enc
    git commit -m "chore: add encrypted env files for production and staging"
    ```

11. Decrypt on any machine that has the age key available:

    ```bash
    sops --decrypt .env.production.enc > .env.production
    ```

    This is the command your deploy script or CI runner will use.

### Wire GitHub Actions to repository secrets

12. Add your production secrets to GitHub Actions as repository secrets. Run once per secret:

    ```bash
    gh secret set DATABASE_URL --body "postgresql://myapp:prodpassword@db.myapp.com:5432/myapp_prod"
    gh secret set OPENAI_API_KEY --body "sk-proj-prodkeyhere"
    gh secret set STRIPE_SECRET_KEY --body "sk_live_yourlivetestkey"
    ```

    Alternatively, open https://github.com/myusername/myapp/settings/secrets/actions and add them via the UI.

13. Reference secrets in your workflow file (`.github/workflows/deploy.yml`):

    ```yaml
    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - name: Run deploy
            env:
              DATABASE_URL: ${{ secrets.DATABASE_URL }}
              OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
              STRIPE_SECRET_KEY: ${{ secrets.STRIPE_SECRET_KEY }}
            run: bash deploy.sh
    ```

    Secrets are masked in logs — GitHub replaces any accidental echo of a secret value with `***`.

### Load local dev secrets from 1Password CLI

14. Store your development key in 1Password. Open 1Password → create a new item (type Login or API Credential) in your vault → add a field named `credential` with the actual value. Note the item name, e.g. `myapp-openai-dev`.

15. Reference secrets via `op` in your local shell or a `Makefile` target:

    ```bash
    # One-off: inject a single secret
    OPENAI_API_KEY=$(op item get myapp-openai-dev --fields credential) python3 main.py
    ```

16. Or write a `load-env.sh` script that injects all development secrets:

    ```bash
    #!/usr/bin/env bash
    set -euo pipefail
    export DATABASE_URL=$(op item get myapp-db-dev --fields credential)
    export OPENAI_API_KEY=$(op item get myapp-openai-dev --fields credential)
    export STRIPE_SECRET_KEY=$(op item get myapp-stripe-dev --fields credential)
    exec "$@"
    ```

    Run any command with dev secrets: `bash load-env.sh python3 main.py`. The file contains no real credentials — safe to commit.

## Verify

Run the following checks from your project root:

```bash
# 1. Confirm no plaintext env files are tracked
git ls-files | grep -E '\.env\.(development|staging|production)$' && echo "LEAK" || echo "OK"

# 2. Confirm encrypted files are tracked
git ls-files | grep -E '\.env\.(production|staging)\.enc$'

# 3. Decrypt production env and confirm a key is present
sops --decrypt .env.production.enc | grep DATABASE_URL
```

Expected: first command prints `OK`; second lists both `.enc` files; third prints `DATABASE_URL=postgresql://...`. Any deviation means a secret is either unencrypted in the repo or the encryption step was skipped.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `sops: error: could not load age identity` when decrypting | `SOPS_AGE_KEY_FILE` env var not set, or `~/.config/sops/age/keys.txt` missing on this machine | Run `export SOPS_AGE_KEY_FILE=~/.config/sops/age/keys.txt`; if the file is missing, restore from 1Password backup (Step 6) |
| `sops: error: no matching creation rule` | `.sops.yaml` regex does not match the filename | Check the `path_regex` values; the regex matches the file path relative to repo root, not just the filename |
| `git ls-files` shows `.env.production` as tracked | The file was staged before `.gitignore` was updated | Run `git rm --cached .env.production` then re-add to `.gitignore`; the encrypted `.enc` version is the one to keep |
| `gh secret set` returns 404 | Wrong repo or not authenticated | Run `gh auth status`; ensure you have admin rights on the repo with `gh repo view myusername/myapp` |
| `op item get` returns `[ERROR] 401: Unauthorized` | 1Password session expired | Run `eval $(op signin)` to re-authenticate, then retry |
| Encrypted `.enc` file committed but decryption fails after key rotation | Old ciphertext encrypted with the previous key | Re-encrypt with the new public key: `sops --rotate --in-place .env.production.enc` after updating `.sops.yaml` |

## Next

- `github-actions-cicd` — build a full CI/CD pipeline that uses the GitHub Actions secrets you wired in Step 12–13.
- `vps-first-deploy` — deploy your app to a VPS where you `sops --decrypt` the env file in the deploy script before starting the service.
- Add a pre-commit hook that blocks commits containing unencrypted env files: `grep -rE '^(DATABASE_URL|OPENAI_API_KEY|STRIPE_SECRET_KEY)=.+' .env.production` exits non-zero if any real value is present unencrypted.

## References

- [knowledge/solo/infra/server-craft/secrets-management](../../../knowledge/solo/infra/server-craft/secrets-management) — the per-environment file naming convention and the age+sops encryption flow in Steps 5–11 follow the secrets-management pattern for at-rest encryption of dotenv files committed to a repo.
- [knowledge/solo/dev/automation-tooling/cd-pipelines](../../../knowledge/solo/dev/automation-tooling/cd-pipelines) — GitHub Actions secrets injection in Steps 12–13 follows the CD pipeline methodology's pattern for passing secrets as environment variables without exposing them in the workflow file or logs.
- [knowledge/free/dev/devtools-developer/github-repo-bootstrap](../../../knowledge/free/dev/devtools-developer/github-repo-bootstrap) — the `.gitignore` rules in Steps 1–2 extend the repo bootstrap rule that all env files and key material must be excluded from tracking before the first commit.
