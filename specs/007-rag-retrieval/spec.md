# Specification: Semantic Retrieval from Qdrant using Cohere Embeddings

**Feature**: RAG Retrieval Layer
**Branch**: `007-rag-retrieval`
**Date**: 2025-12-25
**Author**: Unknown
**Status**: Draft

## Overview

### Purpose
Build a clean, production-ready retrieval module that accepts a natural-language user query, generates a query embedding using Cohere, performs semantic search against Qdrant, and returns the most relevant content chunks for downstream answer generation.

### Context
This spec defines ONLY the retrieval layer. It assumes that Spec-1 has already fetched content from the sitemap, generated embeddings using Cohere, and stored them in Qdrant Cloud. This layer is responsible for converting user queries into embeddings and retrieving the most relevant content chunks.

### Dependencies
- Spec-1: Sitemap-Based Content Ingestion into Qdrant
- Existing Qdrant collection created by Spec-1

## User Scenarios & Testing

### Primary User Flow
1. User submits a natural-language query to the RAG system
2. System generates an embedding for the query using Cohere
3. System performs semantic search against Qdrant collection
4. System returns the most relevant content chunks with source information
5. Downstream components use retrieved chunks for answer generation

### Edge Cases
- Query produces no relevant results in Qdrant
- Query generates invalid embedding
- Qdrant search fails due to connectivity issues
- Empty or malformed user query

## Functional Requirements

### FR-1: Query Processing
**Requirement**: The system MUST accept a user query as plain text and process it for semantic retrieval.

**Acceptance Criteria**:
- System accepts plain text queries of reasonable length (up to 1000 characters)
- System validates query format before processing
- System handles empty queries gracefully with appropriate response

### FR-2: Embedding Generation
**Requirement**: The system MUST generate query embeddings using Cohere's embed-english-v3.0 model with search_query input type.

**Acceptance Criteria**:
- Query embedding uses Cohere embed-english-v3.0 model
- Input type is set to search_query for optimal retrieval
- Generated vectors are 1024-dimensional as expected by Qdrant
- System handles embedding API failures gracefully

### FR-3: Semantic Search
**Requirement**: The system MUST perform semantic search against the existing Qdrant collection using cosine similarity.

**Acceptance Criteria**:
- Search uses cosine similarity for semantic matching
- System queries the correct Qdrant collection specified in configuration
- Search returns top-k most relevant content chunks (k=5 by default)
- System handles search failures gracefully

### FR-4: Result Formatting
**Requirement**: The system MUST return retrieved results containing chunk text and source URL.

**Acceptance Criteria**:
- Results include the text content of retrieved chunks
- Results include the source URL for each chunk
- Results are ordered by relevance score
- System handles cases where no relevant results are found

### FR-5: Configuration Management
**Requirement**: The system MUST load all required configuration from environment variables.

**Acceptance Criteria**:
- All secrets loaded from .env file without hardcoding
- Required environment variables: COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME
- System validates configuration before processing queries
- System fails gracefully if required configuration is missing

## Non-Functional Requirements

### Performance
- Query processing completes within 2 seconds under normal load
- System supports 100 concurrent queries
- 95% of queries return results within 1.5 seconds

### Security
- API keys never exposed in logs or responses
- All external API calls use secure connections
- Input validation prevents injection attacks

### Reliability
- System handles API rate limits gracefully
- Proper retry mechanisms for transient failures
- Comprehensive error logging for debugging

## Key Entities

### QueryEmbedding
- **Description**: Represents the vector representation of a user query
- **Attributes**:
  - vector: 1024-dimensional float array
  - query_text: original user query
  - model: embedding model used

### RetrievalResult
- **Description**: Represents a single retrieved content chunk
- **Attributes**:
  - text: content chunk text
  - source_url: URL where content originated
  - relevance_score: similarity score from Qdrant
  - chunk_id: unique identifier for the chunk

## Success Criteria

### Quantitative Metrics
- 95% of valid queries return results within 2 seconds
- 90% of queries return at least one relevant content chunk
- System maintains 99% uptime under normal operating conditions
- Average relevance score of returned results is above 0.5 (on cosine similarity scale)

### Qualitative Measures
- Retrieved content chunks are semantically aligned with user queries
- System handles errors gracefully without crashing
- Configuration is secure with no hardcoded secrets
- Code is maintainable and follows production-grade standards

## Assumptions

- Spec-1 ingestion pipeline has successfully populated Qdrant with content
- Qdrant collection contains properly indexed embeddings with content and URL metadata
- Cohere API is available and responsive during normal operation
- Network connectivity exists to both Cohere and Qdrant services

## Constraints

- No content ingestion or re-embedding functionality
- No vector storage or collection creation
- No OpenRouter or LLM calls
- No frontend integration
- No duplication of Spec-1 logic
- All secrets must come from environment variables

## Open Questions

[No open questions at this time - all requirements clearly specified in feature description]