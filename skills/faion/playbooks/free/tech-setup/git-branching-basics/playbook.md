---
name: git-branching-basics
description: Create a feature branch, do work on it, push to GitHub, merge back to main, and never break your working code again.
tier: free
group: tech-setup
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will use a trunk-based branching workflow: every change lives on a short-lived feature branch, `main` always stays deployable, and you know how to fix the one mistake that trips every beginner — accidentally committing to `main` directly.

## Prerequisites

- Git installed and configured locally (`git --version` returns 2.x or later).
- A GitHub repository with a `main` branch (see [github-account-and-first-repo](../github-account-and-first-repo/playbook.md)).
- SSH key added to GitHub so `git push` works without a password (see [ssh-key-setup-github](../ssh-key-setup-github/playbook.md)).
- Basic comfort with `git add`, `git commit`, `git push` (one prior session is enough).

## Steps

1. Start from an up-to-date `main` branch before creating any new branch:
   ```bash
   git switch main
   git pull origin main
   ```

2. Create and switch to a new feature branch in one command. Use a short, lowercase, hyphenated name that describes the work:
   ```bash
   git switch -c feature/add-search
   ```
   You are now on `feature/add-search`. `main` is untouched.

3. Do your work — edit files, add new ones. Commit as you go with focused commits:
   ```bash
   git add src/search.js tests/search.test.js
   git commit -m "feat: add search input component"
   ```
   Repeat this cycle (edit → add → commit) as many times as needed. Each commit should represent one logical change.

4. Push the branch to GitHub and set the upstream tracking reference:
   ```bash
   git push -u origin feature/add-search
   ```
   The `-u` flag links the local branch to the remote copy so future `git push` and `git pull` on this branch need no arguments.

5. **Solo workflow — merge directly to main** (skip to Step 6 if you want a PR instead):
   ```bash
   git switch main
   git pull origin main
   git rebase feature/add-search
   git push origin main
   git branch -d feature/add-search
   git push origin --delete feature/add-search
   ```
   Rebase keeps history linear — one straight line of commits rather than a merge bubble. On `main` you will see every commit from the feature branch as if they were always there.

6. **Team / PR workflow — open a pull request** (alternative to Step 5):
   ```bash
   gh pr create --title "feat: add search input" --base main --head feature/add-search
   ```
   Review and merge on GitHub, then clean up locally:
   ```bash
   git switch main
   git pull origin main
   git branch -d feature/add-search
   ```

7. Fix an accidental commit to `main` — the most common beginner mistake. If you committed to `main` instead of a feature branch, undo the commit but keep the changes staged:
   ```bash
   git reset --soft HEAD~1
   ```
   Your files are still modified and staged. Now create the branch you meant to use and commit there:
   ```bash
   git switch -c feature/add-search
   git commit -m "feat: add search input component"
   ```
   If you already pushed to `main`, talk to your team first — rewriting pushed history requires a force-push and affects everyone.

8. **Rebase vs merge — when to choose which:**
   - **Rebase** (`git rebase`) rewrites your branch commits on top of the latest `main`. Result: clean linear history, easy to read with `git log`. Preferred for solo work and squash-before-merge.
   - **Merge** (`git merge`) creates a merge commit that records the join point. Result: preserves the full branching graph. Preferred when you need an audit trail of when branches were combined (e.g. staging → production).
   - For a solo project, default to rebase. The rule of thumb: never rebase a branch that someone else has checked out.

## Verify

Run this after merging your branch back to `main`:

```bash
git log --oneline -5
```

You should see your feature commits at the top of the log, with no merge commit bubble (if you used rebase). The branch list should show only `main` locally:

```bash
git branch
```

Output: `* main` (and nothing else if you deleted the feature branch).

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `git switch -c feature/add-search` says `fatal: A branch named 'feature/add-search' already exists` | You created this branch before and never deleted it | Run `git branch -d feature/add-search` to delete it (safe if fully merged), then re-create it, or switch to it directly with `git switch feature/add-search` |
| `git rebase feature/add-search` stops mid-way with `CONFLICT` | The same line was changed on both `main` and the feature branch | Open the conflicted files (marked with `<<<<<<<`), resolve manually, then `git add <file>` and `git rebase --continue`; abort with `git rebase --abort` if needed |
| `git push` after rebase says `rejected — non-fast-forward` | You rebased a branch that was already pushed, so remote and local histories diverged | For a solo feature branch you are the only user of, `git push --force-with-lease origin feature/add-search` is safe; never force-push `main` |
| `git reset --soft HEAD~1` removed more than one commit | `HEAD~1` means exactly one commit back; if you typed `HEAD~2` you undid two | Run `git reflog` to find the original commit hash and `git reset --soft <hash>` to restore to that exact point |
| After `git switch main && git pull`, the branch looks behind | `git pull` did a fast-forward but you are still on the stale branch view | Run `git log --oneline -5` on `main` again — the log updates after the pull |

## Next

- [vscode-first-project-setup](../vscode-first-project-setup/playbook.md) — configure VS Code to show branch name, diff gutters, and the Git Graph extension so you can see your branch history visually.
- Learn interactive rebase to clean up commit messages before merging: `git rebase -i HEAD~3` lets you squash, reword, or drop the last three commits.
- Explore branch protection on GitHub (Settings → Branches → Add rule) to enforce that `main` can only receive merged PRs — locks in this workflow for the whole team.

## References

- [knowledge/free/dev/devtools-developer/github-repo-bootstrap](../../../knowledge/free/dev/devtools-developer/github-repo-bootstrap) — the squash-only merge setting, branch-deletion-on-merge, and linear-history rule configured in Step 7 of that methodology are the GitHub-side complement to the rebase-first approach taught in Steps 5 and 8 of this playbook; the two documents form the complete trunk-based setup for a solo repo.
