<!--
purpose: Markdown skeleton for a Single Interview Fast Loop Template artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/single-interview-fast-loop-template.json.
token-budget-impact: ~250 tokens.
-->

# Single Interview Fast Loop Template — <artefact_id>

- **loop_id** (string): <stable_id>
- **decision_under_test** (string): <the one decision the loop informs>
- **must_asks** (array): <3–5 past-tense questions>
- **interview_at** (datetime): <iso_datetime>
- **synthesis_due_at** (datetime): <interview_at + ≤36h>
- **synthesis_outcome** (string): <decide-yes | decide-no | park | re-interview>
- **citation_path** (string): <path to transcript in research repo>
- **owner** (string): <named_researcher>
- **version** (string): <document_version>
- **last_reviewed** (date): <last_reviewed_date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
