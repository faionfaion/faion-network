# Dotfiles Management

## Overview

Git-based dotfiles management using GNU stow for symlink management. Covers repository structure, per-category organization (shell, git, tmux, vim, ssh), machine-specific overrides, bootstrap scripts for new machines, privacy considerations (what NOT to commit), and sync strategies. Designed for developers who work across multiple machines and want reproducible configurations.

**Target:** Solo developer maintaining configs across VPS (Hetzner), workstation, and potentially other machines.

## When to Use

| Scenario | Fit |
|----------|-----|
| Setting up a new server and want your configs | Essential |
| Version-controlling your shell/editor/tool configs | Essential |
| Sharing configs between workstation and VPS | Recommended |
| Recovering configs after server rebuild | Recommended |
| Standardizing configs across team members | Good |

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Dotfiles** | Configuration files starting with `.` (e.g., .bashrc, .gitconfig) |
| **GNU stow** | Symlink farm manager, creates symlinks from repo to $HOME |
| **Package** | Stow term for a category folder (e.g., `bash/`, `git/`, `tmux/`) |
| **Target** | Directory where symlinks are created (default: parent of stow dir) |
| **Stow directory** | The dotfiles repo root |
| **Machine-specific** | Configs that differ between machines (server vs workstation) |

## Repository Structure

### Recommended Layout

```
~/dotfiles/
├── bash/
│   └── .bashrc
│   └── .bash_aliases
│   └── .bash_profile
├── git/
│   └── .gitconfig
│   └── .gitignore_global
├── tmux/
│   └── .tmux.conf
├── vim/
│   └── .vimrc
│   └── .vim/
│       └── colors/
├── ssh/
│   └── .ssh/
│       └── config              # SSH config (NOT keys!)
├── claude/
│   └── .claude/
│       └── settings.json
├── mise/
│   └── .config/
│       └── mise/
│           └── config.toml     # Global mise config
├── scripts/
│   └── .local/
│       └── bin/
│           ├── backup.sh
│           └── server-status.sh
├── machine-server/             # Server-specific overrides
│   └── .bashrc.d/
│       └── server.sh
├── machine-workstation/        # Workstation-specific overrides
│   └── .bashrc.d/
│       └── workstation.sh
├── bootstrap.sh                # First-time setup script
├── install.sh                  # Stow all packages
├── .gitignore
└── README.md
```

### How Stow Creates Symlinks

```
Stow directory: ~/dotfiles/
Package: bash/

~/dotfiles/bash/.bashrc  →  creates  →  ~/.bashrc (symlink)
~/dotfiles/tmux/.tmux.conf  →  creates  →  ~/.tmux.conf (symlink)
~/dotfiles/vim/.vimrc  →  creates  →  ~/.vimrc (symlink)
```

The folder structure inside each package mirrors the target ($HOME) structure.

## GNU stow

### Installation

```bash
sudo apt install -y stow
```

### Basic Commands

```bash
# Stow (create symlinks) a package
cd ~/dotfiles
stow bash         # Creates ~/.bashrc → ~/dotfiles/bash/.bashrc

# Stow multiple packages
stow bash git tmux vim

# Unstow (remove symlinks) a package
stow -D bash

# Restow (remove then recreate) - useful after editing
stow -R bash

# Dry run (see what would happen)
stow -n -v bash

# Stow with explicit target
stow -t /home/nero bash

# Stow all packages
stow */
```

### Conflict Resolution

If a real file exists where stow wants to create a symlink:

```bash
# Backup existing file
mv ~/.bashrc ~/.bashrc.backup

# Then stow
stow bash

# Or adopt existing file into stow (moves file into package)
stow --adopt bash
# WARNING: This modifies your dotfiles repo!
# Review changes: git diff
```

## Configuration Categories

### bash/

```
bash/
├── .bashrc              # Main shell config
├── .bash_profile        # Login shell config
├── .bash_aliases        # Aliases
└── .bashrc.d/           # Modular configs (sourced by .bashrc)
    ├── prompt.sh        # PS1 prompt
    ├── history.sh       # History settings
    └── path.sh          # PATH additions
```

Modular .bashrc approach:

```bash
# .bashrc - source all files in .bashrc.d/
for f in ~/.bashrc.d/*.sh; do
    [ -r "$f" ] && source "$f"
done
```

### git/

```
git/
├── .gitconfig
└── .gitignore_global
```

```ini
# .gitconfig
[user]
    name = Ruslan Faion
    email = ruslan@faion.net
[core]
    excludesfile = ~/.gitignore_global
    editor = vim
    autocrlf = input
[init]
    defaultBranch = main
[pull]
    rebase = true
[push]
    default = current
    autoSetupRemote = true
[alias]
    st = status
    co = checkout
    br = branch
    lg = log --oneline --graph --decorate -20
    last = log -1 HEAD
```

### tmux/

```
tmux/
└── .tmux.conf
```

```bash
# .tmux.conf
set -g default-terminal "screen-256color"
set -g history-limit 50000
set -g mouse on
set -g status-interval 5

# Prefix: Ctrl+a (instead of Ctrl+b)
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# Split panes with | and -
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"

# Status bar
set -g status-left '[#S] '
set -g status-right '%Y-%m-%d %H:%M'
set -g status-style 'bg=colour235 fg=colour136'
```

### ssh/

```
ssh/
└── .ssh/
    └── config
```

```
# .ssh/config
Host nero-hetzner
    HostName xxx.xxx.xxx.xxx
    User nero
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes

Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    AddKeysToAgent yes
```

## Privacy: What NOT to Commit

### .gitignore for Dotfiles Repo

```gitignore
# SSH keys (NEVER commit)
.ssh/id_*
.ssh/known_hosts
.ssh/authorized_keys

# Shell history
.bash_history
.zsh_history

# Secrets and tokens
.env
.env.*
*.secret
*.key
*.pem

# 1Password
.op/

# Claude Code (may contain project secrets)
.claude/projects/

# GPG
.gnupg/

# Local machine state
.local/share/
.cache/

# Editor state
.vim/undo/
.vim/swap/
.viminfo
```

### Security Checklist

| Category | Safe to Commit | Never Commit |
|----------|---------------|--------------|
| SSH | config file | Private keys, known_hosts |
| Git | .gitconfig | Credentials, tokens |
| Shell | .bashrc, aliases | .bash_history, .env |
| Claude | settings.json | Project configs with secrets |
| GPG | (nothing) | Private keys, trust DB |

## Machine-Specific Overrides

### Strategy: .bashrc.d/ with Machine-Specific Files

```bash
# In bootstrap.sh or manually:
MACHINE_TYPE="server"  # or "workstation"

cd ~/dotfiles
stow "machine-$MACHINE_TYPE"
# Creates: ~/.bashrc.d/server.sh or ~/.bashrc.d/workstation.sh
```

### Server-Specific Config

```bash
# machine-server/.bashrc.d/server.sh
export EDITOR=vim
export VISUAL=vim

# Server-specific aliases
alias services='systemctl --user list-units --type=service'
alias logs='journalctl --user -f'
alias deploy='bash ~/workspace/deploy/deploy.sh'

# No GUI-related settings
```

### Workstation-Specific Config

```bash
# machine-workstation/.bashrc.d/workstation.sh
export EDITOR=code
export VISUAL=code

# GUI-related
alias open='xdg-open'

# SSH agent
eval "$(ssh-agent -s)" 2>/dev/null
```

## Bootstrap Script

```bash
#!/bin/bash
# bootstrap.sh - First-time dotfiles setup on new machine
set -euo pipefail

DOTFILES_DIR="$HOME/dotfiles"
REPO_URL="git@github.com:faionfaion/dotfiles.git"

# Clone if not exists
if [ ! -d "$DOTFILES_DIR" ]; then
    git clone "$REPO_URL" "$DOTFILES_DIR"
fi

cd "$DOTFILES_DIR"

# Install stow
sudo apt install -y stow

# Backup existing dotfiles
for f in .bashrc .bash_profile .gitconfig .tmux.conf .vimrc; do
    if [ -f "$HOME/$f" ] && [ ! -L "$HOME/$f" ]; then
        mv "$HOME/$f" "$HOME/$f.backup.$(date +%Y%m%d)"
    fi
done

# Stow base packages
stow bash git tmux vim ssh scripts

# Detect machine type and stow overrides
if [ -f /etc/hetzner ]; then
    MACHINE_TYPE="server"
elif command -v code >/dev/null 2>&1; then
    MACHINE_TYPE="workstation"
else
    MACHINE_TYPE="server"
fi

if [ -d "machine-$MACHINE_TYPE" ]; then
    stow "machine-$MACHINE_TYPE"
fi

echo "Dotfiles installed (machine type: $MACHINE_TYPE)"
echo "Restart your shell or run: source ~/.bashrc"
```

## Sync Workflow

```bash
# After editing a config on the server
cd ~/dotfiles
git add -A
git commit -m "chore: update tmux config"
git push

# On workstation
cd ~/dotfiles
git pull
stow -R tmux    # Restow to pick up changes
```

## Related Methodologies

| Methodology | Relationship |
|-------------|-------------|
| [server-init-bootstrap](../server-init-bootstrap/) | Deploy dotfiles during bootstrap |
| [secrets-management](../secrets-management/) | What NOT to put in dotfiles |
| [direnv-mise-versions](../direnv-mise-versions/) | Shell hooks in dotfiles |
| [claude-code-hooks](../claude-code-hooks/) | Claude config in dotfiles |
