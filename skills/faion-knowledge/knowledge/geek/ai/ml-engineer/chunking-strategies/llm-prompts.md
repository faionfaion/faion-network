# LLM Prompts for Chunking

Ready-to-use prompts for strategy selection, optimization, and debugging chunking pipelines.

---

## Table of Contents

1. [Strategy Selection Prompts](#1-strategy-selection-prompts)
2. [Optimization Prompts](#2-optimization-prompts)
3. [Debugging Prompts](#3-debugging-prompts)
4. [Analysis Prompts](#4-analysis-prompts)
5. [Agentic Chunking Prompts](#5-agentic-chunking-prompts)
6. [Evaluation Prompts](#6-evaluation-prompts)

---

## 1. Strategy Selection Prompts

### Document Analysis Prompt

```
Analyze this document and recommend the optimal chunking strategy.

Document Type: {document_type}
Content Length: {word_count} words
Sample Content (first 1000 characters):
---
{content_preview}
---

Consider the following factors:
1. Document structure (headers, sections, paragraphs)
2. Content density (technical vs. narrative)
3. Presence of code blocks, tables, or lists
4. Topic coherence and transitions
5. Expected query patterns

Available strategies:
- fixed: Fixed-size chunks (fast, simple)
- recursive: Split by separators recursively (balanced)
- semantic: Split by embedding similarity (context-aware)
- structure: Split by document structure like headers (hierarchical)
- code: Split by functions/classes (code-specific)
- agentic: LLM-decided splits (highest quality, expensive)

Respond with JSON:
{
    "recommended_strategy": "strategy_name",
    "reasoning": "explanation",
    "chunk_size": recommended_size_in_tokens,
    "overlap": recommended_overlap_percentage,
    "fallback_strategy": "alternative_if_primary_fails",
    "special_handling": ["any special considerations"]
}
```

### Multi-Document Batch Strategy Prompt

```
You need to chunk multiple documents of different types for a RAG system.

Documents:
{documents_summary}

For each document type, recommend:
1. Chunking strategy
2. Parameters (chunk_size, overlap)
3. Priority order for processing

Consider:
- Query patterns: {expected_query_types}
- Storage constraints: {storage_budget}
- Latency requirements: {latency_requirements}

Respond with a JSON mapping document type to chunking configuration.
```

### Query-Optimized Strategy Prompt

```
Given these sample queries that users will ask:

Queries:
{sample_queries}

And this document content:
---
{document_preview}
---

What chunking strategy will maximize retrieval accuracy?

Consider:
1. Query length (short factual vs. long complex)
2. Information density in document
3. Answer spans (single sentence vs. multiple paragraphs)

Recommend chunk_size and overlap to optimize for these query patterns.
```

---

## 2. Optimization Prompts

### Chunk Size Optimization Prompt

```
I'm experiencing retrieval issues with my RAG system.

Current configuration:
- Chunk size: {current_chunk_size} tokens
- Overlap: {current_overlap} tokens
- Strategy: {current_strategy}

Problems observed:
{observed_problems}

Sample failed queries and their expected answers:
{failed_examples}

Analyze the issues and recommend:
1. Optimal chunk size adjustment
2. Optimal overlap adjustment
3. Whether strategy change is needed
4. Any other optimizations

Respond with specific numbers and reasoning.
```

### Overlap Analysis Prompt

```
Analyze if my current overlap configuration is optimal.

Current setup:
- Chunk size: {chunk_size}
- Overlap: {overlap} ({overlap_percentage}%)
- Document type: {document_type}

Problems:
- {problem_1}
- {problem_2}

Sample chunk boundaries where context is lost:
---
Chunk 1 end: "{chunk1_end}"
Chunk 2 start: "{chunk2_start}"
---

Should I increase or decrease overlap? By how much? Why?
```

### Performance vs. Quality Tradeoff Prompt

```
Help me balance performance and quality for my chunking pipeline.

Current metrics:
- Chunking time: {chunking_time}ms per document
- Embedding cost: ${embedding_cost} per 1000 documents
- Retrieval precision@5: {precision}
- Retrieval recall@5: {recall}

Requirements:
- Max latency: {max_latency}ms
- Max cost per document: ${max_cost}
- Minimum acceptable precision: {min_precision}

Current strategy: {current_strategy}
Current chunk size: {chunk_size}

What optimizations can improve the cost/quality tradeoff?
```

### Embedding Model Selection for Semantic Chunking

```
I'm implementing semantic chunking and need to choose an embedding model.

Requirements:
- Document language: {language}
- Domain: {domain}
- Max tokens per chunk: {max_tokens}
- Budget: {budget_tier} (low/medium/high)
- Deployment: {deployment} (cloud/on-premise)

Candidates:
1. OpenAI text-embedding-3-small
2. OpenAI text-embedding-3-large
3. Jina embeddings v3
4. Sentence transformers (local)
5. Cohere embed v3

Recommend the best model considering:
- Semantic similarity quality for chunking
- Token limits and context
- Cost per 1M tokens
- Latency

Provide a ranked list with reasoning.
```

---

## 3. Debugging Prompts

### Chunk Quality Diagnosis Prompt

```
Debug these chunking issues.

Issue: {issue_description}

Sample problematic chunks:
---
Chunk 1: "{chunk1}"
Chunk 2: "{chunk2}"
Chunk 3: "{chunk3}"
---

Current configuration:
- Strategy: {strategy}
- Chunk size: {chunk_size}
- Overlap: {overlap}
- Separators: {separators}

What's causing the problem? How do I fix it?

Provide:
1. Root cause analysis
2. Specific fix recommendations
3. Configuration changes needed
4. Code changes if applicable
```

### Retrieval Failure Analysis Prompt

```
Analyze why this query failed to retrieve relevant content.

Query: "{failed_query}"

Expected relevant content:
---
{expected_content}
---

Retrieved chunks (top 5):
1. Score {score1}: "{chunk1}"
2. Score {score2}: "{chunk2}"
3. Score {score3}: "{chunk3}"
4. Score {score4}: "{chunk4}"
5. Score {score5}: "{chunk5}"

Current chunking setup:
- Strategy: {strategy}
- Chunk size: {chunk_size}
- Overlap: {overlap}

Why wasn't the relevant content retrieved? Is it a chunking issue or embedding issue?

Provide:
1. Diagnosis (chunking, embedding, or both)
2. How the expected content was actually chunked
3. Recommendations to fix
```

### Context Loss Debugging Prompt

```
Help me debug context loss in my chunks.

Original text:
---
{original_text}
---

Resulting chunks:
---
Chunk 1: "{chunk1}"
Chunk 2: "{chunk2}"
---

The problem is that Chunk 2 loses context because {context_problem}.

Current settings:
- Strategy: {strategy}
- Overlap: {overlap}

How should I modify my chunking to preserve this context?
```

### Code Chunking Debug Prompt

```
My code chunking is producing invalid chunks.

Source code ({language}):
```{language}
{source_code}
```

Resulting chunks:
{chunks_json}

Problems:
- {problem_1}
- {problem_2}

Current code chunker settings:
- Language: {language}
- Include imports: {include_imports}
- Max chunk size: {max_chunk_size}

Why is this happening? How do I fix the chunking logic?
```

---

## 4. Analysis Prompts

### Chunk Distribution Analysis Prompt

```
Analyze the chunk size distribution for my document collection.

Statistics:
- Total documents: {total_docs}
- Total chunks: {total_chunks}
- Average chunks per document: {avg_chunks_per_doc}
- Chunk size distribution:
  - Min: {min_size} words
  - Max: {max_size} words
  - Mean: {mean_size} words
  - Median: {median_size} words
  - Std dev: {std_size} words
  - 10th percentile: {p10_size}
  - 90th percentile: {p90_size}

Target chunk size: {target_size} words

Is this distribution healthy? What anomalies do you see?

Provide:
1. Distribution health assessment
2. Anomaly identification
3. Recommendations for improvement
4. Expected impact on retrieval
```

### Semantic Coherence Analysis Prompt

```
Evaluate the semantic coherence of these chunks.

Chunks to analyze:
---
Chunk 1: "{chunk1}"
---
Chunk 2: "{chunk2}"
---
Chunk 3: "{chunk3}"
---

For each chunk, rate on 1-5 scale:
1. Topic coherence (single topic vs. multiple)
2. Completeness (complete thought vs. partial)
3. Context independence (understandable alone vs. needs context)
4. Boundary quality (clean vs. mid-sentence/mid-paragraph)

Provide:
- Individual chunk scores
- Overall assessment
- Specific improvements needed
```

### Content Type Analysis Prompt

```
Analyze the content types present in this document and suggest chunking approach.

Document:
---
{document_content}
---

Identify:
1. Text sections (narrative, technical, instructions)
2. Code blocks (language, size)
3. Tables and structured data
4. Lists (bullet, numbered)
5. Headers and sections

For each content type found, recommend:
- Chunking strategy
- Special handling requirements
- Metadata to extract

Should I use a single strategy or multiple strategies for different sections?
```

---

## 5. Agentic Chunking Prompts

### Document Analysis for Agentic Chunking

```
Analyze this document to determine the optimal chunking approach.

Document:
---
{document_content}
---

Tasks:
1. Identify the document type and structure
2. Find natural topic boundaries
3. Identify sections that need special handling
4. Determine metadata to extract

Respond with JSON:
{
    "document_type": "type",
    "structure": {
        "has_headers": boolean,
        "has_code": boolean,
        "has_tables": boolean,
        "has_lists": boolean
    },
    "topic_boundaries": [
        {"position": approximate_char_position, "topic_change": "description"}
    ],
    "special_sections": [
        {"type": "code|table|list", "handling": "how to chunk"}
    ],
    "recommended_strategy": "strategy_name",
    "chunk_size": recommended_size,
    "metadata_fields": ["fields to extract"]
}
```

### Semantic Boundary Detection Prompt

```
Find semantic boundaries in this text for chunking.

Text:
---
{text}
---

Target chunk size: {target_size} words

Identify natural breakpoints where topics or concepts change.
For each breakpoint:
1. Position (approximate word/character offset)
2. Reason (topic change, section break, etc.)
3. Confidence (high/medium/low)

Do NOT split in the middle of:
- Sentences
- Paragraphs (unless necessary)
- Code blocks
- Lists
- Tables

Respond with JSON:
{
    "breakpoints": [
        {
            "position": offset,
            "reason": "explanation",
            "confidence": "high|medium|low"
        }
    ],
    "total_chunks": estimated_count
}
```

### Chunk Enrichment Prompt

```
Enrich these chunks with metadata for better retrieval.

Chunks:
{chunks_json}

For each chunk, generate:
1. Title (5-10 words summarizing content)
2. Summary (1-2 sentences)
3. Key entities (people, places, concepts)
4. Keywords (3-5 relevant search terms)
5. Category (topic category)
6. Difficulty level (if applicable)

Respond with JSON array of enriched chunks.
```

### Multi-Strategy Decision Prompt

```
This document has multiple content types. Decide chunking strategy for each section.

Document sections:
{sections_preview}

Available strategies:
1. recursive - general text
2. semantic - topic-coherent text
3. structure - structured documents
4. code - source code
5. fixed - uniform content

For each section, decide:
- Strategy to use
- Chunk size
- Whether to include overlap
- Metadata to extract

Respond with:
{
    "sections": [
        {
            "section_id": 1,
            "content_type": "type",
            "strategy": "strategy_name",
            "chunk_size": size,
            "overlap": percentage,
            "metadata_fields": ["fields"]
        }
    ]
}
```

### Chunk Quality Validation Prompt

```
Validate the quality of these chunks before indexing.

Chunks:
{chunks}

Check each chunk for:
1. Minimum length (at least {min_words} words)
2. Maximum length (at most {max_words} words)
3. Completeness (not cut mid-sentence)
4. Context (understandable without other chunks)
5. Content quality (not just whitespace, headers only, etc.)

For any chunk that fails validation:
- Explain the issue
- Suggest how to fix (merge, split, or reprocess)

Respond with:
{
    "valid_chunks": [indices],
    "invalid_chunks": [
        {
            "index": chunk_index,
            "issues": ["list of issues"],
            "fix": "recommended fix"
        }
    ]
}
```

---

## 6. Evaluation Prompts

### Chunk Relevance Scoring Prompt

```
Score how relevant each chunk is to the given query.

Query: "{query}"

Chunks:
1. "{chunk1}"
2. "{chunk2}"
3. "{chunk3}"
4. "{chunk4}"
5. "{chunk5}"

For each chunk, provide:
- Relevance score (0-10, where 10 is highly relevant)
- Reasoning
- Whether it contains the answer (yes/no/partial)

This helps evaluate if our chunking captures relevant information together.
```

### Chunking Quality Assessment Prompt

```
Assess the overall quality of this chunking approach.

Original document (first 500 words):
---
{document_preview}
---

Resulting chunks:
{chunks}

Evaluate:
1. Coverage: Does chunking capture all important information?
2. Coherence: Are chunks semantically coherent?
3. Redundancy: Is there appropriate overlap, or wasteful duplication?
4. Granularity: Are chunks the right size for retrieval?
5. Boundaries: Are chunk boundaries at natural points?

Rate each dimension 1-5 and provide overall assessment.
```

### Retrieval Simulation Prompt

```
Simulate retrieval for these test queries.

Chunks available:
{chunks_with_ids}

Test queries:
{queries}

For each query:
1. Rank chunks by relevance (top 5)
2. Identify if the answer is fully contained in retrieved chunks
3. Note if important context is missing

This simulates retrieval to identify chunking issues before deployment.
```

### Comparative Strategy Evaluation Prompt

```
Compare chunking results from two strategies.

Original text:
---
{original_text}
---

Strategy A ({strategy_a_name}) chunks:
{strategy_a_chunks}

Strategy B ({strategy_b_name}) chunks:
{strategy_b_chunks}

Compare on:
1. Number of chunks
2. Average chunk coherence
3. Information preservation
4. Retrieval suitability for these query types: {query_types}

Which strategy is better for this use case? Why?
```

---

## Usage Tips

### Prompt Variables

When using these prompts, replace placeholders:

| Placeholder | Description |
|-------------|-------------|
| `{document_type}` | Type of document (legal, technical, code, etc.) |
| `{word_count}` | Number of words in document |
| `{content_preview}` | First N characters of content |
| `{strategy}` | Current chunking strategy name |
| `{chunk_size}` | Current chunk size in tokens/words |
| `{overlap}` | Current overlap amount |
| `{chunks}` / `{chunks_json}` | JSON array of chunk objects |
| `{query}` | User query for retrieval |

### Best Practices

1. **Be specific about context**: Include document type, domain, and use case
2. **Provide examples**: Include sample content and expected behavior
3. **Request structured output**: Use JSON format for programmatic processing
4. **Include constraints**: Mention budget, latency, and quality requirements
5. **Iterate**: Use analysis prompts to refine strategy prompts

### Model Recommendations

| Task | Recommended Model |
|------|-------------------|
| Strategy selection | GPT-4o, Claude 3.5 Sonnet |
| Debugging | GPT-4o (detailed reasoning) |
| Quick analysis | GPT-4o-mini, Claude 3.5 Haiku |
| Agentic chunking | GPT-4o, Claude 3.5 Sonnet |
| Batch processing | GPT-4o-mini (cost efficiency) |

### Cost Optimization

For production use:
1. Cache strategy decisions for similar document types
2. Use cheaper models (GPT-4o-mini) for routine analysis
3. Reserve expensive models for complex/important decisions
4. Batch similar documents for single analysis prompt
