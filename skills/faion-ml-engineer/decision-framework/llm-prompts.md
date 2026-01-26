# LLM Prompts

> Prompts for model evaluation, comparison, and selection assistance.

## Model Evaluation Prompts

### Task-Specific Quality Evaluation

```markdown
You are evaluating LLM responses for [TASK TYPE]. Score the following response on these criteria:

**Response to evaluate:**
[RESPONSE]

**Original prompt:**
[PROMPT]

**Evaluation criteria (score 1-5 for each):**

1. **Accuracy** - Factual correctness and relevance
2. **Completeness** - Covers all aspects of the request
3. **Clarity** - Easy to understand, well-structured
4. **Instruction Following** - Follows the prompt requirements exactly
5. **Usefulness** - Practically helpful for the intended purpose

**Output format:**
{
  "accuracy": X,
  "completeness": X,
  "clarity": X,
  "instruction_following": X,
  "usefulness": X,
  "total": X,
  "reasoning": "Brief explanation of scores"
}
```

### Comparative Model Evaluation

```markdown
You are comparing responses from different LLMs for the same task.

**Task prompt:**
[ORIGINAL PROMPT]

**Response A ([MODEL A]):**
[RESPONSE A]

**Response B ([MODEL B]):**
[RESPONSE B]

**Compare on these dimensions:**
1. Which response better addresses the user's needs?
2. Which is more accurate and factually correct?
3. Which is better structured and easier to use?
4. Which handles edge cases or nuances better?
5. Overall winner and margin (slight/clear/significant)

**Output format:**
{
  "winner": "A" | "B" | "tie",
  "margin": "slight" | "clear" | "significant",
  "accuracy_winner": "A" | "B" | "tie",
  "structure_winner": "A" | "B" | "tie",
  "reasoning": "Detailed explanation"
}
```

---

## Complexity Classification Prompts

### Task Complexity Classifier

```markdown
Analyze the following user request and classify its complexity for LLM routing.

**User request:**
[USER REQUEST]

**Classification criteria:**

LOW complexity (route to budget model):
- Simple factual questions
- Basic formatting/conversion
- Short, single-intent requests
- FAQ-type questions

MEDIUM complexity (route to standard model):
- Multi-step but straightforward tasks
- Standard content generation
- Code snippets with clear requirements
- Analysis with defined scope

HIGH complexity (route to premium model):
- Complex reasoning required
- Multi-faceted analysis
- Creative or nuanced tasks
- Long-form content with specific requirements
- Code architecture decisions

**Output format:**
{
  "complexity": "low" | "medium" | "high",
  "reasoning": "Brief explanation",
  "suggested_model_tier": "budget" | "standard" | "premium",
  "token_estimate": number
}
```

### Intent Classification for Routing

```markdown
Classify the intent of this request to determine optimal model routing.

**Request:**
[USER REQUEST]

**Intent categories:**
- FAQ: Simple factual question
- GENERATION: Content creation (text, code, etc.)
- ANALYSIS: Review, critique, or analyze something
- REASONING: Complex problem-solving
- CODE: Programming tasks
- MULTIMODAL: Involves images/audio/video
- EXTRACTION: Pull structured data from text
- TRANSLATION: Language conversion
- CLASSIFICATION: Categorize or label

**Output:**
{
  "primary_intent": "[CATEGORY]",
  "secondary_intent": "[CATEGORY or null]",
  "confidence": 0.0-1.0,
  "routing_recommendation": {
    "model_type": "budget | standard | premium | code-specialized | multimodal",
    "reasoning": "Why this routing"
  }
}
```

---

## Cost Optimization Prompts

### Token Usage Analyzer

```markdown
Analyze the following prompt/response pair for token optimization opportunities.

**System prompt:**
[SYSTEM PROMPT]

**User prompt:**
[USER PROMPT]

**Response:**
[RESPONSE]

**Analyze:**
1. System prompt efficiency - Can it be shortened without losing effectiveness?
2. User prompt structure - Is context being repeated unnecessarily?
3. Response verbosity - Is the output more detailed than needed?
4. Caching opportunities - What parts could be cached across requests?

**Output:**
{
  "current_token_estimate": {
    "system": X,
    "user": X,
    "response": X,
    "total": X
  },
  "optimization_suggestions": [
    {
      "area": "system | user | response",
      "current": "current text snippet",
      "suggested": "optimized version",
      "estimated_savings": "X tokens (Y%)"
    }
  ],
  "caching_opportunities": [
    "Description of cacheable components"
  ],
  "projected_savings": "X% reduction"
}
```

### Batch Processing Analyzer

```markdown
Analyze these requests for batch processing optimization.

**Requests:**
1. [REQUEST 1]
2. [REQUEST 2]
3. [REQUEST 3]
...

**Analysis needed:**
1. Can these requests be batched together?
2. What's the optimal batch size?
3. Are there shared contexts that could be extracted?
4. What's the expected cost reduction from batching?

**Output:**
{
  "batchable": true | false,
  "optimal_batch_size": X,
  "shared_context": "Content that could be shared across requests",
  "individual_cost_estimate": "$X per request",
  "batched_cost_estimate": "$X per batch",
  "savings_percentage": "X%"
}
```

---

## Model Selection Assistant Prompts

### Requirements Analysis

```markdown
Help select the optimal LLM for this use case.

**Application description:**
[DESCRIPTION]

**Requirements:**
- Task type: [TASK]
- Expected volume: [REQUESTS/MONTH]
- Latency requirement: [REAL-TIME | INTERACTIVE | BATCH]
- Quality threshold: [DESCRIPTION]
- Budget: [MONTHLY BUDGET]
- Privacy requirements: [PUBLIC API OK | SELF-HOSTED REQUIRED]
- Special needs: [MULTIMODAL | LONG CONTEXT | CODE | etc.]

**Provide:**
1. Top 3 model recommendations with rationale
2. Cost projection for each
3. Tradeoffs between options
4. Implementation considerations

**Output format:**
{
  "recommendations": [
    {
      "rank": 1,
      "model": "model-name",
      "provider": "provider",
      "rationale": "Why this model",
      "monthly_cost_estimate": "$X",
      "pros": ["pro1", "pro2"],
      "cons": ["con1", "con2"]
    }
  ],
  "routing_suggestion": "Single model vs multi-model strategy",
  "implementation_notes": ["Note 1", "Note 2"]
}
```

### Migration Assessment

```markdown
Assess migrating from [CURRENT MODEL] to [TARGET MODEL].

**Current setup:**
- Model: [CURRENT MODEL]
- Monthly usage: [TOKENS/REQUESTS]
- Current cost: [COST]
- Pain points: [ISSUES]

**Target model:**
- Model: [TARGET MODEL]
- Expected benefits: [BENEFITS]

**Analyze:**
1. Expected quality impact (better/same/worse)
2. Cost impact
3. Migration complexity
4. Risks and mitigations

**Output:**
{
  "recommendation": "migrate" | "stay" | "test_first",
  "quality_impact": "improvement" | "neutral" | "regression",
  "cost_impact": {
    "current": "$X/month",
    "projected": "$Y/month",
    "change": "+/-Z%"
  },
  "migration_effort": "low" | "medium" | "high",
  "risks": ["Risk 1", "Risk 2"],
  "mitigations": ["Mitigation 1", "Mitigation 2"],
  "testing_plan": "Description of recommended testing approach"
}
```

---

## Evaluation Test Set Generation

### Generate Task-Specific Test Cases

```markdown
Generate a diverse test set for evaluating LLMs on [TASK TYPE].

**Task description:**
[DESCRIPTION]

**Requirements:**
- Number of test cases: [N]
- Include: easy, medium, hard difficulty
- Cover edge cases: [LIST EDGE CASES TO COVER]

**Output format for each test case:**
{
  "id": "test_001",
  "difficulty": "easy" | "medium" | "hard",
  "category": "category name",
  "prompt": "The test prompt",
  "expected_output_criteria": [
    "Criterion 1",
    "Criterion 2"
  ],
  "edge_case_covered": "Description or null"
}

Generate [N] test cases covering the full range of scenarios.
```

### Golden Dataset Validator

```markdown
Validate this prompt-response pair for inclusion in a golden evaluation dataset.

**Prompt:**
[PROMPT]

**Response:**
[RESPONSE]

**Task category:**
[CATEGORY]

**Validation criteria:**
1. Is the prompt clear and unambiguous?
2. Is the response correct and complete?
3. Is this a representative example of the task?
4. Does it have a clear "correct" answer or evaluation criteria?
5. Is it free from controversial or sensitive content?

**Output:**
{
  "valid": true | false,
  "issues": ["Issue 1 if any"],
  "quality_score": 1-5,
  "suggested_improvements": ["Improvement if any"],
  "suitable_for_evaluation": true | false
}
```

---

## Quick Reference

| Use Case | Prompt Template |
|----------|-----------------|
| Score single response | Task-Specific Quality Evaluation |
| Compare two models | Comparative Model Evaluation |
| Route request | Task Complexity Classifier |
| Optimize tokens | Token Usage Analyzer |
| Select model | Requirements Analysis |
| Plan migration | Migration Assessment |
| Build test set | Generate Task-Specific Test Cases |
