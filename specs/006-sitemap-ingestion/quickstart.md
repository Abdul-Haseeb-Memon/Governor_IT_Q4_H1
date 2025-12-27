# Quickstart Guide: RAG Content Ingestion Pipeline

## Overview
This guide provides step-by-step instructions to set up and run the RAG content ingestion pipeline that loads documentation content from a sitemap, embeds it using Cohere, and stores it in Qdrant Cloud.

## Prerequisites

### 1. System Requirements
- Python 3.11 or higher
- Git
- Access to Cohere API
- Access to Qdrant Cloud

### 2. Required Accounts
- Cohere API account with `embed-english-v3.0` access
- Qdrant Cloud account with API access

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd <repository-name>
```

### 2. Navigate to Backend Directory
```bash
cd backend/ingestion
```

### 3. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

If no requirements.txt exists yet, install the required packages:
```bash
pip install requests beautifulsoup4 lxml cohere qdrant-client python-dotenv trafilatura
```

## Configuration

### 1. Create Environment File
Create a `.env` file in the backend/ingestion directory:

```bash
touch .env
```

### 2. Add Required Environment Variables
Edit the `.env` file and add the following:

```env
# Cohere Configuration
COHERE_API_KEY=your_cohere_api_key_here

# Qdrant Cloud Configuration
QDRANT_URL=your_qdrant_cluster_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=book_content_chunks

# Sitemap Configuration
SITEMAP_URL=https://governor-it-q4-h1.vercel.app/sitemap.xml
```

**Important Security Note**: Never commit the `.env` file to version control. The `.env` file should be in your `.gitignore`.

### 3. Verify Configuration
Before running the ingestion, verify your configuration:

```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

required_vars = [
    'COHERE_API_KEY',
    'QDRANT_URL',
    'QDRANT_API_KEY',
    'QDRANT_COLLECTION_NAME',
    'SITEMAP_URL'
]

missing = [var for var in required_vars if not os.getenv(var)]
if missing:
    print(f'Missing required environment variables: {missing}')
else:
    print('All required environment variables are set')
"
```

## Running the Ingestion Pipeline

### 1. Basic Ingestion
Run the complete ingestion pipeline:

```bash
python ingest.py
```

### 2. Ingestion with Logging
Run with detailed logging to monitor progress:

```bash
python ingest.py --verbose
```

### 3. Custom Sitemap URL (if needed)
If you need to specify a different sitemap URL:

```bash
SITEMAP_URL=https://your-custom-site.com/sitemap.xml python ingest.py
```

## Expected Output

### 1. Console Output
During execution, you should see progress messages like:

```
[INFO] Starting sitemap ingestion process
[INFO] Fetching sitemap from: https://governor-it-q4-h1.vercel.app/sitemap.xml
[INFO] Found 47 URLs in sitemap
[INFO] Processing URL 1/47: https://governor-it-q4-h1.vercel.app/docs/introduction
[INFO] Successfully extracted content (1250 words) from: https://governor-it-q4-h1.vercel.app/docs/introduction
[INFO] Created 2 content chunks from: https://governor-it-q4-h1.vercel.app/docs/introduction
[INFO] Generated embeddings for 2 chunks
[INFO] Stored 2 vectors in Qdrant collection: book_content_chunks
[INFO] Ingestion completed successfully! Stored 94 vectors in collection.
```

### 2. Qdrant Verification
After completion, verify the vectors were stored:

```bash
# This would be done through Qdrant Cloud dashboard or API
# Check that your collection contains the expected number of vectors
```

## Troubleshooting

### 1. Environment Variables Not Loading
**Problem**: Getting errors about missing API keys
**Solution**:
- Verify `.env` file is in the correct directory
- Check that `python-dotenv` is installed
- Restart your terminal session

### 2. Sitemap Fetch Error
**Problem**: "Failed to fetch sitemap" error
**Solution**:
- Verify the SITEMAP_URL is accessible in a browser
- Check for network connectivity issues
- Ensure the sitemap URL returns valid XML

### 3. Cohere API Error
**Problem**: "Invalid API key" or rate limit errors
**Solution**:
- Verify your COHERE_API_KEY is correct
- Check your Cohere account limits
- Ensure you're using the correct model name

### 4. Qdrant Connection Error
**Problem**: "Failed to connect to Qdrant" error
**Solution**:
- Verify QDRANT_URL and QDRANT_API_KEY are correct
- Check that your Qdrant cluster is running
- Verify network connectivity to Qdrant Cloud

## Development Commands

### 1. Run Individual Components
To test individual components of the pipeline:

```bash
# Test sitemap loading only
python sitemap_loader.py --test

# Test content extraction only
python text_processor.py --test

# Test embedding generation only (with sample data)
python embeddings.py --test
```

### 2. Clean Re-ingestion
To run the ingestion again safely (without creating duplicates):

```bash
python ingest.py --clean
```

### 3. Partial Ingestion
To ingest only a subset of URLs (for testing):

```bash
python ingest.py --limit 5  # Only process first 5 URLs
```

## Next Steps

### 1. Verification
After successful ingestion:
- Verify all vectors are stored in Qdrant
- Check that metadata is correctly preserved
- Test retrieval functionality (if available)

### 2. Integration
- Integrate with your RAG retrieval system
- Set up monitoring for the ingestion process
- Consider setting up scheduled ingestion runs

### 3. Optimization
- Monitor performance metrics
- Adjust chunk size if needed
- Optimize API usage based on your Cohere and Qdrant limits

## Common Use Cases

### 1. Initial Setup
For first-time setup with the Governor IT documentation:

```bash
# Ensure environment is configured
cp .env.example .env  # if you have an example file
# Edit .env with your actual keys

# Run full ingestion
python ingest.py
```

### 2. Scheduled Updates
For periodic updates to keep content fresh:

```bash
# Run regularly to update content
python ingest.py  # This will safely update existing content
```

### 3. Testing Changes
To test with a small subset before full ingestion:

```bash
# Test with only 3 URLs first
python ingest.py --limit 3 --verbose
```

## Support

If you encounter issues not covered in this guide:
1. Check the detailed logs for specific error messages
2. Verify all API keys and endpoints are correct
3. Confirm your accounts have sufficient quotas for the operations
4. Review the main specification document for detailed requirements