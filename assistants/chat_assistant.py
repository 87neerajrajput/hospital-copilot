
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    AIMessage,
)
from prompts.chat_assistant_prompt import CHAT_SYSTEM_PROMPT

from hospital_mcp.hospital_client import mcp

# ==========================================================
# CONFIG
# ==========================================================

MAX_HISTORY = 6

# ==========================================================
# PATIENT CONTEXT
# ==========================================================

def format_list(values):

    if not values:
        return "Not Available"

    return "\n".join(f"- {v}" for v in values)

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

    assessment = patient.get("assessment_summary")

    context = f"""
    Current Patient

    Name:
    {patient.get("name")}

    Age:
    {patient.get("age")}

    Diagnosis:
    {patient.get("diagnosis")}

    """

    if assessment:

        context += f"""

        ==============================
        Assessment Summary
        ==============================

        Diagnosis Confidence:
        {assessment.get("diagnosis_confidence", "Unknown")}

        Diagnosis Reason:
        {assessment.get("diagnosis_reason", "Unknown")}

        Primary Clinical Concerns:
        {format_list(assessment.get("concerns"))}

        Clinical Findings:
        {format_list(assessment.get("clinical_findings"))}

        Sensory Findings:
        {format_list(assessment.get("sensory_findings"))}

        Communication Findings:
        {format_list(assessment.get("communication_findings"))}

        Behaviour Findings:
        {format_list(assessment.get("behavior_findings"))}

        ADL Findings:
        {format_list(assessment.get("adl_findings"))}

        Strengths:
        {format_list(assessment.get("strengths"))}

        Clinical Recommendations:
        {format_list(assessment.get("recommendations"))}
        """

    therapy_summary = patient.get("therapy_plan", "")

    if therapy_summary:

        context += f"""

        Current Therapy Plan

        {therapy_summary}
        """

    else:

        context += """

        Current Therapy Plan

        No therapy plan has been generated yet.
        """

    return context


# ==========================================================
# BUILD RAG QUERY
# ==========================================================

def build_rag_query(question, patient):

    if patient is None:
        return question

    assessment = patient.get("assessment_summary")

    therapy_summary = patient.get("therapy_plan", "")

    query = f"""
    Diagnosis
    ---------
    {patient.get("diagnosis")}

    """

    # -------------------------------------------------
    # Add Assessment only if available
    # -------------------------------------------------

    if assessment:

        query += f"""
        Diagnosis Confidence:
        {assessment.get("diagnosis_confidence", "Unknown")}

        Diagnosis Reason:
        {assessment.get("diagnosis_reason", "Unknown")}

        Assessment Findings
        -------------------

        Primary Concerns:
        {format_list(assessment.get("concerns"))}

        Clinical Findings:
        {format_list(assessment.get("clinical_findings"))}

        Sensory Findings:
        {format_list(assessment.get("sensory_findings"))}

        Communication Findings:
        {format_list(assessment.get("communication_findings"))}

        Behaviour Findings:
        {format_list(assessment.get("behavior_findings"))}

        ADL Findings:
        {format_list(assessment.get("adl_findings"))}

        Strengths:
        {format_list(assessment.get("strengths"))}
        """

    # -------------------------------------------------
    # Add Therapy Plan only if available
    # -------------------------------------------------

    if therapy_summary:

        query += f"""

        Current Therapy Plan
        --------------------

        {therapy_summary}
        """

    # -------------------------------------------------
    # Therapist Question
    # -------------------------------------------------

    query += f"""

    Therapist Question
    ------------------

    {question}
    """

    return query


# ==========================================================
# BUILD RAG CLINICAL KNOWLEDGE
# ==========================================================

async def build_rag_context(question, patient):

    if patient is None:
        return "No patient-specific clinical knowledge retrieved."

    query = build_rag_query(question, patient)

    docs = await mcp.search_knowledge(
        query=query,
        k=3,
    )

    print("\n========== MCP DOCUMENTS ==========")

    for i, doc in enumerate(docs, 1):

        print(f"\nDocument {i}\n")
        print(doc[:500])

    print("==================================\n")

    if not docs:

        return "No relevant clinical knowledge found."

    knowledge = "\n\n-----------------------------\n\n".join(docs)

    return f"""
    Retrieved Clinical Knowledge

    {knowledge}
    """


# ==========================================================
# BUILD CHAT HISTORY
# ==========================================================

def build_chat_history(messages):

    history = []

    if not messages:
        return history

    recent_messages = messages[-MAX_HISTORY:]

    for message in recent_messages:

        if message["role"] == "user":

            history.append(
                HumanMessage(
                    content=message["content"]
                )
            )

        elif message["role"] == "assistant":

            history.append(
                AIMessage(
                    content=message["content"]
                )
            )

    return history


# ==========================================================
# CHAT
# ==========================================================

async def ask_ai(
    question: str,
    patient=None,
    chat_history=None,
):

    patient_context = build_patient_context(patient)

    rag_context = await build_rag_context(
        question,
        patient
    )

    messages = [
        SystemMessage(content=CHAT_SYSTEM_PROMPT),
        SystemMessage(content=patient_context),
        SystemMessage(content=rag_context),
    ]

    messages.extend(
        build_chat_history(chat_history)
    )

    # Current Question
    messages.append(
        HumanMessage(
            content=question
        )
    )

    print("\n========== PATIENT ==========")

    if patient:
        print("Patient loaded:", patient.get("name"))

        print("\nAssessment Summary")
        print(patient.get("assessment_summary"))

        print("\nTherapy Plan")
        print(patient.get("therapy_plan"))

    else:
        print("No patient loaded.")

    print("================================\n")

    print("\n========== FINAL PROMPT ==========")

    for msg in messages:
        print("\n----------------")
        print(type(msg).__name__)
        print(msg.content)

    print("\n==================================")

    from services.llm_service import get_llm

    llm = get_llm()

    response = llm.invoke(messages)

    return response.content