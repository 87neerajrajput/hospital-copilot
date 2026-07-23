
_embeddings = None
_vector_store = None

def get_vector_store():

    global _embeddings, _vector_store

    if _vector_store is None:

        from config.settings import CHROMA_DIR, EMBEDDING_MODEL

        from config.logging import get_logger

        logger = get_logger(__name__)

        logger.info("CHROMA DB EXISTS:  %s", CHROMA_DIR)

        logger.info("Loading embedding model:  %s", EMBEDDING_MODEL)

        from langchain_chroma import Chroma
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        _embeddings = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL
        )

        logger.info("Embedding model loaded.")

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