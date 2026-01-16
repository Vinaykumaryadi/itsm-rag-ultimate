from typing import Annotated, List, TypedDict, Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

# 1. Define the Shared State
class AgentState(TypedDict):
    # 'add_messages' allows the graph to append new messages rather than overwriting
    messages: Annotated[List[BaseMessage], add_messages]
    next_node: str
    confidence: float
    ticket_id: str

# 2. Define the Nodes
def supervisor_node(state: AgentState):
    """The brain: Decides where to go based on ticket content."""
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # Logic to classify and route
    last_message = state["messages"][-1].content
    
    # In a real app, use structured output (Pydantic) for this decision
    if "urgent" in last_message.lower() or "security" in last_message.lower():
        return {"next_node": "human_review"}
    return {"next_node": "retriever_agent"}

def retriever_node(state: AgentState):
    """Worker: Fetches data from ChromaDB."""
    # This is where your vector search logic lives
    query = state["messages"][-1].content
    # Simulated search result
    context = "Solution: Reset VPN settings in the IAM portal."
    
    return {
        "messages": [HumanMessage(content=f"Found Solution: {context}", name="Retriever")],
        "confidence": 0.85
    }

def human_review_node(state: AgentState):
    """Wait for manual approval for high-risk tickets."""
    return {"messages": [HumanMessage(content="Pending human approval for high-risk task.", name="Human")]}

# 3. Build the Graph
workflow = StateGraph(AgentState)

# Add our nodes
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("retriever_agent", retriever_node)
workflow.add_node("human_review", human_review_node)

# 4. Define the Logic (Edges)
workflow.set_entry_point("supervisor")

# Conditional routing from supervisor
workflow.add_conditional_edges(
    "supervisor",
    lambda x: x["next_node"],
    {
        "retriever_agent": "retriever_agent",
        "human_review": "human_review"
    }
)

# After retrieval, go to end (or you could route back to supervisor)
workflow.add_edge("retriever_agent", END)
workflow.add_edge("human_review", END)

# 5. Compile the Graph
app = workflow.compile()