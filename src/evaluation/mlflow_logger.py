import mlflow

def log_rag_metrics(ticket_id, confidence, response_time, status):
    mlflow.set_experiment("ITSM_RAG_Production")
    
    with mlflow.start_run(run_name=f"Ticket_{ticket_id}"):
        # Log Parameters
        mlflow.log_param("ticket_id", ticket_id)
        
        # Log Metrics
        mlflow.log_metric("confidence_score", confidence)
        mlflow.log_metric("latency_ms", response_time)
        
        # Log Tags
        mlflow.set_tag("status", status)
        
        # In a real scenario, you'd log Hallucination scores here
        # using RAGAS or a similar evaluation framework
        print(f"Logged metrics for {ticket_id} to MLflow")