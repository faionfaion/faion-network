// GraphRAG Cypher traversal patterns

// 1-hop neighborhood
MATCH (n:Entity {name: $entity_name})-[r]-(neighbor)
RETURN n, r, neighbor LIMIT 50;

// 2-hop with relationship type filter
MATCH path = (n:Entity {name: $entity_name})-[r*1..2]-(related)
WHERE ALL(rel IN relationships(path) WHERE type(rel) IN $relationship_types)
RETURN path LIMIT 100;

// Weighted traversal — strong edges only
MATCH (n:Entity {name: $entity_name})-[r]-(neighbor)
WHERE r.weight > 0.5
RETURN n, r, neighbor ORDER BY r.weight DESC LIMIT 20;

// Shortest path between two entities
MATCH path = shortestPath(
  (a:Entity {name: $source})-[*1..5]-(b:Entity {name: $target})
)
RETURN path;

// Hybrid: vector search + 2-hop graph expansion
CALL db.index.vector.queryNodes('entity_embeddings', 10, $query_embedding)
YIELD node, score
WHERE score > 0.7
MATCH (node)-[r*1..2]-(related)
RETURN node, score,
       collect(DISTINCT {
         entity: related.name,
         relationship: type(r),
         properties: properties(r)
       }) AS context
ORDER BY score DESC;
