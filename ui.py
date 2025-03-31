import streamlit as st
import json

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.form_data = {}

# Custom CSS for minimal UI
st.markdown("""
    <style>
        /* Minimal styling */
        .stApp {
            padding: 1rem 2rem 4rem;
        }
        .stProgress > div > div > div > div {
            background-color: #FF4B4B;
            height: 3px;
        }
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Arrow buttons styling */
        .arrow-btn {
            background: none !important;
            border: none !important;
            box-shadow: none !important;
            font-size: 24px !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        .arrow-btn:hover {
            color: #FF4B4B !important;
        }
    </style>
""", unsafe_allow_html=True)

def validate_json(uploaded_file):
    try:
        data = json.load(uploaded_file)
        if not isinstance(data, (dict, list)):
            return False, "JSON must be an object or array."
        return True, "JSON is valid!"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}"
    except Exception as e:
        return False, f"Error reading JSON: {str(e)}"

def next_step():
    st.session_state.step += 1
    st.rerun()


def prev_step():
    st.session_state.step -= 1
    st.rerun()


# Progress indicator: show 0% at step 1 and 100% at step 6
progress_value = (st.session_state.step - 1) / 5
st.progress(progress_value)
st.caption(f"Step {st.session_state.step} of 6")

# Form content
with st.container():
    if st.session_state.step == 1:
        st.subheader("School name")
        school_name = st.text_input(
            "Type your school name and press Enter",
            key="school_input",
            label_visibility="collapsed",
            on_change=lambda: next_step() if st.session_state.get("school_input", "").strip() != "" else None
        )
        st.session_state.form_data['school_name'] = school_name

    elif st.session_state.step == 2:
        st.subheader("Periods per day")
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            periods = st.number_input(
                "Enter number of periods",
                min_value=1,
                max_value=20,
                value=6,
                key="periods_input",
                label_visibility="collapsed"
            )
            st.session_state.form_data['periods_per_day'] = periods
        
        # Navigation arrows
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.button("←", on_click=prev_step, key="prev2", help="Go back", use_container_width=True)
        with col3:
            st.button("→", on_click=next_step, key="next2", help="Continue", use_container_width=True)

    elif st.session_state.step == 3:
        st.subheader("Days per week")
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            days = st.number_input(
                "Enter number of days",
                min_value=1,
                max_value=7,
                value=5,
                key="days_input",
                label_visibility="collapsed"
            )
            st.session_state.form_data['days_per_week'] = days
        
        # Navigation arrows
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.button("←", on_click=prev_step, key="prev3", help="Go back", use_container_width=True)
        with col3:
            st.button("→", on_click=next_step, key="next3", help="Continue", use_container_width=True)

    elif st.session_state.step == 4:
        st.subheader("Upload JSON")
        uploaded_file = st.file_uploader(
            "Drag & drop or click to browse",
            type="json",
            key="json_upload",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            valid, message = validate_json(uploaded_file)
            if valid:
                st.success(message)
                uploaded_file.seek(0)  # reset file pointer before reading again
                st.session_state.form_data['json_data'] = json.load(uploaded_file)
                # Auto-advance after successful upload
                st.rerun()
            else:
                st.error(message)
        
        # Navigation arrows
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.button("←", on_click=prev_step, key="prev4", help="Go back", use_container_width=True)
        with col3:
            if uploaded_file is not None and valid:
                st.button("→", on_click=next_step, key="next4", help="Continue", use_container_width=True)

    elif st.session_state.step == 5:
        st.subheader("Review your information")
        
        # Display form data in a clean format
        st.write(f"**School Name:** {st.session_state.form_data.get('school_name', '')}")
        st.write(f"**Periods per Day:** {st.session_state.form_data.get('periods_per_day', '')}")
        st.write(f"**Days per Week:** {st.session_state.form_data.get('days_per_week', '')}")
        
        if 'json_data' in st.session_state.form_data:
            with st.expander("View JSON Data"):
                st.json(st.session_state.form_data['json_data'])
        
        # Navigation and submit
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.button("←", on_click=prev_step, key="prev5", help="Go back", use_container_width=True)
        with col3:
            st.button("Submit", on_click=next_step, type="primary", key="submit5", use_container_width=True)

    elif st.session_state.step == 6:
        st.success("✅ Submission complete!")
        st.write(f"**School:** {st.session_state.form_data.get('school_name', '')}")
        st.write(f"**Schedule:** {st.session_state.form_data.get('periods_per_day', '')} periods/day, {st.session_state.form_data.get('days_per_week', '')} days/week")
        
        if 'json_data' in st.session_state.form_data:
            with st.expander("View Uploaded JSON"):
                st.json(st.session_state.form_data['json_data'])
