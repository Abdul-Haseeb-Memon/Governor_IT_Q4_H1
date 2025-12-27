# RAG Retrieval Layer

This module implements a production-ready retrieval layer for a Retrieval-Augmented Generation (RAG) system. It accepts natural-language queries, generates embeddings using Cohere, performs semantic search against Qdrant, and returns the most relevant content chunks.

## Overview

The retrieval layer is responsible for:
- Converting user queries into embeddings using Cohere
- Performing semantic search against pre-indexed content in Qdrant
- Returning the most relevant content chunks with source information
- Handling errors gracefully and providing meaningful responses

## Architecture

```
backend/
└── retrieval/
    ├── retrieve.py          # Main retrieval orchestration
    ├── embeddings.py        # Query embedding generation
    ├── qdrant_client.py     # Qdrant search operations
    ├── config.py            # Configuration management
    └── README.md            # This file
```

## Prerequisites

- Python 3.11+
- Cohere API access
- Qdrant Cloud account
- Content already ingested by Spec-1 (Sitemap-Based Content Ingestion)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure the `.env` file in the backend directory contains required environment variables:
   ```env
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_URL=your_qdrant_cluster_url
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_COLLECTION_NAME=book_content_chunks
   ```

## Usage

### Basic Usage

```python
from retrieval.retrieve import retrieve_relevant_content

# Retrieve relevant content for a query
query = "What are the key features?"
results = retrieve_relevant_content(query, limit=5)

for result in results:
    print(f"Score: {result['relevance_score']}")
    print(f"Source: {result['source_url']}")
    print(f"Text: {result['text']}")
    print("---")
```

### Advanced Usage with Validation

```python
from retrieval.retrieve import retrieve_with_validation

# Retrieve with minimum relevance threshold
results = retrieve_with_validation(
    query="Your query here",
    limit=5,
    min_relevance_score=0.3
)
```

### Using the ContentRetriever Class

```python
from retrieval.retrieve import ContentRetriever

retriever = ContentRetriever()
results = retriever.retrieve("Your query here", limit=5)
```

## Features

- **Semantic Search**: Uses cosine similarity for semantic matching
- **Query Embeddings**: Generates embeddings using Cohere's embed-english-v3.0 model with search_query input type
- **Result Formatting**: Returns content chunks with text, source URL, and relevance scores
- **Error Handling**: Comprehensive error handling and logging
- **Configuration**: Secure configuration loading from environment variables
- **Validation**: Input validation and minimum relevance scoring

## Configuration

The system requires the following environment variables:

- `COHERE_API_KEY`: Cohere API key for embedding generation
- `QDRANT_URL`: Qdrant Cloud cluster URL
- `QDRANT_API_KEY`: Qdrant API key
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection containing ingested content

## Dependencies

- `cohere`: For embedding generation
- `qdrant-client`: For vector search operations
- `python-dotenv`: For environment configuration
- `requests`: For HTTP requests

## Quality Assurance

- Production-grade error handling
- Comprehensive logging
- Input validation
- Secure configuration management
- Proper separation of concerns