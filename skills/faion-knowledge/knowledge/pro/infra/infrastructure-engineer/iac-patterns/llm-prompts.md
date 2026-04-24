# IaC Patterns LLM Prompts

## Module Development

### Create New Module

```
Create a Terraform module for [RESOURCE_TYPE] with the following requirements:

Context:
- Cloud provider: [AWS/GCP/Azure]
- Use case: [DESCRIPTION]
- Must comply with: [SECURITY_REQUIREMENTS]

Requirements:
1. Follow single responsibility principle
2. Include input validation
3. Use sensible defaults
4. Support tagging
5. Include outputs for common use cases

Structure needed:
- main.tf (resources)
- variables.tf (with descriptions and validation)
- outputs.tf (with descriptions)
- versions.tf (provider constraints)
- README.md (usage examples)

Existing patterns in codebase: [REFERENCE_MODULE_PATH]
```

### Refactor to Module

```
Refactor the following Terraform configuration into a reusable module:

Current configuration:
[PASTE_CURRENT_TF_CODE]

Requirements:
1. Extract configurable values as variables
2. Add validation rules for inputs
3. Expose useful outputs
4. Support multiple environments (dev/staging/prod)
5. Follow DRY principles

The module should:
- Work with existing state (provide migration steps)
- Maintain backward compatibility where possible
- Include example usage
```

### Review Module

```
Review this Terraform module for best practices:

[PASTE_MODULE_CODE]

Check for:
1. Single responsibility - does it do one thing well?
2. Variable validation - are inputs properly constrained?
3. Sensible defaults - are optional vars defaulted appropriately?
4. Output completeness - are necessary values exposed?
5. Documentation - is usage clear?
6. DRY violations - any repeated code?
7. Security issues - any hardcoded secrets or overly permissive settings?
8. Naming conventions - consistent and descriptive?

Provide specific recommendations with code examples.
```

## Composition Patterns

### Design Module Composition

```
Design a module composition strategy for:

Application type: [WEB_APP/API/DATA_PIPELINE/etc.]
Components needed:
- [COMPONENT_1]
- [COMPONENT_2]
- [COMPONENT_3]

Requirements:
- Support multiple environments
- Enable independent component updates
- Minimize blast radius of changes
- Follow dependency inversion principle

Provide:
1. Module hierarchy diagram
2. Dependency flow
3. Interface contracts (inputs/outputs between modules)
4. Example composition in root module
```

### Create Wrapper Module

```
Create a wrapper module around [COMMUNITY_MODULE_OR_RESOURCE] that enforces our organization's standards:

Organization requirements:
- Encryption: [REQUIREMENTS]
- Networking: [REQUIREMENTS]
- Tagging: [REQUIRED_TAGS]
- Naming: [CONVENTION]
- Compliance: [STANDARDS]

The wrapper should:
1. Set non-negotiable defaults for security/compliance
2. Simplify the interface by hiding complexity
3. Allow override of non-critical settings
4. Include validation for org-specific rules
```

### Create Facade Module

```
Create a facade module that deploys a complete [STACK_TYPE] with minimal inputs:

Stack components:
- [COMPONENT_1]
- [COMPONENT_2]
- [COMPONENT_3]

User should only need to provide:
- [MINIMAL_INPUT_1]
- [MINIMAL_INPUT_2]

The facade should:
1. Orchestrate all component modules internally
2. Use sensible defaults for everything else
3. Handle inter-component dependencies
4. Expose only essential outputs
```

## DRY Improvements

### Eliminate Duplication

```
Identify and eliminate duplication in this Terraform configuration:

[PASTE_TF_CODE]

Look for:
1. Repeated resource blocks that could use for_each
2. Repeated nested blocks that could use dynamic
3. Values that should be in locals
4. Patterns that should be extracted to modules
5. Common configurations across environments

Provide refactored code with explanations.
```

### Create Factory Pattern

```
Convert these similar resources into a factory pattern using for_each:

Current resources:
[PASTE_SIMILAR_RESOURCES]

Create a module that:
1. Accepts a map of configuration objects
2. Creates resources dynamically using for_each
3. Handles optional/conditional attributes
4. Outputs a map of created resources
```

## Testing

### Write Module Tests

```
Write tests for this Terraform module:

[PASTE_MODULE_CODE]

Create tests using [terraform test / Terratest]:

Test cases needed:
1. Basic deployment with required inputs only
2. Deployment with all optional inputs
3. Input validation (should reject invalid inputs)
4. Output verification
5. [ENVIRONMENT]-specific behavior

For integration tests, also verify:
- Resources are created correctly
- Security configurations are applied
- Connectivity works as expected
```

### Add Validation Rules

```
Add comprehensive validation rules to these variables:

[PASTE_VARIABLES_TF]

Validation requirements:
1. CIDR blocks should be valid CIDR notation
2. Names should follow pattern: [NAMING_PATTERN]
3. Environment should be one of: [VALID_ENVS]
4. Numeric values should be within reasonable bounds
5. Required tags should be present

Include helpful error messages that guide users to correct values.
```

## State Management

### Plan State Migration

```
Plan a state migration for:

Current state: [DESCRIBE_CURRENT_STATE_STRUCTURE]
Target state: [DESCRIBE_TARGET_STATE_STRUCTURE]

Changes:
- [CHANGE_1]
- [CHANGE_2]

Provide:
1. Pre-migration checklist
2. State manipulation commands needed
3. Verification steps
4. Rollback plan
5. Impact on dependent resources
```

### Design State Structure

```
Design a state management strategy for:

Project: [PROJECT_NAME]
Environments: [dev, staging, prod]
Components: [LIST_COMPONENTS]
Teams: [TEAM_STRUCTURE]

Consider:
1. State isolation (per-env, per-component, or both?)
2. Remote backend configuration
3. Access control (who can modify what?)
4. State locking
5. Blast radius minimization

Provide directory structure and backend configuration.
```

## CI/CD Integration

### Create Pipeline

```
Create a CI/CD pipeline for Terraform using [GitHub Actions/GitLab CI/Jenkins]:

Requirements:
1. Format check on PRs
2. Validation and linting
3. Security scanning (checkov/tfsec)
4. Plan on PR with comment output
5. Apply on merge to main
6. Environment-specific workflows

Security requirements:
- OIDC authentication (no long-lived credentials)
- Approval gates for production
- Audit logging

Provide complete workflow file with comments.
```

### Add Drift Detection

```
Set up drift detection for Terraform-managed infrastructure:

Requirements:
- Scheduled runs (frequency: [SCHEDULE])
- Alert on detected drift
- Option to auto-remediate or report only
- Integration with [ALERTING_SYSTEM]

Provide:
1. Workflow/job configuration
2. Drift detection script
3. Alerting configuration
4. Remediation options
```

## Troubleshooting

### Debug Failed Apply

```
Help debug this failed Terraform apply:

Error message:
[PASTE_ERROR]

Configuration:
[PASTE_RELEVANT_CONFIG]

Context:
- Environment: [ENV]
- Last successful apply: [TIMESTAMP]
- Recent changes: [DESCRIBE_CHANGES]

Provide:
1. Root cause analysis
2. Potential solutions ranked by likelihood
3. Verification steps
4. Prevention recommendations
```

### Resolve State Issues

```
Help resolve this Terraform state issue:

Symptom:
[DESCRIBE_ISSUE]

Current state:
[DESCRIBE_STATE_SITUATION]

Expected behavior:
[DESCRIBE_EXPECTED]

Provide:
1. Diagnosis steps
2. Safe resolution approach
3. State commands needed (with --dry-run first)
4. Verification steps
5. Prevention measures
```

## Prompt Chaining

### Full Module Development Flow

```
Step 1: Analyze requirements
"Analyze these requirements for a [MODULE_TYPE] module: [REQUIREMENTS]
Identify: inputs needed, outputs expected, resources to create, edge cases."

Step 2: Design module interface
"Based on the analysis, design the module interface:
- variables.tf with types, defaults, validation
- outputs.tf with descriptions
- Example usage in README"

Step 3: Implement module
"Implement main.tf following these patterns: [REFERENCE_PATTERNS]
Include: resource definitions, locals, data sources"

Step 4: Add tests
"Write tests for the module covering:
- Happy path with defaults
- All optional parameters
- Validation failures
- Integration verification"

Step 5: Documentation
"Complete the README with:
- Purpose and use cases
- Requirements table
- Input/output tables
- Examples (basic and advanced)
- Related modules"
```

---

*IaC Patterns LLM Prompts | faion-infrastructure-engineer*
