"""
Utility functions for RAG Content Ingestion Pipeline.

This module contains common utility functions and error handling utilities.
"""
import logging
from typing import Any, Callable, TypeVar, Optional
from functools import wraps

T = TypeVar('T')


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    Decorator to retry a function on failure.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                        import time
                        time.sleep(delay)
                    else:
                        logging.error(f"All {max_retries} attempts failed. Last error: {e}")

            # If all retries failed, raise the last exception
            raise last_exception
        return wrapper
    return decorator


def safe_execute(func: Callable[..., T], *args, default: Optional[T] = None, **kwargs) -> Optional[T]:
    """
    Safely execute a function, returning a default value if it fails.

    Args:
        func: Function to execute
        *args: Arguments to pass to the function
        default: Default value to return if function fails
        **kwargs: Keyword arguments to pass to the function

    Returns:
        Result of the function or default value if it fails
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logging.error(f"Function {func.__name__} failed: {e}")
        return default


class IngestionError(Exception):
    """Base exception for ingestion pipeline errors."""
    pass


class SitemapError(IngestionError):
    """Exception raised for sitemap-related errors."""
    pass


class ContentExtractionError(IngestionError):
    """Exception raised for content extraction errors."""
    pass


class EmbeddingError(IngestionError):
    """Exception raised for embedding generation errors."""
    pass


class StorageError(IngestionError):
    """Exception raised for storage-related errors."""
    pass


def validate_url(url: str) -> bool:
    """
    Validate if a string is a properly formatted URL.

    Args:
        url: URL string to validate

    Returns:
        True if URL is valid, False otherwise
    """
    import re
    from urllib.parse import urlparse

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def sanitize_text(text: str) -> str:
    """
    Sanitize text by removing or replacing problematic characters.

    Args:
        text: Text to sanitize

    Returns:
        Sanitized text
    """
    if not text:
        return text

    # Replace null bytes and other problematic characters
    sanitized = text.replace('\x00', '')  # Remove null bytes
    sanitized = sanitized.replace('\r\n', '\n')  # Normalize line endings
    sanitized = sanitized.replace('\r', '\n')  # Normalize line endings

    return sanitized


def get_file_size_mb(file_path: str) -> float:
    """
    Get the size of a file in MB.

    Args:
        file_path: Path to the file

    Returns:
        Size in MB
    """
    import os
    size_bytes = os.path.getsize(file_path)
    size_mb = size_bytes / (1024 * 1024)
    return size_mb