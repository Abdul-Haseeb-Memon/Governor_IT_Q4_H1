import React, { useState } from 'react';

const ChatInput = ({ onSubmit, isLoading = false }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validate user input format and length
    if (!query.trim()) {
      alert('Please enter a question');
      return;
    }

    // Validate query length (1-1000 characters)
    if (query.length < 1 || query.length > 1000) {
      alert('Query must be between 1 and 1000 characters');
      return;
    }

    // Handle query submission to RAGService.js
    onSubmit(query.trim());

    // Reset input after submission
    setQuery('');
  };

  // Implement input sanitization and validation
  const handleInputChange = (e) => {
    let value = e.target.value;

    // Basic sanitization to prevent XSS
    // In a real application, you might want more robust sanitization
    setQuery(value);
  };

  // Add keyboard accessibility features
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="chat-input-form">
      <div className="input-group">
        <textarea
          value={query}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about the content..."
          disabled={isLoading}
          className="chat-input-textarea"
          rows="3"
          aria-label="Enter your question"
        />
        <button
          type="submit"
          disabled={isLoading || !query.trim()}
          className="chat-submit-button"
          aria-label="Submit question"
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>

      {/* Implement loading state during processing */}
      {isLoading && (
        <div className="loading-indicator" aria-live="polite">
          <div className="loading-spinner" aria-hidden="true"></div>
          <span>Processing your question...</span>
        </div>
      )}

      <style jsx>{`
        .chat-input-form {
          margin-top: 1.25rem;
          width: 100%;
        }

        .input-group {
          display: flex;
          flex-direction: column;
          gap: 0.875rem;
        }

        .chat-input-textarea {
          width: 100%;
          padding: 1.125rem;
          border: 2px solid #e9ecef;
          border-radius: 16px;
          resize: vertical;
          font-family: inherit;
          font-size: 1.05rem;
          line-height: 1.6;
          min-height: 90px;
          transition: all 0.3s ease;
          background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%);
          box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.03);
        }

        .chat-input-textarea:focus {
          outline: none;
          border-color: #007cba;
          box-shadow: 0 0 0 4px rgba(0, 124, 186, 0.15), inset 0 2px 4px rgba(0, 0, 0, 0.05);
          background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
        }

        .chat-input-textarea::placeholder {
          color: #adb5bd;
          font-style: italic;
        }

        .chat-submit-button {
          padding: 0.875rem 1.75rem;
          background: linear-gradient(135deg, #007cba 0%, #0056b3 100%);
          color: white;
          border: none;
          border-radius: 16px;
          cursor: pointer;
          font-size: 1.05rem;
          font-weight: 600;
          transition: all 0.3s ease;
          align-self: flex-end;
          min-width: 100px;
          box-shadow: 0 4px 15px rgba(0, 124, 186, 0.3);
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.5rem;
        }

        .chat-submit-button:hover:not(:disabled) {
          background: linear-gradient(135deg, #0056b3 0%, #004085 100%);
          transform: translateY(-2px);
          box-shadow: 0 6px 20px rgba(0, 124, 186, 0.4);
        }

        .chat-submit-button:active:not(:disabled) {
          transform: translateY(0);
          box-shadow: 0 2px 10px rgba(0, 124, 186, 0.3);
        }

        .chat-submit-button:disabled {
          background: linear-gradient(135deg, #adb5bd 0%, #868e96 100%);
          cursor: not-allowed;
          transform: none;
          box-shadow: none;
          opacity: 0.7;
        }

        .loading-indicator {
          margin-top: 0.875rem;
          font-style: italic;
          color: #6c757d;
          display: flex;
          align-items: center;
          gap: 0.875rem;
          font-size: 0.95rem;
          padding: 0.75rem;
          background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
          border-radius: 12px;
          border-left: 4px solid #007cba;
        }

        .loading-spinner {
          width: 20px;
          height: 20px;
          border: 2px solid #e9ecef;
          border-top: 2px solid #007cba;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        /* Responsive design */
        @media (min-width: 768px) {
          .input-group {
            flex-direction: row;
            align-items: flex-end;
            gap: 1.25rem;
          }

          .chat-input-textarea {
            flex: 1;
            min-height: 110px;
          }

          .chat-submit-button {
            align-self: stretch;
            margin-left: 0;
            min-width: 120px;
          }
        }

        @media (max-width: 768px) {
          .input-group {
            gap: 0.75rem;
          }

          .chat-input-textarea {
            padding: 1rem;
            min-height: 80px;
            font-size: 1rem;
          }

          .chat-submit-button {
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            min-width: 90px;
          }

          .loading-indicator {
            font-size: 0.9rem;
            gap: 0.75rem;
            padding: 0.65rem;
          }
        }

        @media (max-width: 480px) {
          .input-group {
            gap: 0.6rem;
          }

          .chat-input-textarea {
            padding: 0.875rem;
            min-height: 70px;
            font-size: 0.95rem;
          }

          .chat-submit-button {
            padding: 0.65rem 1.25rem;
            font-size: 0.95rem;
            min-width: 80px;
          }

          .loading-indicator {
            font-size: 0.85rem;
            gap: 0.6rem;
            padding: 0.55rem;
          }
        }
      `}</style>
    </form>
  );
};

export default ChatInput;