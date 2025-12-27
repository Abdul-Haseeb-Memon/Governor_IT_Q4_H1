# Quickstart: Frontend Integration for RAG Chatbot

**Feature**: Frontend RAG Integration
**Date**: 2025-12-25

## Prerequisites

- Node.js 16+ with npm
- Access to backend RAG API endpoints (Spec-2 and Spec-3)
- API_BASE_URL configured for backend services
- Frontend development environment (React/Docusaurus)

## Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install frontend dependencies
```bash
cd frontend_H_book
npm install
```

### 3. Configure environment variables
Create a `.env` file in the frontend root directory with:
```env
API_BASE_URL=https://your-backend-api.com
AUTH_TOKEN=your_auth_token_if_required
```

### 4. Verify configuration
```bash
npm run dev
```

## Usage

### Basic Chat Interface
```javascript
// Example usage of the chat components
import ChatInterface from './components/ChatInterface';

// Render the chat interface
<ChatInterface />
```

### Using the RAG Service
```javascript
import { RAGService } from './services/RAGService';

const ragService = new RAGService();

// Retrieve context for a query
const context = await ragService.retrieveContext("Your question here");

// Generate an answer
const answer = await ragService.generateAnswer("Your question here", context);

console.log(`Answer: ${answer.answer}`);
console.log(`Sources: ${answer.sources}`);
```

### Chat Input Component
```javascript
import ChatInput from './components/ChatInput';

// Simple query submission
const handleSubmit = async (query) => {
  const response = await ragService.generateAnswer(query);
  console.log(`Generated answer: ${response.answer}`);
};

<ChatInput onSubmit={handleSubmit} />
```

### Chat Display Component
```javascript
import ChatDisplay from './components/ChatDisplay';

// Display answers with source attribution
const messages = [
  { sender: 'user', content: 'What are the key features?' },
  {
    sender: 'system',
    content: 'The key features include context retrieval and answer generation.',
    sources: ['https://example.com/doc1', 'https://example.com/doc2']
  }
];

<ChatDisplay messages={messages} />
```

## Configuration

### Environment Variables
- `API_BASE_URL`: Base URL for backend RAG API endpoints
- `AUTH_TOKEN`: Optional authentication token for protected endpoints

### Parameters
- `debounceDelay`: Delay for debouncing user input (default: 300ms)
- `loadingTimeout`: Timeout for API calls (default: 30000ms)
- `retryAttempts`: Number of retry attempts for failed requests (default: 3)

## Testing the Setup

### 1. Test API connectivity
```javascript
import { RAGService } from './services/RAGService';

const service = new RAGService();
const isConnected = await service.testConnection();
console.log(`API connection: ${isConnected ? 'SUCCESS' : 'FAILURE'}`);
```

### 2. Test query submission
```javascript
// Submit a test query
const testQuery = "What are the main components?";
const response = await ragService.generateAnswer(testQuery);
console.log(`Test response: ${response.answer}`);
```

### 3. End-to-end test
```javascript
// Full integration test
const query = "How does the system work?";
const answer = await ragService.generateAnswer(query);
console.log(`Final answer: ${answer.answer}`);
console.log(`With sources: ${answer.sources.length} references`);
```

## Troubleshooting

### Common Issues

**Issue**: "Failed to fetch" errors during API calls
**Solution**: Verify API_BASE_URL is correctly configured and backend services are running

**Issue**: "Authentication required" errors
**Solution**: Check AUTH_TOKEN configuration in environment variables

**Issue**: Slow response times
**Solution**: Verify backend performance and network connectivity

### Logging
Enable debug logging to see detailed information:
```javascript
// Enable detailed logging
localStorage.setItem('debug', 'rag-chat:*');
```

## Integration with Backend RAG Pipeline

The frontend expects the following from the backend:

1. **Retrieve endpoint**: `POST /retrieve` - accepts query, returns context chunks
2. **Answer endpoint**: `POST /answer` - accepts query and context, returns generated answer
3. **Response format**: JSON with consistent structure for reliable parsing

### Expected Backend Response Format
```javascript
{
  "answer": "Generated answer text",
  "sources": ["https://example.com/source1", "https://example.com/source2"],
  "confidence": 0.85
}
```

## Next Steps

1. Integrate with your existing frontend application
2. Customize the chat interface styling to match your brand
3. Add analytics to track user interactions
4. Monitor performance and user satisfaction metrics