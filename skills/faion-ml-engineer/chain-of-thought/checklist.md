# Chain-of-Thought Checklists

Step-by-step checklists for implementing CoT techniques.

## Pre-Implementation Checklist

Before applying CoT, verify the task is appropriate.

### Task Assessment

- [ ] **Task requires reasoning** - Multiple steps to reach answer
- [ ] **Not simple lookup** - Answer isn't just retrieval
- [ ] **Explainability matters** - Need to understand the "why"
- [ ] **Model supports CoT** - Using capable model (GPT-4+, Claude 3+)
- [ ] **Token budget allows** - CoT increases output tokens

### Technique Selection

- [ ] **Complexity assessed** - Simple, medium, or complex reasoning
- [ ] **Format requirements** - Specific output format needed?
- [ ] **Reliability requirements** - How critical is correctness?
- [ ] **Cost constraints** - Token/latency budget defined

```
Decision Matrix:

Simple + Format flexible → Zero-Shot CoT
Simple + Format strict → Few-Shot CoT
Complex + Single answer → Self-Consistency
Complex + Exploration → Tree-of-Thoughts
Sequential dependencies → Least-to-Most
```

---

## Zero-Shot CoT Checklist

### Setup

- [ ] **Trigger phrase selected**
  - "Let's think step by step"
  - "Let's work through this carefully"
  - "Let's analyze this systematically"
- [ ] **Problem clearly stated** - Unambiguous task description
- [ ] **Output format defined** - What final answer should look like
- [ ] **Sections separated** - `<thinking>` and `<answer>` tags

### Prompt Structure

- [ ] **Task description first**
- [ ] **Problem/input marked**
- [ ] **Trigger phrase positioned** - Before or after problem
- [ ] **Answer format specified** - How to present final result

### Validation

- [ ] **Reasoning is relevant** - Steps address the problem
- [ ] **Steps are logical** - Each follows from previous
- [ ] **Conclusion matches reasoning** - No contradictions
- [ ] **Answer extractable** - Can parse final answer

### Template Verification

```
✓ [Task description]
✓ [Problem statement clearly marked]
✓ [Trigger: "Let's think step by step"]
✓ [Thinking section marker]
✓ [Answer section marker]
✓ [Output format specification]
```

---

## Few-Shot CoT Checklist

### Example Selection

- [ ] **Diverse examples** - Cover different scenarios
- [ ] **Representative complexity** - Match expected inputs
- [ ] **Correct reasoning** - All examples have valid logic
- [ ] **Appropriate count** - 2-3 examples typically sufficient
- [ ] **Edge cases included** - At least one non-obvious case

### Example Quality

- [ ] **Reasoning is explicit** - Shows intermediate steps
- [ ] **Format is consistent** - All examples match
- [ ] **No contradictions** - Examples don't conflict
- [ ] **Realistic inputs** - Match production data

### Example Structure

```
For each example verify:

✓ Input clearly marked
✓ Reasoning shown step-by-step
✓ Each step numbered or bulleted
✓ Final answer clearly separated
✓ Reasoning leads to answer logically
```

### Formatting Checklist

- [ ] **Delimiter consistency** - Same tags throughout
- [ ] **Step numbering** - Consistent numbering scheme
- [ ] **Answer separation** - Clear boundary with reasoning
- [ ] **Input/output balance** - Examples not too long

---

## Self-Consistency Checklist

### Configuration

- [ ] **Sample count defined** - Start with 5, adjust as needed
- [ ] **Temperature set** - 0.7-1.0 for diversity
- [ ] **Aggregation method chosen** - Majority vote or weighted
- [ ] **Budget calculated** - samples * tokens per sample

### Implementation

- [ ] **Base prompt created** - Working CoT prompt
- [ ] **Parallel execution** - Run samples concurrently if possible
- [ ] **Answer extraction** - Parse final answers from each
- [ ] **Voting logic** - Implement aggregation

### Quality Checks

- [ ] **Diverse paths generated** - Not all identical reasoning
- [ ] **Consensus threshold** - Define minimum agreement
- [ ] **Tie-breaking strategy** - Handle equal votes
- [ ] **Confidence metric** - Track agreement level

### Monitoring

```
Track these metrics:

✓ Agreement rate (% same answer)
✓ Unique answer count
✓ Token usage per sample
✓ Total latency
✓ Accuracy improvement vs single sample
```

---

## Tree-of-Thoughts Checklist

### Design

- [ ] **Branching factor defined** - Number of thoughts per step (3-5)
- [ ] **Max depth set** - Limit exploration depth (3-5)
- [ ] **Evaluation criteria** - How to score thoughts
- [ ] **Search strategy** - BFS, DFS, or best-first

### Thought Generation

- [ ] **Diverse thoughts** - Different approaches generated
- [ ] **Relevant thoughts** - All address the problem
- [ ] **Granularity appropriate** - Not too broad or narrow
- [ ] **Format consistent** - Standardized thought structure

### Evaluation

- [ ] **Scoring prompt created** - How to evaluate thoughts
- [ ] **Score range defined** - Typically 1-10
- [ ] **Criteria explicit** - What makes a good thought
- [ ] **Pruning threshold** - Below X score, don't expand

### Traversal

- [ ] **Selection strategy** - How to pick next thought
- [ ] **Backtracking enabled** - Can return to alternatives
- [ ] **Termination condition** - When to stop
- [ ] **Best path tracking** - Record winning path

### Resource Management

```
Monitor and limit:

✓ Total API calls (branching^depth worst case)
✓ Token usage per branch
✓ Wall-clock time
✓ Cost per solution
```

---

## Least-to-Most Checklist

### Decomposition Phase

- [ ] **Clear decomposition prompt** - How to break down
- [ ] **Ordering specified** - Simplest to most complex
- [ ] **Dependencies identified** - Which subproblems need others
- [ ] **Granularity appropriate** - Not too many/few subproblems

### Solution Phase

- [ ] **Context accumulation** - Previous solutions included
- [ ] **Subproblem format** - Clear input for each
- [ ] **Progress tracking** - Which subproblems solved
- [ ] **Error handling** - What if subproblem fails

### Synthesis Phase

- [ ] **Synthesis prompt** - How to combine solutions
- [ ] **All solutions included** - None missing
- [ ] **Coherent integration** - Parts fit together
- [ ] **Final answer extracted** - Clear conclusion

### Validation

```
Check:

✓ Decomposition is complete (covers full problem)
✓ Ordering is correct (dependencies respected)
✓ Each solution is valid
✓ Synthesis uses all solutions
✓ Final answer addresses original problem
```

---

## Production Deployment Checklist

### Pre-Deployment

- [ ] **Prompt tested** - Validated on representative inputs
- [ ] **Edge cases handled** - Graceful failures
- [ ] **Error handling** - Malformed responses handled
- [ ] **Fallback defined** - What to do when CoT fails
- [ ] **Cost estimated** - Token usage projections

### Monitoring Setup

- [ ] **Logging enabled** - Track inputs, outputs, reasoning
- [ ] **Metrics defined** - Accuracy, latency, cost
- [ ] **Alerts configured** - Notify on failures
- [ ] **Quality sampling** - Random audit of outputs

### Performance Optimization

- [ ] **Caching considered** - Cache similar problems?
- [ ] **Parallelization** - Concurrent requests if applicable
- [ ] **Timeout configured** - Max wait time
- [ ] **Token limits** - Max reasoning length

### Documentation

- [ ] **Prompt documented** - Version, purpose, parameters
- [ ] **Examples documented** - Test cases and expected behavior
- [ ] **Failure modes documented** - Known limitations
- [ ] **Runbook created** - How to troubleshoot

---

## Troubleshooting Checklist

### CoT Not Improving Results

- [ ] **Task appropriate** - Does task actually need reasoning?
- [ ] **Trigger phrase present** - CoT actually being invoked?
- [ ] **Prompt clear** - Instructions unambiguous?
- [ ] **Examples quality** - Few-shot examples correct?

### Reasoning is Irrelevant

- [ ] **Problem clearly stated** - Model understands task?
- [ ] **Context sufficient** - All needed information provided?
- [ ] **Constraints explicit** - Boundaries defined?

### Inconsistent Outputs

- [ ] **Temperature appropriate** - Lower for consistency
- [ ] **Format strictly defined** - Clear output structure
- [ ] **Examples consistent** - No conflicting patterns

### High Token Usage

- [ ] **Reasoning bounded** - Max steps defined?
- [ ] **Conciseness instructed** - "Be concise" added?
- [ ] **Zero-shot sufficient** - Do you need few-shot?

### Slow Performance

- [ ] **Technique appropriate** - Using simplest that works?
- [ ] **Samples minimal** - Self-consistency count optimal?
- [ ] **Depth limited** - ToT not going too deep?

---

## Quick Reference: Checklist Selection

| Situation | Use Checklist |
|-----------|---------------|
| First time implementing CoT | Pre-Implementation + Zero-Shot |
| Need specific format | Few-Shot CoT |
| Critical accuracy needed | Self-Consistency |
| Complex planning/search | Tree-of-Thoughts |
| Sequential subproblems | Least-to-Most |
| Going to production | Production Deployment |
| Something's not working | Troubleshooting |
