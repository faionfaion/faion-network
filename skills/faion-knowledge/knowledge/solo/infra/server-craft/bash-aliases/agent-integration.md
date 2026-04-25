# Agent Integration — Bash Aliases

## When to use
- Setting up a new server or workstation where productivity shortcuts are missing
- Onboarding to a new project where project-specific aliases speed up repetitive tasks
- Auditing existing `.bash_aliases` for conflicts, missing completions, or undocumented shortcuts
- Documenting a server's operational commands as aliases (aliases-as-runbook pattern)
- Consolidating ad-hoc functions scattered across `.bashrc` into organized alias files

## When NOT to use
- Environments where shell config is managed by configuration management (Ansible, Chef) — use those tools instead
- Shared servers with multiple users where one user's aliases conflict with others' expectations
- Scripts and pipelines that need portability across shells (zsh, fish, sh) — aliases are bash-specific
- Replacing proper scripts: complex multi-step operations belong in `~/bin/` scripts, not alias functions

## Where it fails / limitations
- Aliases are not inherited by subshells or scripts (only interactive shells load `.bash_aliases`)
- Tab completion doesn't carry through aliases unless explicitly wired with `complete -F`
- Function aliases that `cd` into directories don't work from non-interactive scripts
- Aliasing built-in commands (`alias echo=...`) can cause infinite recursion in edge cases
- Aliases defined in `.bash_aliases` are unavailable in systemd services, cron jobs, and SSH non-interactive sessions
- Changes to `.bash_aliases` require `source ~/.bash_aliases` to take effect in the current session — often forgotten

## Agentic workflow
Agents rarely create aliases directly, but they frequently read, audit, and extend `.bash_aliases` as part of server setup or dotfiles management tasks. An agent can scan the existing aliases for coverage gaps, add project-specific shortcuts, and validate that completions are wired correctly. When writing deployment scripts, an agent should check whether required aliases exist before assuming they work in non-interactive contexts.

### Recommended subagents
- `faion-sdd-executor-agent` — add project-specific aliases as part of an SDD onboarding task
- `nero-sdd-executor-agent` — extend NERO platform aliases when new services are added

### Prompt pattern
```
Audit ~/.bash_aliases on this server:
1. List all defined aliases and functions with one-line descriptions
2. Identify: (a) undocumented aliases, (b) aliases that shadow built-ins, (c) missing completions for git/docker/systemctl wrappers
3. Suggest additions for these missing categories: nginx reload, journalctl shortcuts, Docker compose workflow
Output as a markdown table with columns: alias, current-command, issue, suggested-fix
```

```
Add these project-specific aliases to ~/.bash_aliases for the faion-net project.
Place them under a "# === faion-net ===" section comment.
Aliases needed:
- `fn-logs` → `journalctl --user -u faion-net-api -f`
- `fn-restart` → `systemctl --user restart faion-net-api`
- `fn-status` → `systemctl --user status faion-net-api`
- `fn-deploy` → `bash ~/workspace/projects/faion-net/deploy-be.sh`
After writing, output: source ~/.bash_aliases
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `bash` | Shell that loads `.bash_aliases` | Built-in |
| `complete` | Shell completion configuration | Built-in bash |
| `type` | Check if name is alias, function, or command | Built-in bash |
| `alias` | Define and list aliases | Built-in bash |
| `unalias` | Remove an alias | Built-in bash |
| `source` / `.` | Reload alias file without restart | Built-in bash |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GNU Bash | OSS | Yes | Primary target for alias configuration |
| Oh My Bash | OSS | Partial | Alias plugin framework; adds complexity for solo use |
| Bash-it | OSS | Partial | Similar to Oh My Bash; large collection of pre-made aliases |
| zsh + Oh My Zsh | OSS | Partial | Richer alias ecosystem; not compatible with bash aliases directly |

## Templates & scripts
See `templates.md` for the full categorized `.bash_aliases` reference.

Inline: minimal production-ready alias file skeleton (≤45 lines):
```bash
# ~/.bash_aliases — categorized, commented, safe

# === Safety ===
alias rm="rm -i"
alias mv="mv -i"
alias cp="cp -i"

# === Navigation ===
alias ..="cd .."
alias ...="cd ../.."
alias ~="cd ~"
mkcd() { mkdir -p "$1" && cd "$1"; }

# === System ===
alias df="df -h"
alias du="du -sh"
alias free="free -h"
alias ports="ss -tulnp"
alias psg="ps aux | grep -v grep | grep"

# === Git ===
alias g="git"
alias gs="git status -sb"
alias gl="git log --oneline --graph --decorate -20"
alias gd="git diff"
alias gp="git push"

# === Docker ===
alias dps="docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
alias dlog="docker logs -f"
dk-stop-all() { docker stop $(docker ps -q) 2>/dev/null || echo "No containers running"; }

# === Systemd ===
alias scu="systemctl --user"
alias jcu="journalctl --user"
alias jcuf="journalctl --user -f"
scu-log() { journalctl --user -u "$1" -f; }

# === Reload ===
alias reload="source ~/.bash_aliases && echo 'Aliases reloaded'"
```

## Best practices
- Comment every non-obvious alias — aliases serve as self-documenting runbook entries
- Group by domain with `# === Section ===` headers; finding aliases in 200-line files requires structure
- Use `type -t <name>` to check if an alias already exists before overwriting it; shadowing unexpected built-ins causes hard-to-debug behavior
- Wire tab completion for wrapper aliases: `alias g="git" && complete -o default -o nospace -F _git g`
- Put complex multi-line logic in `~/bin/<script>.sh` and create a simple alias to it — not in alias functions
- Version-control `.bash_aliases` in dotfiles repo (see dotfiles-management) so it's reproducible across servers
- Use `\command` or `command <name>` to bypass aliases when you need the raw binary in a script

## AI-agent gotchas
- Aliases defined in `.bash_aliases` are NOT available when an agent runs bash scripts via SSH non-interactive mode — the script must source explicitly or use full commands
- Agent must not assume `ll`, `g`, `dps` exist on a fresh server; always check with `type <name>` before using
- Appending to `.bash_aliases` without checking for duplicate definitions creates silent conflicts — agent should grep before appending
- Functions that `cd` in `.bash_aliases` only work in interactive shells; agent-run bash scripts do not inherit the directory change
- When an agent sources `.bash_aliases` inside a script, the parent shell's `$PS1` is unset, which some tools use to detect interactive mode

## References
- [Bash manual: aliases](https://www.gnu.org/software/bash/manual/html_node/Aliases.html)
- [Bash manual: programmable completion](https://www.gnu.org/software/bash/manual/html_node/Programmable-Completion.html)
- [Bash manual: shell functions](https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html)
