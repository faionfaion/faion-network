# Tool Use Basics - Checklist

## Tool Definition

- [ ] Define tool with name, description, and input_schema
- [ ] Write clear, descriptive tool names (e.g., get_weather)
- [ ] Provide detailed description of when to use tool
- [ ] Define input_schema as JSON Schema object
- [ ] Specify required properties for input
- [ ] Use enum for restricted choice values
- [ ] Add descriptions to schema properties
- [ ] Document tool return values and error cases

## Basic Tool Usage

- [ ] Initialize client with API key
- [ ] Define tools array with tool definitions
- [ ] Pass tools parameter to messages.create()
- [ ] Check stop_reason for "tool_use" detection
- [ ] Parse response.content for tool_use blocks
- [ ] Extract tool name, id, and input from blocks
- [ ] Implement corresponding tool function

## Tool Invocation Loop

- [ ] Implement function to execute each tool
- [ ] Append assistant response with tool_use to messages
- [ ] Execute tool based on tool name
- [ ] Format tool result as tool_result object
- [ ] Include tool_use_id in tool_result
- [ ] Set is_error flag for error results
- [ ] Append tool_result to messages as user role
- [ ] Continue conversation with next API call
- [ ] Loop until stop_reason is "end_turn" or similar

## Tool Choice Configuration

- [ ] Use auto tool_choice (default, model decides)
- [ ] Use any tool_choice for required tool usage
- [ ] Use tool tool_choice to force specific tool
- [ ] Test different tool_choice strategies
- [ ] Document when to use each strategy
- [ ] Handle cases where model refuses tool use

## Parallel Tool Calls

- [ ] Support multiple tool calls in single response
- [ ] Parse all tool_use blocks from content
- [ ] Execute all tools (can be done in parallel)
- [ ] Collect all tool results
- [ ] Return all results in single user message
- [ ] Test parallel tool scenarios

## Error Handling

- [ ] Handle tool execution errors gracefully
- [ ] Set is_error flag in tool_result for failures
- [ ] Provide descriptive error messages
- [ ] Include error context for debugging
- [ ] Implement retry logic for transient errors
- [ ] Log tool errors for monitoring

## Testing & Validation

- [ ] Test each tool with valid inputs
- [ ] Test tool error handling
- [ ] Test multi-tool conversations
- [ ] Test parallel tool execution
- [ ] Verify tool output format
- [ ] Test edge cases for each tool
- [ ] Benchmark tool execution performance
- [ ] Document tool behavior and limitations
