from src.chain import get_rag_chain

def main():
    """
    Main function to run the command-line interface for the RAG application.
    """
    print("🤖 Initializing Diabetes RAG Assistant...")
    
    try:
        rag_chain = get_rag_chain()
        print("✅ Assistant is ready. Ask your questions below.")
        print("   (Type 'exit' or 'quit' to end the session)")

        while True:
            question = input("\n> Question: ")
            
            if question.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break
            
            if not question.strip():
                continue

            print("\n🧠 Thinking...")
            
            # Invoke the RAG chain to get the answer
            answer = rag_chain.invoke(question)
            
            print("\n💡 Answer:")
            print(answer)

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("   Please ensure Qdrant is running and the collection has been ingested.")

if __name__ == "__main__":
    main()