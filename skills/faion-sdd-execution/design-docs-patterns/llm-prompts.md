# Design Docs Patterns LLM Prompts

## Prompt 1: Apply Methodology

```
You are applying the Design Docs Patterns methodology.

CONTEXT:
{context}

REQUIREMENTS:
{requirements}

METHODOLOGY PRINCIPLES:
[Key principles from README.md]

TASK:
Apply the Design Docs Patterns methodology to analyze the given context and requirements.

OUTPUT FORMAT:
{
  "analysis": "Analysis results",
  "recommendations": ["Recommendation 1", "Recommendation 2"],
  "implementation_steps": [
    {
      "step": 1,
      "action": "Action description",
      "validation": "How to verify"
    }
  ],
  "confidence": "high|medium|low",
  "rationale": "Reasoning for approach"
}
```

## Prompt 2: Validate Application

```
You are validating the application of Design Docs Patterns methodology.

METHODOLOGY APPLICATION:
{application_details}

EXPECTED OUTCOMES:
{expected_outcomes}

VALIDATION CRITERIA:
- Criterion 1
- Criterion 2
- Criterion 3

TASK:
Validate whether the methodology was correctly applied and outcomes match expectations.

OUTPUT FORMAT:
{
  "validation_status": "pass|fail|partial",
  "criteria_results": [
    {
      "criterion": "Criterion name",
      "status": "pass|fail",
      "evidence": "Evidence for status",
      "notes": "Additional notes"
    }
  ],
  "issues_found": [
    {
      "issue": "Issue description",
      "severity": "critical|high|medium|low",
      "recommendation": "How to fix"
    }
  ],
  "overall_quality": "excellent|good|acceptable|poor"
}
```

## Prompt 3: Generate Implementation Plan

```
You are creating an implementation plan using Design Docs Patterns methodology.

PROJECT CONTEXT:
{project_context}

GOALS:
{goals}

CONSTRAINTS:
{constraints}

METHODOLOGY: Design Docs Patterns
Apply this methodology to create a detailed implementation plan.

OUTPUT FORMAT:
{
  "phases": [
    {
      "phase": "Phase name",
      "objectives": ["Objective 1", "Objective 2"],
      "tasks": [
        {
          "task": "Task description",
          "methodology_application": "How Design Docs Patterns applies",
          "estimated_tokens": number,
          "dependencies": ["task_ids"]
        }
      ]
    }
  ],
  "risks": [
    {
      "risk": "Risk description",
      "mitigation": "Mitigation strategy using Design Docs Patterns"
    }
  ],
  "success_criteria": ["Criterion 1", "Criterion 2"]
}
```

## Prompt 4: Troubleshoot Issues

```
You are troubleshooting issues with Design Docs Patterns methodology application.

ISSUE DESCRIPTION:
{issue_description}

METHODOLOGY APPLICATION:
{how_it_was_applied}

EXPECTED VS ACTUAL:
Expected: {expected}
Actual: {actual}

TASK:
Identify what went wrong and how to fix it using Design Docs Patterns principles.

OUTPUT FORMAT:
{
  "root_cause": "Why the issue occurred",
  "methodology_gaps": ["Gap 1", "Gap 2"],
  "corrective_actions": [
    {
      "action": "Action description",
      "methodology_principle": "Which principle this addresses",
      "priority": "high|medium|low"
    }
  ],
  "prevention": "How to prevent this in future",
  "lessons_learned": ["Lesson 1", "Lesson 2"]
}
```

## Prompt 5: Optimize Application

```
You are optimizing the application of Design Docs Patterns methodology.

CURRENT APPLICATION:
{current_application}

METRICS:
{metrics}

CONSTRAINTS:
{constraints}

TASK:
Suggest optimizations to improve effectiveness while maintaining methodology principles.

OUTPUT FORMAT:
{
  "optimization_opportunities": [
    {
      "area": "Area to optimize",
      "current_approach": "How it's done now",
      "optimized_approach": "Better way using Design Docs Patterns",
      "expected_improvement": "What will improve",
      "tradeoffs": "Any tradeoffs to consider"
    }
  ],
  "quick_wins": ["Quick win 1", "Quick win 2"],
  "long_term_improvements": ["Improvement 1", "Improvement 2"],
  "implementation_priority": [
    {
      "optimization": "What to optimize",
      "priority": "high|medium|low",
      "effort": "low|medium|high",
      "impact": "low|medium|high"
    }
  ]
}
```

## Prompt 6: Generate Report

```
You are generating a report on Design Docs Patterns methodology application.

PROJECT/TASK:
{project_or_task}

METHODOLOGY APPLICATION:
{application_details}

RESULTS:
{results}

TASK:
Create a comprehensive report on how Design Docs Patterns was applied and outcomes achieved.

OUTPUT FORMAT:
{
  "executive_summary": "High-level summary",
  "methodology_application": {
    "how_applied": "Description of application",
    "adherence_to_principles": "How well principles were followed",
    "adaptations_made": ["Adaptation 1", "Adaptation 2"]
  },
  "results": {
    "quantitative": {
      "metric_1": "value",
      "metric_2": "value"
    },
    "qualitative": ["Outcome 1", "Outcome 2"]
  },
  "lessons_learned": {
    "what_worked": ["Success 1", "Success 2"],
    "what_didnt": ["Challenge 1", "Challenge 2"],
    "improvements": ["Improvement 1", "Improvement 2"]
  },
  "recommendations": {
    "for_this_project": ["Recommendation 1"],
    "for_future_projects": ["Recommendation 2"]
  }
}
```
