"""
Qdrant client module for RAG Retrieval Layer.

This module handles semantic search operations in Qdrant Cloud.
"""
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any
import logging
from .config import Config


class QdrantRetriever:
    """Handles semantic search operations in Qdrant Cloud for retrieval."""

    def __init__(self):
        # Validate config before initializing
        Config.validate()

        self.client = QdrantClient(
            url=Config.QDRANT_URL,
            api_key=Config.QDRANT_API_KEY,
        )
        self.collection_name = Config.QDRANT_COLLECTION_NAME

    def search(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Perform semantic search in the Qdrant collection.

        Args:
            query_embedding: Embedding vector to search for
            limit: Number of results to return (top-k)

        Returns:
            List of matching points with payload (text and source URL)
        """
        try:
            response = self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=limit,
                with_payload=True
            )

            # The response object has a 'points' attribute containing the results
            results = response.points if hasattr(response, 'points') else response

            # Format results to include required information
            formatted_results = []
            for result in results:
                # Handle different possible result formats
                if hasattr(result, 'payload') and hasattr(result, 'score'):
                    # New API format
                    formatted_result = {
                        "text": result.payload.get("text", "") if hasattr(result.payload, 'get') else result.payload.get("text", ""),
                        "source_url": result.payload.get("url", "") if hasattr(result.payload, 'get') else result.payload.get("url", ""),
                        "relevance_score": result.score,
                        "chunk_id": result.payload.get("chunk_id", "") if hasattr(result.payload, 'get') else result.payload.get("chunk_id", ""),
                        "position": result.payload.get("position", 0) if hasattr(result.payload, 'get') else result.payload.get("position", 0),
                        "title": result.payload.get("title", "") if hasattr(result.payload, 'get') else result.payload.get("title", "")
                    }
                else:
                    # Fallback format
                    formatted_result = {
                        "text": result.payload.get("text", "") if isinstance(result.payload, dict) else "",
                        "source_url": result.payload.get("url", "") if isinstance(result.payload, dict) else "",
                        "relevance_score": getattr(result, 'score', 0),
                        "chunk_id": result.payload.get("chunk_id", "") if isinstance(result.payload, dict) else "",
                        "position": result.payload.get("position", 0) if isinstance(result.payload, dict) else 0,
                        "title": result.payload.get("title", "") if isinstance(result.payload, dict) else ""
                    }
                formatted_results.append(formatted_result)

            return formatted_results

        except Exception as e:
            logging.error(f"Error during Qdrant search: {str(e)}", exc_info=True)
            raise

    def search_with_filters(self, query_embedding: List[float], filters: Dict[str, Any],
                           limit: int = 5) -> List[Dict[str, Any]]:
        """
        Perform semantic search with additional filters.

        Args:
            query_embedding: Embedding vector to search for
            filters: Dictionary of filters to apply
            limit: Number of results to return

        Returns:
            List of matching points with payload
        """
        try:
            # Convert filters to Qdrant filter format
            filter_conditions = []
            for key, value in filters.items():
                filter_conditions.append(
                    models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value)
                    )
                )

            search_filter = models.Filter(must=filter_conditions) if filter_conditions else None

            response = self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                query_filter=search_filter,
                limit=limit,
                with_payload=True
            )

            # The response object has a 'points' attribute containing the results
            results = response.points if hasattr(response, 'points') else response

            # Format results
            formatted_results = []
            for result in results:
                # Handle different possible result formats
                if hasattr(result, 'payload') and hasattr(result, 'score'):
                    # New API format
                    formatted_result = {
                        "text": result.payload.get("text", "") if hasattr(result.payload, 'get') else result.payload.get("text", ""),
                        "source_url": result.payload.get("url", "") if hasattr(result.payload, 'get') else result.payload.get("url", ""),
                        "relevance_score": result.score,
                        "chunk_id": result.payload.get("chunk_id", "") if hasattr(result.payload, 'get') else result.payload.get("chunk_id", ""),
                        "position": result.payload.get("position", 0) if hasattr(result.payload, 'get') else result.payload.get("position", 0),
                        "title": result.payload.get("title", "") if hasattr(result.payload, 'get') else result.payload.get("title", "")
                    }
                else:
                    # Fallback format
                    formatted_result = {
                        "text": result.payload.get("text", "") if isinstance(result.payload, dict) else "",
                        "source_url": result.payload.get("url", "") if isinstance(result.payload, dict) else "",
                        "relevance_score": getattr(result, 'score', 0),
                        "chunk_id": result.payload.get("chunk_id", "") if isinstance(result.payload, dict) else "",
                        "position": result.payload.get("position", 0) if isinstance(result.payload, dict) else 0,
                        "title": result.payload.get("title", "") if isinstance(result.payload, dict) else ""
                    }
                formatted_results.append(formatted_result)

            return formatted_results

        except Exception as e:
            logging.error(f"Error during filtered Qdrant search: {str(e)}", exc_info=True)
            raise

    def get_collection_info(self):
        """Get information about the collection being searched."""
        return self.client.get_collection(self.collection_name)

    def count_points(self) -> int:
        """Get the total number of points in the collection."""
        collection_info = self.client.get_collection(self.collection_name)
        return collection_info.points_count


def retrieve_content_chunks(query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
    """
    Convenience function to retrieve content chunks from Qdrant.

    Args:
        query_embedding: Embedding vector to search for
        limit: Number of results to return

    Returns:
        List of content chunks with text and source URL
    """
    retriever = QdrantRetriever()
    return retriever.search(query_embedding, limit)