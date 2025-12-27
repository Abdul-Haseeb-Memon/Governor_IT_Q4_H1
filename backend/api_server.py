"""
RAG API Server for frontend integration.

This module provides API endpoints for the frontend to interact with the RAG system.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from retrieval.retrieve import retrieve_relevant_content
from answer_generation.answer_generator import generate_answer
# Import the GeneratedAnswer class separately to avoid conflicts
from answer_generation.answer_generator import GeneratedAnswer
from ingestion.ingest import run_ingestion_pipeline

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG API",
    description="API for Retrieval-Augmented Generation system",
    version="1.0.0"
)

# Add CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RetrieveRequest(BaseModel):
    query: str
    limit: Optional[int] = 5

class RetrieveResponse(BaseModel):
    text: str
    source_url: str
    relevance_score: float
    title: Optional[str] = ""

class AnswerRequest(BaseModel):
    query: str
    context: List[Dict[str, Any]]

class AnswerResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float

class HealthResponse(BaseModel):
    status: str
    message: str

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", message="RAG API is running")

@app.post("/retrieve", response_model=List[RetrieveResponse])
async def retrieve_endpoint(request: RetrieveRequest):
    """Retrieve relevant content chunks for a query."""
    try:
        logger.info(f"Retrieving content for query: {request.query[:50]}...")
        results = retrieve_relevant_content(request.query, limit=request.limit)

        formatted_results = []
        for result in results:
            formatted_results.append(RetrieveResponse(
                text=result.get('text', ''),
                source_url=result.get('source_url', ''),
                relevance_score=result.get('relevance_score', 0.0),
                title=result.get('title', '')
            ))

        logger.info(f"Retrieved {len(formatted_results)} results")
        return formatted_results

    except Exception as e:
        logger.error(f"Error in retrieve endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/answer", response_model=AnswerResponse)
async def answer_endpoint(request: AnswerRequest):
    """Generate an answer based on query and context."""
    try:
        logger.info(f"Generating answer for query: {request.query[:50]}...")

        # Extract text from context chunks
        context_texts = [chunk.get('text', '') for chunk in request.context if 'text' in chunk]
        sources = [chunk.get('source_url', '') for chunk in request.context if 'source_url' in chunk]

        # Generate answer using the backend system
        answer_obj: GeneratedAnswer = generate_answer(request.query, context_texts, sources)

        response = AnswerResponse(
            answer=answer_obj.answer_text,
            sources=answer_obj.source_citations,
            confidence=answer_obj.confidence_score
        )

        logger.info("Answer generated successfully")
        return response

    except Exception as e:
        logger.error(f"Error in answer endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/qa", response_model=AnswerResponse)
async def qa_endpoint(request: RetrieveRequest):
    """Complete QA endpoint that retrieves and answers in one call."""
    try:
        logger.info(f"Processing QA request for query: {request.query[:50]}...")

        # First retrieve relevant content
        results = retrieve_relevant_content(request.query, limit=request.limit)

        # Format context for answer generation
        context_texts = [result.get('text', '') for result in results if result.get('text')]
        sources = [result.get('source_url', '') for result in results if result.get('source_url')]

        # Generate answer based on retrieved context
        answer_obj: GeneratedAnswerObj = generate_answer(request.query, context_texts, sources)

        response = AnswerResponse(
            answer=answer_obj.answer_text,
            sources=answer_obj.source_citations,
            confidence=answer_obj.confidence_score
        )

        logger.info("QA request processed successfully")
        return response

    except Exception as e:
        logger.error(f"Error in QA endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


class IngestionRequest(BaseModel):
    sitemap_url: Optional[str] = None
    skip_duplicates: bool = True
    resume: bool = False


class IngestionResponse(BaseModel):
    status: str
    message: str
    processed_urls: int = 0
    failed_urls: int = 0


@app.post("/ingest", response_model=IngestionResponse)
async def ingestion_endpoint(request: IngestionRequest):
    """Trigger the ingestion pipeline to populate the vector database."""
    try:
        logger.info(f"Starting ingestion pipeline with sitemap: {request.sitemap_url or 'default'}")

        # Run the ingestion pipeline
        run_ingestion_pipeline(
            sitemap_url=request.sitemap_url,
            skip_duplicates=request.skip_duplicates,
            resume=request.resume
        )

        # For a more complete response, we would need to modify run_ingestion_pipeline
        # to return statistics, but for now we'll return a basic success response
        response = IngestionResponse(
            status="success",
            message="Ingestion pipeline completed successfully"
        )

        logger.info("Ingestion pipeline completed successfully")
        return response

    except Exception as e:
        logger.error(f"Error in ingestion endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)