from mcp.server.fastmcp import FastMCP

from hospital_mcp.rag_tools import search_knowledge

from hospital_mcp.patient_tools import (
    get_patient_dashboard,
    search_patients,
    get_patient,
    get_patient_plans,
    get_therapy_plan,
    update_patient,
    save_patient,
    save_therapy_plan,
    save_report
)

import logging

logging.basicConfig(
    filename="hospital_server.log",
    level=logging.INFO,
)


# ==========================================================
# MCP SERVER
# ==========================================================

mcp = FastMCP("Hospital MCP Server")

# ==========================================================
# PATIENT SEARCH TOOLS
# ==========================================================

@mcp.tool(name="search_patients")
def search_patients_tool(search_text: str):
    """
    Search for patients by name.
    """
    return search_patients(search_text)


@mcp.tool(name="get_patient")
def get_patient_tool(patient_id: int):
    """
    Retrieve a patient by ID.
    """
    return get_patient(patient_id)


@mcp.tool(name="get_patient_plans")
def get_patient_plans_tool(patient_id: int):
    """
    Retrieve all therapy plans for a patient.
    """
    return get_patient_plans(patient_id)


# ==========================================================
# SAVE THERAPY PLAN
# ==========================================================

@mcp.tool(name="save_therapy_plan")
def save_therapy_plan_tool(
    patient_id: int,
    patient_info: dict,
    therapy_plan: dict,
):
    """
    Save a therapy plan.
    """
    return save_therapy_plan(
        patient_id,
        patient_info,
        therapy_plan,
    )

# ==========================================================
# GET THERAPY PLAN
# ==========================================================

@mcp.tool(name="get_therapy_plan")
def get_therapy_plan_tool(plan_id: int):
    """
    Retrieve a therapy plan by PLAN ID.
    """
    return get_therapy_plan(plan_id)


# ==========================================================
# UPDATE PATIENT
# ==========================================================

@mcp.tool(name="update_patient")
def update_patient_tool(
    patient_id: int,
    patient_info: dict,
):
    """
    Update patient details.
    """
    return update_patient(
        patient_id,
        patient_info,
    )


# ==========================================================
# SAVE PATIENT
# ==========================================================

@mcp.tool(name="save_patient")
def save_patient_tool(patient_info: dict):
    """
    Save a new patient.
    """
    return save_patient(patient_info)


# ==========================================================
# SAVE REPORT
# ==========================================================

@mcp.tool(name="save_report")
def save_report_tool(
    patient_id: int,
    report_type: str,
    report_content: str,
):
    """
    Save a clinical report.
    """
    return save_report(
        patient_id,
        report_type,
        report_content,
    )


@mcp.tool(name="search_knowledge")
def search_knowledge_tool(
    query: str,
    k: int = 3,
):
    """
    Search the clinical knowledge base.
    """

    logging.info("search_knowledge called")
    logging.info(query)

    return search_knowledge(
        query=query,
        k=k,
    )


@mcp.tool(name="get_patient_dashboard")
def get_patient_dashboard_tool(patient_id: int):

    return get_patient_dashboard(
        patient_id
    )

# ==========================================================
# START SERVER
# ==========================================================

if __name__ == "__main__":
    print("Starting Hospital MCP Server...")
    mcp.run()
    print("Server exited.")