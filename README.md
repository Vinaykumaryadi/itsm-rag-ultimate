# 🚀 Agentic RAG for ITSM Automation

![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Framework](https://img.shields.io/badge/Framework-LangGraph-orange)
![Linter](https://img.shields.io/badge/Code%20Style-Black-000000)

**A production-grade IT Service Management (ITSM) automation engine using LangGraph, FastAPI, and ChromaDB.**

This project demonstrates a sophisticated multi-agent approach to resolving IT tickets. Unlike standard linear RAG pipelines, this system uses a **Supervisor Agent** to analyze risk and route tickets between **Automated Resolution**, **Semantic Search**, and **Human-in-the-Loop (HITL)** oversight.

---

## 🏗️ System Architecture

![System Workflow](docs/plots/preprocessing_impact.png)

### 1. Data Engineering & EDA
* **Automated Cleaning:** Custom pipeline to strip noise (RE: tags, HTML, headers) from messy human-written tickets.
* **Exploratory Analysis:** Statistical profiling of ticket distributions and resolution bottlenecks.

### 2. Hybrid Retrieval Engine
* **Vector Store:** ChromaDB utilizing `all-MiniLM-L6-v2` embeddings for deep semantic understanding.
* **Metadata Filtering:** Enhanced retrieval narrowed by ticket category to reduce search space.

### 3. Agentic Orchestration (LangGraph)
* **The Supervisor:** Acts as the "Brain," classifying incoming tickets by risk. 
* **Retriever Agent:** Executes vector search and synthesizes a solution using RAG.
* **Human-in-the-Loop Node:** A safety-first node that intercepts high-priority requests.

![Category Distribution](docs/plots/category_dist.png)

---

## 🛠️ Tech Stack

| Category | Technology |
| :--- | :--- |
| **Orchestration** | **LangChain, LangGraph** |
| **LLMs** | **OpenAI GPT-4o / Claude 3.5** |
| **Vector DB** | **ChromaDB** |
| **Data Science** | **Pandas, Matplotlib, Seaborn** |
| **Backend** | **FastAPI** |
| **Frontend** | **Streamlit** |
| **Observability** | **MLflow** |

---

## 📊 Evaluation & Monitoring

![Resolution Trends](docs/plots/resolution_trends.png)

We utilize **MLflow** to track the lifecycle of every agentic decision:
* **Confidence Scores:** Monitored to prevent "hallucinated" resolutions.
* **Latency Tracking:** Measuring the overhead of multi-agent reasoning.
* **Resolution Trends:** Visualized via Seaborn to identify common "unresolvable" clusters.

---

## 🛡️ Technical Challenges & Decisions

### **Why LangGraph instead of a simple Chain?**
Standard chains are linear. In ITSM, we need **cycles**. LangGraph allows the agent to loop and self-correct if the first retrieval is insufficient.

### **Ensuring Safety (HITL)**
Any ticket tagged as **"Security"** or **"Critical"** bypasses automation entirely and is routed to a human, ensuring 0% automation risk for mission-critical infrastructure.

---

## 🚀 Getting Started

1. **Install:** `pip install -r requirements.txt`
2. **Setup Data:** `python generate_all.py && python research/eda_report.py`
3. **Run API:** `uvicorn api.fastapi_app:app --reload`
4. **Run UI:** `streamlit run ui/streamlit_hitl.py`

---
MIT License | © 2026 Vinay Kumar