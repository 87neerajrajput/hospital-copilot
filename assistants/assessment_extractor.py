import json
import re
from pydantic import BaseModel
from services.llm_service import llm

# ======================================================
# Output Schema
# ======================================================

class AssessmentSummary(BaseModel):

    name: str

    age: int

    diagnosis: str

    diagnosis_confidence: str

    diagnosis_reason: str

    concerns: list[str]

    clinical_findings: list[str]

    sensory_findings: list[str]

    communication_findings: list[str]

    behavior_findings: list[str]

    adl_findings: list[str]

    strengths: list[str]

    recommendations: list[str]


# ======================================================
# Prompt Builder
# ======================================================

def build_prompt(document: str) -> str:

    return f"""
    You are an expert Pediatric Occupational Therapist.

    Your task is to extract structured clinical information from a Developmental Assessment Report.

    Return ONLY valid JSON.

    Do NOT return markdown.

    Do NOT explain anything.

    Do NOT use ```.

    Return ONLY one JSON object.

    Expected JSON format

    {{
        "name":"Patient Name",

        "age":4,

        "diagnosis":"Autism Spectrum Disorder",

        "diagnosis_confidence":"High",

        "diagnosis_reason":"Diagnosis explicitly stated in the report.",

        "concerns":[
            "Poor eye contact",
            "Poor joint attention"
        ],

        "clinical_findings":[
            "Delayed developmental milestones",
            "Reduced attention span"
        ],

        "sensory_findings":[
            "Poor sensory regulation",
            "Sensory seeking behaviour"
        ],

        "communication_findings":[
            "Delayed expressive language",
            "Poor receptive language"
        ],

        "behavior_findings":[
            "Hyperactivity",
            "Difficulty coping with transitions"
        ],

        "adl_findings":[
            "Requires assistance with dressing",
            "Difficulty feeding independently"
        ],

        "strengths":[
            "Responds well to visual cues",
            "Good imitation skills"
        ],

        "recommendations":[
            "Occupational Therapy",
            "Speech Therapy"
        ]
    }}

    --------------------------------------------------------

    Diagnosis Rules

    1. If a CURRENT diagnosis is explicitly mentioned, use it.

    2. Ignore Birth History Medical Diagnosis if it is:
    - Nil
    - None
    - Unknown
    - Not specified

    3. If no current diagnosis is provided, infer the MOST LIKELY developmental diagnosis from the assessment findings.

    Possible diagnoses include:

    - Autism Spectrum Disorder
    - ADHD
    - Global Developmental Delay
    - Developmental Delay
    - Cerebral Palsy
    - Down Syndrome
    - Sensory Processing Disorder
    - Intellectual Disability

    4. If diagnosis cannot reasonably be inferred, return:

    "Unknown"

    --------------------------------------------------------

    Diagnosis Confidence

    Return one of:

    - High
    - Medium
    - Low

    High:
    Diagnosis explicitly stated.

    Medium:
    Strong clinical evidence supports the diagnosis.

    Low:
    Only partial evidence is available.

    --------------------------------------------------------

    Diagnosis Reason

    Provide one short sentence explaining why the diagnosis was selected.

    Examples:

    "Diagnosis explicitly stated in the report."

    "Diagnosis inferred from persistent social communication deficits and restricted behaviours."

    --------------------------------------------------------

    Concern Rules

    Extract ONLY the child's major functional concerns.

    Priority:

    1. Parent Concerns
    2. Functional limitations
    3. Important therapist observations

    Merge duplicate concerns.

    Examples:

    - Poor eye contact
    - Poor sitting tolerance
    - Hyperactivity
    - Delayed speech
    - Poor sensory regulation
    - Poor social interaction

    --------------------------------------------------------

    Clinical Findings

    Extract important clinical observations such as:

    - Developmental delays
    - Motor planning difficulties
    - Attention difficulties
    - Fine motor deficits
    - Gross motor deficits
    - Play skill deficits
    - Cognitive observations

    Return an empty list if none are present.

    --------------------------------------------------------

    Sensory Findings

    Extract sensory observations including:

    - Sensory seeking
    - Sensory avoiding
    - Vestibular issues
    - Proprioceptive issues
    - Tactile defensiveness
    - Poor sensory regulation

    Return an empty list if none are present.

    --------------------------------------------------------

    Communication Findings

    Extract communication observations including:

    - Delayed speech
    - Receptive language difficulties
    - Expressive language difficulties
    - Echolalia
    - Poor joint attention
    - Pragmatic language deficits

    Return an empty list if none are present.

    --------------------------------------------------------

    Behavior Findings

    Extract behavioural observations including:

    - Hyperactivity
    - Impulsivity
    - Poor transitions
    - Emotional dysregulation
    - Aggression
    - Self-injurious behaviour
    - Repetitive behaviours
    - Poor compliance

    Return an empty list if none are present.

    --------------------------------------------------------

    ADL Findings

    Extract functional daily living difficulties including:

    - Feeding
    - Dressing
    - Toileting
    - Grooming
    - Sleep
    - School participation

    Return an empty list if none are present.

    --------------------------------------------------------

    Strengths

    Extract positive abilities including:

    - Good imitation
    - Visual learning
    - Social strengths
    - Interests
    - Motivation
    - Family support

    Return an empty list if none are present.

    --------------------------------------------------------

    Recommendations

    Extract only major therapy recommendations mentioned in the report.

    Examples:

    - Occupational Therapy
    - Speech Therapy
    - Behaviour Therapy
    - Sensory Integration
    - Parent Training
    - School Readiness

    Return an empty list if none are present.

    --------------------------------------------------------

    Do NOT include

    - Hospital information
    - Addresses
    - Phone numbers
    - Therapist names
    - Signatures
    - Dates
    - Billing information

    --------------------------------------------------------

    If any field is unavailable, return:

    - Empty string ("") for text fields.
    - Empty list ([]) for list fields.

    Never invent information.

    --------------------------------------------------------

    Developmental Assessment Report

    {document}
    """


# ======================================================
# JSON Extractor
# ======================================================

def extract_json(text: str):

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if not match:

        raise ValueError(
            "LLM did not return JSON."
        )

    return match.group()


# ======================================================
# Main Function
# ======================================================

def extract_assessment_information(
    document: str,
) -> AssessmentSummary:

    prompt = build_prompt(document)

    # -------- DEBUG --------
    # print("\n========== PROMPT ==========\n")
    # print(prompt[:2500])
    # print("\n============================\n")

    response = llm.invoke(prompt)

    # -------- DEBUG --------
    # print("\n========== RAW RESPONSE ==========\n")
    # print(response.content)
    # print("\n==================================\n")

    json_text = extract_json(
        response.content
    )

    data = json.loads(
        json_text
    )

    return AssessmentSummary.model_validate(
        data
    )