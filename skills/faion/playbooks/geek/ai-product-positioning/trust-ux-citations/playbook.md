---
name: trust-ux-citations
description: Design AI-output UI patterns — inline footnote citations, source side-panel, confidence-band color coding, and explicit "I don't know" fallbacks — so users can verify every AI answer.
tier: geek
group: ai-product-positioning
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working React component set that renders AI-generated answers with inline numbered citations linked to retrieved source chunks, a collapsible side-panel showing the raw source excerpt alongside the answer, confidence bands (high / medium / low) displayed via Tailwind color tokens, and a structured "I don't know" fallback that names the exact gap in retrieved knowledge. Users can click any citation to see exactly which source chunk drove that sentence, and low-confidence answers are visually distinct before the user even reads the text.

## Prerequisites

- React 18+ with TypeScript.
- Tailwind CSS v3+ (or equivalent utility classes).
- A RAG backend that returns structured output: `answer`, `citations[]`, `confidence`, and optional `knowledge_gap`. Use the Anthropic Python SDK with `claude-sonnet-4-6` or `claude-opus-4-7` for generation.
- `pip install anthropic>=0.51 pydantic>=2.0` on the backend.
- Familiarity with the RAG retrieval pipeline — specifically how chunks carry a `source_id`, `url`, and `excerpt` in metadata.
- Read [knowledge/geek/ai/rag-engineer/rag-implementation](../../../knowledge/geek/ai/rag-engineer/rag-implementation) — the chunk metadata schema and retrieval response format that Steps 1–2 extend with citation fields.

## Steps

1. **Define the structured citation response schema on the backend.**

   The model must emit citations as a typed list alongside the answer text. Use Pydantic v2 and the Anthropic SDK's tool-use / structured-output path to enforce the shape:

   ```python
   # trust_ux/schemas.py
   from __future__ import annotations
   from enum import Enum
   from pydantic import BaseModel, Field


   class Confidence(str, Enum):
       HIGH = "high"
       MEDIUM = "medium"
       LOW = "low"


   class Citation(BaseModel):
       index: int = Field(..., description="1-based footnote number matching [^N] in answer_text")
       source_id: str = Field(..., description="Unique ID of the retrieved chunk")
       url: str = Field(..., description="Canonical URL of the source document")
       title: str = Field(..., description="Document or section title")
       excerpt: str = Field(..., description="Verbatim 1–3 sentence excerpt from the chunk")


   class CitedAnswer(BaseModel):
       answer_text: str = Field(
           ...,
           description=(
               "Answer in Markdown. Every factual claim carries an inline citation "
               "like [^1]. Use [^N] for each citation index."
           ),
       )
       citations: list[Citation] = Field(default_factory=list)
       confidence: Confidence
       knowledge_gap: str | None = Field(
           None,
           description=(
               "If confidence is LOW, name what specific information was missing "
               "from retrieved chunks. Leave null otherwise."
           ),
       )
   ```

2. **Call the model and force structured output via tool use.**

   Pass retrieved chunks in the system prompt and require the model to respond using the `CitedAnswer` tool:

   ```python
   # trust_ux/generate.py
   from __future__ import annotations
   import json
   import anthropic
   from trust_ux.schemas import CitedAnswer

   _client = anthropic.Anthropic()

   SYSTEM = """You are a precise research assistant.
   You receive retrieved document chunks and a user question.
   Answer ONLY from the provided chunks.
   For every factual sentence add an inline citation [^N] where N matches a citation index.
   If retrieved chunks do not contain enough information to answer confidently,
   set confidence to "low" and fill knowledge_gap with what is missing."""


   def answer_with_citations(question: str, chunks: list[dict]) -> CitedAnswer:
       """chunks: list of {source_id, url, title, excerpt}"""
       chunk_block = "\n\n".join(
           f"[Chunk {i+1}] source_id={c['source_id']} title={c['title']}\n{c['excerpt']}"
           for i, c in enumerate(chunks)
       )
       tools = [
           {
               "name": "cited_answer",
               "description": "Structured answer with citations and confidence.",
               "input_schema": CitedAnswer.model_json_schema(),
           }
       ]
       response = _client.messages.create(
           model="claude-sonnet-4-6",
           max_tokens=1024,
           system=SYSTEM,
           tools=tools,  # type: ignore[arg-type]
           tool_choice={"type": "tool", "name": "cited_answer"},
           messages=[
               {
                   "role": "user",
                   "content": f"Chunks:\n{chunk_block}\n\nQuestion: {question}",
               }
           ],
       )
       tool_block = next(b for b in response.content if b.type == "tool_use")
       return CitedAnswer.model_validate(tool_block.input)
   ```

3. **Build the `CitationMark` inline component.**

   Each `[^N]` token in `answer_text` is replaced with a superscript button that opens the corresponding source panel:

   ```tsx
   // src/components/CitationMark.tsx
   import React from "react";

   interface Props {
     index: number;
     onClick: (index: number) => void;
   }

   export function CitationMark({ index, onClick }: Props) {
     return (
       <sup>
         <button
           onClick={() => onClick(index)}
           className="ml-0.5 text-blue-600 hover:text-blue-800 underline decoration-dotted
                      text-xs font-semibold focus:outline-none focus-visible:ring-2
                      focus-visible:ring-blue-500 rounded"
           aria-label={`View source ${index}`}
         >
           [{index}]
         </button>
       </sup>
     );
   }
   ```

4. **Build the `AnswerRenderer` that parses `[^N]` markers and injects `CitationMark`.**

   Split `answer_text` on the `[^N]` pattern and interleave text nodes with citation buttons:

   ```tsx
   // src/components/AnswerRenderer.tsx
   import React from "react";
   import { CitationMark } from "./CitationMark";

   const CITATION_RE = /\[\^(\d+)\]/g;

   interface Props {
     text: string;
     onCitationClick: (index: number) => void;
   }

   export function AnswerRenderer({ text, onCitationClick }: Props) {
     const parts: React.ReactNode[] = [];
     let cursor = 0;
     let match: RegExpExecArray | null;

     while ((match = CITATION_RE.exec(text)) !== null) {
       if (match.index > cursor) {
         parts.push(text.slice(cursor, match.index));
       }
       const idx = parseInt(match[1], 10);
       parts.push(
         <CitationMark key={`cite-${idx}-${match.index}`} index={idx} onClick={onCitationClick} />
       );
       cursor = match.index + match[0].length;
     }
     if (cursor < text.length) {
       parts.push(text.slice(cursor));
     }

     return <p className="text-base leading-7 text-gray-900">{parts}</p>;
   }
   ```

5. **Add a confidence-band header using Tailwind color tokens.**

   Map the three confidence levels to distinct color schemes so users see the signal before reading the answer:

   ```tsx
   // src/components/ConfidenceBadge.tsx
   import React from "react";

   type Confidence = "high" | "medium" | "low";

   const CONFIG: Record<Confidence, { label: string; classes: string }> = {
     high: {
       label: "High confidence",
       classes: "bg-emerald-50 text-emerald-800 border-emerald-200",
     },
     medium: {
       label: "Medium confidence",
       classes: "bg-amber-50 text-amber-800 border-amber-200",
     },
     low: {
       label: "Low confidence",
       classes: "bg-red-50 text-red-800 border-red-200",
     },
   };

   interface Props {
     confidence: Confidence;
     knowledgeGap?: string | null;
   }

   export function ConfidenceBadge({ confidence, knowledgeGap }: Props) {
     const { label, classes } = CONFIG[confidence];
     return (
       <div className={`rounded-md border px-3 py-2 text-sm font-medium mb-3 ${classes}`}>
         {label}
         {confidence === "low" && knowledgeGap && (
           <p className="mt-1 font-normal text-xs">
             Missing: {knowledgeGap}
           </p>
         )}
       </div>
     );
   }
   ```

6. **Build the `SourcePanel` side-by-side drawer showing source vs. answer.**

   Render the active citation's title, URL, and verbatim excerpt in a collapsible panel pinned to the right of the answer column:

   ```tsx
   // src/components/SourcePanel.tsx
   import React from "react";

   interface Citation {
     index: number;
     source_id: string;
     url: string;
     title: string;
     excerpt: string;
   }

   interface Props {
     citation: Citation | null;
     onClose: () => void;
   }

   export function SourcePanel({ citation, onClose }: Props) {
     if (!citation) return null;

     return (
       <aside
         className="w-80 shrink-0 border-l border-gray-200 bg-gray-50 p-4 overflow-y-auto"
         aria-label="Source citation"
       >
         <div className="flex items-start justify-between mb-3">
           <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
             Source [{citation.index}]
           </span>
           <button
             onClick={onClose}
             className="text-gray-400 hover:text-gray-600 text-lg leading-none"
             aria-label="Close source panel"
           >
             ×
           </button>
         </div>
         <p className="text-sm font-semibold text-gray-900 mb-1">{citation.title}</p>
         <a
           href={citation.url}
           target="_blank"
           rel="noopener noreferrer"
           className="text-xs text-blue-600 hover:underline break-all block mb-3"
         >
           {citation.url}
         </a>
         <blockquote className="border-l-2 border-gray-300 pl-3 text-sm text-gray-700 italic leading-6">
           {citation.excerpt}
         </blockquote>
       </aside>
     );
   }
   ```

7. **Compose the full `TrustAnswer` page layout.**

   Wire all components together. The answer column and source panel share a flex row; clicking a citation opens the panel and highlights the source:

   ```tsx
   // src/components/TrustAnswer.tsx
   import React, { useState } from "react";
   import { AnswerRenderer } from "./AnswerRenderer";
   import { ConfidenceBadge } from "./ConfidenceBadge";
   import { SourcePanel } from "./SourcePanel";

   interface Citation {
     index: number;
     source_id: string;
     url: string;
     title: string;
     excerpt: string;
   }

   interface CitedAnswer {
     answer_text: string;
     citations: Citation[];
     confidence: "high" | "medium" | "low";
     knowledge_gap?: string | null;
   }

   interface Props {
     answer: CitedAnswer;
   }

   export function TrustAnswer({ answer }: Props) {
     const [activeIndex, setActiveIndex] = useState<number | null>(null);

     const activeCitation =
       activeIndex !== null
         ? answer.citations.find((c) => c.index === activeIndex) ?? null
         : null;

     return (
       <div className="flex gap-0 max-w-4xl mx-auto">
         {/* Answer column */}
         <div className="flex-1 px-6 py-5">
           <ConfidenceBadge
             confidence={answer.confidence}
             knowledgeGap={answer.knowledge_gap}
           />
           <AnswerRenderer
             text={answer.answer_text}
             onCitationClick={(idx) =>
               setActiveIndex((prev) => (prev === idx ? null : idx))
             }
           />
           {answer.citations.length > 0 && (
             <footer className="mt-4 border-t border-gray-100 pt-3">
               <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                 Sources
               </p>
               <ol className="space-y-1">
                 {answer.citations.map((c) => (
                   <li key={c.source_id} className="text-xs text-gray-600">
                     <span className="font-semibold">[{c.index}]</span>{" "}
                     <a
                       href={c.url}
                       target="_blank"
                       rel="noopener noreferrer"
                       className="text-blue-600 hover:underline"
                     >
                       {c.title}
                     </a>
                   </li>
                 ))}
               </ol>
             </footer>
           )}
         </div>

         {/* Source panel */}
         <SourcePanel citation={activeCitation} onClose={() => setActiveIndex(null)} />
       </div>
     );
   }
   ```

## Verify

Render a hardcoded `CitedAnswer` fixture in a Storybook story or plain React dev server and check all four trust signals:

```tsx
// src/stories/TrustAnswer.stories.tsx
import { TrustAnswer } from "../components/TrustAnswer";

const fixture = {
  answer_text:
    "RAG pipelines retrieve document chunks before generation.[^1] " +
    "Confidence scoring is derived from reranker logits.[^2]",
  citations: [
    {
      index: 1,
      source_id: "doc-001",
      url: "https://docs.anthropic.com/en/docs/build-with-claude/retrieval-augmented-generation",
      title: "Retrieval-Augmented Generation — Anthropic Docs",
      excerpt:
        "RAG grounds model responses in retrieved document chunks, reducing hallucination " +
        "by constraining generation to verified source material.",
    },
    {
      index: 2,
      source_id: "doc-042",
      url: "https://www.pinecone.io/learn/series/rag/rerankers/",
      title: "Rerankers and Two-Stage Retrieval — Pinecone",
      excerpt:
        "A reranker model assigns a relevance score to each (query, chunk) pair; " +
        "the top-K by score enter the context window.",
    },
  ],
  confidence: "high" as const,
  knowledge_gap: null,
};

export default { title: "TrustAnswer", component: TrustAnswer };
export const HighConfidence = () => <TrustAnswer answer={fixture} />;
export const LowConfidence = () => (
  <TrustAnswer
    answer={{
      ...fixture,
      confidence: "low",
      knowledge_gap: "No retrieved chunks cover the 2025 pricing changes.",
    }}
  />
);
```

Checks to confirm manually:

- `[1]` and `[2]` render as superscript buttons in the answer text.
- Clicking `[1]` opens the side panel with the Anthropic docs excerpt.
- Clicking the same button again closes the panel.
- `LowConfidence` story shows a red banner with the `knowledge_gap` text before the answer.
- The footer sources list shows both titles as links.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `[^N]` appears as raw text instead of citation button | `CITATION_RE` uses `[^(\d+)]` but the model emitted `[1]` (no caret) | Update the regex to also match `\[(\d+)\]`; adjust the system prompt to enforce `[^N]` format |
| Source panel stays open after navigating to a new question | `activeIndex` state not reset between answer loads | Call `setActiveIndex(null)` in the parent's fetch handler when `answer` prop changes (`useEffect`) |
| `knowledge_gap` is null but confidence is "low" | Model ignored the schema instruction | Add an explicit Pydantic `model_validator` that enforces `knowledge_gap is not None` when `confidence == LOW` |
| `CitedAnswer.model_json_schema()` produces `$defs` references Anthropic rejects | Pydantic v2 generates nested `$defs`; Anthropic tool schema must be flat | Call `CitedAnswer.model_json_schema(mode="serialization")` and flatten with `jsonref.replace_refs` |
| Confidence badge color doesn't change in Tailwind JIT | Dynamic class strings purged at build | Add `bg-emerald-50`, `bg-amber-50`, `bg-red-50` (and border/text variants) to `tailwind.config.js` `safelist` |
| Backend returns `citations: []` even when chunks are relevant | Model omitted citations because answer was paraphrased across multiple chunks | Strengthen system prompt: "You MUST cite every chunk you used, even if you paraphrase across them. Omitting a citation for a used chunk is an error." |

## Next

- Add citation-hover tooltips: on `mouseenter` over `CitationMark`, show a floating popover with the excerpt without requiring a click — reduces friction for quick source checks; see the `SourcePanel` pattern from Step 6.
- Implement confidence calibration: log each `(confidence, user_thumbs_up/down)` pair and retrain the system prompt or reranker threshold when logged `high-confidence + thumbs_down` rate exceeds 5%.
- Extend to multi-turn chat: preserve `citations[]` per message turn in a `messages` array so users can scroll back and click citations from earlier turns.

## References

- [knowledge/geek/ai/rag-engineer/rag-implementation](../../../knowledge/geek/ai/rag-engineer/rag-implementation) — chunk metadata schema (`source_id`, `url`, `excerpt`) and retrieval response structure that the `Citation` Pydantic model in Step 1 directly extends
- [knowledge/geek/ai/llm-integration/structured-output-patterns](../../../knowledge/geek/ai/llm-integration/structured-output-patterns) — tool-use forced-output pattern used in Step 2 to guarantee `CitedAnswer` JSON shape from `claude-sonnet-4-6`
- [knowledge/geek/ai/llm-integration/guardrails-implementation](../../../knowledge/geek/ai/llm-integration/guardrails-implementation) — low-confidence fallback and knowledge-gap signalling patterns that back the `knowledge_gap` field and the "I don't know" render path in Steps 1 and 5
