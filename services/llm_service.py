
from functools import lru_cache

@lru_cache(maxsize=1)
def get_llm():

    from dotenv import load_dotenv
    from langchain_groq import ChatGroq

    load_dotenv()

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
    )