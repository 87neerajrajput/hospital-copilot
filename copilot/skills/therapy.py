"""
therapy.py

Milestone 9.2

Therapy Skill

Responsibilities
----------------
Execute therapy-related business tasks.

Supported Tasks
---------------
- generate_therapy_plan
- load_latest_plan
- save_plan
"""

from agents.planner import planning_agent

from graph.state import HealthcareState

from hospital_mcp.hospital_client import mcp


class TherapySkill:

    def __init__(self):

        self.mcp = mcp

    # ======================================================
    # EXECUTE
    # ======================================================

    async def execute(
        self,
        task: str,
        arguments: dict,
        context: dict,
    ):

        if task == "generate_therapy_plan":

            return await self.generate_therapy_plan(
                arguments,
                context,
            )
        
        elif task == "load_patient_plans":

            patient_id = arguments["patient_id"]

            intent = context.get("intent")

            if intent in {
                "therapy_evolution",
                "therapy_trend",
            }:

                plans = await self.mcp.get_patient_plans_with_details(
                    patient_id
                )

            else:

                plans = await self.mcp.get_patient_plans(
                    patient_id
                )

            return {
                "therapy_plan_list": plans
            }
        
        
        elif task == "build_clinical_memory":

            return await self.build_clinical_memory(
                arguments,
                context,
            )

        elif task == "load_latest_plan":

            return await self.load_latest_plan(
                arguments,
                context,
            )
        
        elif task == "load_selected_plans":

            return await self.load_selected_plans(
                arguments,
                context,
            )

        elif task == "save_plan":

            return await self.save_plan(
                arguments,
                context,
            )

        raise ValueError(
            f"Unknown Therapy task: {task}"
        )

    # ======================================================
    # GENERATE THERAPY PLAN
    # ======================================================

    async def generate_therapy_plan(
        self,
        arguments: dict,
        context: dict,
    ):

        patient = context.get("patient")

        if patient is None:

            raise ValueError(
                "Patient not available in execution context."
            )

        assessment_summary = context.get(
            "assessment_summary",
            {}
        )

        knowledge = context.get(
            "knowledge",
            []
        )

        clinical_memory = context.get(
            "clinical_memory",
            {},
        )

        state = HealthcareState(

            patient_form=None,

            user_query="",

            assessment_summary=assessment_summary,

            patient_info=patient,

            patient_id=patient["id"],

            clinical_memory=clinical_memory,

            therapy_plan=None,

            plan_id=None,

            retrieved_docs=knowledge,

            qa_result=None,

            approval_status=None,

            report_types=None,

            clinical_report=None,

            parent_report=None,

            clinical_report_id=None,

            parent_report_id=None,

            next_agent="",

        )

        result = await planning_agent(state, auto_save=False)

        return result

    # ======================================================
    # LOAD LATEST PLAN
    # ======================================================

    async def load_latest_plan(
        self,
        arguments: dict,
        context: dict,
    ):

        plan_id = arguments["plan_id"]

        therapy_plan = await self.mcp.get_therapy_plan(
            plan_id
        )

        return {

            "therapy_plan": therapy_plan["therapy_plan"],

            "plan_id": plan_id,

        }
    
    # ======================================================
    # LOAD SELECTED PLANS
    # ======================================================

    async def load_selected_plans(
        self,
        arguments: dict,
        context: dict,
    ):

        plans = context.get("therapy_plan_list", [])

        if not plans:
            raise ValueError("No therapy plans available.")

        left = str(arguments["left_plan_selector"]).strip().lower()
        right = str(arguments["right_plan_selector"]).strip().lower()

        import re

        def resolve_selector(selector):

            if selector == "latest":
                return plans[0]

            if selector == "previous":
                return plans[1] if len(plans) > 1 else plans[0]

            match = re.search(r"\d+", selector)

            if match:

                plan_id = int(match.group())

                for plan in plans:

                    if plan["id"] == plan_id:
                        return plan

            return None


        left_plan = resolve_selector(left)
        right_plan = resolve_selector(right)

        selected = []

        for plan in (left_plan, right_plan):

            if plan is None:
                continue

            therapy_plan = await self.mcp.get_therapy_plan(plan["id"])

            selected.append({

                "plan_id": plan["id"],

                "created_at": plan.get("created_at"),

                "therapy_plan": therapy_plan["therapy_plan"]

            })

        if len(selected) != 2:

            raise ValueError(
                "Unable to load both selected therapy plans."
            )

        return {
            "selected_plans": selected
        }
    

    # ======================================================
    # BUILD CLINICAL MEMORY
    # ======================================================

    async def build_clinical_memory(
        self,
        arguments: dict,
        context: dict,
    ):

        plans = context.get(
            "therapy_plan_list",
            [],
        )

        latest_plan = None

        if plans:

            latest_plan = await self.mcp.get_therapy_plan(
                plans[0]["id"]
            )

        return {

            "clinical_memory": {

                "latest_therapy_plan": latest_plan

            }

        }


    # ======================================================
    # SAVE PLAN
    # ======================================================

    async def save_plan(
        self,
        arguments: dict,
        context: dict,
    ):

        patient = context.get("patient")

        therapy_plan = context.get("therapy_plan")

        if patient is None:

            raise ValueError(
                "Patient not available in execution context."
            )

        if therapy_plan is None:

            raise ValueError(
                "Therapy plan not available in execution context."
            )

        result = await self.mcp.save_therapy_plan(

            patient_id=patient["id"],

            patient_info=patient,

            therapy_plan=therapy_plan,

        )

        return {
            
            "saved_plan": result,

            "plan_id": result["plan_id"],

        }