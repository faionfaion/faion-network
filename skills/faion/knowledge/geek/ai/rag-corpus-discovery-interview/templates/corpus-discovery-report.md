<!-- purpose: corpus-discovery-report narrative skeleton -->
<!-- consumes: corpus-discovery-report.json -->
<!-- produces: review draft for RAG engineer + product owner -->
<!-- depends-on: content/02-output-contract.xml schema -->
<!-- token-budget-impact: ~400 tokens loaded as context -->

# Corpus Discovery — `<artefact_id>`

- **Owner:** `<handle>`
- **Version:** `1.0.0`
- **Last reviewed:** `2026-05-22`

## Guide prompts

1. Walk me through the last time you looked up <topic>.
2. Show me where the answer actually lives in your tools.
3. Tell me about a time the answer was wrong or stale.
4. Describe how you decide which source to trust.
5. Which document classes are licensed for embedding?

## Interviews

| transcript_id | role | recording |
|---|---|---|
| t1 | <role> | s3://<bucket>/t1.m4a |
| t2 | <role> | s3://<bucket>/t2.m4a |
| t3 | <role> | s3://<bucket>/t3.m4a |
| t4 | <role> | s3://<bucket>/t4.m4a |
| t5 | <role> | s3://<bucket>/t5.m4a |

## Findings

| id | label | evidence |
|---|---|---|
| f1 | finding | t1@00:08:42, t3@00:05:18 |
| f2 | hypothesis | t2@00:12:10 |
