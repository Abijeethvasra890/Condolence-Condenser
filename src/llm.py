from langchain_groq import ChatGroq
from src.config import GROQ_API_KEY, GROQ_MODEL

def get_llm(temperature: float = 0.2) -> ChatGroq:
    """
    Create a Groq Chat LLM client via LangChain.
    """
    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=temperature,
    )
