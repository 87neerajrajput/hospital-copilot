from dotenv import load_dotenv

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from langchain_groq import ChatGroq

load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
)


SYSTEM_PROMPT = """
You are an expert Occupational Therapist AI Assistant.

Your role is to assist therapists during clinical decision making.

You have expertise in:

- Autism Spectrum Disorder
- ADHD
- Cerebral Palsy
- Down Syndrome
- Sensory Integration
- Feeding Therapy
- Speech & Language Therapy
- School Readiness
- Fine Motor Skills
- Gross Motor Skills

Guidelines:

- Use the current patient information whenever available.
- Use the current therapy plan summary whenever available.
- Never invent patient information.
- Never diagnose a patient.
- Never contradict the existing therapy plan unless explicitly asked.
- When suggesting new activities, ensure they complement the current therapy plan.
- Give practical, evidence-informed recommendations.
- Use bullet points whenever appropriate.
- Keep answers concise and clinically useful.
"""


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

    therapy_plan = patient.get("therapy_plan")

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

    if therapy_plan:

        context += f"""

        Current Therapy Plan Summary:

        {therapy_plan}
        """

    else:

        context += """

        Current Therapy Plan Summary:

        No therapy plan has been generated yet.
        """

    return context


def ask_ai(question: str, patient=None):

    patient_context = build_patient_context(patient)

    messages = [

        SystemMessage(
            content=SYSTEM_PROMPT
        ),

        SystemMessage(
            content=patient_context
        ),

        HumanMessage(
            content=question
        ),
    ]

    response = llm.invoke(messages)

    return response.content