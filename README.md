
# 🩺 Diabetes RAG System with Qdrant & Google Gemini

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline focused on **diabetes management**.  
It uses **Qdrant** as a vector database and **Google Gemini embeddings** for semantic search and question answering.

The application allows you to:
- 📜 **Store medical knowledge documents** like research papers and clinical guidelines.  
- 💬 **Save historical doctor–patient conversations** in structured transcript format.  
- 🔍 **Query documents and conversations intelligently** using natural language.

---

## 🚀 Features
- **Document Ingestion Pipeline**  
  Splits documents into semantic chunks and stores them in Qdrant for fast retrieval.  
- **Gemini Embeddings**  
  Uses Google Generative AI embeddings for high-quality vector representations.  
- **Vector Search with Qdrant**  
  Efficient similarity search using a modern vector database.  
- **Interactive CLI Assistant**  
  Ask questions and receive contextual answers powered by RAG.  
- **Environment-based Configuration**  
  Secure `.env` support for API keys and configurations.

---

## 🗂 Project Structure
```
Qdrant-agent/
│
├── ingest.py # Script to ingest data into Qdrant
├── app.py # Interactive CLI to query the RAG system
├── .env.example # Example environment configuration file
│
├── src/
│ ├── config.py # Project configuration variables
│ ├── utils.py # Helper functions (document loading, etc.)
│ └── chain.py # RAG chain pipeline logic
│
├── requirements.txt # Python dependencies
└── README.md # Project documentation
```
---

## 🛠 Setup Instructions

### **1. Clone the Repository**
```bash
git clone https://github.com/KalisoftAI/Qdrant-agent.git
cd Qdrant-agent
git checkout Qdrant-Vector-database
```
---

## 2. Install Qdrant (Vector Database)

Qdrant will run locally to store embeddings.

- Go to [Qdrant Releases](https://github.com/qdrant/qdrant/releases)
- Download: qdrant-x86_64-pc-windows-msvc.zip (for Windows).
- Extract the folder to your system.

```bash
Start Qdrant by running:

./qdrant.exe

```

```
Expected Output:

 _                 _     
__ _  __| |_ __ __ _ _ __ | |_ 
/ _` |/ _` | '__/ _` | '_ \| __|
| (_| | (_| | | | (_| | | | | |_ 
 \__, |\__,_|_|  \__,_|_| |_|\__|
 |___/                            

```
---
## 3. Create and Activate a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # For Windows
# OR
source venv/bin/activate  # For Linux/Mac
```
---
## 4. Install Dependencies

Install all required Python libraries:
```bash
pip install -r requirements.txt
```
---

## 5. Configure Environment Variables

Create a .env file in the project root and add the following configuration:
```bash
# Google AI Configuration
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE

# Qdrant Configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333
COLLECTION_NAME=diabetes_rag_gemini

# Model Configuration
EMBEDDING_MODEL=models/embedding-001
LLM_MODEL=gemini-1.5-flash-latest

```
Important Notes:

Replace YOUR_GOOGLE_API_KEY_HERE with your actual Google API key.
Add .env to .gitignore to prevent committing sensitive information.

Example .gitignore:
```bash
.env
venv/
__pycache__/
*.log
```
---

## 7. Ingest Data into Qdrant

Run the ingestion script to process and store documents:
```bash
python ingest.py
```

What Happens:
- Documents are loaded from data/general and data/patients.
- Documents are split into semantic chunks.
- Gemini embeddings are generated for each chunk.
- Embeddings are stored in Qdrant.


Expected Output:
```bash
🚀 Starting data ingestion process with Gemini embeddings...
📂 Loading documents...
✅ Loaded 25 documents.
Splitting documents into chunks...
✅ Split documents into 120 chunks.
🧠 Initializing Gemini embedding model: 'models/embedding-001'
💾 Storing chunks in Qdrant collection: 'diabetes_rag_gemini'...
🎉 Ingestion complete! Your Qdrant database is ready.
```
---

## 8. Run the RAG CLI Assistant

Start the interactive chatbot:
```bash
python app.py
```

Example session:
```bash
🤖 Initializing Diabetes RAG Assistant...
✅ Assistant is ready. Ask your questions below.
   (Type 'exit' or 'quit' to end the session)

> Question: What are the common symptoms of type 2 diabetes?

🧠 Thinking...

💡 Answer:
Type 2 diabetes symptoms include increased thirst, frequent urination, fatigue, blurred vision, and slow-healing wounds.

🗃 Workflow Overview

Qdrant Server → Runs locally to store and retrieve vector embeddings.

Ingest Script (ingest.py) → Processes data and populates Qdrant.

Query Interface (app.py) → Uses the RAG pipeline to provide answers from stored data.
```
---
## 🧪 Tech Stack

- Python 3.10+
- LangChain – RAG pipeline
- Qdrant – Vector database
- Google Gemini – Embedding & LLM models
- RecursiveCharacterTextSplitter – For efficient document chunking

---

## 🧾 Example Query Flow

User asks a question:
```bash
What are the treatment options for type 2 diabetes?

The query is embedded and matched with the closest chunks in Qdrant.

Relevant chunks are retrieved and passed to Gemini LLM.

The assistant generates a detailed, context-aware answer.
```
