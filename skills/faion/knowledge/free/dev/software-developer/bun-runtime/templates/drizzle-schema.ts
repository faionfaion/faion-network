// src/db/schema.ts — Drizzle ORM schema with bun:sqlite
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core"
import { sql } from "drizzle-orm"

export const users = sqliteTable("users", {
  id: text("id").primaryKey(),
  email: text("email").notNull().unique(),
  name: text("name").notNull(),
  createdAt: integer("created_at", { mode: "timestamp" })
    .notNull()
    .default(sql`CURRENT_TIMESTAMP`),
})

// src/db/index.ts — Drizzle instance with bun:sqlite
import { drizzle } from "drizzle-orm/bun-sqlite"
import { Database } from "bun:sqlite"
import * as schema from "./schema"

const sqlite = new Database("app.db")
export const db = drizzle(sqlite, { schema })
