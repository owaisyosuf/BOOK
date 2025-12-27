import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fastapi import FastAPI
from contextlib import asynccontextmanager
from config.settings import settings
from .routes.health import router as health_router
from .routes.chat import router as chat_router
from .routes.index import router as index_router
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up RAG Chatbot API")
    # Any initialization code can go here

    yield

    # Shutdown
    logger.info("Shutting down RAG Chatbot API")
    # Any cleanup code can go here


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug,
    lifespan=lifespan
)

# Include routers
app.include_router(health_router, prefix="", tags=["health"])
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(index_router, prefix="/api", tags=["index"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "RAG Chatbot API", "version": settings.version}