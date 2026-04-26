# Dotfiles Management Templates

## Dotfiles Repository Structure

```
~/dotfiles/
├── bash/
│   ├── .bashrc
│   ├── .bash_profile
│   └── .bashrc.d/
│       ├── aliases.sh
│       ├── history.sh
│       ├── path.sh
│       └── prompt.sh
├── git/
│   ├── .gitconfig
│   └── .gitignore_global
├── tmux/
│   └── .tmux.conf
├── vim/
│   └── .vimrc
├── ssh/
│   └── .ssh/
│       └── config
├── scripts/
│   └── .local/
│       └── bin/
│           ├── server-status.sh
│           └── deploy.sh
├── machine-server/
│   └── .bashrc.d/
│       └── server.sh
├── machine-workstation/
│   └── .bashrc.d/
│       └── workstation.sh
├── bootstrap.sh
├── install.sh
├── .gitignore
└── README.md
```

## .bashrc (Modular)

```bash
# ~/.bashrc - Main shell configuration
# Loaded by non-login interactive shells

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# ============================================================
# Source modular configurations from .bashrc.d/
# ============================================================
if [ -d "$HOME/.bashrc.d" ]; then
    for f in "$HOME/.bashrc.d"/*.sh; do
        [ -r "$f" ] && source "$f"
    done
    unset f
fi

# ============================================================
# Tool integrations (order matters)
# ============================================================

# mise: runtime version management
if command -v mise &>/dev/null; then
    eval "$(mise activate bash)"
fi

# direnv: per-directory environment (MUST be last)
if command -v direnv &>/dev/null; then
    eval "$(direnv hook bash)"
fi
```

## .bashrc.d/aliases.sh

```bash
# ~/.bashrc.d/aliases.sh - Shell aliases

# Navigation
alias ..='cd ..'
alias ...='cd ../..'
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Safety
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Grep with color
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# Git shortcuts
alias g='git'
alias gs='git status'
alias gd='git diff'
alias gl='git log --oneline -20'
alias gco='git checkout'
alias gb='git branch'
alias gp='git push'
alias gpl='git pull'

# Disk usage
alias du='du -h'
alias df='df -h'

# Process
alias psg='ps aux | grep -v grep | grep'
```

## .bashrc.d/history.sh

```bash
# ~/.bashrc.d/history.sh - Shell history configuration

# Large history
HISTSIZE=50000
HISTFILESIZE=100000

# Append to history, don't overwrite
shopt -s histappend

# Save multi-line commands as one entry
shopt -s cmdhist

# Ignore duplicates and blank lines
HISTCONTROL=ignoreboth:erasedups

# Timestamp history entries
HISTTIMEFORMAT="%Y-%m-%d %H:%M:%S  "

# Immediately append to history (for multiple terminals)
PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND$'\n'}history -a; history -c; history -r"
```

## .bashrc.d/path.sh

```bash
# ~/.bashrc.d/path.sh - PATH configuration

# Local scripts
[ -d "$HOME/.local/bin" ] && PATH="$HOME/.local/bin:$PATH"
[ -d "$HOME/bin" ] && PATH="$HOME/bin:$PATH"

# Project scripts
[ -d "$HOME/workspace/scripts" ] && PATH="$HOME/workspace/scripts:$PATH"

export PATH
```

## .bashrc.d/prompt.sh

```bash
# ~/.bashrc.d/prompt.sh - Prompt configuration

# Colors
RED='\[\033[0;31m\]'
GREEN='\[\033[0;32m\]'
YELLOW='\[\033[0;33m\]'
BLUE='\[\033[0;34m\]'
RESET='\[\033[0m\]'

# Git branch in prompt
parse_git_branch() {
    git branch 2>/dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}

# Prompt: user@host:dir (branch)$
PS1="${GREEN}\u@\h${RESET}:${BLUE}\w${RESET}${YELLOW}\$(parse_git_branch)${RESET}\$ "
```

## .gitconfig

```ini
# ~/.gitconfig
[user]
    name = Your Name
    email = your@email.com

[core]
    excludesfile = ~/.gitignore_global
    editor = vim
    autocrlf = input
    pager = less -FRX

[init]
    defaultBranch = main

[pull]
    rebase = true

[push]
    default = current
    autoSetupRemote = true

[fetch]
    prune = true

[diff]
    algorithm = histogram
    colorMoved = default

[merge]
    conflictstyle = diff3

[rebase]
    autoStash = true

[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    lg = log --oneline --graph --decorate -20
    last = log -1 HEAD
    unstage = reset HEAD --
    amend = commit --amend --no-edit
    branches = branch -a
    tags = tag -l
    stashes = stash list
    wip = !git add -A && git commit -m 'wip: work in progress'

[color]
    ui = auto
```

## .gitignore_global

```gitignore
# OS
.DS_Store
Thumbs.db
*.swp
*.swo
*~

# IDE
.idea/
.vscode/
*.sublime-project
*.sublime-workspace

# Environment
.env
.env.local

# Python
__pycache__/
*.pyc
.venv/
venv/
*.egg-info/
dist/
build/

# Node
node_modules/

# direnv
.direnv/
```

## .tmux.conf

```bash
# ~/.tmux.conf

# ============================================================
# General
# ============================================================
set -g default-terminal "screen-256color"
set -g history-limit 50000
set -g mouse on
set -g status-interval 5
set -g focus-events on
set -sg escape-time 0

# Start windows and panes at 1, not 0
set -g base-index 1
setw -g pane-base-index 1

# Renumber windows when one is closed
set -g renumber-windows on

# ============================================================
# Key Bindings
# ============================================================
# Prefix: Ctrl+a (more ergonomic than Ctrl+b)
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# Split panes with | and -
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
unbind '"'
unbind %

# New window in current directory
bind c new-window -c "#{pane_current_path}"

# Reload config
bind r source-file ~/.tmux.conf \; display "Config reloaded"

# Navigate panes with Alt+arrow
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# Resize panes with Shift+arrow
bind -n S-Left resize-pane -L 2
bind -n S-Right resize-pane -R 2
bind -n S-Up resize-pane -U 2
bind -n S-Down resize-pane -D 2

# ============================================================
# Status Bar
# ============================================================
set -g status-position bottom
set -g status-style 'bg=colour235 fg=colour136'
set -g status-left '[#S] '
set -g status-left-length 30
set -g status-right '#H | %Y-%m-%d %H:%M'
set -g status-right-length 50

# Window status
setw -g window-status-current-style 'bg=colour238 fg=colour81 bold'
setw -g window-status-current-format ' #I:#W#F '
setw -g window-status-style 'fg=colour244'
setw -g window-status-format ' #I:#W#F '
```

## .vimrc

```vim
" ~/.vimrc - Minimal but productive vim config

" General
set nocompatible
set encoding=utf-8
set fileencoding=utf-8
set backspace=indent,eol,start

" Display
syntax on
set number
set relativenumber
set ruler
set showcmd
set showmode
set laststatus=2
set cursorline
set scrolloff=5
set wildmenu
set wildmode=longest:full,full

" Search
set hlsearch
set incsearch
set ignorecase
set smartcase
nnoremap <CR> :nohlsearch<CR><CR>

" Indentation
set autoindent
set smartindent
set expandtab
set tabstop=4
set shiftwidth=4
set softtabstop=4

" Files
set autoread
set noswapfile
set nobackup
set nowritebackup

" Clipboard
set clipboard=unnamedplus

" Status line
set statusline=%f\ %m%r%h%w\ [%{&ff}]\ [%Y]\ [%l/%L,\ %c]\ %p%%
```

## .ssh/config

```
# ~/.ssh/config

Host nero-hetzner
    HostName SERVER_IP
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
    IdentitiesOnly yes
```

## bootstrap.sh

```bash
#!/bin/bash
# bootstrap.sh - Install dotfiles on a new machine
set -euo pipefail

DOTFILES_DIR="$HOME/dotfiles"
REPO_URL="${1:-git@github.com:USER/dotfiles.git}"

echo "=== Dotfiles Bootstrap ==="

# Clone if needed
if [ ! -d "$DOTFILES_DIR" ]; then
    echo "Cloning dotfiles..."
    git clone "$REPO_URL" "$DOTFILES_DIR"
fi

cd "$DOTFILES_DIR"

# Install stow
if ! command -v stow &>/dev/null; then
    echo "Installing stow..."
    sudo apt install -y stow
fi

# Create .bashrc.d directory
mkdir -p "$HOME/.bashrc.d"

# Backup existing dotfiles
BACKUP_DIR="$HOME/.dotfiles-backup-$(date +%Y%m%d)"
for f in .bashrc .bash_profile .gitconfig .tmux.conf .vimrc; do
    if [ -f "$HOME/$f" ] && [ ! -L "$HOME/$f" ]; then
        mkdir -p "$BACKUP_DIR"
        mv "$HOME/$f" "$BACKUP_DIR/"
        echo "Backed up $f to $BACKUP_DIR/"
    fi
done

# Stow base packages
echo "Stowing packages..."
for pkg in bash git tmux vim ssh scripts; do
    if [ -d "$pkg" ]; then
        stow -v "$pkg" 2>&1 | grep -v "^$" || true
        echo "  Stowed: $pkg"
    fi
done

# Machine-specific overrides
if systemctl is-active sshd >/dev/null 2>&1 && [ ! -f /proc/version ] || grep -q "Hetzner\|DigitalOcean\|Linode" /proc/version 2>/dev/null; then
    MACHINE_TYPE="server"
elif command -v code &>/dev/null || [ -n "${DISPLAY:-}" ]; then
    MACHINE_TYPE="workstation"
else
    MACHINE_TYPE="server"
fi

if [ -d "machine-$MACHINE_TYPE" ]; then
    stow -v "machine-$MACHINE_TYPE" 2>&1 | grep -v "^$" || true
    echo "  Stowed: machine-$MACHINE_TYPE"
fi

echo ""
echo "=== Bootstrap complete (type: $MACHINE_TYPE) ==="
echo "Restart your shell: source ~/.bashrc"
```

## install.sh (Quick Re-stow)

```bash
#!/bin/bash
# install.sh - Re-stow all packages (after git pull)
set -euo pipefail

cd "$(dirname "$0")"

# Restow all packages
for pkg in bash git tmux vim ssh scripts; do
    [ -d "$pkg" ] && stow -R "$pkg"
done

# Machine-specific (detect or pass as arg)
MACHINE_TYPE="${1:-server}"
[ -d "machine-$MACHINE_TYPE" ] && stow -R "machine-$MACHINE_TYPE"

echo "All packages restowed."
```

## .gitignore (for dotfiles repo)

```gitignore
# SSH keys (NEVER commit)
ssh/.ssh/id_*
ssh/.ssh/known_hosts
ssh/.ssh/authorized_keys

# Shell history
bash/.bash_history
bash/.zsh_history

# Secrets
*.secret
*.key
*.pem
.env
.env.*

# Editor state
vim/.vim/undo/
vim/.vim/swap/
vim/.viminfo

# Claude Code projects (may contain secrets)
claude/.claude/projects/

# GPG
.gnupg/

# OS files
.DS_Store
Thumbs.db
```

## machine-server/.bashrc.d/server.sh

```bash
# Server-specific configuration

export EDITOR=vim
export VISUAL=vim

# Service management aliases
alias services='systemctl --user list-units --type=service --state=active'
alias logs='journalctl --user -f'
alias dps='docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'

# Deploy shortcut
alias deploy='bash ~/workspace/deploy/deploy.sh'
alias deploy-all='bash ~/workspace/deploy/deploy.sh all'

# Health check
alias health='bash /srv/nero/health-check.sh'

# Quick server status
alias status='echo "=== Memory ===" && free -h && echo "" && echo "=== Disk ===" && df -h / && echo "" && echo "=== Load ===" && uptime && echo "" && echo "=== Services ===" && systemctl --user list-units --type=service --state=active --no-pager'
```
