"""
Search module for RAG Retrieval Layer.

This module provides search functionality.
"""
from .retrieve import retrieve_relevant_content, retrieve_with_validation
from .qdrant_client import retrieve_content_chunks, QdrantRetriever

def search_content(query: str, limit: int = 5):
    """Search for content using the retrieval system."""
    return retrieve_relevant_content(query, limit)

def main():
    """Main entry point for search functionality."""
    pass

if __name__ == "__main__":
    main()