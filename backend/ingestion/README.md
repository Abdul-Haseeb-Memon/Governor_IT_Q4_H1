# RAG Content Ingestion Pipeline

This module implements a production-ready ingestion pipeline that loads documentation content from a sitemap, embeds it using Cohere, and stores it in Qdrant Cloud for RAG usage.

## Overview

The ingestion pipeline performs the following steps:
1. Fetches documentation URLs from a sitemap.xml
2. Extracts clean textual content from each page
3. Chunks content into semantically coherent pieces (≤1200 characters)
4. Generates embeddings using Cohere `embed-english-v3.0`
5. Stores embeddings in Qdrant Cloud with proper metadata

## Architecture

```
backend/
└── ingestion/
    ├── ingest.py                 # Main ingestion entry point
    ├── embeddings.py            # Cohere embedding generation
    ├── qdrant_client.py         # Qdrant storage operations
    ├── sitemap_loader.py        # Sitemap parsing and URL extraction
    ├── text_processor.py        # Content extraction and chunking
    ├── config.py                # Environment configuration
    ├── __init__.py
    └── README.md                # This file
```

## Prerequisites

- Python 3.11+
- Cohere API access
- Qdrant Cloud account

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with required environment variables:
   ```env
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_URL=your_qdrant_cluster_url
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_COLLECTION_NAME=book_content_chunks
   SITEMAP_URL=https://governor-it-q4-h1.vercel.app/sitemap.xml
   ```

## Usage

Run the complete ingestion pipeline:
```bash
python ingest.py
```

## Configuration

All configuration is loaded from environment variables:

- `COHERE_API_KEY`: Cohere API key for embedding generation
- `QDRANT_URL`: Qdrant Cloud cluster URL
- `QDRANT_API_KEY`: Qdrant API key
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection
- `SITEMAP_URL`: URL of the sitemap.xml to process

## Features

- **Idempotent**: Safe to run multiple times without creating duplicates
- **Resilient**: Handles network errors and malformed content gracefully
- **Efficient**: Batches operations for optimal API usage
- **Monitored**: Comprehensive logging for debugging and monitoring

## Dependencies

- `requests`: HTTP requests
- `beautifulsoup4`: HTML parsing
- `lxml`: XML parsing
- `cohere`: Embedding generation
- `qdrant-client`: Vector storage
- `python-dotenv`: Environment configuration

## Quality Assurance

- Production-grade error handling
- Comprehensive logging
- Memory-efficient processing
- Safe re-ingestion without duplicates