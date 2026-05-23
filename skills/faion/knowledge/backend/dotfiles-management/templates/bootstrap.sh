#!/bin/bash
# bootstrap.sh — Install dotfiles on a new machine using GNU stow
#
# Usage: bash bootstrap.sh [repo-url]
#   repo-url defaults to git@github.com:USER/dotfiles.git

set -euo pipefail

DOTFILES_DIR="$HOME/dotfiles"
REPO_URL="${1:-git@github.com:USER/dotfiles.git}"

echo "=== Dotfiles Bootstrap ==="

# Clone if not present
if [ ! -d "$DOTFILES_DIR" ]; then
    echo "Cloning dotfiles from $REPO_URL..."
    git clone "$REPO_URL" "$DOTFILES_DIR"
fi

cd "$DOTFILES_DIR"

# Install stow
if ! command -v stow &>/dev/null; then
    echo "Installing stow..."
    sudo apt install -y stow
fi

# Create .bashrc.d directory (needed for modular config)
mkdir -p "$HOME/.bashrc.d"

# Backup existing dotfiles that would conflict
BACKUP_DIR="$HOME/.dotfiles-backup-$(date +%Y%m%d)"
for f in .bashrc .bash_profile .gitconfig .tmux.conf .vimrc; do
    if [ -f "$HOME/$f" ] && [ ! -L "$HOME/$f" ]; then
        mkdir -p "$BACKUP_DIR"
        mv "$HOME/$f" "$BACKUP_DIR/"
        echo "Backed up ~/$f → $BACKUP_DIR/$f"
    fi
done

# Stow base packages
echo ""
echo "Stowing base packages..."
for pkg in bash git tmux vim ssh scripts; do
    if [ -d "$DOTFILES_DIR/$pkg" ]; then
        stow -v "$pkg" 2>&1 | grep -v "^$" || true
        echo "  OK: $pkg"
    fi
done

# Detect machine type and stow machine-specific overrides
if [ -n "${DISPLAY:-}" ] || command -v code &>/dev/null; then
    MACHINE_TYPE="workstation"
else
    MACHINE_TYPE="server"
fi

if [ -d "$DOTFILES_DIR/machine-$MACHINE_TYPE" ]; then
    stow -v "machine-$MACHINE_TYPE" 2>&1 | grep -v "^$" || true
    echo "  OK: machine-$MACHINE_TYPE"
fi

echo ""
echo "=== Bootstrap complete (type: $MACHINE_TYPE) ==="
echo "Restart your shell or run: source ~/.bashrc"
