import React, { useCallback, useEffect } from 'react';
import ChatInput from './ChatInput';
import ChatDisplay from './ChatDisplay';
import useChatState from './useChatState';
import RAGService from './RAGService';
import config from '../src/utils/config';

// Debounce function to limit API calls
const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

const ChatInterface = () => {
  const ragService = new RAGService();

  // Configure the RAG service with the environment variable when component mounts
  useEffect(() => {
    // Get the API base URL from the config file
    const apiBaseUrl = config.API_BASE_URL;

    // Configure the RAG service with the proper API base URL
    ragService.configureAPI(apiBaseUrl);
  }, []);
  const {
    messages,
    isLoading,
    error,
    setIsLoading,
    setError,
    processQuery,
    addSystemMessage,
    clearMessages
  } = useChatState();

  const handleSubmit = async (query) => {
    if (!processQuery(query)) {
      return; // Query validation failed
    }

    setIsLoading(true);
    setError(null);

    try {
      // Retrieve context from backend
      const context = await ragService.retrieveContext(query);

      // Generate answer based on query and context
      const answerResponse = await ragService.generateAnswer(query, context);

      // Add system response to chat
      addSystemMessage(answerResponse.answer, answerResponse.sources, answerResponse.confidence);
    } catch (err) {
      setError(err.message);
      console.error('Error processing query:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Debounced version of handleSubmit to optimize API calls
  const debouncedHandleSubmit = useCallback(
    debounce((query) => handleSubmit(query), 300),
    [handleSubmit]
  );

  return (
    <div className="chat-interface" role="main" aria-label="RAG Chat Interface">
      <div className="chat-header">
        <h2 tabIndex="0">RAG Chat Interface</h2>
        <button
          onClick={clearMessages}
          className="clear-button"
          aria-label="Clear all chat messages"
          title="Clear Chat"
        >
          Clear Chat
        </button>
      </div>

      {error && (
        <div className="error-message" role="alert" tabIndex="0" aria-live="polite">
          Error: {error}
        </div>
      )}

      <div className="chat-area" tabIndex="0" aria-label="Chat messages area">
        <ChatDisplay messages={messages} />
      </div>

      <div className="input-area" tabIndex="0" aria-label="Chat input area">
        <ChatInput onSubmit={handleSubmit} isLoading={isLoading} />
      </div>

      <style jsx>{`
        .chat-interface {
          display: flex;
          flex-direction: column;
          max-width: 100%;
          width: 100%;
          height: 80vh;
          min-height: 500px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
          background: linear-gradient(135deg, var(--ifm-color-gray-100) 0%, var(--ifm-color-gray-200) 100%);
          border-radius: 20px;
          padding: 1.5rem;
          box-shadow: var(--ifm-shadow-xl);
          background-color: var(--ifm-background-surface-color);
          overflow: hidden;
          position: relative;
        }

        .chat-interface::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 4px;
          background: linear-gradient(90deg, var(--ifm-color-primary), var(--ifm-color-primary-light), var(--ifm-color-primary));
          background-size: 200% 200%;
          animation: gradient 3s ease infinite;
        }

        @keyframes gradient {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }

        .chat-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1.5rem;
          padding-bottom: 1rem;
          border-bottom: 2px solid var(--ifm-border-color);
          position: relative;
        }

        .chat-header::after {
          content: '';
          position: absolute;
          bottom: -2px;
          left: 0;
          right: 0;
          height: 2px;
          background: linear-gradient(90deg, transparent, var(--ifm-color-primary), transparent);
        }

        h2 {
          margin: 0;
          color: var(--ifm-text-color);
          font-size: 1.75rem;
          font-weight: 700;
          background: linear-gradient(135deg, var(--ifm-color-primary), var(--ifm-color-primary-dark));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .clear-button {
          padding: 0.75rem 1.5rem;
          background: linear-gradient(135deg, #dc3545, #c82333);
          color: white;
          border: none;
          border-radius: 25px;
          cursor: pointer;
          font-size: 0.9rem;
          font-weight: 600;
          transition: all 0.3s ease;
          box-shadow: var(--ifm-shadow-md);
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .clear-button:hover {
          transform: translateY(-2px);
          box-shadow: var(--ifm-shadow-lg);
          background: linear-gradient(135deg, #c82333, #b2212f);
        }

        .clear-button:active {
          transform: translateY(0);
        }

        .error-message {
          background: linear-gradient(135deg, #f8d7da, #f1c1c6);
          color: #721c24;
          padding: 1rem 1.25rem;
          border-radius: 12px;
          margin-bottom: 1.25rem;
          font-size: 0.95rem;
          margin-top: 0.75rem;
          border-left: 4px solid #dc3545;
          box-shadow: var(--ifm-shadow-sm);
        }

        .chat-area {
          flex: 1;
          margin-bottom: 1.5rem;
          overflow: hidden;
          border-radius: 16px;
          background: var(--ifm-background-color);
          box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .input-area {
          margin-top: auto;
          background: rgba(255, 255, 255, 0.9);
          backdrop-filter: blur(10px);
          border-radius: 16px;
          padding: 1rem;
          box-shadow: var(--ifm-shadow-lg);
        }

        .chat-area:focus,
        .input-area:focus {
          outline: 2px solid var(--ifm-color-primary);
        }

        /* Responsive design */
        @media (max-width: 768px) {
          .chat-interface {
            height: 85vh;
            min-height: 450px;
            padding: 1rem;
            margin: 0.5rem;
            border-radius: 16px;
          }

          .chat-header {
            margin-bottom: 1.25rem;
            padding-bottom: 0.75rem;
            flex-direction: column;
            align-items: stretch;
            gap: 1rem;
          }

          h2 {
            font-size: 1.5rem;
            text-align: center;
          }

          .clear-button {
            align-self: center;
            padding: 0.6rem 1.2rem;
            font-size: 0.85rem;
          }

          .error-message {
            font-size: 0.9rem;
            padding: 0.875rem;
          }

          .input-area {
            padding: 0.875rem;
            margin-top: 1rem;
          }
        }

        @media (max-width: 480px) {
          .chat-interface {
            height: 90vh;
            min-height: 400px;
            padding: 0.75rem;
            margin: 0.25rem;
            border-radius: 12px;
          }

          .chat-header {
            gap: 0.75rem;
          }

          h2 {
            font-size: 1.35rem;
          }

          .clear-button {
            padding: 0.5rem 1rem;
            font-size: 0.8rem;
          }
        }
      `}</style>
    </div>
  );
};


export default ChatInterface;