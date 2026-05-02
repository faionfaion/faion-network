---
name: github-account-and-first-repo
description: Create a GitHub account, initialise a local project with Git, and push your first repository with a README and initial commit.
tier: free
group: tech-setup
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a GitHub account with 2FA enabled, a local Git repository initialised, a README committed, and the repository pushed to GitHub so that it is visible at `https://github.com/<your-username>/<your-repo>`.

## Prerequisites

- A computer running macOS, Linux, or Windows (WSL recommended on Windows).
- Git installed locally — verify with `git --version` (must return 2.x or later). Install from https://git-scm.com/ if missing.
- A valid email address for the GitHub account.
- No prior GitHub account required (if you already have one, skip Steps 1–3).

## Steps

1. Open https://github.com/signup in your browser, enter your email address, create a password, and choose a username (e.g. `alice-dev`). Complete the email verification that GitHub sends.

2. Enable two-factor authentication: go to https://github.com/settings/security, scroll to "Two-factor authentication", click "Enable", and follow the prompts using an authenticator app (e.g. Google Authenticator or 1Password). Save your recovery codes in a secure location.

3. Add an SSH key so Git can push without a password on every push:
   ```bash
   ssh-keygen -t ed25519 -C "your@email.com" -f ~/.ssh/id_ed25519
   cat ~/.ssh/id_ed25519.pub
   ```
   Copy the output, go to https://github.com/settings/ssh/new, paste it in "Key", give it a title like `laptop-2026`, and click "Add SSH key".

4. Configure Git with your name and email — these appear in every commit:
   ```bash
   git config --global user.name "Alice Dev"
   git config --global user.email "your@email.com"
   git config --global init.defaultBranch main
   ```

5. Create a new repository on GitHub: go to https://github.com/new, set the repository name (e.g. `my-first-project`), choose "Public" or "Private", leave "Initialize this repository" unchecked (you will push from the local machine), and click "Create repository".

6. On your local machine, create the project folder and initialise Git:
   ```bash
   mkdir my-first-project && cd my-first-project
   git init
   ```

7. Create a README file and make the first commit:
   ```bash
   echo "# my-first-project" > README.md
   echo "" >> README.md
   echo "My first GitHub repository." >> README.md
   git add README.md
   git commit -m "docs: add README"
   ```

8. Connect the local repo to GitHub and push:
   ```bash
   git remote add origin git@github.com:alice-dev/my-first-project.git
   git push -u origin main
   ```
   Replace `alice-dev` with your GitHub username and `my-first-project` with your repo name.

9. Confirm the push succeeded: open `https://github.com/alice-dev/my-first-project` in your browser — your README should be visible on the repository home page.

## Verify

Open your browser and navigate to `https://github.com/<your-username>/my-first-project`. The page must show:
- The repository name in the header.
- The `README.md` rendered below the file list with the heading "my-first-project".
- A green "1 commit" badge (or the commit count if you pushed more).

Alternatively run:
```bash
git remote -v
```
Output must show `origin  git@github.com:<your-username>/my-first-project.git (fetch)` and the same for `(push)`.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `git push` fails with `Permission denied (publickey)` | SSH key not added to GitHub or wrong key in use | Run `ssh -T git@github.com` — if it says "permission denied", re-check https://github.com/settings/ssh and confirm the public key matches `cat ~/.ssh/id_ed25519.pub` |
| `error: remote origin already exists` when running `git remote add` | A remote named `origin` was already configured | Run `git remote set-url origin git@github.com:<your-username>/my-first-project.git` instead of `add` |
| `push` succeeds but README does not render on GitHub | README filename wrong (e.g. `readme.md` on a case-sensitive system) | Rename to `README.md` with `git mv readme.md README.md`, commit, and push again |
| `git push` says `src refspec main does not match any` | The initial commit was never made, so the `main` branch does not exist | Run `git add README.md && git commit -m "docs: add README"` first, then push |
| GitHub signup step blocked by CAPTCHA loop | Browser or VPN issue | Try a different browser without extensions, or disable the VPN temporarily for signup |

## Next

- [github-repo-bootstrap](../../../knowledge/free/dev/devtools-developer/github-repo-bootstrap) — apply production-grade defaults to your new repo: branch protection, CI workflow stub, Dependabot, CODEOWNERS, and squash-only merges.
- Add a `.gitignore` for your language (https://gitignore.io) to keep generated files out of version control.
- Learn the three-command daily workflow: `git add`, `git commit`, `git push` — and practise with a second commit that edits the README.

## References

- [knowledge/free/dev/devtools-developer/github-repo-bootstrap](../../../knowledge/free/dev/devtools-developer/github-repo-bootstrap) — the SSH key setup in Step 3, the `git remote add` + `git push -u origin main` sequence in Steps 8, and the branch naming convention (`main`) in Step 4 all align directly with this methodology's bootstrap recipe, making the two documents a natural first-use pair.
