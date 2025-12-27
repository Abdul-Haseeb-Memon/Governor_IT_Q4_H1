"""
Prompt Constructor Module for RAG Answer Generation

This module handles the construction of prompts that combine user queries
with retrieved context, ensuring proper grounding instructions to prevent
hallucination in the generated answers.
"""
import logging
from typing import List, Optional
from .config import Config


logger = logging.getLogger(__name__)


def construct_prompt(query: str, context_chunks: List[str], max_context_length: Optional[int] = None) -> str:
    """
    Construct a prompt that combines query and context with grounding instructions

    Args:
        query: User query text
        context_chunks: List of context chunk strings
        max_context_length: Optional maximum length for context (truncate if needed)

    Returns:
        Formatted prompt string ready for LLM
    """
    if not query or len(query.strip()) == 0:
        raise ValueError("Query cannot be empty")

    if not context_chunks:
        logger.warning("No context provided for prompt construction")
        return _create_prompt_without_context(query)

    # Filter out empty context chunks
    filtered_context = [chunk for chunk in context_chunks if chunk and chunk.strip()]

    if not filtered_context:
        logger.warning("No valid context chunks provided for prompt construction")
        return _create_prompt_without_context(query)

    # Join context chunks
    context_text = "\n".join(filtered_context)

    # Truncate context if needed
    if max_context_length and len(context_text) > max_context_length:
        logger.info(f"Truncating context from {len(context_text)} to {max_context_length} characters")
        context_text = context_text[:max_context_length]
        # Ensure we don't cut in the middle of a word
        if max_context_length < len(context_text):
            # Find the last space to avoid cutting words
            last_space = context_text.rfind(' ')
            if last_space > 0:
                context_text = context_text[:last_space]

    # Construct the prompt with grounding instructions
    prompt = f"""Context:
{context_text}

Question: {query}

Instructions: Answer the question using ONLY the provided context. Do not use any prior knowledge or information not present in the context. If the context does not contain sufficient information to answer the question, respond with "I cannot answer this question based on the provided context." Ensure your answer is directly supported by the information in the context section above."""

    return prompt


def _create_prompt_without_context(query: str) -> str:
    """
    Create a prompt when no context is available

    Args:
        query: User query text

    Returns:
        Formatted prompt string for no-context scenario
    """
    return f"""Question: {query}

Instructions: The context needed to answer this question is not available. Respond with "I cannot answer this question based on the provided context." Do not attempt to answer using any prior knowledge."""


def validate_context(context_chunks: List[str]) -> bool:
    """
    Validate if context is sufficient for answering

    Args:
        context_chunks: List of context chunk strings

    Returns:
        Boolean indicating if context is sufficient for answering
    """
    if not context_chunks:
        return False

    # Check if there's at least one non-empty context chunk
    for chunk in context_chunks:
        if chunk and chunk.strip():
            # Check if chunk has some meaningful content (at least 5 characters)
            if len(chunk.strip()) >= 5:
                return True

    return False


def construct_prompt_with_length_management(
    query: str,
    context_chunks: List[str],
    max_total_length: int = 3000
) -> str:
    """
    Construct a prompt with intelligent length management

    Args:
        query: User query text
        context_chunks: List of context chunk strings
        max_total_length: Maximum total length for the prompt

    Returns:
        Formatted prompt string within length limits
    """
    if not query or len(query.strip()) == 0:
        raise ValueError("Query cannot be empty")

    if not context_chunks:
        return _create_prompt_without_context(query)

    # Start with the query and instructions template
    base_prompt = f"""Question: {query}

Instructions: Answer the question using ONLY the provided context. Do not use any prior knowledge or information not present in the context. If the context does not contain sufficient information to answer the question, respond with "I cannot answer this question based on the provided context." Ensure your answer is directly supported by the information in the context section above.

Context:
"""

    # Calculate remaining space for context
    remaining_length = max_total_length - len(base_prompt) - 500  # Reserve 500 chars for answer

    if remaining_length <= 0:
        logger.warning("Insufficient space for context in prompt")
        return _create_prompt_without_context(query)

    # Add context chunks up to the limit
    selected_context = []
    current_length = 0

    for chunk in context_chunks:
        if not chunk or not chunk.strip():
            continue

        chunk_length = len(chunk) + 1  # +1 for newline
        if current_length + chunk_length <= remaining_length:
            selected_context.append(chunk)
            current_length += chunk_length
        else:
            # Add as much of this chunk as possible
            remaining_space = remaining_length - current_length
            if remaining_space > 100:  # Only add if there's meaningful space
                truncated_chunk = chunk[:remaining_space].rsplit(' ', 1)[0]  # Avoid cutting words
                selected_context.append(truncated_chunk)
                break

    if not selected_context:
        logger.warning("No context could fit within length constraints")
        return _create_prompt_without_context(query)

    # Build final prompt
    context_text = "\n".join(selected_context)
    final_prompt = f"""Context:
{context_text}

Question: {query}

Instructions: Answer the question using ONLY the provided context. Do not use any prior knowledge or information not present in the context. If the context does not contain sufficient information to answer the question, respond with "I cannot answer this question based on the provided context." Ensure your answer is directly supported by the information in the context section above."""

    return final_prompt


def validate_prompt_format(prompt: str) -> bool:
    """
    Validate if the prompt format meets requirements

    Args:
        prompt: The constructed prompt string

    Returns:
        Boolean indicating if prompt format is valid
    """
    if not prompt or len(prompt.strip()) == 0:
        return False

    # Check if prompt contains required sections
    has_context = "Context:" in prompt
    has_question = "Question:" in prompt
    has_instructions = "Instructions:" in prompt

    return has_context and has_question and has_instructions


# Example usage and testing
if __name__ == "__main__":
    # Example usage
    query = "What are the key features?"
    context_chunks = [
        "The system provides comprehensive RAG functionality.",
        "Key features include context retrieval and answer generation.",
        "The system ensures answers are grounded in provided context."
    ]

    prompt = construct_prompt(query, context_chunks)
    print("Constructed prompt:")
    print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
    print(f"\nPrompt length: {len(prompt)} characters")

    # Test with length management
    long_context = ["This is a sample context chunk. " * 100]  # Create a long context
    managed_prompt = construct_prompt_with_length_management(query, long_context, max_total_length=1000)
    print(f"\nManaged prompt length: {len(managed_prompt)} characters")

    # Validate prompt format
    is_valid = validate_prompt_format(prompt)
    print(f"\nPrompt format is valid: {is_valid}")