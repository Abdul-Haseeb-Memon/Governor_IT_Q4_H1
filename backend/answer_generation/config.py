"""
Configuration module for RAG Answer Generation

Handles environment variable loading and validation for OpenRouter API access.
"""
import os
import logging
from typing import Optional
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Configuration class to manage environment variables and settings
    """

    # Required environment variables
    OPENROUTER_API_KEY: str = os.getenv('OPENROUTER_API_KEY')
    OPENROUTER_BASE_URL: str = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
    OPENROUTER_MODEL: str = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')
    APP_NAME: str = os.getenv('APP_NAME', 'g-house-project')

    # Model parameters for deterministic output
    TEMPERATURE: float = float(os.getenv('OPENROUTER_TEMPERATURE', '0.1'))
    TOP_P: float = float(os.getenv('OPENROUTER_TOP_P', '0.9'))
    MAX_TOKENS: int = int(os.getenv('OPENROUTER_MAX_TOKENS', '1000'))
    PRESENCE_PENALTY: float = float(os.getenv('OPENROUTER_PRESENCE_PENALTY', '0.0'))
    FREQUENCY_PENALTY: float = float(os.getenv('OPENROUTER_FREQUENCY_PENALTY', '0.0'))

    # API request settings
    REQUEST_TIMEOUT: int = int(os.getenv('OPENROUTER_REQUEST_TIMEOUT', '30'))
    MAX_RETRIES: int = int(os.getenv('OPENROUTER_MAX_RETRIES', '3'))

    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')

    @classmethod
    def validate(cls) -> bool:
        """
        Validate that all required environment variables are present

        Returns:
            bool: True if all required variables are present, False otherwise
        """
        required_vars = [
            ('OPENROUTER_API_KEY', cls.OPENROUTER_API_KEY),
            ('OPENROUTER_BASE_URL', cls.OPENROUTER_BASE_URL),
            ('OPENROUTER_MODEL', cls.OPENROUTER_MODEL),
            ('APP_NAME', cls.APP_NAME)
        ]

        missing_vars = []
        for var_name, var_value in required_vars:
            if not var_value or var_value.strip() == '':
                missing_vars.append(var_name)

        if missing_vars:
            logging.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            return False

        # Validate URL format
        if not cls.OPENROUTER_BASE_URL.startswith(('http://', 'https://')):
            logging.error(f"Invalid base URL format: {cls.OPENROUTER_BASE_URL}")
            return False

        # Validate model name format (basic check)
        if '/' not in cls.OPENROUTER_MODEL or len(cls.OPENROUTER_MODEL.split('/')) < 2:
            logging.error(f"Invalid model format: {cls.OPENROUTER_MODEL}")
            return False

        # Validate numeric parameters
        try:
            if not (0.0 <= cls.TEMPERATURE <= 2.0):
                logging.error(f"Invalid temperature value: {cls.TEMPERATURE}")
                return False

            if not (0.0 <= cls.TOP_P <= 1.0):
                logging.error(f"Invalid top_p value: {cls.TOP_P}")
                return False

            if cls.MAX_TOKENS <= 0:
                logging.error(f"Invalid max_tokens value: {cls.MAX_TOKENS}")
                return False

            if cls.REQUEST_TIMEOUT <= 0:
                logging.error(f"Invalid request timeout value: {cls.REQUEST_TIMEOUT}")
                return False

            if cls.MAX_RETRIES < 0:
                logging.error(f"Invalid max_retries value: {cls.MAX_RETRIES}")
                return False
        except (ValueError, TypeError):
            logging.error("Invalid numeric configuration values")
            return False

        logging.info("Configuration validation passed")
        return True

    @classmethod
    def get_headers(cls) -> dict:
        """
        Get headers for OpenRouter API requests

        Returns:
            dict: Headers for API requests
        """
        return {
            'Authorization': f'Bearer {cls.OPENROUTER_API_KEY}',
            'Content-Type': 'application/json',
            'HTTP-Referer': f'https://{cls.APP_NAME}.com',
            'X-Title': cls.APP_NAME
        }

    @classmethod
    def get_model_params(cls) -> dict:
        """
        Get model parameters for OpenRouter API requests

        Returns:
            dict: Model parameters
        """
        return {
            'temperature': cls.TEMPERATURE,
            'top_p': cls.TOP_P,
            'max_tokens': cls.MAX_TOKENS,
            'presence_penalty': cls.PRESENCE_PENALTY,
            'frequency_penalty': cls.FREQUENCY_PENALTY
        }


# Initialize logging with the configured level
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO))
logger = logging.getLogger(__name__)


def load_config() -> Config:
    """
    Load and validate configuration

    Returns:
        Config: Validated configuration object
    """
    if not Config.validate():
        error_msg = "Configuration validation failed"
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info("Configuration loaded and validated successfully")
    return Config


# Example usage and testing
if __name__ == "__main__":
    try:
        config = load_config()
        print("Configuration loaded successfully:")
        print(f"  Model: {config.OPENROUTER_MODEL}")
        print(f"  Base URL: {config.OPENROUTER_BASE_URL}")
        print(f"  Temperature: {config.TEMPERATURE}")
        print(f"  Max Tokens: {config.MAX_TOKENS}")
    except ValueError as e:
        print(f"Configuration error: {e}")