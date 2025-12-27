# Tasks: RAG Content Ingestion Pipeline using Sitemap, Cohere, and Qdrant

**Feature**: RAG Content Ingestion Pipeline using Sitemap, Cohere, and Qdrant
**Branch**: `006-sitemap-ingestion`
**Created**: 2025-12-25
**Spec**: [spec.md](spec.md)
**Plan**: [plan.md](plan.md)

## Dependencies

- User Story 2 (Clean Content Extraction) depends on User Story 1 (Sitemap Content Fetching)
- User Story 3 (Semantic Content Chunking) depends on User Story 2 (Clean Content Extraction)
- User Story 4 (Embedding Generation and Storage) depends on User Story 3 (Semantic Content Chunking)

## Parallel Execution Examples

- **Phase 2 (Foundational)**: T001 [P], T002 [P], T003 [P] can run in parallel
- **User Story 2**: Content fetching for different URLs can run in parallel after sitemap is loaded
- **User Story 3**: Text processing for different pages can run in parallel
- **User Story 4**: Embedding generation can be batched and run in parallel

## Implementation Strategy

- MVP: Complete User Story 1 (Sitemap fetching) + basic User Story 2 (content extraction)
- Incremental delivery: Add chunking, embeddings, and storage in phases
- Each user story delivers independent value

---

## Phase 1: Setup

### Goal
Initialize project structure and dependencies for the ingestion pipeline.

- [x] T001 Create backend/ingestion directory structure
- [x] T002 [P] Create requirements.txt with required dependencies
- [x] T003 [P] Create .env.example file with required environment variables
- [x] T004 Create main entry point file backend/ingestion/ingest.py
- [x] T005 Create __init__.py files for Python package structure
- [x] T006 Set up logging configuration in backend/ingestion/__init__.py

---

## Phase 2: Foundational

### Goal
Implement core configuration and initialization components that are prerequisites for all user stories.

- [x] T007 Create configuration module backend/ingestion/config.py
- [x] T008 [P] Implement environment variable validation in config.py
- [x] T009 Create sitemap loader module backend/ingestion/sitemap_loader.py
- [x] T010 [P] Create text processing module backend/ingestion/text_processor.py
- [x] T011 Create embedding module backend/ingestion/embeddings.py
- [x] T012 [P] Create Qdrant client module backend/ingestion/qdrant_client.py
- [x] T013 [P] Implement error handling utilities in backend/ingestion/utils.py

---

## Phase 3: User Story 1 - Sitemap Content Fetching (Priority: P1)

### Goal
As a system administrator, I want to fetch all documentation URLs from a live sitemap so that I can ensure all content is indexed for the RAG system.

### Independent Test
Can be fully tested by configuring a sitemap URL and verifying that all URLs are extracted and logged successfully, delivering the complete set of pages to process.

- [x] T014 [US1] Implement sitemap fetching functionality in sitemap_loader.py
- [x] T015 [US1] Add XML parsing for sitemap in sitemap_loader.py
- [x] T016 [US1] Handle malformed sitemap errors gracefully in sitemap_loader.py
- [x] T017 [US1] Extract all URLs from sitemap and return list of SitemapEntry objects
- [x] T018 [US1] Add logging for sitemap processing in sitemap_loader.py
- [x] T019 [US1] Implement sitemap index handling (nested sitemaps) in sitemap_loader.py
- [x] T020 [US1] Add validation for extracted URLs in sitemap_loader.py

---

## Phase 4: User Story 2 - Clean Content Extraction (Priority: P2)

### Goal
As a content consumer, I want the system to extract clean, readable text from each documentation page so that the RAG system can provide accurate responses based on the content.

### Independent Test
Can be fully tested by processing individual URLs and verifying that clean, readable text is extracted while navigation, scripts, and styles are excluded.

- [x] T021 [US2] Implement HTML fetching for URLs in text_processor.py
- [x] T022 [US2] Add HTML parsing and content extraction using BeautifulSoup in text_processor.py
- [x] T023 [US2] Remove navigation, scripts, and styles from extracted content in text_processor.py
- [x] T024 [US2] Add error handling for invalid or empty pages in text_processor.py
- [x] T025 [US2] Extract page titles from HTML in text_processor.py
- [x] T026 [US2] Add content validation and word count in text_processor.py
- [x] T027 [US2] Implement retry mechanism for failed content fetches in text_processor.py

---

## Phase 5: User Story 3 - Semantic Content Chunking (Priority: P3)

### Goal
As a RAG system user, I want content to be split into semantically meaningful chunks so that the search and retrieval process can find relevant information efficiently.

### Independent Test
Can be fully tested by taking content and verifying it's split into chunks ≤ 1200 characters with preserved sentence boundaries, traceable to source URLs.

- [x] T028 [US3] Implement text chunking logic in text_processor.py
- [x] T029 [US3] Ensure chunks are ≤ 1200 characters in text_processor.py
- [x] T030 [US3] Preserve sentence boundaries during chunking in text_processor.py
- [x] T031 [US3] Generate unique chunk IDs with source URL and position in text_processor.py
- [x] T032 [US3] Add chunk metadata (position, character count) in text_processor.py
- [x] T033 [US3] Validate chunk quality and coherence in text_processor.py

---

## Phase 6: User Story 4 - Embedding Generation and Storage (Priority: P4)

### Goal
As a RAG system user, I want content chunks to be converted to embeddings and stored in Qdrant so that semantic search can be performed efficiently.

### Independent Test
Can be fully tested by taking chunks and verifying they're converted to embeddings and stored in Qdrant with proper metadata.

### Part A: Embedding Generation
- [x] T034 [US4] Initialize Cohere client with API key from config in embeddings.py
- [x] T035 [US4] Implement embedding generation using embed-english-v3.0 model in embeddings.py
- [x] T036 [US4] Set input type to 'search_document' for embeddings in embeddings.py
- [x] T037 [US4] Validate 1024-dimensional vectors are generated in embeddings.py
- [x] T038 [US4] Implement batch processing for embeddings to optimize API usage in embeddings.py
- [x] T039 [US4] Add error handling for Cohere API rate limits in embeddings.py

### Part B: Qdrant Storage
- [x] T040 [US4] Initialize Qdrant client with configuration from config in qdrant_client.py
- [x] T041 [US4] Create or recreate Qdrant collection with cosine distance in qdrant_client.py
- [x] T042 [US4] Store embeddings with proper metadata (url, text, chunk_id) in qdrant_client.py
- [x] T043 [US4] Implement duplicate prevention for safe re-ingestion in qdrant_client.py
- [x] T044 [US4] Add progress logging for vector storage in qdrant_client.py
- [x] T045 [US4] Implement content replacement for outdated entries in qdrant_client.py

---

## Phase 7: Idempotency & Safety

### Goal
Implement safe re-ingestion without creating duplicates and replace outdated content cleanly.

- [x] T046 [P] Add duplicate detection logic to prevent re-storing identical content
- [x] T047 Implement safe re-ingestion that replaces outdated content
- [x] T048 Add comprehensive logging for ingestion progress and failures
- [x] T049 Implement resume capability for interrupted ingestion processes
- [x] T050 Add validation to confirm all sitemap URLs were processed
- [x] T051 Add confirmation that all vectors were stored successfully

---

## Phase 8: Integration & Main Pipeline

### Goal
Combine all components into a cohesive ingestion pipeline with proper error handling.

- [x] T052 [P] Create main ingestion workflow in backend/ingestion/ingest.py
- [x] T053 Integrate sitemap loading with content extraction in main workflow
- [x] T054 Connect content extraction to text chunking in main workflow
- [x] T055 Link chunking to embedding generation in main workflow
- [x] T056 Connect embeddings to Qdrant storage in main workflow
- [x] T057 Add overall progress tracking and reporting in main workflow
- [x] T058 Implement graceful shutdown on errors in main workflow

---

## Phase 9: Polish & Cross-Cutting Concerns

### Goal
Add final touches, documentation, and quality improvements to the complete system.

- [x] T059 [P] Add comprehensive error logging throughout all modules
- [x] T060 Create README.md for backend/ingestion module
- [x] T061 Add command-line argument support for main ingestion script
- [x] T062 Implement memory-efficient processing for large documents
- [x] T063 Add progress indicators and status updates during ingestion
- [x] T064 Optimize API calls with appropriate rate limiting and batching
- [x] T065 Add final validation to confirm 100% of sitemap URLs ingested successfully
- [x] T066 Verify all content stored as vectorized chunks in Qdrant collection
- [x] T067 Confirm ingestion completes without errors and is deterministic