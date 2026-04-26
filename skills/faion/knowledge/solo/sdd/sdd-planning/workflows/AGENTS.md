# SDD Workflows Navigation Hub

## Summary

Navigation hub for the three-phase SDD lifecycle: Spec Phase (requirements) → Design Phase
(technical blueprint) → Execution Phase (implementation). Provides phase-by-phase
input/output tables, a complete workflow path, and links to the detailed phase files.
This file routes; it does not instruct.

## Why

Agents receiving a vague task like "work on feature X" need to locate the current lifecycle
state before doing anything. Without a navigation entry point they either re-derive the phase
from artifact existence checks or jump straight to execution on an unapproved spec, producing
work that must be discarded. This hub makes the three-phase structure and transition criteria
explicit in one place.

## When To Use

- Starting work on a feature without knowing which SDD phase is active
- Bootstrapping a new project: constitution through first execution
- Switching phases mid-feature (spec approved, starting design)
- Explaining the SDD system to a new agent or contributor

## When NOT To Use

- Already in a specific phase and know what to do — go directly to the phase file
- As a substitute for phase-specific workflow files: this file is navigation, not instructions
- Looking for document templates — those live in `../template-spec/`, `../template-design/`, `../template-task/`

## Content

| File | What's inside |
|------|---------------|
| `content/01-phase-map.xml` | Three-phase structure, inputs/outputs per phase, complete workflow path, confidence thresholds, quality gate levels |
| `content/02-common-workflows.xml` | Quick-reference table: goal → which file to use; key principles (100k rule, quality gates, wave execution) |

## Templates

none

## Scripts

none
