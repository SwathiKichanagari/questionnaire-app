import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ===============================
# LOAD DATA
# ===============================
@st.cache_data
def load_data():
    return pd.read_excel("questionnaire.xlsx", sheet_name=None)

data = load_data()

# ===============================
# SIDEBAR
# ===============================
st.sidebar.header("Filters")

domain = st.sidebar.selectbox("Select Domain", list(data.keys()))

df = data[domain]
df.columns = ["Category", "Question", "Notes", "Priority"]

categories = df["Category"].unique()
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    categories,
    default=categories
)

filtered_df = df[df["Category"].isin(selected_categories)]

# ===============================
# SESSION STATE INIT
# ===============================
if "checkbox_state" not in st.session_state:
    st.session_state.checkbox_state = {}

# ===============================
# MAIN UI
# ===============================
st.title("📋 Integration Questionnaire Generator")

# ===============================
# BUTTONS (WORKING)
# ===============================
col1, col2 = st.columns(2)

with col1:
    if st.button("Select All"):
        for i in filtered_df.index:
            key = f"{domain}_{i}"
            st.session_state[key] = True

with col2:
    if st.button("Deselect All"):
        for i in filtered_df.index:
            key = f"{domain}_{i}"
            st.session_state[key] = False

# ===============================
# DISPLAY QUESTIONS
# ===============================
st.subheader(f"Questions for: {domain}")

selected_questions = []
current_category = None

for i, row in filtered_df.iterrows():

    category = row["Category"]
    question = f"{category} → {row['Question']}"

    if category != current_category:
        st.markdown(f"### {category}")
        current_category = category

    key = f"{domain}_{i}"

    # IMPORTANT: initialize only once
    if key not in st.session_state:
        st.session_state[key] = False

    # NO value= HERE
    val = st.checkbox(question, key=key)

    if val:
        selected_questions.append({
            "Category": category,
            "Question": row["Question"],
            "Priority": row["Priority"]
        })

# ===============================
# EXPORT
# ===============================
st.divider()

if selected_questions:
    export_df = pd.DataFrame(selected_questions)

    st.download_button(
        "Download Selected Questions",
        export_df.to_csv(index=False),
        file_name=f"{domain}_questions.csv",
        mime="text/csv"
    )
else:
    st.info("No questions selected")
