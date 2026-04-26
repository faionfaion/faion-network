#!/bin/bash
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
