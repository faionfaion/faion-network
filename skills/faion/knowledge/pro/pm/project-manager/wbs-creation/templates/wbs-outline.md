<!-- purpose: Hierarchical WBS outline skeleton with append-only IDs and noun-only naming. -->
<!-- consumes: scope statement + glossary + (optional) architecture sketch -->
<!-- produces: outline that converts 1:1 into items[] of the WBS spec -->
<!-- depends-on: content/01-core-rules.xml#deliverable-orientation, mandatory-overhead-branches -->
<!-- token-budget-impact: ~150 tokens when loaded as context -->

# WBS: [Project Name]

## 1 Project Management
- 1.1 Planning Documentation
- 1.2 Status Reporting
- 1.3 Risk Management
- 1.4 Change Control

## 2 [Major Deliverable — noun]
### 2.1 [Sub-deliverable — noun]
- 2.1.1 [Work Package — noun]
- 2.1.2 [Work Package — noun]

## 3 [Major Deliverable — noun]
### 3.1 [Sub-deliverable — noun]

## 4 Quality Assurance
## 5 Deployment
## 6 Documentation
## 7 Training
## 8 Transition

<!--
Rules:
- Every node is a noun phrase (output). Reject "Build/Design/Test/..." starts.
- All six overhead branches must be present (PM/QA/Deployment/Documentation/Training/Transition).
- IDs are append-only; never reuse a deleted id.
- Max depth 4; sibling depth difference <= 1.
-->
