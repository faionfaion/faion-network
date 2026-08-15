<!--
purpose: 15-minute quick spec — problem, requirements, design sketch, tasks, acceptance
consumes: a single feature request small enough to scope in one sitting
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~250-600 tokens when loaded as context
variables:
  - name: feature_name
    type: string
    required: true
    description: The feature or task, named the way the branch will name it. This is a 15-minute spec - if naming it takes more than a minute, it is too big for this template and wants the full one.
  - name: problem
    type: text
    required: true
    description: What breaks today without this, and for whom. Concrete enough that someone could disagree - "users are confused" is a survey summary, not a problem statement.
  - name: requirement_one
    type: text
    required: true
    description: The first thing the system must do, observable from outside it. If it names a class or a file, it is a task and belongs three sections further down.
  - name: out_of_scope
    type: text
    required: true
    description: What you are deliberately not doing. In a 15-minute spec this is the field that does the work - without it the task list keeps growing for a week and the spec expires.
  - name: approach
    type: text
    required: true
    description: Two or three sentences on the technical approach and the one decision that matters. Say what you rejected: the next person's first question is always "why not X".
  - name: done_when
    type: text
    required: true
    description: The acceptance criterion, verifiable and singular. If saying when this is done takes three sentences, the feature is not scoped for a quick spec yet.
-->
# Quick Spec: {{feature_name}}

<!-- 15-minute waterfall template. Fill in order; stop after 15 minutes total. -->

## Problem (2 min)

{{problem}}

---

## Requirements (5 min)

- [ ] R1: {{requirement_one}}
- [ ] R2: [Requirement]
- [ ] R3: [Requirement]

**Out of scope:**

{{out_of_scope}}

---

## Design Sketch (5 min)

**Files to change:**
- CREATE: `[path/to/new-file.ext]` — [purpose]
- MODIFY: `[path/to/existing-file.ext]` — [what changes]

**Approach:**
{{approach}}

---

## Tasks (3 min)

1. [ ] [Task 1 — maps to R1]
2. [ ] [Task 2 — maps to R2]
3. [ ] [Task 3]
4. [ ] [Task 4 — optional]

---

## Done When

- {{done_when}}
- [Acceptance criterion 2]
- [Acceptance criterion 3]
