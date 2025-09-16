from chain import get_rag_chain
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

def main():
    """
    Main function to run the command-line interface for the RAG application.
    """
    print("🤖 Initializing Diabetes Clinical Assistant...")
    
    try:
        rag_chain = get_rag_chain()
        print("✅ Assistant is ready. Ask clinical questions about your patients.")
        print("   (Type 'exit' or 'quit' to end the session)")

        while True:
            question = input("\n> Question: ")
            
            if question.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break
            
            if not question.strip():
                continue

            print("\n🧠 Thinking and retrieving information...")
            
            # Invoke the RAG chain to get the answer
            answer = rag_chain.invoke(question)
            
            print("\n💡 Assistant's Response:")
            print(answer)

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("   Please ensure the Qdrant server is running and you have run the ingestion script.")

if __name__ == "__main__":
    main()