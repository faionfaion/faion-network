# Release Planning

## Summary

A six-step process for deciding what goes into each release, when it ships, and how
it is communicated. Covers release-type taxonomy (major/minor/patch/hotfix),
readiness checklists, rollback requirements, and audience-specific communication
plans. The concrete rule: every release needs a goal statement, a rollback plan, and
a communication plan before code touches production.

## Why

Releases without structure are chaotic, missed, or anticlimactic — features are ready
but not shipped, or shipped without communication, or broken in production with no
rollback path. A structured approach prevents the three most common failure modes:
scope creep into a release, skipping staging, and going dark to customers.

## When To Use

- Planning what to include in an upcoming version (major, minor, patch, or hotfix).
- Coordinating release timing across engineering, support, and marketing.
- Writing release notes for an existing set of changes.
- Setting up a repeatable release cadence for a solo or small-team product.

## When NOT To Use

- Continuous deployment with feature flags — individual flag decisions replace release bundling.
- Pre-launch, pre-user products — no communication audience yet, use task lists instead.
- Emergency hotfixes under time pressure — use the hotfix checklist only, not the full plan.

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | Six-step release process with release types, readiness checklist, and post-release loop. |
| `content/02-antipatterns.xml` | Seven common mistakes (Friday deploys, no rollback, last-minute additions, etc.) with fixes. |
| `content/03-examples.xml` | SaaS monthly release and solo patch release worked examples. |

## Templates

| File | Purpose |
|------|---------|
| `templates/release-plan.md` | Full release plan: metadata, goal, contents, dependencies, risks, rollback plan, communication plan, timeline. |
| `templates/release-notes.md` | Release notes template: highlights, new features, improvements, bug fixes, breaking changes. |
