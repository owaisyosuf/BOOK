import React, { useState, useRef } from 'react';
import clsx from 'clsx';
import styles from './ChatInterface.module.css';
import QueryForm from './QueryForm';
import Message from './Message';

// ChatInterface component that manages the chat state and API communication
const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  React.useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (queryText, scope = "full_book", section = null) => {
    // Add user message to the chat
    const userMessage = {
      id: Date.now(),
      text: queryText,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: queryText,
          scope: scope,
          section: section
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await response.json();

      if (result.status === 'error') {
        throw new Error(result.error?.message || 'Error processing query');
      }

      const botMessage = {
        id: Date.now() + 1,
        text: result.data.response,
        sender: 'bot',
        citations: result.data.citations || [],
        timestamp: new Date(),
        status: result.data.status
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: `Sorry, I encountered an error: ${error.message}. Please try again.`,
        sender: 'bot',
        timestamp: new Date(),
        status: 'error'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={clsx('container', styles.chatContainer)}>
      <div className={styles.chatHeader}>
        <h3>Book Q&A Assistant</h3>
        <p>Ask questions about this book's content</p>
      </div>

      <div className={styles.chatMessages}>
        {messages.length === 0 ? (
          <div className={styles.welcomeMessage}>
            <p>Hello! I'm your book assistant. Ask me questions about this book's content, and I'll find answers based on the provided material.</p>
            <p>Try asking: "What are RAG systems?" or "How do I deploy this?"</p>
          </div>
        ) : (
          messages.map((message) => (
            <Message
              key={message.id}
              message={message}
            />
          ))
        )}
        {isLoading && (
          <div className={clsx(styles.message, styles.botMessage)}>
            <div className={styles.messageText}>Thinking...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className={styles.chatInputArea}>
        <QueryForm onSubmit={handleSubmit} isLoading={isLoading} />
      </div>
    </div>
  );
};

export default ChatInterface;