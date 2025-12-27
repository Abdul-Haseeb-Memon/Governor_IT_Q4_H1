# Quickstart: RAG Retrieval Layer

**Feature**: RAG Retrieval Layer
**Date**: 2025-12-25

## Prerequisites

- Python 3.11+
- Cohere API access
- Qdrant Cloud account
- Content already ingested by Spec-1 (Sitemap-Based Content Ingestion)
- `.env` file with required environment variables in backend directory

## Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install dependencies
```bash
cd backend/retrieval
pip install -r requirements.txt
```

### 3. Configure environment variables
Ensure your backend/.env file contains:
```env
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=book_content_chunks
```

### 4. Verify configuration
```bash
python -c "from retrieval.config import Config; Config.validate(); print('Configuration validated successfully')"
```

## Usage

### Basic Retrieval
```python
from retrieval.retrieve import retrieve_relevant_content

# Simple query retrieval
query = "What are the key features?"
results = retrieve_relevant_content(query, limit=5)

for result in results:
    print(f"Score: {result['relevance_score']:.3f}")
    print(f"Source: {result['source_url']}")
    print(f"Text: {result['text'][:200]}...")
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

# Initialize the retriever
retriever = ContentRetriever()

# Retrieve content
results = retriever.retrieve("Your query here", limit=5)

# Get retrieval statistics
stats = retriever.get_retrieval_stats()
print(f"Total documents in collection: {stats['total_documents']}")
```

## Configuration

### Environment Variables
- `COHERE_API_KEY`: Cohere API key for embedding generation
- `QDRANT_URL`: Qdrant Cloud cluster URL
- `QDRANT_API_KEY`: Qdrant API key
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection containing ingested content

### Parameters
- `limit`: Number of results to return (default: 5)
- `min_relevance_score`: Minimum score threshold for results (default: 0.3)

## Testing the Setup

### 1. Test embedding generation
```python
from retrieval.embeddings import generate_query_embedding

query = "Test query"
embedding = generate_query_embedding(query)
print(f"Generated embedding with {len(embedding)} dimensions")
```

### 2. Test Qdrant connection
```python
from retrieval.qdrant_client import QdrantRetriever

retriever = QdrantRetriever()
stats = retriever.get_collection_info()
print(f"Connected to collection: {stats.config.params.vectors_count}")
```

### 3. End-to-end test
```python
from retrieval.retrieve import retrieve_relevant_content

results = retrieve_relevant_content("test query", limit=3)
print(f"Retrieved {len(results)} results")
```

## Troubleshooting

### Common Issues

**Issue**: "Missing required environment variables"
**Solution**: Verify your .env file contains all required variables

**Issue**: "Cohere API error during query embedding generation"
**Solution**: Check your COHERE_API_KEY and ensure your account has sufficient credits

**Issue**: "Error during Qdrant search"
**Solution**: Verify QDRANT_URL, QDRANT_API_KEY, and QDRANT_COLLECTION_NAME are correct

### Logging
Enable debug logging to see detailed information:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Next Steps

1. Integrate with your RAG application
2. Connect to the answer generation module (Spec-3)
3. Add to your frontend application (Spec-4)
4. Monitor performance and relevance scores