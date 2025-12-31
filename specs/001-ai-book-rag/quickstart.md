# Quickstart Guide: AI/Spec-Driven Book with Integrated RAG Chatbot

## Overview
This guide provides a quick setup and deployment process for the AI-driven technical book with integrated RAG chatbot system. Follow these steps to get your system running in under 10 minutes.

## Prerequisites
- Node.js (v18 or higher)
- Python (v3.11 or higher)
- Git
- Access to OpenAI API key
- Access to Qdrant Cloud (free tier)
- Access to Neon Serverless Postgres (free tier)

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Dependencies

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend Setup
```bash
cd frontend
npm install
```

### 3. Configure Environment Variables

#### Backend Configuration
Create `backend/.env`:
```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
NEON_DATABASE_URL=your_neon_postgres_connection_string
DEBUG=false
LOG_LEVEL=INFO
```

#### Frontend Configuration
Create `frontend/.env`:
```env
REACT_APP_API_BASE_URL=http://localhost:8000  # or your backend URL
```

## Local Development Setup

### 1. Start Backend API
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m src.api.main
```
The API will start on `http://localhost:8000`

### 2. Start Frontend Development Server
```bash
cd frontend
npm start
```
The frontend will start on `http://localhost:3000`

## Content Management

### 1. Adding Book Content
1. Add Markdown files to `frontend/docs/`
2. Update `frontend/sidebars.js` to include new pages in navigation
3. Run indexing script to update the vector database:
```bash
cd backend
python -m scripts.utilities.index_content
```

### 2. Content Structure
```
frontend/docs/
├── intro.md
├── chapter-1/
│   ├── getting-started.md
│   └── basic-concepts.md
├── chapter-2/
│   ├── advanced-topics.md
│   └── examples.md
└── reference/
    └── api-reference.md
```

## API Usage

### Query the RAG System
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Your question here",
    "scope": "full_book"
  }'
```

### Query Parameters
- `query`: The question to ask (required)
- `scope`: "full_book", "section", or "page" (optional, default: "full_book")
- `section`: Section name if scope is "section" (optional)

## Deployment

### 1. Frontend Deployment (GitHub Pages)
```bash
cd frontend
npm run build
npm run deploy  # This will deploy to GitHub Pages
```

### 2. Backend Deployment (Railway/Render)
#### Using Railway:
1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Link project: `railway link`
4. Deploy: `railway up`

#### Using Render:
1. Create a new Web Service on Render
2. Connect to your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`

## Testing

### 1. Run Backend Tests
```bash
cd backend
source venv/bin/activate
pytest
```

### 2. Run Frontend Tests
```bash
cd frontend
npm test
```

## Monitoring and Maintenance

### 1. Check System Health
```bash
curl http://localhost:8000/health
```

### 2. View API Documentation
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Troubleshooting

### Common Issues

#### 1. API Connection Errors
- Verify backend is running on `http://localhost:8000`
- Check CORS configuration in backend settings

#### 2. Vector Search Issues
- Ensure content has been indexed: `python -m scripts.utilities.index_content`
- Verify Qdrant connection settings in `.env`

#### 3. Frontend Build Issues
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`

### Performance Issues
- Check if Qdrant Cloud is responding within expected timeframes
- Verify OpenAI API key has sufficient rate limits
- Monitor Neon Postgres connection pool usage

## Next Steps

1. **Customize your book content** in the `frontend/docs/` directory
2. **Configure your domain** for GitHub Pages
3. **Set up monitoring** for production deployment
4. **Optimize performance** based on usage patterns
5. **Review the full documentation** in the `specs/` directory for advanced configuration