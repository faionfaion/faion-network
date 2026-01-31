# Chain-of-Thought Basics - Checklist

## Zero-shot CoT

- [ ] Add "Let's think step by step" to prompt
- [ ] Implement zero-shot CoT on complex tasks
- [ ] Test reasoning quality without examples
- [ ] Evaluate answer correctness
- [ ] Document cases where zero-shot CoT helps
- [ ] Compare with non-CoT prompts
- [ ] Use for math, logic, and debugging tasks

## Few-shot CoT

- [ ] Create examples with reasoning steps shown
- [ ] Include step-by-step thinking in examples
- [ ] Add final answer after reasoning
- [ ] Provide 2-5 examples minimum
- [ ] Cover different problem types
- [ ] Test few-shot performance vs zero-shot
- [ ] Evaluate example quality impact

## Reasoning Steps

- [ ] Implement numbered step format (1., 2., 3., etc.)
- [ ] Guide model to explicit reasoning
- [ ] Use prompt: "Break this down step by step"
- [ ] Parse intermediate steps from response
- [ ] Validate logical progression
- [ ] Extract reasoning quality metrics
- [ ] Document common reasoning patterns

## Answer Extraction

- [ ] Implement parsing for final answer
- [ ] Separate reasoning from answer in prompt
- [ ] Use prompt: "Final answer: "
- [ ] Extract last paragraph/sentence as answer
- [ ] Validate answer against expected format
- [ ] Handle cases where answer is embedded in reasoning
- [ ] Implement fallback extraction strategies

## Self-consistency for Reliability

- [ ] Generate multiple samples (N=5-10)
- [ ] Extract answers from each sample
- [ ] Implement majority voting
- [ ] Track answer frequency
- [ ] Use most consistent answer
- [ ] Measure consistency improvement
- [ ] Balance cost vs reliability

## Complex Reasoning Tasks

- [ ] Test on math word problems
- [ ] Test on logic puzzles
- [ ] Test on coding problems
- [ ] Test on strategy questions
- [ ] Evaluate reasoning correctness
- [ ] Document task complexity levels
- [ ] Identify when CoT helps most

## Performance & Cost

- [ ] Measure token usage with/without CoT
- [ ] Compare quality vs cost trade-offs
- [ ] Evaluate inference time
- [ ] Track reliability improvements
- [ ] Document performance metrics
- [ ] Optimize example selection
- [ ] Balance explanation length vs accuracy

## Testing & Validation

- [ ] Test zero-shot vs few-shot vs multi-shot
- [ ] Test reasoning quality metrics
- [ ] Test answer extraction accuracy
- [ ] Test on diverse problem types
- [ ] Validate on known test sets
- [ ] Compare reasoning patterns
- [ ] Document best practices learned
