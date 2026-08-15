<!--
purpose: corpus-discovery-report narrative skeleton
consumes: corpus-discovery-report.json
produces: review draft for RAG engineer + product owner
depends-on: content/02-output-contract.xml schema
token-budget-impact: ~400 tokens loaded as context
variables:
  - name: slug
    type: string
    required: true
    description: Kebab-case name of the corpus being scoped - the knowledge base, not the product it will serve. The eval set built later has to carry the same name or the two drift apart.
  - name: owner
    type: string
    required: true
    description: Handle of the RAG engineer who owns this discovery, not the product owner who asked for it. One name; this document gets argued about and needs someone to defend it.
  - name: lookup_topic
    type: text
    required: true
    description: The thing you will ask people to recall looking up, in their words. Concrete enough that they remember a specific occasion - "the refund window for EU orders", never "policy".
  - name: recording_bucket
    type: string
    required: true
    description: Where the interview recordings actually land, e.g. s3://acme-research. If there is no durable location, the findings below cannot be re-checked and are hearsay with timestamps.
  - name: licensed_classes
    type: text
    required: true
    description: Which document classes are licensed for embedding, and who confirmed it on what date. Corpora get built out of documents nobody had the right to index; this line is where that is caught.
-->

# Corpus Discovery — `{{slug}}`

- **Owner:** `{{owner}}`
- **Version:** `1.0.0`
- **Last reviewed:** `2026-05-22`

## Guide prompts

1. Walk me through the last time you looked up {{lookup_topic}}.
2. Show me where the answer actually lives in your tools.
3. Tell me about a time the answer was wrong or stale.
4. Describe how you decide which source to trust.
5. Which document classes are licensed for embedding?

## Licensing

{{licensed_classes}}

## Interviews

| transcript_id | role | recording |
|---|---|---|
| t1 | [role] | {{recording_bucket}}/t1.m4a |
| t2 | [role] | {{recording_bucket}}/t2.m4a |
| t3 | [role] | {{recording_bucket}}/t3.m4a |
| t4 | [role] | {{recording_bucket}}/t4.m4a |
| t5 | [role] | {{recording_bucket}}/t5.m4a |

## Findings

| id | label | evidence |
|---|---|---|
| f1 | finding | t1@00:08:42, t3@00:05:18 |
| f2 | hypothesis | t2@00:12:10 |
