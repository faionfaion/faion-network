# Candidate Methodologies

Format per candidate:

```
## CAND-NN: <slug>
- **Category:** so- | mm- | tu- | pl- | lp- | mem- | cli- | eval- | cost- | mcp-
- **Source:** URL or `project:path/to/file.py`
- **Status:** new | reviewed | accepted | rejected | duplicate-of(ID)
- **Why valuable:** 1 sentence
- **One-line rule:** the actionable nugget
```

---

(seeded by user — must be among first accepted)

## CAND-01: schema-field-order-autoregressive
- **Category:** so-
- **Source:** user-spec
- **Status:** new
- **Why valuable:** Hidden structured-output trick that gives free CoT context: fields generated later "see" fields generated earlier.
- **One-line rule:** In a structured-output schema, place dependent fields after their dependencies (e.g., `title` AFTER `content` so the title is generated from the content, not the other way around).

## CAND-02: weak-model-preselection
- **Category:** mm-
- **Source:** user-spec
- **Status:** new
- **Why valuable:** Cuts 5-10x cost on long-context filtering before strong-model reasoning.
- **One-line rule:** Use a cheap/small model to filter or select inputs (e.g., return only file paths or item IDs), then pass the filtered set to the strong model for actual work.

## CAND-03: file-reference-passing
- **Category:** pl-
- **Source:** user-spec
- **Status:** new
- **Why valuable:** Avoids context blow-up; lets next pipeline step decide what to load.
- **One-line rule:** When agent step N analyzes content, return only references (file paths, IDs, URLs) — not raw content — for step N+1 to load on demand.
