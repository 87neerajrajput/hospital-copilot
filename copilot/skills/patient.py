"""
patient.py

Milestone 9.2

Patient Skill

Responsibilities
----------------
Execute patient-related business tasks.

Supported Tasks
---------------
- find_patient
- load_patient
- create_patient
- update_patient
"""

from hospital_mcp.hospital_client import HospitalMCPClient


class PatientSkill:

    def __init__(self):

        self.mcp = HospitalMCPClient()

    # ======================================================
    # EXECUTE
    # ======================================================

    async def execute(
        self,
        task: str,
        arguments: dict,
        context: dict,
    ):

        if task == "find_patient":

            return await self.find_patient(
                arguments,
                context,
            )

        elif task == "load_patient":

            return await self.load_patient(
                arguments,
                context,
            )

        elif task == "create_patient":

            return await self.create_patient(
                arguments,
                context,
            )

        elif task == "update_patient":

            return await self.update_patient(
                arguments,
                context,
            )

        raise ValueError(
            f"Unknown Patient task: {task}"
        )

    # ======================================================
    # FIND PATIENT
    # ======================================================

    async def find_patient(
        self,
        arguments: dict,
        context: dict,
    ):

        name = arguments.get("name", "")

        patients = await self.mcp.search_patients(
            search_text=name
        )

        return {

            "patients": patients

        }

    # ======================================================
    # LOAD PATIENT
    # ======================================================

    async def load_patient(
        self,
        arguments: dict,
        context: dict,
    ):

        patient_id = arguments.get("patient_id")

        patient = await self.mcp.get_patient(
            patient_id
        )

        return {

            "patient": patient

        }

    # ======================================================
    # CREATE PATIENT
    # ======================================================

    async def create_patient(
        self,
        arguments: dict,
        context: dict,
    ):

        patient_id = await self.mcp.save_patient(
            arguments
        )

        return {

            "patient_id": patient_id

        }

    # ======================================================
    # UPDATE PATIENT
    # ======================================================

    async def update_patient(
        self,
        arguments: dict,
        context: dict,
    ):

        patient_id = arguments["patient_id"]

        patient_info = arguments["patient_info"]

        success = await self.mcp.update_patient(
            patient_id=patient_id,
            patient_info=patient_info,
        )

        return {

            "success": success

        }