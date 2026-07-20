import asyncio
from hospital_mcp.hospital_client import mcp

class HospitalService:

    # ==========================================================
    # Knowledge Base
    # ==========================================================

    @staticmethod
    def search_knowledge(query: str):

        return asyncio.run(
            mcp.search_knowledge(
                query
            )
        )
    

    # ==========================================================
    # Patient
    # ==========================================================

    @staticmethod
    def search_patients(search_text: str):

        return asyncio.run(
            mcp.search_patients(search_text)
        )
    
    @staticmethod
    def get_patient(patient_id: int):

        return asyncio.run(
            mcp.get_patient(patient_id)
        )
    
    @staticmethod
    def update_patient(patient_id: int, patient_info: dict):

        return asyncio.run(
            mcp.update_patient(
                patient_id,
                patient_info,
            )
        )

    @staticmethod
    def save_patient(patient_info: dict):

        return asyncio.run(
            mcp.save_patient(patient_info)
        )
    

    # ==========================================================
    # Therapy Plans
    # ==========================================================

    @staticmethod
    def get_patient_plans(patient_id: int):

        return asyncio.run(
            mcp.get_patient_plans(patient_id)
        )
    
    @staticmethod
    def get_patient_plans_with_details(patient_id: int):

        return asyncio.run(
            mcp.get_patient_plans_with_details(patient_id)
        )
    
    @staticmethod
    def get_therapy_plan(plan_id: int):

        return asyncio.run(
            mcp.get_therapy_plan(plan_id)
        )

    @staticmethod
    def save_therapy_plan(patient_id: int, patient_info: dict, therapy_plan: dict):

        return asyncio.run(
            mcp.save_therapy_plan(
                patient_id,
                patient_info,
                therapy_plan,
            )
        )
    

    # ==========================================================
    # Reports
    # ==========================================================
    
    @staticmethod
    def save_report(patient_id: int, report_type: str, report_content: str):

        return asyncio.run(
            mcp.save_report(
                patient_id,
                report_type,
                report_content,
            )
        )
    

    # ==========================================================
    # Dashboard
    # ==========================================================

    @staticmethod
    def get_patient_dashboard(patient_id: int):

        return asyncio.run(
            mcp.get_patient_dashboard(
                patient_id
            )
        )

    


    