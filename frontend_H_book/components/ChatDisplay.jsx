import React, { memo } from 'react';

const ChatDisplay = memo(({ messages = [] }) => {
  return (
    <div className="chat-display">
      {messages.length === 0 ? (
        <div className="empty-state">
          <p>Ask a question to get started!</p>
        </div>
      ) : (
        <div className="messages-container">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              <div className="message-content">
                {message.sender === 'system' ? (
                  <div>
                    {/* Implement answer display */}
                    <div className="answer-text">{message.content}</div>

                    {/* Show source references from retrieved context as small icons */}
                    {message.sources && message.sources.length > 0 && (
                      <div className="sources-section">
                        <span className="sources-label">Sources:</span>
                        <div className="sources-icons">
                          {message.sources.slice(0, 3).map((source, idx) => (
                            <a
                              key={idx}
                              href={source}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="source-icon"
                              title="View source"
                              aria-label={`Source ${idx + 1}`}
                            >
                              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6m4-3h6m-6 0v6m0-6H9m6 0l-7 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                              </svg>
                            </a>
                          ))}
                          {message.sources.length > 3 && (
                            <span className="source-count" title={`${message.sources.length} sources`}>
                              +{message.sources.length - 3}
                            </span>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Handle fallback responses ("Not covered in the book") */}
                    {message.content.includes("Not covered in the book") && (
                      <div className="fallback-notice">
                        The information you requested is not available in our knowledge base.
                      </div>
                    )}
                  </div>
                ) : (
                  <div>{message.content}</div>
                )}
              </div>
              <div className="message-meta">
                {message.timestamp && (
                  <small className="timestamp">
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </small>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      <style jsx>{`
        .chat-display {
          width: 100%;
          height: 100%;
          max-height: 100%;
          overflow-y: auto;
          border-radius: 12px;
          padding: 1.25rem;
          background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
          background-attachment: fixed;
          position: relative;
        }

        .chat-display::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: radial-gradient(ellipse at top, rgba(0, 124, 186, 0.05) 0%, transparent 70%);
          pointer-events: none;
        }

        .empty-state {
          text-align: center;
          padding: 3rem 1rem;
          color: #666;
          font-style: italic;
          font-size: 1.1rem;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 100%;
        }

        .empty-state::before {
          content: '🤖';
          font-size: 3rem;
          margin-bottom: 1rem;
          opacity: 0.6;
        }

        .messages-container {
          display: flex;
          flex-direction: column;
          gap: 1.25rem;
          padding: 0.5rem;
        }

        .message {
          padding: 1.25rem;
          border-radius: 18px;
          margin-bottom: 0.75rem;
          max-width: 80%;
          position: relative;
          animation: fadeIn 0.3s ease-out;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
          transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .message:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
        }

        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }

        .message.user {
          background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
          align-self: flex-end;
          margin-left: auto;
          border-bottom-right-radius: 4px;
          border: 1px solid rgba(0, 124, 186, 0.1);
        }

        .message.system {
          background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
          align-self: flex-start;
          border-bottom-left-radius: 4px;
          border: 1px solid rgba(0, 0, 0, 0.05);
        }

        .message-content {
          margin-bottom: 0.75rem;
        }

        .answer-text {
          line-height: 1.7;
          color: #2c3e50;
          font-size: 1.05rem;
          word-wrap: break-word;
        }

        .sources-section {
          margin-top: 1rem;
          padding-top: 0.75rem;
          border-top: 1px solid rgba(0, 0, 0, 0.08);
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .sources-label {
          font-size: 0.8rem;
          color: #6c757d;
          font-weight: 500;
          white-space: nowrap;
        }

        .sources-icons {
          display: flex;
          gap: 0.5rem;
          align-items: center;
          flex-wrap: wrap;
        }

        .source-icon {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 28px;
          height: 28px;
          border: 2px solid #e9ecef;
          border-radius: 50%;
          background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
          color: #495057;
          text-decoration: none;
          transition: all 0.3s ease;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .source-icon:hover {
          background: linear-gradient(135deg, #007cba 0%, #0056b3 100%);
          color: white;
          border-color: #007cba;
          transform: translateY(-2px) scale(1.1);
          box-shadow: 0 4px 12px rgba(0, 124, 186, 0.3);
        }

        .source-count {
          font-size: 0.75rem;
          color: #6c757d;
          background: rgba(0, 124, 186, 0.1);
          padding: 3px 8px;
          border-radius: 12px;
          border: 1px solid rgba(0, 124, 186, 0.2);
          font-weight: 500;
        }

        .fallback-notice {
          margin-top: 1rem;
          padding: 1rem;
          background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
          border: 1px solid rgba(255, 193, 7, 0.3);
          border-radius: 12px;
          font-size: 0.95rem;
          color: #856404;
          font-weight: 500;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .fallback-notice::before {
          content: '⚠️';
          font-size: 1.2rem;
        }

        .timestamp {
          color: #6c757d;
          font-size: 0.75rem;
          text-align: right;
          font-weight: 500;
          opacity: 0.7;
        }

        /* Responsive design */
        @media (max-width: 768px) {
          .chat-display {
            max-height: 100%;
            padding: 1rem;
          }

          .message {
            max-width: 85%;
            padding: 1rem;
            border-radius: 16px;
          }

          .message.user, .message.system {
            border-radius: 16px;
          }

          .sources-icons {
            gap: 0.3rem;
          }

          .source-icon {
            width: 26px;
            height: 26px;
          }

          .answer-text {
            font-size: 1rem;
            line-height: 1.6;
          }

          .empty-state {
            padding: 2rem 0.75rem;
            font-size: 1rem;
          }

          .empty-state::before {
            font-size: 2.5rem;
          }
        }

        @media (max-width: 480px) {
          .chat-display {
            max-height: 100%;
            padding: 0.75rem;
          }

          .message {
            max-width: 90%;
            padding: 0.875rem;
            border-radius: 14px;
          }

          .source-icon {
            width: 24px;
            height: 24px;
          }

          .sources-label {
            font-size: 0.75rem;
          }

          .timestamp {
            font-size: 0.7rem;
          }

          .answer-text {
            font-size: 0.95rem;
          }

          .fallback-notice {
            font-size: 0.9rem;
            padding: 0.875rem;
          }
        }
      `}</style>
    </div>
  );
});

export default ChatDisplay;