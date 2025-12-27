"""
Sitemap loader module for RAG Content Ingestion Pipeline.

This module handles fetching and parsing sitemap.xml files to extract URLs.
"""
import requests
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET
import logging


class SitemapLoader:
    """Handles loading and parsing sitemap files."""

    def __init__(self, sitemap_url: str):
        """
        Initialize the sitemap loader.

        Args:
            sitemap_url: URL of the sitemap.xml file
        """
        self.sitemap_url = sitemap_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'RAG-Ingestion-Pipeline/1.0'
        })

    def fetch_sitemap(self) -> str:
        """
        Fetch the sitemap content from the URL.

        Returns:
            The raw XML content of the sitemap

        Raises:
            requests.RequestException: If the sitemap cannot be fetched
        """
        try:
            response = self.session.get(self.sitemap_url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Failed to fetch sitemap from {self.sitemap_url}: {e}")
            raise

    def parse_sitemap(self, xml_content: str) -> List[Dict[str, Any]]:
        """
        Parse the sitemap XML content and extract URLs.

        Args:
            xml_content: Raw XML content of the sitemap

        Returns:
            List of dictionaries containing URL information
        """
        try:
            root = ET.fromstring(xml_content)

            # Define namespaces for parsing
            namespaces = {
                'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9',
                'xhtml': 'http://www.w3.org/1999/xhtml'
            }

            # Check if this is a sitemap index (contains other sitemaps)
            sitemap_elements = root.findall('.//sitemap:url', namespaces)

            if not sitemap_elements:
                # This might be a sitemap index file
                sitemap_index_elements = root.findall('.//sitemap:sitemap', namespaces)
                if sitemap_index_elements:
                    return self._parse_sitemap_index(xml_content)

            # Parse regular sitemap
            urls = []
            for url_element in root.findall('.//sitemap:url', namespaces):
                url_data = {
                    'url': '',
                    'last_modified': None,
                    'change_frequency': None,
                    'priority': None
                }

                loc_element = url_element.find('sitemap:loc', namespaces)
                if loc_element is not None:
                    url_data['url'] = loc_element.text.strip()

                lastmod_element = url_element.find('sitemap:lastmod', namespaces)
                if lastmod_element is not None:
                    url_data['last_modified'] = lastmod_element.text.strip()

                changefreq_element = url_element.find('sitemap:changefreq', namespaces)
                if changefreq_element is not None:
                    url_data['change_frequency'] = changefreq_element.text.strip()

                priority_element = url_element.find('sitemap:priority', namespaces)
                if priority_element is not None:
                    try:
                        url_data['priority'] = float(priority_element.text.strip())
                    except ValueError:
                        pass  # Invalid priority value, leave as None

                if url_data['url']:  # Only add if URL is present
                    urls.append(url_data)

            return urls

        except ET.ParseError as e:
            logging.error(f"Failed to parse sitemap XML: {e}")
            raise ValueError(f"Invalid sitemap XML: {e}")

    def _parse_sitemap_index(self, xml_content: str) -> List[Dict[str, Any]]:
        """
        Parse a sitemap index file that contains references to other sitemaps.

        Args:
            xml_content: Raw XML content of the sitemap index

        Returns:
            List of dictionaries containing URL information
        """
        namespaces = {
            'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'
        }

        root = ET.fromstring(xml_content)
        urls = []

        # Get all sitemap references
        for sitemap_element in root.findall('.//sitemap:sitemap', namespaces):
            loc_element = sitemap_element.find('sitemap:loc', namespaces)
            if loc_element is not None:
                sitemap_url = loc_element.text.strip()
                # Fetch and parse the referenced sitemap
                try:
                    sitemap_content = self._fetch_sitemap_content(sitemap_url)
                    sub_urls = self.parse_sitemap(sitemap_content)
                    urls.extend(sub_urls)
                except Exception as e:
                    logging.warning(f"Failed to process referenced sitemap {sitemap_url}: {e}")

        return urls

    def _fetch_sitemap_content(self, sitemap_url: str) -> str:
        """
        Fetch content of a specific sitemap URL.

        Args:
            sitemap_url: URL of the sitemap to fetch

        Returns:
            Raw XML content of the sitemap
        """
        try:
            response = self.session.get(sitemap_url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Failed to fetch sitemap from {sitemap_url}: {e}")
            raise

    def get_urls(self) -> List[Dict[str, Any]]:
        """
        Get all URLs from the sitemap.

        Returns:
            List of dictionaries containing URL information
        """
        xml_content = self.fetch_sitemap()
        return self.parse_sitemap(xml_content)


def load_sitemap_urls(sitemap_url: str) -> List[Dict[str, Any]]:
    """
    Convenience function to load URLs from a sitemap.

    Args:
        sitemap_url: URL of the sitemap.xml file

    Returns:
        List of dictionaries containing URL information
    """
    loader = SitemapLoader(sitemap_url)
    return loader.get_urls()