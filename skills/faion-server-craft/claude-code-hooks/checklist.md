# Setup Claude Code Hooks Checklist

## Prerequisites

- [ ] Claude Code installed and working
- [ ] `jq` installed: `sudo apt install jq`
- [ ] Understand hook types: command, prompt
- [ ] Understand events: PreToolUse, PostToolUse, UserPromptSubmit, etc.
- [ ] Know settings.json location: `~/.claude/settings.json` (global)

## Hook Directory Setup

- [ ] Create hooks directory: `mkdir -p ~/.claude/hooks/`
- [ ] All hook scripts will live here
- [ ] Make scripts executable: `chmod +x ~/.claude/hooks/*.sh`

## settings.json Configuration

- [ ] Open or create `~/.claude/settings.json`
- [ ] Add `"hooks"` key with event entries
- [ ] Each event maps to an array of hook definitions
- [ ] Each hook has: `type`, `command`, optional `matcher`, optional `timeout`
- [ ] JSON is valid: test with `jq . ~/.claude/settings.json`

## Common Hooks to Implement

### Post-Edit Formatter
- [ ] Create `~/.claude/hooks/post-edit-format.sh`
- [ ] Read file path from stdin JSON
- [ ] Detect file extension
- [ ] Run appropriate formatter (ruff for .py, prettier for .ts/.js)
- [ ] Handle missing formatter gracefully (exit 0)
- [ ] Add to settings.json: PostToolUse with matcher "Edit"
- [ ] Test: edit a Python file, verify it gets formatted

### Post-Write Formatter
- [ ] Create `~/.claude/hooks/post-write-format.sh`
- [ ] Same logic as post-edit, but for Write tool
- [ ] Add to settings.json: PostToolUse with matcher "Write"
- [ ] Test: write a new file, verify it gets formatted

### Tmux Save
- [ ] Create `~/.claude/hooks/tmux-save.sh`
- [ ] Check if running in tmux ($TMUX is set)
- [ ] Capture current pane content
- [ ] Add to settings.json: UserPromptSubmit and SubagentStart
- [ ] Test: send a prompt, verify tmux state is captured

### Git Safety (Optional)
- [ ] Create `~/.claude/hooks/pre-bash-validate.sh`
- [ ] Block `git push --force main/master`
- [ ] Block `git reset --hard` without confirmation
- [ ] Add to settings.json: PreToolUse with matcher "Bash"
- [ ] Test: try a force push command, verify it's blocked

## Hook Script Best Practices

- [ ] Always read stdin (even if not used): `INPUT=$(cat)`
- [ ] Parse JSON with `jq`: `echo "$INPUT" | jq -r '.field'`
- [ ] Always exit 0 (non-zero may break Claude)
- [ ] Return valid JSON on stdout (or no output)
- [ ] Log errors to a file, not stderr
- [ ] Keep execution under 5 seconds
- [ ] Handle missing files/tools gracefully

## Testing Hooks

### Manual Testing
- [ ] Test each hook manually with piped JSON:
  ```
  echo '{"event":"PostToolUse","tool":"Edit","parameters":{"file_path":"/tmp/test.py"}}' | bash ~/.claude/hooks/post-edit-format.sh
  ```
- [ ] Verify exit code is 0
- [ ] Verify JSON output is valid (if any)

### Integration Testing
- [ ] Start Claude Code session
- [ ] Trigger each hook event
- [ ] Verify hook executed (check logs or side effects)
- [ ] Verify no errors in Claude Code output

## Debugging

- [ ] Add logging to hooks: `echo "$(date) - event" >> /tmp/claude-hooks.log`
- [ ] Check Claude Code for hook error messages
- [ ] Verify settings.json is valid JSON
- [ ] Verify hook scripts are executable
- [ ] Verify `jq` is available
- [ ] Check hook timeout (increase if needed)

## Performance Check

- [ ] Each hook completes in under 5 seconds
- [ ] No hooks make network calls
- [ ] No hooks process very large files
- [ ] Timeout set appropriately for slow hooks
- [ ] Hooks don't interfere with each other

## Documentation

- [ ] Hook purpose documented in script header comment
- [ ] settings.json commented (or documented in README)
- [ ] Known limitations documented
- [ ] How to add new hooks documented
