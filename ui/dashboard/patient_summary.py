import streamlit as st


class PatientSummary:

    @staticmethod
    def render(patient):

        with st.container():

            st.subheader("👤 Patient Summary")

            if patient is None:

                st.info(
                    "No patient selected."
                )

                return

            # --------------------------------------------------
            # Patient Data
            # --------------------------------------------------

            name = patient.get("name", "-")
            age = patient.get("age", "-")
            diagnosis = patient.get("diagnosis", "-")
            gender = patient.get("gender")

            therapist = patient.get("therapist")
            last_visit = patient.get("last_visit")
            next_visit = patient.get("next_visit")
            active_plan = patient.get("active_plan")
            sessions = patient.get("sessions")

            status = patient.get(
                "status",
                "🟢 Active",
            )

            # --------------------------------------------------
            # Header
            # --------------------------------------------------

            st.markdown(
                f"### {name}"
            )

            subtitle = []

            if diagnosis:
                subtitle.append(diagnosis)

            if age:
                subtitle.append(f"{age} Years")

            if status:
                subtitle.append(status)

            st.caption(
                " • ".join(subtitle)
            )

            # --------------------------------------------------
            # Metrics
            # --------------------------------------------------

            metrics = [

                ("Age", f"{age} Years"),

                ("Diagnosis", diagnosis),

                ("Status", status),

            ]

            if sessions:

                metrics.append(

                    ("Sessions", str(sessions))

                )

            metrics_container, _ = st.columns([3, 2])

            # with metrics_container:

            #     cols = st.columns(len(metrics))

            #     for col, (label, value) in zip(cols, metrics):

            #         with col:

            #             st.metric(
            #                 label=label,
            #                 value=value,
            #             )

            # st.divider()

            st.markdown("#### 🎯 Primary Concerns")

            concerns = patient.get("concerns", [])

            if concerns:

                for concern in concerns:

                    st.markdown(
                        f"- {concern}"
                    )

            else:

                st.caption(
                    "No concerns recorded."
                )

            #st.divider()

            # --------------------------------------------------
            # Additional Information
            # --------------------------------------------------

            info = []

            if gender:
                info.append(("Gender", gender))

            if therapist:
                info.append(("Therapist", therapist))

            if last_visit:
                info.append(("Last Visit", last_visit))

            if next_visit:
                info.append(("Next Visit", next_visit))

            if active_plan:
                info.append(("Active Plan", active_plan))

            if info:

                left, right = st.columns(2)

                midpoint = (len(info) + 1) // 2

                left_items = info[:midpoint]
                right_items = info[midpoint:]

                with left:

                    for label, value in left_items:

                        st.markdown(
                            f"**{label}**"
                        )

                        st.write(value)

                with right:

                    for label, value in right_items:

                        st.markdown(
                            f"**{label}**"
                        )

                        st.write(value)