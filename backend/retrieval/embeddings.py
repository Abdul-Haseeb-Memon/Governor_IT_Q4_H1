"""
Embeddings module for RAG Retrieval Layer.

This module handles query embedding generation using Cohere API.
"""
import cohere
from typing import List
import logging
from .config import Config


class QueryEmbeddingsGenerator:
    """Handles query embedding generation using Cohere API for retrieval."""

    def __init__(self):
        # Validate config before initializing
        Config.validate()

        # Use Cohere with the correct input type for search queries
        self.cohere_client = cohere.Client(Config.COHERE_API_KEY)
        self.model = "embed-english-v3.0"
        self.input_type = "search_query"  # Specifically for search queries as required

    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a query using Cohere API with search_query input type.

        Args:
            query: User query text to embed

        Returns:
            Embedding vector as a list of floats (1024-dimensional)

        Raises:
            Exception: If embedding generation fails
        """
        try:
            response = self.cohere_client.embed(
                texts=[query],
                model=self.model,
                input_type=self.input_type
            )

            # Validate that we got the expected embedding
            if len(response.embeddings) != 1:
                raise ValueError(f"Expected 1 embedding, got {len(response.embeddings)}")

            # Validate embedding dimensions (should be 1024 for embed-english-v3.0)
            embedding = response.embeddings[0]
            if len(embedding) != 1024:
                logging.warning(f"Unexpected embedding dimension: {len(embedding)}, expected 1024")

            return embedding

        except Exception as e:
            # Check if it's a Cohere-specific error
            if "CohereError" in str(type(e)) or "cohere" in str(e).lower():
                logging.error(f"Cohere API error during query embedding generation: {e}")
            else:
                logging.error(f"Error during query embedding generation: {e}")
            raise

    def generate_embeddings_batch(self, queries: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of queries.

        Args:
            queries: List of query texts to embed

        Returns:
            List of embedding vectors
        """
        all_embeddings = []

        # Cohere has a limit on batch size, so we'll process in chunks if needed
        batch_size = 96  # Max batch size for Cohere
        for i in range(0, len(queries), batch_size):
            batch = queries[i:i + batch_size]
            try:
                response = self.cohere_client.embed(
                    texts=batch,
                    model=self.model,
                    input_type=self.input_type
                )

                # Validate the number of embeddings
                if len(response.embeddings) != len(batch):
                    raise ValueError(f"Expected {len(batch)} embeddings, got {len(response.embeddings)}")

                all_embeddings.extend(response.embeddings)

            except cohere.CohereError as e:
                logging.error(f"Cohere API error during batch embedding generation: {e}")
                raise
            except Exception as e:
                logging.error(f"Unexpected error during batch embedding generation: {e}")
                raise

        return all_embeddings


def generate_query_embedding(query: str) -> List[float]:
    """
    Convenience function to generate embedding for a single query.

    Args:
        query: User query text to embed

    Returns:
        Embedding vector as a list of floats
    """
    generator = QueryEmbeddingsGenerator()
    return generator.generate_query_embedding(query)


