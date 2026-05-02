---
name: git-daily-workflow
description: Apply the 5-command git rhythm — status, add, commit, pull --rebase, push — to ship code safely every day without clobbering teammates or yourself.
tier: free
group: tech-setup
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will use a repeatable 5-command sequence — `git status`, `git add <files>`, `git commit -m "..."`, `git pull --rebase`, `git push` — as your default daily coding rhythm, keeping your history linear and your shared branches free of accidental overwrites.

## Prerequisites

- Git 2.x installed — verify with `git --version`.
- A GitHub repository cloned locally (see [github-account-and-first-repo](../github-account-and-first-repo/playbook.md)).
- Your name and email configured: `git config --global user.name` and `git config --global user.email` must return non-empty values.
- You are working on a branch (any branch) — `git status` must not say "Not a git repository".

## Steps

1. Check what changed before touching anything:
   ```bash
   git status
   ```
   Read the output. Untracked files appear under "Untracked files". Modified files appear under "Changes not staged for commit". Staged files appear under "Changes to be committed".

2. Stage only the files that belong to this logical change — never `git add .`:
   ```bash
   git add src/auth/login.py
   git add src/auth/tests/test_login.py
   ```
   Staging specific files keeps unrelated work — debug prints, scratch notes, half-finished experiments — out of the commit. Run `git status` again to confirm the right files are staged.

3. Commit with a short, action-leading message (≤50 characters on the title line):
   ```bash
   git commit -m "feat: add login endpoint with JWT"
   ```
   Use a prefix that signals intent: `feat` for new behaviour, `fix` for bug fix, `docs` for documentation, `chore` for maintenance, `refactor` for restructuring without behaviour change, `test` for tests only.

4. Fetch and integrate upstream work before pushing, rebasing your commits on top of the latest remote state:
   ```bash
   git pull --rebase origin main
   ```
   Rebase rewrites your local commits on top of the remote commits instead of creating a merge commit. If there are no upstream changes this is a no-op. If conflicts arise, Git pauses and tells you which file to edit — fix the conflict markers, `git add <file>`, then `git rebase --continue`.

5. Push your commits to the remote:
   ```bash
   git push origin main
   ```
   If the push is rejected with "non-fast-forward", someone pushed while you were rebasing. Repeat Step 4, then push again. Do not use `--force` on shared branches.

### Full session log (example)

```
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  modified:   src/auth/login.py

Untracked files:
  src/auth/tests/test_login.py

$ git add src/auth/login.py src/auth/tests/test_login.py
$ git status
On branch main
Changes to be committed:
  modified:   src/auth/login.py
  new file:   src/auth/tests/test_login.py

$ git commit -m "feat: add login endpoint with JWT"
[main 3f9c2a1] feat: add login endpoint with JWT
 2 files changed, 47 insertions(+), 2 deletions(-)

$ git pull --rebase origin main
Successfully rebased and updated refs/heads/main.

$ git push origin main
To github.com:alice-dev/myapp.git
   c8d4f02..3f9c2a1  main -> main
```

## Verify

Run this sequence after completing any coding session:

```bash
git log --oneline -5
```

Each line should show one focused commit message. No lines like "WIP", "asdf", "fix fix fix", or "merge branch main into main". If the log looks clean and the latest commit hash matches what `git push` reported, the workflow is working correctly.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `git push` rejected: "Updates were rejected because the remote contains work that you do not have locally" | Someone pushed to the same branch between your last pull and your push | Run `git pull --rebase origin main` again, then `git push` |
| Rebase paused mid-way with conflict markers (`<<<<<<<`) in a file | Two commits changed the same lines differently | Open the file, find the `<<<<<<< HEAD` / `>>>>>>> <sha>` markers, edit to the correct final state, run `git add <file>`, then `git rebase --continue` |
| `git add .` staged `.env` or `node_modules/` | Missing or incomplete `.gitignore` | Run `git reset HEAD .env` to unstage, add `.env` to `.gitignore`, commit the updated `.gitignore`, then re-stage only the intended files |
| Commit message too long — pre-commit hook blocks | Title line exceeds 50 characters (project hook enforces this) | Re-run with a shorter message: `git commit -m "fix: correct token expiry check"` |
| `git push --force` was used on a shared branch and a teammate's commits disappeared | Force push rewrites history and discards remote commits not in your local copy | Restore from the teammate's local branch or `git reflog` on their machine. Use `git push --force-with-lease` only on your own feature branch, never on `main` |

## Next

- [git-branching-basics](../git-branching-basics/playbook.md) — isolate each feature or fix in its own branch so the `main` history stays deployable at all times.
- Add a `.gitignore` for your stack at https://www.toptal.com/developers/gitignore to prevent secrets and build artefacts from being staged accidentally.
- Set `git config --global pull.rebase true` to make `--rebase` the default for every `git pull`, so you never create accidental merge commits.

## References

- [knowledge/free/dev/devtools-developer/github-repo-bootstrap](../../../knowledge/free/dev/devtools-developer/github-repo-bootstrap) — the squash-only merge model and linear-history branch-protection rules enforced by this methodology are exactly what the `git pull --rebase` step in Step 4 preserves; without rebasing locally, pushes to a repo configured this way will be rejected.
