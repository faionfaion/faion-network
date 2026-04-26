# Shell Productivity Checklist

Step-by-step checklist for installing and configuring modern CLI tools on Ubuntu 24.04.

## Phase 1: Core Tools (apt)

- [ ] **Install from apt**
  ```bash
  sudo apt update
  sudo apt install -y bat fd-find fzf ripgrep btop duf
  ```

- [ ] **Create symlinks** (Ubuntu naming conflicts)
  ```bash
  sudo ln -sf /usr/bin/batcat /usr/local/bin/bat
  sudo ln -sf /usr/bin/fdfind /usr/local/bin/fd
  ```

- [ ] **Verify**
  ```bash
  bat --version
  fd --version
  fzf --version
  rg --version
  btop --version
  duf --version
  ```

## Phase 2: Additional Tools (GitHub releases)

- [ ] **Install eza** (better ls)
  ```bash
  sudo apt install -y gpg
  sudo mkdir -p /etc/apt/keyrings
  wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc | \
      sudo gpg --dearmor -o /etc/apt/keyrings/gierens.gpg
  echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" | \
      sudo tee /etc/apt/sources.list.d/gierens.list
  sudo apt update && sudo apt install -y eza
  ```

- [ ] **Install delta** (better git diff)
  ```bash
  DELTA_VER="0.18.2"
  wget -q "https://github.com/dandavison/delta/releases/download/${DELTA_VER}/git-delta_${DELTA_VER}_amd64.deb"
  sudo dpkg -i "git-delta_${DELTA_VER}_amd64.deb" && rm "git-delta_${DELTA_VER}_amd64.deb"
  ```

- [ ] **Install starship** (prompt)
  ```bash
  curl -sS https://starship.rs/install.sh | sh -s -- -y
  ```

- [ ] **Install zoxide** (smart cd)
  ```bash
  curl -sSfL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | sh
  ```

- [ ] **Install dust** (better du)
  ```bash
  DUST_VER="1.1.1"
  wget -q "https://github.com/bootandy/dust/releases/download/v${DUST_VER}/du-dust_${DUST_VER}-1_amd64.deb"
  sudo dpkg -i "du-dust_${DUST_VER}-1_amd64.deb" && rm "du-dust_${DUST_VER}-1_amd64.deb"
  ```

## Phase 3: Shell Configuration

- [ ] **Add to ~/.bashrc**
  ```bash
  cat >> ~/.bashrc << 'BASHEOF'

  # --- Modern CLI Tools ---

  # fzf
  eval "$(fzf --bash)"
  export FZF_DEFAULT_COMMAND='fd --type f --hidden --exclude .git'
  export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
  export FZF_CTRL_T_OPTS="--preview 'bat --color=always --style=numbers --line-range=:200 {}'"
  export FZF_ALT_C_COMMAND='fd --type d --hidden --exclude .git'
  export FZF_ALT_C_OPTS="--preview 'eza --tree --level=2 --color=always {} 2>/dev/null'"

  # bat
  export BAT_THEME="TwoDark"
  export BAT_STYLE="numbers,changes,header"

  # starship prompt
  eval "$(starship init bash)"

  # zoxide (smart cd)
  eval "$(zoxide init bash)"
  BASHEOF
  ```

- [ ] **Source bashrc**
  ```bash
  source ~/.bashrc
  ```

## Phase 4: Git Integration

- [ ] **Configure delta as git pager**
  ```bash
  git config --global core.pager delta
  git config --global interactive.diffFilter "delta --color-only"
  git config --global delta.navigate true
  git config --global delta.side-by-side true
  git config --global delta.line-numbers true
  git config --global delta.syntax-theme TwoDark
  git config --global merge.conflictstyle diff3
  git config --global diff.colorMoved default
  ```

## Phase 5: Starship Prompt

- [ ] **Create starship config**
  ```bash
  mkdir -p ~/.config
  cat > ~/.config/starship.toml << 'STAR'
  # Minimal, fast prompt
  format = "$directory$git_branch$git_status$character"

  [directory]
  truncation_length = 3

  [git_branch]
  format = " [$branch]($style) "
  style = "bold purple"

  [git_status]
  format = '([$all_status$ahead_behind]($style) )'

  [character]
  success_symbol = "[>](bold green)"
  error_symbol = "[>](bold red)"
  STAR
  ```

## Phase 6: Aliases

- [ ] **Add tool aliases to ~/.bash_aliases**
  ```bash
  cat >> ~/.bash_aliases << 'ALIASEOF'

  # Modern CLI replacements
  alias ls="eza --color=always --group-directories-first"
  alias ll="eza -la --color=always --group-directories-first --git"
  alias lt="eza --tree --level=2 --color=always"
  alias la="eza -a --color=always --group-directories-first"
  alias cat="bat --paging=never"
  alias grep="rg"
  alias find="fd"
  alias du="dust"
  alias df="duf"
  alias top="btop"
  ALIASEOF
  source ~/.bash_aliases
  ```

## Phase 7: Verification

- [ ] **Test each tool**
  ```bash
  bat ~/.bashrc                    # Syntax highlighted file view
  fd "*.md" ~/workspace            # Find markdown files
  rg "TODO" ~/workspace            # Search for TODO comments
  eza -la ~/workspace              # List files with git status
  duf                              # Disk usage overview
  dust ~/workspace                 # Directory size tree
  ```

- [ ] **Test fzf integration**
  ```bash
  # Ctrl+R: fuzzy search command history
  # Ctrl+T: fuzzy file search
  # Alt+C:  fuzzy directory change
  ```

- [ ] **Test delta**
  ```bash
  cd ~/workspace/repos/nero-core
  git log --oneline -5             # Should show with delta
  git diff                         # Side-by-side diff
  ```

- [ ] **Test starship prompt**
  ```bash
  cd ~/workspace/repos/nero-core   # Should show git branch
  cd /tmp                          # Should show directory only
  ```

- [ ] **Test zoxide**
  ```bash
  z workspace                      # Jump to ~/workspace
  z nero-core                      # Jump to nero-core directory
  ```
