// purpose: smoke Cypher schema for nosql-neo4j-patterns
// consumes: domain model
// produces: indexes + constraints + sample traversal
// depends-on: scripts/validate-nosql-neo4j-patterns.py
// token-budget-impact: ~250 tokens
// indexes + constraints
CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.user_id IS UNIQUE;
CREATE INDEX IF NOT EXISTS FOR (p:Product) ON (p.product_id);

// sample bounded traversal
PROFILE MATCH (u:User {user_id: $id})-[:PURCHASED*..3]->(p:Product) RETURN p LIMIT 50;
