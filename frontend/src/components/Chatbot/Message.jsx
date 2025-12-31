import React from 'react';
import clsx from 'clsx';
import styles from './Message.module.css';

// Message component to display individual chat messages
const Message = ({ message }) => {
  const isUser = message.sender === 'user';

  return (
    <div className={clsx(styles.message, isUser ? styles.userMessage : styles.botMessage)}>
      <div className={styles.messageText}>
        {message.text}
      </div>

      {message.citations && message.citations.length > 0 && (
        <div className={styles.citations}>
          <strong>Citations:</strong>
          {message.citations.map((citation, index) => (
            <div key={index} className={styles.citation}>
              <a href={citation.page_path} target="_blank" rel="noopener noreferrer">
                {citation.page_path}
              </a>
              <div className={styles.snippet}>
                {citation.content_snippet}
              </div>
            </div>
          ))}
        </div>
      )}

      {message.status === 'not_found' && (
        <div className={styles.notFoundMessage}>
          The information you requested was not found in the book content.
        </div>
      )}
    </div>
  );
};

export default Message;