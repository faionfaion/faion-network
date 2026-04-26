// Neo4j GraphRAG schema setup
// Run once during initial setup

// Entity uniqueness constraints
CREATE CONSTRAINT entity_name IF NOT EXISTS
FOR (e:Entity) REQUIRE e.name IS UNIQUE;

// Vector index for semantic search
CREATE VECTOR INDEX entity_embeddings IF NOT EXISTS
FOR (e:Entity) ON e.embedding
OPTIONS {indexConfig: {
  `vector.dimensions`: 1536,
  `vector.similarity_function`: 'cosine'
}};

// Fulltext index for hybrid search
CREATE FULLTEXT INDEX entity_fulltext IF NOT EXISTS
FOR (e:Entity) ON EACH [e.name, e.description];

// Traversal performance indexes
CREATE INDEX entity_type IF NOT EXISTS FOR (e:Entity) ON (e.type);
CREATE INDEX relationship_type IF NOT EXISTS FOR ()-[r:RELATED_TO]-() ON (r.type);
