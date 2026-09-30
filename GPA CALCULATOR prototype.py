
import streamlit as st

# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="GPA Calculator",
    page_icon="🎓",
    layout="centered"
)


# ==========================================
# SESSION STATE
# ==========================================

if "subjects" not in st.session_state:
    st.session_state.subjects = [
        {
            "name": "Subject 1",
            "mark": 0.0
        }
    ]


if "remove_message" not in st.session_state:
    st.session_state.remove_message = ""


# ==========================================
# GPA SYSTEM
# ==========================================

def get_gpa(mark):

    if mark >= 90:
        return 4.00

    elif mark >= 80:
        return 4.00

    elif mark >= 70:
        return 3.00

    elif mark >= 60:
        return 2.00

    elif mark >= 50:
        return 1.00

    else:
        return 0.00


# ==========================================
# ADD SUBJECT
# ==========================================

def add_subject():

    number = len(st.session_state.subjects) + 1

    st.session_state.subjects.append(
        {
            "name": f"Subject {number}",
            "mark": 0.0
        }
    )


# ==========================================
# REMOVE SUBJECT
# ==========================================

def remove_subject():

    if len(st.session_state.subjects) > 1:

        st.session_state.subjects.pop()

        st.session_state.remove_message = ""

    else:

        st.session_state.remove_message = (
            "You must have at least 1 subject."
        )


# ==========================================
# TITLE
# ==========================================

st.title("🎓 GPA 4.0 Calculator")

st.write(
    "Add your subjects, rename them, enter your marks, "
    "and calculate your GPA."
)


# ==========================================
# SUBJECT CONTROLS
# ==========================================

st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])


with col1:

    st.button(
        "➖",
        on_click=remove_subject,
        use_container_width=True
    )


with col2:

    st.markdown(
        f"""
        <h3 style="text-align: center;">
            {len(st.session_state.subjects)} Subjects
        </h3>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.button(
        "➕",
        on_click=add_subject,
        use_container_width=True
    )


# ==========================================
# REMOVE WARNING
# ==========================================

if st.session_state.remove_message:

    st.warning(
        st.session_state.remove_message
    )


# ==========================================
# SUBJECTS
# ==========================================

st.markdown("---")

total_gpa = 0.0


for i, subject in enumerate(
    st.session_state.subjects
):

    st.subheader(
        f"📚 Subject {i + 1}"
    )


    # --------------------------------------
    # SUBJECT NAME
    # --------------------------------------

    subject["name"] = st.text_input(
        "Subject Name",
        value=subject["name"],
        key=f"subject_name_{i}",
        placeholder="Enter subject name"
    )


    # --------------------------------------
    # MARK
    # --------------------------------------

    subject["mark"] = st.number_input(
        "Mark (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(subject["mark"]),
        step=0.1,
        key=f"subject_mark_{i}"
    )


    # --------------------------------------
    # INDIVIDUAL GPA
    # --------------------------------------

    individual_gpa = get_gpa(
        subject["mark"]
    )


    st.write(
        f"📊 **{subject['name']} GPA:** "
        f"{individual_gpa:.2f}"
    )


    total_gpa += individual_gpa


    st.markdown("---")


# ==========================================
# OVERALL GPA
# ==========================================

number_of_subjects = len(
    st.session_state.subjects
)


overall_gpa = (
    total_gpa / number_of_subjects
)


# ==========================================
# FINAL GPA
# ==========================================

st.header("🏆 Overall GPA")


st.metric(
    "GPA",
    f"{overall_gpa:.2f} / 4.00"
)


# ==========================================
# GPA MESSAGE
# ==========================================

if overall_gpa >= 3.50:

    st.success(
        "🌟 Excellent GPA! Keep up the great work!"
    )

elif overall_gpa >= 3.00:

    st.success(
        "👏 Great job! You are doing really well!"
    )

elif overall_gpa >= 2.00:

    st.info(
        "👍 Good effort! Keep working to improve!"
    )

elif overall_gpa >= 1.00:

    st.warning(
        "💪 Keep studying and you can raise your GPA!"
    )

else:

    st.error(
        "📚 Keep practicing and don't give up!"
    )

