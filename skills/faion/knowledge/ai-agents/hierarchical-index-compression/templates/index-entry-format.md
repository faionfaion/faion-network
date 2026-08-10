<!--
purpose: the index entry shape — what a routing entry may carry and what it must not.
consumes: leaf metadata (id, tier, produces, summary) from the corpus being indexed.
produces: index entries under the discriminator cap declared in index-budget-record.yaml.
depends-on: content/01-core-rules.xml (r2-entries-discriminate-not-describe)
token-budget-impact: this is the per-entry cost, multiplied by every entry in the index and by every lookup that reads it.
-->

# The entry

An index entry exists to answer one question: **would I open this leaf rather than
its neighbours?** It is not a catalogue record and not an abstract. Everything else
the reader might want is in the leaf, one read away, and paying for it in the index
means paying for it on every lookup that does not open that leaf — which is most of them.

## Shape

```
<id> | <routing keys> | <discriminator, <= 90 chars>
```

- **id** — stable, the path or slug the caller will open. Never a display title.
- **routing keys** — the fields the caller pre-filters on before reading any discriminator:
  tier, produces, complexity, owner, status. Enumerated values only; free text here is
  a second discriminator wearing a different hat.
- **discriminator** — one clause naming what makes this leaf the right choice *against
  its siblings*. Under the declared cap. Contrastive, not descriptive.

## Before and after

Restating the leaf — this is the failure (f2):

> **retrieval-cost-per-answer-audit** — Produces a Retrieval Cost Ledger over ten real
> queries, recording index tokens, candidate tokens, delivered-body tokens and
> correctness per query, then deriving median tokens per lookup and the overhead ratio
> that decides whether to compress, restructure or leave the retrieval structure alone.

That is 47 words the leaf already contains verbatim in its own metadata, paid again by
every lookup into this index, and it still does not say when to pick it over the four
neighbouring cost methodologies.

Discriminating — this is the target:

> `retrieval-cost-per-answer-audit | solo, measurement-ledger | when retrieval cost is unmeasured and a structure decision is blocked on the number`

Fourteen words, and the reader now knows precisely when to open it. Note what the
compressed form gained rather than lost: the original never mentioned the blocked
decision, which is the only reason anyone reaches for this leaf.

## Test for a discriminator

Read the entry with the leaf's siblings covered. If it could be describing any of
three neighbours, it is a description. If removing it would not change which leaf a
reader opens, delete it and save the tokens.

## What never goes in

The fields listed under `leaf_owns` in the budget record — typically the full summary,
the body, and any rationale or evidence. Also: word counts, dates, author names, and
anything a filter can key on that is not already a routing key. These are the fields
that grow an index faster than its corpus.

## Sharding (r4)

When a level crosses `shard_trigger_tokens`, split it on the declared partition key and
leave a stub at the original path with one row per shard — same entry shape, the
discriminator now describing the shard rather than a leaf:

```
dev/backend/INDEX | 61 entries | server-side runtime, data access, job scheduling
dev/frontend/INDEX | 58 entries | browser runtime, rendering, client state
```

The caller's first read is now the stub, not the whole level. Do not respond to the
trigger by trimming entries: that removes discrimination, not cost, and the regression
lands in routing quality rather than in the budget.
