"""
Main generation module for RAG Answer Generation.

This module provides the main answer generation functionality.
"""
from .answer_generator import generate_answer, GeneratedAnswer

def main():
    """Main entry point for answer generation."""
    import argparse
    parser = argparse.ArgumentParser(description='RAG Answer Generation')
    parser.add_argument('--query', type=str, help='Query to answer')
    parser.add_argument('--context', nargs='+', help='Context chunks for answering')

    args = parser.parse_args()

    if args.query:
        if args.context:
            answer = generate_answer(args.query, args.context)
            print(f"Answer: {answer}")
        else:
            print("Context required to generate answer")
    else:
        print("Query required to generate answer")

if __name__ == "__main__":
    main()