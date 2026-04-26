# PM Tools Overview

## Summary

A structured framework for selecting the right project management tool based on team size, workflow complexity, compliance requirements, and ecosystem fit. The core rule: anchor every tool selection to a MoSCoW requirements table grounded in stakeholder evidence, then apply hard constraints (price ceiling, data residency, compliance, IDP) to produce a shortlist of 3-5 candidates before evaluating features.

## Why

Tool selections driven by executive preference, hype, or feature-list comparisons routinely fail at adoption. Anchoring to documented requirements with verbatim evidence forces rigor and makes the decision defensible during post-mortem reviews. A weighted scorecard with sensitivity analysis reveals when the "winner" is fragile (ranking flips under reasonable weight perturbations).

## When To Use

- Starting a new team or project without existing tooling.
- Outgrowing a current PM solution (capacity, compliance, or integrations).
- Consolidating multiple tools across an organization after merger or acquisition.
- Evaluating tools during vendor renewal when pricing model changes.
- Post-acquisition tool standardization requiring a defensible ADR.

## When NOT To Use

- Single-team / solo decision with low switching cost — pick by gut, time-box a 2-week trial, ship.
- Switching tools to escape a process or personnel problem — fix the root cause instead.
- A tool already works with no measurable pain — overhead exceeds value.
- Pre-product-market-fit startups — tool-selection theatre distracts from product.
- Decisions already locked by executive preference or vendor relationship — analysis will not change the outcome.

## Content

| File | What's inside |
|------|---------------|
| `content/01-tool-profiles.xml` | Quick-reference comparison of 10 major PM tools: strengths, weaknesses, team-size fit. |
| `content/02-selection-process.xml` | MoSCoW requirements gathering, weighted scoring, sensitivity analysis, ADR output format. |
| `content/03-agent-usage.xml` | Agentic workflow: requirements-distiller, vendor-shortlister, poc-runner, scoring-agent, decision-writer. Gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/requirements-doc.md` | Stakeholder-interview questions and MoSCoW requirements matrix template. |
| `templates/poc-runner.py` | Minimal POC scenario harness that drives scripted tasks against any REST-enabled PM tool. |
