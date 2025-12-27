"""
Main retrieval module for RAG Retrieval Layer.

This module orchestrates the complete retrieval workflow: query embedding -> semantic search -> result formatting.
"""
import logging
from typing import List, Dict, Any
from .embeddings import generate_query_embedding, QueryEmbeddingsGenerator
from .qdrant_client import retrieve_content_chunks, QdrantRetriever
from .config import Config


def setup_logging():
    """Set up logging configuration for the retrieval module."""
    import os
    os.makedirs('logs', exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/retrieval.log'),
            logging.StreamHandler()
        ]
    )


def retrieve_relevant_content(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Main function to retrieve relevant content chunks for a user query.

    Args:
        query: Natural language query from user
        limit: Number of top-k results to return

    Returns:
        List of retrieved content chunks with text and source URL
    """
    try:
        # Validate configuration
        Config.validate()
        logging.info("Configuration validated successfully")

        # Validate input
        if not query or not query.strip():
            logging.warning("Empty or invalid query provided")
            return []

        # Generate embedding for the query using Cohere
        logging.info(f"Generating embedding for query: {query[:100]}...")
        query_embedding = generate_query_embedding(query)
        logging.info(f"Generated embedding vector of dimension {len(query_embedding)}")

        # Perform semantic search in Qdrant
        logging.info(f"Performing semantic search in Qdrant collection")
        results = retrieve_content_chunks(query_embedding, limit)
        logging.info(f"Retrieved {len(results)} relevant content chunks")

        # Return formatted results
        return results

    except Exception as e:
        logging.error(f"Retrieval process failed: {str(e)}", exc_info=True)
        raise


def retrieve_with_validation(query: str, limit: int = 5, min_relevance_score: float = 0.3) -> List[Dict[str, Any]]:
    """
    Retrieve relevant content with validation for relevance scores.

    Args:
        query: Natural language query from user
        limit: Number of top-k results to return
        min_relevance_score: Minimum relevance score for results to be included

    Returns:
        List of retrieved content chunks with text and source URL, filtered by relevance
    """
    results = retrieve_relevant_content(query, limit)

    # Filter results based on minimum relevance score
    filtered_results = [
        result for result in results
        if result.get('relevance_score', 0) >= min_relevance_score
    ]

    logging.info(f"Filtered {len(results)} results to {len(filtered_results)} based on relevance threshold")

    if not filtered_results:
        logging.warning("No results met the minimum relevance threshold")

    return filtered_results


class ContentRetriever:
    """Main class for content retrieval operations."""

    def __init__(self):
        # Validate configuration
        Config.validate()
        self.embedding_generator = QueryEmbeddingsGenerator()
        self.qdrant_retriever = QdrantRetriever()

    def retrieve(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant content chunks for a query.

        Args:
            query: Natural language query from user
            limit: Number of top-k results to return

        Returns:
            List of retrieved content chunks with text and source URL
        """
        # Generate embedding for the query
        query_embedding = self.embedding_generator.generate_query_embedding(query)

        # Perform semantic search in Qdrant
        results = self.qdrant_retriever.search(query_embedding, limit)

        return results

    def retrieve_with_context(self, query: str, context_filters: Dict[str, Any] = None, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant content chunks with additional context filters.

        Args:
            query: Natural language query from user
            context_filters: Additional filters to apply during search
            limit: Number of top-k results to return

        Returns:
            List of retrieved content chunks with text and source URL
        """
        # Generate embedding for the query
        query_embedding = self.embedding_generator.generate_query_embedding(query)

        # Perform semantic search in Qdrant with filters
        if context_filters:
            results = self.qdrant_retriever.search_with_filters(query_embedding, context_filters, limit)
        else:
            results = self.qdrant_retriever.search(query_embedding, limit)

        return results

    def get_retrieval_stats(self) -> Dict[str, Any]:
        """Get statistics about the retrieval system."""
        collection_info = self.qdrant_retriever.get_collection_info()
        return {
            "collection_name": collection_info.config.params.vectors.get("text").size if hasattr(collection_info.config.params.vectors, "get") else "unknown",
            "total_documents": self.qdrant_retriever.count_points(),
            "collection_status": collection_info.status
        }


def main():
    """Example usage of the retrieval module."""
    setup_logging()

    # Example usage
    query = "What are the key features of the governor IT system?"
    results = retrieve_relevant_content(query)

    print(f"Query: {query}")
    print(f"Found {len(results)} relevant chunks:")
    for i, result in enumerate(results):
        print(f"{i+1}. Score: {result['relevance_score']:.3f}")
        print(f"   Source: {result['source_url']}")
        print(f"   Text: {result['text'][:200]}...")
        print()


if __name__ == "__main__":
    main()