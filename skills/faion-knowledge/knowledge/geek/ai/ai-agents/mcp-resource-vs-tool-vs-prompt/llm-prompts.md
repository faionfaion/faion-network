# LLM Prompts — MCP Resource vs Tool vs Prompt

## Prompt 1: Classify capabilities

```
For each capability below, classify as Tool, Resource, or Prompt using the three-question test:

1. Does the model need to act / mutate / fetch live? → Tool
2. Is this content the model reads (static-per-URI)? → Resource
3. Is this a slash command the user invokes? → Prompt

Output STRICT JSON:
{
  "classifications": [
    {"capability": "...", "type": "tool"|"resource"|"prompt", "rationale": "..."}
  ]
}

Capabilities:
{list}
```

## Prompt 2: Audit existing MCP server

```
Review this MCP server's capabilities. Flag:
- Tools that always return the same content (should be Resources)
- Resources with side effects (should be Tools)
- Tools meant for user invocation (should be Prompts)
- Mode-arg tools that should be split into N named tools

Output: list of issues with proposed reclassifications.

Capabilities:
{paste}
```

## Prompt 3: Design new MCP server

```
You are designing an MCP server for {domain}. List the capabilities the server should expose, classified as Tool, Resource, or Prompt. Include verb_object names, signatures, descriptions.

Output STRICT JSON.

Domain:
{description}
```

## Prompt 4: Generate cross-runtime test

```
Given an MCP server with these primitives, generate a test plan that exercises each primitive on:
- Anthropic MCP host
- OpenAI Responses API + MCP
- Vercel AI SDK 6
- LangChain MCP adapter

For each, list expected behavior and known gaps.

Server:
{server description}
```
