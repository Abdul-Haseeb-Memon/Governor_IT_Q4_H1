"""
Embeddings module for RAG Content Ingestion Pipeline.

This module handles embedding generation using Cohere API.
"""
import cohere
from typing import List, Dict, Any
import logging
from .config import Config


class EmbeddingsGenerator:
    """Handles embedding generation using Cohere API."""

    def __init__(self):
        # Validate config before initializing
        Config.validate()

        self.cohere_client = cohere.Client(Config.COHERE_API_KEY)
        self.model = "embed-english-v3.0"
        self.input_type = "search_document"

    def generate_embeddings(self, texts: List[str], batch_size: int = 96) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Cohere API.

        Args:
            texts: List of texts to embed
            batch_size: Number of texts to process in each batch (max 96 for Cohere)

        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        all_embeddings = []

        # Process in batches to respect API limits
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            try:
                response = self.cohere_client.embed(
                    texts=batch,
                    model=self.model,
                    input_type=self.input_type
                )

                # Validate that we got the expected number of embeddings
                if len(response.embeddings) != len(batch):
                    raise ValueError(f"Expected {len(batch)} embeddings, got {len(response.embeddings)}")

                # Validate embedding dimensions (should be 1024 for embed-english-v3.0)
                if len(response.embeddings[0]) != 1024:
                    logging.warning(f"Unexpected embedding dimension: {len(response.embeddings[0])}, expected 1024")

                all_embeddings.extend(response.embeddings)

            except Exception as e:
                # Check if it's a Cohere-specific error
                if "CohereError" in str(type(e)) or "cohere" in str(e).lower():
                    logging.error(f"Cohere API error during embedding generation: {e}")
                else:
                    logging.error(f"Error during embedding generation: {e}")
                raise

        return all_embeddings

    def generate_embedding_for_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector as a list of floats
        """
        embeddings = self.generate_embeddings([text])
        return embeddings[0] if embeddings else []


def create_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Convenience function to create embeddings for a list of texts.

    Args:
        texts: List of texts to embed

    Returns:
        List of embedding vectors
    """
    generator = EmbeddingsGenerator()
    return generator.generate_embeddings(texts)