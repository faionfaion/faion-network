# Prompt Basics - Checklist

## Prompt Structure

- [ ] Create PromptTemplate class for reusable templates
- [ ] Define system prompt with role definition
- [ ] Define user_template with variable placeholders
- [ ] Structure prompts with clear sections (context, task, format)
- [ ] Use delimiters for clarity (---,###, etc.)
- [ ] Document prompt variables and their purpose

## System Prompt Design

- [ ] Define model role clearly (e.g., "You are a data analyst")
- [ ] Specify behavioral constraints (be concise, ask clarifying questions)
- [ ] Document output format expectations
- [ ] Include guidelines and best practices
- [ ] Separate instruction from content in system prompt
- [ ] Test system prompt effectiveness

## Zero-shot Prompting

- [ ] Write simple, clear task descriptions
- [ ] Include output format instructions
- [ ] Test with single examples
- [ ] Evaluate output quality
- [ ] Refine based on results
- [ ] Document effective zero-shot patterns

## Few-shot Prompting

- [ ] Create examples array for few-shot learning
- [ ] Include input/output pairs for examples
- [ ] Add 2-5 examples (quality over quantity)
- [ ] Cover edge cases in examples
- [ ] Format examples consistently
- [ ] Test output with few-shot approach
- [ ] Compare few-shot vs zero-shot quality

## Chain-of-Thought Prompting

- [ ] Add "Let's think step by step" to prompt
- [ ] Encourage explicit reasoning in examples
- [ ] Test with complex reasoning tasks
- [ ] Evaluate intermediate steps
- [ ] Document when CoT improves results
- [ ] Use for math, logic, and debugging tasks

## Self-consistency Prompting

- [ ] Generate multiple samples for same prompt
- [ ] Implement voting mechanism for answers
- [ ] Compare accuracy vs single sample
- [ ] Document consistency improvements
- [ ] Use for complex, ambiguous problems
- [ ] Balance cost vs reliability

## ReAct Pattern

- [ ] Define "Reason" instruction (think through problem)
- [ ] Define "Act" instruction (take action/call tool)
- [ ] Implement reasoning before tool calls
- [ ] Test ReAct on tool-use scenarios
- [ ] Document tool interaction flows
- [ ] Validate reasoning quality

## Constraint and Format Definition

- [ ] Specify exact output format (markdown, JSON, etc.)
- [ ] Define required fields in structured output
- [ ] Set content constraints (length, tone, style)
- [ ] Add validation requirements
- [ ] Include examples of desired format
- [ ] Test format compliance

## Testing & Iteration

- [ ] Test prompts with diverse inputs
- [ ] Compare outputs across different model versions
- [ ] Measure output quality metrics
- [ ] Identify edge cases that fail
- [ ] Refine prompts based on failures
- [ ] Document prompt versions and improvements
- [ ] Track prompt performance over time
