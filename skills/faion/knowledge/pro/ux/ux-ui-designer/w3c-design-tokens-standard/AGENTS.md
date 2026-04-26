# W3C Design Tokens Standard

## Summary

A methodology for authoring design tokens that conform to the W3C Design Tokens Community Group
(DTCG) format module — using `$type`, `$value`, `$description`, and `{alias}` references — so
that the same token file can round-trip between Figma, Style Dictionary v4, and native platforms
without lossy remapping.

## Why

Every non-standard token format (custom Style Dictionary JSON, Theo, Tokens Studio) creates a
translation layer that loses type information, breaks aliases, or produces platform-specific
names. The DTCG format is the emerging interoperability standard already implemented by Tokens
Studio, Specify, Supernova, Penpot, and Style Dictionary v4. Adopting it now prevents a costly
migration when tooling locks in and prevents cross-tool collaboration on token ownership.

## When To Use

- Authoring a token source-of-truth that must round-trip between Figma and code platforms.
- Migrating a legacy Style Dictionary, Theo, or Tokens Studio file to vendor-neutral DTCG JSON.
- Setting up a shared token pipeline across web, iOS, Android, or React Native.
- Preparing for tooling that implements DTCG: Style Dictionary v4, Tokens Studio, Specify, Penpot.

## When NOT To Use

- Single-platform single-app project — DTCG overhead is not justified; CSS custom properties suffice.
- Fast spike or throwaway prototype — schema discipline slows iteration with no payoff.
- Team with no token naming discipline yet — fix primitives/semantic split first (`token-organization`).

## Content

| File | What's inside |
|------|---------------|
| `content/01-format.xml` | DTCG JSON structure: `$type`, `$value`, `$description`, alias syntax, group nesting. |
| `content/02-rules.xml` | Authoring rules, known `$type` gaps, alias resolver requirements, agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tokens.json` | Minimal DTCG-compliant token file with color, spacing, and typography groups. |
