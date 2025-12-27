# Implementation Plan: RAG Content Ingestion Pipeline using Sitemap, Cohere, and Qdrant

**Branch**: `006-sitemap-ingestion` | **Date**: 2025-12-25 | **Spec**: [link to spec.md](../spec.md)
**Input**: Feature specification from `/specs/006-sitemap-ingestion/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a production-ready ingestion pipeline that loads documentation content from a sitemap, embeds it using Cohere, and stores it in Qdrant Cloud for RAG usage. The pipeline will fetch all documentation URLs from a sitemap, extract clean textual content, chunk it into semantically coherent pieces, generate embeddings using Cohere embed-english-v3.0, and store them in Qdrant Cloud with proper metadata.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**:
- requests (for HTTP requests)
- beautifulsoup4 (for HTML parsing)
- cohere (for embeddings)
- qdrant-client (for vector storage)
- python-dotenv (for environment variables)
- lxml (for XML parsing)
**Storage**: Qdrant Cloud (vector database)
**Testing**: pytest (for unit and integration tests)
**Target Platform**: Linux server (deployment-ready)
**Project Type**: backend (single project)
**Performance Goals**: Process 100+ documentation pages within 30 minutes, generate embeddings efficiently
**Constraints**: Must work within free-tier limitations for Cohere and Qdrant, <1200 char chunks, idempotent execution
**Scale/Scope**: Handle sitemap with 50+ documentation pages, store thousands of content chunks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Spec-First, AI-Driven Authoring**: Implementation follows formal specifications from Spec-Kit Plus ✓
2. **Technical Accuracy and Clarity**: All technical content meets professional standards and is factually accurate ✓
3. **Reproducibility and Maintainability**: Architecture and processes are reproducible and maintainable ✓
4. **No Unsupported or Speculative Content**: Only verified, proven technologies and practices allowed ✓
5. **Docusaurus-First Documentation Framework**: Technical book platform uses Docusaurus with MDX ✓
6. **RAG-Powered Chatbot Integration**: Chatbot will provide accurate, context-aware responses without hallucinations ✓
7. **Free-Tier Infrastructure Compliance**: All infrastructure choices work within free-tier limitations ✓
8. **GitHub Pages Deployment**: Final output will be deployable to GitHub Pages ✓

## Project Structure

### Documentation (this feature)

```text
specs/006-sitemap-ingestion/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command output)
├── data-model.md        # Phase 1 output (/sp.plan command output)
├── quickstart.md        # Phase 1 output (/sp.plan command output)
├── contracts/           # Phase 1 output (/sp.plan command output)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
└── ingestion/
    ├── ingest.py                 # Main ingestion entry point
    ├── embeddings.py            # Cohere embedding generation
    ├── qdrant_client.py         # Qdrant storage operations
    ├── sitemap_loader.py        # Sitemap parsing and URL extraction
    ├── text_processor.py        # Content extraction and chunking
    ├── config.py                # Environment configuration
    ├── __init__.py
    └── README.md
```

**Structure Decision**: Selected Option 2: Web application backend structure with dedicated ingestion module. The ingestion pipeline will be implemented as a backend service with a clean, modular architecture following single responsibility principle.

## Implementation Phases

### Phase 1: Configuration & Setup
- Load environment variables from `.env`
- Validate required configs: COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME, SITEMAP_URL
- Initialize Cohere and Qdrant clients

### Phase 2: Sitemap Processing
- Fetch `sitemap.xml` from target URL
- Parse XML and extract all page URLs
- Handle unreachable or malformed sitemap gracefully

### Phase 3: Content Ingestion
- Fetch HTML for each URL
- Extract clean, readable text
- Skip empty or invalid pages with logging

### Phase 4: Text Processing
- Chunk extracted text into ≤1200 character segments
- Preserve sentence boundaries
- Attach source URL metadata to each chunk

### Phase 5: Embedding Generation
- Generate embeddings using Cohere embed-english-v3.0
- Input type: search_document
- Ensure 1024-dimensional vectors

### Phase 6: Vector Storage
- Create or recreate Qdrant collection explicitly
- Store each chunk as a vector point
- Include metadata: url, text, chunk_id
- Use cosine similarity

### Phase 7: Idempotency & Safety
- Prevent duplicate ingestion
- Replace outdated content cleanly
- Log ingestion progress and failures

### Phase 8: Validation & Completion
- Confirm all sitemap URLs processed
- Confirm vectors stored successfully
- Exit cleanly with success message

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [None] | [No violations identified] | [N/A] |