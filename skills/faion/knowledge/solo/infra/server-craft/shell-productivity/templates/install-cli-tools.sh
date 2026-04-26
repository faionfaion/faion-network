#!/bin/bash
# install-cli-tools.sh — Idempotent install of modern CLI tools on Ubuntu 24.04
#
# Tools: bat, fd, fzf, ripgrep, eza, delta, starship, zoxide, btop, duf, dust
# Run as a user with sudo; does not require root directly.

set -euo pipefail

echo "=== Installing Modern CLI Tools ==="

# apt-available tools
echo "--- apt packages ---"
sudo apt-get update -qq
sudo apt-get install -y bat fd-find fzf ripgrep btop duf

# Fix Ubuntu naming conflicts (batcat -> bat, fdfind -> fd)
[ -x /usr/bin/batcat ] && sudo ln -sf /usr/bin/batcat /usr/local/bin/bat || true
[ -x /usr/bin/fdfind ] && sudo ln -sf /usr/bin/fdfind /usr/local/bin/fd || true

# eza (better ls)
echo "--- eza ---"
if ! command -v eza &>/dev/null; then
    sudo mkdir -p /etc/apt/keyrings
    wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc \
        | sudo gpg --dearmor -o /etc/apt/keyrings/gierens.gpg 2>/dev/null
    echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" \
        | sudo tee /etc/apt/sources.list.d/gierens.list >/dev/null
    sudo apt-get update -qq && sudo apt-get install -y eza
    echo "  Installed eza"
else
    echo "  Already installed: eza"
fi

# delta (better git diff)
echo "--- delta ---"
if ! command -v delta &>/dev/null; then
    DELTA_VER="0.18.2"
    wget -q "https://github.com/dandavison/delta/releases/download/${DELTA_VER}/git-delta_${DELTA_VER}_amd64.deb" -O /tmp/delta.deb
    sudo dpkg -i /tmp/delta.deb && rm /tmp/delta.deb
    echo "  Installed delta $DELTA_VER"
else
    echo "  Already installed: delta"
fi

# starship (prompt)
echo "--- starship ---"
if ! command -v starship &>/dev/null; then
    curl -sS https://starship.rs/install.sh | sh -s -- -y
    echo "  Installed starship"
else
    echo "  Already installed: starship"
fi

# zoxide (smart cd)
echo "--- zoxide ---"
if ! command -v zoxide &>/dev/null; then
    curl -sSfL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | sh
    echo "  Installed zoxide"
else
    echo "  Already installed: zoxide"
fi

# dust (better du)
echo "--- dust ---"
if ! command -v dust &>/dev/null; then
    DUST_VER="1.1.1"
    wget -q "https://github.com/bootandy/dust/releases/download/v${DUST_VER}/du-dust_${DUST_VER}-1_amd64.deb" -O /tmp/dust.deb
    sudo dpkg -i /tmp/dust.deb && rm /tmp/dust.deb
    echo "  Installed dust $DUST_VER"
else
    echo "  Already installed: dust"
fi

echo ""
echo "=== Verification ==="
for tool in bat fd fzf rg eza delta starship zoxide btop duf dust; do
    if command -v "$tool" &>/dev/null; then
        printf "  OK      %-12s %s\n" "$tool" "$(command -v "$tool")"
    else
        printf "  MISSING %-12s\n" "$tool"
    fi
done

echo ""
echo "=== Next Steps ==="
echo "1. Add to ~/.bashrc:"
echo "   eval \"\$(fzf --bash)\""
echo "   eval \"\$(starship init bash)\""
echo "   eval \"\$(zoxide init bash)\""
echo "2. Copy templates/starship.toml to ~/.config/starship.toml"
echo "3. Add templates/fzf-config.sh block to ~/.bashrc"
echo "4. Add delta section to ~/.gitconfig"
echo "5. Add tool aliases to ~/.bash_aliases"
