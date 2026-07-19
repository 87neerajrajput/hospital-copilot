
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# ==========================================================
# Loading API KEY
# ==========================================================

load_dotenv()

# ==========================================================
# Shared LLM
# ==========================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)