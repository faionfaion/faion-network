# Dotfiles Management Examples

## Example 1: NERO Server Dotfiles

Complete dotfiles setup for the NERO Hetzner CX53 server.

### Repository Structure

```
~/dotfiles/
├── bash/
│   ├── .bashrc
│   └── .bashrc.d/
│       ├── aliases.sh
│       ├── history.sh
│       ├── path.sh
│       └── prompt.sh
├── git/
│   ├── .gitconfig
│   └── .gitignore_global
├── tmux/
│   └── .tmux.conf
├── vim/
│   └── .vimrc
├── ssh/
│   └── .ssh/
│       └── config
├── scripts/
│   └── .local/
│       └── bin/
│           ├── deploy
│           ├── health
│           └── status
├── machine-server/
│   └── .bashrc.d/
│       └── server.sh
├── bootstrap.sh
├── .gitignore
└── README.md
```

### Setup on the Server

```bash
# Clone dotfiles
$ git clone git@github.com:faionfaion/dotfiles.git ~/dotfiles

# Install stow
$ sudo apt install -y stow

# Backup existing files
$ mv ~/.bashrc ~/.bashrc.backup
$ mv ~/.gitconfig ~/.gitconfig.backup 2>/dev/null

# Create .bashrc.d directory
$ mkdir -p ~/.bashrc.d

# Stow all packages
$ cd ~/dotfiles
$ stow bash git tmux vim ssh scripts machine-server

# Verify symlinks
$ ls -la ~/ | grep "\->"
.bashrc -> dotfiles/bash/.bashrc
.gitconfig -> dotfiles/git/.gitconfig
.gitignore_global -> dotfiles/git/.gitignore_global
.tmux.conf -> dotfiles/tmux/.tmux.conf
.vimrc -> dotfiles/vim/.vimrc

$ ls -la ~/.bashrc.d/
aliases.sh -> ../../dotfiles/bash/.bashrc.d/aliases.sh
history.sh -> ../../dotfiles/bash/.bashrc.d/history.sh
path.sh -> ../../dotfiles/bash/.bashrc.d/path.sh
prompt.sh -> ../../dotfiles/bash/.bashrc.d/prompt.sh
server.sh -> ../../dotfiles/machine-server/.bashrc.d/server.sh

$ ls -la ~/.ssh/config
.ssh/config -> ../dotfiles/ssh/.ssh/config

# Reload shell
$ source ~/.bashrc
nero@nero-hetzner:~$
```

### Server-Specific Aliases in Action

```bash
# Quick deploy (from server.sh)
$ deploy nero-core
=== Deploying nero-core (systemd) ===
...

# Health check shortcut
$ health
=== Health Check: 2026-03-21T10:00:00Z ===
[OK]   nero-core (systemd)
[OK]   nero-channel-web (HTTP /health)
...

# Server status
$ status
=== Memory ===
              total        used        free
Mem:           30Gi       8.2Gi        18Gi
=== Disk ===
/dev/sda1       310G   12G  283G   4% /
=== Services ===
nero-core.service         active running
nero-channel-web.service  active running
...
```

### Utility Scripts in .local/bin/

```bash
# ~/dotfiles/scripts/.local/bin/deploy
#!/bin/bash
# Quick deploy shortcut
bash ~/workspace/deploy/deploy.sh "$@"

# ~/dotfiles/scripts/.local/bin/health
#!/bin/bash
# Quick health check
bash /srv/nero/health-check.sh "$@"

# ~/dotfiles/scripts/.local/bin/status
#!/bin/bash
# Quick status
bash ~/workspace/deploy/status.sh "$@"
```

```bash
$ chmod +x ~/dotfiles/scripts/.local/bin/*
$ stow -R scripts
```

## Example 2: Syncing Dotfiles Between Machines

Making a change on the server, syncing to workstation.

### Edit on Server

```bash
# On server: add a new alias
$ vim ~/dotfiles/bash/.bashrc.d/aliases.sh
# Add: alias dlog='docker logs --tail 50 -f'

# Commit and push
$ cd ~/dotfiles
$ git add -A
$ git commit -m "chore: add docker log alias"
$ git push
```

### Pull on Workstation

```bash
# On workstation
$ cd ~/dotfiles
$ git pull
remote: Enumerating objects: 7, done.
...
Fast-forward
 bash/.bashrc.d/aliases.sh | 1 +

# Restow (in case any paths changed)
$ stow -R bash

# Reload shell
$ source ~/.bashrc
```

### Machine-Specific: No Conflict

Server aliases (like `deploy`, `health`) live in `machine-server/.bashrc.d/server.sh` and are only stowed on the server. Workstation-specific config lives in `machine-workstation/.bashrc.d/workstation.sh` and is only stowed on the workstation.

```bash
# Server
$ stow machine-server
# Creates ~/.bashrc.d/server.sh

# Workstation
$ stow machine-workstation
# Creates ~/.bashrc.d/workstation.sh
# Server aliases are NOT present
```

## Example 3: Adopting Existing Configs into Stow

You already have a `.tmux.conf` that you've been editing directly. Moving it into the dotfiles repo.

### Using stow --adopt

```bash
$ ls -la ~/.tmux.conf
-rw-r--r-- 1 nero nero 1234 Mar 15 .tmux.conf   # Real file, not symlink

# stow --adopt moves the file INTO the package and creates the symlink
$ cd ~/dotfiles
$ mkdir -p tmux
$ stow --adopt tmux

# Now check
$ ls -la ~/.tmux.conf
lrwxrwxrwx 1 nero nero 28 Mar 21 .tmux.conf -> dotfiles/tmux/.tmux.conf

# IMPORTANT: review what was adopted
$ cd ~/dotfiles
$ git diff
# Shows the content that was moved in
# Review to make sure it looks right

$ git add tmux/.tmux.conf
$ git commit -m "chore: adopt existing tmux config"
```

## Example 4: Claude Code Settings in Dotfiles

Managing Claude Code settings.json as part of dotfiles.

### Structure

```
~/dotfiles/claude/
└── .claude/
    └── settings.json
```

### settings.json (Safe to Version Control)

```json
{
    "hooks": {
        "PostToolUse": [
            {
                "type": "command",
                "command": "bash ~/.claude/hooks/post-edit-format.sh",
                "matcher": "Edit",
                "timeout": 10000
            }
        ],
        "UserPromptSubmit": [
            {
                "type": "command",
                "command": "bash ~/.claude/hooks/tmux-save.sh",
                "timeout": 5000
            }
        ]
    }
}
```

### Stow It

```bash
$ cd ~/dotfiles
$ stow claude

$ ls -la ~/.claude/settings.json
lrwxrwxrwx 1 nero nero 42 Mar 21 .claude/settings.json -> ../dotfiles/claude/.claude/settings.json
```

### What NOT to Include

```gitignore
# In ~/dotfiles/.gitignore
claude/.claude/projects/     # May contain project-specific secrets
claude/.claude/settings.local.json  # Local overrides
```

## Example 5: Bootstrap on a Fresh Server

First-time dotfiles installation during server bootstrap.

```bash
# After server bootstrap (user created, SSH working)
$ ssh nero@new-server.example.com

# Install prerequisites
$ sudo apt install -y git stow

# Clone dotfiles
$ git clone git@github.com:faionfaion/dotfiles.git ~/dotfiles

# Run bootstrap
$ cd ~/dotfiles
$ bash bootstrap.sh

=== Dotfiles Bootstrap ===
Backed up .bashrc to /home/nero/.dotfiles-backup-20260321/
Stowing packages...
  Stowed: bash
  Stowed: git
  Stowed: tmux
  Stowed: vim
  Stowed: ssh
  Stowed: scripts
  Stowed: machine-server

=== Bootstrap complete (type: server) ===
Restart your shell: source ~/.bashrc

$ source ~/.bashrc
nero@new-server:~$

# Everything works: aliases, prompt, git config, tmux, vim
$ g st    # git status alias works
$ ll      # ls -alF works
$ tmux    # tmux config applied
```
