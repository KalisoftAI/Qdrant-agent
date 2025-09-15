from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Import configurations and utility functions from the current package
from . import config, utils

def main():
    """
    Main function to perform data ingestion, chunking, embedding, and storage.
    """
    print("🚀 Starting data ingestion process with Gemini embeddings...")

    # 1. Load documents
    print(f"📂 Loading documents...")
    all_docs = utils.load_documents(config.DATA_DIR_GENERAL) + utils.load_documents(config.DATA_DIR_PATIENTS)
    if not all_docs:
        print("No documents found. Exiting.")
        return
    print(f"✅ Loaded {len(all_docs)} documents.")

    # 2. Chunk the documents
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(all_docs)
    print(f"✅ Split documents into {len(chunks)} chunks.")

    # 3. Initialize Gemini embedding model
    print(f"🧠 Initializing Gemini embedding model: '{config.EMBEDDING_MODEL}'")
    embeddings = GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL) # <-- Changed instantiation

    # 4. Store chunks in Qdrant
    print(f"💾 Storing chunks in Qdrant collection: '{config.COLLECTION_NAME}'...")
    Qdrant.from_documents(
        documents=chunks,
        embedding=embeddings,
        host=config.QDRANT_HOST,
        port=config.QDRANT_PORT,
        collection_name=config.COLLECTION_NAME,
        prefer_grpc=True,
    )

    print("🎉 Ingestion complete! Your Qdrant database is ready.")

if __name__ == "__main__":
    main()