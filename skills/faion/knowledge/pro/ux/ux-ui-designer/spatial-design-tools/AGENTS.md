# Spatial Design Tools

## Summary

A phase-gated tool selection methodology for spatial (AR/VR/MR) product workflows: concept in Figma + ShapesXR, prototype in Unity or Unreal, production in engine. Standardize on USD/USDZ for visionOS, glTF for Web/Quest handoff. Asset-budget constraints (polygon count, file size) must be set at concept stage, not after artist work is done.

## Why

Traditional 2D design tools have no first-class spatial canvas. Teams that pick tools per project rather than per phase accumulate file-format friction (USDZ, glTF, FBX, USD, Unity prefabs) that breaks asset pipelines mid-sprint. Setting polygon and texture budgets early prevents the most common rework loop — artists over-build, optimizing assets under deadline pressure.

## When To Use

- Choosing or reviewing a tool stack for a new AR/VR/MR project.
- Setting up designer-to-developer handoff path (Figma 2D wireframes → ShapesXR → Unity/Unreal).
- Evaluating a solopreneur stack for visionOS, Quest, or WebXR delivery.
- Onboarding designers from 2D backgrounds onto a spatial workflow.

## When NOT To Use

- 2D-only projects — spatial tool overhead yields no benefit.
- Teams already locked into a vendor mid-project — switching costs exceed gains.
- Marketing-only AR effects — Spark AR / Lens Studio handle that niche; the full landscape is overkill.

## Content

| File | What's inside |
|------|---------------|
| `content/01-tool-landscape.xml` | Tool matrix by phase (concept/prototype/production), device targets, and format standards. |
| `content/02-pipeline-rules.xml` | Asset-budget rules, format-choice rules, CI lint script, agentic workflow guidance. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spatial-budget.sh` | CI script: fail build if glTF asset exceeds polygon or size budget. |

## Scripts

none
