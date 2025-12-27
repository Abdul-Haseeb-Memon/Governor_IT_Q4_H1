"""
Main entry point for RAG Answer Generation.

This module serves as the main entry point for the answer generation system.
"""
import argparse
from .answer_generator import generate_answer

def main():
    """Main entry point for answer generation."""
    parser = argparse.ArgumentParser(description='RAG Answer Generation System')
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