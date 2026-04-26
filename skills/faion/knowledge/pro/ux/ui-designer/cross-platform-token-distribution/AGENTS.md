# Cross-Platform Token Distribution

## Summary

A pipeline pattern for distributing design tokens from a single source (Tokens Studio / Figma) to multiple platform outputs — CSS variables, SCSS maps, iOS Swift, Android XML, React Native — using Style Dictionary as the transform engine. Tokens are authored once and emitted per-platform via config-driven transforms; CI blocks merges when outputs drift from source.

## Why

Without a shared pipeline, per-platform token copies diverge silently. A wrong primary color ships on iOS while web stays correct. Style Dictionary's transform groups isolate platform quirks (rem→dp, hex→UIColor) without polluting the shared source, and a CI drift check makes drift visible before it reaches users.

## When To Use

- Setting up a multi-platform product (web + iOS + Android) with shared brand tokens.
- Migrating a web-only token set to cover native platforms.
- Adding CI gates that fail when generated platform outputs are stale relative to source.
- Auditing drift between Figma token export and shipped artifacts.

## When NOT To Use

- Single-platform web-only products — Style Dictionary adds pipeline complexity with no payoff.
- Pre-design-system phase where the token contract is still unstable; pipeline churn exceeds value.
- Brand assets that change every campaign — distribution overhead exceeds reuse benefit.
- Closed mobile apps with a single developer who hand-edits XML — overhead exceeds saved minutes.

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline.xml` | Pipeline stages, tool roles, platform output formats, CI drift check pattern. |
| `content/02-gotchas.xml` | Agent pitfalls, common failure modes, and best practices for automated token pipelines. |

## Templates

| File | Purpose |
|------|---------|
| `templates/style-dictionary-config.json` | Style Dictionary config skeleton for CSS, SCSS, iOS, Android, React Native outputs. |
| `templates/tokens-drift-check.sh` | CI script that fails if Style Dictionary outputs are stale relative to source. |

## Scripts

none
