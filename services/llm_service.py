
from functools import lru_cache

@lru_cache(maxsize=1)
def get_llm():

    from langchain_groq import ChatGroq
    from config.settings import LLM_MODEL, LLM_TEMPERATURE
    
    return ChatGroq(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
    )