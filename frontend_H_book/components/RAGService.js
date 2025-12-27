import axios from 'axios';

class RAGService {
  constructor(apiBaseUrl = null) {
    // Initialize with provided URL or leave as null to be configured later
    this.apiBaseUrl = apiBaseUrl || null;

    this.authToken = null; // No authentication token for development
  }

  /**
   * Configure API base URL from environment variables
   */
  configureAPI(apiBaseUrl, authToken = null) {
    this.apiBaseUrl = apiBaseUrl;
    this.authToken = authToken;
    console.log('RAGService configured with API Base URL:', this.apiBaseUrl); // Debug log
  }

  /**
   * Implement retrieve endpoint call
   * @param {string} query - User query text
   * @returns {Promise<Array>} Array of context chunks with source information
   */
  async retrieveContext(query) {
    const startTime = Date.now();
    try {
      const response = await axios.post(`${this.apiBaseUrl}/retrieve`, {
        query: query
      }, {
        headers: {
          'Content-Type': 'application/json',
          ...(this.authToken && { 'Authorization': `Bearer ${this.authToken}` })
        },
        timeout: 30000 // 30 second timeout
      });

      // Validate JSON request/response format compatibility
      if (!response.data || !Array.isArray(response.data)) {
        throw new Error('Invalid response format from retrieve endpoint');
      }

      const responseTime = Date.now() - startTime;
      console.log(`Retrieve context response time: ${responseTime}ms`);

      return response.data;
    } catch (error) {
      // Handle API errors gracefully
      const responseTime = Date.now() - startTime;
      console.error(`Retrieve context error after ${responseTime}ms:`, error);
      throw this.handleError(error);
    }
  }

  /**
   * Implement answer endpoint call
   * @param {string} query - User query text
   * @param {Array} context - Retrieved context chunks
   * @returns {Promise<Object>} AnswerResponse object with answer text and sources
   */
  async generateAnswer(query, context) {
    const startTime = Date.now();
    try {
      const response = await axios.post(`${this.apiBaseUrl}/answer`, {
        query: query,
        context: context || []
      }, {
        headers: {
          'Content-Type': 'application/json',
          ...(this.authToken && { 'Authorization': `Bearer ${this.authToken}` })
        },
        timeout: 30000 // 30 second timeout
      });

      // Validate JSON request/response format compatibility
      if (!response.data || typeof response.data !== 'object') {
        throw new Error('Invalid response format from answer endpoint');
      }

      // Expected response format: { answer: string, sources: array, confidence: number }
      const { answer, sources, confidence } = response.data;

      if (typeof answer !== 'string' || !Array.isArray(sources)) {
        throw new Error('Invalid answer response format');
      }

      const responseTime = Date.now() - startTime;
      console.log(`Generate answer response time: ${responseTime}ms`);

      return {
        answer: answer,
        sources: sources,
        confidence: confidence || 0.5
      };
    } catch (error) {
      // Handle API errors gracefully
      const responseTime = Date.now() - startTime;
      console.error(`Generate answer error after ${responseTime}ms:`, error);
      throw this.handleError(error);
    }
  }

  /**
   * Test API connectivity with backend endpoints
   * @returns {Promise<boolean>} True if API is accessible, false otherwise
   */
  async testConnection() {
    try {
      // Test with a simple ping or health check endpoint if available
      // For now, we'll try to make a simple request to see if the server is reachable
      const response = await axios.get(`${this.apiBaseUrl}/health`, {
        timeout: 30000, // 30 second timeout
        headers: {
          ...(this.authToken && { 'Authorization': `Bearer ${this.authToken}` })
        }
      });

      return response.status >= 200 && response.status < 300;
    } catch (error) {
      console.error('API connectivity test failed:', error);
      return false;
    }
  }

  /**
   * Handle API errors gracefully
   * @param {Error} error - The error object
   * @returns {Error} Formatted error for frontend handling
   */
  handleError(error) {
    // Add request/response logging for debugging
    if (error.response) {
      // Server responded with error status
      console.log('Response data:', error.response.data);
      console.log('Response status:', error.response.status);
      console.log('Response headers:', error.response.headers);

      return new Error(`API Error: ${error.response.status} - ${error.response.data.message || 'Request failed'}`);
    } else if (error.request) {
      // Request was made but no response received
      console.log('Request data:', error.request);
      return new Error('Network Error: No response received from server');
    } else {
      // Something else happened
      return new Error(`Request Error: ${error.message}`);
    }
  }

  /**
   * Implement authentication token handling if required
   * @param {string} token - Authentication token
   */
  setAuthToken(token) {
    this.authToken = token;
  }

  /**
   * Get current API base URL
   * @returns {string} Current API base URL
   */
  getApiBaseUrl() {
    return this.apiBaseUrl;
  }
}

export default RAGService;