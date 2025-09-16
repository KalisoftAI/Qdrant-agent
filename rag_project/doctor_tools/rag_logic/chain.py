# doctor_tools/rag_logic/chain.py
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Qdrant
import qdrant_client

from . import rag_config

def get_doctor_rag_chain():
    client = qdrant_client.QdrantClient(host=rag_config.QDRANT_HOST, port=rag_config.QDRANT_PORT)
    embeddings = GoogleGenerativeAIEmbeddings(
        model=rag_config.EMBEDDING_MODEL,
        google_api_key=rag_config.GOOGLE_API_KEY
    )
    qdrant_vector_store = Qdrant(
        client=client,
        collection_name=rag_config.COLLECTION_NAME,
        embeddings=embeddings
    )
    retriever = qdrant_vector_store.as_retriever(search_kwargs={"k": 5})

    template = """
    You are an expert clinical assistant AI for diabetes management.
    Your task is to analyze the provided context, which includes patient conversation transcripts and medical knowledge,
    and answer the user's question. Based on the analysis, provide clear, actionable insights for a doctor.

    CONTEXT:
    {context}

    QUESTION: {question}

    Based on the context and question, provide a structured response with the following sections:

    **1. Summary of Key Information:**
    Briefly summarize the patient's current status, symptoms, and relevant history from the provided context.

    **2. Actionable Insights & Recommendations:**
    - **Drug Changes:** Suggest any specific changes to medication (e.g., "Consider increasing Metformin to 1000mg twice daily," or "Evaluate adding a GLP-1 agonist."). Justify each suggestion.
    - **Monitoring & Follow-up Tests:** Recommend necessary tests or monitoring (e.g., "Order a new HbA1c test," or "Recommend patient to monitor blood glucose levels 4 times daily.").
    - **Potential Warnings:** Highlight any potential drug interactions, complications, or red-flag symptoms that require immediate attention.

    **3. Detailed Answer:**
    Provide a comprehensive answer to the original question, integrating information from the context.
    """
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    llm = ChatGoogleGenerativeAI(
        model=rag_config.LLM_MODEL,
        temperature=0.3,
        google_api_key=rag_config.GOOGLE_API_KEY
    )

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain