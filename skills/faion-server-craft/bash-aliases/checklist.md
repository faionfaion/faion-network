# Bash Aliases Checklist

Step-by-step checklist for organizing and deploying aliases on Ubuntu 24.04.

## Phase 1: Audit Current State

- [ ] **Check existing aliases**
  ```bash
  alias | wc -l
  alias
  ```

- [ ] **Check existing ~/.bash_aliases**
  ```bash
  cat ~/.bash_aliases 2>/dev/null || echo "(no file)"
  ```

- [ ] **Check ~/.bashrc sources aliases**
  ```bash
  grep -n "bash_aliases" ~/.bashrc
  # Should contain: if [ -f ~/.bash_aliases ]; then . ~/.bash_aliases; fi
  ```

## Phase 2: Create Organized Alias File

- [ ] **Back up existing aliases**
  ```bash
  cp ~/.bash_aliases ~/.bash_aliases.bak 2>/dev/null
  ```

- [ ] **Create categorized ~/.bash_aliases**
  Use the template from templates.md.

- [ ] **Source and verify**
  ```bash
  source ~/.bash_aliases
  alias | wc -l
  ```

## Phase 3: Test Critical Aliases

- [ ] **Test navigation aliases**
  ```bash
  type ws    # Should show workspace alias
  type repos # Should show repos alias
  ```

- [ ] **Test system aliases**
  ```bash
  type ports    # Should show ss command
  type meminfo  # Should show free command
  ```

- [ ] **Test docker aliases** (if Docker installed)
  ```bash
  type dk-ps    # Should show docker ps
  ```

- [ ] **Test git aliases**
  ```bash
  type gs    # Should show git status
  type gl    # Should show git log
  ```

- [ ] **Test function aliases**
  ```bash
  type mkcd    # Should show function
  type port    # Should show function
  ```

## Phase 4: Project-Specific Aliases

- [ ] **Add project aliases**
  Aliases specific to NERO platform or other projects.

- [ ] **Verify project aliases work**
  ```bash
  type nero-status    # Service status
  type nero-logs      # Follow logs
  ```

## Phase 5: Verification

- [ ] **Count total aliases**
  ```bash
  alias | wc -l
  grep -c "^alias\|^[a-z_-]*() {" ~/.bash_aliases
  ```

- [ ] **Verify no conflicts**
  ```bash
  # Check for aliases that shadow important commands
  for cmd in ls cat grep find rm mv cp; do
      TYPE=$(type -t "$cmd")
      [ "$TYPE" = "alias" ] && echo "ALIASED: $cmd -> $(alias $cmd)"
  done
  ```

- [ ] **Test in new shell**
  ```bash
  bash -l -c "alias | head -20"
  ```

## Maintenance

- [ ] **Review quarterly** and remove unused aliases
- [ ] **Add new aliases** as patterns emerge
- [ ] **Share across machines** via dotfiles repo or copy
