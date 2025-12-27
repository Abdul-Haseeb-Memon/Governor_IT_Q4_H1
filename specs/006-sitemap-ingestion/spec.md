# Feature Specification: RAG Content Ingestion Pipeline using Sitemap, Cohere, and Qdrant

**Feature Branch**: `006-sitemap-ingestion`
**Created**: 2025-12-25
**Status**: Draft
**Input**: User description: "RAG Content Ingestion Pipeline using Sitemap, Cohere, and Qdrant"

## Context

The system ingests live documentation content from a Vercel-hosted site and prepares it for semantic retrieval. This spec defines ONLY the ingestion layer and serves as the foundation for retrieval, answer generation, and frontend integration.

## Objective

Build a clean, deployable ingestion pipeline that:
- Fetches all documentation URLs from a sitemap
- Extracts clean textual content from each page
- Chunks content into semantically coherent pieces
- Generates embeddings using Cohere `embed-english-v3.0`
- Stores embeddings in Qdrant Cloud with proper metadata
- Supports safe re-ingestion without duplication

## Target Sitemap

https://governor-it-q4-h1.vercel.app/sitemap.xml

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Sitemap Content Fetching (Priority: P1)

As a system administrator, I want to fetch all documentation URLs from a live sitemap so that I can ensure all content is indexed for the RAG system.

**Why this priority**: This is the foundational capability that enables all other features. Without content fetching, no other functionality is possible.

**Independent Test**: Can be fully tested by configuring a sitemap URL and verifying that all URLs are extracted and logged successfully, delivering the complete set of pages to process.

**Acceptance Scenarios**:

1. **Given** a valid sitemap.xml URL, **When** the ingestion process starts, **Then** all URLs from the sitemap are successfully extracted and stored for processing
2. **Given** an invalid or unreachable sitemap URL, **When** the ingestion process starts, **Then** the system logs an error and fails gracefully without crashing

---

### User Story 2 - Clean Content Extraction (Priority: P2)

As a content consumer, I want the system to extract clean, readable text from each documentation page so that the RAG system can provide accurate responses based on the content.

**Why this priority**: This is the core value-add that converts raw HTML pages into useful content that can be processed by the embedding system.

**Independent Test**: Can be fully tested by processing individual URLs and verifying that clean, readable text is extracted while navigation, scripts, and styles are excluded.

**Acceptance Scenarios**:

1. **Given** a documentation page with HTML content, **When** content extraction runs, **Then** clean readable text is extracted with navigation and scripts excluded
2. **Given** an empty or unreadable page, **When** content extraction runs, **Then** the system logs an error and continues processing other pages

---

### User Story 3 - Semantic Content Chunking (Priority: P3)

As a RAG system user, I want content to be split into semantically meaningful chunks so that the search and retrieval process can find relevant information efficiently.

**Why this priority**: This optimizes the retrieval quality by ensuring chunks are meaningful and within optimal size limits for embedding models.

**Independent Test**: Can be fully tested by taking content and verifying it's split into chunks ≤ 1200 characters with preserved sentence boundaries, traceable to source URLs.

**Acceptance Scenarios**:

1. **Given** a long text document, **When** chunking process runs, **Then** the text is split into semantically coherent chunks of ≤ 1200 characters
2. **Given** a text document, **When** chunking process runs, **Then** sentence boundaries are preserved and each chunk is traceable to its source URL

---

### User Story 4 - Embedding Generation and Storage (Priority: P4)

As a RAG system user, I want content chunks to be converted to embeddings and stored in Qdrant so that semantic search can be performed efficiently.

**Why this priority**: This is the final step that makes content searchable and enables the RAG system to function effectively.

**Independent Test**: Can be fully tested by taking chunks and verifying they're converted to embeddings and stored in Qdrant with proper metadata.

**Acceptance Scenarios**:

1. **Given** content chunks, **When** embedding generation runs, **Then** vectors are generated using Cohere embed-english-v3.0 and stored in Qdrant
2. **Given** a re-ingestion process, **When** it runs, **Then** no duplicates are created and outdated content is replaced safely

---

### Edge Cases

- What happens when the sitemap is malformed or contains invalid URLs?
- How does the system handle pages that return 404 or 500 errors during content extraction?
- How does the system handle extremely large documents that might exceed memory limits during processing?
- What happens when Qdrant is temporarily unavailable during storage operations?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST fetch and parse sitemap.xml from the configured URL
- **FR-002**: System MUST extract all page URLs from the sitemap and handle malformed sitemaps gracefully
- **FR-003**: System MUST download HTML content for each extracted URL
- **FR-004**: System MUST extract clean, readable text while excluding navigation, scripts, and styles
- **FR-005**: System MUST chunk text into semantically coherent pieces of ≤ 1200 characters
- **FR-006**: System MUST preserve sentence boundaries during text chunking
- **FR-007**: System MUST generate embeddings using Cohere embed-english-v3.0 with input type 'search_document'
- **FR-008**: System MUST store embeddings in Qdrant Cloud with proper metadata including URL, text, and chunk_id
- **FR-009**: System MUST use cosine distance metric when creating Qdrant collections
- **FR-010**: System MUST support safe re-ingestion without creating duplicates
- **FR-011**: System MUST replace outdated content safely during re-ingestion
- **FR-012**: System MUST log errors clearly without crashing during processing
- **FR-013**: System MUST load all configuration from environment variables as specified
- **FR-014**: System MUST support local and cloud deployment via environment configuration
- **FR-015**: System MUST ensure output is deterministic and reproducible

### Key Entities *(include if feature involves data)*

- **Content Chunk**: Represents a semantically coherent piece of text extracted from documentation, with metadata including source URL, chunk text, and unique chunk ID
- **Sitemap Entry**: Represents a URL extracted from a sitemap.xml file, including the original URL and processing status
- **Qdrant Vector**: Represents an embedding vector with associated metadata stored in Qdrant Cloud, including URL, text, and chunk_id

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of sitemap URLs ingested successfully from target sitemap
- **SC-002**: All content stored as vectorized chunks in a single Qdrant collection
- **SC-003**: Ingestion completes without errors
- **SC-004**: Progress and failures are clearly logged
- **SC-005**: Output is deterministic and reproducible
- **SC-006**: System successfully handles re-ingestion without creating duplicate content

### Constitution Alignment

- **Spec-First, AI-Driven Authoring**: This feature follows the spec-first methodology by defining clear, testable requirements before implementation, ensuring the ingestion pipeline meets exact specifications for the RAG system
- **Technical Accuracy and Clarity**: The specification clearly defines technical requirements for sitemap parsing, content extraction, and vector storage without ambiguity
- **Reproducibility and Maintainability**: The spec defines a clean, deployable backend module with no duplicate files or experimental code, ensuring reproducible results
- **No Unsupported or Speculative Content**: The specification only covers the ingestion layer as defined, without speculative features beyond the defined scope
- **Docusaurus-First Documentation Framework**: The ingestion pipeline specifically targets Docusaurus book content, ensuring optimal integration with the documentation framework
- **RAG-Powered Chatbot Integration**: This ingestion layer serves as the foundational component for the complete RAG chatbot system, enabling semantic search and answer generation
- **Free-Tier Infrastructure Compliance**: The specification accommodates free-tier infrastructure constraints by using Cohere and Qdrant free-tier services as specified
- **GitHub Pages Deployment**: The backend ingestion system is designed as a separate deployable module that doesn't interfere with GitHub Pages documentation deployment