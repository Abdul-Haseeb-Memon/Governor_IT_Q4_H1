# RAG Answer Generation Module

This module provides grounded answer generation using the OpenRouter API. It takes user queries and retrieved context chunks to generate accurate, contextually-relevant answers without hallucination.

## Overview

The RAG Answer Generation module is responsible for:
- Accepting user queries and context chunks from the retrieval layer
- Constructing prompts with proper grounding instructions
- Generating answers using OpenRouter's language models
- Ensuring all answers are grounded in the provided context
- Handling errors gracefully with fallback responses

## Architecture

The module follows a clean separation of concerns:

- `config.py`: Handles environment variable loading and validation
- `prompt_constructor.py`: Formats prompts with context and grounding instructions
- `openrouter_client.py`: Interfaces with the OpenRouter API
- `answer_generator.py`: Main orchestration and business logic
- `utils.py`: Shared utilities and error handling functions

## Installation

```bash
cd backend/answer_generation
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the backend directory with the following variables:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-3.5-turbo
APP_NAME=g-house-project
```

## Usage

### Basic Answer Generation

```python
from answer_generator import generate_answer

# Simple query with context
query = "What are the key features?"
context_chunks = [
    "The system provides comprehensive RAG functionality.",
    "Key features include context retrieval and answer generation."
]

answer = generate_answer(query, context_chunks)
print(f"Answer: {answer.answer_text}")
print(f"Confidence: {answer.confidence_score}")
```

### Advanced Usage with Sources

```python
from answer_generator import generate_answer_with_sources

# Generate answer with source tracking
query = "How does the system work?"
context_chunks = [
    "The system retrieves relevant context from the knowledge base.",
    "It then generates answers based on the provided context."
]
sources = [
    "https://example.com/doc1",
    "https://example.com/doc2"
]

answer = generate_answer_with_sources(query, context_chunks, sources)
print(f"Answer: {answer.answer_text}")
print(f"Sources used: {answer.source_citations}")
print(f"Hallucination detected: {answer.hallucination_detected}")
```

### Using the AnswerGenerator Class

```python
from answer_generator import AnswerGenerator

# Initialize the generator
generator = AnswerGenerator()

# Generate answer
answer = generator.generate("Your query here", ["context chunk 1", "context chunk 2"])
print(f"Generated answer: {answer.answer_text}")
```

## Data Model

### QueryWithContext
- `query`: User query text (required)
- `context_chunks`: List of context chunk strings (required)
- `retrieved_sources`: List of source URLs (optional)

### GeneratedAnswer
- `answer_text`: The generated answer text (required)
- `confidence_score`: Confidence in the grounding of the answer (0.0-1.0)
- `source_citations`: List of sources used in generating the answer
- `hallucination_detected`: Flag indicating if potential hallucination was detected

## Error Handling

The module implements comprehensive error handling:
- API failures: Returns safe fallback responses
- Empty context: Returns appropriate message
- Invalid input: Returns error message
- Rate limiting: Implements retry with exponential backoff

## Integration with Spec-2

The answer generation module expects context in the format provided by Spec-2:

```python
from retrieval.retrieve import retrieve_relevant_content

# Get context from Spec-2
query = "Your question here"
retrieved_results = retrieve_relevant_content(query)

# Extract context chunks
context_chunks = [result['text'] for result in retrieved_results]
sources = [result['source_url'] for result in retrieved_results]

# Generate answer
from answer_generation.answer_generator import generate_answer_with_sources
answer = generate_answer_with_sources(query, context_chunks, sources)
```

## Security

- All API keys are loaded from environment variables
- No sensitive information is logged
- Input validation is performed on all user inputs

## Performance

- Efficient prompt processing
- Proper resource management
- Scalable architecture

## Usage Examples

### Basic Answer Generation

```python
from answer_generator import generate_answer

# Simple query with context
query = "What are the key features?"
context_chunks = [
    "The system provides comprehensive RAG functionality.",
    "Key features include context retrieval and answer generation."
]

answer = generate_answer(query, context_chunks)
print(f"Answer: {answer.answer_text}")
print(f"Confidence: {answer.confidence_score}")
```

### Advanced Usage with Sources

```python
from answer_generator import generate_answer_with_sources

# Generate answer with source tracking
query = "How does the system work?"
context_chunks = [
    "The system retrieves relevant context from the knowledge base.",
    "It then generates answers based on the provided context."
]
sources = [
    "https://example.com/doc1",
    "https://example.com/doc2"
]

answer = generate_answer_with_sources(query, context_chunks, sources)
print(f"Answer: {answer.answer_text}")
print(f"Sources used: {answer.source_citations}")
print(f"Hallucination detected: {answer.hallucination_detected}")
```

### Using the AnswerGenerator Class

```python
from answer_generator import AnswerGenerator

# Initialize the generator
generator = AnswerGenerator()

# Generate answer with progress tracking
answer = generator.generate_with_progress_tracking("Your query here", ["context chunk 1", "context chunk 2"])
print(f"Generated answer: {answer.answer_text}")

# Generate answer without progress tracking
answer = generator.generate("Your query here", ["context chunk 1", "context chunk 2"])
print(f"Generated answer: {answer.answer_text}")
```

### Command Line Interface

You can also use the command-line interface for testing:

```bash
# Basic usage
python -m cli --query "What are the key features?" --context "The system provides comprehensive RAG functionality." "Key features include context retrieval."

# With context from a file
python -m cli --query "How does the system work?" --context-file /path/to/context.txt

# With verbose logging
python -m cli --query "Your question" --context "Context chunk" --verbose
```

## Integration Guide

### Integration with Spec-2 (Retrieval Layer)

The answer generation module expects context in the format provided by Spec-2:

```python
from retrieval.retrieve import retrieve_relevant_content  # Assuming this is the Spec-2 module

# Get context from Spec-2
query = "Your question here"
retrieved_results = retrieve_relevant_content(query)

# Extract context chunks
context_chunks = [result['text'] for result in retrieved_results]
sources = [result['source_url'] for result in retrieved_results]

# Generate answer
from answer_generation.answer_generator import generate_answer_with_sources
answer = generate_answer_with_sources(query, context_chunks, sources)
```

### Configuration Options

You can customize the behavior through environment variables:

```env
# API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-3.5-turbo
APP_NAME=g-house-project

# Model Parameters
OPENROUTER_TEMPERATURE=0.1          # Lower for more deterministic output
OPENROUTER_TOP_P=0.9
OPENROUTER_MAX_TOKENS=1000
OPENROUTER_PRESENCE_PENALTY=0.0
OPENROUTER_FREQUENCY_PENALTY=0.0

# API Request Settings
OPENROUTER_REQUEST_TIMEOUT=30       # Request timeout in seconds
OPENROUTER_MAX_RETRIES=3            # Number of retry attempts
MAX_CALLS_PER_MINUTE=10             # Rate limiting (optional)

# Logging
LOG_LEVEL=INFO                      # Log level (DEBUG, INFO, WARNING, ERROR)
```

## Validation and Testing

The system includes comprehensive validation to ensure answers are properly grounded and deterministic:

```bash
# Run comprehensive validation
python validate_deterministic.py

# Run integration tests
python test_integration.py

# Run the main module to validate all requirements
python -m answer_generator
```