# Setup Dotfiles Repository Checklist

## Repository Setup

- [ ] Create dotfiles directory: `mkdir ~/dotfiles && cd ~/dotfiles`
- [ ] Initialize git repo: `git init`
- [ ] Create .gitignore (exclude secrets, keys, history)
- [ ] Create README.md with setup instructions
- [ ] Create bootstrap.sh script
- [ ] Add remote: `git remote add origin git@github.com:USER/dotfiles.git`

## Install GNU stow

- [ ] Install: `sudo apt install stow`
- [ ] Verify: `stow --version`
- [ ] Understand stow directory = dotfiles repo
- [ ] Understand target = $HOME (parent of stow directory)

## Create Packages

### bash/
- [ ] Move .bashrc to `~/dotfiles/bash/.bashrc`
- [ ] Move .bash_profile to `~/dotfiles/bash/.bash_profile`
- [ ] Create .bash_aliases if using aliases
- [ ] Create .bashrc.d/ for modular configs
- [ ] Add `source ~/.bashrc.d/*.sh` loop to .bashrc
- [ ] Test: `stow bash && source ~/.bashrc`

### git/
- [ ] Move .gitconfig to `~/dotfiles/git/.gitconfig`
- [ ] Create .gitignore_global
- [ ] Reference global gitignore in .gitconfig
- [ ] Test: `stow git && git config --list`

### tmux/
- [ ] Move .tmux.conf to `~/dotfiles/tmux/.tmux.conf`
- [ ] Test: `stow tmux && tmux source ~/.tmux.conf`

### vim/
- [ ] Move .vimrc to `~/dotfiles/vim/.vimrc`
- [ ] Move .vim/ directory if exists
- [ ] Test: `stow vim && vim --version`

### ssh/
- [ ] Create `~/dotfiles/ssh/.ssh/config`
- [ ] Configure Host entries for common servers
- [ ] Do NOT include private keys
- [ ] Do NOT include known_hosts
- [ ] Do NOT include authorized_keys
- [ ] Test: `stow ssh && ssh -T git@github.com`

### scripts/
- [ ] Create `~/dotfiles/scripts/.local/bin/`
- [ ] Add utility scripts
- [ ] Ensure .bashrc adds `~/.local/bin` to PATH
- [ ] Test: `stow scripts && which <script-name>`

## Machine-Specific Overrides

- [ ] Create `machine-server/` package
- [ ] Create `machine-workstation/` package
- [ ] Add machine detection to bootstrap.sh
- [ ] Server-specific: aliases for systemctl, journalctl
- [ ] Workstation-specific: editor, GUI settings
- [ ] Test: `stow machine-server` on server

## Security Review

- [ ] .gitignore blocks SSH private keys
- [ ] .gitignore blocks .bash_history
- [ ] .gitignore blocks .env files
- [ ] .gitignore blocks .gnupg/
- [ ] .gitignore blocks credentials/tokens
- [ ] No secrets in any committed file
- [ ] `git status` shows no sensitive files

## Stow All Packages

- [ ] Backup existing dotfiles: `mv ~/.bashrc ~/.bashrc.backup`
- [ ] Stow base packages: `stow bash git tmux vim ssh scripts`
- [ ] Stow machine-specific: `stow machine-<type>`
- [ ] Verify symlinks: `ls -la ~/ | grep "\->"`
- [ ] Source shell: `source ~/.bashrc`
- [ ] Verify everything works

## Bootstrap Script

- [ ] Script clones repo if not exists
- [ ] Script installs stow
- [ ] Script backs up existing dotfiles
- [ ] Script stows all base packages
- [ ] Script detects machine type
- [ ] Script stows machine-specific package
- [ ] Script prints success message
- [ ] Test on a fresh account/machine

## Initial Commit

- [ ] `git add -A`
- [ ] `git status` - verify only safe files
- [ ] `git commit -m "init: dotfiles with stow"`
- [ ] `git push -u origin main`

## Sync Workflow

- [ ] After editing config: `cd ~/dotfiles && git add -A && git commit && git push`
- [ ] On other machine: `cd ~/dotfiles && git pull && stow -R <package>`
- [ ] Workflow documented in README.md
