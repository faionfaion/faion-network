---
id: pattern-memory
name: "Pattern Memory"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# Pattern Memory

## Overview

System for capturing, storing, and retrieving successful patterns learned during development. Creates evolving knowledge base that improves over time, enabling consistent application of proven solutions and faster problem-solving.

## When to Use

- Documenting successful solutions for reuse
- Finding applicable patterns for current tasks
- Building team knowledge base
- Onboarding new developers
- Standardizing best practices
- Improving consistency across codebase

## Pattern Memory Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Pattern Memory System                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   Capture   │ →  │   Storage   │ →  │  Retrieval  │    │
│  │   Layer     │    │   Layer     │    │   Layer     │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│        │                  │                  │             │
│        ▼                  ▼                  ▼             │
│  Pattern         patterns_learned      Query by:          │
│  Recognition     .jsonl               - Category          │
│  & Extraction                         - Context           │
│                                       - Similarity        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Storage:**
```
~/.sdd/memory/
├── patterns_learned.jsonl
├── patterns_index.json
├── patterns_archive/
└── patterns_stats.json
```

## Pattern Schema

```json
{
  "id": "PAT_2024_001",
  "version": 1,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T15:45:00Z",

  "metadata": {
    "category": "coding",
    "subcategory": "error-handling",
    "language": "typescript",
    "framework": "react",
    "tags": ["async", "error-boundary", "user-experience"]
  },

  "pattern": {
    "name": "Async Operation Error Boundary",
    "summary": "Graceful error handling for async operations with user feedback",

    "problem": {
      "description": "Async operations can fail, causing poor UX or app crashes",
      "symptoms": [
        "Unhandled promise rejections",
        "Blank screens on errors",
        "No user feedback on failures"
      ],
      "contexts": [
        "API calls in React components",
        "Data fetching with useEffect",
        "Form submissions"
      ]
    },

    "solution": {
      "description": "Wrap async operations with try-catch and manage error/loading states",
      "approach": [
        "Create error and loading state variables",
        "Wrap async code in try-catch-finally",
        "Set loading true before, false in finally",
        "Set error in catch block",
        "Display appropriate UI for each state"
      ],
      "code_example": "function useAsyncOperation<T>(asyncFn: () => Promise<T>) {\n  const [data, setData] = useState<T | null>(null);\n  const [error, setError] = useState<Error | null>(null);\n  const [loading, setLoading] = useState(false);\n\n  const execute = useCallback(async () => {\n    try {\n      setLoading(true);\n      setError(null);\n      const result = await asyncFn();\n      setData(result);\n      return result;\n    } catch (e) {\n      setError(e instanceof Error ? e : new Error(String(e)));\n      throw e;\n    } finally {\n      setLoading(false);\n    }\n  }, [asyncFn]);\n\n  return { data, error, loading, execute };\n}"
    },

    "benefits": [
      "Prevents unhandled errors",
      "Provides user feedback",
      "Enables graceful degradation",
      "Simplifies debugging"
    ],

    "trade_offs": [
      "Additional state management",
      "Need to design error UI",
      "Slight code overhead"
    ],

    "related_patterns": ["PAT_2024_015", "PAT_2024_022"]
  },

  "validation": {
    "confidence": 0.92,
    "usage_count": 15,
    "success_rate": 0.93,
    "last_used": "2024-01-20T14:30:00Z"
  },

  "provenance": {
    "discovered_in": "TASK_042",
    "verified_in": ["TASK_055", "TASK_067", "TASK_089"]
  }
}
```

## Pattern Categories

```yaml
coding_patterns:
  error_handling:
    - exception_patterns
    - fallback_strategies
    - retry_mechanisms

  data_management:
    - state_management
    - caching_patterns
    - data_transformation

  api_design:
    - endpoint_structure
    - response_formats
    - versioning

  testing:
    - unit_test_patterns
    - mock_strategies
    - test_data_management

architecture_patterns:
  structural:
    - component_organization
    - module_boundaries
    - layer_separation

  behavioral:
    - event_handling
    - pub_sub_patterns
    - command_patterns

  integration:
    - api_integration
    - service_communication
    - data_sync

process_patterns:
  planning:
    - estimation_techniques
    - decomposition_strategies
    - risk_assessment

  execution:
    - implementation_order
    - debugging_approaches
    - review_practices
```

## Pattern Capture

```python
def capture_pattern(task_id: str, solution: dict) -> Pattern:
    """Capture a new pattern from successful task execution"""

    # 1. Extract pattern components
    pattern = Pattern(
        id=generate_pattern_id(),
        metadata=extract_metadata(solution),
        problem=identify_problem(task_id),
        solution=document_solution(solution),
        provenance=create_provenance(task_id)
    )

    # 2. Check for duplicates/similar
    similar = find_similar_patterns(pattern)
    if similar:
        return merge_or_link_patterns(pattern, similar)

    # 3. Initial validation
    pattern.validation = ValidationData(
        confidence=0.5,
        usage_count=1,
        success_rate=1.0,
        last_used=datetime.now()
    )

    # 4. Store pattern
    store_pattern(pattern)
    update_pattern_index(pattern)

    return pattern
```

## Pattern Retrieval

```python
def query_patterns(
    category: str = None,
    tags: List[str] = None,
    context: str = None,
    min_confidence: float = 0.7,
    limit: int = 5
) -> List[Pattern]:
    """Query patterns matching criteria"""

    patterns = load_patterns()

    # Filter by category
    if category:
        patterns = [p for p in patterns
                   if p.metadata.category == category]

    # Filter by tags
    if tags:
        patterns = [p for p in patterns
                   if any(t in p.metadata.tags for t in tags)]

    # Filter by confidence
    patterns = [p for p in patterns
               if p.validation.confidence >= min_confidence]

    # Rank by relevance
    if context:
        patterns = rank_by_context_similarity(patterns, context)
    else:
        patterns = rank_by_usage_and_confidence(patterns)

    return patterns[:limit]
```

## Pattern Validation

```yaml
validation_workflow:
  initial_capture:
    confidence: 0.5
    requirements:
      - "Successful in original context"
      - "Basic documentation"

  early_validation:
    confidence: 0.6-0.7
    requirements:
      - "Used successfully 2-3 times"
      - "Works in similar contexts"
      - "No critical failures"

  established:
    confidence: 0.8-0.9
    requirements:
      - "Used successfully 5+ times"
      - "Verified across different contexts"
      - "Documented trade-offs"
      - "Peer reviewed"

  proven:
    confidence: 0.9+
    requirements:
      - "Used successfully 10+ times"
      - "Adopted as team standard"
      - "Full documentation"
      - "Training material available"
```

## Quick Pattern Capture

```markdown
## New Pattern: [Name]

**Category:** [coding|architecture|process|devops] / [subcategory]
**Tags:** [tag1, tag2, tag3]

**Problem:**
[What problem does this solve?]

**Solution:**
[Brief description of the approach]

**Code Example:**
```[language]
[Minimal working example]
```

**When to Use:**
- [Context 1]
- [Context 2]

**When NOT to Use:**
- [Anti-context 1]

**Discovered In:** TASK_XXX
```

## Pattern Usage Report

```yaml
pattern_usage_report:
  period: "2024-01"

  most_used:
    - id: PAT_2024_001
      name: "Async Error Boundary"
      usage_count: 15
      success_rate: 93%

    - id: PAT_2024_015
      name: "API Response Normalization"
      usage_count: 12
      success_rate: 100%

  newly_established:
    - id: PAT_2024_042
      name: "Form Validation Pattern"
      confidence_increase: 0.5 → 0.8

  needs_attention:
    - id: PAT_2024_008
      name: "Legacy Cache Pattern"
      reason: "3 failures this month"
      action: "Review and update or deprecate"

  gap_analysis:
    missing_patterns:
      - "Database transaction handling"
      - "File upload chunking"
```

## Best Practices

### Pattern Quality
- **Specific but generalizable** - Clear context, broad applicability
- **Complete documentation** - Problem, solution, trade-offs
- **Working examples** - Real code, not just theory
- **Known limitations** - When NOT to use

### Memory Management
- **Regular cleanup** - Archive unused patterns
- **Merge duplicates** - Avoid fragmentation
- **Version control** - Track pattern evolution
- **Index optimization** - Fast retrieval

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Executing design patterns | haiku | Pattern application, code generation |
| Reviewing implementation against spec | sonnet | Quality assurance, consistency check |
| Resolving design-execution conflicts | opus | Trade-off analysis, adaptive decisions |

## Sources

- [Design Patterns (GoF)](https://www.oreilly.com/library/view/design-patterns-elements/0201633612/)
- [Patterns of Enterprise Application Architecture](https://martinfowler.com/eaaCatalog/)
- [Software Design Patterns](https://refactoring.guru/design-patterns)
- [Pattern Languages](https://www.hillside.net/patterns/patterns-catalog)
- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)
