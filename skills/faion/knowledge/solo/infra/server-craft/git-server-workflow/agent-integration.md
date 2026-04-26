# Agent Integration — Git Server Workflow

## When to use
- Solo developer VPS platform with multiple repos that deploy to a single server
- Agents need to make changes and deploy without triggering full CI/CD pipeline overhead
- Parallel agent tasks on the same repo (worktrees isolate branches, prevent conflicts)
- Rapid iteration cycles where workspace/runtime separation keeps services running during development
- Post-receive hook automation: push to deploy without SSH login on each deploy

## When NOT to use
- Multi-server deployments where code must land on multiple hosts — use a CI/CD pipeline instead
- Team environments with multiple developers — bare repo push-to-deploy conflicts under concurrent pushes
- When the deployment unit is a Docker image — build/push/pull pattern replaces rsync
- Repos with large binary assets (> 500 MB) — rsync is fine but git rollback becomes slow
- When strict audit trail of deployments is required — post-receive hooks have no built-in deployment log

## Where it fails / limitations
- `git checkout HEAD~1` + redeploy is not truly atomic; service briefly runs old code while rsync transfers new code
- Worktrees share the `.git` directory; a corrupted pack file affects all worktrees simultaneously
- Post-receive hook failures are silent to the pushing developer unless the hook explicitly prints to stdout/stderr and exits non-zero
- `git worktree prune` only removes entries from `.git/worktrees`; stale directories on disk must be cleaned manually
- rsync `--delete` will remove files in runtime that were manually placed there (e.g., uploaded user files) if those paths are not excluded

## Agentic workflow
An agent working on a feature creates a worktree off the main repo (`git worktree add`), makes changes inside the isolated worktree, runs the deploy script pointing at the worktree source, and verifies the service health endpoint. After confirmation, it merges back to main and removes the worktree. The parent agent serializes merges using `flock` to prevent concurrent merge races. Human approval is required before merging agent branches that touch schema migrations or service configuration.

### Recommended subagents
- `faion` (infra/server-craft/deploy-scripts) — the deploy.sh patterns that git-server-workflow triggers
- `faion` (infra/server-craft/systemd-user-services) — services that get restarted after rsync
- `faion` (infra/server-craft/agent-dev-tuning) — worktree-specific inotify and resource tuning for parallel agents

### Prompt pattern
```
Create a git worktree for branch feature/<task-id> in ../nero-core-<task-id>.
Make the required changes inside the worktree.
Run: bash ~/workspace/deploy/deploy.sh nero-core
Verify service health: curl -sf http://127.0.0.1:8100/health
If healthy, output the list of changed files. Do not merge — await human approval.
```

```
Roll back nero-core to the previous commit:
1. cd ~/workspace/repos/nero-core
2. git log --oneline -5  (show me the candidates)
3. git checkout HEAD~1
4. bash ~/workspace/deploy/deploy.sh nero-core
5. Verify service is active with systemctl --user is-active nero-core
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git worktree` | Multiple working trees from one repo | Built into git 2.5+ |
| `rsync` | Fast incremental file sync for deploy | Pre-installed on Ubuntu; `man rsync` |
| `flock` | Serialize concurrent shell operations | Part of `util-linux`; pre-installed |
| `git log --oneline` | Compact commit history for rollback selection | Built-in |
| `git tag -a` | Mark known-good states before risky changes | Built-in |
| `git post-receive` hook | Push-to-deploy automation on bare repo | Git hook; script in `hooks/post-receive` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub / GitLab | SaaS | Yes (API + push) | Remote origin; agents push branches via `git push` |
| Gitea | OSS | Yes (REST API) | Self-hosted option; supports webhooks for push-to-deploy |
| Bare repo on VPS | OSS (manual) | Yes | Post-receive hook pattern; no external dependency |
| Portainer | OSS | Yes (REST API) | If Compose is used; can trigger stack updates on push via webhook |

## Templates & scripts
See `templates.md` for complete deploy.sh and rollback.sh. Inline worktree-based agent task script:

```bash
#!/bin/bash
# agent-task.sh — create isolated worktree for an agent task
# Usage: bash agent-task.sh <repo-path> <task-id> <branch-base>
set -euo pipefail
REPO="${1:?repo path required}"
TASK="${2:?task id required}"
BASE="${3:-main}"
WORKTREE_DIR="${REPO}-${TASK}"

cd "$REPO"
git fetch origin
git worktree add "$WORKTREE_DIR" -b "feature/$TASK" "origin/$BASE"
echo "Worktree created: $WORKTREE_DIR (branch: feature/$TASK)"
echo "Work inside: $WORKTREE_DIR"
echo "Deploy with: bash ~/workspace/deploy/deploy.sh <service>"
echo "Cleanup: git worktree remove $WORKTREE_DIR && git branch -d feature/$TASK"
```

## Best practices
- Always tag known-good states before any risky deploy (`git tag -a v<x> -m "pre-<change>"`) — enables one-command rollback
- Keep rsync excludes explicit and version-controlled in the deploy script; never rely on memory for what to exclude
- Enable `set -euo pipefail` in all deploy and hook scripts — silent partial deploys are worse than hard failures
- Post-receive hooks must be executable (`chmod +x hooks/post-receive`) and tested with `git push` to a test branch first
- Worktrees should be placed outside the repo directory (`../repo-task-id`) to avoid nested `.git` confusion
- Deploy order matters for shared-library repos: SDK first, then all dependent services in dependency order
- Use `systemctl --user is-active service` with a retry loop (not `sleep 5`) in post-deploy validation

## AI-agent gotchas
- Agents must never run `git checkout` on the main workspace while a service is running from its source directory — this causes the service to load partially-staged files; use worktrees for all changes
- `git worktree remove` fails if the worktree has uncommitted changes; agents must stash or commit before cleanup
- rsync `--delete` is destructive; agents must specify all necessary `--exclude` flags before running; a missing exclude can wipe runtime-only files (uploads, generated caches) permanently
- Post-receive hooks run as the git user, not the application user; agents writing hook scripts must account for PATH and environment differences
- `git checkout HEAD~1` puts HEAD in detached state; agents must `git checkout main` to return or subsequent commits are lost

## References
- https://git-scm.com/docs/git-worktree
- https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
- https://linux.die.net/man/1/rsync
- https://www.freedesktop.org/software/systemd/man/systemctl.html
