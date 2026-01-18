from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables (Groq API key, etc.)
load_dotenv()

from langchain_core.messages import HumanMessage
from src.workflows.langgraph_flow import app as graph_app

# Initialize FastAPI application
app = FastAPI(title="ITSM RAG Ultimate API")

# Global state for vector store (lazy-loaded on first request)
vector_db = None

@app.on_event("startup")
async def startup_event():
    """Initialize API on startup (FAISS index loaded on first query)."""
    global vector_db
    print("Initializing API...")
    # Vector DB is lazy-loaded on first ticket processing in langgraph_flow
    print("✅ API Ready")

class TicketRequest(BaseModel):
    """Request schema for ticket processing."""
    ticket_id: str
    description: str

@app.post("/process_ticket")
async def process_ticket(request: TicketRequest):
    """Process IT ticket through RAG-based agentic workflow."""
    try:
        # Prepare LangGraph state with user query and ticket ID
        initial_state = {
            "messages": [HumanMessage(content=request.description)],
            "ticket_id": request.ticket_id
        }
        
        # Execute the LangGraph workflow (retrieval + LLM response)
        result = graph_app.invoke(initial_state)
        
        # Extract the assistant's response from the final message
        final_msg = result["messages"][-1].content
        
        return {
            "ticket_id": request.ticket_id,
            "decision": result.get("next_node", "completed"),
            "resolution": final_msg,
            "confidence": result.get("confidence", 1.0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))