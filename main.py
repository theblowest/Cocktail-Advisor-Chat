from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
from typing import List, Dict, Any
from contextlib import asynccontextmanager

# Import application modules
from app.db.models import ChatRequest, ChatResponse
from app.db.vector_store import VectorStore
from app.llm.engine import LLMEngine
from app.llm.rag import CocktailRAG
from app.utils.cocktail_parser import load_cocktail_data
from app.config import HOST, PORT

from dotenv import load_dotenv

load_dotenv()

# Initialize components
vector_store = VectorStore()
llm_engine = LLMEngine()
cocktail_rag = CocktailRAG(vector_store, llm_engine)

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the application on startup"""
    # Load cocktail data
    cocktails = load_cocktail_data()

    # Add cocktails to vector store
    vector_store.add_cocktails(cocktails)

    print("Application initialized successfully")
    yield  # App is running
    print("Application shutting down")

# Create FastAPI application
app = FastAPI(title="Cocktail Advisor Chat", lifespan=lifespan)

# Setup templates and static files
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Define routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the chat interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process chat message and return response"""
    try:
        # Process query using RAG
        response, sources = cocktail_rag.process_query(request.message, request.history)

        return ChatResponse(
            message=response,
            sources=sources if sources else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the application
if __name__ == "__main__":
    print(f"Starting Cocktail Advisor Chat on http://{HOST}:{PORT}")
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
3