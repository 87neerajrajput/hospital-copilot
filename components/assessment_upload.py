import streamlit as st


def render_assessment_upload():

    st.subheader("📎 Assessment Report")

    uploaded_file = st.file_uploader(
        "Upload Assessment PDF",
        type=["pdf"],
        key=f"assessment_pdf_{st.session_state.assessment_uploader_key}",
    )

    # ------------------------------------------
    # Synchronize session state with uploader
    # ------------------------------------------

    st.session_state.assessment_pdf = uploaded_file

    # ------------------------------------------
    # Nothing uploaded
    # ------------------------------------------

    if uploaded_file is None:
        return

    # ------------------------------------------
    # Show uploaded filename
    # ------------------------------------------

    st.success(f"Uploaded: {uploaded_file.name}")

    # ------------------------------------------
    # Optional Remove Button
    # ------------------------------------------

    if st.button(
        "❌ Remove Assessment",
        type="secondary",
        use_container_width=True,
    ):

        st.session_state.assessment_pdf = None

        #st.session_state.assessment_applied = False

        st.session_state.pending_autofill = False

        st.session_state.assessment_uploader_key += 1

        st.session_state.assessment_summary = None

        st.session_state.assessment_text = None

        st.session_state.pending_assessment_summary = None

        st.rerun()



