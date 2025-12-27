import React, { useState } from 'react';
import clsx from 'clsx';
import styles from './QueryForm.module.css';

// QueryForm component for submitting questions to the chatbot
const QueryForm = ({ onSubmit, isLoading }) => {
  const [query, setQuery] = useState('');
  const [scope, setScope] = useState('full_book');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSubmit(query.trim(), scope);
      setQuery('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.queryForm}>
      <div className={styles.inputGroup}>
        <select
          value={scope}
          onChange={(e) => setScope(e.target.value)}
          className={styles.scopeSelect}
          disabled={isLoading}
        >
          <option value="full_book">Entire Book</option>
          <option value="section">Specific Section</option>
          <option value="page">Current Page</option>
        </select>

        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about this book..."
          className={styles.queryInput}
          disabled={isLoading}
          aria-label="Ask a question about this book"
        />

        <button
          type="submit"
          className={clsx(styles.queryButton, isLoading && styles.loading)}
          disabled={isLoading || !query.trim()}
        >
          {isLoading ? 'Sending...' : 'Ask'}
        </button>
      </div>

      <div className={styles.hint}>
        Your question will be answered based only on the book's content with proper citations.
      </div>
    </form>
  );
};

export default QueryForm;