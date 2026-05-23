<!--
purpose: 5-line CEO email body (state + 3 numbers + 1 risk)
consumes: source spreadsheet (RAG, progress, budget, risks)
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~100-300 tokens when loaded as context
-->
Subject: {project} — Week {n} — {On plan|Slipping|At risk}

State:   {On plan|Slipping|At risk}.
Numbers: {progress %} complete · {budget %} of budget · {weeks to next milestone}.
Risk:    {one risk OR ask in 1-2 lines}.
