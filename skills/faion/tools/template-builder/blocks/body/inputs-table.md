<!--
purpose: The Inputs section as a Name/Format/Source table. Byte-identical in 76 templates; the column set is the input contract itself, which is why it is the same everywhere and correctly so.
consumes: one input row
produces: an H2 Inputs section with a three-column table
depends-on: nothing
token-budget-impact: ~40 tokens
variables:
  - name: input_name
    type: string
    required: true
    default: "[input-1]"
    description: Name of the input, as the Prerequisites table calls it.
  - name: input_format
    type: string
    required: true
    default: "[format]"
    description: Format of the input, e.g. JSON, CSV, transcript, design file.
  - name: input_source
    type: string
    required: true
    default: "[source]"
    description: Where the input comes from — path, URL or system of record.
-->
## Inputs

| Name | Format | Source |
|------|--------|--------|
| {{input_name}} | {{input_format}} | {{input_source}} |
