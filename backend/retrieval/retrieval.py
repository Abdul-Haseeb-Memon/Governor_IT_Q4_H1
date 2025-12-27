"""
Main retrieval module for RAG Retrieval Layer.

This module provides the main retrieval functionality.
"""
from .retrieve import retrieve_relevant_content, retrieve_with_validation, ContentRetriever

def main():
    """Main entry point for retrieval."""
    from .retrieve import main as retrieval_main
    retrieval_main()

if __name__ == "__main__":
    main()