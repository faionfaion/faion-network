// purpose: MongoDB schema validation template.
// consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
// produces: a data-modeling artefact validating against scripts/validate-data-modeling.py
// depends-on: content/01-core-rules.xml, content/02-output-contract.xml
// token-budget-impact: ~400-1500 tokens once filled
// MongoDB document schema template
// Demonstrates embedded vs referenced patterns and schema validation

// -------------------------------------------------------------------
// EMBEDDED: use when child data is only accessed via parent
//           and the sub-document set is bounded and small (<100 items)
// -------------------------------------------------------------------
db.createCollection("order", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["userId", "status", "items", "totalAmount", "createdAt"],
      properties: {
        _id:         { bsonType: "objectId" },
        userId:      { bsonType: "objectId", description: "Reference to user collection" },
        status: {
          bsonType: "string",
          enum: ["pending", "confirmed", "shipped", "delivered", "cancelled"],
        },
        totalAmount: { bsonType: "decimal", minimum: 0 },
        // Embedded sub-documents — items are never queried independently
        items: {
          bsonType: "array",
          minItems: 1,
          items: {
            bsonType: "object",
            required: ["productId", "productName", "quantity", "unitPrice"],
            properties: {
              productId:   { bsonType: "objectId" },
              productName: { bsonType: "string" },   // denormalized at write time
              quantity:    { bsonType: "int", minimum: 1 },
              unitPrice:   { bsonType: "decimal", minimum: 0 },
            },
          },
        },
        createdAt:   { bsonType: "date" },
        updatedAt:   { bsonType: "date" },
      },
    },
  },
  validationLevel: "strict",
  validationAction: "error",
});

// Indexes for order
db.order.createIndex({ userId: 1, createdAt: -1 });         // orders by user, newest first
db.order.createIndex({ status: 1, createdAt: -1 });         // orders by status queue
db.order.createIndex({ "items.productId": 1 });             // reverse lookup: orders containing product


// -------------------------------------------------------------------
// REFERENCED: use when the related document is large, shared,
//             queried independently, or grows without bound
// -------------------------------------------------------------------
db.createCollection("product", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["sku", "name", "price", "isActive"],
      properties: {
        _id:      { bsonType: "objectId" },
        sku:      { bsonType: "string" },
        name:     { bsonType: "string" },
        price:    { bsonType: "decimal", minimum: 0 },
        isActive: { bsonType: "bool" },
        // Flexible attributes: use for truly variable fields only
        attributes: { bsonType: "object" },
        createdAt:  { bsonType: "date" },
        updatedAt:  { bsonType: "date" },
      },
    },
  },
});

db.product.createIndex({ sku: 1 }, { unique: true });
db.product.createIndex({ name: "text" });                   // full-text search
db.product.createIndex({ isActive: 1, price: 1 });          // active products by price
