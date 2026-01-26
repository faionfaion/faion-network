# LLM Evaluation Prompts

## Faithfulness Evaluation

### Basic Faithfulness Prompt

```
Evaluate if the answer is faithful to the given context.

Context:
{context}

Answer:
{answer}

Analyze the answer and determine:
1. What claims does the answer make?
2. Is each claim supported by the context?
3. Are there any hallucinations (claims not in context)?

Provide a score from 0 to 1 where:
- 1.0: Completely faithful, all claims supported
- 0.5: Partially faithful, some unsupported claims
- 0.0: Unfaithful, major hallucinations

Return JSON with:
{
  "score": <float>,
  "supported_claims": [<list of claims found in context>],
  "unsupported_claims": [<list of claims NOT in context>],
  "explanation": "<reasoning>"
}
```

### Detailed Faithfulness Prompt (with claim extraction)

```
You are evaluating the faithfulness of a generated answer against retrieved context.

## Context
{context}

## Generated Answer
{answer}

## Task

Step 1: Extract all factual claims from the answer.
Step 2: For each claim, determine if it is:
  - SUPPORTED: Directly stated or clearly implied in context
  - UNSUPPORTED: Not mentioned in context (hallucination)
  - CONTRADICTED: Directly contradicts context

Step 3: Calculate faithfulness score = supported_claims / total_claims

## Output Format (JSON)

{
  "claims": [
    {
      "claim": "<the factual claim>",
      "status": "SUPPORTED|UNSUPPORTED|CONTRADICTED",
      "evidence": "<quote from context or null>",
      "confidence": <0.0-1.0>
    }
  ],
  "score": <float 0-1>,
  "total_claims": <int>,
  "supported_count": <int>,
  "unsupported_count": <int>,
  "contradicted_count": <int>,
  "summary": "<brief explanation>"
}
```

## Answer Relevance Evaluation

### Basic Relevance Prompt

```
Evaluate if the answer addresses the question.

Question:
{question}

Answer:
{answer}

Analyze:
1. Does the answer directly address the question?
2. Is the answer complete or partial?
3. Is there irrelevant information?

Score from 0 to 1 where:
- 1.0: Completely answers the question
- 0.5: Partially answers or includes irrelevant info
- 0.0: Does not answer the question

Return JSON with:
{
  "score": <float>,
  "addresses_question": <boolean>,
  "completeness": "full|partial|none",
  "irrelevant_content": <boolean>,
  "explanation": "<reasoning>"
}
```

### Detailed Relevance Prompt (with aspect analysis)

```
You are evaluating whether a generated answer addresses the user's question.

## Question
{question}

## Answer
{answer}

## Evaluation Criteria

1. **Directness**: Does the answer directly address what was asked?
2. **Completeness**: Are all aspects of the question covered?
3. **Conciseness**: Is the answer free of unnecessary information?
4. **Specificity**: Does the answer provide specific information, not vague generalities?

## Scoring Guide

| Score | Description |
|-------|-------------|
| 1.0 | Perfect - addresses all aspects directly and completely |
| 0.8 | Good - addresses main question with minor gaps |
| 0.6 | Acceptable - addresses question but incomplete or verbose |
| 0.4 | Poor - partially addresses question, significant gaps |
| 0.2 | Bad - tangentially related, doesn't really answer |
| 0.0 | Fail - completely off-topic or empty |

## Output Format (JSON)

{
  "score": <float>,
  "directness": {
    "score": <float>,
    "explanation": "<why>"
  },
  "completeness": {
    "score": <float>,
    "covered_aspects": [<list>],
    "missing_aspects": [<list>]
  },
  "conciseness": {
    "score": <float>,
    "irrelevant_content": "<any irrelevant parts>"
  },
  "specificity": {
    "score": <float>,
    "explanation": "<why>"
  },
  "overall_explanation": "<summary>"
}
```

## Context Relevance Evaluation

### Basic Context Relevance Prompt

```
Evaluate if the context is relevant to answering the question.

Question:
{question}

Context:
{context}

Analyze:
1. Does the context contain information to answer the question?
2. How much of the context is relevant?
3. What relevant information is missing?

Score from 0 to 1 where:
- 1.0: Context fully relevant and sufficient
- 0.5: Partially relevant or incomplete
- 0.0: Irrelevant context

Return JSON with:
{
  "score": <float>,
  "relevant_sentences": [<list of relevant parts>],
  "irrelevant_sentences": [<list of irrelevant parts>],
  "missing_info": "<what info would help answer the question>",
  "explanation": "<reasoning>"
}
```

### Detailed Context Relevance Prompt (with sentence-level analysis)

```
You are evaluating the relevance of retrieved context for answering a question.

## Question
{question}

## Retrieved Context
{context}

## Task

For each sentence/paragraph in the context, determine:
- RELEVANT: Directly helps answer the question
- PARTIAL: Contains some useful information
- IRRELEVANT: Does not help answer the question
- NOISE: Distracting or potentially misleading

## Metrics to Calculate

1. **Precision**: relevant_content / total_content
2. **Coverage**: Does context contain enough to fully answer?
3. **Noise Ratio**: irrelevant_content / total_content

## Output Format (JSON)

{
  "score": <float 0-1>,
  "analysis": [
    {
      "text": "<sentence/paragraph>",
      "relevance": "RELEVANT|PARTIAL|IRRELEVANT|NOISE",
      "reason": "<why>"
    }
  ],
  "metrics": {
    "precision": <float>,
    "coverage": "full|partial|none",
    "noise_ratio": <float>
  },
  "missing_information": "<what's needed but not present>",
  "summary": "<overall assessment>"
}
```

## Answer Correctness Evaluation

### Comparison Against Ground Truth

```
Compare the generated answer against the ground truth answer.

## Question
{question}

## Ground Truth Answer
{ground_truth}

## Generated Answer
{answer}

## Evaluation

1. **Semantic Similarity**: How similar in meaning are the answers?
2. **Factual Overlap**: What facts are shared between answers?
3. **Factual Correctness**: Are there any factual errors in generated answer?

## Scoring

- 1.0: Semantically equivalent, all facts correct
- 0.8: Same meaning with minor wording differences
- 0.6: Mostly correct, some details differ
- 0.4: Partially correct, significant differences
- 0.2: Mostly incorrect or incomplete
- 0.0: Completely wrong or contradicts ground truth

## Output Format (JSON)

{
  "score": <float>,
  "semantic_similarity": <float>,
  "factual_overlap": {
    "shared_facts": [<list>],
    "missing_facts": [<list>],
    "extra_facts": [<list>],
    "incorrect_facts": [<list>]
  },
  "explanation": "<detailed comparison>"
}
```

## Hallucination Detection

### Dedicated Hallucination Prompt

```
You are a hallucination detector. Identify any statements in the answer that are NOT supported by the provided context.

## Context (Source of Truth)
{context}

## Generated Answer
{answer}

## Definition of Hallucination

A hallucination is any statement that:
1. Claims a fact not present in the context
2. Misrepresents information from the context
3. Makes assumptions not supported by context
4. Adds details not mentioned in context
5. Uses specific numbers/dates/names not in context

## Task

Extract each factual statement from the answer and classify it:
- GROUNDED: Directly supported by context
- INFERRED: Reasonable inference from context
- HALLUCINATED: Not supported by context

## Output Format (JSON)

{
  "hallucination_detected": <boolean>,
  "hallucination_rate": <float 0-1>,
  "statements": [
    {
      "statement": "<text>",
      "classification": "GROUNDED|INFERRED|HALLUCINATED",
      "supporting_evidence": "<quote from context or null>",
      "severity": "minor|moderate|severe"
    }
  ],
  "summary": {
    "total_statements": <int>,
    "grounded": <int>,
    "inferred": <int>,
    "hallucinated": <int>
  },
  "most_severe_hallucination": "<if any>"
}
```

## Composite RAG Evaluation

### All-in-One Evaluation Prompt

```
You are evaluating a RAG (Retrieval-Augmented Generation) system response.

## Input

**Question:** {question}

**Retrieved Context:**
{context}

**Generated Answer:**
{answer}

**Ground Truth (if available):** {ground_truth}

## Evaluate These Dimensions

### 1. Context Relevance
Is the retrieved context relevant to answering the question?

### 2. Faithfulness
Is the answer grounded in the retrieved context?

### 3. Answer Relevance
Does the answer address the question asked?

### 4. Answer Correctness (if ground truth provided)
Is the answer factually correct?

### 5. Completeness
Does the answer fully address all aspects of the question?

## Output Format (JSON)

{
  "context_relevance": {
    "score": <float 0-1>,
    "explanation": "<why>"
  },
  "faithfulness": {
    "score": <float 0-1>,
    "hallucinations": [<list if any>],
    "explanation": "<why>"
  },
  "answer_relevance": {
    "score": <float 0-1>,
    "explanation": "<why>"
  },
  "answer_correctness": {
    "score": <float 0-1 or null if no ground truth>,
    "explanation": "<why>"
  },
  "completeness": {
    "score": <float 0-1>,
    "missing_aspects": [<list if any>]
  },
  "overall_score": <float 0-1>,
  "overall_assessment": "<summary>",
  "recommendations": [<list of improvements>]
}
```

## Question Generation Prompts

### Generate Test Questions from Documents

```
Generate diverse test questions from this document for RAG evaluation.

## Document
{document}

## Requirements

Generate 5 questions of different types:
1. **Factual**: Simple fact lookup (who, what, when, where)
2. **Definitional**: Ask for definition or explanation
3. **Comparative**: Compare concepts mentioned
4. **Reasoning**: Requires inference from multiple facts
5. **Multi-hop**: Requires connecting information from different parts

## Output Format (JSON)

{
  "questions": [
    {
      "question": "<the question>",
      "type": "factual|definitional|comparative|reasoning|multi_hop",
      "answer": "<correct answer based on document>",
      "source_quote": "<exact quote supporting the answer>",
      "difficulty": "easy|medium|hard"
    }
  ]
}
```

### Generate Adversarial Questions

```
Generate adversarial test questions that might cause a RAG system to fail.

## Document Corpus Topic
{topic_description}

## Generate Questions That Might Cause

1. **Hallucination**: Question seems related but answer isn't in docs
2. **Confusion**: Similar entities/concepts that could be mixed up
3. **Out-of-scope**: Question outside document coverage
4. **Recency**: Question about information that might be outdated
5. **Ambiguity**: Question that could be interpreted multiple ways

## Output Format (JSON)

{
  "adversarial_questions": [
    {
      "question": "<the question>",
      "failure_mode": "hallucination|confusion|out_of_scope|recency|ambiguity",
      "expected_issue": "<what might go wrong>",
      "ideal_response": "<what a good system should say>"
    }
  ]
}
```

## Prompt Best Practices

### Tips for Effective LLM Evaluation

1. **Be Specific**: Define exactly what you're measuring
2. **Provide Examples**: Show what good/bad looks like
3. **Use Structured Output**: JSON ensures parseable results
4. **Include Scoring Rubric**: Explicit criteria reduce variance
5. **Ask for Explanation**: Reasoning helps debug issues

### Reducing Evaluator Variance

```
## Calibration Examples

Before evaluating, here are calibrated examples:

### Example 1: Score 1.0 (Perfect Faithfulness)
Context: "The company was founded in 2010 by John Smith."
Answer: "The company was founded by John Smith in 2010."
Reasoning: Exact same facts, just reworded.

### Example 2: Score 0.5 (Partial Faithfulness)
Context: "The company was founded in 2010."
Answer: "The company was founded in 2010 and has grown significantly."
Reasoning: First claim supported, second claim (growth) not in context.

### Example 3: Score 0.0 (Hallucination)
Context: "The company was founded in 2010."
Answer: "The company was founded in 2008 by two engineers."
Reasoning: Wrong year, fabricated founders.

Now evaluate the following...
```

### Cost Optimization

For high-volume evaluation, use a two-stage approach:

```
## Stage 1: Quick Filter (GPT-4o-mini)

Is this answer obviously problematic?
- YES: Flag for detailed review
- NO: Mark as likely acceptable

## Stage 2: Detailed Analysis (GPT-4o)

[Full evaluation prompt for flagged items only]
```
