/**
 * Error handling utilities for the RAG chatbot frontend
 */

/**
 * Format error messages for user display
 * @param {Error} error - The error object
 * @returns {string} Formatted error message for user display
 */
export const formatUserErrorMessage = (error) => {
  if (error.response) {
    // Server responded with error status
    switch (error.response.status) {
      case 400:
        return 'Bad request: Please check your input and try again.';
      case 401:
        return 'Unauthorized: Please check your authentication credentials.';
      case 403:
        return 'Forbidden: You do not have permission to access this resource.';
      case 404:
        return 'Not found: The requested resource could not be found.';
      case 429:
        return 'Rate limited: Too many requests. Please try again later.';
      case 500:
        return 'Server error: An internal server error occurred. Please try again later.';
      case 502:
        return 'Gateway error: The server received an invalid response. Please try again.';
      case 503:
        return 'Service unavailable: The service is temporarily unavailable. Please try again later.';
      case 504:
        return 'Gateway timeout: The server did not respond in time. Please try again.';
      default:
        return `Error ${error.response.status}: ${error.response.data?.message || 'Request failed'}`;
    }
  } else if (error.request) {
    // Request was made but no response received
    return 'Network error: Unable to connect to the server. Please check your connection.';
  } else {
    // Something else happened
    return `Request error: ${error.message}`;
  }
};

/**
 * Log error for debugging purposes
 * @param {Error} error - The error object
 * @param {string} context - Context where the error occurred
 */
export const logError = (error, context = '') => {
  console.error(`[ERROR] ${context ? context + ' - ' : ''}`, {
    message: error.message,
    stack: error.stack,
    ...(error.response && {
      responseStatus: error.response.status,
      responseData: error.response.data,
      responseHeaders: error.response.headers,
    }),
    ...(error.request && {
      request: error.request,
    }),
  });
};

/**
 * Validate response format meets requirements
 * @param {any} response - The response to validate
 * @param {string} responseType - Type of response to validate (e.g., 'answer', 'context')
 * @returns {boolean} True if response format is valid, false otherwise
 */
export const validateResponseFormat = (response, responseType) => {
  if (!response) {
    console.error(`Invalid ${responseType} response: Response is null or undefined`);
    return false;
  }

  try {
    switch (responseType) {
      case 'answer':
        // Validate AnswerResponse format: { answer: string, sources: array, confidence?: number }
        if (typeof response !== 'object') {
          console.error('Invalid answer response: Response is not an object');
          return false;
        }
        if (typeof response.answer !== 'string') {
          console.error('Invalid answer response: Answer is not a string');
          return false;
        }
        if (!Array.isArray(response.sources)) {
          console.error('Invalid answer response: Sources is not an array');
          return false;
        }
        if (response.confidence !== undefined && typeof response.confidence !== 'number') {
          console.error('Invalid answer response: Confidence is not a number');
          return false;
        }
        return true;

      case 'context':
        // Validate context response: Array of context chunks
        if (!Array.isArray(response)) {
          console.error('Invalid context response: Response is not an array');
          return false;
        }
        // Check that each item in the array has required properties
        for (let i = 0; i < response.length; i++) {
          const item = response[i];
          if (typeof item !== 'object') {
            console.error(`Invalid context response: Item ${i} is not an object`);
            return false;
          }
        }
        return true;

      default:
        console.warn(`Unknown response type: ${responseType}`);
        return true; // Don't validate unknown response types
    }
  } catch (error) {
    console.error(`Error validating ${responseType} response format:`, error);
    return false;
  }
};

/**
 * Sanitize user input to prevent XSS
 * @param {string} input - User input to sanitize
 * @returns {string} Sanitized input
 */
export const sanitizeInput = (input) => {
  if (typeof input !== 'string') {
    return '';
  }

  // Remove potentially dangerous characters/sequences
  return input
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '') // Remove script tags
    .replace(/javascript:/gi, '') // Remove javascript: protocol
    .replace(/on\w+\s*=/gi, '') // Remove event handlers
    .trim();
};

/**
 * Validate query input format and length
 * @param {string} query - Query to validate
 * @returns {object} Validation result with isValid boolean and error message
 */
export const validateQuery = (query) => {
  if (!query || typeof query !== 'string') {
    return {
      isValid: false,
      error: 'Query is required and must be a string'
    };
  }

  // Check if query is empty after trimming
  if (!query.trim()) {
    return {
      isValid: false,
      error: 'Query cannot be empty'
    };
  }

  // Validate query length (1-1000 characters)
  if (query.length < 1 || query.length > 1000) {
    return {
      isValid: false,
      error: 'Query must be between 1 and 1000 characters'
    };
  }

  return {
    isValid: true,
    error: null
  };
};

/**
 * Implement response error handling
 * @param {Error} error - The error to handle
 * @param {Function} setError - Function to set error state
 * @param {string} context - Context for the error
 */
export const handleResponseError = (error, setError, context = '') => {
  // Log error for debugging
  logError(error, context);

  // Format error for user display
  const userErrorMessage = formatUserErrorMessage(error);

  // Set error state if setError function is provided
  if (setError && typeof setError === 'function') {
    setError(userErrorMessage);
  }

  // Return formatted error message
  return userErrorMessage;
};

export default {
  formatUserErrorMessage,
  logError,
  validateResponseFormat,
  sanitizeInput,
  validateQuery,
  handleResponseError
};