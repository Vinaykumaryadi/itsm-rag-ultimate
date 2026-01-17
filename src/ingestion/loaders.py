import os
from langchain_community.document_loaders import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def run_ingestion():
    """Loads CSV data and creates a FAISS vector database."""
    data_path = "data/incidents_advanced.csv"
    save_path = "faiss_index"

    if not os.path.exists(data_path):
        print(f"❌ Error: {data_path} not found.")
        return

    print("📂 Loading ITSM data...")
    loader = CSVLoader(data_path)
    documents = loader.load()

    print("🧠 Generating HuggingFace Embeddings (Local)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("⚡ Building FAISS Index...")
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    # Save locally
    vectorstore.save_local(save_path)
    print(f"✅ FAISS index saved to '{save_path}'")

if __name__ == "__main__":
    run_ingestion()