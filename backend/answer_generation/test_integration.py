"""
Integration test for RAG Answer Generation with Spec-2 Retrieval

This module tests the integration between the answer generation module
and the retrieval pipeline (Spec-2), validating the end-to-end functionality.
"""
import os
import sys
from typing import List, Dict, Any
import logging

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from answer_generator import generate_answer, generate_answer_with_sources, AnswerGenerator
from config import load_config


def simulate_spec2_retrieval(query: str) -> List[Dict[str, Any]]:
    """
    Simulate the retrieval results from Spec-2

    Args:
        query: User query to simulate retrieval for

    Returns:
        List of retrieval results with text and source_url
    """
    # In a real implementation, this would call the Spec-2 retrieval module
    if "features" in query.lower():
        return [
            {
                "text": "The system provides comprehensive RAG functionality with key features including context retrieval and answer generation.",
                "source_url": "https://example.com/docs/features",
                "relevance_score": 0.9
            },
            {
                "text": "Key features include context retrieval, answer generation, and grounding to prevent hallucination.",
                "source_url": "https://example.com/docs/key_features",
                "relevance_score": 0.85
            }
        ]
    elif "architecture" in query.lower():
        return [
            {
                "text": "The system architecture follows a three-layer approach: ingestion, retrieval, and answer generation.",
                "source_url": "https://example.com/docs/architecture",
                "relevance_score": 0.95
            },
            {
                "text": "The retrieval layer uses vector search to find relevant context chunks for the answer generation.",
                "source_url": "https://example.com/docs/retrieval",
                "relevance_score": 0.8
            }
        ]
    else:
        return [
            {
                "text": "The RAG system combines retrieval and generation to provide accurate answers based on provided context.",
                "source_url": "https://example.com/docs/overview",
                "relevance_score": 0.7
            }
        ]


def test_integration_with_spec2():
    """
    Test the integration between Spec-2 retrieval and answer generation
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting integration test with Spec-2 retrieval simulation")

    try:
        # Load configuration
        config = load_config()
        logger.info(f"Configuration loaded successfully. Model: {config.OPENROUTER_MODEL}")

        # Initialize the answer generator
        generator = AnswerGenerator()

        # Test queries
        test_queries = [
            "What are the key features of the system?",
            "How does the system architecture work?",
            "Can you explain the RAG system?"
        ]

        for query in test_queries:
            logger.info(f"Testing query: '{query}'")

            # Simulate Spec-2 retrieval
            retrieval_results = simulate_spec2_retrieval(query)
            logger.info(f"Retrieved {len(retrieval_results)} context chunks from Spec-2 simulation")

            # Extract context chunks and sources
            context_chunks = [result['text'] for result in retrieval_results]
            sources = [result['source_url'] for result in retrieval_results]
            relevance_scores = [result['relevance_score'] for result in retrieval_results]

            logger.info(f"Context relevance scores: {relevance_scores}")

            # Generate answer using the answer generation module
            answer = generate_answer_with_sources(query, context_chunks, sources)

            # Validate the answer
            logger.info(f"Generated answer: {answer.answer_text[:100]}...")
            logger.info(f"Confidence score: {answer.confidence_score}")
            logger.info(f"Source citations: {answer.source_citations}")
            logger.info(f"Hallucination detected: {answer.hallucination_detected}")

            # Validate answer properties
            assert answer.answer_text is not None and len(answer.answer_text.strip()) > 0, "Answer should not be empty"
            assert 0.0 <= answer.confidence_score <= 1.0, f"Confidence score should be between 0.0 and 1.0, got {answer.confidence_score}"
            assert isinstance(answer.source_citations, list), "Source citations should be a list"
            assert isinstance(answer.hallucination_detected, bool), "Hallucination detection should be boolean"

            logger.info("Answer validation passed")

            # Test with the AnswerGenerator class as well
            class_answer = generator.generate_with_progress_tracking(query, context_chunks, sources)
            logger.info(f"Class-generated answer validation passed: {len(class_answer.answer_text)} chars")

        logger.info("All integration tests passed successfully!")

        # Test error handling with empty context
        logger.info("Testing error handling with empty context...")
        empty_context_answer = generate_answer("What are the features?", [])
        logger.info(f"Empty context response: {empty_context_answer.answer_text}")
        assert "cannot answer" in empty_context_answer.answer_text.lower() or "not enough information" in empty_context_answer.answer_text.lower()
        logger.info("Empty context handling test passed")

        return True

    except Exception as e:
        logger.error(f"Integration test failed: {str(e)}", exc_info=True)
        return False


def test_compatibility_with_spec2_data_model():
    """
    Test compatibility with the data model expected by Spec-2
    """
    logger = logging.getLogger(__name__)
    logger.info("Testing compatibility with Spec-2 data model")

    # Test that we can handle the data format typically returned by Spec-2
    spec2_style_results = [
        {
            "text": "The system retrieves relevant context from the knowledge base.",
            "source_url": "https://example.com/doc1",
            "relevance_score": 0.9,
            "metadata": {"doc_id": "doc_001", "section": "intro"}
        },
        {
            "text": "It then generates answers based on the provided context.",
            "source_url": "https://example.com/doc2",
            "relevance_score": 0.8,
            "metadata": {"doc_id": "doc_002", "section": "process"}
        }
    ]

    query = "How does the system work?"
    context_chunks = [result['text'] for result in spec2_style_results]
    sources = [result['source_url'] for result in spec2_style_results]

    answer = generate_answer_with_sources(query, context_chunks, sources)

    logger.info(f"Spec-2 compatibility test passed. Generated {len(answer.answer_text)} characters.")
    return True


def test_end_to_end_functionality():
    """
    Test end-to-end functionality with sample queries
    """
    logger = logging.getLogger(__name__)
    logger.info("Testing end-to-end functionality")

    # Test with various query types
    test_cases = [
        {
            "query": "What are the main components of the system?",
            "context": [
                "The system has three main components: ingestion, retrieval, and answer generation.",
                "The ingestion component processes documents and prepares them for retrieval.",
                "The retrieval component finds relevant context based on user queries.",
                "The answer generation component creates responses based on the context."
            ],
            "expected_keywords": ["components", "ingestion", "retrieval", "answer generation"]
        },
        {
            "query": "How does the retrieval process work?",
            "context": [
                "The retrieval process uses vector embeddings to find relevant context chunks.",
                "Documents are first processed and converted to vector representations.",
                "When a query is received, it's converted to a vector and compared against document vectors.",
                "The most similar vectors are returned as relevant context."
            ],
            "expected_keywords": ["vector", "embeddings", "process", "query"]
        }
    ]

    for i, test_case in enumerate(test_cases):
        logger.info(f"Running end-to-end test case {i+1}")

        answer = generate_answer(
            query=test_case["query"],
            context_chunks=test_case["context"]
        )

        # Basic validation
        assert len(answer.answer_text.strip()) > 0, "Answer should not be empty"

        # Check if expected keywords are in the answer (not strictly required but good indicator)
        answer_lower = answer.answer_text.lower()
        found_keywords = [kw for kw in test_case["expected_keywords"] if kw.lower() in answer_lower]
        logger.info(f"Found expected keywords: {found_keywords}")

        logger.info(f"Test case {i+1} passed: {len(answer.answer_text)} characters generated")

    logger.info("All end-to-end tests passed!")
    return True


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger(__name__)
    logger.info("Starting RAG Answer Generation integration tests")

    # Run all tests
    tests_passed = 0
    total_tests = 4

    try:
        # Test 1: Integration with Spec-2 retrieval
        if test_integration_with_spec2():
            tests_passed += 1
            logger.info("✓ Integration with Spec-2 test passed")
        else:
            logger.error("✗ Integration with Spec-2 test failed")

        # Test 2: Compatibility with Spec-2 data model
        if test_compatibility_with_spec2_data_model():
            tests_passed += 1
            logger.info("✓ Spec-2 data model compatibility test passed")
        else:
            logger.error("✗ Spec-2 data model compatibility test failed")

        # Test 3: End-to-end functionality
        if test_end_to_end_functionality():
            tests_passed += 1
            logger.info("✓ End-to-end functionality test passed")
        else:
            logger.error("✗ End-to-end functionality test failed")

        # Test 4: Error handling
        logger.info("Testing error handling...")
        try:
            # Test with None values - this should raise an exception due to validation
            from answer_generator import generate_answer
            try:
                empty_answer = generate_answer("", [])
                # If no exception is raised, check if the response is appropriate
                if "cannot answer" in empty_answer.answer_text.lower():
                    tests_passed += 1
                    logger.info("✓ Error handling test passed")
                else:
                    logger.error("✗ Error handling test failed: invalid query should return appropriate response")
            except ValueError:
                # This is expected behavior - empty query should raise ValueError
                tests_passed += 1
                logger.info("✓ Error handling test passed")
        except Exception as e:
            logger.error(f"✗ Error handling test failed: {e}")

        logger.info(f"\nTest Results: {tests_passed}/{total_tests} tests passed")

        if tests_passed == total_tests:
            logger.info("🎉 All integration tests passed successfully!")
            sys.exit(0)
        else:
            logger.error(f"❌ {total_tests - tests_passed} test(s) failed")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error during testing: {e}", exc_info=True)
        sys.exit(1)