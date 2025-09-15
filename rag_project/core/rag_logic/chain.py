import qdrant_client
from langchain_community.vectorstores import Qdrant
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from . import config # <-- Relative import

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
    You are an intelligent healthcare assistant specialized in diabetes care.
    Use the following retrieved context to answer the user’s question:

    Context: {context}
    Question: {question}

    Instructions:

    Base your answer strictly on the information provided in the context (related to diabetes symptoms, complications, treatments, lifestyle management, or medications).

    If the answer is not available in the context, clearly state: “The information is not available in the provided documents.”

    Do not invent or assume information beyond the given context.

    If the context indicates that the patient has major symptoms of diabetes or related complications (e.g., severe fatigue, blurred vision, chest pain, high/low blood sugar emergencies, foot ulcers), advise them to seek immediate doctor’s consultation or go to the hospital.

    After providing the answer, politely ask: “Would you like me to help you book an appointment with a diabetes specialist?”

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