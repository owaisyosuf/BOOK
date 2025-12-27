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

  const handleSubmit = async (queryText, scope = "full_book") => {
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
      // In a real implementation, this would call the backend API
      // For now, we'll simulate an API call
      const response = await simulateApiCall(queryText, scope);

      const botMessage = {
        id: Date.now() + 1,
        text: response.response,
        sender: 'bot',
        citations: response.citations || [],
        timestamp: new Date(),
        status: response.status
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: "Sorry, I encountered an error processing your query. Please try again.",
        sender: 'bot',
        timestamp: new Date(),
        status: 'error'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Simulate API call - in real implementation, this would call the backend
  const simulateApiCall = async (query, scope) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    // This is a placeholder response - real implementation would call the backend API
    if (query.toLowerCase().includes("not found") || Math.random() > 0.8) {
      return {
        response: "Information not found in the book content.",
        status: "not_found",
        citations: []
      };
    }

    return {
      response: `This is a simulated response to your query: "${query}". In a real implementation, this would come from the RAG system based on the book content.`,
      status: "success",
      citations: [
        {
          page_path: "/docs/getting-started",
          content_snippet: "Retrieval-Augmented Generation (RAG) systems combine the power of information retrieval with text generation...",
          position: 10
        }
      ]
    };
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