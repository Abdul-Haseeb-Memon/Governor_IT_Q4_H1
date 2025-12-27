# Data Model: RAG Retrieval Layer

**Feature**: RAG Retrieval Layer
**Date**: 2025-12-25

## Core Entities

### QueryEmbedding
**Description**: Represents the vector representation of a user query

**Fields**:
- `vector`: List[float] (1024-dimensional)
  - **Type**: Array of floats
  - **Required**: Yes
  - **Validation**: Must have exactly 1024 elements
  - **Description**: The embedding vector representation of the query

- `query_text`: str
  - **Type**: String
  - **Required**: Yes
  - **Validation**: Must not be empty
  - **Description**: The original user query text

- `model`: str
  - **Type**: String
  - **Required**: Yes
  - **Default**: "embed-english-v3.0"
  - **Description**: The embedding model used

### RetrievalResult
**Description**: Represents a single retrieved content chunk with metadata

**Fields**:
- `text`: str
  - **Type**: String
  - **Required**: Yes
  - **Validation**: Must not be empty
  - **Description**: The content chunk text

- `source_url`: str
  - **Type**: String
  - **Required**: Yes
  - **Validation**: Must be a valid URL format
  - **Description**: The URL where the content originated

- `relevance_score`: float
  - **Type**: Float
  - **Required**: Yes
  - **Range**: 0.0 to 1.0 (cosine similarity)
  - **Description**: The similarity score from Qdrant search

- `chunk_id`: str
  - **Type**: String
  - **Required**: Yes
  - **Description**: Unique identifier for the content chunk

- `position`: int
  - **Type**: Integer
  - **Required**: Yes
  - **Default**: 0
  - **Description**: Position of the chunk in the original document

- `title`: str
  - **Type**: String
  - **Required**: No
  - **Default**: ""
  - **Description**: Title of the source document

## Data Flow

### Query Processing Flow
1. **Input**: User query (str)
2. **Processing**: Query embedding generation
3. **Vector**: QueryEmbedding with 1024-dimensional vector
4. **Search**: Vector search in Qdrant
5. **Output**: List[RetrievalResult]

### Data Validation Rules
- Query text must be between 1 and 1000 characters
- Query embedding vector must have exactly 1024 dimensions
- Retrieved results must include text and source_url
- Relevance score must be between 0.0 and 1.0
- Source URL must be a valid URL format

## API Contracts

### Function: generate_query_embedding(query: str) -> QueryEmbedding
**Input**:
- query: Natural language query text (1-1000 characters)

**Output**:
- QueryEmbedding object with vector, query_text, and model fields

**Errors**:
- ValueError if query is invalid
- Exception if Cohere API call fails

### Function: retrieve_content_chunks(query_embedding: List[float], limit: int = 5) -> List[RetrievalResult]
**Input**:
- query_embedding: 1024-dimensional vector
- limit: Number of results to return (default: 5)

**Output**:
- List of RetrievalResult objects

**Errors**:
- Exception if Qdrant search fails
- Returns empty list if no results found

## Integration with Spec-1 Data Model

The retrieval layer expects the following fields in the Qdrant collection from Spec-1:

- `text`: Content chunk text
- `url`: Source URL
- `chunk_id`: Unique chunk identifier
- `position`: Position in original document
- `title`: Document title
- `content_hash`: For duplicate detection (optional)

This ensures seamless integration with the existing ingestion pipeline.