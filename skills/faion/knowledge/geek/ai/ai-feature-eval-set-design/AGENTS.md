---
slug: ai-feature-eval-set-design
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Concrete template for designing a regression eval set for a shipping AI feature — gold rows, adversarial rows, drift watch — with judge selection, versioning, and CI wiring suitable for a non-ML PM or QA engineer.
content_id: 51f2534fc84d8546
---

# AI Feature Eval Set Design

## Summary
A tier-appropriate methodology for PMs and QA engineers shipping a chatbot, copilot, or classifier who need a regression eval set without becoming an ML engineer. Covers: gold-data sourcing, edge-case curation, judge selection (heuristic vs LLM-as-judge vs human), versioning rules, and CI gating thresholds. Outcome: a versioned eval set, a scoring harness, and a CI signal that fails a build on regression — for any AI feature.

## Applies If
- You ship an AI feature (chat, copilot, classifier, RAG, agent) to real users
- The feature has a definable correct/incorrect outcome on at least some inputs
- You can collect or generate ≥50 representative input examples
- You have a CI pipeline you can extend with a new check

## Skip If
- The feature is purely generative with no correctness criterion (creative copy, art)
- You have <20 weekly users (eval set has no signal; ship and watch first)
- You are doing offline research, not shipping (use ml-engineer eval cookbook)
- You already have eval coverage with judge calibration (then use eval-contract-template)

## Content
See `content/01-core-rules.xml`.

## Related
- [[eval-contract-template]]
- [[eval-set-stratified-sampling-recipe]]
- [[judge-calibration-protocol]]
- [[model-migration-checklist]]
