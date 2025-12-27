"""
Command-line interface for testing answer generation

This module provides a CLI for testing the RAG answer generation functionality.
"""
import argparse
import sys
import os
import logging
from typing import List

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from answer_generator import generate_answer, AnswerGenerator
from config import load_config


def setup_logging(verbose: bool = False):
    """Set up logging for the CLI"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main():
    parser = argparse.ArgumentParser(
        description='RAG Answer Generation CLI - Generate answers using OpenRouter API'
    )
    parser.add_argument(
        '--query',
        type=str,
        required=True,
        help='The query to generate an answer for'
    )
    parser.add_argument(
        '--context',
        type=str,
        nargs='+',
        help='Context chunks to use for answer generation'
    )
    parser.add_argument(
        '--context-file',
        type=str,
        help='Path to a file containing context (one chunk per line, or entire content as single chunk)'
    )
    parser.add_argument(
        '--source',
        type=str,
        nargs='*',
        help='Source URLs for the context chunks'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--model',
        type=str,
        help='Override the model specified in config'
    )

    args = parser.parse_args()
    setup_logging(args.verbose)

    logger = logging.getLogger(__name__)
    logger.info("Starting RAG Answer Generation CLI")

    try:
        # Load configuration
        config = load_config()
        if args.model:
            config.OPENROUTER_MODEL = args.model
            logger.info(f"Using model override: {args.model}")

        logger.info(f"Using model: {config.OPENROUTER_MODEL}")

        # Prepare context
        context_chunks: List[str] = []

        if args.context:
            context_chunks.extend(args.context)

        if args.context_file:
            if not os.path.exists(args.context_file):
                raise FileNotFoundError(f"Context file not found: {args.context_file}")

            with open(args.context_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    context_chunks.append(content)

        if not context_chunks:
            logger.warning("No context provided - answers will be generated without context")

        # Prepare sources
        sources = args.source or []

        # Initialize the answer generator
        generator = AnswerGenerator()

        logger.info(f"Generating answer for query: '{args.query}'")
        logger.info(f"Number of context chunks: {len(context_chunks)}")
        if sources:
            logger.info(f"Sources: {sources}")

        # Generate the answer
        answer = generator.generate_with_progress_tracking(
            query=args.query,
            context_chunks=context_chunks,
            sources=sources
        )

        # Print the results
        print("\n" + "="*60)
        print("ANSWER GENERATION RESULTS")
        print("="*60)
        print(f"Query: {args.query}")
        print(f"Answer: {answer.answer_text}")
        print(f"Confidence Score: {answer.confidence_score:.2f}")
        print(f"Hallucination Detected: {answer.hallucination_detected}")
        if answer.source_citations:
            print(f"Source Citations: {answer.source_citations}")
        print("="*60)

        # Log performance metrics if available
        logger.info(f"Answer generated successfully: {len(answer.answer_text)} characters")

    except Exception as e:
        logger.error(f"Error during answer generation: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()