# core/rag_logic/chain.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from . import config

# Define the stages of our conversation
CONVERSATION_STAGES = {
    'GET_INITIAL_PROBLEM': {
        'prompt': "To start, could you please tell me about the main problem or symptoms you are experiencing?",
        'next_stage': 'ASK_DIET'
    },
    'ASK_DIET': {
        'prompt': "Thank you for sharing. Could you describe your typical daily diet? What do you usually eat for breakfast, lunch, and dinner?",
        'next_stage': 'ASK_ROUTINE'
    },
    'ASK_ROUTINE': {
        'prompt': "That's helpful. What is your daily routine like? Are you generally active, or do you have a sedentary job?",
        'next_stage': 'ASK_SLEEP'
    },
    'ASK_SLEEP': {
        'prompt': "Understood. How would you describe your sleep cycle? How many hours of sleep do you get per night on average?",
        'next_stage': 'ASK_SYMPTOMS'
    },
    'ASK_SYMPTOMS': {
        'prompt': "Lastly, could you list any other symptoms you've been feeling? For example, frequent urination, excessive thirst, unexplained weight loss, fatigue, blurred vision, or anything else, even if it seems minor like a cold or sneezing.",
        'next_stage': 'ANALYZE'
    }
}

# --- THIS IS THE CORRECTED PROMPT ---
ANALYSIS_PROMPT_TEMPLATE = """
You are an expert AI medical assistant specializing in diabetes screening.
Your task is to analyze the following conversation transcript with a patient and determine the potential severity of their condition.

**Conversation Transcript:**
{chat_history}

**Your Analysis Instructions:**

1.  **Review the entire transcript.** Pay close attention to the patient's diet, daily routine, sleep cycle, and listed symptoms.
2.  **Categorize the risk level** as either "Minor" or "Major" based on classic diabetes indicators.
3.  **Generate a response based on the category:**
    * If the risk is **"Minor"**, generate an encouraging message with a sample one-week wellness routine.
    * If the risk is **"Major"**, generate a firm, clear, and empathetic message strongly advising the patient to consult a doctor as soon as possible.

4.  **CRITICAL INSTRUCTION: Add a conclusion tag.** At the very beginning of your response, you MUST include a tag on its own line: either "[CONCLUSION: MAJOR]" if you are advising them to see a doctor, or "[CONCLUSION: MINOR]" if you are providing a wellness routine. This tag is for system use.

**Example for a Major Case:**
[CONCLUSION: MAJOR]
I understand you're experiencing several concerning symptoms. Based on our conversation, I strongly advise you to consult a doctor...

**Example for a Minor Case:**
[CONCLUSION: MINOR]
Thank you for sharing this information. While your symptoms don't point to a major issue, we can work on a wellness plan...
"""

def get_analysis_chain():
    """
    Returns a LangChain chain that takes a conversation history and performs
    the final analysis to determine if the condition is minor or major.
    """
    prompt = ChatPromptTemplate.from_template(ANALYSIS_PROMPT_TEMPLATE)
    llm = ChatGoogleGenerativeAI(model=config.LLM_MODEL, temperature=0.5)
    
    analysis_chain = (
        prompt
        | llm
        | StrOutputParser()
    )
    return analysis_chain