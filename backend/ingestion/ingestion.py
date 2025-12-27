"""
Main ingestion module for RAG Content Ingestion Pipeline.

This module provides the main ingestion functionality.
"""
from .ingest import run_ingestion_pipeline

def main():
    """Main entry point for ingestion."""
    from .ingest import main as ingestion_main
    ingestion_main()

if __name__ == "__main__":
    main()