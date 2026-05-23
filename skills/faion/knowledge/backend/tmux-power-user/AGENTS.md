# tmux Power User

## Summary

**One-sentence:** Generates a tmux config + named-session script + plugin set (resurrect, continuum, yank) for a multi-host operator — gated by versioned dotfiles.

**One-paragraph:** Solo operators live in tmux: persistent sessions across SSH disconnects, named projects, copy-mode that works on macOS and Linux. This methodology pins a tmux.conf (TPM plugin loader, prefix C-a, mouse on, 100k history), a session-launcher script, and the plugin set. Output: a TmuxPlan + tmux.conf.

**Ефективно для:**

- SSH operator who reconnects to the same VPS dozens of times daily.
- Multi-project workflows where each project deserves a named session.
- Long-running interactive work (claude code, repl, log tailing) that must survive disconnect.
- macOS + Linux operators sharing the same tmux.conf.

## Applies If (ALL must hold)

- Operator runs ≥3 tmux sessions/day.
- SSH connections drop occasionally and work must survive.
- Multiple projects on one host needing per-project sessions.
- Standardising tmux across personal + remote machines.

## Skip If (ANY kills it)

- Operator uses a different terminal multiplexer (zellij, screen) by preference.
- Single-session usage with no copy-mode needs.
- Locked-down env where plugins can't be installed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Operator prefix preference | C-a or C-b | operator |
| Plugin allow-list | list of TPM plugins | TmuxPlan |
| OS list | macos / linux | operator hosts |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| dotfiles-management | tmux.conf is part of the dotfiles repo. |
| shell-productivity | Shell prompt + history coordinate with tmux defaults. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-prefix-not-c-b, r2-tpm-managed-plugins, r3-large-history, r4-named-owner, r5-os-conditional-copy | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the tmux Power User artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: default-prefix-c-b, history-1024-loses, copy-mode-platform-mismatch, plugin-versions-floating | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-tmux-conf` | sonnet | Per-operator key-binding tweaks. |
| `render-session-script` | haiku | Mechanical template fill. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tmux-power-user.json` | TmuxPlan JSON skeleton. |
| `templates/tmux-power-user.md` | Human-readable audit trail + keybinding cheatsheet. |
| `templates/tmux.conf` | Reference tmux.conf with prefix C-a, mouse on, 100k history, TPM. |
| `templates/tmux-session.sh` | Launcher for a named project session with split layout. |
| `templates/tmux-system.sh` | System tmux session (monitoring, logs). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tmux-power-user.py` | Validate TmuxPlan JSON against the schema. | Pre-apply on each host. |

## Related

- [[dotfiles-management]]
- [[shell-productivity]]
- [[bash-aliases]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
