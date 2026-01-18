import os
from langchain_community.document_loaders import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def load_incidents(path='data/incidents_advanced.csv'):
    """Load CSV incident data and return as LangChain Document objects."""
    if not os.path.exists(path):
        print(f"❌ Error: {path} not found.")
        return []
    
    loader = CSVLoader(path)
    return loader.load()

def run_ingestion():
    """Execute data ingestion pipeline: CSV -> Embeddings -> FAISS Index."""
    data_path = "data/incidents_advanced.csv"
    save_path = "faiss_index"

    if not os.path.exists(data_path):
        print(f"❌ Error: {data_path} not found.")
        return

    print("📂 Loading ITSM data...")
    documents = load_incidents(data_path)

    print("🧠 Generating HuggingFace Embeddings (Local)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("⚡ Building FAISS Index...")
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    # Persist FAISS index locally for fast retrieval
    vectorstore.save_local(save_path)
    print(f"✅ FAISS index saved to '{save_path}'")

if __name__ == "__main__":
    run_ingestion()