# AI-Driven Technical Book with Integrated RAG Chatbot

This project implements an AI-driven technical book with an integrated RAG (Retrieval-Augmented Generation) chatbot that answers questions strictly from book content with zero hallucination.

## Project Overview

The system consists of:

- **Frontend**: Docusaurus-based technical book deployed to GitHub Pages
- **Backend**: FastAPI-based RAG system with vector search capabilities
- **Data Storage**: Qdrant Cloud (vector database) and Neon Postgres (metadata)
- **AI Integration**: OpenAI API with Langchain for RAG implementation

## Architecture

### Frontend (Docusaurus)
- Markdown-first content authoring
- Integrated chatbot UI
- GitHub Pages deployment
- Responsive design for documentation

### Backend (FastAPI)
- RAG chat API endpoints
- Content indexing service
- Vector search integration
- Zero-hallucination enforcement

### Data Layer
- Qdrant Cloud for vector embeddings
- Neon Postgres for metadata storage
- Content versioning and management

## Features

1. **Technical Book Creation**:
   - Markdown-based authoring
   - Docusaurus-powered frontend
   - GitHub Pages deployment

2. **RAG Chatbot**:
   - Questions answered only from book content
   - Zero hallucination guarantee
   - Proper citation of sources
   - Context-restricted responses

3. **Performance**:
   - Fast response times (<3s for 95% of queries)
   - Optimized vector search
   - Caching mechanisms

## Implementation Status

Based on the task breakdown in `specs/001-ai-book-rag/tasks.md`, the following has been implemented:

### Setup Phase (Complete)
- Project structure created
- Backend (FastAPI) and frontend (Docusaurus) initialized
- Configuration files set up

### Foundational Phase (Complete)
- Data models created (BookContent, Query, Response, etc.)
- Embedding and indexing services implemented
- API endpoints defined (health, chat, index)

### User Story 1: Create and Publish Technical Book (Complete)
- Docusaurus configuration
- Initial book content (intro and getting started)
- Styling and navigation components

### User Story 2: Query Book Content via RAG Chatbot (Implementation Ready)
- RAG service with context restriction
- Chat interface components
- API endpoints for querying

### User Story 3: Performance Optimization (Implementation Ready)
- Performance monitoring considerations
- Response time tracking

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js LTS
- OpenAI API key
- Qdrant Cloud account
- Neon Postgres account

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env`:
   ```
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   DATABASE_URL=your_neon_postgres_connection_string
   ```
4. Start the API: `uvicorn src.api.main:app --reload`

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm start`

### Content Indexing
To index your book content:
1. Place Markdown files in `frontend/docs/`
2. Run the indexing script: `python scripts/utilities/index-content.py`

## Configuration

### Environment Variables
The backend requires the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `QDRANT_URL`: URL to your Qdrant Cloud instance
- `QDRANT_API_KEY`: Your Qdrant API key
- `DATABASE_URL`: Connection string for Neon Postgres

### API Endpoints

- `GET /health`: Health check endpoint
- `POST /api/chat`: Query the RAG system
- `POST /api/index`: Index new content
- `GET /api/content`: List available content

## Deployment

### Frontend (GitHub Pages)
1. Build the site: `npm run build`
2. Deploy: `npm run deploy`

### Backend
Deploy to your preferred cloud platform (Railway, Render, etc.) with the required environment variables.

## Security

- Input validation for all user queries
- Rate limiting to prevent abuse
- Context-restricted responses to prevent hallucinations
- Secure API key management

## Testing

Unit tests are available in the `backend/tests/` directory. Run them with:
```
cd backend
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the terms specified in the project constitution.