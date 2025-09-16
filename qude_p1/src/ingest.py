import qdrant_client
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Import from our own project files
import config, utils

def main():
    """Main function to ingest data into Qdrant."""
    print("🚀 Starting data ingestion process...")

    # 1. Load all data sources
    print(f"📂 Loading patient conversations from '{config.CONVERSATIONS_DIR}'...")
    conversations = utils.load_json_conversations(config.CONVERSATIONS_DIR)
    
    print(f"📚 Loading knowledge base documents from '{config.KNOWLEDGE_BASE_DIR}'...")
    knowledge_docs = utils.load_knowledge_base_documents(config.KNOWLEDGE_BASE_DIR)
    
    all_docs = conversations + knowledge_docs
    if not all_docs:
        print("❌ No documents found. Exiting.")
        return
    print(f"✅ Loaded a total of {len(all_docs)} documents.")

    # 2. Chunk the documents
    print("🔪 Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(all_docs)
    print(f"✅ Split into {len(chunks)} chunks.")

    # 3. Initialize Gemini embedding model
    print(f"🧠 Initializing Gemini embedding model: '{config.EMBEDDING_MODEL}'")
    embeddings = GoogleGenerativeAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        google_api_key=config.GOOGLE_API_KEY
    )

    # 4. Store chunks in Qdrant
    print(f"💾 Storing chunks in Qdrant collection: '{config.COLLECTION_NAME}'...")
    # This will create the collection if it doesn't exist
    Qdrant.from_documents(
        documents=chunks,
        embedding=embeddings,
        host=config.QDRANT_HOST,
        port=config.QDRANT_PORT,
        collection_name=config.COLLECTION_NAME,
        #prefer_grpc=True,
    )

    print("\n🎉 Ingestion complete! Your Qdrant database is ready for queries.")

if __name__ == "__main__":
    main()