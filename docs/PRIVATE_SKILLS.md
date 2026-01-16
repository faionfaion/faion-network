# Private Skills Configuration

How to add project-specific skills that won't sync to faion-network repo.

## Setup

1. **Global excludes** configured in `~/.gitconfig`:
   ```
   [core]
       excludesFile = ~/.gitignore
   ```

2. **Add private skill pattern** to `~/.gitignore`:
   ```
   # Private skills (not in faion-network)
   skills/epass-devops/
   skills/another-private-skill/
   ```

## How It Works

- `~/.claude/` is a git repo synced to `github.com/faionfaion/faion-network`
- `~/.gitignore` acts as global excludes for ALL repos (via `core.excludesFile`)
- Patterns in `~/.gitignore` are relative to each repo's root
- Pattern `skills/epass-devops/` ignores `~/.claude/skills/epass-devops/`

## Adding New Private Skill

1. Create skill in `~/.claude/skills/my-private-skill/`
2. Add to `~/.gitignore`:
   ```
   skills/my-private-skill/
   ```
3. Verify: `cd ~/.claude && git status` - should not show the skill

## Why Not Use `~/.claude/.gitignore`?

`~/.claude/.gitignore` is tracked in faion-network repo. Adding private skills there would expose their names to everyone who pulls the repo.

Using `~/.gitignore` keeps private skill names local.
