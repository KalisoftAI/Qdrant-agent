# doctor_tools/rag_logic/utils.py
import os
import json
import logging
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_json_conversations(directory_path: str):
    documents = []
    if not os.path.isdir(directory_path):
        logging.error(f"Directory not found: {directory_path}")
        return documents
        
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                full_transcript_text = "\n".join([f"{turn['speaker']}: {turn['line']}" for turn in data['transcript']])
                
                doc = Document(
                    page_content=full_transcript_text,
                    metadata={
                        'data_type': 'patient_conversation',
                        'patient_id': data.get('patient_id'),
                        'conversation_date': data.get('conversation_date'),
                        'source': filename
                    }
                )
                documents.append(doc)
                logging.info(f"Successfully loaded conversation: {filename}")
            except Exception as e:
                logging.error(f"Failed to process JSON file {filename}: {e}")
    return documents

def load_knowledge_base_documents(directory_path: str):
    if not os.path.isdir(directory_path):
        logging.error(f"Directory not found: {directory_path}")
        return []

    loader = DirectoryLoader(
        directory_path,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
        use_multithreading=True
    )
    
    try:
        documents = loader.load()
        for doc in documents:
            doc.metadata['data_type'] = 'knowledge_base'
        logging.info(f"Loaded {len(documents)} pages from knowledge base PDFs.")
        return documents
    except Exception as e:
        logging.error(f"Failed to load knowledge base documents: {e}")
        return []