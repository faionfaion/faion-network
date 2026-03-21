# Shell Productivity LLM Prompts

Prompts for AI assistants to install, configure, and integrate modern CLI tools.

## Prompt 1: CLI Tools Audit

```
Audit the CLI tools installed on this Ubuntu server and recommend modern replacements.

Check which tools are installed:
```bash
for tool in bat batcat fd fdfind fzf rg eza exa delta starship zoxide btop htop duf dust; do
    LOC=$(command -v "$tool" 2>/dev/null)
    [ -n "$LOC" ] && echo "INSTALLED: $tool ($LOC)" || echo "MISSING: $tool"
done
```

Also check:
- Current shell: `echo $SHELL`
- Shell version: `bash --version | head -1`
- Terminal: `echo $TERM`
- Existing aliases: `alias`
- Current prompt: `echo $PS1`
- Git pager: `git config --get core.pager`

Report:

| Category | Traditional | Modern | Status |
|----------|-------------|--------|--------|
| File view | cat | bat | INSTALLED/MISSING |
| File list | ls | eza | INSTALLED/MISSING |
| ...

Provide installation commands for all missing tools.
```

## Prompt 2: Full CLI Modernization

```
Install and configure the complete modern CLI toolkit on this Ubuntu 24.04 server.

Install these tools:
1. bat (syntax-highlighted cat)
2. fd (fast find)
3. fzf (fuzzy finder)
4. ripgrep (fast grep)
5. eza (better ls)
6. delta (better git diff)
7. starship (cross-shell prompt)
8. zoxide (smart cd)
9. btop (system monitor)
10. duf (disk usage)
11. dust (directory usage)

After installation:
1. Create symlinks for Ubuntu naming (bat -> batcat, fd -> fdfind)
2. Add shell integrations to ~/.bashrc (fzf, starship, zoxide)
3. Create starship.toml (minimal, fast prompt)
4. Configure delta in ~/.gitconfig
5. Add aliases to ~/.bash_aliases
6. Verify all tools work

Output the verification results.
```

## Prompt 3: fzf Power User Setup

```
Configure fzf for maximum productivity on this server.

1. Install fzf if not present
2. Configure in ~/.bashrc:
   - Ctrl+R: fuzzy history search
   - Ctrl+T: fuzzy file search with bat preview
   - Alt+C: fuzzy directory jump with eza tree preview
3. Set FZF_DEFAULT_COMMAND to use fd
4. Create custom fzf functions:
   - fgl: browse git log interactively
   - fbr: switch git branches interactively
   - fkill: kill process interactively
   - frg: search content with ripgrep + fzf
5. Test each keybinding and function
```

## Prompt 4: Shell Prompt Optimization

```
My shell prompt is slow. Optimize it.

Current prompt: {show current PS1 or starship config}
Shell: bash

Diagnostics:
1. Time the prompt: `time bash -ic exit`
2. If using starship: `starship timings`
3. Check what's slow (git status? language detection?)

Optimization options:
A. Starship with minimal modules (disable unused: aws, docker, k8s)
B. Pure bash PS1 (fastest, no external deps)
C. Starship with async modules

For option A:
- Create optimized starship.toml
- Disable all modules except: directory, git_branch, git_status, character
- Set scan_timeout and command_timeout low
- Test speed

For option B:
- Write a pure bash PS1 with directory and git branch
- No external tool calls
- Test speed
```

## Prompt 5: Tool Integration

```
Show me how to integrate these CLI tools with each other for maximum productivity.

Tools available: {list installed tools}

Integration examples needed:
1. fzf + bat: file search with preview
2. fzf + rg: content search with preview
3. fzf + git + delta: browse commits/diffs
4. fd + fzf: smart file navigation
5. bat + git: syntax-highlighted diffs
6. zoxide + fzf: interactive directory jumping

For each integration:
- The command/function
- A brief explanation
- Where to add it (bashrc, aliases, etc.)
```

## Prompt 6: Tool Updates

```
Check for updates to all modern CLI tools and upgrade them.

For each installed tool:
1. Check current version
2. Check latest available version
3. Show upgrade command
4. Note any breaking changes

Tools to check:
- bat, fd, fzf, rg (apt)
- eza (apt from custom repo)
- delta, dust (GitHub releases / deb)
- starship (install script)
- zoxide (install script)
- btop, duf (apt)

Provide a single script that updates all tools safely.
```
