# Slash-Command Surface for PR Review Bots

## Summary

Expose review-bot capabilities as PR-comment slash commands so humans steer the bot in-band rather than through a separate dashboard. Qodo Merge / PR-Agent set the standard: `/describe` regenerates title and walkthrough, `/review` posts inline issues, `/improve` posts code-suggestion patches you can apply with one click, `/ask "why does this regex differ?"` queries the diff. Auto-trigger `/describe` plus `/review` on PR open and re-push; leave `/improve` opt-in (it's the noisy one). CodeRabbit (`@coderabbitai resolve|review`) and Sourcery follow the same surface.

## Why

Without slash commands, humans must visit a vendor dashboard or re-push a commit to re-trigger a bot — slow, friction-heavy, and outside the PR audit trail. With slash commands, every steering action is a comment in the PR, captured by GitHub history, and reproducible without leaving the review thread. Auto-running `/describe` and `/review` on open keeps the cheap-and-useful surface always-on; gating `/improve` behind explicit invocation prevents suggestion-patch noise from drowning real review.

## When To Use

- Multi-author repos where humans want a "second pair of eyes" before requesting human review.
- High-PR-volume repos (>20/day) where humans drown in description-writing.
- Repos already using a slash-command-capable bot (Qodo Merge, CodeRabbit, Sourcery).
- Open-source repos where contributors lack institutional context to describe risk in PR bodies.

## When NOT To Use

- Tiny PRs (<20 LOC) — `/review` adds more noise than it removes.
- Repos with strict "no third-party app on source" policy without a self-hosted PR-Agent install.
- Single-author repos where the author already writes the description — auto-describe overwrites it.
- Compliance setups where bot comments must be pre-approved before posting.

## Content

| File | What's inside |
|------|---------------|
| `content/01-command-surface.xml` | Standard command vocabulary; auto-trigger policy; idempotent describe block. |

## Templates

| File | Purpose |
|------|---------|
| `templates/qodo-merge.yml` | GitHub Actions workflow for Qodo Merge with auto-describe/auto-review. |
| `templates/pr-description-block.md` | HTML-comment-delimited block separating bot output from human edits. |
