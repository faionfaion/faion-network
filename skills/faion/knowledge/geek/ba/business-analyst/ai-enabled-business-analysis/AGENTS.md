# AI-Enabled Business Analysis

## Summary

A methodology for integrating AI tools into core BA workflows: requirements extraction from documents using NLP, stakeholder sentiment analysis, process discovery via process mining, and AI-accelerated BA documentation (acceptance criteria, gap analyses, RACI matrices). Covers the BA's role in agentic system specifications — defining agent boundaries, human oversight requirements, and escalation criteria. Applies the Gartner AI TRiSM (Trust, Risk, Security Management) framework to AI initiative requirements.

## Why

Traditional requirements gathering is manual, time-consuming, and inconsistent. AI tools accelerate the drafting phase, but 60% of AI project failures trace to poor data quality — the BA's data quality assessment is the highest-leverage early activity. NLP-extracted requirements lack implicit knowledge; they are starting points, not final deliverables. AI TRiSM compliance is expected to improve AI adoption success rates by 50% by 2026 (Gartner).

## When To Use

- Extracting requirements from large document corpora (contracts, transcripts, RFPs) where manual reading is impractical
- Performing stakeholder sentiment analysis on communication logs before requirements prioritization
- Generating first-draft requirements documents, acceptance criteria, or gap analysis reports
- Validating AI initiative requirements against the AI TRiSM framework
- Defining agent boundaries, escalation rules, and human oversight requirements for an agentic AI initiative

## When NOT To Use

- Requirements involve sensitive stakeholder dynamics where AI analysis of communications is ethically inappropriate
- Domain is too specialized for the model's training — hallucinations on domain terms produce plausible-but-wrong requirements
- Organization has not assessed data privacy obligations for feeding stakeholder communications to an external AI model
- The BA role is primarily facilitation (workshops, negotiations) — AI adds little value in real-time human facilitation

## Content

| File | What's inside |
|------|---------------|
| `content/01-workflow.xml` | AI-assisted BA workflow rules; requirements extraction; traceability requirement |
| `content/02-trism.xml` | AI TRiSM framework application; agentic system BA role; acceptance criteria quality |

## Templates

| File | Purpose |
|------|---------|
| `templates/requirements-extractor.py` | Extract requirements from a PDF using Claude; returns structured list with source refs |
| `templates/prompt-requirements.txt` | Prompt for structured requirements extraction with ID, type, source, ambiguity flag |
| `templates/prompt-gap-analysis.txt` | Prompt for gap analysis between current and target state |
