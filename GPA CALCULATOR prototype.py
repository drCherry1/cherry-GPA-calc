import streamlit as st

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="GPA Calculator",
    page_icon="🎓",
    layout="centered"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.block-container {
    max-width: 900px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

.summary-box {
    border: 1px solid #dadce0;
    border-radius: 12px;
    padding: 24px;
    margin: 25px 0 30px 0;
}

.summary-label {
    font-size: 14px;
    color: #5f6368;
    margin-bottom: 5px;
}

.summary-gpa {
    font-size: 40px;
    font-weight: 500;
    color: #202124;
}

.summary-value {
    font-size: 24px;
    font-weight: 500;
    color: #202124;
}

.course-header {
    font-size: 14px;
    font-weight: 500;
    color: #5f6368;
    margin-bottom: 5px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# GPA SCALE
# =========================================================

grade_points = {
    "A": 4.00,
    "A-": 3.70,
    "B+": 3.30,
    "B": 3.00,
    "B-": 2.70,
    "C+": 2.30,
    "C": 2.00,
    "C-": 1.70,
    "D+": 1.30,
    "D": 1.00,
    "D-": 0.70,
    "F": 0.00
}

grade_options = list(grade_points.keys())


# =========================================================
# SESSION STATE
# =========================================================

if "courses" not in st.session_state:
    st.session_state.courses = [
        {
            "name": "",
            "grade": "A",
            "credits": 3.0
        }
    ]


# =========================================================
# FUNCTIONS
# =========================================================

def add_course():
    st.session_state.courses.append({
        "name": "",
        "grade": "A",
        "credits": 3.0
    })


def delete_course(index):

    # Keep at least one course
    if len(st.session_state.courses) > 1:
        st.session_state.courses.pop(index)

    else:
        st.session_state.courses[0] = {
            "name": "",
            "grade": "A",
            "credits": 3.0
        }


def reset_courses():
    st.session_state.courses = [
        {
            "name": "",
            "grade": "A",
            "credits": 3.0
        }
    ]


# =========================================================
# CALCULATE GPA
# =========================================================

total_credits = 0.0
total_points = 0.0

for course in st.session_state.courses:

    credits = course["credits"]
    grade = course["grade"]

    total_credits += credits
    total_points += grade_points[grade] * credits


if total_credits > 0:
    cumulative_gpa = total_points / total_credits
else:
    cumulative_gpa = 0.0


# =========================================================
# TITLE
# =========================================================

st.title("GPA Calculator")

st.write(
    "Enter your courses, grades, and credits to calculate your cumulative GPA."
)


# =========================================================
# SUMMARY BOX
# =========================================================

st.markdown(
    f"""
    <div class="summary-box">

        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            text-align: left;
        ">

            <div style="flex: 1;">
                <div class="summary-label">
                    Cumulative GPA
                </div>

                <div class="summary-gpa">
                    {cumulative_gpa:.2f}
                </div>
            </div>

            <div style="flex: 1;">
                <div class="summary-label">
                    Total Credits
                </div>

                <div class="summary-value">
                    {total_credits:.1f}
                </div>
            </div>

            <div style="flex: 1;">
                <div class="summary-label">
                    Total Points
                </div>

                <div class="summary-value">
                    {total_points:.1f}
                </div>
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# COURSE HEADERS
# =========================================================

h1, h2, h3, h4 = st.columns([5, 2, 2, 0.7])

with h1:
    st.markdown(
        '<div class="course-header">Course Name</div>',
        unsafe_allow_html=True
    )

with h2:
    st.markdown(
        '<div class="course-header">Grade</div>',
        unsafe_allow_html=True
    )

with h3:
    st.markdown(
        '<div class="course-header">Credits</div>',
        unsafe_allow_html=True
    )


# =========================================================
# COURSE ROWS
# =========================================================

for i, course in enumerate(st.session_state.courses):

    col1, col2, col3, col4 = st.columns([5, 2, 2, 0.7])

    # Course name
    with col1:

        course["name"] = st.text_input(
            "Course Name",
            value=course["name"],
            key=f"name_{i}",
            placeholder="Course name",
            label_visibility="collapsed"
        )

    # Grade
    with col2:

        course["grade"] = st.selectbox(
            "Grade",
            grade_options,
            index=grade_options.index(course["grade"]),
            key=f"grade_{i}",
            label_visibility="collapsed"
        )

    # Credits
    with col3:

        course["credits"] = st.number_input(
            "Credits",
            min_value=0.0,
            max_value=100.0,
            value=float(course["credits"]),
            step=0.5,
            key=f"credits_{i}",
            label_visibility="collapsed"
        )

    # Delete
    with col4:

        st.button(
            "×",
            key=f"delete_{i}",
            on_click=delete_course,
            args=(i,),
            use_container_width=True
        )


# =========================================================
# BUTTONS
# =========================================================

st.write("")

button1, button2 = st.columns(2)

with button1:

    st.button(
        "＋ Add course",
        on_click=add_course,
        use_container_width=True
    )

with button2:

    st.button(
        "Reset",
        on_click=reset_courses,
        use_container_width=True
    )


# =========================================================
# GPA SCALE
# =========================================================

st.markdown("---")

with st.expander("View GPA scale"):

    st.write("A = 4.00")
    st.write("A− = 3.70")
    st.write("B+ = 3.30")
    st.write("B = 3.00")
    st.write("B− = 2.70")
    st.write("C+ = 2.30")
    st.write("C = 2.00")
    st.write("C− = 1.70")
    st.write("D+ = 1.30")
    st.write("D = 1.00")
    st.write("D− = 0.70")
    st.write("F = 0.00")
