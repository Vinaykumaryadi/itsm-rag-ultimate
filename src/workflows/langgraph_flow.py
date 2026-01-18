import os
from typing import Annotated, TypedDict
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Define the state schema for the LangGraph workflow
class State(TypedDict):
    messages: Annotated[list, add_messages]  # Conversation history with auto-merging

def chatbot(state: State):
    # Initialize Groq LLM with free tier model (no API cost)
    # Alternative: 'llama3-8b-8192' for faster but less capable responses
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    # Load HuggingFace embeddings for semantic similarity
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if os.path.exists("faiss_index"):
        # Load local FAISS index with historical incident data
        # allow_dangerous_deserialization=True needed for pickled FAISS indices
        vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        
        # Retrieve top 3 similar incidents from the database
        user_input = state["messages"][-1].content
        docs = retriever.invoke(user_input)
        context = "\n".join([d.page_content for d in docs])
        
        # Build system prompt with RAG context from historical incidents
        system_prompt = (
            "You are a professional ITSM Assistant. Use the provided context "
            "from the incident database to answer accurately.\n\n"
            f"Context:\n{context}"
        )
        messages = [{"role": "system", "content": system_prompt}] + state["messages"]
        response = llm.invoke(messages)
    else:
        # Fallback: Answer without context if FAISS index unavailable
        response = llm.invoke(state["messages"])
        
    return {"messages": [response]}

# Compile the LangGraph workflow
# Simple linear flow: START -> chatbot -> END
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

app = graph_builder.compile()