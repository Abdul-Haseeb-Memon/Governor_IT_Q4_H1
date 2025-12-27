"""
Initialization module for RAG Content Ingestion Pipeline.

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

# Set up comprehensive logging configuration
def setup_logging():
    """Set up comprehensive logging configuration."""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create file handler
    file_handler = logging.FileHandler('logs/ingestion.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Get root logger and add handlers
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


setup_logging()

# Define the package version
__version__ = "1.0.0"

# Define what should be imported when using "from ingestion import *"
__all__ = [
    'SitemapLoader',
    'TextProcessor',
    'EmbeddingsGenerator',
    'QdrantStorage',
    'Config'
]

# Optional: Import classes to make them available at package level
# This is commented out to avoid potential import issues during package initialization
# from .sitemap_loader import SitemapLoader
# from .text_processor import TextProcessor
# from .embeddings import EmbeddingsGenerator
# from .qdrant_client import QdrantStorage
# from .config import Config