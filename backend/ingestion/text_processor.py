"""
Text processor module for RAG Content Ingestion Pipeline.

This module handles content extraction from HTML pages and text chunking.
"""
import requests
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging
import time
import re
from dataclasses import dataclass


@dataclass
class ContentChunk:
    """Represents a chunk of content with metadata."""
    id: str
    text: str
    source_url: str
    position: int
    char_count: int


class TextProcessor:
    """Handles content extraction and chunking from web pages."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'RAG-Ingestion-Pipeline/1.0'
        })

    def fetch_html(self, url: str, max_retries: int = 3) -> Optional[str]:
        """
        Fetch HTML content from a URL with retry mechanism.

        Args:
            url: URL to fetch
            max_retries: Maximum number of retry attempts

        Returns:
            HTML content as string or None if failed
        """
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logging.warning(f"Attempt {attempt + 1} failed to fetch {url}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logging.error(f"Failed to fetch {url} after {max_retries} attempts: {e}")
                    return None

    def extract_content(self, html: str, url: str) -> Dict[str, Any]:
        """
        Extract clean content from HTML using BeautifulSoup.

        Args:
            html: Raw HTML content
            url: Source URL for the content

        Returns:
            Dictionary containing extracted content, title, and metadata
        """
        soup = BeautifulSoup(html, 'html.parser')

        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form']):
            element.decompose()

        # Try to find main content area
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main|article')) or soup

        # Extract title
        title = ''
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip()
        else:
            h1_tag = soup.find('h1')
            if h1_tag:
                title = h1_tag.get_text().strip()

        # Extract clean text content
        text_content = main_content.get_text(separator=' ', strip=True)

        # Clean up excessive whitespace
        text_content = re.sub(r'\s+', ' ', text_content)

        # Validate content
        word_count = len(text_content.split())

        return {
            'title': title,
            'content': text_content,
            'word_count': word_count,
            'url': url
        }

    def validate_content(self, content_data: Dict[str, Any]) -> bool:
        """
        Validate extracted content.

        Args:
            content_data: Dictionary containing content data

        Returns:
            True if content is valid, False otherwise
        """
        content = content_data.get('content', '')
        word_count = content_data.get('word_count', 0)

        # Check if content is empty or too short
        if not content or len(content.strip()) == 0:
            logging.warning(f"Content is empty for URL: {content_data.get('url')}")
            return False

        if word_count < 10:
            logging.warning(f"Content has fewer than 10 words ({word_count}) for URL: {content_data.get('url')}")
            return False

        return True

    def chunk_text(self, text: str, source_url: str, max_chunk_size: int = 1200) -> List[ContentChunk]:
        """
        Split text into semantically meaningful chunks ≤ max_chunk_size characters.

        Args:
            text: Text to be chunked
            source_url: Source URL for the text
            max_chunk_size: Maximum size of each chunk in characters

        Returns:
            List of ContentChunk objects
        """
        if len(text) <= max_chunk_size:
            return [ContentChunk(
                id=f"{abs(hash(source_url + '_0'))}",
                text=text,
                source_url=source_url,
                position=0,
                char_count=len(text)
            )]

        chunks = []
        position = 0

        # Split text into sentences using regex
        sentences = re.split(r'[.!?]+', text)

        current_chunk = ""

        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue

            # Add sentence ending back to all sentences except the last one that had one
            original_endings = re.findall(r'[.!?]+', text)
            ending = original_endings[min(i, len(original_endings)-1)] if i < len(original_endings) else '.'

            # Add the ending back to the sentence
            sentence_with_ending = sentence + ending if i < len(sentences) - 1 or ending != '.' else sentence

            # Check if adding this sentence would exceed the limit
            if len(current_chunk) + len(sentence_with_ending) + (1 if current_chunk else 0) <= max_chunk_size:
                if current_chunk:
                    current_chunk += " " + sentence_with_ending
                else:
                    current_chunk = sentence_with_ending
            else:
                # If current chunk is not empty, save it and start a new one
                if current_chunk:
                    chunk_id = f"{abs(hash(source_url + f'_{position}'))}"
                    chunks.append(ContentChunk(
                        id=chunk_id,
                        text=current_chunk.strip(),
                        source_url=source_url,
                        position=position,
                        char_count=len(current_chunk)
                    ))
                    position += 1
                    current_chunk = sentence_with_ending
                else:
                    # If a single sentence is longer than max_chunk_size, split it
                    if len(sentence_with_ending) > max_chunk_size:
                        # Split the long sentence into smaller chunks
                        for sub_chunk in self._split_long_sentence(sentence_with_ending, max_chunk_size):
                            chunk_id = f"{abs(hash(source_url + f'_{position}'))}"
                            chunks.append(ContentChunk(
                                id=chunk_id,
                                text=sub_chunk,
                                source_url=source_url,
                                position=position,
                                char_count=len(sub_chunk)
                            ))
                            position += 1
                    else:
                        current_chunk = sentence_with_ending

        # Add the last chunk if it exists
        if current_chunk:
            chunk_id = f"{abs(hash(source_url + f'_{position}'))}"
            chunks.append(ContentChunk(
                id=chunk_id,
                text=current_chunk.strip(),
                source_url=source_url,
                position=position,
                char_count=len(current_chunk)
            ))

        return chunks

    def _split_long_sentence(self, sentence: str, max_chunk_size: int) -> List[str]:
        """
        Split a sentence that is longer than max_chunk_size into smaller chunks.

        Args:
            sentence: Sentence to split
            max_chunk_size: Maximum size of each chunk

        Returns:
            List of smaller text chunks
        """
        if len(sentence) <= max_chunk_size:
            return [sentence]

        chunks = []
        words = sentence.split()

        current_chunk = ""
        for word in words:
            if len(current_chunk) + len(word) + 1 <= max_chunk_size:
                if current_chunk:
                    current_chunk += " " + word
                else:
                    current_chunk = word
            else:
                if current_chunk:  # If there's content to save
                    chunks.append(current_chunk)
                    current_chunk = word
                else:
                    # If a single word is longer than max_chunk_size, split it
                    if len(word) > max_chunk_size:
                        # Split the long word into smaller pieces
                        for i in range(0, len(word), max_chunk_size):
                            chunks.append(word[i:i + max_chunk_size])
                    else:
                        current_chunk = word

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def process_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Process a single URL to extract content.

        Args:
            url: URL to process

        Returns:
            Dictionary containing extracted content or None if failed
        """
        html = self.fetch_html(url)
        if not html:
            return None

        content_data = self.extract_content(html, url)

        if not self.validate_content(content_data):
            return None

        return content_data


def extract_and_chunk_url(url: str, max_chunk_size: int = 1200) -> Optional[List[ContentChunk]]:
    """
    Convenience function to extract content from a URL and chunk it.

    Args:
        url: URL to process
        max_chunk_size: Maximum size of each chunk in characters

    Returns:
        List of ContentChunk objects or None if failed
    """
    processor = TextProcessor()
    content_data = processor.process_url(url)

    if not content_data:
        return None

    chunks = processor.chunk_text(content_data['content'], url, max_chunk_size)
    return chunks