# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for ChromaDB and Unstructured
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose ports for FastAPI (8000), Streamlit (8501), and MLflow (5000)
EXPOSE 8000 8501 5000

# Create a start script to run all services
RUN echo '#!/bin/bash\n\
mlflow ui --host 0.0.0.0 --port 5000 &\n\
uvicorn api.fastapi_app:app --host 0.0.0.0 --port 8000 &\n\
streamlit run ui/streamlit_hitl.py --server.port 8501 --server.address 0.0.0.0\n\
' > /app/start.sh

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]