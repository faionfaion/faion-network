<!-- purpose: voice dialogue authoring template -->
<!-- consumes: use-case + persona -->
<!-- produces: 3+ sample dialogues per intent -->
<!-- depends-on: content/01-core-rules.xml dialogues-before-code rule -->
<!-- token-budget-impact: ~200 tokens when loaded as context -->

# Intent: <name>

## Dialogue 1 (happy path)
User: <natural wording>
Assistant: <≤12 words>
User: <follow-up>
Assistant: <≤12 words>

## Dialogue 2 (missing slot)
User: <utterance without time>
Assistant: <rephrase prompt>
User: <provides slot>
Assistant: <confirms>

## Dialogue 3 (error recovery)
User: <ambiguous utterance>
Assistant: <tier-1 rephrase>
User: <still ambiguous>
Assistant: <tier-2 examples>
