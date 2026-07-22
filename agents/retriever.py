
def retrieval_agent(state):

    from tools.rag_tools import retrieve_context

    diagnosis = state["patient_info"]["diagnosis"]

    concerns = ", ".join(
        state["patient_info"]["concerns"]
    )

    query = f"{diagnosis} {concerns}"

    docs = retrieve_context(query)

    return {
        "retrieved_docs": docs
    }