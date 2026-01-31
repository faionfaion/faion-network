# Chain-of-Thought Techniques - Checklist

## Least-to-Most Prompting

- [ ] Break complex problems into subproblems
- [ ] Solve simpler subproblems first
- [ ] Use subproblem solutions to solve main problem
- [ ] Implement step-by-step decomposition
- [ ] Test on multi-step reasoning tasks
- [ ] Document decomposition strategies
- [ ] Measure effectiveness vs standard CoT

## Plan-First Approach

- [ ] Generate plan before reasoning
- [ ] Separate planning from execution
- [ ] Include planning steps in prompt
- [ ] Refine plan based on initial reasoning
- [ ] Test on complex multi-part problems
- [ ] Validate plan quality
- [ ] Implement plan extraction

## Self-Refine Pattern

- [ ] Generate initial answer
- [ ] Implement self-critique step
- [ ] Refine answer based on critique
- [ ] Iterate improvement cycles
- [ ] Test on complex problems
- [ ] Measure improvement progression
- [ ] Document refinement strategies

## Tree-of-Thought

- [ ] Generate multiple reasoning paths
- [ ] Implement path evaluation
- [ ] Select best path
- [ ] Explore alternative branches
- [ ] Test on decision-making problems
- [ ] Benchmark vs single-path reasoning
- [ ] Document exploration strategies

## Performance Optimization

- [ ] Measure token usage of advanced CoT techniques
- [ ] Compare quality vs cost trade-offs
- [ ] Optimize example count
- [ ] Reduce unnecessary reasoning steps
- [ ] Test on varied problem complexities
- [ ] Document optimal configurations
- [ ] Implement caching for common subproblems

## Testing & Validation

- [ ] Test all advanced techniques
- [ ] Compare technique effectiveness
- [ ] Measure quality metrics
- [ ] Test on diverse problem types
- [ ] Benchmark performance
- [ ] Document best practices
- [ ] Build technique library
