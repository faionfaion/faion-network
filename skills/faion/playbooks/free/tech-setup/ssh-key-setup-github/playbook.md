---
name: ssh-key-setup-github
description: Generate an ed25519 SSH key, add it to ssh-agent, and connect it to your GitHub account so you can push code without a password.
tier: free
group: tech-setup
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have an ed25519 SSH key pair on your machine, the private key loaded into ssh-agent, and the public key registered in your GitHub account — so that `git clone`, `git push`, and `git pull` over SSH work without entering a password.

## Prerequisites

- A GitHub account (free signup at https://github.com).
- A Unix-like terminal: macOS Terminal, Linux terminal, or Git Bash on Windows.
- `git` installed (`git --version` prints a version number).
- `ssh-keygen` and `ssh-agent` available (bundled with OpenSSH, present by default on macOS and most Linux distros; included in Git for Windows).

## Steps

1. Open a terminal and generate a new ed25519 key, replacing `<your-github-email>` with the email address on your GitHub account:

   ```bash
   ssh-keygen -t ed25519 -C "<your-github-email>"
   ```

   When prompted `Enter file in which to save the key`, press Enter to accept the default (`~/.ssh/id_ed25519`).
   When prompted for a passphrase, enter a strong passphrase (recommended) or press Enter twice to skip.

2. Start the SSH agent in the background:

   ```bash
   eval "$(ssh-agent -s)"
   ```

   The output will be `Agent pid <number>`. If you see a pid, the agent is running.

3. Add your private key to the agent:

   ```bash
   ssh-add ~/.ssh/id_ed25519
   ```

   If you set a passphrase in step 1, enter it now. The agent will hold the decrypted key for the current session.

4. Copy your public key to the clipboard.

   On **macOS**:
   ```bash
   pbcopy < ~/.ssh/id_ed25519.pub
   ```

   On **Linux** (requires `xclip`):
   ```bash
   xclip -selection clipboard < ~/.ssh/id_ed25519.pub
   ```

   On **Windows (Git Bash)**:
   ```bash
   clip < ~/.ssh/id_ed25519.pub
   ```

   Alternatively, print the key and copy it manually:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

5. Sign in at https://github.com and navigate to **Settings** → **SSH and GPG keys** → **New SSH key**.

6. Set the **Title** to something identifying your machine (e.g., `MacBook Pro 2024` or `Ubuntu dev workstation`). Leave **Key type** as `Authentication Key`. Paste the public key into the **Key** field and click **Add SSH key**.

7. Test the connection:

   ```bash
   ssh -T git@github.com
   ```

   GitHub responds with:
   ```
   Hi your-username! You've successfully authenticated, but GitHub does not provide shell access.
   ```

## Verify

Run the authentication test and confirm GitHub greets you by your username:

```bash
ssh -T git@github.com
```

Expected output (exit code 1 is normal here — GitHub denies shell access intentionally):

```
Hi your-username! You've successfully authenticated, but GitHub does not provide shell access.
```

If you see your correct username in the response, the key is wired up correctly and you can push to any repo you have access to.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Permission denied (publickey)` | Public key not added to GitHub, or wrong key in agent | Run `ssh-add -L` to list loaded keys; confirm the fingerprint matches `ssh-keygen -lf ~/.ssh/id_ed25519.pub`; if the key is missing, re-run `ssh-add ~/.ssh/id_ed25519` |
| `ssh -T` prompts for passphrase every terminal session | Agent is not persisting across sessions | Add `ssh-add ~/.ssh/id_ed25519` to your shell profile (`~/.zshrc` or `~/.bashrc`), or use `~/.ssh/config` with `AddKeysToAgent yes` |
| `Could not open a connection to your authentication agent` | `ssh-agent` not running | Run `eval "$(ssh-agent -s)"` in the same terminal before `ssh-add` |
| Key fingerprint on GitHub does not match local key | Multiple keys generated; wrong one uploaded | Run `ssh-keygen -lf ~/.ssh/id_ed25519.pub` and compare the fingerprint with what GitHub shows under **Settings → SSH and GPG keys** |
| `git push` still prompts for a GitHub password | Remote URL uses HTTPS instead of SSH | Switch with `git remote set-url origin git@github.com:your-username/your-repo.git` |

## Next

- [ssh-key-setup-github → github-account-and-first-repo](../github-account-and-first-repo/playbook.md) — create your first GitHub repository and push an initial commit using the SSH key you just configured.
- Configure `~/.ssh/config` to manage multiple GitHub accounts (personal + work) by assigning different keys per `Host` alias.
- Enable SSH key forwarding to use your local key on remote servers without copying the private key there.

## References

- [knowledge/free/dev/devtools-developer/github-repo-bootstrap](../../../knowledge/free/dev/devtools-developer/github-repo-bootstrap) — the `gh auth` and SSH-URL patterns in this methodology back step 7's `git remote set-url` troubleshooting fix and the SSH-over-HTTPS alternative for networks that block port 22.
