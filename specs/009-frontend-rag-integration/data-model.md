# Data Model: Frontend Integration for RAG Chatbot

**Feature**: Frontend RAG Integration
**Date**: 2025-12-25

## Core Entities

### QueryRequest
**Description**: Represents a user query submitted to the RAG system

**Fields**:
- `query`: string
  - **Type**: String
  - **Required**: Yes
  - **Validation**: Must not be empty, length 1-1000 characters
  - **Description**: The user's question text

### AnswerResponse
**Description**: Represents the final answer received from the RAG system

**Fields**:
- `answer`: string
  - **Type**: String
  - **Required**: Yes
  - **Validation**: Must not be empty
  - **Description**: The generated answer text from the backend

- `sources`: Array<string>
  - **Type**: Array of strings
  - **Required**: No
  - **Default**: Empty array
  - **Description**: List of source URLs for the information in the answer

- `confidence`: number
  - **Type**: Number
  - **Required**: No
  - **Default**: 0.5
  - **Range**: 0.0 to 1.0
  - **Description**: Confidence score for the answer quality

### ChatMessage
**Description**: Represents a message in the chat interface

**Fields**:
- `id`: string
  - **Type**: String
  - **Required**: Yes
  - **Validation**: Unique identifier
  - **Description**: Unique ID for the message

- `content`: string
  - **Type**: String
  - **Required**: Yes
  - **Description**: The message content (either user query or system response)

- `sender`: string
  - **Type**: String
  - **Required**: Yes
  - **Validation**: Must be either "user" or "system"
  - **Description**: Indicates who sent the message

- `timestamp`: Date
  - **Type**: Date
  - **Required**: Yes
  - **Description**: When the message was created

### ChatSession
**Description**: Represents a chat session with the RAG system

**Fields**:
- `sessionId`: string
  - **Type**: String
  - **Required**: Yes
  - **Validation**: Unique identifier
  - **Description**: Unique ID for the chat session

- `messages`: Array<ChatMessage>
  - **Type**: Array of ChatMessage objects
  - **Required**: No
  - **Default**: Empty array
  - **Description**: Collection of messages in the chat session

- `createdAt`: Date
  - **Type**: Date
  - **Required**: Yes
  - **Description**: When the session was created

## API Contracts

### Function: retrieveContext(query: string) -> Promise<Array<ContextChunk>>
**Input**:
- query: User query text (1-1000 characters)

**Output**:
- Array of ContextChunk objects with text and source information

**Errors**:
- Error if backend is unreachable
- Error if query is invalid
- Error if context retrieval fails

### Function: generateAnswer(query: string, context: Array<ContextChunk>) -> Promise<AnswerResponse>
**Input**:
- query: User query text (1-1000 characters)
- context: Array of context chunks from retrieval

**Output**:
- AnswerResponse object with answer text and metadata

**Errors**:
- Error if backend is unreachable
- Error if query is invalid
- Error if answer generation fails

### Function: validateQuery(query: string) -> boolean
**Input**:
- query: User query text

**Output**:
- Boolean indicating if query is valid for submission

**Errors**:
- None, always returns a boolean

## Data Flow

### Frontend Request Flow
1. **Input**: User enters query in ChatInput component
2. **Processing**: Query validation and sanitization
3. **API Call**: Request sent to backend `/retrieve` endpoint
4. **API Call**: Request sent to backend `/answer` endpoint
5. **Output**: AnswerResponse displayed in ChatDisplay component

### Component State Flow
1. **State**: ChatSession with messages array
2. **Action**: User submits query
3. **Update**: Add user message to messages array
4. **API**: Retrieve context and generate answer
5. **Update**: Add system response to messages array
6. **Render**: Display updated chat in ChatDisplay component

### Data Validation Rules
- Query must be between 1 and 1000 characters
- Answer text must not be empty
- Sources must be valid URLs
- Confidence score must be between 0.0 and 1.0
- Messages must have unique IDs
- Sender must be either "user" or "system"

## Integration with Backend Data Model

The frontend expects the following from the backend:

- `ContextChunk`: Objects with `text` and `source_url` fields from Spec-2
- `GeneratedAnswer`: Objects from Spec-3 with `answer_text`, `source_citations`, and `confidence_score`
- API responses in JSON format with proper error handling
- Consistent data structure for reliable frontend parsing

This ensures seamless integration between the frontend interface and the backend RAG pipeline.