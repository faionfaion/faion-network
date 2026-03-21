# Shell Productivity Templates

Copy-paste ready configurations for modern CLI tools.

## Template 1: starship.toml (Minimal Server Prompt)

File: `~/.config/starship.toml`

```toml
# ~/.config/starship.toml
# Minimal prompt for server use — fast, informative, no clutter

# Prompt format (left to right)
format = """
$hostname\
$directory\
$git_branch\
$git_status\
$python\
$nodejs\
$character"""

# Don't add blank line between prompts
add_newline = false

# Scan timeout (ms) — keep low for fast prompt
scan_timeout = 30
command_timeout = 500

[hostname]
ssh_only = true
format = "[$hostname](bold blue):"
disabled = false

[directory]
truncation_length = 3
truncation_symbol = ".../"
style = "bold cyan"

[git_branch]
format = " [$branch]($style)"
style = "bold purple"
truncation_length = 20

[git_status]
format = '([$all_status$ahead_behind]($style))'
style = "bold red"
ahead = " +"
behind = " -"
modified = " ~"
untracked = " ?"
staged = " +"
conflicted = " !"

[python]
format = ' [py$version]($style)'
style = "yellow"
detect_files = ["pyproject.toml", "setup.py", "Pipfile"]

[nodejs]
format = ' [node$version]($style)'
style = "green"
detect_files = ["package.json"]

[character]
success_symbol = "[>](bold green)"
error_symbol = "[>](bold red)"

# Disable unused modules for speed
[aws]
disabled = true

[docker_context]
disabled = true

[gcloud]
disabled = true

[kubernetes]
disabled = true

[package]
disabled = true
```

## Template 2: .gitconfig with delta

```gitconfig
# ~/.gitconfig — Git configuration with delta integration

[user]
    name = Your Name
    email = your@email.com

[core]
    editor = vim
    pager = delta
    autocrlf = input

[interactive]
    diffFilter = delta --color-only

[delta]
    navigate = true
    side-by-side = true
    line-numbers = true
    syntax-theme = TwoDark
    plus-style = "syntax #003800"
    minus-style = "syntax #3f0001"
    hunk-header-decoration-style = blue box
    file-style = bold yellow ul
    file-decoration-style = none

[merge]
    conflictstyle = diff3

[diff]
    colorMoved = default
    algorithm = histogram

[pull]
    rebase = true

[push]
    default = current
    autoSetupRemote = true

[init]
    defaultBranch = main

[alias]
    s = status -sb
    l = log --oneline -20
    lg = log --graph --oneline --decorate -20
    d = diff
    ds = diff --staged
    co = checkout
    br = branch -vv
    aa = add -A
    cm = commit -m
    amend = commit --amend --no-edit
    undo = reset --soft HEAD~1
    stash-all = stash push --include-untracked
```

## Template 3: fzf Configuration with Previews

```bash
# ~/.bashrc — fzf configuration block

# Initialize fzf
eval "$(fzf --bash)"

# --- Default command (what fzf searches) ---
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git --exclude node_modules --exclude .venv --exclude __pycache__'

# --- Ctrl+T: File search with preview ---
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_CTRL_T_OPTS="
    --preview 'bat --color=always --style=numbers --line-range=:300 {} 2>/dev/null || echo {}'
    --preview-window 'right:50%:wrap'
    --bind 'ctrl-/:toggle-preview'
    --header 'CTRL+T: File search | CTRL+/: toggle preview'"

# --- Alt+C: Directory search ---
export FZF_ALT_C_COMMAND='fd --type d --hidden --follow --exclude .git --exclude node_modules --exclude .venv'
export FZF_ALT_C_OPTS="
    --preview 'eza --tree --level=2 --color=always {} 2>/dev/null'
    --preview-window 'right:50%'
    --header 'ALT+C: Directory jump'"

# --- Ctrl+R: History search ---
export FZF_CTRL_R_OPTS="
    --preview 'echo {}'
    --preview-window 'down:3:wrap'
    --header 'CTRL+R: History search'"

# --- Custom fzf functions ---

# fzf + git log (browse commits)
fgl() {
    git log --oneline --color=always | fzf --ansi --preview 'git show --color=always {1}' --preview-window 'right:60%'
}

# fzf + git branch (switch branches)
fbr() {
    local branch
    branch=$(git branch -vv --color=always | fzf --ansi | awk '{print $1}' | tr -d '* ')
    [ -n "$branch" ] && git checkout "$branch"
}

# fzf + process kill
fkill() {
    local pid
    pid=$(ps aux | fzf --header-lines=1 --preview 'echo {}' | awk '{print $2}')
    [ -n "$pid" ] && kill -9 "$pid"
}

# fzf + ripgrep (search content, open in editor)
frg() {
    local selection
    selection=$(rg --color=always --line-number "$@" | fzf --ansi --delimiter : --preview 'bat --color=always --highlight-line {2} {1}' --preview-window '+{2}/2')
    if [ -n "$selection" ]; then
        local file=$(echo "$selection" | cut -d: -f1)
        local line=$(echo "$selection" | cut -d: -f2)
        ${EDITOR:-vim} "+$line" "$file"
    fi
}
```

## Template 4: Complete ~/.bash_aliases (Tool Aliases)

```bash
# ~/.bash_aliases — Modern CLI tool aliases

# --- File listing (eza) ---
if command -v eza &>/dev/null; then
    alias ls="eza --color=always --group-directories-first"
    alias ll="eza -la --color=always --group-directories-first --git"
    alias lt="eza --tree --level=2 --color=always --group-directories-first"
    alias lt3="eza --tree --level=3 --color=always --group-directories-first"
    alias la="eza -a --color=always --group-directories-first"
    alias l="eza -1 --color=always --group-directories-first"
fi

# --- File viewing (bat) ---
if command -v bat &>/dev/null; then
    alias cat="bat --paging=never"
    alias less="bat --paging=always"
    alias batdiff="bat --diff"
fi

# --- Disk usage ---
if command -v duf &>/dev/null; then
    alias df="duf"
fi
if command -v dust &>/dev/null; then
    alias du="dust"
fi

# --- System monitoring ---
if command -v btop &>/dev/null; then
    alias top="btop"
fi
```

## Template 5: Installation Script (All-in-One)

```bash
#!/bin/bash
# install-cli-tools.sh — Install all modern CLI tools on Ubuntu 24.04

set -euo pipefail

echo "=== Installing Modern CLI Tools ==="

# apt packages
echo "--- apt packages ---"
sudo apt update
sudo apt install -y bat fd-find fzf ripgrep btop duf

# Symlinks for Ubuntu naming
sudo ln -sf /usr/bin/batcat /usr/local/bin/bat 2>/dev/null || true
sudo ln -sf /usr/bin/fdfind /usr/local/bin/fd 2>/dev/null || true

# eza
echo "--- eza ---"
if ! command -v eza &>/dev/null; then
    sudo mkdir -p /etc/apt/keyrings
    wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc | \
        sudo gpg --dearmor -o /etc/apt/keyrings/gierens.gpg 2>/dev/null
    echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" | \
        sudo tee /etc/apt/sources.list.d/gierens.list >/dev/null
    sudo apt update && sudo apt install -y eza
fi

# delta
echo "--- delta ---"
if ! command -v delta &>/dev/null; then
    DELTA_VER="0.18.2"
    wget -q "https://github.com/dandavison/delta/releases/download/${DELTA_VER}/git-delta_${DELTA_VER}_amd64.deb" -O /tmp/delta.deb
    sudo dpkg -i /tmp/delta.deb && rm /tmp/delta.deb
fi

# starship
echo "--- starship ---"
if ! command -v starship &>/dev/null; then
    curl -sS https://starship.rs/install.sh | sh -s -- -y
fi

# zoxide
echo "--- zoxide ---"
if ! command -v zoxide &>/dev/null; then
    curl -sSfL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | sh
fi

# dust
echo "--- dust ---"
if ! command -v dust &>/dev/null; then
    DUST_VER="1.1.1"
    wget -q "https://github.com/bootandy/dust/releases/download/v${DUST_VER}/du-dust_${DUST_VER}-1_amd64.deb" -O /tmp/dust.deb
    sudo dpkg -i /tmp/dust.deb && rm /tmp/dust.deb
fi

echo ""
echo "=== Verification ==="
for tool in bat fd fzf rg eza delta starship zoxide btop duf dust; do
    if command -v "$tool" &>/dev/null; then
        printf "  OK  %-12s %s\n" "$tool" "$(command -v $tool)"
    else
        printf "  MISSING  %s\n" "$tool"
    fi
done

echo ""
echo "=== Next Steps ==="
echo "1. Add shell integrations to ~/.bashrc"
echo "2. Create ~/.config/starship.toml"
echo "3. Configure delta in ~/.gitconfig"
echo "4. Add aliases to ~/.bash_aliases"
echo "5. Source: source ~/.bashrc"
```
