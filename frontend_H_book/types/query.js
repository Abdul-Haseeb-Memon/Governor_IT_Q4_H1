/**
 * QueryRequest data structure
 * Represents a user query submitted to the RAG system
 */

/**
 * Creates a QueryRequest object
 * @param {string} query - The user's question text
 * @returns {Object} QueryRequest object
 */
export const createQueryRequest = (query) => {
  // Validate query format and length
  if (!query || typeof query !== 'string') {
    throw new Error('Query must be a non-empty string');
  }

  if (query.length < 1 || query.length > 1000) {
    throw new Error('Query must be between 1 and 1000 characters');
  }

  return {
    query: query,
    timestamp: new Date().toISOString()
  };
};

/**
 * Validates a QueryRequest object
 * @param {Object} request - The QueryRequest object to validate
 * @returns {boolean} True if valid, false otherwise
 */
export const validateQueryRequest = (request) => {
  if (!request || typeof request !== 'object') {
    console.error('QueryRequest validation failed: Request is not an object');
    return false;
  }

  if (!request.query || typeof request.query !== 'string') {
    console.error('QueryRequest validation failed: Query is not a valid string');
    return false;
  }

  if (request.query.length < 1 || request.query.length > 1000) {
    console.error('QueryRequest validation failed: Query length is invalid');
    return false;
  }

  return true;
};

/**
 * Sanitizes a QueryRequest object
 * @param {Object} request - The QueryRequest object to sanitize
 * @returns {Object} Sanitized QueryRequest object
 */
export const sanitizeQueryRequest = (request) => {
  if (!request) {
    return null;
  }

  // Remove potentially dangerous characters/sequences
  const sanitizedQuery = request.query
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '') // Remove script tags
    .replace(/javascript:/gi, '') // Remove javascript: protocol
    .replace(/on\w+\s*=/gi, '') // Remove event handlers
    .trim();

  return {
    ...request,
    query: sanitizedQuery
  };
};

export default {
  createQueryRequest,
  validateQueryRequest,
  sanitizeQueryRequest
};