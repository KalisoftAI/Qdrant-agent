import os
import logging
import base64
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from . import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def image_to_base64(image_path):
    """Converts an image file to a base64 encoded string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def load_documents(directory_path: str):
    """
    Loads documents from the specified directory.
    - PDFs are loaded with PyPDFLoader.
    - Images (PNG, JPG) are processed using Gemini Vision for OCR.
    """
    documents = []
    if not os.path.isdir(directory_path):
        logging.error(f"Directory not found: {directory_path}")
        return documents

    # Initialize the Gemini model for OCR tasks
    # We use gemini-1.5-flash as it's fast, cheap, and has vision capabilities
    llm_vision = ChatGoogleGenerativeAI(model=config.LLM_MODEL, temperature=0)

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if filename.lower().endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
                logging.info(f"Loaded PDF: {filename}")

            elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
                logging.info(f"Processing image with Gemini: {filename}...")
                
                # Convert image to base64
                b64_image = image_to_base64(file_path)

                # Create the message for the Gemini API
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Extract all text from this image. Preserve the original layout and formatting as much as possible."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
                        ],
                    }
                ]
                
                # Invoke the model and get the response
                response = llm_vision.invoke(messages)
                extracted_text = response.content
                
                # Create a LangChain Document object
                doc = Document(page_content=extracted_text, metadata={"source": file_path})
                documents.append(doc)
                logging.info(f"Successfully extracted text from {filename}")

        except Exception as e:
            logging.error(f"Failed to load or process {filename}: {e}")
            
    return documents