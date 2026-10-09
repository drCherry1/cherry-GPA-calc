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
        linear-gradient(
            120deg,
            transparent 49.5%,
            rgba(255, 255, 255, 0.08) 50%,
            transparent 50.5%
        ),
        linear-gradient(
            30deg,
            transparent 49.5%,
            rgba(255, 255, 255, 0.045) 50%,
            transparent 50.5%
        );

    background-size: 220px 220px;

    animation: backgroundMove 30s linear infinite;
}


@keyframes backgroundMove {

    0% {
        background-position:
            0px 0px,
            0px 0px;
    }

    50% {
        background-position:
            110px 70px,
            -70px 100px;
    }

    100% {
        background-position:
            220px 140px,
            -140px 200px;
    }

}


.block-container {
    position: relative;
    z-index: 1;

    max-width: 900px;

    padding-top: 3rem;
    padding-bottom: 3rem;
}


h1,
h2,
h3,
h4,
h5,
h6,
p,
label {
    color: #f1f3f4 !important;
}


/* =========================================================
   GPA SUMMARY
   ========================================================= */

[data-testid="stMetric"] {

    background: rgba(32, 33, 36, 0.92);

    border: 1px solid rgba(255, 255, 255, 0.12);

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


/* =========================================================
   INPUTS
   ========================================================= */

[data-testid="stTextInput"],
[data-testid="stSelectbox"],
[data-testid="stNumberInput"] {

    background: rgba(32, 33, 36, 0.92);
}


input {

    color: #ffffff !important;
}


[data-baseweb="select"] {

    color: #ffffff !important;
}


/* =========================================================
   BUTTONS
   ========================================================= */

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


/* =========================================================
   EXPANDER
   ========================================================= */

[data-testid="stExpander"] {

    background: rgba(32, 33, 36, 0.90);

    border: 1px solid rgba(255, 255, 255, 0.12);
}


/* =========================================================
   DIVIDER
   ========================================================= */

hr {

    border-color: rgba(255, 255, 255, 0.15);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# GPA SCALE
# =========================================================

grade_points = {

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
            "credits": 3
        }

    ]


# =========================================================
# FUNCTIONS
# =========================================================

def add_course():

    st.session_state.courses.append({

        "name": "",
        "grade": "A",
        "credits": 3

    })


def delete_course(index):

    if len(st.session_state.courses) > 1:

        st.session_state.courses.pop(index)

    else:

        st.session_state.courses[0] = {

            "name": "",
            "grade": "A",
            "credits": 3

        }


def reset_courses():

    st.session_state.courses = [

        {
            "name": "",
            "grade": "A",
            "credits": 3
        }

    ]


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


# ---------------------------------------------------------
# IMPORTANT:
# Read the CURRENT widget values from session state.
# ---------------------------------------------------------

current_credits = 0
current_points = 0.0


for i, course in enumerate(st.session_state.courses):

    credit_key = f"credits_{i}"
    grade_key = f"grade_{i}"

    if credit_key in st.session_state:

        credits = int(
            st.session_state[credit_key]
        )

    else:

        credits = int(
            course["credits"]
        )


    if grade_key in st.session_state:

        grade = st.session_state[grade_key]

    else:

        grade = course["grade"]


    current_credits += credits

    current_points += (
        grade_points[grade] * credits
    )


if current_credits > 0:

    current_gpa = (
        current_points / current_credits
    )

else:

    current_gpa = 0.0


# ---------------------------------------------------------
# GPA
# ---------------------------------------------------------

with summary1:

    st.metric(
        label="Cumulative GPA",
        value=f"{current_gpa:.2f}"
    )


# ---------------------------------------------------------
# TOTAL CREDITS
# ---------------------------------------------------------

with summary2:

    st.metric(
        label="Total Credits",
        value=f"{current_credits}"
    )


# ---------------------------------------------------------
# TOTAL POINTS
# ---------------------------------------------------------

with summary3:

    st.metric(
        label="Total Points",
        value=f"{current_points:.2f}"
    )


# =========================================================
# COURSES
# =========================================================

st.subheader("Courses")


# =========================================================
# COURSE HEADERS
# =========================================================

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

            "Course Name",

            value=course["name"],

            key=f"name_{i}",

            placeholder="Course name",

            label_visibility="collapsed"
        )


    # -----------------------------------------------------
    # GRADE
    # -----------------------------------------------------

    with col2:

        course["grade"] = st.selectbox(

            "Grade",

            grade_options,

            index=grade_options.index(
                course["grade"]
            ),

            key=f"grade_{i}",

            label_visibility="collapsed"
        )


    # -----------------------------------------------------
    # CREDITS
    # -----------------------------------------------------
    # WHOLE NUMBERS ONLY

    with col3:

        course["credits"] = st.number_input(

            "Credits",

            min_value=1,

            max_value=100,

            value=int(course["credits"]),

            step=1,

            key=f"credits_{i}",

            label_visibility="collapsed"
        )


    # -----------------------------------------------------
    # DELETE
    # -----------------------------------------------------

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
