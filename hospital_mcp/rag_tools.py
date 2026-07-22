
def search_knowledge(query: str, k: int = 3):

    """
    Search the clinical knowledge base.

    Returns the most relevant knowledge chunks.
    """

    from tools.rag_tools import retrieve_context

    docs = retrieve_context(
        query=query,
        k=k
    )

    return {
        "documents": docs
    }