from django.core.management.base import BaseCommand
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Import from our doctor_tools app
from doctor_tools.rag_logic import rag_config, utils

class Command(BaseCommand):
    help = 'Ingests patient conversations and knowledge base into Qdrant for the doctor tool.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🚀 Starting data ingestion process..."))

        # 1. Load data sources
        self.stdout.write(f"📂 Loading patient conversations from '{rag_config.CONVERSATIONS_DIR}'...")
        conversations = utils.load_json_conversations(rag_config.CONVERSATIONS_DIR)
        
        self.stdout.write(f"📚 Loading knowledge base documents from '{rag_config.KNOWLEDGE_BASE_DIR}'...")
        knowledge_docs = utils.load_knowledge_base_documents(rag_config.KNOWLEDGE_BASE_DIR)
        
        all_docs = conversations + knowledge_docs
        if not all_docs:
            self.stdout.write(self.style.ERROR("❌ No documents found. Exiting."))
            return
        self.stdout.write(self.style.SUCCESS(f"✅ Loaded a total of {len(all_docs)} documents."))

        # 2. Chunk documents
        self.stdout.write("🔪 Splitting documents into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=rag_config.CHUNK_SIZE,
            chunk_overlap=rag_config.CHUNK_OVERLAP
        )
        chunks = text_splitter.split_documents(all_docs)
        self.stdout.write(self.style.SUCCESS(f"✅ Split into {len(chunks)} chunks."))

        # 3. Initialize embedding model
        self.stdout.write(f"🧠 Initializing Gemini embedding model: '{rag_config.EMBEDDING_MODEL}'")
        embeddings = GoogleGenerativeAIEmbeddings(
            model=rag_config.EMBEDDING_MODEL,
            google_api_key=rag_config.GOOGLE_API_KEY
        )

        # 4. Store in Qdrant
        self.stdout.write(f"💾 Storing chunks in Qdrant collection: '{rag_config.COLLECTION_NAME}'...")
        Qdrant.from_documents(
            documents=chunks,
            embedding=embeddings,
            host=rag_config.QDRANT_HOST,
            port=rag_config.QDRANT_PORT,
            collection_name=rag_config.COLLECTION_NAME,
        )

        self.stdout.write(self.style.SUCCESS("\n🎉 Ingestion complete! Your Qdrant database is ready."))