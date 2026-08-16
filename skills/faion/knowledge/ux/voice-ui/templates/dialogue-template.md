<!-- purpose: voice dialogue authoring template -->
<!-- consumes: use-case + persona -->
<!-- produces: 3+ sample dialogues per intent -->
<!-- depends-on: content/01-core-rules.xml dialogues-before-code rule -->
<!-- token-budget-impact: ~200 tokens when loaded as context -->

# Intent: <name>

## Dialogue 1 (happy path)
User: <natural_wording>
Assistant: <≤12 words>
User: <follow_up>
Assistant: <≤12 words>

## Dialogue 2 (missing slot)
User: <utterance_without_time>
Assistant: <rephrase_prompt>
User: <provides_slot>
Assistant: <confirms>

## Dialogue 3 (error recovery)
User: <ambiguous_utterance>
Assistant: <tier_1_rephrase>
User: <still_ambiguous>
Assistant: <tier_2_examples>
