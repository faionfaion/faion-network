# LLM Prompts for Vector Databases

Prompts for database selection, performance optimization, debugging, and implementation guidance.

---

## Table of Contents

- [Database Selection Prompts](#database-selection-prompts)
- [Performance Optimization Prompts](#performance-optimization-prompts)
- [Debugging Prompts](#debugging-prompts)
- [Implementation Prompts](#implementation-prompts)
- [Migration Prompts](#migration-prompts)
- [Architecture Review Prompts](#architecture-review-prompts)

---

## Database Selection Prompts

### Initial Requirements Gathering

```
You are a vector database consultant helping select the right database for a project.

Ask clarifying questions about:
1. Scale: Expected number of vectors (current and 12-month growth)
2. Performance: Latency requirements (p50, p95, p99), QPS expectations
3. Query patterns: Filtering complexity, hybrid search needs
4. Infrastructure: Cloud vs self-hosted, existing tech stack
5. Team: DevOps capabilities, familiarity with specific databases
6. Budget: Monthly cost constraints
7. Compliance: Security requirements (SOC2, HIPAA, GDPR)

Based on answers, recommend one of:
- Qdrant: Production self-hosted, complex filtering
- Weaviate: Knowledge graphs, semantic relationships
- Milvus: Enterprise scale (1B+ vectors)
- Pinecone: Managed service, zero ops
- pgvector: Existing PostgreSQL apps
- Chroma: Prototyping, local development

Provide reasoning for your recommendation and potential alternatives.
```

### Quick Selection Decision

```
Based on these requirements, recommend a vector database:

Requirements:
- Vector count: {vector_count}
- Update frequency: {update_frequency}
- Latency requirement: {latency_ms}ms p95
- Filtering needs: {filtering_complexity}
- Hosting preference: {self_hosted_or_managed}
- Existing infrastructure: {existing_tech}
- Team expertise: {devops_level}
- Monthly budget: ${budget}

Consider these options:
1. Qdrant - Self-hosted production, excellent filtering
2. Weaviate - Knowledge graphs, hybrid search
3. Milvus - Billion-scale, high throughput
4. Pinecone - Managed serverless, zero ops
5. pgvector - PostgreSQL extension, SQL integration
6. Chroma - Prototyping, simple API

Provide:
1. Primary recommendation with reasoning
2. Alternative option
3. Key configuration recommendations
4. Estimated monthly cost
5. Potential migration path if needs change
```

### Comparison Analysis

```
Compare {database_1} vs {database_2} for the following use case:

Use Case: {description}

Analyze across these dimensions:
1. Performance (latency, throughput, recall)
2. Filtering capabilities
3. Hybrid search support
4. Operational complexity
5. Cost at scale
6. Community and documentation
7. SDK quality for {programming_language}
8. Production readiness

Provide a clear recommendation with trade-offs.
```

---

## Performance Optimization Prompts

### Index Tuning

```
I need to optimize the HNSW index for my vector database.

Current configuration:
- Database: {database_name}
- Vector count: {vector_count}
- Vector dimensions: {dimensions}
- Current M: {current_m}
- Current ef_construct: {current_ef_construct}
- Current ef_search: {current_ef_search}

Performance metrics:
- Current latency (p95): {current_latency}ms
- Current recall: {current_recall}%
- Target latency: {target_latency}ms
- Target recall: {target_recall}%

Recommend:
1. Optimal M value
2. Optimal ef_construct value
3. Optimal ef_search value
4. Whether to enable quantization
5. Expected memory usage change
6. Expected performance change

Explain the trade-offs of each recommendation.
```

### Query Optimization

```
My vector search queries are slow. Help me optimize.

Database: {database_name}
Query pattern:
```
{query_code}
```

Current performance:
- Average latency: {avg_latency}ms
- P95 latency: {p95_latency}ms
- Queries per second: {qps}

Available information:
- Collection size: {collection_size} vectors
- Filter complexity: {filter_description}
- Index type: {index_type}
- Hardware: {hardware_specs}

Analyze and provide:
1. Potential bottlenecks
2. Index optimization recommendations
3. Query restructuring suggestions
4. Caching strategies
5. Hardware scaling recommendations if needed

Provide optimized query code.
```

### Memory Optimization

```
I need to reduce memory usage for my vector database.

Current state:
- Database: {database_name}
- Vector count: {vector_count}
- Vector dimensions: {dimensions}
- Current memory usage: {current_memory}GB
- Available memory: {available_memory}GB
- Payload size (average): {avg_payload_size}KB

Constraints:
- Maximum acceptable recall loss: {max_recall_loss}%
- Maximum acceptable latency increase: {max_latency_increase}%

Recommend memory reduction strategies:
1. Quantization options (scalar, product, binary)
2. On-disk storage configurations
3. Payload optimization
4. Index parameter adjustments

For each recommendation, provide:
- Expected memory reduction
- Impact on performance
- Implementation steps
```

### Scaling Analysis

```
Help me plan scaling for my vector database.

Current state:
- Database: {database_name}
- Current vector count: {current_vectors}
- Current QPS: {current_qps}
- Current latency (p95): {current_latency}ms
- Current hardware: {hardware_specs}

Growth projections:
- Expected vectors in 6 months: {projected_vectors_6m}
- Expected vectors in 12 months: {projected_vectors_12m}
- Expected QPS growth: {qps_growth_rate}%/month

Constraints:
- Latency SLA: {latency_sla}ms p95
- Budget ceiling: ${monthly_budget}/month

Provide scaling recommendations:
1. Vertical scaling options
2. Horizontal scaling strategy
3. Sharding/partitioning approach
4. Index optimization for scale
5. Cost projection at each milestone
6. Warning signs to watch for
```

---

## Debugging Prompts

### Slow Query Investigation

```
Debug slow vector search query.

Database: {database_name}
Query:
```
{query_code}
```

Symptoms:
- Expected latency: {expected_latency}ms
- Actual latency: {actual_latency}ms
- Occurs: {frequency} (always/sometimes/specific conditions)

Collection info:
- Vector count: {vector_count}
- Dimensions: {dimensions}
- Index type: {index_type}
- Index parameters: {index_params}

System metrics during slow queries:
- CPU usage: {cpu_percent}%
- Memory usage: {memory_percent}%
- Disk I/O: {disk_io}

Recent changes:
{recent_changes}

Help me:
1. Identify the root cause
2. Provide diagnostic queries/commands to run
3. Suggest fixes in order of likelihood
4. Recommend monitoring to prevent recurrence
```

### Low Recall Investigation

```
My vector search recall is lower than expected.

Database: {database_name}
Embedding model: {embedding_model}

Test setup:
- Test queries: {num_test_queries}
- Expected relevant docs per query: {expected_relevant}
- Ground truth method: {ground_truth_method}

Results:
- Current recall@10: {current_recall}%
- Expected recall@10: {expected_recall}%
- Precision@10: {current_precision}%

Index configuration:
- Type: {index_type}
- Parameters: {index_params}

Investigate:
1. Is the embedding model appropriate for this data?
2. Are index parameters optimal?
3. Could data preprocessing be an issue?
4. Are there data quality issues?

Provide:
1. Diagnostic steps to identify root cause
2. Specific parameter adjustments to try
3. Data quality checks to perform
4. Alternative approaches if index tuning doesn't help
```

### Connection Issues

```
Troubleshoot vector database connection problems.

Database: {database_name}
Client: {client_library} version {client_version}
Server: {server_version}

Error message:
```
{error_message}
```

Connection configuration:
```
{connection_config}
```

Environment:
- Client location: {client_location}
- Server location: {server_location}
- Network: {network_type} (VPC, public, localhost)
- TLS: {tls_enabled}

Symptoms:
- Frequency: {frequency}
- Time of occurrence: {time_pattern}
- Affected operations: {affected_operations}

Help me:
1. Identify the cause of connection failures
2. Provide specific troubleshooting steps
3. Suggest configuration changes
4. Recommend resilience patterns to handle transient failures
```

### Data Inconsistency

```
Investigate data inconsistency in vector database.

Database: {database_name}

Symptoms:
- Expected document count: {expected_count}
- Actual document count: {actual_count}
- Specific inconsistency: {description}

Operations that may have caused this:
{recent_operations}

Consistency configuration:
- Replication factor: {replication_factor}
- Consistency level: {consistency_level}
- Write concern: {write_concern}

Help me:
1. Diagnose the root cause
2. Verify data integrity
3. Recover missing/corrupted data
4. Prevent future inconsistencies
5. Set up monitoring for data integrity
```

---

## Implementation Prompts

### Collection Design

```
Design a vector database collection/schema for my use case.

Use case: {use_case_description}

Data characteristics:
- Document types: {document_types}
- Average document length: {avg_length}
- Metadata fields needed: {metadata_fields}
- Expected relationships: {relationships}

Query patterns:
- Primary query type: {primary_query}
- Filters commonly used: {common_filters}
- Hybrid search needed: {hybrid_search}

Scale requirements:
- Initial documents: {initial_count}
- Growth rate: {growth_rate}
- Query volume: {query_volume}

Database: {database_name}

Design:
1. Collection/table schema
2. Vector field configuration
3. Metadata/payload structure
4. Index configuration
5. Payload indexes for filtering
6. Partitioning strategy (if needed)

Provide complete schema definition code.
```

### Hybrid Search Implementation

```
Implement hybrid search (vector + keyword) for my application.

Database: {database_name}
Programming language: {language}

Requirements:
- Dense vectors from: {embedding_model}
- Sparse vectors/keywords: {keyword_approach}
- Fusion method: {fusion_method}
- Result count: {k}

Data structure:
- Document fields: {fields}
- Example document: {example_doc}

Query example:
- User query: "{example_query}"
- Expected behavior: {expected_behavior}

Provide:
1. Collection schema with both dense and sparse vectors
2. Indexing code for documents
3. Hybrid search implementation
4. Tuning recommendations (alpha/weights)
5. Reranking integration (optional)

Include error handling and logging.
```

### Filtering Implementation

```
Implement complex filtering for vector search.

Database: {database_name}
Programming language: {language}

Filter requirements:
- Categorical filters: {categorical_fields}
- Numeric range filters: {numeric_fields}
- Date filters: {date_fields}
- Text search: {text_search_fields}
- Nested/array filters: {nested_fields}

Example queries:
1. {example_filter_1}
2. {example_filter_2}
3. {example_filter_3}

Provide:
1. Payload/metadata index creation
2. Filter builder utility
3. Query examples for each filter type
4. Combination of filters (AND, OR, NOT)
5. Performance optimization tips
```

### Batch Operations

```
Implement efficient batch operations for vector database.

Database: {database_name}
Programming language: {language}

Requirements:
- Operation type: {upsert/delete/update}
- Batch size: {batch_size}
- Total records: {total_records}
- Rate limit (if any): {rate_limit}

Data source:
- Source type: {source_type}
- Data format: {data_format}
- Example record: {example_record}

Constraints:
- Memory limit: {memory_limit}
- Time limit: {time_limit}
- Error handling: {error_strategy}

Provide:
1. Batch processing function
2. Progress tracking
3. Error handling and retry logic
4. Memory-efficient streaming (if applicable)
5. Logging and monitoring
6. Resume capability for interrupted operations
```

---

## Migration Prompts

### Database Migration

```
Plan migration from {source_db} to {target_db}.

Source database:
- Type: {source_db}
- Vector count: {vector_count}
- Schema: {source_schema}
- Indexes: {source_indexes}

Target database:
- Type: {target_db}
- Hosting: {target_hosting}

Requirements:
- Downtime tolerance: {downtime_tolerance}
- Data validation: {validation_requirements}
- Rollback capability: {rollback_needed}

Provide:
1. Pre-migration checklist
2. Schema mapping (source to target)
3. Migration script
4. Validation queries
5. Cutover procedure
6. Rollback plan
7. Post-migration verification
```

### Embedding Model Migration

```
Plan embedding model migration for existing vector database.

Current state:
- Database: {database_name}
- Current embedding model: {current_model}
- Vector dimensions: {current_dimensions}
- Vector count: {vector_count}

Target:
- New embedding model: {new_model}
- New dimensions: {new_dimensions}

Constraints:
- Downtime tolerance: {downtime_tolerance}
- Reprocessing time available: {time_available}
- Budget for embeddings API: ${embedding_budget}

Provide:
1. Strategy options (in-place vs parallel collection)
2. Recommended approach with reasoning
3. Implementation steps
4. Validation plan
5. Cutover procedure
6. Cost and time estimates
```

---

## Architecture Review Prompts

### System Design Review

```
Review my vector search architecture.

Architecture diagram/description:
{architecture_description}

Components:
- Vector database: {database}
- Embedding service: {embedding_service}
- Application layer: {app_layer}
- Caching: {caching_strategy}

Scale:
- Current: {current_scale}
- Target: {target_scale}

Review for:
1. Performance bottlenecks
2. Scalability concerns
3. Reliability/availability
4. Cost efficiency
5. Security considerations
6. Operational complexity

Provide:
1. Identified issues (ranked by severity)
2. Specific recommendations
3. Alternative architectures to consider
4. Quick wins vs long-term improvements
```

### RAG Pipeline Review

```
Review my RAG pipeline architecture.

Pipeline components:
1. Document ingestion: {ingestion_process}
2. Chunking strategy: {chunking_strategy}
3. Embedding model: {embedding_model}
4. Vector database: {vector_database}
5. Retrieval: {retrieval_strategy}
6. Reranking: {reranking_approach}
7. Generation: {llm_model}

Current metrics:
- Retrieval recall: {retrieval_recall}%
- Answer relevance: {answer_relevance}
- Latency: {latency}ms
- Cost per query: ${cost_per_query}

Issues observed:
{observed_issues}

Review and recommend:
1. Chunking optimization
2. Embedding model selection
3. Retrieval strategy improvements
4. Reranking effectiveness
5. Prompt optimization
6. Caching opportunities
7. Cost reduction strategies
```

### Production Readiness Review

```
Assess production readiness of vector search implementation.

Implementation details:
- Database: {database}
- Hosting: {hosting}
- Current environment: {environment}

Checklist areas to review:
1. High availability
2. Backup and recovery
3. Monitoring and alerting
4. Security
5. Performance under load
6. Operational runbooks
7. Capacity planning

Current state for each area:
{current_state}

Provide:
1. Readiness score (1-10) for each area
2. Critical gaps that must be addressed
3. Recommended improvements
4. Prioritized action items
5. Estimated effort for each item
```

---

## Usage Guidelines

### Prompt Customization

When using these prompts:

1. **Replace placeholders**: Fill in all `{placeholder}` values with actual data
2. **Add context**: Include relevant error messages, logs, or code snippets
3. **Specify constraints**: Mention any limitations (budget, time, expertise)
4. **Define success criteria**: What does "solved" look like?

### Iterative Refinement

For complex problems:

1. Start with a broad prompt to understand the issue
2. Follow up with specific diagnostic prompts
3. Validate recommendations before implementing
4. Request implementation details for chosen solution

### Documentation

After resolving issues:

1. Ask for documentation of the solution
2. Request runbook entries for common issues
3. Get monitoring recommendations to prevent recurrence

---

*LLM Prompts v2.0*
*Part of vector-databases skill*
