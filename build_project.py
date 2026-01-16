import os

# Define the project structure and file contents
project_files = {
    "data/incidents.csv": "ticket_id,title,description,category,priority,resolution,reopened\nINC001,VPN not working,User cannot connect to VPN,Network,High,Restart VPN service,false\nINC002,Email sync issue,Outlook emails not syncing,Application,Medium,Restart Outlook,false",
    "src/ingestion/loaders.py": "from langchain_community.document_loaders import CSVLoader\n\ndef load_incidents(path='data/incidents.csv'):\n    loader = CSVLoader(file_path=path)\n    return loader.load()",
    "src/retrieval/vector_store.py": "from langchain_community.vectorstores import Chroma\nfrom langchain_huggingface import HuggingFaceEmbeddings\n\ndef build_store(docs):\n    embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')\n    return Chroma.from_documents(docs, embeddings)",
    "src/workflows/langgraph_flow.py": "from langgraph.graph import StateGraph, END\n\ndef build_workflow():\n    workflow = StateGraph(dict)\n    workflow.add_node('retrieve', lambda x: x)\n    workflow.set_entry_point('retrieve')\n    workflow.add_edge('retrieve', END)\n    return workflow.compile()",
    "api/fastapi_app.py": "from fastapi import FastAPI\napp = FastAPI(title='RAG ITSM')\n\n@app.get('/')\ndef root(): return {'status': 'active'}",
    "requirements.txt": "langchain\nlanggraph\nfastapi\nuvicorn\nchromadb\nsentence-transformers\nlangchain-huggingface\nstreamlit",
    "README.md": "# RAG ITSM Ultimate\n\n## Setup\n1. Install: `pip install -r requirements.txt`\n2. Run API: `uvicorn api.fastapi_app:app --reload`",
    "architecture.md": "graph TD\n    A[User Ticket] --> B[RAG Pipeline]\n    B --> C[Vector Search]\n    C --> D[LangGraph Logic]\n    D --> E[Response]"
}

def create_project():
    print("📂 Creating RAG ITSM Ultimate Project Structure...")
    for path, content in project_files.items():
        # Get the directory part of the path
        directory = os.path.dirname(path)
        
        # Only attempt to create directory if the path actually contains one
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        # Write file content
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✔️ Created: {path}")
    
    print("\n🚀 Project ready! Your files are structured and ready for GitHub.")

if __name__ == "__main__":
    create_project()