# Shell Productivity

Modern CLI toolkit for Ubuntu/Debian servers. Covers installation, configuration, and integration of tools that replace traditional Unix utilities with faster, more informative alternatives.

## Scope

- Modern CLI tool selection and installation
- Configuration and integration between tools
- Shell prompt customization (starship)
- File search and preview (fzf, fd)
- Better cat/less (bat)
- Better ls (eza)
- Better git diff (delta)
- Directory jumping (zoxide)
- System monitoring (btop, duf, dust)
- Fast search (ripgrep)

## Why This Matters

Traditional Unix utilities (ls, cat, grep, find, top) work but lack:

- **Color coding** for quick visual parsing
- **Git integration** for development workflows
- **Preview** capabilities for quick file inspection
- **Fuzzy search** for fast navigation
- **Smart defaults** that match modern workflows

For a solo developer managing multiple projects via SSH, these tools save significant time daily.

## Tool Overview

| Traditional | Modern | Improvement |
|-------------|--------|-------------|
| `cat` | `bat` | Syntax highlighting, git integration, line numbers |
| `ls` | `eza` | Colors, icons, git status, tree view |
| `find` | `fd` | Faster, simpler syntax, respects .gitignore |
| `grep` | `ripgrep` (rg) | Faster, respects .gitignore, better output |
| `top` | `btop` | Beautiful UI, process tree, network, disk |
| `diff` | `delta` | Side-by-side, syntax highlighting, git integration |
| `df` | `duf` | Colored table, human-readable, filters |
| `du` | `dust` | Visual tree, sorted by size |
| `cd` | `zoxide` | Frecency-based directory jumping |
| prompt | `starship` | Fast, customizable, cross-shell prompt |
| `Ctrl+R` | `fzf` | Fuzzy search history, files, processes |

## Installation on Ubuntu 24.04

### Package Manager (apt)

```bash
# Available in Ubuntu repos
sudo apt install -y bat fd-find fzf ripgrep

# bat is installed as 'batcat' on Ubuntu (name conflict)
# Create alias or symlink:
sudo ln -sf /usr/bin/batcat /usr/local/bin/bat
```

### From GitHub Releases (latest versions)

```bash
# eza (better ls)
sudo apt install -y gpg
sudo mkdir -p /etc/apt/keyrings
wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc | sudo gpg --dearmor -o /etc/apt/keyrings/gierens.gpg
echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" | sudo tee /etc/apt/sources.list.d/gierens.list
sudo apt update && sudo apt install -y eza

# delta (better diff)
DELTA_VERSION="0.18.2"
wget "https://github.com/dandavison/delta/releases/download/${DELTA_VERSION}/git-delta_${DELTA_VERSION}_amd64.deb"
sudo dpkg -i "git-delta_${DELTA_VERSION}_amd64.deb"
rm "git-delta_${DELTA_VERSION}_amd64.deb"

# starship (prompt)
curl -sS https://starship.rs/install.sh | sh

# zoxide (smart cd)
curl -sSfL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | sh

# btop (system monitor)
sudo apt install -y btop

# duf (disk usage)
sudo apt install -y duf

# dust (directory usage)
DUST_VERSION="1.1.1"
wget "https://github.com/bootandy/dust/releases/download/v${DUST_VERSION}/du-dust_${DUST_VERSION}-1_amd64.deb"
sudo dpkg -i "du-dust_${DUST_VERSION}-1_amd64.deb"
rm "du-dust_${DUST_VERSION}-1_amd64.deb"
```

## Tool Configuration

### bat

```bash
# ~/.bashrc or ~/.bash_aliases
export BAT_THEME="TwoDark"
export BAT_STYLE="numbers,changes,header"
alias cat="bat --paging=never"
alias less="bat --paging=always"
```

### fzf

```bash
# ~/.bashrc
# Enable fzf key bindings and completion
eval "$(fzf --bash)"

# Use fd for file search (faster, respects .gitignore)
export FZF_DEFAULT_COMMAND='fd --type f --hidden --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"

# Preview files with bat
export FZF_CTRL_T_OPTS="--preview 'bat --color=always --style=numbers --line-range=:200 {}'"

# Preview directories with eza
export FZF_ALT_C_COMMAND='fd --type d --hidden --exclude .git'
export FZF_ALT_C_OPTS="--preview 'eza --tree --level=2 --color=always {}'"
```

### delta (git diff)

```gitconfig
# ~/.gitconfig
[core]
    pager = delta

[interactive]
    diffFilter = delta --color-only

[delta]
    navigate = true
    side-by-side = true
    line-numbers = true
    syntax-theme = TwoDark

[merge]
    conflictstyle = diff3

[diff]
    colorMoved = default
```

### starship

```bash
# ~/.bashrc (add at the end)
eval "$(starship init bash)"
```

### zoxide

```bash
# ~/.bashrc (add at the end)
eval "$(zoxide init bash)"

# Usage:
# z foo      -> cd to most frecent directory matching 'foo'
# zi foo     -> interactive selection with fzf
```

### eza

```bash
# ~/.bash_aliases
alias ls="eza --color=always --group-directories-first"
alias ll="eza -la --color=always --group-directories-first --git"
alias lt="eza --tree --level=2 --color=always"
alias la="eza -a --color=always --group-directories-first"
```

## Common Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| bat installed as batcat on Ubuntu | `bat` command not found | Create symlink or alias |
| fd installed as fdfind on Ubuntu | `fd` command not found | Create symlink or alias |
| fzf overrides Ctrl+R | Unexpected behavior | Learn fzf search syntax |
| starship slow on large git repos | Prompt delay | Configure git status timeout |
| delta as pager breaks non-git output | Garbled output | Only set as git pager |

## Verification

```bash
# Check all tools are installed
for tool in bat fd fzf rg eza delta starship zoxide btop duf dust; do
    if command -v "$tool" &>/dev/null; then
        echo "OK: $tool ($(command -v $tool))"
    else
        echo "MISSING: $tool"
    fi
done
```

## Integration Points

| Tool | Integrates With |
|------|----------------|
| bat | fzf (preview), less (pager), git (diff) |
| fd | fzf (file source), find replacement |
| fzf | bash (Ctrl+R, Ctrl+T), bat (preview), fd (source) |
| delta | git (diff, log, blame), bat (syntax theme) |
| rg | fzf (search source), grep replacement |
| starship | bash/zsh/fish (prompt), git (branch, status) |
| zoxide | cd replacement, fzf (interactive mode) |

## References

- [bat](https://github.com/sharkdp/bat)
- [fd](https://github.com/sharkdp/fd)
- [fzf](https://github.com/junegunn/fzf)
- [ripgrep](https://github.com/BurntSushi/ripgrep)
- [eza](https://github.com/eza-community/eza)
- [delta](https://github.com/dandavison/delta)
- [starship](https://starship.rs/)
- [zoxide](https://github.com/ajeetdsouza/zoxide)
- [btop](https://github.com/aristocratos/btop)
- [duf](https://github.com/muesli/duf)
- [dust](https://github.com/bootandy/dust)
