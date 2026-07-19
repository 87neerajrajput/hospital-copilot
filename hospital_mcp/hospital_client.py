import json
from datetime import datetime
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class HospitalMCPClient:

    def __init__(self):

        self.server = StdioServerParameters(
            command="uv",
            args=[
                "run",
                "python",
                "-m",
                "hospital_mcp.hospital_server",
            ],
        )

    # ==========================================================
    # Generic MCP Tool Caller
    # ==========================================================

    async def _call_tool(
        self,
        tool_name: str,
        arguments: dict,
    ):

        async with stdio_client(self.server) as (read, write):

            async with ClientSession(read, write) as session:

                await session.initialize()

                result = await session.call_tool(
                    tool_name,
                    arguments,
                )

                return result

    # ==========================================================
    # Knowledge Search
    # ==========================================================

    async def search_knowledge(
        self,
        query: str,
        k: int = 3,
    ):

        result = await self._call_tool(

            "search_knowledge",

            {
                "query": query,
                "k": k,
            },
        )

        try:

            if result.content:

                payload = json.loads(
                    result.content[0].text
                )

                return payload.get(
                    "documents",
                    []
                )

        except Exception as e:

            print(f"MCP search_knowledge error: {e}")

        return []

    # ==========================================================
    # Patient Search
    # ==========================================================

    async def search_patients(self, search_text: str):

        result = await self._call_tool(
            "search_patients",
            {
                "search_text": search_text,
            },
        )

        patients = []

        for item in result.content:
            patients.append(json.loads(item.text))

        return patients


    # ==========================================================
    # Get Patient
    # ==========================================================

    async def get_patient(self, patient_id: int):

        result = await self._call_tool(
            "get_patient",
            {
                "patient_id": patient_id,
            },
        )

        if result.content:
            return json.loads(result.content[0].text)

        return None

    # ==========================================================
    # Get Patient Plans
    # ==========================================================

    async def get_patient_plans(self, patient_id: int):

        result = await self._call_tool(
            "get_patient_plans",
            {
                "patient_id": patient_id,
            },
        )

        patient_plans = []

        if result.content:

            for item in result.content:

                plan = json.loads(item.text)

                # Convert ISO datetime string back to datetime object
                if plan.get("created_at"):
                    plan["created_at"] = datetime.fromisoformat(
                        plan["created_at"]
                    )

                patient_plans.append(plan)

        return patient_plans
    

    # ==========================================================
    # GET THERAPY PLAN WITH THERPAY DETAILS
    # ==========================================================

    async def get_patient_plans_with_details(
        self,
        patient_id: int,
    ):

        patient_plans = await self.get_patient_plans(
            patient_id
        )

        detailed_plans = []

        for plan in patient_plans:

            therapy_plan = await self.get_therapy_plan(
                plan["id"]
            )

            if therapy_plan:

                detailed_plans.append({

                    "id": plan["id"],

                    "created_at": plan["created_at"],

                    "therapy_plan": therapy_plan["therapy_plan"],

                })

        return detailed_plans


    # ==========================================================
    # GET THERAPY PLAN
    # ==========================================================

    async def get_therapy_plan(self, plan_id: int):

        result = await self._call_tool(
            "get_therapy_plan",
            {
                "plan_id": plan_id,
            },
        )

        if result.content:

            plan = json.loads(result.content[0].text)

            # Convert timestamps back into datetime
            if plan.get("created_at"):
                plan["created_at"] = datetime.fromisoformat(
                    plan["created_at"]
                )

            if plan.get("updated_at"):
                plan["updated_at"] = datetime.fromisoformat(
                    plan["updated_at"]
                )

            return plan

        return None
    

    # ==========================================================
    # UPDATE PATIENT
    # ==========================================================

    async def update_patient(
        self,
        patient_id: int,
        patient_info: dict,
    ):

        result = await self._call_tool(
            "update_patient",
            {
                "patient_id": patient_id,
                "patient_info": patient_info,
            },
        )

        if result.content:
            return json.loads(result.content[0].text)

        return {
            "success": False,
            "message": "Unknown MCP error."
        }
    

    # ==========================================================
    # SAVE PATIENT
    # ==========================================================

    async def save_patient(
        self,
        patient_info: dict,
    ):

        result = await self._call_tool(
            "save_patient",
            {
                "patient_info": patient_info,
            },
        )

        if result.content:
            return json.loads(result.content[0].text)

        return {
            "success": False,
            "message": "Unknown MCP error."
        }
    


    # ==========================================================
    # SAVE THERAPY PLAN
    # ==========================================================

    async def save_therapy_plan(
        self,
        patient_id: int,
        patient_info: dict,
        therapy_plan: dict,
    ):

        result = await self._call_tool(
            "save_therapy_plan",
            {
                "patient_id": patient_id,
                "patient_info": patient_info,
                "therapy_plan": therapy_plan,
            },
        )

        if result.content:
            return json.loads(result.content[0].text)

        return {
            "success": False,
            "message": "Unknown MCP error."
        }
    

    # ==========================================================
    # SAVE REPORT
    # ==========================================================

    async def save_report(
        self,
        patient_id: int,
        report_type: str,
        report_content: str,
    ):

        result = await self._call_tool(
            "save_report",
            {
                "patient_id": patient_id,
                "report_type": report_type,
                "report_content": report_content,
            },
        )

        if result.content:
            return json.loads(result.content[0].text)

        return {
            "success": False,
            "message": "Unknown MCP error."
        }


    # ==========================================================
    # Dashboard
    # ==========================================================

    async def get_patient_dashboard(self, patient_id: int):

        result = await self._call_tool(
            "get_patient_dashboard",
            {
                "patient_id": patient_id,
            },
        )

        if not result.content:
            return None

        dashboard = json.loads(result.content[0].text)

        # ------------------------------------------
        # Convert datetime strings
        # ------------------------------------------

        for plan in dashboard.get("plans", []):

            if plan.get("created_at"):

                plan["created_at"] = datetime.fromisoformat(
                    plan["created_at"]
                )

        return dashboard


# ==========================================================
# Shared MCP Client (Singleton)
# ==========================================================

mcp = HospitalMCPClient() 