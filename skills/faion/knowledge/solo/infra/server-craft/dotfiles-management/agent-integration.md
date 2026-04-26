# Agent Integration — Dotfiles Management

## When to use
- Setting up a new server and need to deploy the developer's standard config (tmux, git, bash, vim, ssh)
- Rebuilding a server after data loss — dotfiles bootstrap restores the developer environment quickly
- Standardizing configuration across multiple machines (workstation + VPS + staging)
- Version-controlling shell/editor configs for reproducibility and change tracking
- Onboarding a new machine type that needs machine-specific overrides

## When NOT to use
- Configs that contain secrets (SSH private keys, `.env` files, `.bash_history`) — these must never enter dotfiles
- Environments managed by configuration management (Ansible, Puppet) where dotfiles deployment conflicts with CM
- Shared servers where one developer's dotfiles pollute the environment for others
- Disposable containers where the filesystem is ephemeral (build Docker container)

## Where it fails / limitations
- `stow --adopt` modifies the dotfiles repo silently — running it without a subsequent `git diff` can accidentally commit the server's existing config
- Stow conflicts with existing real files (not symlinks) require manual backup before stow can proceed
- Machine-specific configs in `machine-server/` and `machine-workstation/` diverge over time if not maintained in sync
- SSH config in dotfiles is useful, but SSH keys must never be in the repo; a bootstrap script that installs keys separately is required
- `git push` from server in an automated agent workflow requires SSH agent forwarding or a deploy key — agent must handle this
- Circular symlink creation: stow package structure must mirror `$HOME` exactly or stow creates symlinks in wrong locations

## Agentic workflow
An agent can drive the full dotfiles bootstrap: clone the dotfiles repo, run `stow` for each package category, detect machine type, apply machine-specific overrides, and source the new shell config. The key human-in-loop checkpoint is reviewing what `stow -n -v <package>` would do before actually stowing — especially on non-fresh servers where real config files may exist and need backup.

### Recommended subagents
- `faion-sdd-executor-agent` — execute dotfiles bootstrap as part of a server-init SDD task
- `nero-sdd-executor-agent` — deploy dotfiles as part of NERO platform provisioning

### Prompt pattern
```
Deploy dotfiles to this server:
1. Check if ~/dotfiles exists; if not: git clone git@github.com:faionfaion/dotfiles.git ~/dotfiles
2. Run dry-run for each package: stow -n -v bash git tmux vim ssh scripts
3. For any conflicts, backup existing files: mv ~/.bashrc ~/.bashrc.backup.$(date +%Y%m%d)
4. Stow all packages: cd ~/dotfiles && stow bash git tmux vim ssh scripts
5. Detect machine type: if hostname matches "hetzner" or "faion-net", stow machine-server
6. Source the new config: source ~/.bashrc
7. Verify: run 'type ll' (should be alias), 'git config user.email' (should be ruslan@faion.net)
```

```
Add a new dotfiles package for Claude Code configuration:
1. Create ~/dotfiles/claude/.claude/settings.json with the current content of ~/.claude/settings.json
2. Run: stow -n -v claude (dry run first)
3. If the real ~/.claude/settings.json exists, backup and remove it
4. Run: stow claude
5. Verify: ls -la ~/.claude/settings.json (should show → ~/dotfiles/claude/.claude/settings.json)
6. Commit: cd ~/dotfiles && git add claude/ && git commit -m "chore: add claude package"
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `stow` | Symlink farm manager — creates `$HOME` symlinks from repo | `apt install stow` |
| `git` | Version control for dotfiles repo | `apt install git` |
| `ssh-keyscan` | Add host keys without interactive prompt during bootstrap | Built-in OpenSSH |
| `ln -sf` | Manual symlink creation if stow is unavailable | Built-in |
| `chezmoi` | Alternative to stow; template-aware, handles secrets | [chezmoi.io](https://www.chezmoi.io/) |
| `yadm` | Git wrapper for dotfiles (no stow needed) | [yadm.io](https://yadm.io/) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub (private repo) | SaaS | Yes | Standard dotfiles hosting; deploy key for server access |
| GitLab (self-hosted) | OSS | Yes | Alternative if self-hosting; same deploy key pattern |
| chezmoi | OSS | Yes | Template rendering, encryption support, 1Password integration |
| yadm | OSS | Yes | Git-native, no stow dependency; simpler for smaller configs |
| Mackup | OSS | Partial | macOS-focused; less useful for Ubuntu VPS |
| dotbot | OSS | Yes | Python-based, YAML config; more explicit than stow |

## Templates & scripts
See `templates.md` for the full bootstrap.sh template.

Inline: idempotent stow installer (≤35 lines):
```bash
#!/bin/bash
# install-dotfiles.sh — safe to re-run on any machine
set -euo pipefail

DOTFILES="$HOME/dotfiles"
REPO="git@github.com:faionfaion/dotfiles.git"

# 1. Clone or update
if [ -d "$DOTFILES/.git" ]; then
    git -C "$DOTFILES" pull --ff-only
else
    git clone "$REPO" "$DOTFILES"
fi

cd "$DOTFILES"

# 2. Backup conflicts
for pkg in bash git tmux vim ssh scripts; do
    stow -n "$pkg" 2>&1 | grep "existing target" | awk '{print $NF}' | while read target; do
        [ -f "$HOME/$target" ] && ! [ -L "$HOME/$target" ] && \
          mv "$HOME/$target" "$HOME/$target.bak.$(date +%Y%m%d)"
    done
done

# 3. Stow all base packages
stow bash git tmux vim ssh scripts

# 4. Machine-specific
HOSTNAME=$(hostname -s)
if [[ "$HOSTNAME" == *"hetzner"* ]] || [[ "$HOSTNAME" == *"faion"* ]] || [[ "$HOSTNAME" == *"nero"* ]]; then
    stow machine-server 2>/dev/null || true
fi

echo "Dotfiles installed. Run: source ~/.bashrc"
```

## Best practices
- Run `stow -n -v <package>` (dry run) before actually stowing, especially on non-fresh servers
- Keep the dotfiles repo private if it contains SSH config or any identifying information
- Use `machine-server/` and `machine-workstation/` stow packages for environment-specific config, not branching
- Never store secrets in dotfiles; store the `.ssh/config` (host aliases), never the private keys
- `.gitignore` in the dotfiles repo must exclude `.bash_history`, `.ssh/id_*`, `.env`, `.op/`
- Add a `README.md` in the dotfiles repo documenting which packages exist and what each stows
- After editing a config on the server, commit and push so the workstation can pull — treat dotfiles repo like any code

## AI-agent gotchas
- `stow --adopt` is dangerous in agent context — it moves the server's existing file into the repo and stages it for commit; agent may then commit server-specific config back to the shared repo
- Agent must not run `stow` without checking for conflicts first (`stow -n`); stow aborts on conflict but may have partially created some symlinks before the abort
- Git clone via SSH requires either SSH agent forwarding or a deploy key; agent running in a non-interactive SSH session often doesn't have SSH agent available — use HTTPS with a token or a deploy key
- Sourcing `.bashrc` in a non-interactive bash session (`bash -c "source ~/.bashrc"`) may cause issues if `.bashrc` has an early exit guard for non-interactive shells
- Agent must handle the case where dotfiles repo already exists on the server (pull vs clone) — `git clone` onto existing directory fails

## References
- [GNU stow documentation](https://www.gnu.org/software/stow/manual/)
- [chezmoi — dotfiles manager with secret support](https://www.chezmoi.io/)
- [yadm — yet another dotfiles manager](https://yadm.io/)
- [dotfiles.github.io — community resource](https://dotfiles.github.io/)
- [Atlassian: dotfiles tutorial](https://www.atlassian.com/git/tutorials/dotfiles)
