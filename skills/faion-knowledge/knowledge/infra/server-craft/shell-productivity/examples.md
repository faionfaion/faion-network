# Shell Productivity Examples

Real-world usage examples of modern CLI tools on the NERO server.

## Example 1: fzf + fd File Search

### Find and Preview Any File

```bash
# Ctrl+T to search files, with bat preview
$ # Press Ctrl+T
# Shows interactive file picker with syntax-highlighted preview
# Type to filter: "nero" -> shows only nero-related files
# Select file -> path is inserted at cursor

# Search Python files only
$ fd -e py | fzf --preview 'bat --color=always {}'

# Search in specific directory
$ fd -e md . ~/workspace/repos/nero-core | fzf --preview 'bat --color=always {}'
```

### Quick Project File Navigation

```bash
# Jump to any file in workspace
$ vim $(fd -e py . ~/workspace/repos | fzf --preview 'bat --color=always --line-range=:50 {}')

# Find and open a config file
$ vim $(fd "config" ~/workspace --type f | fzf)
```

## Example 2: bat as Pager

### Syntax-Highlighted File View

```bash
# View Python file with line numbers and git changes
$ bat ~/workspace/repos/nero-core/src/nero_core/worker.py
# Shows: line numbers, syntax highlighting, git diff markers (+/-)

# View just a range of lines
$ bat --line-range=50:100 ~/workspace/repos/nero-core/src/nero_core/worker.py

# Compare two files
$ bat --diff file1.py file2.py

# View nginx config with highlighting
$ bat /etc/nginx/sites-enabled/nero.faion.net
# Automatically detects nginx config syntax
```

### Use bat as Man Pager

```bash
export MANPAGER="sh -c 'col -bx | bat -l man -p'"
# Now 'man ssh' has syntax highlighting
```

## Example 3: eza Tree Views

### Project Structure

```bash
# Tree view of NERO workspace
$ eza --tree --level=2 ~/workspace/repos/
workspace/repos/
  nero-core/
    src/
    tests/
    pyproject.toml
    CLAUDE.md
  nero-channel-web/
    src/
    tests/
    pyproject.toml
  nero-sdk/
    src/
    pyproject.toml
  ...

# With git status indicators
$ eza --tree --level=2 --git ~/workspace/repos/nero-core/
nero-core/
  src/
    nero_core/
      worker.py       [M]   # Modified
      config.py              # Clean
      __init__.py            # Clean
  tests/
    test_worker.py    [N]   # New/untracked
  pyproject.toml             # Clean

# Long listing with git, size, date
$ eza -la --git --header ~/workspace/repos/nero-core/
Permissions Size User Date Modified Name
drwxr-xr-x     - nero 21 Mar 10:00  src
drwxr-xr-x     - nero 20 Mar 15:30  tests
.rw-r--r--  1.2k nero 19 Mar 09:00  pyproject.toml  --
.rw-r--r--   845 nero 21 Mar 10:00  CLAUDE.md       M-
```

## Example 4: delta Git Diffs

### Side-by-Side Diff

```bash
$ cd ~/workspace/repos/nero-core
$ git diff

# delta shows side-by-side with:
# - Line numbers on both sides
# - Syntax highlighting
# - Color-coded additions (green) and deletions (red)
# - Moved code detection (different color)
# - Navigate between hunks: n/N keys

# View specific commit
$ git show HEAD --stat    # Shows changed files
$ git show HEAD           # Full diff with delta formatting

# Git log with diffs
$ git log -p --follow src/nero_core/worker.py
```

## Example 5: ripgrep (rg) Search

### Search Across All Repos

```bash
# Find all TODO comments
$ rg "TODO" ~/workspace/repos/
nero-core/src/nero_core/worker.py:42:    # TODO: implement retry logic
nero-channel-web/src/channel_web/router.py:15:    # TODO: add rate limiting
nero-sdk/src/nero_sdk/models.py:88:    # TODO: add validation

# Search for function definitions
$ rg "^def |^async def " ~/workspace/repos/nero-core/src/ --type py

# Search with context (3 lines before and after)
$ rg -C3 "class MessageEnvelope" ~/workspace/repos/nero-sdk/

# Count matches per file
$ rg -c "import" ~/workspace/repos/nero-core/src/ --type py

# Search and replace preview
$ rg "old_function_name" --replace "new_function_name" ~/workspace/repos/
```

## Example 6: zoxide Directory Jumping

### Frecency-Based Navigation

```bash
# After using cd for a while, zoxide learns your patterns:
$ z nero-core          # Jumps to ~/workspace/repos/nero-core
$ z channel-web        # Jumps to ~/workspace/repos/nero-channel-web
$ z infra              # Jumps to ~/workspace/repos/nero-infra
$ z workspace          # Jumps to ~/workspace

# Interactive mode (with fzf)
$ zi nero              # Shows all directories matching "nero", pick one

# Check what zoxide has learned
$ zoxide query --list | head -10
120.5  /home/nero/workspace/repos/nero-core
 98.2  /home/nero/workspace/repos/nero-channel-web
 76.8  /home/nero/workspace
 45.1  /home/nero/workspace/repos/nero-sdk
 32.4  /home/nero/workspace/repos/nero-infra
```

## Example 7: btop System Monitoring

```bash
# Launch btop (replaces top/htop)
$ btop

# Shows:
# - CPU usage per core (16 cores on CX53)
# - Memory usage with swap
# - Network I/O
# - Disk I/O
# - Process tree with sorting
# - Color themes
#
# Key bindings:
# - 1: CPU view
# - 2: Memory view
# - 3: Network view
# - 4: Disk view
# - f: Filter processes
# - t: Toggle tree view
# - s: Sort by column
# - q: Quit
```

## Example 8: duf and dust for Disk Analysis

### Disk Space Overview

```bash
$ duf
# Shows beautiful table:
# Device     Size  Used  Avail  Use%  Mounted on
# /dev/sda1  150G   63G    87G   42%  /
# tmpfs       15G    0B    15G    0%  /dev/shm
# (with color coding for usage levels)

$ duf --only local
# Show only local filesystems (not tmpfs, devtmpfs)
```

### Directory Size Analysis

```bash
$ dust ~/workspace/repos/
# Shows visual tree of disk usage:
# 1.2G  ┌── nero-web/node_modules
# 1.5G  ├── nero-web
# 450M  ├── nero-core/.venv
# 680M  ├── nero-core
# 320M  ├── nero-channel-web/.venv
# 510M  ├── nero-channel-web
# ...
# 4.2G  └── repos

$ dust -n 10 ~/workspace
# Show only top 10 largest directories
```

## Example 9: Combined Workflow

### Finding and Fixing a Bug

```bash
# 1. Search for the error message
$ rg "Connection refused" ~/workspace/repos/ --type py
#    nero-core/src/nero_core/worker.py:142: "Connection refused"

# 2. View the file with context
$ bat --highlight-line 142 ~/workspace/repos/nero-core/src/nero_core/worker.py

# 3. Check git blame for that line
$ cd ~/workspace/repos/nero-core
$ git log --oneline -5 src/nero_core/worker.py

# 4. Make the fix (edit the file)

# 5. Review changes
$ git diff    # delta shows side-by-side

# 6. Commit
$ git add -A && git commit -m "fix: handle connection refused in worker"
```
