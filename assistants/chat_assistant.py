from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)
from dotenv import load_dotenv

load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
)


SYSTEM_PROMPT = """
You are an expert Occupational Therapist AI Assistant.

Your role is to assist therapists by providing
evidence-informed clinical suggestions.

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

- Always answer clinically.
- Use clear bullet points whenever appropriate.
- Keep answers practical and therapist-focused.
- Never invent facts.
- Never diagnose patients.
- If uncertain, clearly mention the limitation.
"""


def ask_ai(question: str, history: list | None = None) -> str:

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=question),
    ]

    response = llm.invoke(messages)

    return response.content