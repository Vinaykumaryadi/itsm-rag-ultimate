🚀 Agentic RAG for ITSM Automation
A production-grade IT Service Management (ITSM) automation engine using LangGraph, FastAPI, and ChromaDB.

This project demonstrates a multi-agent approach to resolving IT tickets. Unlike standard RAG, which simply retrieves and summarizes, this system uses a Supervisor Agent to determine the risk level of a ticket and routes it between automated resolution and Human-in-the-Loop (HITL) oversight.

🏗️ System Architecture
1. Ingestion & Chunking
Multi-source Loaders: Handles CSV ticket exports and PDF documentation using Unstructured.

Recursive Splitting: Maintains semantic context by splitting documents based on structural boundaries.

2. Hybrid Retrieval Engine
Vector Store: ChromaDB with all-MiniLM-L6-v2 embeddings for semantic similarity.

Keyword Search: BM25 integration to ensure specific error codes and IDs are never missed.

3. Agentic Orchestration (LangGraph)
The Supervisor: Analyzes the user's intent. If a ticket is flagged as "High Priority" or "Security Related," the agent halts automation.

The Retriever Agent: Fetches solutions and generates a resolution plan only for safe, standard requests.

🛠️ Tech Stack
Orchestration: LangChain, LangGraph

LLMs: OpenAI GPT-4o / Anthropic Claude 3.5

Vector Database: ChromaDB

Backend: FastAPI (Model Context Protocol ready)

Frontend: Streamlit (Human-in-the-Loop Dashboard)

Observability: MLflow (Tracking confidence and latency)

🚀 Getting Started
Prerequisites
Python 3.10+

OpenAI API Key (or local LLM via Ollama)

Docker (Optional)

Installation
Clone the repo:

Bash

git clone https://github.com/your-username/itsm-rag-ultimate.git
cd itsm-rag-ultimate
Install dependencies:

Bash

pip install -r requirements.txt
Set environment variables: Create a .env file:

Plaintext

OPENAI_API_KEY=your_sk_...
Running the Project
Start the Backend: uvicorn api.fastapi_app:app --reload

Start the UI: streamlit run ui/streamlit_hitl.py

Start MLflow: mlflow ui

🧹 Data Engineering & EDA
This project includes a robust preprocessing pipeline to improve RAG performance:

Noise Reduction: Automated cleaning of ticket metadata and special characters.

Feature Engineering: Merging logical fields to create dense context for the Vector Store.

EDA: Insightful analysis of incident categories and resolution bottlenecks (see /research).

📊 Evaluation & Monitoring
We use MLflow to track every agentic decision. Key metrics monitored include:

Confidence Score: The agent's self-reported certainty in a resolution.

Auto-Resolution Rate: Percentage of tickets handled without human intervention.

Retrieval Precision: How relevant the fetched context was to the specific error code.

🛡️ Technical Challenges & Decisions
Q: Why LangGraph instead of a simple Chain?
A: Standard RAG chains are linear. In ITSM, we need cycles. If a retrieved solution doesn't work, the agent needs to loop back, search again, or escalate. LangGraph allows for the stateful, cyclic logic required for real-world reliability.

Q: How do we prevent hallucinations?
A: We implemented a "Confidence Threshold." If the LLM's confidence score in the retrieved solution is below 0.8, the graph automatically routes the state to the human_review_node, ensuring an agent never sends bad advice to a user.

📄 License
Distributed under the MIT License. See LICENSE for more information.

