"""
Answer generation module for RAG Answer Generation.

This module provides answer generation functionality.
"""
from .answer_generator import generate_answer, GeneratedAnswer, AnswerGenerator

def main():
    """Main entry point for answer generation."""
    # Example usage
    query = "What are the key features?"
    context = ["The system provides comprehensive RAG functionality.", "Key features include context retrieval and answer generation."]

    if query and context:
        answer = generate_answer(query, context)
        print(f"Query: {query}")
        print(f"Answer: {answer}")
    else:
        print("Query and context required to generate answer")

if __name__ == "__main__":
    main()