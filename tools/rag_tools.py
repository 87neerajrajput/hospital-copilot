#from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = str(BASE_DIR / "chroma_db")

#CHROMA_DIR = "chroma_db"

print("CHROMA EXISTS:", os.path.exists(CHROMA_DIR))

_embeddings = None
_vector_store = None

def get_vector_store():
    global _embeddings, _vector_store
    

    if _vector_store is None:
        print("Loading Gemini model...")
        _embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )
        print("Gemini Embedding model loaded.")

        _vector_store = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=_embeddings,
        )

    return _vector_store


def retrieve_context(query: str, k: int = 2):
    vector_store = get_vector_store()

    docs = vector_store.similarity_search(
        query=query,
        k=k
    )

    context = []

    for doc in docs:
        context.append(doc.page_content)

    return context