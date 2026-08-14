Commit discipline — binding on every file your role writes.

A deliverable git has never seen does not survive a clone, and a
deploy script that copies a working tree ships it anyway. That is how
"ready to deploy" comes to be satisfied by files that are not in the
repository: two pipeline runs ended with 23 and 9 untracked
deliverables and both reported success. The run now checks, so an
uncommitted file fails the stage that wrote it rather than the
release that needed it.

This block adds rules; it never widens your boundary. It authorises
exactly two git commands for exactly the paths your own output
contract names — `git add` and `git commit` — and nothing else.

- Stage explicit paths, the ones your output contract names. Never
  `git add -A`, never `git add .`; a bulk stage sweeps in whatever
  else the run left lying around and calls it yours.
- Commit before you finish. One commit, or one per logical group:
  title `type: short description` within 50 characters, no
  Co-Authored-By trailer, no emojis, plus whatever changelog entry
  the repository requires.
- Never `--no-verify`, never `--amend` a commit you did not make in
  this stage, never push, rebase, reset or force anything.
- Leave the paths you touched clean. The run reads them back with
  `git ls-files --error-unmatch` and `git status --porcelain`, and an
  untracked or still-modified deliverable fails the stage.
- If you could not produce a deliverable, say so plainly and commit
  nothing in its place. An empty commit is not a deliverable, and a
  file committed to satisfy the check is worse than the missing one:
  it fails later, further from the stage that owed it.
