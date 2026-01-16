from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.ingestion.loaders import load_incidents
from src.retrieval.vector_store import build_store
from src.workflows.langgraph_flow import app as graph_app
from langchain_core.messages import HumanMessage

app = FastAPI(title="ITSM RAG Ultimate API")

# Global state for the vector store
vector_db = None

@app.on_event("startup")
async def startup_event():
    global vector_db
    print("Initializing Vector Database...")
    docs = load_incidents()
    vector_db = build_store(docs)

class TicketRequest(BaseModel):
    ticket_id: str
    description: str

@app.post("/process_ticket")
async def process_ticket(request: TicketRequest):
    try:
        # Initialize LangGraph state
        initial_state = {
            "messages": [HumanMessage(content=request.description)],
            "ticket_id": request.ticket_id
        }
        
        # Execute Workflow
        result = graph_app.invoke(initial_state)
        
        # Extract the last message (the resolution or status)
        final_msg = result["messages"][-1].content
        
        return {
            "ticket_id": request.ticket_id,
            "decision": result.get("next_node", "completed"),
            "resolution": final_msg,
            "confidence": result.get("confidence", 1.0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))