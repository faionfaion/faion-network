# Shell Productivity

## Summary

**One-sentence:** Generates a per-host shell-productivity bundle (fzf + ripgrep + bat + starship + zoxide) with shell config + alias file, gated by an idempotent installer.

**One-paragraph:** Solo devs live in the terminal; small ergonomic gains compound. This methodology pins the tool list (fzf, ripgrep, bat, starship, zoxide, eza), shell wiring (bash/zsh), and starship preset. Output: a ShellPlan + install-cli-tools.sh that converges to the same end state when re-run.

**Ефективно для:**

- Long-lived SSH sessions where fuzzy-find + history search cut keystrokes.
- Multi-host tmux workflows that need the same prompt + aliases.
- Onboarding a new server with a 30-second 'feels like home' setup.
- Replacing legacy ~/.bashrc cruft with a versioned config.

## Applies If (ALL must hold)

- Operator works in interactive shell ≥1h/day.
- Setting up shell on a fresh server or workstation.
- Standardising shell across multiple hosts.
- Replacing ad-hoc dotfiles with a versioned bundle.

## Skip If (ANY kills it)

- Read-only / production hosts where operator login is rare.
- Containers / CI runners — install overhead not worth it.
- Locked-down environments where third-party binaries are blocked.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Operator shell preference | bash|zsh | operator |
| Tool list | list of CLI tools | ShellPlan inventory |
| Starship preset choice | preset name | starship.toml |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| dotfiles-management | Shell configs are part of the dotfiles repo; this methodology delegates storage. |
| tmux-power-user | tmux pairs with the shell config; shared prompt expectations. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-idempotent-installer, r2-versioned-rc, r3-no-secrets-in-rc, r4-named-owner, r5-history-shared | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Shell Productivity artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: rc-overwrite-clobbers, secrets-in-bashrc, slow-prompt-blocks-shell, history-not-shared | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-shell-plan` | sonnet | Tool selection + shell wiring. |
| `render-installer` | haiku | Template fill from plan. |

## Templates

| File | Purpose |
|------|---------|
| `templates/shell-productivity.json` | ShellPlan JSON skeleton (tool list, shell, starship preset). |
| `templates/shell-productivity.md.j2` | Human-readable audit trail. |
| `templates/shell-productivity.md` | Human-readable audit trail. Generated from `templates/shell-productivity.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/install-cli-tools.sh` | Idempotent installer for the chosen tool list. |
| `templates/fzf-config.sh` | fzf key-bindings + completion source block. |
| `templates/starship.toml` | starship preset with concise prompt. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-shell-productivity.py` | Validate ShellPlan JSON against the schema. | Before applying installer to a host. |

## Related

- [[dotfiles-management]]
- [[tmux-power-user]]
- [[bash-aliases]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/shell-productivity.json`

```json
{
  "artefact_id": "shell-<host>",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "shell": "bash",
  "tools": [
    "fzf",
    "ripgrep",
    "bat",
    "starship",
    "zoxide",
    "eza"
  ],
  "starship_preset": "tokyo-night",
  "owner": "<@handle>"
}
```

### `templates/install-cli-tools.sh`

```bash
# install-cli-tools.sh — Idempotent install of modern CLI tools on Ubuntu 24.04
#
# Tools: bat, fd, fzf, ripgrep, eza, delta, starship, zoxide, btop, duf, dust
# Run as a user with sudo; does not require root directly.

set -euo pipefail

echo "=== Installing Modern CLI Tools ==="

# apt-available tools
echo "--- apt packages ---"
sudo apt-get update -qq
sudo apt-get install -y bat fd-find fzf ripgrep btop duf

# Fix Ubuntu naming conflicts (batcat -> bat, fdfind -> fd)
[ -x /usr/bin/batcat ] && sudo ln -sf /usr/bin/batcat /usr/local/bin/bat || true
[ -x /usr/bin/fdfind ] && sudo ln -sf /usr/bin/fdfind /usr/local/bin/fd || true

# eza (better ls)
echo "--- eza ---"
if ! command -v eza &>/dev/null; then
    sudo mkdir -p /etc/apt/keyrings
    wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc \
        | sudo gpg --dearmor -o /etc/apt/keyrings/gierens.gpg 2>/dev/null
    echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" \
        | sudo tee /etc/apt/sources.list.d/gierens.list >/dev/null
    sudo apt-get update -qq && sudo apt-get install -y eza
    echo "  Installed eza"
else
    echo "  Already installed: eza"
fi

# delta (better git diff)
echo "--- delta ---"
if ! command -v delta &>/dev/null; then
    DELTA_VER="0.18.2"
    wget -q "https://github.com/dandavison/delta/releases/download/${DELTA_VER}/git-delta_${DELTA_VER}_amd64.deb" -O /tmp/delta.deb
    sudo dpkg -i /tmp/delta.deb && rm /tmp/delta.deb
    echo "  Installed delta $DELTA_VER"
else
    echo "  Already installed: delta"
fi

# starship (prompt)
echo "--- starship ---"
if ! command -v starship &>/dev/null; then
    curl -sS https://starship.rs/install.sh | sh -s -- -y
    echo "  Installed starship"
else
    echo "  Already installed: starship"
fi

# zoxide (smart cd)
echo "--- zoxide ---"
if ! command -v zoxide &>/dev/null; then
    curl -sSfL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | sh
    echo "  Installed zoxide"
else
    echo "  Already installed: zoxide"
fi

# dust (better du)
echo "--- dust ---"
if ! command -v dust &>/dev/null; then
    DUST_VER="1.1.1"
    wget -q "https://github.com/bootandy/dust/releases/download/v${DUST_VER}/du-dust_${DUST_VER}-1_amd64.deb" -O /tmp/dust.deb
    sudo dpkg -i /tmp/dust.deb && rm /tmp/dust.deb
    echo "  Installed dust $DUST_VER"
else
    echo "  Already installed: dust"
fi

echo ""
echo "=== Verification ==="
for tool in bat fd fzf rg eza delta starship zoxide btop duf dust; do
    if command -v "$tool" &>/dev/null; then
        printf "  OK      %-12s %s\n" "$tool" "$(command -v "$tool")"
    else
        printf "  MISSING %-12s\n" "$tool"
    fi
done

echo ""
echo "=== Next Steps ==="
echo "1. Add to ~/.bashrc:"
echo "   eval \"\$(fzf --bash)\""
echo "   eval \"\$(starship init bash)\""
echo "   eval \"\$(zoxide init bash)\""
echo "2. Copy templates/starship.toml to ~/.config/starship.toml"
echo "3. Add templates/fzf-config.sh block to ~/.bashrc"
echo "4. Add delta section to ~/.gitconfig"
echo "5. Add tool aliases to ~/.bash_aliases"
```

### `templates/fzf-config.sh`

```bash
# fzf shell integration block
# Source or paste this into ~/.bashrc
#
# Requires: fzf, fd (as fd, not fdfind), bat, eza

# Initialize fzf (key bindings: Ctrl+R, Ctrl+T, Alt+C)
if command -v fzf &>/dev/null; then
    eval "$(fzf --bash)"

    # Use fd as fzf's file source (faster, .gitignore-aware)
    if command -v fd &>/dev/null; then
        export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow \
            --exclude .git --exclude node_modules --exclude .venv --exclude __pycache__'
        export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
        export FZF_ALT_C_COMMAND='fd --type d --hidden --follow --exclude .git'
    fi

    # Ctrl+T: file picker with bat preview
    if command -v bat &>/dev/null; then
        export FZF_CTRL_T_OPTS="
            --preview 'bat --color=always --style=numbers --line-range=:300 {} 2>/dev/null'
            --preview-window 'right:50%:wrap'
            --bind 'ctrl-/:toggle-preview'"
    fi

    # Alt+C: directory jump with eza tree preview
    if command -v eza &>/dev/null; then
        export FZF_ALT_C_OPTS="
            --preview 'eza --tree --level=2 --color=always {} 2>/dev/null'
            --preview-window 'right:50%'"
    fi

    # Ctrl+R: history search
    export FZF_CTRL_R_OPTS="--preview 'echo {}' --preview-window 'down:3:wrap'"
fi

# --- Helper functions ---

# Browse git log and show commit diff in preview
fgl() {
    git log --oneline --color=always | \
        fzf --ansi --preview 'git show --color=always {1}' --preview-window 'right:60%'
}

# Interactive git branch switch
fbr() {
    local branch
    branch=$(git branch -vv --color=always | fzf --ansi | awk '{print $1}' | tr -d '* ')
    [ -n "$branch" ] && git checkout "$branch"
}

# Search file contents with ripgrep, open result in editor
frg() {
    [ -z "${1:-}" ] && { echo "Usage: frg <search-term>"; return 1; }
    local selection
    selection=$(rg --color=always --line-number "$@" | \
        fzf --ansi --delimiter : \
            --preview 'bat --color=always --highlight-line {2} {1} 2>/dev/null' \
            --preview-window '+{2}/2')
    if [ -n "$selection" ]; then
        local file line
        file=$(echo "$selection" | cut -d: -f1)
        line=$(echo "$selection" | cut -d: -f2)
        "${EDITOR:-vim}" "+$line" "$file"
    fi
}

# Interactive process kill
fkill() {
    local pid
    pid=$(ps aux | fzf --header-lines=1 | awk '{print $2}')
    [ -n "$pid" ] && kill -9 "$pid" && echo "Killed PID $pid"
}
```

### `templates/starship.toml`

```toml
# ~/.config/starship.toml
# Minimal server-optimized starship prompt
# Install: mkdir -p ~/.config && cp starship.toml ~/.config/starship.toml
# Activate: add `eval "$(starship init bash)"` to ~/.bashrc

format = """
$hostname\
$directory\
$git_branch\
$git_status\
$python\
$nodejs\
$character"""

add_newline = false
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
detect_files = ["pyproject.toml", "setup.py", "Pipfile", "requirements.txt"]

[nodejs]
format = ' [node$version]($style)'
style = "green"
detect_files = ["package.json"]

[character]
success_symbol = "[>](bold green)"
error_symbol = "[>](bold red)"

# Disable unused modules for faster prompt
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

[terraform]
disabled = true
```
