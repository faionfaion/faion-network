The search for `{{slot:query}}` is lexical and local. It matched
**{{slot:matched}}** of your terms against a returned document and rates its own
coverage **{{slot:level}}**.

Terms that no returned document carried: {{slot?:unmatched}}

The corpus is written in English, and a document is matched on its path, its
title and an 80-character summary — not on its body. So a query that describes
a *situation* usually loses to one that uses the *vocabulary a methodology
would put in its own title*. "my writes get duplicated when a call is retried"
finds less than "idempotency keys". You have the session and a model; the CLI
has neither. Rewriting the query is your half of this.

**To run the second pass**, either execute the `<next>` line verbatim — it
retries with your unmatched terms pinned — or replace its `--terms` with better
ones:

- Prefer nouns the corpus would use as a slug: `retry-backoff`, `message-queues`,
  `idempotency-keys`. A term that *is* a document's slug pins that document into
  the result whatever the scoring says.
- Use `--domain` or `--kind` only when the `<distribution>` histogram shows the
  wrong area dominating the shortlist. They are hard filters: a wrong guess
  removes the answer instead of demoting it.
- Use `--not` to drop a term that is flooding the result, not to express a
  preference.

**There is no third pass** ({{slot:pass}} of {{slot:max_pass}}). A pass-2 result
carries no refine block and no next line, and that absence is the instruction:
stop, and answer from what you have — including "the corpus does not cover
this", which is a correct answer and cheaper than a confident wrong one.
