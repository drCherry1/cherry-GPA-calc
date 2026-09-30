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
# MINIMAL ANIMATED BACKGROUND
# =========================================================

st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"] {
    background: #f7f7f7;
}

/* Moving background lines */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;

    background-image:
        linear-gradient(
            115deg,
            transparent 48%,
            rgba(0, 0, 0, 0.035) 49%,
            rgba(0, 0, 0, 0.035) 50%,
            transparent 51%
        ),
        linear-gradient(
            25deg,
            transparent 48%,
            rgba(0, 0, 0, 0.025) 49%,
            rgba(0, 0, 0, 0.025) 50%,
            transparent 51%
        );

    background-size: 180px 180px;
    animation: moveLines 25s linear infinite;

    pointer-events: none;
    z-index: 0;
}

/* Keep the app above the background */
[data-testid="stAppViewContainer"] > .main {
    position: relative;
    z-index: 1;
}

@keyframes moveLines {

    0% {
        transform: translate(0, 0);
    }

    50% {
        transform: translate(90px, 60px);
    }

    100% {
        transform: translate(180px, 120px);
    }
}

/* Make the main content slightly cleaner */
.block-container {
    max-width: 900px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

/* Summary metrics */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 12px;
    padding: 15px;
    backdrop-filter: blur(8px);
}

/* Course inputs */
[data-testid="stTextInput"],
[data-testid="stSelectbox"],
[data-testid="stNumberInput"] {
    background: rgba(255, 255, 255, 0.8);
    border-radius: 8px;
}

/* Buttons */
.stButton > button {
    border-radius: 8px;
}

/* Keep sidebar from affecting background */
section[data-testid="stSidebar"] {
    background: #f7f7f7;
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

    grade = course["grade"]
    credits = course["credits"]

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
# SUMMARY
# =========================================================

st.subheader("Summary")

summary1, summary2, summary3 = st.columns(3)

with summary1:
    st.caption("Cumulative GPA")
    st.metric(
        label="",
        value=f"{cumulative_gpa:.2f}"
    )

with summary2:
    st.caption("Total Credits")
    st.metric(
        label="",
        value=f"{total_credits:.1f}"
    )

with summary3:
    st.caption("Total Points")
    st.metric(
        label="",
        value=f"{total_points:.1f}"
    )


# =========================================================
# COURSES
# =========================================================

st.subheader("Courses")

header1, header2, header3, header4 = st.columns(
    [5, 2, 2, 0.7]
)

with header1:
    st.caption("Course Name")

with header2:
    st.caption("Grade")

with header3:
    st.caption("Credits")


# =========================================================
# COURSE ROWS
# =========================================================

for i, course in enumerate(st.session_state.courses):

    col1, col2, col3, col4 = st.columns(
        [5, 2, 2, 0.7]
    )

    with col1:

        course["name"] = st.text_input(
            "Course Name",
            value=course["name"],
            key=f"name_{i}",
            placeholder="Course name",
            label_visibility="collapsed"
        )

    with col2:

        course["grade"] = st.selectbox(
            "Grade",
            grade_options,
            index=grade_options.index(course["grade"]),
            key=f"grade_{i}",
            label_visibility="collapsed"
        )

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

st.divider()

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
