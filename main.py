import os
import sys
from dotenv import load_dotenv

# Load environment variables (API keys, Groq API key, etc.)
load_dotenv()

# Add 'src' directory to Python path for relative imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from workflows.langgraph_flow import app
    from ingestion.loaders import run_ingestion
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

def main():
    # Initialize FAISS vector index if it doesn't exist
    if not os.path.exists("faiss_index"):
        print("🕵️ FAISS index not found. Initializing...")
        run_ingestion()

    print("\n🤖 ITSM Agent Ready. (Type 'exit' to quit)")
    
    # Main conversation loop
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Stream the user query through the LangGraph workflow
        events = app.stream({"messages": [("user", user_input)]})
        for event in events:
            for value in event.values():
                print(f"Assistant: {value['messages'][-1].content}")

if __name__ == "__main__":
    main()