from dotenv import load_dotenv

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from langchain_groq import ChatGroq

from tools.rag_tools import retrieve_context

load_dotenv()


# ==========================================================
# LLM
# ==========================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
)


# ==========================================================
# SYSTEM PROMPT
# ==========================================================

SYSTEM_PROMPT = """
You are an expert Occupational Therapist AI Assistant.

Your role is to support therapists in clinical decision making.

Guidelines:

- Use the patient's clinical information whenever available.
- Use the current therapy plan summary whenever available.
- Use the retrieved clinical knowledge as the primary source of truth.
- If retrieved knowledge conflicts with your general knowledge, prioritize the retrieved knowledge.
- Never invent patient information.
- Never diagnose a patient.
- Never contradict the current therapy plan unless the therapist explicitly asks for alternatives.
- When suggesting activities, ensure they complement the existing therapy plan.
- Keep answers practical, evidence-informed, and concise.
- Use bullet points whenever appropriate.
"""


# ==========================================================
# PATIENT CONTEXT
# ==========================================================

def build_patient_context(patient):

    if patient is None:

        return """
Current Patient

No patient is currently loaded.

Answer as a general Occupational Therapy assistant.
"""

    concerns = patient.get("concerns", [])

    if isinstance(concerns, list):
        concerns = ", ".join(concerns)

    therapy_summary = patient.get("therapy_plan", "")

    context = f"""
Current Patient

Name:
{patient.get("name")}

Age:
{patient.get("age")}

Diagnosis:
{patient.get("diagnosis")}

Primary Concerns:
{concerns}
"""

    if therapy_summary:

        context += f"""

Current Therapy Plan Summary

{therapy_summary}
"""

    else:

        context += """

Current Therapy Plan Summary

No therapy plan has been generated yet.
"""

    return context


# ==========================================================
# BUILD RAG QUERY
# ==========================================================

def build_rag_query(question, patient):

    if patient is None:
        return question

    concerns = patient.get("concerns", [])

    if isinstance(concerns, list):
        concerns = ", ".join(concerns)

    return f"""
Diagnosis:
{patient.get("diagnosis")}

Primary Concerns:
{concerns}

Therapist Question:
{question}
"""


# ==========================================================
# BUILD CLINICAL KNOWLEDGE
# ==========================================================

def build_rag_context(question, patient):

    query = build_rag_query(question, patient)

    docs = retrieve_context(
        query=query,
        k=3
    )

    if not docs:

        return "No relevant clinical knowledge found."

    knowledge = "\n\n-----------------------------\n\n".join(docs)

    return f"""
Retrieved Clinical Knowledge

{knowledge}
"""


# ==========================================================
# CHAT
# ==========================================================

def ask_ai(
    question: str,
    patient=None,
):

    patient_context = build_patient_context(patient)

    rag_context = build_rag_context(
        question,
        patient
    )

    messages = [

        SystemMessage(
            content=SYSTEM_PROMPT
        ),

        SystemMessage(
            content=patient_context
        ),

        SystemMessage(
            content=rag_context
        ),

        HumanMessage(
            content=question
        ),
    ]

    response = llm.invoke(messages)

    return response.content