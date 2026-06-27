from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = str(BASE_DIR / "chroma_db")

#CHROMA_DIR = "chroma_db"

print("CHROMA EXISTS:", os.path.exists(CHROMA_DIR))

_embeddings = None
_vector_store = None

def get_vector_store():
    global _embeddings, _vector_store
    

    if _vector_store is None:
        print("Loading HuggingFace model...")
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        print("Embedding model loaded.")

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