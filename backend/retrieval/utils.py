"""
Utility functions for RAG Retrieval Layer.

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


class RetrievalError(Exception):
    """Base exception for retrieval pipeline errors."""
    pass


class EmbeddingError(RetrievalError):
    """Exception raised for embedding generation errors."""
    pass


class SearchError(RetrievalError):
    """Exception raised for search-related errors."""
    pass


def validate_query(query: str) -> bool:
    """
    Validate if a query string is appropriate for processing.

    Args:
        query: Query string to validate

    Returns:
        True if query is valid, False otherwise
    """
    if not query or not query.strip():
        return False

    # Check length constraints
    if len(query.strip()) < 1 or len(query.strip()) > 1000:
        return False

    return True


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


def calculate_similarity_score(vector1: list, vector2: list) -> float:
    """
    Calculate cosine similarity between two vectors.

    Args:
        vector1: First vector
        vector2: Second vector

    Returns:
        Cosine similarity score between -1 and 1
    """
    # This is a simplified implementation - in production, use numpy or scipy
    try:
        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(vector1, vector2))

        # Calculate magnitudes
        magnitude1 = sum(a * a for a in vector1) ** 0.5
        magnitude2 = sum(b * b for b in vector2) ** 0.5

        # Calculate cosine similarity
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        similarity = dot_product / (magnitude1 * magnitude2)
        return similarity
    except Exception:
        # If calculation fails, return 0
        return 0.0