# RAG Chatbot Frontend Integration

This project implements the frontend integration for a RAG (Retrieval-Augmented Generation) chatbot system. It provides a user interface for querying a knowledge base and receiving AI-generated answers with source attribution.

## Features

- **Chat Interface**: Clean, responsive chat interface for interacting with the RAG system
- **Source Attribution**: Clear display of source references for generated answers
- **Error Handling**: Comprehensive error handling and user feedback
- **Responsive Design**: Works on desktop and mobile devices
- **Security**: Secure API communication with environment-based configuration

## Setup

### Prerequisites

- Node.js 16+ with npm
- Access to the RAG backend API (Spec-2 and Spec-3)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables by creating a `.env` file:
```env
API_BASE_URL=https://your-backend-api.com
# AUTH_TOKEN=your_auth_token_if_required
```

3. Start the development server:
```bash
npm run start
```

## Usage

### Running the Application

The application is built as a Docusaurus site. To run it:

```bash
# Development mode
npm run start

# Build for production
npm run build

# Serve production build locally
npm run serve
```

### API Configuration

The application connects to the RAG backend through two main endpoints:

- `POST /retrieve` - Retrieves context chunks relevant to the user query
- `POST /answer` - Generates an answer based on the query and retrieved context

The API base URL is configured through the `API_BASE_URL` environment variable.

### Components

The frontend consists of several key components:

- **ChatInterface**: Main component that orchestrates the chat experience
- **ChatInput**: Handles user input with validation and submission
- **ChatDisplay**: Displays conversation history with source attribution
- **RAGService**: API service layer for backend communication
- **useChatState**: React hook for chat state management
- **errorHandler**: Utilities for error handling and validation

## Testing

A command-line interface is available for testing components:

```bash
node test-cli.js test-connection
node test-cli.js test-query "Your question here"
node test-cli.js validate-query "A sample query"
```

For full validation:

```bash
node validate-integration.js
node validate-requirements.js
```

## Architecture

The frontend maintains a clear separation of concerns:

- **Presentation Layer**: React components for UI
- **Service Layer**: RAGService for API communication
- **Data Layer**: Type definitions and validation utilities
- **State Management**: React hooks for component state

## Security

- API keys and sensitive information are stored in environment variables
- No retrieval or embedding logic exists in the frontend
- All processing happens on the backend
- Input validation and sanitization are implemented
- Secure communication via HTTPS

## Environment Variables

- `API_BASE_URL`: Base URL for backend RAG API endpoints
- `AUTH_TOKEN`: Optional authentication token for protected endpoints

## API Response Format

The frontend expects responses in the following format:

```javascript
{
  "answer": "Generated answer text",
  "sources": ["https://example.com/source1", "https://example.com/source2"],
  "confidence": 0.85
}
```

## Error Handling

The system provides user-friendly error messages and graceful degradation when backend services are unavailable.

## Integration with Backend

This frontend integrates with:
- Spec-1: Content ingestion in Qdrant (provides knowledge base)
- Spec-2: Semantic retrieval module (provides context retrieval)
- Spec-3: OpenRouter answer generation module (provides answer generation)

## Development

To run tests and validation:

```bash
# Run integration validation
node validate-integration.js

# Run requirements validation
node validate-requirements.js

# Run component tests via CLI
node test-cli.js help
```

## Deployment

The application is designed for deployment on Vercel but can be deployed on any platform that supports Docusaurus applications.

## Troubleshooting

### Common Issues

- **API Connection Errors**: Verify `API_BASE_URL` is correctly configured
- **Authentication Issues**: Check `AUTH_TOKEN` if required by backend
- **Slow Response Times**: Verify backend performance and network connectivity

For detailed logging, enable debug mode in the browser console.
