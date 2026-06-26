import os
from typing import List
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from graph.state import HealthcareState
from langchain_core.messages import SystemMessage, HumanMessage

from tools.db_tools import save_patient, update_patient

load_dotenv()

# 1. Define the structural schema using Pydantic
class PatientProfile(BaseModel):
    name: str = Field(description="First or full name of the child")
    age: int = Field(description="Current age of the child in years")
    diagnosis: str = Field(description="Primary clinical or developmental diagnosis")
    concerns: List[str] = Field(description="Specific areas of concern or struggle")

# 2. Initialize the Groq model
# Low temperature (0) keeps the extraction strict and deterministic
llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0
)

# 3. Create the structured wrapper
# This forces the LLM to output data fitting the Pydantic schema perfectly
structured_llm = llm.with_structured_output(PatientProfile)


def intake_agent(state: HealthcareState):

    print("\n=== Intake Agent ===")

    profile = structured_llm.invoke([
        SystemMessage(content="""
        You are a clinical intake assistant.

            Extract:
            - name
            - age
            - diagnosis
            - concerns

        """),
        HumanMessage(content=state['user_query'])
    ])

    patient_info = profile.model_dump()

    print("\nExtracted Patient Info:")
    print(patient_info)

    #patient_id = save_patient(patient_info)

    if state.get("patient_id"):
        
        patient_id = state["patient_id"]
        update_patient(patient_id, patient_info)

    else:
        patient_id = save_patient(patient_info)

    return {
        "patient_info": patient_info,
        "patient_id": patient_id
    }


