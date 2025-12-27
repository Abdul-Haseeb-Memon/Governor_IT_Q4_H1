---
id: 11
title: Sitemap Content Ingestion Spec
stage: spec
date: 2025-12-25
surface: agent
model: claude-sonnet-4-5-20250929
feature: sitemap-ingestion
branch: 006-sitemap-ingestion
user: unknown
command: /sp.specify
labels: ["spec", "ingestion", "qdrant", "cohere", "sitemap"]
links:
  spec: specs/006-sitemap-ingestion/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/006-sitemap-ingestion/spec.md
 - specs/006-sitemap-ingestion/checklists/requirements.md
tests:
 - none
---

## Prompt

/sp.specify RAG Content Ingestion Pipeline using Sitemap, Cohere, and Qdrant

Target system:
Backend ingestion layer for a Retrieval-Augmented Generation (RAG) chatbot powering a published Docusaurus book.

Context:
The system ingests live documentation content from a Vercel-hosted site and prepares it for semantic retrieval. This spec defines ONLY the ingestion layer and serves as the foundation for retrieval, answer generation, and frontend integration.

Objective:
Build a clean, deployable ingestion pipeline that:
- Fetches all documentation URLs from a sitemap
- Extracts clean textual content from each page
- Chunks content into semantically coherent pieces
- Generates embeddings using Cohere `embed-english-v3.0`
- Stores embeddings in Qdrant Cloud with proper metadata
- Supports safe re-ingestion without duplication

Target sitemap:
https://governor-it-q4-h1.vercel.app/sitemap.xml

Functional requirements:
- Fetch and parse `sitemap.xml` and extract all page URLs
- Gracefully handle sitemap fetch or parse failures
- Download HTML for each URL and extract readable text only
- Skip empty or unreadable pages with clear logging
- Chunk text into segments ≤ 1200 characters while preserving sentence boundaries
- Generate embeddings using:
  - Provider: Cohere
  - Model: embed-english-v3.0
  - Input type: search_document
  - Dimension: 1024
- Store embeddings in Qdrant Cloud using cosine similarity
- Each stored chunk MUST include metadata:
  - source URL
  - chunk text
  - unique chunk ID
- Re-running ingestion MUST NOT create duplicate content
- Collection recreation MUST be explicit and logged

Configuration constraints:
- All secrets MUST be loaded from `.env`
- No hard-coded credentials
- Required environment variables:
  - COHERE_API_KEY
  - QDRANT_URL
  - QDRANT_API_KEY
  - QDRANT_COLLECTION_NAME
  - SITEMAP_URL
- Must support local and cloud deployment

Non-goals:
- Frontend implementation
- Retrieval or search logic
- OpenRouter or LLM answer generation
- Evaluation or testing scripts
- Debug or experimental code
- Unused helper files

Success criteria:
- 100% of sitemap URLs ingested successfully
- All content stored as vectorized chunks in a single Qdrant collection
- Ingestion completes without errors
- Progress and failures are clearly logged
- Output is deterministic and reproducible

Required output structure:
backend/
└── ingestion/
    ├── ingest.py
    ├── embeddings.py
    ├── qdrant_client.py
    ├── sitemap_loader.py
    ├── text_processor.py
    └── README.md

Quality bar:
- Production-grade code only
- One responsibility per file
- No duplicate logic
- Clean imports
- Fully compatible with future specs:
  - Retrieval
  - Answer generation
  - Frontend integration

Final instruction:
Implement this ingestion spec only.
Do not add speculative features.
Do not include unused code.
This module is the foundation of the full RAG system.

## Response snapshot

Created comprehensive specification for sitemap-based content ingestion into Qdrant using Cohere embeddings. The specification defines a robust, spec-driven ingestion pipeline that fetches documentation URLs from sitemaps, extracts clean content, chunks it semantically, generates embeddings, and stores them in Qdrant with proper metadata.

## Outcome

- ✅ Impact: Created complete specification for sitemap ingestion system that serves as foundation for RAG chatbot
- 🧪 Tests: none
- 📁 Files: Created specs/006-sitemap-ingestion/spec.md, specs/006-sitemap-ingestion/checklists/requirements.md
- 🔁 Next prompts: /sp.plan to create implementation plan
- 🧠 Reflection: Specification follows spec-first methodology with clear, testable requirements for ingestion layer

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Create implementation plan for the sitemap ingestion system