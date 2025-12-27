"""
Main ingestion pipeline for RAG Content Ingestion Pipeline.

This module orchestrates the complete ingestion workflow.
"""
import logging
import time
import argparse
import json
import os
from typing import List, Dict, Any
from .sitemap_loader import load_sitemap_urls
from .text_processor import extract_and_chunk_url, ContentChunk
from .embeddings import create_embeddings
from .qdrant_client import store_content_chunks
from .config import Config


def setup_logging():
    """Set up logging configuration."""
    import os
    os.makedirs('logs', exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/ingestion.log'),
            logging.StreamHandler()
        ]
    )


def save_progress(processed_urls: List[str], failed_urls: List[str], checkpoint_file: str = 'ingestion_progress.json'):
    """
    Save the progress of the ingestion pipeline to a checkpoint file.

    Args:
        processed_urls: List of URLs that have been successfully processed
        failed_urls: List of URLs that failed to process
        checkpoint_file: Path to the checkpoint file
    """
    progress_data = {
        'processed_urls': processed_urls,
        'failed_urls': failed_urls,
        'timestamp': time.time()
    }

    with open(checkpoint_file, 'w') as f:
        json.dump(progress_data, f, indent=2)

    logging.info(f"Progress saved to {checkpoint_file}")


def load_progress(checkpoint_file: str = 'ingestion_progress.json') -> Dict[str, List[str]]:
    """
    Load the progress of the ingestion pipeline from a checkpoint file.

    Args:
        checkpoint_file: Path to the checkpoint file

    Returns:
        Dictionary containing processed and failed URLs
    """
    try:
        with open(checkpoint_file, 'r') as f:
            progress_data = json.load(f)
        logging.info(f"Progress loaded from {checkpoint_file}")
        return progress_data
    except FileNotFoundError:
        logging.info(f"No checkpoint file found at {checkpoint_file}")
        return {'processed_urls': [], 'failed_urls': []}
    except Exception as e:
        logging.error(f"Error loading progress from {checkpoint_file}: {e}")
        return {'processed_urls': [], 'failed_urls': []}


def run_ingestion_pipeline(sitemap_url: str = None, skip_duplicates: bool = True, resume: bool = False):
    """Run the complete ingestion pipeline."""
    start_time = time.time()
    logging.info("Starting RAG Content Ingestion Pipeline")

    try:
        # Validate configuration
        Config.validate()
        logging.info("Configuration validated successfully")

        # Use provided sitemap URL or fall back to config
        target_sitemap_url = sitemap_url or Config.SITEMAP_URL
        logging.info(f"Loading URLs from sitemap: {target_sitemap_url}")

        sitemap_urls = load_sitemap_urls(target_sitemap_url)
        logging.info(f"Loaded {len(sitemap_urls)} URLs from sitemap")

        # Handle resume functionality
        processed_urls = []
        failed_urls = []

        if resume:
            progress_data = load_progress()
            processed_urls = progress_data.get('processed_urls', [])
            failed_urls = progress_data.get('failed_urls', [])

            # Filter out already processed URLs
            urls_to_process = [url_data for url_data in sitemap_urls
                              if url_data['url'] not in processed_urls]
            logging.info(f"Resuming from checkpoint: {len(urls_to_process)} URLs remaining to process")
        else:
            urls_to_process = sitemap_urls
            # Clear any existing progress file
            if os.path.exists('ingestion_progress.json'):
                os.remove('ingestion_progress.json')

        # Step 2: Process each URL to extract content and create chunks
        all_chunks: List[ContentChunk] = []
        newly_processed_urls = []

        for i, url_data in enumerate(urls_to_process):
            url = url_data['url']
            logging.info(f"Processing URL {i+1}/{len(urls_to_process)}: {url}")

            try:
                chunks = extract_and_chunk_url(url)
                if chunks:
                    all_chunks.extend(chunks)
                    newly_processed_urls.append(url)
                    processed_urls.append(url)
                    logging.info(f"Extracted {len(chunks)} chunks from {url}")
                else:
                    logging.warning(f"Failed to extract content from {url}")
                    failed_urls.append(url)
            except Exception as e:
                logging.error(f"Error processing URL {url}: {str(e)}")
                failed_urls.append(url)

            # Save progress periodically
            if (i + 1) % 10 == 0:  # Save every 10 URLs
                save_progress(processed_urls, failed_urls)

        # Save final progress
        save_progress(processed_urls, failed_urls)

        logging.info(f"Successfully processed {len(newly_processed_urls)}/{len(urls_to_process)} new URLs")
        logging.info(f"Previously processed {len([url for url in sitemap_urls if url['url'] in processed_urls and url['url'] not in newly_processed_urls])} URLs")
        logging.info(f"Failed to process {len(failed_urls)} URLs in total")
        logging.info(f"Total chunks created: {len(all_chunks)}")

        if not all_chunks:
            logging.info("No new content chunks were created (all URLs may have been previously processed).")
            return

        # Step 3: Prepare texts and metadata for embedding
        texts = [chunk.text for chunk in all_chunks]
        metadata_list = [
            {
                'url': chunk.source_url,
                'chunk_id': chunk.id,
                'position': chunk.position,
                'char_count': chunk.char_count
            }
            for chunk in all_chunks
        ]

        # Step 4: Generate embeddings
        logging.info(f"Generating embeddings for {len(texts)} text chunks")
        embeddings = create_embeddings(texts)
        logging.info(f"Generated {len(embeddings)} embeddings")

        # Step 5: Store embeddings in Qdrant
        logging.info("Storing embeddings in Qdrant")
        store_content_chunks(texts, embeddings, metadata_list, skip_duplicates=skip_duplicates)
        logging.info("Successfully stored embeddings in Qdrant")

        # Step 6: Validation checks
        # Validate that all expected URLs were processed
        all_expected_urls = {url_data['url'] for url_data in sitemap_urls}
        all_processed_urls = set(processed_urls)
        all_failed_urls = set(failed_urls)

        # Calculate unprocessed URLs
        unprocessed_urls = all_expected_urls - all_processed_urls - all_failed_urls

        if unprocessed_urls:
            logging.warning(f"Found {len(unprocessed_urls)} URLs that were not processed: {list(unprocessed_urls)[:5]}...")  # Show first 5
        else:
            logging.info("All URLs from sitemap were processed successfully")

        # Step 7: Report completion
        elapsed_time = time.time() - start_time
        logging.info(f"Ingestion pipeline completed successfully in {elapsed_time:.2f} seconds")
        logging.info(f"Processed {len(newly_processed_urls)} new URLs and stored {len(all_chunks)} content chunks")
        logging.info(f"Total processed URLs: {len(processed_urls)}, Failed URLs: {len(failed_urls)}")

    except Exception as e:
        logging.error(f"Ingestion pipeline failed: {str(e)}", exc_info=True)
        # Save progress even if there's an error
        try:
            save_progress(processed_urls, failed_urls)
        except:
            pass  # If we can't save progress during an error, continue with raising the error
        raise


def main():
    """Main entry point for the ingestion pipeline with command-line arguments."""
    parser = argparse.ArgumentParser(description='RAG Content Ingestion Pipeline')
    parser.add_argument('--sitemap-url', type=str, help='Sitemap URL to process (overrides config)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    parser.add_argument('--skip-duplicates', action='store_true', default=True,
                        help='Skip storing duplicate content (default: True)')
    parser.add_argument('--allow-duplicates', action='store_false', dest='skip_duplicates',
                        help='Allow storing duplicate content')
    parser.add_argument('--resume', action='store_true', default=False,
                        help='Resume from a previous checkpoint')

    args = parser.parse_args()

    # Set logging level based on verbose flag
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    setup_logging()
    run_ingestion_pipeline(args.sitemap_url, args.skip_duplicates, args.resume)


if __name__ == "__main__":
    main()