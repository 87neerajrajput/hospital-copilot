from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


CHROMA_DIR = "chroma_db"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vector_store = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embeddings
)


def retrieve_context(query: str, k: int = 2):

    docs = vector_store.similarity_search(
        query=query,
        k=k
    )

    context = []

    for doc in docs:
        context.append(doc.page_content)

    return context