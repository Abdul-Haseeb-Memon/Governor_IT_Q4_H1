# Quickstart: RAG System Validation

## Overview
This guide provides instructions for running the RAG system validation to ensure all components (Spec-006 through Spec-009) work correctly together.

## Prerequisites
- Python 3.11+ installed
- Node.js and npm installed
- Access to Qdrant Cloud instance
- API keys for Cohere and OpenRouter
- Git for version control

## Environment Setup
1. Create a `.env` file in the project root with the following variables:
   ```env
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   COHERE_API_KEY=your_cohere_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   BACKEND_URL=http://localhost:8000
   FRONTEND_URL=http://localhost:3000
   QDRANT_COLLECTION_NAME=your_collection_name
   ```

## Running the Validation
1. Navigate to the project root directory
2. Ensure all required services are running:
   - Backend API server
   - Frontend development server
   - Qdrant vector database
3. Execute the validation command:
   ```bash
   # Run validation for all components
   python -m backend.validate_complete_system
   ```

## Validation Process
The validation system will:
1. Check Spec-006 (Ingestion): Verify sitemap ingestion and Qdrant population
2. Check Spec-007 (Retrieval): Test backend retrieval endpoint functionality
3. Check Spec-008 (Generation): Validate OpenRouter answer generation
4. Check Spec-009 (Frontend): Confirm frontend builds and communicates with backend
5. Execute end-to-end pipeline test

## Expected Output
- Component validation results for each of the four specs
- Error identification for any failing components
- Corrective actions applied to fix common issues
- Confirmation that all components work together

## Troubleshooting
- If validation fails, check that all environment variables are properly set
- Verify that all services are running before starting validation
- Review logs for specific error messages
- Ensure API keys have appropriate permissions