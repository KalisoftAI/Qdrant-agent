import qdrant_client
from langchain_community.vectorstores import Qdrant
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI # <-- Changed imports
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from . import config

def get_rag_chain():
    """
    Initializes and returns a RAG chain powered by Google Gemini.
    """
    # 1. Initialize Gemini Embeddings and Vector Store
    embeddings = GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL) # <-- Changed to Gemini
    
    client = qdrant_client.QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)
    
    vector_store = Qdrant(
        client=client,
        collection_name=config.COLLECTION_NAME,
        embeddings=embeddings
    )
    
    retriever = vector_store.as_retriever(search_kwargs={"k": 10})

    # 2. Define the Prompt Template (no change needed here)
    prompt_template = """
    You are an intelligent assistant for healthcare professionals.
    Use the following retrieved context to answer the question.
    If you don't know the answer from the context, clearly state that the information is not available in the provided documents.
    Do not invent information. Your answer must be based solely on the context.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)

    # 3. Initialize the Gemini LLM
    llm = ChatGoogleGenerativeAI(model=config.LLM_MODEL, temperature=0.3) # <-- Changed to Gemini

    # 4. Define a function to format the retrieved documents
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # 5. Build the RAG chain using LCEL
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain