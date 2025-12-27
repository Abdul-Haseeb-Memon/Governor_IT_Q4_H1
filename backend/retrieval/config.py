"""
Configuration module for RAG Retrieval Layer.

This module handles environment variable loading and validation for the retrieval system.
"""
import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from .env file in backend directory if it exists
backend_dir = Path(__file__).parent.parent
env_path = backend_dir / '.env'

if env_path.exists():
    load_dotenv(env_path)


class Config:
    """Configuration class to manage environment variables for retrieval."""

    # Cohere configuration
    COHERE_API_KEY: Optional[str] = os.getenv("COHERE_API_KEY")

    # Qdrant configuration
    QDRANT_URL: Optional[str] = os.getenv("QDRANT_URL")
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME: Optional[str] = os.getenv("QDRANT_COLLECTION_NAME")

    @classmethod
    def validate(cls) -> None:
        """Validate that all required environment variables are set."""
        required_vars = [
            "COHERE_API_KEY",
            "QDRANT_URL",
            "QDRANT_API_KEY",
            "QDRANT_COLLECTION_NAME"
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