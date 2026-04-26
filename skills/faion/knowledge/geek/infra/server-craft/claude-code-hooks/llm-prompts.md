# Claude Code Hooks LLM Prompts

## Create Custom Hook

```
Create a Claude Code hook for: [DESCRIBE WHAT YOU WANT]

Examples:
- "Auto-format Python files after Claude edits them"
- "Block dangerous git commands"
- "Save tmux state on each prompt"
- "Run tests after editing a source file"
- "Lint TypeScript files after write"

Hook details:
- Event: [PreToolUse / PostToolUse / UserPromptSubmit / etc.]
- Matcher: [Edit / Write / Bash / or leave blank for all]
- Language: bash

Requirements:
- Parse JSON input from stdin using jq
- Handle missing fields gracefully
- Always exit 0 (don't break Claude)
- Return valid JSON output
- Complete in under [N] seconds

Provide:
1. Hook script (bash)
2. settings.json configuration entry
3. How to test the hook manually (pipe test JSON)
4. Expected behavior in a Claude Code session
5. Edge cases to handle
```

## Debug Hook Issues

```
My Claude Code hook is not working correctly.

Hook: [NAME/DESCRIPTION]
Event: [EVENT]
Matcher: [MATCHER]

Problem: [DESCRIBE, e.g.:
- "Hook doesn't fire at all"
- "Hook fires but formatting doesn't apply"
- "Hook causes Claude to hang"
- "Hook output is not recognized"
]

settings.json hook entry:
[PASTE JSON]

Hook script:
[PASTE SCRIPT or PATH]

What I've tried:
[LIST DEBUGGING STEPS]

Please:
1. Identify the most likely cause
2. Debugging steps to narrow it down
3. Fix the issue
4. How to verify the fix
5. Prevent similar issues in the future
```

## Hook Optimization

```
Optimize my Claude Code hooks for performance.

Current hooks:
[PASTE settings.json hooks section]

Issues:
- [e.g., "Hooks feel slow", "npx prettier takes 3-5 seconds"]
- [e.g., "Hooks run on files they shouldn't"]

For each hook:
1. Is this the right event and matcher?
2. Can the script be faster?
3. Should I skip certain file types/sizes?
4. Is the timeout appropriate?
5. Are there unnecessary operations?

Optimization strategies to consider:
- File extension filtering (skip non-relevant files)
- File size limits (skip large files)
- Caching (don't re-format unchanged files)
- Tool availability checks (exit fast if tool not installed)
- Parallel execution where possible
```

## Design Hook Suite

```
Design a complete hook suite for my [PROJECT_TYPE] development workflow.

Project: [DESCRIBE, e.g., "Python FastAPI backend with PostgreSQL"]
Tools: [LIST, e.g., "ruff, pytest, mypy, alembic"]
Version control: git

Hooks I want:
1. PostToolUse/Edit: [WHAT SHOULD HAPPEN]
2. PostToolUse/Write: [WHAT SHOULD HAPPEN]
3. PreToolUse/Bash: [WHAT SHOULD HAPPEN]
4. UserPromptSubmit: [WHAT SHOULD HAPPEN]
5. [Any others?]

Constraints:
- Each hook should complete in under 5 seconds
- Hooks should not break if a tool is not installed
- Hooks should work on Ubuntu 24.04 server (no GUI)

Provide:
1. Complete settings.json with all hooks
2. Each hook script
3. Installation script (install-hooks.sh)
4. Testing procedure for each hook
5. README for the hooks directory
```

## Hook for Pre-Commit Validation

```
Create a Claude Code PreToolUse hook that validates code quality before commits.

When Claude runs `git commit`:
1. Check for staged .env files (block if found)
2. Check for large files > 5MB (warn)
3. Check for debug/console.log statements in staged code (warn)
4. Check for TODO/FIXME in staged code (warn, don't block)
5. Run linter on staged files (block if errors)

Return:
- {"action": "allow"} if all checks pass
- {"action": "block", "reason": "..."} if critical issues found

Provide:
1. Hook script
2. settings.json entry
3. Testing with simulated git commit
4. How to temporarily bypass the hook if needed
```

## Hook for Auto-Testing

```
Create a hook that automatically runs related tests after Claude edits source code.

Language: [Python / TypeScript / etc.]
Test framework: [pytest / jest / etc.]
Project structure: [describe, e.g., "src/ and tests/ directories, test files named test_*.py"]

Behavior:
1. After Edit tool modifies a source file
2. Find the corresponding test file
3. Run only that specific test file
4. Report results (pass/fail) in hook output
5. Don't block Claude (informational only)

Edge cases:
- No corresponding test file exists (skip silently)
- Test file itself is edited (don't run tests on test file edit)
- Multiple test files for one source file
- File is not in the expected directory structure

Provide:
1. Hook script with test file discovery logic
2. settings.json entry
3. Example of hook output (pass and fail)
4. How to handle different project structures
```

## Migrate Hooks Between Machines

```
I have hooks set up on my server and want to use the same hooks on my workstation.

Current setup (server):
- Settings: ~/.claude/settings.json
- Hooks: ~/.claude/hooks/*.sh
- Tools available: ruff, jq

Workstation differences:
- OS: [macOS / Linux / Windows WSL]
- Tools: [what's installed, what's different]
- Paths may differ

Please:
1. Review my hooks for portability issues
2. Fix any OS-specific commands (stat, sed, etc.)
3. Add tool availability checks (command -v)
4. Create a portable install script
5. How to keep hooks in sync (dotfiles repo?)
6. Handle tool differences (ruff on server, black on workstation)
```
