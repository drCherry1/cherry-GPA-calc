
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

st.markdown(
    """
    <style>

    .block-container {
        max-width: 900px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    .summary-box {
        border: 1px solid #dadce0;
        border-radius: 12px;
        padding: 25px 20px;
        margin-bottom: 30px;
        background-color: white;
    }

    .summary-label {
        font-size: 14px;
        color: #5f6368;
        margin-bottom: 5px;
    }

    .summary-gpa {
        font-size: 38px;
        font-weight: 500;
        color: #202124;
        line-height: 1.2;
    }

    .summary-value {
        font-size: 24px;
        font-weight: 500;
        color: #202124;
        line-height: 1.5;
    }

    .course-header {
        font-size: 14px;
        font-weight: 500;
        color: #5f6368;
        margin-bottom: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


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
# GPA SCALE
# =========================================================
# A is the HIGHEST grade.
# There is NO A+.

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


# =========================================================
# ADD COURSE
# =========================================================

def add_course():

    st.session_state.courses.append(
        {
            "name": "",
            "grade": "A",
            "credits": 3.0
        }
    )


# =========================================================
# DELETE COURSE
# =========================================================

def delete_course(index):

    if len(st.session_state.courses) > 1:

        st.session_state.courses.pop(index)

    else:

        st.session_state.courses[0] = {
            "name": "",
            "grade": "A",
            "credits": 3.0
        }


# =========================================================
# RESET
# =========================================================

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

    points = grade_points[grade]

    total_credits += credits

    total_points += points * credits


if total_credits > 0:

    cumulative_gpa = (
        total_points / total_credits
    )

else:

    cumulative_gpa = 0.0


# =========================================================
# TITLE
# =========================================================

st.title("GPA Calculator")

st.write(
    "Enter your courses, grades, and credits to calculate "
    "your cumulative GPA."
)


# =========================================================
# SUMMARY
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

header1, header2, header3, header4 = st.columns(
    [5, 2, 2, 0.7]
)


with header1:

    st.markdown(
        '<div class="course-header">Course Name</div>',
        unsafe_allow_html=True
    )


with header2:

    st.markdown(
        '<div class="course-header">Grade</div>',
        unsafe_allow_html=True
    )


with header3:

    st.markdown(
        '<div class="course-header">Credits</div>',
        unsafe_allow_html=True
    )


with header4:

    st.markdown(
        '<div class="course-header"></div>',
        unsafe_allow_html=True
    )


# =========================================================
# COURSE ROWS
# =========================================================

for i, course in enumerate(
    st.session_state.courses
):

    col1, col2, col3, col4 = st.columns(
        [5, 2, 2, 0.7]
    )


    # -----------------------------------------------------
    # COURSE NAME
    # -----------------------------------------------------

    with col1:

        course["name"] = st.text_input(
            "Course",
            value=course["name"],
            key=f"course_name_{i}",
            label_visibility="collapsed",
            placeholder="Course name"
        )


    # -----------------------------------------------------
    # GRADE
    # -----------------------------------------------------

    with col2:

        grade_options = list(
            grade_points.keys()
        )

        course["grade"] = st.selectbox(
            "Grade",
            grade_options,
            index=grade_options.index(
                course["grade"]
            ),
            key=f"course_grade_{i}",
            label_visibility="collapsed"
        )


    # -----------------------------------------------------
    # CREDITS
    # -----------------------------------------------------

    with col3:

        course["credits"] = st.number_input(
            "Credits",
            min_value=0.0,
            max_value=100.0,
            value=float(course["credits"]),
            step=0.5,
            key=f"course_credits_{i}",
            label_visibility="collapsed"
        )


    # -----------------------------------------------------
    # DELETE
    # -----------------------------------------------------

    with col4:

        st.button(
            "×",
            key=f"delete_course_{i}",
            on_click=delete_course,
            args=(i,),
            use_container_width=True
        )


# =========================================================
# BUTTONS
# =========================================================

st.markdown("")


col1, col2 = st.columns(2)


with col1:

    st.button(
        "＋ Add course",
        on_click=add_course,
        use_container_width=True
    )


with col2:

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

