import streamlit as st
import pandas as pd

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Questionnaire Generator", layout="wide")

# -------------------------
# Title
# -------------------------
st.markdown("## 📋 Integration Questionnaire Generator")

# -------------------------
# Load Excel
# -------------------------
@st.cache_data
def load_data():
    return pd.read_excel("questionnaire.xlsx", sheet_name=None)

data = load_data()

# -------------------------
# Sidebar (Professional UI)
# -------------------------
st.sidebar.title("Filters")

domain = st.sidebar.selectbox("Select Domain", list(data.keys()))

df = data[domain]

categories = df["Category"].dropna().unique()
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    categories,
    default=categories
)

# -------------------------
# Filter Data
# -------------------------
filtered_df = df[df["Category"].isin(selected_categories)]

# -------------------------
# Select All Option
# -------------------------
select_all = st.checkbox("Select All Questions", value=True)

st.markdown(f"### Questions for: {domain}")

selected_rows = []

for i, row in filtered_df.iterrows():
    checked = select_all

    if st.checkbox(
        f"{row['Category']} → {row['Detailed Question']}",
        value=checked,
        key=i
    ):
        selected_rows.append(row)

# -------------------------
# Export Section
# -------------------------
st.markdown("---")
st.subheader("Export")

if selected_rows:
    export_df = pd.DataFrame(selected_rows)

    file_name = f"{domain}_Questionnaire.xlsx"

    export_df.to_excel(file_name, index=False)

    with open(file_name, "rb") as f:
        st.download_button(
            label="Download Excel",
            data=f,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.warning("No questions selected")