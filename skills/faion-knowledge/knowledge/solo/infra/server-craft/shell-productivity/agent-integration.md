# Agent Integration — Shell Productivity

## When to use
- Setting up a new Ubuntu VPS where the default shell tools make daily admin slower than necessary
- Server rebuild — restoring the developer's modern tool stack alongside dotfiles
- Replacing `grep`/`find`/`cat` with faster alternatives in admin and monitoring scripts
- Improving agent-generated shell pipelines by using tools with better output formats
- Auditing which tools are installed before writing scripts that depend on them

## When NOT to use
- Minimal containers or CI environments where image size matters (stick to POSIX tools)
- Scripts that must run on arbitrary servers without knowing what tools are installed (write POSIX sh with fallbacks)
- Environments with strict package policy (air-gapped, compliance-hardened) where adding external apt repos is forbidden
- Replacing tools in scripts checked into shared repos — others may not have the same tools installed

## Where it fails / limitations
- `bat` is installed as `batcat` on Ubuntu 22.04/24.04 — scripts using `bat` directly fail unless symlink or alias exists
- `fd` is installed as `fdfind` on Ubuntu — same problem; alias or symlink required
- `eza` requires a third-party apt repository (gierens); not in Ubuntu main repos
- `delta` and `dust` require downloading `.deb` from GitHub releases — version pinning is manual
- `starship` prompt initialization adds ~50ms to shell startup on slow filesystems or large git repos
- `zoxide` database (`~/.local/share/zoxide/db.zo`) is per-machine; doesn't sync across servers
- `fzf` `Ctrl+R` binding conflicts with some terminal emulators that intercept that key

## Agentic workflow
An agent can run the full tool installation sequence as part of server bootstrap, then verify all tools are present via the check loop from README.md. When writing shell pipelines for other tasks, agents should prefer these tools for better output: `rg` over `grep` (faster, colored, gitignore-aware), `fd` over `find` (simpler syntax, gitignore-aware), `bat` over `cat` (structured output for review). However, agent-generated scripts for production use should still prefer POSIX tools unless the target server is known to have the modern alternatives installed.

### Recommended subagents
- `faion-sdd-executor-agent` — install productivity tools as part of server-init SDD task sequence
- `nero-sdd-executor-agent` — verify tool availability before writing monitoring/admin scripts

### Prompt pattern
```
Install the modern CLI tool stack on this Ubuntu 24.04 server:
1. apt install: bat fd-find fzf ripgrep btop duf
2. Create symlinks: ln -sf /usr/bin/batcat /usr/local/bin/bat && ln -sf /usr/bin/fdfind /usr/local/bin/fd
3. Install eza from gierens repo (see templates.md for commands)
4. Install starship: curl -sS https://starship.rs/install.sh | sh -s -- --yes
5. Install zoxide: curl -sSfL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | sh
6. Add to ~/.bashrc: eval "$(starship init bash)" and eval "$(zoxide init bash)"
7. Verify: for tool in bat fd fzf rg eza starship zoxide btop duf; do command -v "$tool" && echo "OK $tool" || echo "MISSING $tool"; done
```

```
Write a log investigation pipeline using modern tools to analyze the last 24h of nginx errors:
- Use: journalctl -u nginx --since "24 hours ago" -o short-iso --no-pager
- Pipe to: rg "error|crit|emerg" (case-insensitive)
- Count by error pattern: sort | uniq -c | sort -rn | head -20
- If bat is available, pipe final output through bat for syntax highlighting
Fall back to grep if rg is not installed.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `bat` | Syntax-highlighted cat/less | `apt install bat` + symlink |
| `fd` (`fdfind`) | Fast find with gitignore support | `apt install fd-find` + symlink |
| `fzf` | Fuzzy finder for files, history, processes | `apt install fzf` |
| `ripgrep` (`rg`) | Fast grep with gitignore, colored output | `apt install ripgrep` |
| `eza` | Modern ls with git status, icons, tree | Third-party apt repo; [eza.rocks](https://eza.rocks/) |
| `delta` | Side-by-side git diff with syntax highlight | GitHub releases `.deb` |
| `starship` | Fast cross-shell prompt with git info | `curl -sS https://starship.rs/install.sh \| sh` |
| `zoxide` | Frecency-based smart `cd` | `curl` install script |
| `btop` | Interactive system monitor (beautiful) | `apt install btop` |
| `duf` | Colored disk usage summary | `apt install duf` |
| `dust` | Directory size tree | GitHub releases `.deb` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| starship.rs | OSS | Yes — shell integration only | Config in `~/.config/starship.toml`; no daemon |
| zoxide | OSS | Yes — CLI only | Database at `~/.local/share/zoxide/db.zo` |
| atuin | OSS | Partial | Shell history sync with encryption; cloud or self-hosted |
| nix | OSS | Yes | Reproducible tool installation across systems; steep learning curve |
| mise | OSS | Yes | Manages tool versions (node, python, etc.); complements this stack |

## Templates & scripts
See `templates.md` for full installation script and `.bashrc` integration snippets.

Inline: tool verification script (≤20 lines):
```bash
#!/bin/bash
# verify-shell-tools.sh — check modern CLI tool installation
tools=(bat fd fzf rg eza delta starship zoxide btop duf dust)
missing=()
for tool in "${tools[@]}"; do
    if command -v "$tool" &>/dev/null; then
        echo "OK   $tool $(command -v "$tool")"
    else
        echo "MISS $tool"
        missing+=("$tool")
    fi
done
echo ""
if [ ${#missing[@]} -eq 0 ]; then
    echo "All tools present"
else
    echo "Missing ${#missing[@]} tools: ${missing[*]}"
    exit 1
fi
```

## Best practices
- Create symlinks immediately after installing `bat`/`fd` on Ubuntu so scripts don't need to use `batcat`/`fdfind`
- Configure `FZF_DEFAULT_COMMAND` to use `fd` instead of `find` — respects `.gitignore` and is 3-10x faster on large repos
- Wire `bat` as the `fzf` preview command for `Ctrl+T` file search: `FZF_CTRL_T_OPTS="--preview 'bat --color=always {}'"` 
- Set `delta` only as the git pager, not the system default pager — `core.pager = delta` in `.gitconfig` only
- Configure `starship` to timeout git status on large repos: `[git_status] disabled = false` + `scan_timeout = 10`
- Add tool presence check at the top of admin scripts that use modern tools; fall back to POSIX equivalents gracefully
- Keep tool versions pinned in dotfiles (or note the versions) so rebuilds produce identical environments

## AI-agent gotchas
- Agent must check `command -v bat` vs `command -v batcat` before using either — Ubuntu package name differs from binary name
- `fzf` is interactive by default; using it in agent-run scripts without `--filter` or `--select-1` causes the agent to hang waiting for user input
- `rg` respects `.gitignore` by default — this is usually desirable but can miss files the agent expects to find; use `--no-ignore` to override
- `delta` as a git pager breaks agent pipelines that parse `git diff` output — agent should use `GIT_PAGER=cat git diff` to get plain text
- `starship` writes to stderr for some warnings; agent pipelines that capture stderr may see noise
- `zoxide` `zi` command is interactive (fzf-based); agent must use `z <query>` (non-interactive) form or it hangs

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
- [atuin — shell history sync](https://atuin.sh/)
