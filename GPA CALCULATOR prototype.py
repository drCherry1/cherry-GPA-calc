
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
# DARK GREY ANIMATED BACKGROUND
# =========================================================

st.markdown("""
<style>
.stApp {
    background-color: #202124;
    background-image:
        linear-gradient(120deg, transparent 49.5%,
        rgba(255,255,255,0.08) 50%, transparent 50.5%),
        linear-gradient(30deg, transparent 49.5%,
        rgba(255,255,255,0.045) 50%, transparent 50.5%);
    background-size: 220px 220px;
    animation: backgroundMove 30s linear infinite;
}

@keyframes backgroundMove {
    0% {
        background-position: 0px 0px, 0px 0px;
    }
    50% {
        background-position: 110px 70px, -70px 100px;
    }
    100% {
        background-position: 220px 140px, -140px 200px;
    }
}

.block-container {
    max-width: 900px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4, h5, h6, p, label {
    color: #f1f3f4 !important;
}

[data-testid="stMetric"] {
    background: rgba(32,33,36,0.92);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 18px 12px;
    text-align: center;
}

[data-testid="stMetricLabel"] {
    width: 100%;
    justify-content: center;
    text-align: center;
    color: #9aa0a6 !important;
}

[data-testid="stMetricValue"] {
    width: 100%;
    justify-content: center;
    text-align: center;
    color: #ffffff !important;
    margin-top: 4px;
}

[data-testid="stMetric"] > div {
    align-items: center;
}

input {
    color: #ffffff !important;
}

[data-baseweb="select"] {
    color: #ffffff !important;
}

.stButton > button {
    background-color: #292a2d;
    color: #ffffff;
    border: 1px solid #5f6368;
    border-radius: 8px;
}

.stButton > button:hover {
    background-color: #3c4043;
    border-color: #ffffff;
}

[data-testid="stExpander"] {
    background: rgba(32,33,36,0.90);
    border: 1px solid rgba(255,255,255,0.12);
}

hr {
    border-color: rgba(255,255,255,0.15);
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# YOUR GPA SCALE
# =========================================================

grade_points = {
    "A": 4.00,
    "A-": 3.70,
    "B+": 3.40,
    "B": 3.10,
    "B-": 2.90,
    "C+": 2.60,
    "C": 2.30,
    "C-": 2.00,
    "D+": 2.00,
    "D": 1.50,
    "D-": 1.00,
    "F": 0.00
}

grade_options = list(grade_points.keys())

# =========================================================
# SESSION STATE
# =========================================================

if "courses" not in st.session_state:
    st.session_state.courses = [
        {"name": "", "grade": "A", "credits": 3}
    ]

# Unique IDs prevent widget values shifting when deleting courses.
if "next_course_id" not in st.session_state:
    st.session_state.next_course_id = 1

if "course_ids" not in st.session_state:
    st.session_state.course_ids = [0]


# =========================================================
# FUNCTIONS
# =========================================================

def add_course():
    new_id = st.session_state.next_course_id
    st.session_state.next_course_id += 1

    st.session_state.courses.append({
        "name": "",
        "grade": "A",
        "credits": 3
    })

    st.session_state.course_ids.append(new_id)


def delete_course(index):
    if len(st.session_state.courses) > 1:
        st.session_state.courses.pop(index)
        st.session_state.course_ids.pop(index)
    else:
        st.session_state.courses[0] = {
            "name": "",
            "grade": "A",
            "credits": 3
        }

        course_id = st.session_state.course_ids[0]
        for field in ("name", "grade", "credits"):
            key = f"{field}_{course_id}"
            if key in st.session_state:
                del st.session_state[key]


def reset_courses():
    for course_id in st.session_state.course_ids:
        for field in ("name", "grade", "credits"):
            key = f"{field}_{course_id}"
            if key in st.session_state:
                del st.session_state[key]

    st.session_state.courses = [
        {"name": "", "grade": "A", "credits": 3}
    ]
    st.session_state.course_ids = [0]


# =========================================================
# TITLE
# =========================================================

st.title("GPA Calculator")
st.write(
    "Enter your courses, grades, and credits to calculate "
    "your cumulative GPA."
)

# Reserve the summary's position at the top.
# We fill it after the inputs have been updated.
summary_placeholder = st.empty()

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
    course_id = st.session_state.course_ids[i]

    col1, col2, col3, col4 = st.columns([5, 2, 2, 0.7])

    with col1:
        course["name"] = st.text_input(
            "Course Name",
            value=course["name"],
            key=f"name_{course_id}",
            placeholder="Course name",
            label_visibility="collapsed"
        )

    with col2:
        course["grade"] = st.selectbox(
            "Grade",
            grade_options,
            index=grade_options.index(course["grade"]),
            key=f"grade_{course_id}",
            label_visibility="collapsed"
        )

    with col3:
        course["credits"] = st.number_input(
            "Credits",
            min_value=1,
            max_value=100,
            value=int(course["credits"]),
            step=1,
            key=f"credits_{course_id}",
            label_visibility="collapsed"
        )

    with col4:
        st.button(
            "×",
            key=f"delete_{course_id}",
            on_click=delete_course,
            args=(i,),
            use_container_width=True
        )

# =========================================================
# CALCULATE USING THE LATEST INPUT VALUES
# =========================================================

total_credits = sum(
    int(course["credits"])
    for course in st.session_state.courses
)

total_points = sum(
    grade_points[course["grade"]] * int(course["credits"])
    for course in st.session_state.courses
)

cumulative_gpa = (
    total_points / total_credits
    if total_credits > 0
    else 0.0
)

# =========================================================
# SUMMARY — DISPLAYED AT THE TOP
# =========================================================

with summary_placeholder.container():
    st.subheader("Summary")

    summary1, summary2, summary3 = st.columns(3)

    with summary1:
        st.metric(
            label="Cumulative GPA",
            value=f"{cumulative_gpa:.2f}"
        )

    with summary2:
        st.metric(
            label="Total Credits",
            value=str(total_credits)
        )

    with summary3:
        st.metric(
            label="Total Points",
            value=f"{total_points:.2f}"
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
    for grade, points in grade_points.items():
        st.write(f"{grade} = {points:.2f}")
