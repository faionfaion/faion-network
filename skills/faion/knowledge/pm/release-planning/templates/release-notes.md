<!--
purpose: Customer-facing release notes template.
consumes: input from methodology
produces: artefact for downstream agent
depends-on: content/02-output-contract.xml
token-budget-impact: ~200-500 tokens when loaded as context
variables:
  - name: version
    type: string
    required: true
    description: The released version, semver. Read it off the tag, not off the plan - this string is the anchor for every support conversation about this change for the next year.
  - name: date
    type: string
    required: true
    description: Date this actually reached users, ISO. Not the merge date and not the planned date; support correlates incidents against the day behaviour changed for real people.
  - name: highlights
    type: text
    required: true
    description: One or two plain sentences leading with what changed for the user. The lint rejects excited, seamless, powerful and revolutionary - write what a user would tell a colleague in a corridor.
  - name: support_link
    type: string
    required: true
    description: Where a reader goes when this release broke something for them. A release note with no exit is a wall people shout at on social media instead of a channel you can answer.
  - name: has_breaking_changes
    type: boolean
    required: true
    description: Does this break anything a caller depends on - an API shape, a default, a removed field? If yes, the Breaking Changes section must carry migration steps, not a warning. If you are unsure, the answer is yes.
sections:
  - name: breaking
    description: Breaking changes and the migration steps for them.
    when: has_breaking_changes in [true]
-->

# v{{version}} ({{date}})

## Highlights
{{highlights}}

## New
- [Feature name]: [what it does and why it matters — customer-observable outcome]

## Improved
- [Change]: [observable user impact]

## Fixed
- Fixed [issue description] — [link to public issue if any]

<!-- faion:section breaking -->
## Breaking Changes

- [What broke]: [migration steps, command by command — not just a warning]
<!-- faion:endsection -->

## Known Issues
- [Issue]: workaround [solution if any]

## Deprecations
[Timeline + replacement path. Omit section if none.]

---
Questions? {{support_link}}

<!-- Anti-fluff rules (enforced by lint):
  - No "excited", "delighted", "thrilled", "powerful", "seamless", "next-gen", "revolutionary"
  - No internal codenames without a one-line gloss
  - Omit empty sections entirely — do not write "None"
  - Each bullet cites its merge SHA in an HTML comment for traceability
  - Known Issues is required if any exist; absence for 2+ releases is a smell
-->
