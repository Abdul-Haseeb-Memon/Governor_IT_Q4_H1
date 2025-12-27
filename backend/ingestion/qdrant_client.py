"""
Qdrant client module for RAG Content Ingestion Pipeline.

This module handles storage operations in Qdrant Cloud.
"""
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any
import logging
import hashlib
from .config import Config


class QdrantStorage:
    """Handles storage operations in Qdrant Cloud."""

    def __init__(self):
        # Validate config before initializing
        Config.validate()

        self.client = QdrantClient(
            url=Config.QDRANT_URL,
            api_key=Config.QDRANT_API_KEY,
        )
        self.collection_name = Config.QDRANT_COLLECTION_NAME
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Ensure the collection exists with proper configuration."""
        try:
            # Check if collection exists and get its configuration
            collection_info = self.client.get_collection(self.collection_name)
            logging.info(f"Collection {self.collection_name} already exists")

            # Check if the vector dimensions are correct
            # Get the vector configuration
            vector_config = collection_info.config.params.vectors
            if hasattr(vector_config, 'size'):
                current_size = vector_config.size
            elif isinstance(vector_config, dict) and 'text' in vector_config:
                current_size = vector_config['text'].size
            else:
                # If we can't determine the size, assume it's wrong and recreate
                current_size = None

            # If the collection has wrong dimensions, recreate it
            if current_size != 1024:
                logging.info(f"Collection has wrong dimensions ({current_size}), recreating with 1024 dimensions")
                # Delete the existing collection
                self.client.delete_collection(self.collection_name)
                logging.info(f"Deleted existing collection {self.collection_name}")

                # Create collection with cosine distance and 1024 dimensions (for Cohere embeddings)
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=1024,  # Cohere embed-english-v3.0 produces 1024-dimensional vectors
                        distance=models.Distance.COSINE
                    )
                )
                logging.info(f"Recreated collection {self.collection_name} with 1024 dimensions and cosine distance")
            else:
                logging.info(f"Collection has correct dimensions (1024)")

        except:
            # Collection doesn't exist, create it with cosine distance and 1024 dimensions (for Cohere embeddings)
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1024,  # Cohere embed-english-v3.0 produces 1024-dimensional vectors
                    distance=models.Distance.COSINE
                )
            )
            logging.info(f"Created collection {self.collection_name} with 1024 dimensions and cosine distance")

    def _generate_content_hash(self, text: str, url: str) -> str:
        """
        Generate a hash for content to detect duplicates.

        Args:
            text: Text content
            url: URL of the content

        Returns:
            Hash string for the content
        """
        content_to_hash = f"{url}::{text}".encode('utf-8')
        return hashlib.sha256(content_to_hash).hexdigest()

    def _check_duplicate(self, content_hash: str) -> bool:
        """
        Check if content with the given hash already exists in the collection.

        Args:
            content_hash: Hash of the content to check

        Returns:
            True if duplicate exists, False otherwise
        """
        try:
            results = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="content_hash",
                            match=models.MatchValue(value=content_hash)
                        )
                    ]
                ),
                limit=1
            )
            return len(results[0]) > 0  # If any results found, it's a duplicate
        except:
            # If there's an error checking for duplicates, assume it's not a duplicate
            return False

    def store_embeddings(self, texts: List[str], embeddings: List[List[float]],
                        metadata_list: List[Dict[str, Any]], batch_size: int = 64,
                        skip_duplicates: bool = True):
        """
        Store embeddings with metadata in Qdrant.

        Args:
            texts: Original text chunks
            embeddings: Corresponding embedding vectors
            metadata_list: List of metadata dictionaries for each chunk
            batch_size: Number of points to store in each batch
            skip_duplicates: Whether to skip storing duplicate content
        """
        if len(texts) != len(embeddings) or len(texts) != len(metadata_list):
            raise ValueError("texts, embeddings, and metadata_list must have the same length")

        # Prepare points for storage
        points = []
        skipped_count = 0

        for i, (text, embedding, metadata) in enumerate(zip(texts, embeddings, metadata_list)):
            # Generate content hash for duplicate detection
            content_hash = self._generate_content_hash(text, metadata.get("url", ""))

            # Check for duplicates if enabled
            if skip_duplicates and self._check_duplicate(content_hash):
                logging.info(f"Skipping duplicate content for URL: {metadata.get('url', '')}")
                skipped_count += 1
                continue

            # Create a unique ID based on the content hash to prevent collisions
            point_id = abs(int(content_hash[:16], 16))  # Use first 16 hex chars of hash as ID

            point = models.PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "text": text,
                    "url": metadata.get("url", ""),
                    "chunk_id": metadata.get("chunk_id", ""),
                    "position": metadata.get("position", 0),
                    "title": metadata.get("title", ""),
                    "char_count": metadata.get("char_count", 0),
                    "content_hash": content_hash  # Store hash for future duplicate detection
                }
            )
            points.append(point)

        if points:
            # Store in batches to optimize performance
            for i in range(0, len(points), batch_size):
                batch = points[i:i + batch_size]
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch
                )
                logging.info(f"Stored batch {i//batch_size + 1}/{(len(points)-1)//batch_size + 1} "
                            f"({len(batch)} points) in Qdrant collection {self.collection_name}")

        logging.info(f"Skipped {skipped_count} duplicate entries during storage")

    def store_embedding(self, text: str, embedding: List[float], metadata: Dict[str, Any],
                       skip_duplicates: bool = True):
        """
        Store a single embedding with metadata in Qdrant.

        Args:
            text: Original text chunk
            embedding: Embedding vector
            metadata: Metadata dictionary for the chunk
            skip_duplicates: Whether to skip storing duplicate content
        """
        # Generate content hash for duplicate detection
        content_hash = self._generate_content_hash(text, metadata.get("url", ""))

        # Check for duplicates if enabled
        if skip_duplicates and self._check_duplicate(content_hash):
            logging.info(f"Skipping duplicate content for URL: {metadata.get('url', '')}")
            return

        # Create a unique ID based on the content hash to prevent collisions
        point_id = abs(int(content_hash[:16], 16))  # Use first 16 hex chars of hash as ID

        point = models.PointStruct(
            id=point_id,
            vector=embedding,
            payload={
                "text": text,
                "url": metadata.get("url", ""),
                "chunk_id": metadata.get("chunk_id", ""),
                "position": metadata.get("position", 0),
                "title": metadata.get("title", ""),
                "char_count": metadata.get("char_count", 0),
                "content_hash": content_hash  # Store hash for future duplicate detection
            }
        )

        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
        logging.info(f"Stored single point in Qdrant collection {self.collection_name}")

    def search(self, query_embedding: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in the collection.

        Args:
            query_embedding: Embedding vector to search for
            limit: Number of results to return

        Returns:
            List of matching points with payload
        """
        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit
        )

        # The response object has a 'points' attribute containing the results
        results = response.points if hasattr(response, 'points') else response

        return [
            {
                "text": result.payload.get("text", "") if hasattr(result.payload, 'get') else (result.payload.get("text", "") if isinstance(result.payload, dict) else ""),
                "url": result.payload.get("url", "") if hasattr(result.payload, 'get') else (result.payload.get("url", "") if isinstance(result.payload, dict) else ""),
                "score": result.score if hasattr(result, 'score') else getattr(result, 'score', 0),
                "title": result.payload.get("title", "") if hasattr(result.payload, 'get') else (result.payload.get("title", "") if isinstance(result.payload, dict) else "")
            }
            for result in results
        ]

    def delete_collection(self):
        """Delete the entire collection (use with caution)."""
        self.client.delete_collection(self.collection_name)
        logging.info(f"Deleted collection {self.collection_name}")

    def get_collection_info(self):
        """Get information about the collection."""
        return self.client.get_collection(self.collection_name)

    def get_content_by_url(self, url: str) -> List[Dict[str, Any]]:
        """
        Retrieve all content chunks for a specific URL.

        Args:
            url: URL to search for

        Returns:
            List of content chunks for the URL
        """
        results = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="url",
                        match=models.MatchValue(value=url)
                    )
                ]
            )
        )
        return [point.payload for point in results[0]]

    def delete_content_by_url(self, url: str):
        """
        Delete all content chunks for a specific URL.

        Args:
            url: URL whose content should be deleted
        """
        points = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="url",
                        match=models.MatchValue(value=url)
                    )
                ]
            ),
            with_payload=False,
            with_vectors=False
        )

        point_ids = [point.id for point in points[0]]

        if point_ids:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(points=point_ids)
            )
            logging.info(f"Deleted {len(point_ids)} points for URL: {url}")


def store_content_chunks(texts: List[str], embeddings: List[List[float]],
                        metadata_list: List[Dict[str, Any]], skip_duplicates: bool = True) -> None:
    """
    Convenience function to store content chunks in Qdrant.

    Args:
        texts: Original text chunks
        embeddings: Corresponding embedding vectors
        metadata_list: List of metadata dictionaries for each chunk
        skip_duplicates: Whether to skip storing duplicate content
    """
    storage = QdrantStorage()
    storage.store_embeddings(texts, embeddings, metadata_list, skip_duplicates=skip_duplicates)