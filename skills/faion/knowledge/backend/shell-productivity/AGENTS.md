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
| `templates/shell-productivity.md` | Human-readable audit trail. |
| `templates/install-cli-tools.sh` | Idempotent installer for the chosen tool list. |
| `templates/fzf-config.sh` | fzf key-bindings + completion source block. |
| `templates/starship.toml` | starship preset with concise prompt. |

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
