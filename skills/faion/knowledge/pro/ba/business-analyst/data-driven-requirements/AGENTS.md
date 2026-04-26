# Data-Driven Requirements Engineering

## Summary

An evidence-based approach to requirements definition that replaces opinion-driven prioritization with data analytics. Each requirement is anchored to a business question, quantified baseline metrics, and a measurable success target. Prioritization uses usage data, performance data, business metrics, and customer feedback rather than stakeholder seniority or gut feel.

## Why

Requirements based on stakeholder opinion are frequently wrong about user needs and business impact; prioritization becomes political; success metrics are defined post-implementation when the team wants to declare victory. Data-driven engineering anchors every requirement to evidence, establishes the baseline before development, and locks success criteria upfront so measurement cannot be gamed.

## When To Use

- Prioritizing a backlog where features compete for limited capacity and ROI data is available
- Feature validation before investment when analytics (usage, conversion, error rate) can answer the business question
- Post-MVP iteration where product analytics reveal which flows users actually take
- A/B test design where the requirement specifies what hypothesis is being tested and what outcome declares success
- AI/ML feature scoping where business impact measurement (cycle time, CSAT, error rate) must be defined before model training

## When NOT To Use

- Greenfield products with no users and no baseline — hypothesis-driven development (Lean Startup) applies before data exists
- Requirements driven by compliance or legal obligation where the mandate, not ROI, is the reason to build
- One-off internal tooling with a known, small user group where analytics instrumentation cost exceeds value
- When the organization has no analytics tooling and instrumenting is out of scope — gather qualitative evidence instead

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Evidence-based process (business question → data → analysis → insight → requirement), analytics competencies, tool categories |
| `content/02-analytics-prioritization.xml` | Metric types for prioritization, self-service analytics tools, AI/ML ROI measurement framework across four impact areas |
| `content/03-examples.xml` | Data-driven requirement specification example, success metrics with baseline/target/measurement method, validation plan |

## Templates

| File | Purpose |
|------|---------|
| `templates/data-driven-req.md` | Requirement template with business context, data sources table, analysis summary, success metrics, and A/B validation plan |
