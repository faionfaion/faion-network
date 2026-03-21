# tmux Power User LLM Prompts

Prompts for AI assistants to configure, customize, and troubleshoot tmux.

## Prompt 1: tmux Setup

```
Set up tmux on this server for an AI agent development workflow.

Steps:
1. Install tmux if not present
2. Install TPM (tmux Plugin Manager)
3. Create ~/.tmux.conf with:
   - Ctrl+A prefix
   - Mouse support
   - Vi copy mode
   - Intuitive split keys (| and -)
   - Pane navigation (Ctrl+arrows)
   - Window navigation (Alt+1-9)
   - True color support
   - Plugins: resurrect, continuum
   - Status bar with system metrics
4. Create status bar script (~/.tmux-system.sh)
5. Source the config
6. Install plugins (prefix + I)
7. Verify everything works

Also create a session template script for the user's main project.
```

## Prompt 2: Status Bar Customization

```
Customize the tmux status bar for this server.

Current status bar: {describe or show current config}

I want the status bar to show:
{list desired elements, e.g.:
- Session name (left)
- System metrics: RAM%, CPU%, Disk% (right, color-coded)
- Current time (right)
- Git branch (if in a repo)
- Number of running Docker containers
}

Create:
1. The status bar configuration for .tmux.conf
2. The status bar script that generates the dynamic parts
3. Make the script efficient (runs every few seconds)

Test the script standalone first, then integrate with tmux.
```

## Prompt 3: Session Template Creation

```
Create a tmux session template for the following project:

Project: {name}
Directory: {path}
Layout:
- Window 1: {purpose, e.g., "main editor"}
- Window 2: {purpose, e.g., "terminal"}
- Window 3: {purpose, e.g., "logs with 3 panes"}
- Window 4: {purpose, e.g., "docker/infra"}

Requirements:
- Named session
- Named windows
- Specific pane layouts for multi-pane windows
- Each pane starts in the correct directory
- Long-running commands auto-started in specific panes
- If session exists, attach instead of creating

Output a bash script that creates this layout.
```

## Prompt 4: tmux Troubleshooting

```
I'm having an issue with tmux: {describe the problem}

Common issues and diagnostics:

1. Colors not working:
   - Check TERM: `echo $TERM` (inside and outside tmux)
   - Check tmux config: `tmux show -g default-terminal`
   - Fix: `set -g default-terminal "screen-256color"` + terminal-overrides

2. Mouse not working:
   - Check: `tmux show -g mouse` (should be "on")
   - Nested tmux? Both need mouse enabled

3. Copy/paste not working:
   - Check: `tmux show -gw mode-keys` (should be "vi")
   - Check clipboard: is xclip/xsel installed?
   - Over SSH: tmux-yank plugin needed

4. Plugins not loading:
   - Check TPM: `ls ~/.tmux/plugins/tpm/`
   - Try: prefix + I to install
   - Check last line: `run '~/.tmux/plugins/tpm/tpm'`

5. Status bar blank:
   - Check script: `bash ~/.tmux-system.sh`
   - Check executable: `ls -la ~/.tmux-system.sh`
   - Check config: `tmux show -g status-right`

6. resurrect not restoring:
   - Check save files: `ls ~/.tmux/resurrect/`
   - Manual save: prefix + Ctrl+S
   - Manual restore: prefix + Ctrl+R

Run the appropriate diagnostics and fix the issue.
```

## Prompt 5: Workflow Optimization

```
Optimize my tmux workflow. Current setup:

- Current .tmux.conf: {read ~/.tmux.conf}
- Number of sessions: {tmux ls}
- Daily tasks: {describe workflow}

Analyze and suggest:
1. Are there repetitive actions that can be bound to a key?
2. Should any windows be merged or split differently?
3. Are there useful plugins I'm missing?
4. Is the status bar showing useful information?
5. Can session templates automate my daily startup?
6. Are there tmux features I'm not using?

Provide specific config changes and explain the benefit of each.
```

## Prompt 6: Theme Configuration

```
Apply a theme to my tmux setup.

Theme options:
1. Tokyo Night (dark, blue accent)
2. Catppuccin (pastel, mocha variant)
3. Dracula (dark, purple accent)
4. Nord (cool blue tones)
5. Minimal (dark background, white text, blue accents)

Selected theme: {number or name}

Apply the theme to:
- Status bar colors (background, foreground)
- Active/inactive window indicators
- Pane borders (active vs inactive)
- Message/command prompt colors
- Copy mode highlight colors

Output the complete color configuration to add to .tmux.conf.
Do NOT use a plugin for the theme (keep it in config for simplicity).
```

## Prompt 7: Migration from screen to tmux

```
I'm migrating from GNU screen to tmux. Map my screen workflow to tmux.

Screen commands I use:
- Ctrl+A, c  (new window)
- Ctrl+A, n  (next window)
- Ctrl+A, p  (prev window)
- Ctrl+A, d  (detach)
- Ctrl+A, S  (split horizontal)
- Ctrl+A, |  (split vertical)
- Ctrl+A, tab (switch pane)

Create a tmux config that:
1. Uses Ctrl+A as prefix (same as screen)
2. Maps these screen keybindings to tmux
3. Adds tmux-specific improvements (mouse, plugins, etc.)
4. Explains the key differences between screen and tmux
```

## Prompt 8: Performance Debugging

```
tmux is slow/laggy. Help diagnose and fix.

Diagnostics:
1. Check tmux version: `tmux -V`
2. Check status-interval: `tmux show -g status-interval` (lower = more CPU)
3. Check status bar script performance: `time ~/.tmux-system.sh`
4. Check scrollback buffer size: `tmux show -g history-limit`
5. Check number of panes: `tmux list-panes -a | wc -l`
6. Check if a pane is producing excessive output (logging)
7. Check system resources: `top -bn1 | head -5`

Common fixes:
- Increase status-interval from 1 to 5
- Reduce history-limit from 100000 to 50000
- Optimize status bar script (cache values)
- Reduce scrollback in high-output panes
- Close unused panes/windows
```
