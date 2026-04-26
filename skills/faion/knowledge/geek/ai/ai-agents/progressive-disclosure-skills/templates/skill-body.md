# Faion Deploy

> Procedure-only body. Loads on activation. Defers details to `references/`.

## When this skill applies

User asks to deploy any faion-net surface. If the request is about NERO
(nero-prod), use `nero-deploy` instead.

## Procedure

1. Confirm 1Password is unlocked: `op-unlock` or `source ~/bin/op_unlock.sh`.
2. Identify target. If unclear, ask which surface (faion.net | dev | api |
   storybook | roadmap | neromedia | pashtelka | longlife | ender).
3. Run the matching script:
   - faion.net → `bash projects/faion.net/deploy-gh.sh`
   - dev.faion.net → `bash projects/faion-net/deploy-fe-dev.sh`
   - api.faion.net → `bash projects/faion-net/deploy-be.sh`
   - storybook → `bash projects/faion-net/deploy-storybook.sh`
   - roadmap → `bash projects/faion-net/deploy-roadmap.sh`
   - neromedia → `bash projects/neromedia-faion-net/gatsby/deploy-gh.sh`
   - pashtelka → `bash projects/pashtelka-faion-net/gatsby/deploy-gh.sh`
   - longlife → `bash projects/longlife-faion-net/gatsby/deploy-gh.sh`
   - ender → `bash projects/ender-faion-net/gatsby/deploy-gh.sh`
4. Verify: Read `references/post-deploy-checks.md` and run the checks.
5. Notify: `tg-send "deployed <surface>"` on success.

## On failure

Read `references/rollback.md` for surface-specific rollback steps.

## Detailed references (load on demand)

- `references/post-deploy-checks.md` — health endpoints, TLS, DNS sanity.
- `references/rollback.md` — per-surface rollback (rsync from backup, git revert).
- `references/troubleshooting.md` — common stuck states and fixes.

## Scripts

- `scripts/select-target.sh` — interactive picker when surface is ambiguous.
