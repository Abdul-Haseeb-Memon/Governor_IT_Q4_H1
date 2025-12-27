# Research: RAG Answer Generation using OpenRouter

**Feature**: RAG Answer Generation
**Date**: 2025-12-25

## Research Findings

### OpenRouter API Integration

**Decision**: Use direct HTTP API calls to OpenRouter instead of a dedicated SDK
**Rationale**: OpenRouter provides a RESTful API that can be accessed directly with standard HTTP requests. This approach avoids adding an extra dependency and provides more control over request formatting and response handling.
**Alternatives considered**:
- OpenRouter Python SDK: May not exist or be actively maintained
- Third-party libraries: Would add unnecessary complexity
- Other LLM providers: Would break compatibility with specified OpenRouter requirement

### Prompt Engineering for Grounding

**Decision**: Use clear context-question separation with explicit grounding instructions
**Rationale**: The most effective way to prevent hallucination is to clearly separate the context from the question and explicitly instruct the model to only use the provided context. This approach has been proven effective in RAG systems.
**Prompt format example**:
```
Context:
[context chunk 1]
[context chunk 2]
[context chunk 3]

Question: [user question]

Instructions: Answer the question using ONLY the provided context. Do not use any prior knowledge or information not present in the context. If the context does not contain sufficient information to answer the question, respond with "I cannot answer this question based on the provided context."
```

**Alternatives considered**:
- Few-shot examples: More complex and token-intensive
- System messages: May not be as effective for grounding
- Different context-question ordering: Less clear separation of information

### Error Handling Strategy

**Decision**: Comprehensive error handling with graceful degradation and safe fallbacks
**Rationale**: Production systems must handle various failure modes (API limits, network issues, empty context) gracefully without exposing internal details or crashing. The system should return meaningful responses even when components fail.
**Approach**:
- API failure: Return safe fallback response
- Empty context: Return appropriate message
- Invalid input: Return error message
- Rate limiting: Implement retry with exponential backoff

**Alternatives considered**:
- Fail-fast approach: Would result in poor user experience
- Silent failure: Would hide issues from monitoring
- Different retry strategies: Exponential backoff for API calls

### Configuration Management

**Decision**: Load all secrets from environment variables using python-dotenv
**Rationale**: This follows security best practices by avoiding hardcoded credentials and allows for easy configuration across different environments.
**Required environment variables**:
- `OPENROUTER_API_KEY`: OpenRouter API key
- `OPENROUTER_BASE_URL`: OpenRouter API endpoint
- `OPENROUTER_MODEL`: Model identifier to use
- `APP_NAME`: For OpenRouter headers

**Alternatives considered**:
- Configuration files: Risk of committing secrets to version control
- Command-line arguments: Risk of exposing secrets in process lists
- External configuration services: Added complexity for this use case

### Model Parameters for Deterministic Output

**Decision**: Use low temperature settings and other deterministic parameters
**Rationale**: To ensure consistent, grounded answers, we need to minimize randomness in the model's output. Low temperature makes the model more deterministic and focused on the provided context.
**Parameters to set**:
- `temperature`: 0.1 (very low for consistency)
- `top_p`: 0.9 (to maintain some diversity while being focused)
- `max_tokens`: Appropriate limit for response length

**Alternatives considered**:
- Higher temperature: Would produce more creative but less consistent answers
- Different sampling strategies: Would introduce more randomness

### Context Length Management

**Decision**: Implement context chunk selection and truncation
**Rationale**: Language models have token limits, so we need to manage how much context is sent. We should select the most relevant chunks and truncate if necessary while preserving the most important information.
**Approach**:
- Select top-k most relevant chunks from Spec-2 retrieval
- Implement truncation if total context exceeds token limits
- Preserve beginning and end of important chunks

**Alternatives considered**:
- Send all context: Would exceed token limits
- Random selection: Would not optimize for relevance
- Fixed context size: Would not adapt to query needs

### Hallucination Detection

**Decision**: Implement post-processing to detect potential hallucinations
**Rationale**: While prompt engineering helps minimize hallucinations, some may still occur. A secondary check can flag potential hallucinations by comparing the answer to the provided context.
**Approach**:
- Compare answer content to context using similarity measures
- Flag answers that contain information not present in context
- Log potential hallucinations for monitoring

**Alternatives considered**:
- No detection: Would allow hallucinations to pass through
- More complex NLP: Would add unnecessary complexity
- Different similarity measures: Cosine similarity is sufficient for this purpose