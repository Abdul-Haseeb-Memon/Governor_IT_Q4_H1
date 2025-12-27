"""
Configuration module for RAG Content Ingestion Pipeline.

This module handles environment variable loading and validation.
"""
import os
from typing import Optional
import sys
from pathlib import Path

# Add the backend directory to the path so we can load .env from there
backend_dir = Path(__file__).parent.parent
env_path = backend_dir / '.env'

# Load environment variables from .env file if it exists
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)


class Config:
    """Configuration class to manage environment variables."""

    # Cohere configuration
    COHERE_API_KEY: Optional[str] = os.getenv("COHERE_API_KEY")

    # Qdrant configuration
    QDRANT_URL: Optional[str] = os.getenv("QDRANT_URL")
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME: Optional[str] = os.getenv("QDRANT_COLLECTION_NAME")

    # Sitemap configuration
    SITEMAP_URL: Optional[str] = os.getenv("SITEMAP_URL")

    @classmethod
    def validate(cls) -> None:
        """Validate that all required environment variables are set."""
        required_vars = [
            "COHERE_API_KEY",
            "QDRANT_URL",
            "QDRANT_API_KEY",
            "QDRANT_COLLECTION_NAME",
            "SITEMAP_URL"
        ]

        missing_vars = []
        for var in required_vars:
            value = getattr(cls, var)
            if not value:
                missing_vars.append(var)

        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

    @classmethod
    def get_cohere_config(cls) -> dict:
        """Get Cohere-specific configuration."""
        return {
            "api_key": cls.COHERE_API_KEY
        }

    @classmethod
    def get_qdrant_config(cls) -> dict:
        """Get Qdrant-specific configuration."""
        return {
            "url": cls.QDRANT_URL,
            "api_key": cls.QDRANT_API_KEY,
            "collection_name": cls.QDRANT_COLLECTION_NAME
        }

    @classmethod
    def get_sitemap_config(cls) -> dict:
        """Get sitemap-specific configuration."""
        return {
            "url": cls.SITEMAP_URL
        }