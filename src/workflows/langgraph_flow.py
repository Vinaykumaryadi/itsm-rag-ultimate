import os
from typing import Annotated, TypedDict
from langchain_groq import ChatGroq  # <--- Switched to Groq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Load Free Groq LLM (No OpenAI needed!)
# You can use 'llama-3.3-70b-versatile' or 'llama3-8b-8192'
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

def chatbot(state: State):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if os.path.exists("faiss_index"):
        # allow_dangerous_deserialization is required for loading local FAISS files
        vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        
        user_input = state["messages"][-1].content
        docs = retriever.invoke(user_input)
        context = "\n".join([d.page_content for d in docs])
        
        system_prompt = (
            "You are a professional ITSM Assistant. Use the provided context "
            "from the incident database to answer accurately.\n\n"
            f"Context:\n{context}"
        )
        messages = [{"role": "system", "content": system_prompt}] + state["messages"]
        response = llm.invoke(messages)
    else:
        response = llm.invoke(state["messages"])
        
    return {"messages": [response]}

# Build Graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

app = graph_builder.compile()