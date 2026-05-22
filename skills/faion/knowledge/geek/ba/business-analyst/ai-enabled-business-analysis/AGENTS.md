---
slug: ai-enabled-business-analysis
tier: geek
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for integrating AI tools into core BA workflows: requirements extraction from documents using NLP, stakeholder sentiment analysis, process discovery via process mining, and AI-accelerated BA documentation (acceptance criteria, gap analyses, RACI matrices).
content_id: "c5e6da8efc613786"
tags: [business-analysis, ai-integration, requirements, governance, agentic-systems]
---
# AI-Enabled Business Analysis

## Summary

**One-sentence:** A methodology for integrating AI tools into core BA workflows: requirements extraction from documents using NLP, stakeholder sentiment analysis, process discovery via process mining, and AI-accelerated BA documentation (acceptance criteria, gap analyses, RACI matrices).

**One-paragraph:** A methodology for integrating AI tools into core BA workflows: requirements extraction from documents using NLP, stakeholder sentiment analysis, process discovery via process mining, and AI-accelerated BA documentation (acceptance criteria, gap analyses, RACI matrices). Covers the BA's role in agentic system specifications — defining agent boundaries, human oversight requirements, and escalation criteria. Applies the Gartner AI TRiSM (Trust, Risk, Security Management) framework to AI initiative requirements.

## Applies If (ALL must hold)

- Extracting requirements from large document corpora (contracts, transcripts, RFPs) where manual reading is impractical
- Performing stakeholder sentiment analysis on communication logs before requirements prioritization
- Generating first-draft requirements documents, acceptance criteria, or gap analysis reports
- Validating AI initiative requirements against the AI TRiSM framework
- Defining agent boundaries, escalation rules, and human oversight requirements for an agentic AI initiative

## Skip If (ANY kills it)

- Requirements involve sensitive stakeholder dynamics where AI analysis of communications is ethically inappropriate
- Domain is too specialized for the model's training — hallucinations on domain terms produce plausible-but-wrong requirements
- Organization has not assessed data privacy obligations for feeding stakeholder communications to an external AI model
- The BA role is primarily facilitation (workshops, negotiations) — AI adds little value in real-time human facilitation

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ba/business-analyst/`
