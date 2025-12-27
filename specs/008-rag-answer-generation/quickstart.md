# Quickstart: RAG Answer Generation using OpenRouter

**Feature**: RAG Answer Generation
**Date**: 2025-12-25

## Prerequisites

- Python 3.11+
- OpenRouter API access
- Content retrieved by Spec-2 (RAG Retrieval Layer)
- `.env` file with required environment variables in backend directory

## Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install dependencies
```bash
cd backend/answer_generation
pip install -r requirements.txt
```

### 3. Configure environment variables
Ensure your backend/.env file contains:
```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-3.5-turbo
APP_NAME=g-house-project
```

### 4. Verify configuration
```bash
python -c "from answer_generation.config import Config; Config.validate(); print('Configuration validated successfully')"
```

## Usage

### Basic Answer Generation
```python
from answer_generation.answer_generator import generate_answer

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
from answer_generation.answer_generator import generate_answer_with_sources

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
from answer_generation.answer_generator import AnswerGenerator

# Initialize the generator
generator = AnswerGenerator()

# Generate answer
answer = generator.generate("Your query here", ["context chunk 1", "context chunk 2"])
print(f"Generated answer: {answer.answer_text}")
```

## Configuration

### Environment Variables
- `OPENROUTER_API_KEY`: OpenRouter API key for LLM access
- `OPENROUTER_BASE_URL`: OpenRouter API endpoint URL
- `OPENROUTER_MODEL`: Model identifier to use for generation
- `APP_NAME`: Application name for OpenRouter headers

### Parameters
- `temperature`: Controls randomness (default: 0.1 for consistency)
- `max_tokens`: Maximum tokens in response (default: 1000)
- `top_p`: Nucleus sampling parameter (default: 0.9)

## Testing the Setup

### 1. Test OpenRouter connection
```python
from answer_generation.openrouter_client import OpenRouterClient

client = OpenRouterClient()
response = client.test_connection()
print(f"Connection test: {response}")
```

### 2. Test prompt construction
```python
from answer_generation.prompt_constructor import construct_prompt

query = "Test query"
context = ["Test context chunk"]
prompt = construct_prompt(query, context)
print(f"Constructed prompt: {prompt[:200]}...")
```

### 3. End-to-end test
```python
from answer_generation.answer_generator import generate_answer

context = ["The system uses RAG to generate answers."]
answer = generate_answer("What does the system do?", context)
print(f"Generated answer: {answer.answer_text}")
```

## Troubleshooting

### Common Issues

**Issue**: "Missing required environment variables"
**Solution**: Verify your .env file contains all required variables

**Issue**: "OpenRouter API error during answer generation"
**Solution**: Check your OPENROUTER_API_KEY and ensure your account has sufficient credits

**Issue**: "Context too long for model"
**Solution**: Reduce the number of context chunks or truncate longer chunks

### Logging
Enable debug logging to see detailed information:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

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

## Next Steps

1. Integrate with your RAG application
2. Connect to the retrieval layer (Spec-2) for context
3. Add to your frontend application (Spec-4)
4. Monitor answer quality and grounding