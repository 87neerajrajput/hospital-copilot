import uuid

import streamlit as st

from langgraph.types import Command

from graph.workflow import build_graph

from utils.pdf_generator import generate_pdf

from tools.db_tools import initialize_database, search_patients, get_patient, get_patient_plans, get_therapy_plan

from assistants.therapist_chat import render_chat



# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Paravartan Healthcare Copilot",
    layout="wide"
)


# @st.cache_resource
# def initialize_app():
#     initialize_database()

# initialize_app()


st.title("🏥 Paravartan Healthcare Copilot")


# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "patient_name" not in st.session_state:
    st.session_state.patient_name = ""

if "age" not in st.session_state:
    st.session_state.age = 0

if "diagnosis" not in st.session_state:
    st.session_state.diagnosis = ""

if "primary_concerns" not in st.session_state:
    st.session_state.primary_concerns = ""

if "waiting_for_approval" not in st.session_state:
    st.session_state.waiting_for_approval = False

if "workflow_started" not in st.session_state:
    st.session_state.workflow_started = False

if "plan_generated" not in st.session_state:
    st.session_state.plan_generated = False

if "reports_generated" not in st.session_state:
    st.session_state.reports_generated = False

if "selected_patient_id" not in st.session_state:
    st.session_state.selected_patient_id = None

if "patient_search" not in st.session_state:
    st.session_state.patient_search = ""

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "patient_plans" not in st.session_state:
    st.session_state.patient_plans = []

if "selected_plan" not in st.session_state:
    st.session_state.selected_plan = None

if "selected_plan_label" not in st.session_state:
    st.session_state.selected_plan_label = None

if "loaded_patient" not in st.session_state:
    st.session_state.loaded_patient = None

if "search_message" not in st.session_state:
    st.session_state.search_message = None

if "screen_mode" not in st.session_state:
    st.session_state.screen_mode = "workspace"



def reset_application():
    # Remove all widget and application state
    st.session_state.clear()

    # Reinitialize only the values that must exist
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.screen_mode = "workspace"

    # st.session_state.thread_id = str(uuid.uuid4())

    # st.session_state.selected_patient_id = None
    # st.session_state.patient_name = ""
    # st.session_state.age = 0
    # st.session_state.diagnosis = ""
    # st.session_state.primary_concerns = ""

    # st.session_state.patient_search = ""
    # st.session_state.search_results = []
    # st.session_state.search_message = ""

    # st.session_state.patient_plans = []
    # st.session_state.selected_plan = None
    # st.session_state.selected_plan_label = None

    # st.session_state.workflow_started = False
    # st.session_state.waiting_for_approval = False
    # st.session_state.plan_generated = False
    # st.session_state.reports_generated = False

    # st.session_state.screen_mode = "workspace"

# ==========================================
# PATIENT MANAGEMENT
# ==========================================

st.sidebar.header("👤 Patient Management")

if st.sidebar.button(
    "🆕 New Patient Assessment",
    use_container_width=True
):
    reset_application()
    st.rerun()

search_text = st.sidebar.text_input(
    "Search Patient",
    key="patient_search"
)

if st.sidebar.button("🔍 Search"):

    st.session_state.search_results = (
        search_patients(search_text)
    )

    if st.session_state.search_results:

        st.session_state.search_message = (
            f"Found {len(st.session_state.search_results)} patient(s)."
        )

    else:

        st.session_state.search_message = (
            "No matching patient record found. "
            "Please create a new patient assessment."
        )


# Display message outside button block
if st.session_state.search_message:

    if st.session_state.search_results:

        st.sidebar.success(
            st.session_state.search_message
        )

    else:

        st.sidebar.info(
            st.session_state.search_message
        )


if st.session_state.search_results:

    st.sidebar.subheader("Results")
    patient_options = {

        f"{p['name']} "
        f"(ID: {p['id']})":

        p["id"]

        for p in st.session_state.search_results
    }

    selected_label = st.sidebar.selectbox(
        "Select Patient",
        options=list(patient_options.keys())
    )

if st.sidebar.button("📂 Load Patient"):

    patient_id = (
        patient_options[selected_label]
    )

    patient = get_patient(patient_id)

    st.session_state.selected_patient_id = (
        patient_id
    )

    st.session_state.patient_plans = (
        get_patient_plans(patient_id)
    )

    st.session_state.loaded_patient = patient

    # Clear previously viewed plan
    st.session_state.selected_plan = None
    st.session_state.selected_plan_label = None

    #clear the search message
    st.session_state.search_message = None

    st.session_state.patient_name = (
        patient["name"]
    )

    st.session_state.age = (
        patient["age"]
    )

    st.session_state.diagnosis = (
        patient["diagnosis"]
    )

    st.session_state.primary_concerns = (
        "\n".join(
            patient["concerns"]
        )
    )

    st.success(
        "Patient loaded successfully."
    )

    # Loading a patient should reset the UI to a clean workspace ready for a new session.
    st.session_state.screen_mode = "workspace"
    st.session_state.workflow_started = False

    # Hide any previously viewed history
    st.session_state.selected_plan = None

    st.rerun()

# ==========================================
# PATIENT HISTORY
# ==========================================

if st.session_state.selected_patient_id:

    st.sidebar.divider()

    st.sidebar.subheader(
        "📋 Previous Therapy Plans"
    )

    # Show Plans
    if st.session_state.patient_plans:
        plan_options = {

            f"Plan #{plan['id']} - "
            f"{plan['created_at'].strftime('%d-%b-%Y')}":

            plan["id"]

            for plan in st.session_state.patient_plans
        }

        selected_plan_label = (
            st.sidebar.selectbox(
                "Select Plan",
                options=list(plan_options.keys()),
                key="selected_plan_label"
            )
        )

        # Load Plan
        if st.sidebar.button("📖 View Plan"):

            plan_id = (
                plan_options[
                    selected_plan_label
                ]
            )

            # st.session_state.selected_plan = (
            #     get_therapy_plan(plan_id)
            # )

            plan = get_therapy_plan(plan_id)

            st.session_state.selected_plan = plan["therapy_plan"]

            patient = plan["patient_info"]

            st.session_state.patient_name = patient["name"]
            st.session_state.age = patient["age"]
            st.session_state.diagnosis = patient["diagnosis"]
            st.session_state.primary_concerns = "\n".join(
                patient["concerns"]
            )

            # Switch to history mode
            st.session_state.screen_mode = "history"

            # Leave the current workspace
            st.session_state.workflow_started = False
            st.session_state.waiting_for_approval = False
            st.session_state.reports_generated = False

            # Leave history mode
            #st.session_state.plan_generated = False
            
            # Clear current workspace
            # st.session_state.therapy_plan = None
            # st.session_state.qa_result = None
            # st.session_state.clinical_report = None
            # st.session_state.parent_report = None

            st.rerun()
    else:

        st.sidebar.info(
            "No previous therapy plans found."
        )


# ==========================================
# GRAPH
# ==========================================

@st.cache_resource
def get_graph():
    return build_graph()

graph = get_graph()


# ==========================================
# CONFIG
# ==========================================

config = {
    "configurable": {
        "thread_id": st.session_state.thread_id
    }
}

# Safety Restore accidentally wiped the loaded patient.
if st.session_state.loaded_patient:

    patient = st.session_state.loaded_patient

    if not st.session_state.patient_name:

        st.session_state.patient_name = patient["name"]

    if st.session_state.age == 0:

        st.session_state.age = patient["age"]

    if not st.session_state.diagnosis:

        st.session_state.diagnosis = patient["diagnosis"]

    if not st.session_state.primary_concerns:

        st.session_state.primary_concerns = (
            "\n".join(patient["concerns"])
        )



left_col, right_col = st.columns(
    [3, 1],
    gap="small"
)

with left_col:

    # ==========================================
    # PATIENT INTAKE
    # ==========================================

    st.header("👤 Patient Intake")

    patient_name = st.text_input(
        "Patient Name",
        key="patient_name"
    )

    age = st.number_input(
        "Age",
        min_value=0,
        max_value=18,
        key="age"
    )

    diagnosis = st.text_input(
        "Diagnosis",
        key="diagnosis"
    )

    concerns = st.text_area(
        "Primary Concerns",
        key="primary_concerns"
    )


    # ==========================================
    # DISPLAY PREVIOUS THERAPY PLAN
    # ==========================================

    if (st.session_state.screen_mode == "history" and 
        st.session_state.selected_plan):

        previous_plan = (
            st.session_state.selected_plan
        )

        st.header(
            "📋 Previous Therapy Plan"
        )

        # ======================================
        # THERAPY GOALS
        # ======================================

        st.subheader(
            "🎯 Therapy Goals"
        )

        for goal in previous_plan[
            "therapy_goals"
        ]:

            st.write(
                f"• {goal}"
            )

        # ======================================
        # WEEKLY THERAPY SCHEDULE
        # ======================================

        st.subheader(
            "📅 Weekly Therapy Schedule"
        )

        with st.expander(
            "View Weekly Therapy Schedule"
        ):

            for week in previous_plan[
                "weekly_schedule"
            ]:

                st.markdown(
                    f"### {week['week']}"
                )

                st.write(
                    f"**Focus Area:** "
                    f"{week['focus_area']}"
                )

                st.write(
                    "**Activities:**"
                )

                for activity in week[
                    "activities"
                ]:

                    st.write(
                        f"• {activity}"
                    )

                st.write(
                    f"**Expected Outcome:** "
                    f"{week['expected_outcome']}"
                )

                st.divider()

        # ======================================
        # HOME PROGRAM
        # ======================================

        st.subheader(
            "🏠 Home Program Suggestion"
        )

        with st.expander(
            "View Home Program Activities"
        ):

            for activity in previous_plan[
                "home_program"
            ]:

                st.markdown(
                    f"### {activity['activity_name']}"
                )

                st.write(
                    f"**Instructions:** "
                    f"{activity['instructions']}"
                )

                st.write(
                    f"**Frequency:** "
                    f"{activity['recommended_frequency']}"
                )

                st.divider()


    # ==========================================
    # GENERATE PLAN
    # ==========================================

    if st.button("🚀 Generate Therapy Plan"):

        # ----------------------------------
        # Hide previous history
        # ----------------------------------

        st.session_state.selected_plan = None

        st.session_state.plan_generated = False

        st.session_state.reports_generated = False

        st.session_state.screen_mode = "workspace"
        st.session_state.workflow_started = True

        with st.spinner(
            "Processing patient information, retrieving clinical knowledge, and generating therapy plan..."
        ):

            initial_state = {

                "user_query": f"""
                Patient Name: {patient_name}
                Age: {age}
                Diagnosis: {diagnosis}
                Concerns: {concerns}
                """,

                "patient_info": None,
                "patient_id": st.session_state.selected_patient_id,

                "retrieved_docs": None,

                "therapy_plan": None,
                "plan_id": None,

                "qa_result": None,

                "approval_status": None,

                "clinical_report": None,
                "parent_report": None,

                "clinical_report_id": None,
                "parent_report_id": None,

                "next_agent": ""
            }

            result = graph.invoke(
                initial_state,
                config=config
            )

            st.session_state.plan_generated = True

            # Select Plan Dropdown updates automatically without needing to reload the patient.
            if st.session_state.selected_patient_id:

                st.session_state.patient_plans = (
                    get_patient_plans(
                        st.session_state.selected_patient_id
                    )
                )


            if (st.session_state.screen_mode == "workspace"
                and st.session_state.plan_generated):

                st.success("✅ Therapy plan generated successfully.")

            
            # st.write("RESULT")
            # st.write(result)
            
            # Check interrupt
            graph_state = graph.get_state(config)
            # st.write("STATE")
            # st.write(graph_state)

            if graph_state.next:
                st.session_state.waiting_for_approval = True

            st.rerun()


    # ==========================================
    # DISPLAY STATE
    # ==========================================

    if (
        st.session_state.workflow_started
        and st.session_state.screen_mode == "workspace"
    ):

        graph_state = graph.get_state(config)

        #st.write(graph_state)

        state = graph_state.values

        if state:

            # ==================================
            # THERAPY PLAN
            # ==================================

            therapy_plan = state.get("therapy_plan")

            if therapy_plan:

                st.divider()

                st.header("📋 Therapy Plan")

                # ------------------------------
                # Goals
                # ------------------------------

                st.subheader("🎯 Therapy Goals")

                for goal in therapy_plan["therapy_goals"]:

                    st.write(f"• {goal}")

                # ------------------------------
                # Weekly Schedule
                # ------------------------------

                st.subheader("📅 Weekly Therapy Schedule")

                with st.expander(
                    "View Full 4-Week Therapy Plan",
                    expanded=False
                ):

                    for week_plan in therapy_plan["weekly_schedule"]:

                        st.markdown(
                            f"### 🗓️ {week_plan['week']}"
                        )

                        st.markdown(
                            f"**🎯 Focus Area:** "
                            f"{week_plan['focus_area']}"
                        )

                        st.markdown("**🛠️ Activities:**")

                        for activity in week_plan["activities"]:
                            st.markdown(f"- {activity}")

                        st.info(
                            f"Expected Outcome: "
                            f"{week_plan['expected_outcome']}"
                        )

                        st.divider()

                # ------------------------------
                # Home Program
                # ------------------------------

                st.subheader("🏠 Home Program Suggestion")

                with st.expander(
                    "View Home Program Activities",
                    expanded=False
                ):

                    for idx, activity in enumerate(
                        therapy_plan["home_program"],
                        start=1
                    ):

                        st.markdown(
                            f"### 🧩 Activity {idx}: {activity['activity_name']}"
                        )

                        col1, col2 = st.columns([3, 1])

                        with col1:
                            st.markdown("**📝 Instructions**")
                            st.write(activity["instructions"])

                        with col2:
                            st.markdown("**📅 Recommended Frequency**")
                            st.success(
                                activity["recommended_frequency"]
                            )

                        st.divider()

            # ==================================
            # QA REVIEW
            # ==================================

            qa = state.get("qa_result")

            if (st.session_state.screen_mode == "workspace" and qa):

                st.divider()

                st.header("🩺 Clinical Quality Review")

                if qa["status"] == "PASS":

                    st.success("PASS")

                else:

                    st.error("FAIL")

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Concern Coverage",
                        str(
                            qa["concern_coverage"]
                        )
                    )

                with col2:

                    st.metric(
                        "Knowledge Base Alignment",
                        str(
                            qa["knowledge_alignment"]
                        )
                    )

                with col3:

                    st.metric(
                        "Completeness",
                        str(
                            qa["completeness"]
                        )
                    )

                st.subheader("🚨 Issues")

                if qa["issues"]:

                    for issue in qa["issues"]:

                        st.write(f"• {issue}")

                else:

                    st.write("No issues found.")

                st.subheader("📝 Recommendations")

                if qa["suggestions"]:

                    for suggestion in qa["suggestions"]:

                        st.write(f"• {suggestion}")

                else:

                    st.write("No suggestions.")

            # ==================================
            # HUMAN REVIEW
            # ==================================

            if (
                st.session_state.screen_mode == "workspace"
                and st.session_state.waiting_for_approval
            ):

                st.divider()

                st.header("👨‍⚕️ Clinical Approval")

                st.info(
                    "Please review the therapy plan and clinical review findings "
                    "before approving the treatment plan."
                )

                col1, col2 = st.columns(2)

                # ------------------------------
                # APPROVE
                # ------------------------------

                with col1:

                    if st.button("✅ Approve Plan", use_container_width=True):
                        with st.spinner("Preparing clinical and parent reports..."):

                            graph.invoke(
                                Command(
                                    resume="approved"
                                ),
                                config=config
                            )

                            st.session_state.waiting_for_approval = False
                            
                            st.session_state.reports_generated = True
                            
                            if st.session_state.get("reports_generated", False):
                                st.success(
                                    "✅ Clinical and parent reports generated successfully."
                                )
                            
                            st.rerun()

                # ------------------------------
                # REJECT
                # ------------------------------

                with col2:

                    if st.button(
                        "❌ Reject Plan",
                        use_container_width=True
                    ):

                        graph.invoke(
                            Command(
                                resume="rejected"
                            ),
                            config=config
                        )

                        st.session_state.waiting_for_approval = False

                        st.rerun()

            # ==================================
            # APPROVAL STATUS
            # ==================================

            approval_status = state.get(
                "approval_status"
            )

            if approval_status == "approved":

                st.success(
                    "Therapy Plan Approved"
                )

            elif approval_status == "rejected":

                st.error(
                    "Therapy Plan Rejected"
                )

            # ==================================
            # REPORTS
            # ==================================

            clinical_report = state.get(
                "clinical_report"
            )

            parent_report = state.get(
                "parent_report"
            )

            if clinical_report:

                st.divider()

                st.header(
                    "Clinical Report"
                )

                #st.markdown(clinical_report)
                with st.expander(
                    "View Clinical Report",
                    expanded=True
                ):
                    st.markdown(clinical_report)

            if parent_report:

                st.header(
                    "Parent Report"
                )

                #st.markdown(parent_report)

                with st.expander(
                    "View Parent Report",
                    expanded=True
                ):
                    st.markdown(parent_report)


            if clinical_report and parent_report:
                clinical_pdf = generate_pdf(
                    "Clinical Report",
                    clinical_report
                )

                parent_pdf = generate_pdf(
                    "Parent Report",
                    parent_report
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.download_button(
                        label="🏠 Download Parent Report PDF",
                        data=parent_pdf,
                        file_name="Parent_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                with col2:
                    st.download_button(
                        label="📋 Download Clinical Report PDF",
                        data=clinical_pdf,
                        file_name="Clinical_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                # ==========================================
                # CLEAR ALL STATES
                # ==========================================
                with col3:
                    if st.button("🆕 Start New Patient", use_container_width=True):
                        reset_application()
                        # st.session_state.clear()
                        # st.session_state.plan_generated = False
                        # st.session_state.reports_generated = False
                        # st.session_state.thread_id = str(uuid.uuid4())
                        st.rerun()


# ==================================
# Chat UI
# ==================================
with right_col:

    render_chat()
