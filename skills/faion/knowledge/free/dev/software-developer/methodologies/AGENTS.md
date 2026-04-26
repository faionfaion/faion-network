# Software Developer Methodology Index

## Summary

A dispatcher index for the software-developer skill. Not a standalone methodology — maps task keywords to the canonical sibling methodology folder under `free/dev/software-developer/`. Each sibling contains the full, authoritative content; this index gives the agent a starting routing point only.

## Why

The legacy umbrella README listed 68 patterns as 5-line stubs, causing agents to produce shallow output by quoting stubs instead of loading the real sibling content. This index encodes the routing table and explicitly forbids agents from implementing directly from it.

## When To Use

- Routing a coarse task ("implement a Django service", "scaffold a Go API") to the correct sibling folder.
- Building a multi-step plan that requires knowing the canonical order: Python → JS/TS → backend → DevOps → docs.
- Auditing which methodology slugs exist before dispatching parallel subagents.

## When NOT To Use

- Implementing from this file directly — every entry is a routing pointer, not a spec.
- Treating it as authoritative best-practices guidance — pull current guidance from each sibling.
- Citing it as the source of any rule — cite the sibling folder instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-routing-index.xml` | Slug table mapping task domains to sibling folder names; dispatch rules. |
| `content/02-gotchas.xml` | Known agent failure modes when using this index (stub seduction, hallucinated agent names, outdated snippets). |

## Templates

none

## Scripts

| File | Purpose |
|------|---------|
| `scripts/stub-detect.sh` | Lists sibling methodologies whose README is too thin (< 80 lines) to be actionable. |
