# Bash Aliases

Comprehensive bash alias organization and productivity methodology. Covers alias design, function aliases, completion-aware aliases, and categorized shortcut collections for server management.

## Scope

- Alias file organization (~/.bash_aliases)
- Simple aliases vs function aliases
- Completion-aware aliases (preserving tab completion)
- Category-based organization (system, docker, git, nginx, systemd, logs, network)
- Project-specific aliases (NERO platform)
- Safety aliases (rm, mv, cp confirmations)
- Navigation aliases
- Best practices for maintainable alias files

## Why This Matters

A well-organized alias file:

- Reduces repetitive typing (save 30+ keystrokes per common command)
- Prevents mistakes (safety aliases for destructive commands)
- Provides consistent shortcuts across sessions
- Documents common operations (aliases serve as runbook)
- Speeds up server administration significantly

## Architecture

Bash loads aliases from `~/.bash_aliases` automatically (sourced by `~/.bashrc`):

```bash
# In ~/.bashrc (Ubuntu default):
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi
```

### Alias Types

**Simple aliases:** Direct command substitution
```bash
alias ll="ls -la"
```

**Function aliases:** Multi-step operations with parameters
```bash
mkcd() { mkdir -p "$1" && cd "$1"; }
```

**Completion-aware aliases:** Use `complete -F` to preserve tab completion
```bash
alias g="git"
complete -o default -o nospace -F _git g
```

## Key Concepts

### 1. Organization by Category

Group aliases by domain for easy maintenance:

```bash
# === System ===
# === Docker ===
# === Git ===
# === nginx ===
# === Systemd ===
# === Logs ===
# === Network ===
# === Navigation ===
# === Project-specific ===
```

### 2. Naming Conventions

| Convention | Example | When to Use |
|------------|---------|-------------|
| Short abbreviation | `g` for git | Very frequent commands |
| Prefix + action | `dk-ps` for docker ps | Grouped commands |
| Descriptive | `ports` for listening ports | Infrequent but memorable |
| Verb-noun | `show-services` | Self-documenting |

### 3. Safety Aliases

Always add confirmation for destructive commands:

```bash
alias rm="rm -i"
alias mv="mv -i"
alias cp="cp -i"
```

Or use a trash function instead of rm:

```bash
trash() { mv "$@" ~/.local/share/Trash/files/; }
```

### 4. Function Aliases vs Simple Aliases

Use functions when you need:
- Parameters: `mkcd() { mkdir -p "$1" && cd "$1"; }`
- Multiple commands: `deploy() { git pull && make build && make deploy; }`
- Conditionals: `port() { sudo lsof -i ":$1" 2>/dev/null || echo "Nothing on port $1"; }`

Use simple aliases when:
- Direct substitution: `alias gs="git status -sb"`
- Adding default flags: `alias grep="grep --color=auto"`

### 5. Listing and Managing Aliases

```bash
# List all aliases
alias

# List aliases matching a pattern
alias | grep docker

# Remove an alias
unalias ll

# Bypass an alias (use original command)
\rm file.txt        # Backslash bypasses alias
command rm file.txt  # 'command' keyword bypasses alias
```

## Common Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Aliasing over critical commands | Unexpected behavior | Test in subshell first |
| Complex logic in aliases | Hard to debug | Use functions instead |
| Missing quotes around values | Word splitting issues | Always quote alias values |
| Circular aliases | Infinite recursion | Don't alias a command to itself with different flags |
| No comments | Forget what alias does | Comment every non-obvious alias |
| Not sourcing after changes | Aliases not active | `source ~/.bash_aliases` |

## Verification

```bash
# List all aliases
alias

# Check specific alias
type ll

# Check if alias or function
type -t mkcd

# Test an alias (without executing)
alias | grep "alias ll="

# Count aliases
alias | wc -l
```

## References

- [Bash manual: aliases](https://www.gnu.org/software/bash/manual/html_node/Aliases.html)
- [Bash manual: functions](https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html)
