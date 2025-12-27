"""
Initialization module for RAG Retrieval Layer.

This module sets up the package-level configuration and utilities.
"""
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in backend directory if it exists
backend_dir = Path(__file__).parent.parent
env_path = backend_dir / '.env'

if env_path.exists():
    load_dotenv(env_path)

# Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Define the package version
__version__ = "1.0.0"

# Define what should be imported when using "from retrieval import *"
__all__ = [
    'ContentRetriever',
    'QueryEmbeddingsGenerator',
    'QdrantRetriever',
    'Config'
]

# Optional: Import classes to make them available at package level
# This is commented out to avoid potential import issues during package initialization
# from .retrieve import ContentRetriever
# from .embeddings import QueryEmbeddingsGenerator
# from .qdrant_client import QdrantRetriever
# from .config import Config