/**
 * AnswerResponse data structure
 * Represents the final answer received from the RAG system
 */

/**
 * Creates an AnswerResponse object
 * @param {string} answer - The generated answer text from the backend
 * @param {Array<string>} sources - List of source URLs for the information in the answer
 * @param {number} confidence - Confidence score for the answer quality (0.0 to 1.0)
 * @returns {Object} AnswerResponse object
 */
export const createAnswerResponse = (answer, sources = [], confidence = 0.5) => {
  // Validate answer text
  if (!answer || typeof answer !== 'string') {
    throw new Error('Answer must be a non-empty string');
  }

  if (answer.length === 0) {
    throw new Error('Answer text must not be empty');
  }

  // Validate sources
  if (!Array.isArray(sources)) {
    throw new Error('Sources must be an array of URLs');
  }

  // Validate each source URL
  for (const source of sources) {
    if (typeof source !== 'string') {
      throw new Error('Each source must be a string URL');
    }
    try {
      new URL(source); // Validate URL format
    } catch (e) {
      throw new Error(`Invalid source URL: ${source}`);
    }
  }

  // Validate confidence score
  if (typeof confidence !== 'number' || confidence < 0.0 || confidence > 1.0) {
    throw new Error('Confidence must be a number between 0.0 and 1.0');
  }

  return {
    answer: answer,
    sources: sources,
    confidence: confidence,
    timestamp: new Date().toISOString()
  };
};

/**
 * Validates an AnswerResponse object
 * @param {Object} response - The AnswerResponse object to validate
 * @returns {boolean} True if valid, false otherwise
 */
export const validateAnswerResponse = (response) => {
  if (!response || typeof response !== 'object') {
    console.error('AnswerResponse validation failed: Response is not an object');
    return false;
  }

  if (!response.answer || typeof response.answer !== 'string' || response.answer.length === 0) {
    console.error('AnswerResponse validation failed: Answer is not a valid non-empty string');
    return false;
  }

  if (response.sources !== undefined && !Array.isArray(response.sources)) {
    console.error('AnswerResponse validation failed: Sources is not an array');
    return false;
  }

  if (response.confidence !== undefined && (typeof response.confidence !== 'number' || response.confidence < 0.0 || response.confidence > 1.0)) {
    console.error('AnswerResponse validation failed: Confidence is not a number between 0.0 and 1.0');
    return false;
  }

  // Validate each source URL if sources exist
  if (response.sources) {
    for (const source of response.sources) {
      if (typeof source !== 'string') {
        console.error('AnswerResponse validation failed: Each source must be a string URL');
        return false;
      }
      try {
        new URL(source); // Validate URL format
      } catch (e) {
        console.error(`AnswerResponse validation failed: Invalid source URL: ${source}`);
        return false;
      }
    }
  }

  return true;
};

/**
 * Sanitizes an AnswerResponse object
 * @param {Object} response - The AnswerResponse object to sanitize
 * @returns {Object} Sanitized AnswerResponse object
 */
export const sanitizeAnswerResponse = (response) => {
  if (!response) {
    return null;
  }

  // Sanitize answer text
  let sanitizedAnswer = response.answer || '';
  if (typeof sanitizedAnswer === 'string') {
    // Remove potentially dangerous content
    sanitizedAnswer = sanitizedAnswer
      .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '') // Remove script tags
      .replace(/javascript:/gi, '') // Remove javascript: protocol
      .replace(/on\w+\s*=/gi, '') // Remove event handlers
      .trim();
  }

  // Sanitize sources
  let sanitizedSources = response.sources || [];
  if (Array.isArray(sanitizedSources)) {
    sanitizedSources = sanitizedSources
      .filter(source => typeof source === 'string') // Only keep string sources
      .map(source => source.trim()) // Trim whitespace
      .filter(source => {
        try {
          new URL(source); // Validate URL format
          return true;
        } catch (e) {
          return false; // Remove invalid URLs
        }
      });
  }

  // Validate confidence
  let sanitizedConfidence = response.confidence !== undefined ? response.confidence : 0.5;
  if (typeof sanitizedConfidence !== 'number' || sanitizedConfidence < 0.0 || sanitizedConfidence > 1.0) {
    sanitizedConfidence = 0.5; // Default to 0.5 if invalid
  }

  return {
    ...response,
    answer: sanitizedAnswer,
    sources: sanitizedSources,
    confidence: sanitizedConfidence
  };
};

/**
 * Creates a fallback response when content is not covered
 * @param {string} fallbackMessage - The fallback message to use
 * @returns {Object} AnswerResponse object with fallback content
 */
export const createFallbackResponse = (fallbackMessage = "The information requested is not covered in the book.") => {
  return createAnswerResponse(fallbackMessage, [], 0.0);
};

export default {
  createAnswerResponse,
  validateAnswerResponse,
  sanitizeAnswerResponse,
  createFallbackResponse
};