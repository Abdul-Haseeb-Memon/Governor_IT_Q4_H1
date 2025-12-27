"""
Main entry point for RAG Content Ingestion Pipeline.

This module serves as the main entry point for the ingestion system.
"""
from .ingest import main as ingestion_main

if __name__ == "__main__":
    ingestion_main()