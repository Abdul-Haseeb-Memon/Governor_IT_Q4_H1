# Data Model: RAG Content Ingestion Pipeline

## Overview
This document defines the data structures and models used in the RAG content ingestion pipeline that loads documentation content from a sitemap, embeds it using Cohere, and stores it in Qdrant Cloud.

## Core Data Structures

### 1. SitemapEntry
Represents a single URL entry extracted from a sitemap.xml file.

**Fields:**
- `url` (string): The absolute URL of the documentation page
- `last_modified` (datetime, optional): Last modification timestamp from sitemap
- `change_frequency` (string, optional): How frequently the page changes (from sitemap)
- `priority` (float, optional): Priority of the page (0.0 to 1.0, from sitemap)

**Example:**
```json
{
  "url": "https://governor-it-q4-h1.vercel.app/docs/introduction",
  "last_modified": "2025-12-25T10:30:00Z",
  "change_frequency": "weekly",
  "priority": 0.8
}
```

### 2. RawContent
Represents the raw HTML content fetched from a URL before processing.

**Fields:**
- `url` (string): The source URL
- `html_content` (string): The raw HTML content
- `status_code` (integer): HTTP status code from the response
- `fetched_at` (datetime): Timestamp when content was fetched
- `content_type` (string): Content type from HTTP response header

**Example:**
```json
{
  "url": "https://governor-it-q4-h1.vercel.app/docs/introduction",
  "status_code": 200,
  "fetched_at": "2025-12-25T10:30:00Z",
  "content_type": "text/html; charset=utf-8"
}
```

### 3. ExtractedContent
Represents the clean, readable text extracted from HTML content.

**Fields:**
- `url` (string): The source URL
- `clean_text` (string): The extracted, clean text content
- `title` (string, optional): Page title extracted from HTML
- `extracted_at` (datetime): Timestamp when content was extracted
- `word_count` (integer): Number of words in the extracted content

**Example:**
```json
{
  "url": "https://governor-it-q4-h1.vercel.app/docs/introduction",
  "title": "Introduction to Governor IT Program",
  "word_count": 1250,
  "extracted_at": "2025-12-25T10:30:15Z"
}
```

### 4. ContentChunk
Represents a semantically coherent piece of text that will be converted to an embedding.

**Fields:**
- `chunk_id` (string): Unique identifier for the chunk (URL + position)
- `url` (string): The source URL
- `text` (string): The chunk text (≤1200 characters)
- `position` (integer): Position of the chunk within the original content
- `char_count` (integer): Number of characters in the chunk
- `chunk_metadata` (object): Additional metadata about the chunk

**Example:**
```json
{
  "chunk_id": "https://governor-it-q4-h1.vercel.app/docs/introduction_0",
  "url": "https://governor-it-q4-h1.vercel.app/docs/introduction",
  "text": "The Governor IT program is designed to provide advanced training in modern technologies...",
  "position": 0,
  "char_count": 420,
  "chunk_metadata": {
    "sentence_count": 3,
    "is_complete_sentence": true
  }
}
```

### 5. EmbeddingVector
Represents the vector embedding of a content chunk.

**Fields:**
- `chunk_id` (string): Reference to the original content chunk
- `vector` (array of floats): The 1024-dimensional embedding vector
- `model` (string): The model used to generate the embedding
- `generated_at` (datetime): Timestamp when embedding was generated

**Example:**
```json
{
  "chunk_id": "https://governor-it-q4-h1.vercel.app/docs/introduction_0",
  "model": "embed-english-v3.0",
  "generated_at": "2025-12-25T10:30:30Z"
}
// Note: The actual vector array would contain 1024 float values
```

### 6. VectorPoint
Represents the data structure stored in Qdrant Cloud.

**Fields:**
- `id` (string): Unique identifier for the point in Qdrant
- `vector` (array of floats): The 1024-dimensional embedding vector
- `payload` (object): Metadata stored with the vector
  - `url` (string): Source URL
  - `text` (string): The chunk text
  - `chunk_id` (string): Original chunk identifier
  - `created_at` (datetime): When the point was created

**Example:**
```json
{
  "id": "chunk_001",
  "vector": [0.1, 0.2, 0.3, ...], // 1024-dimensional vector
  "payload": {
    "url": "https://governor-it-q4-h1.vercel.app/docs/introduction",
    "text": "The Governor IT program is designed to provide advanced training in modern technologies...",
    "chunk_id": "https://governor-it-q4-h1.vercel.app/docs/introduction_0",
    "created_at": "2025-12-25T10:30:30Z"
  }
}
```

## Processing Pipeline Data Flow

### 1. Sitemap Processing
```
Input: sitemap.xml URL
Output: List<SitemapEntry>
```

### 2. Content Fetching
```
Input: List<SitemapEntry>
Output: List<RawContent>
```

### 3. Content Extraction
```
Input: List<RawContent>
Output: List<ExtractedContent>
```

### 4. Text Chunking
```
Input: List<ExtractedContent>
Output: List<ContentChunk>
```

### 5. Embedding Generation
```
Input: List<ContentChunk>
Output: List<EmbeddingVector>
```

### 6. Vector Storage
```
Input: List<EmbeddingVector>
Output: Stored in Qdrant collection
```

## Qdrant Collection Schema

### Collection Name
- Dynamic based on `QDRANT_COLLECTION_NAME` environment variable

### Vector Configuration
- Size: 1024 (for embed-english-v3.0 model)
- Distance: Cosine

### Payload Schema
- `url` (keyword): Source URL for the content chunk
- `text` (text): The actual content text
- `chunk_id` (keyword): Unique identifier for the chunk
- `created_at` (datetime): Timestamp of creation

## Relationships

### 1. Hierarchical Relationships
- Sitemap contains multiple SitemapEntry items
- Each URL can produce one ExtractedContent
- Each ExtractedContent can produce multiple ContentChunk items

### 2. Processing Relationships
- ContentChunk is transformed into EmbeddingVector
- EmbeddingVector is stored as VectorPoint in Qdrant

## Validation Rules

### 1. ContentChunk Validation
- `text` must be ≤ 1200 characters
- `text` must not be empty
- `position` must be ≥ 0
- `chunk_id` must be unique within the system

### 2. EmbeddingVector Validation
- `vector` must have exactly 1024 dimensions
- `model` must be "embed-english-v3.0"
- `chunk_id` must reference an existing ContentChunk

### 3. SitemapEntry Validation
- `url` must be a valid absolute URL
- `priority` must be between 0.0 and 1.0 if specified
- `change_frequency` must be one of: "always", "hourly", "daily", "weekly", "monthly", "yearly", "never"

## Performance Considerations

### 1. Memory Efficiency
- Process content in batches to avoid memory overflow
- Stream processing where possible
- Clean up intermediate objects after processing

### 2. Storage Efficiency
- Compress large text fields when storing temporarily
- Use efficient data structures for intermediate processing
- Optimize for read operations in Qdrant

### 3. Network Efficiency
- Batch API calls where possible (e.g., Cohere embeddings)
- Cache frequently accessed data
- Implement appropriate retry mechanisms