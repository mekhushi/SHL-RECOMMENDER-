import os
from fastapi import FastAPI, HTTPException
from schemas import ChatRequest, ChatResponse
from data_loader import CatalogManager
from agent import SHLAgent
from dotenv import load_dotenv

# Load environment variables (e.g. GEMINI_API_KEY)
load_dotenv()

app = FastAPI(title="SHL Assessment Recommender API")

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Initialize dependencies
try:
    catalog_mgr = CatalogManager("catalog.json")
    agent = SHLAgent(catalog_mgr)
    logger.info("Successfully loaded catalog and initialized SHLAgent.")
except Exception as e:
    logger.error(f"Error initializing services: {e}")
    catalog_mgr = None
    agent = None

@app.get("/health")
async def health_check():
    """Health check endpoint required by evaluator."""
    if agent is None:
        raise HTTPException(status_code=500, detail="Service not initialized properly")
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Stateless chat endpoint. 
    Receives full conversation history and returns the next assistant reply, 
    recommendations (if any), and whether the conversation has ended.
    """
    if agent is None:
        raise HTTPException(status_code=500, detail="Service not initialized properly")
        
    try:
        response = agent.process_chat(request)
        return response
    except Exception as e:
        logger.error(f"Error processing chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error while processing chat.")
