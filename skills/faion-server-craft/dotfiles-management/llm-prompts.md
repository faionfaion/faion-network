# Dotfiles Management LLM Prompts

## Setup Dotfiles Repository

```
Help me create a dotfiles repository with GNU stow.

Current configs I want to manage:
- ~/.bashrc (with aliases and PATH)
- ~/.gitconfig
- ~/.tmux.conf
- ~/.vimrc
- ~/.ssh/config (NOT keys)
- Custom scripts in ~/.local/bin/

Machines:
- VPS server (Ubuntu 24.04, headless)
- Workstation ([OS]) (optional)

Requirements:
- Modular .bashrc (split into .bashrc.d/ files)
- Machine-specific overrides (server vs workstation)
- Never commit secrets or private keys
- Bootstrap script for new machines
- git + GNU stow workflow

Provide:
1. Repository directory structure
2. Each config file content
3. .gitignore for the dotfiles repo
4. bootstrap.sh script
5. install.sh for re-stowing after git pull
6. Step-by-step setup commands
7. How to add a new config file in the future
```

## Migrate Existing Configs to Stow

```
Help me migrate my existing dotfiles into a GNU stow managed repository.

I currently have these files directly in $HOME:
[LIST, e.g.:
- ~/.bashrc (1200 lines, accumulated over years)
- ~/.gitconfig
- ~/.tmux.conf
- ~/.vimrc
- ~/.ssh/config
]

Issues:
- .bashrc is a mess (needs cleanup and modularization)
- Some configs have hardcoded paths
- Some have machine-specific settings mixed in

Please:
1. How to use stow --adopt to move files into the repo
2. How to split a monolithic .bashrc into modular .bashrc.d/ files
3. How to separate machine-specific settings
4. What to review before committing (security audit)
5. How to handle stow conflicts (existing files vs symlinks)
6. How to test that everything works after migration
```

## Dotfiles Sync Strategy

```
Design a sync strategy for dotfiles across my machines.

Machines:
[LIST with descriptions, e.g.:
- VPS server: Ubuntu 24.04, headless, production
- Dev workstation: [OS], GUI, development
- Laptop: [OS], travel
]

Differences between machines:
- Server needs: systemctl aliases, deploy shortcuts, no GUI
- Workstation needs: editor config (VS Code), GUI tools, SSH agent
- Common: git config, tmux, vim, shell basics

Questions:
1. How to structure machine-specific overrides?
2. Git branching vs conditional sourcing vs stow packages?
3. How to handle sensitive configs (SSH config with IPs)?
4. How to test changes on one machine before syncing to all?
5. How to handle conflicts (same file changed on two machines)?

Provide:
- Recommended approach with rationale
- Directory structure
- Sync workflow (edit, commit, pull on other machines)
- What to do when git pull has conflicts
```

## Organize .bashrc

```
Help me organize my messy .bashrc into a clean, modular structure.

Current .bashrc: [PASTE or describe what's in it]
Length: [NUMBER] lines

I want it split into:
1. ~/.bashrc (minimal: source .bashrc.d/ files, tool hooks)
2. ~/.bashrc.d/aliases.sh (shell aliases)
3. ~/.bashrc.d/history.sh (history configuration)
4. ~/.bashrc.d/path.sh (PATH additions)
5. ~/.bashrc.d/prompt.sh (PS1 prompt)
6. ~/.bashrc.d/functions.sh (custom functions, if any)

Additional requirements:
- mise and direnv hooks in correct order
- Machine-specific file (server.sh or workstation.sh)
- Clean, well-commented
- No duplicate or conflicting settings

Please:
1. Analyze my current .bashrc
2. Propose the split into files
3. Write each file
4. Main .bashrc that sources .bashrc.d/
5. Verify: what should `source ~/.bashrc` do?
```

## Add New Tool Config to Dotfiles

```
Add a new tool's configuration to my existing dotfiles.

Tool: [TOOL NAME, e.g., "starship prompt", "lazygit", "bat"]
Config file location: [WHERE IT LIVES, e.g., ~/.config/starship.toml]
Dotfiles repo: [PATH, e.g., ~/dotfiles/]

Current stow packages:
[LIST, e.g.: bash, git, tmux, vim, ssh, scripts]

Please:
1. Create the stow package directory structure
2. Write a good default config for the tool
3. Stow commands to install
4. Update .bashrc if shell integration needed
5. Test commands to verify it works
```

## Dotfiles Security Audit

```
Audit my dotfiles repository for security issues before I push to GitHub.

Repository: [PATH]

Check for:
1. SSH private keys (any file starting with id_)
2. Known hosts file
3. Hardcoded passwords or tokens in configs
4. API keys in shell history references
5. Machine-specific IPs or hostnames that shouldn't be public
6. .env files or references to secret files
7. GPG keys
8. Browser or application tokens

For each issue found:
- File and line
- Risk level (critical/warning/info)
- How to fix (remove, redact, add to .gitignore)
- If already committed: how to remove from git history

Provide:
- grep commands to search for common patterns
- Checklist of things to review manually
- .gitignore additions to prevent future leaks
```
