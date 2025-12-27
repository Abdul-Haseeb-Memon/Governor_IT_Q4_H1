import { useState, useEffect } from 'react';
import { validateQueryRequest } from '../types/query';
import { validateAnswerResponse } from '../types/response';

/**
 * Custom hook for managing chat state
 * @returns {Object} Chat state and management functions
 */
const useChatState = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);

  // Initialize session ID
  useEffect(() => {
    if (!sessionId) {
      setSessionId(`session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
    }
  }, [sessionId]);

  /**
   * Add a message to the chat
   * @param {Object} message - The message to add
   */
  const addMessage = (message) => {
    if (!message || !message.content || !message.sender) {
      console.error('Invalid message format:', message);
      return;
    }

    // Validate message structure
    if (message.sender !== 'user' && message.sender !== 'system') {
      console.error('Invalid message sender:', message.sender);
      return;
    }

    setMessages(prevMessages => [
      ...prevMessages,
      {
        id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        ...message,
        timestamp: new Date().toISOString()
      }
    ]);
  };

  /**
   * Add a user message to the chat
   * @param {string} content - The user's message content
   */
  const addUserMessage = (content) => {
    addMessage({
      content,
      sender: 'user'
    });
  };

  /**
   * Add a system message to the chat
   * @param {string} content - The system's message content
   * @param {Array} sources - Source references for the response
   * @param {number} confidence - Confidence score for the response
   */
  const addSystemMessage = (content, sources = [], confidence = 0.5) => {
    addMessage({
      content,
      sender: 'system',
      sources,
      confidence
    });
  };

  /**
   * Clear all messages from the chat
   */
  const clearMessages = () => {
    setMessages([]);
    setError(null);
  };

  /**
   * Process a user query and add to messages
   * @param {string} query - The user's query
   * @returns {Promise<boolean>} True if query was added successfully, false otherwise
   */
  const processQuery = (query) => {
    try {
      // Validate query
      const queryRequest = { query };
      if (!validateQueryRequest(queryRequest)) {
        setError('Invalid query format');
        return false;
      }

      addUserMessage(query);
      return true;
    } catch (err) {
      setError(err.message);
      return false;
    }
  };

  /**
   * Process a system response and add to messages
   * @param {Object} response - The system response
   * @returns {Promise<boolean>} True if response was added successfully, false otherwise
   */
  const processResponse = (response) => {
    try {
      // Validate response
      if (!validateAnswerResponse(response)) {
        setError('Invalid response format from backend');
        return false;
      }

      addSystemMessage(response.answer, response.sources, response.confidence);
      return true;
    } catch (err) {
      setError(err.message);
      return false;
    }
  };

  /**
   * Reset the chat state
   */
  const resetChat = () => {
    setMessages([]);
    setIsLoading(false);
    setError(null);
    setSessionId(`session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
  };

  return {
    messages,
    setMessages,
    isLoading,
    setIsLoading,
    error,
    setError,
    sessionId,
    addMessage,
    addUserMessage,
    addSystemMessage,
    clearMessages,
    processQuery,
    processResponse,
    resetChat
  };
};

export default useChatState;