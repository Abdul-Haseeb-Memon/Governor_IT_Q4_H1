"""
OpenRouter Client Module for RAG Answer Generation

This module handles communication with the OpenRouter API for
language model inference, including request formatting, response
processing, and error handling.
"""
import requests
import time
import logging
from typing import Dict, Any, Optional
from .config import Config


logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Simple rate limiter to control API call frequency
    """
    def __init__(self, max_calls: int = 10, time_window: int = 60):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []

    def wait_if_needed(self):
        """Wait if we're making calls too fast"""
        now = time.time()
        # Remove calls that are outside the time window
        self.calls = [call_time for call_time in self.calls if now - call_time < self.time_window]

        if len(self.calls) >= self.max_calls:
            # Wait until we're under the limit
            sleep_time = self.time_window - (now - self.calls[0])
            if sleep_time > 0:
                logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
                time.sleep(sleep_time)
                # Update calls list after sleeping
                now = time.time()
                self.calls = [call_time for call_time in self.calls if now - call_time < self.time_window]

        self.calls.append(now)


class CircuitBreaker:
    """
    Circuit breaker pattern implementation to handle API failures gracefully
    """
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self._state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN

    @property
    def state(self):
        if self._state == 'OPEN' and self.last_failure_time:
            # Check if recovery timeout has passed
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self._state = 'HALF_OPEN'
        return self._state

    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            raise Exception("Circuit breaker is OPEN - API calls temporarily disabled")
        elif self.state == 'HALF_OPEN':
            # Try to make the call, if it fails, go back to OPEN
            try:
                result = func(*args, **kwargs)
                # Success, close the circuit
                self._state = 'CLOSED'
                self.failure_count = 0
                return result
            except Exception:
                # Failure, open the circuit again
                self._open_circuit()
                raise
        else:  # CLOSED
            try:
                result = func(*args, **kwargs)
                return result
            except Exception:
                self.failure_count += 1
                if self.failure_count >= self.failure_threshold:
                    self._open_circuit()
                raise

    def _open_circuit(self):
        self._state = 'OPEN'
        self.last_failure_time = time.time()

    def reset(self):
        self._state = 'CLOSED'
        self.failure_count = 0
        self.last_failure_time = None


class OpenRouterClient:
    """
    Client for interacting with OpenRouter API
    """

    def __init__(self):
        """Initialize the OpenRouter client with configuration"""
        self.config = Config
        self.base_url = self.config.OPENROUTER_BASE_URL
        self.headers = self.config.get_headers()
        self.model_params = self.config.get_model_params()
        self.session = requests.Session()
        # Initialize circuit breaker with default threshold of 5 failures, 60 seconds timeout
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=self.config.MAX_RETRIES + 2,  # Slightly higher than retry count
            recovery_timeout=60  # 1 minute recovery timeout
        )
        # Initialize rate limiter - default to 10 calls per minute
        self.rate_limiter = RateLimiter(
            max_calls=10,  # Default rate limiting
            time_window=60
        )

    def _make_request(self, prompt: str) -> Optional[str]:
        """
        Internal method to make the actual request to OpenRouter API
        This method is wrapped by the circuit breaker
        """
        # Apply rate limiting before making the request
        self.rate_limiter.wait_if_needed()

        # Prepare the payload for OpenRouter API
        payload = {
            "model": self.config.OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            **self.model_params
        }

        # Add additional parameters that might be needed
        payload["temperature"] = self.config.TEMPERATURE
        payload["top_p"] = self.config.TOP_P
        payload["max_tokens"] = self.config.MAX_TOKENS

        logger.info(f"Sending request to OpenRouter API with model: {self.config.OPENROUTER_MODEL}")

        for attempt in range(self.config.MAX_RETRIES):
            try:
                response = self.session.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=self.config.REQUEST_TIMEOUT
                )

                # Check if the request was successful
                if response.status_code == 200:
                    response_data = response.json()
                    if 'choices' in response_data and len(response_data['choices']) > 0:
                        answer_text = response_data['choices'][0]['message']['content']
                        logger.info("Successfully received response from OpenRouter API")
                        return answer_text
                    else:
                        logger.error("No choices returned in OpenRouter response")
                        # Return a safe fallback if API returns unexpected response
                        if attempt < self.config.MAX_RETRIES - 1:
                            logger.info(f"Retrying request (attempt {attempt + 1}/{self.config.MAX_RETRIES})")
                            time.sleep(2 ** attempt)  # Exponential backoff
                            continue
                        return None
                elif response.status_code == 429:
                    # Rate limit error - wait before retrying
                    wait_time = (2 ** attempt) * 1  # Exponential backoff
                    logger.warning(f"Rate limited by OpenRouter. Waiting {wait_time}s before retry {attempt + 1}/{self.config.MAX_RETRIES}")
                    time.sleep(wait_time)
                elif response.status_code == 401:
                    logger.error("Unauthorized: Check your OpenRouter API key")
                    # Don't retry if it's an auth error
                    return None
                elif response.status_code == 400:
                    logger.error(f"Bad request to OpenRouter: {response.text}")
                    # Don't retry if it's a bad request
                    return None
                elif response.status_code == 403:
                    logger.error(f"Forbidden request to OpenRouter: {response.text}")
                    # Don't retry if it's a forbidden request
                    return None
                elif response.status_code == 404:
                    logger.error(f"OpenRouter endpoint not found: {response.text}")
                    # Don't retry if it's a 404 error
                    return None
                elif response.status_code >= 500:
                    logger.error(f"Server error from OpenRouter: {response.status_code}, response: {response.text}")
                    # Retry for server errors
                    if attempt < self.config.MAX_RETRIES - 1:
                        wait_time = (2 ** attempt) * 1  # Exponential backoff
                        logger.info(f"Retrying after server error (attempt {attempt + 1}/{self.config.MAX_RETRIES}) - waiting {wait_time}s")
                        time.sleep(wait_time)
                    else:
                        return None
                else:
                    logger.error(f"Unexpected status code from OpenRouter: {response.status_code}, response: {response.text}")
                    # For other errors, retry up to max_retries
                    if attempt < self.config.MAX_RETRIES - 1:
                        wait_time = (2 ** attempt) * 1  # Exponential backoff
                        logger.info(f"Retrying after unexpected status (attempt {attempt + 1}/{self.config.MAX_RETRIES}) - waiting {wait_time}s")
                        time.sleep(wait_time)
                    else:
                        return None

            except requests.exceptions.Timeout:
                logger.error(f"Request to OpenRouter timed out (attempt {attempt + 1}/{self.config.MAX_RETRIES})")
                if attempt == self.config.MAX_RETRIES - 1:
                    return None
                time.sleep(2 ** attempt)  # Exponential backoff
            except requests.exceptions.ConnectionError:
                logger.error(f"Connection error to OpenRouter (attempt {attempt + 1}/{self.config.MAX_RETRIES})")
                if attempt == self.config.MAX_RETRIES - 1:
                    return None
                time.sleep(2 ** attempt)  # Exponential backoff
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error to OpenRouter: {str(e)} (attempt {attempt + 1}/{self.config.MAX_RETRIES})")
                if attempt == self.config.MAX_RETRIES - 1:
                    return None
                time.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                logger.error(f"Unexpected error during OpenRouter request: {str(e)} (attempt {attempt + 1}/{self.config.MAX_RETRIES})")
                if attempt == self.config.MAX_RETRIES - 1:
                    return None
                time.sleep(2 ** attempt)  # Exponential backoff

        logger.error("Max retries exceeded for OpenRouter API request")
        return None

    def send_request(self, prompt: str) -> Optional[str]:
        """
        Send a request to OpenRouter API and return the response text

        Args:
            prompt: Formatted prompt to send to the model

        Returns:
            Response text from the model or None if request fails
        """
        try:
            # Use the circuit breaker to wrap the actual request
            return self.circuit_breaker.call(self._make_request, prompt)
        except Exception as e:
            logger.error(f"Circuit breaker prevented API call or request failed: {str(e)}")
            # Return a safe fallback when circuit breaker is open or request fails
            return None

    def test_connection(self) -> bool:
        """
        Test the connection to OpenRouter API

        Returns:
            Boolean indicating if connection is successful
        """
        try:
            # Send a simple test request
            test_prompt = "Hello, are you available?"
            response = self.send_request(test_prompt)
            return response is not None and len(response) > 0
        except Exception as e:
            logger.error(f"Connection test to OpenRouter failed: {str(e)}")
            return False


def call_openrouter_api(prompt: str) -> Optional[str]:
    """
    Convenience function to call OpenRouter API with a prompt

    Args:
        prompt: Formatted prompt to send to the model

    Returns:
        Response text from the model or None if request fails
    """
    client = OpenRouterClient()
    return client.send_request(prompt)


# Example usage and testing
if __name__ == "__main__":
    # Test the OpenRouter client
    client = OpenRouterClient()

    # Test connection
    is_connected = client.test_connection()
    print(f"OpenRouter connection test: {'PASSED' if is_connected else 'FAILED'}")

    if is_connected:
        # Test with a sample prompt
        sample_prompt = """Context:
The system provides comprehensive RAG functionality. Key features include context retrieval and answer generation. The system ensures answers are grounded in provided context.

Question: What are the key features?

Instructions: Answer the question using ONLY the provided context. Do not use any prior knowledge or information not present in the context. If the context does not contain sufficient information to answer the question, respond with "I cannot answer this question based on the provided context." Ensure your answer is directly supported by the information in the context section above."""

        response = client.send_request(sample_prompt)
        print(f"Sample response: {response}")
    else:
        print("Skipping sample request due to connection failure")