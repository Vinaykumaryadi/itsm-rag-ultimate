import os
import sys
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Load environment variables (API Keys)
load_dotenv()

# Add 'src' to system path so Python can find your modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import the logic based on your existing Git structure
# Note: Adjusting imports to match your 'git ls-files' output
try:
    from workflows.langgraph_flow import app as workflow  # Your LangGraph flow
    from ingestion.loaders import run_ingestion           # Your ingestion logic
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Ensure your folder structure matches: src/workflows/langgraph_flow.py")
    sys.exit(1)

def main():
    """
    Main entry point for the ITSM AI Agent.
    Checks for the knowledge base, runs ingestion if needed, and starts the chat.
    """
    # 1. Check if the database exists locally
    if not os.path.exists("chroma_db"):
        print("🕵️ No knowledge base (chroma_db) found. Starting ingestion...")
        run_ingestion()
    else:
        print("✅ Knowledge base found. Ready to process queries.")

    print("\n" + "="*50)
    print("🤖 ITSM AI AGENT ONLINE")
    print("Ask about IT tickets, VPN issues, or hardware requests.")
    print("Type 'exit' to quit.")
    print("="*50)

    while True:
        user_query = input("\nUser: ").strip()
        
        if user_query.lower() in ['exit', 'quit', 'q']:
            print("Goodbye!")
            break
        
        if not user_query:
            continue

        print("🧠 Thinking...")
        
        try:
            # Initialize the state for LangGraph
            inputs = {"messages": [HumanMessage(content=user_query)]}
            
            # Invoke the LangGraph workflow
            result = workflow.invoke(inputs)
            
            # Print the final AI response
            print(f"\n--- Response ---\n{result['messages'][-1].content}")
        
        except Exception as e:
            print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()