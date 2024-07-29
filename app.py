# Import Relevant Libraries
import pandas as pd
import plotly.express as px
import streamlit as st

# Streamlit page configuration
st.set_page_config(
    page_title="Salary Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Dataframe
def get_data_from_csv():
    df = pd.read_csv("cleaned_data_ds_salaries.csv")
    df_temp = df.copy()

    # Convert work year column from integer to string
    df_temp["work_year"] = df_temp["work_year"].astype(str)
    return df_temp
df_temp = get_data_from_csv()

# ------------------------------ Sidebar ------------------------------

# Job Title Filter
st.sidebar.header("Please Filter the Data Here:")
job_title = st.sidebar.multiselect(
    "Select Job Title",
    options=df_temp["job_title"].unique(),
    default=df_temp['job_title'].unique(),
    key="job_title"
)

# Work Year Filter
work_year = st.sidebar.multiselect(
    "Select Work Year",
    options=df_temp["work_year"].unique(),
    default=df_temp['work_year'].unique(),
    key="work_year"
)

# Experience Level Filter
exp_level = st.sidebar.multiselect(
    "Select Experience Level",
    options=df_temp["experience_level"].unique(),
    default=df_temp['experience_level'].unique(),
    key="exp_level"
)

# Remote Ratio Filter
remote_ratio = st.sidebar.multiselect(
    "Select Working Style",
    options=df_temp["remote_ratio"].unique(),
    default=df_temp['remote_ratio'].unique(),
    key="remote_ratio"
)

# Company Size Filter
company_size = st.sidebar.multiselect(
    "Select Company Size",
    options=df_temp["company_size"].unique(),
    default=df_temp['company_size'].unique(),
    key="company_size"
)

# Apply Filters Function
df_selection = df_temp.query(
    "(job_title == @job_title) and (work_year == @work_year) and (experience_level == @exp_level) and (remote_ratio in @remote_ratio) and (company_size == @company_size)"
)

# ------------------------------ Main Panel ------------------------------
st.title("📊Data Professionals Salary Dashboard")
st.markdown("##")

# Top KPI's 
total_records = int(df_selection.shape[0])
total_income = int(df_selection["salary_in_usd"].sum())

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Records:")
    st.subheader(f"{total_records:,}")

with right_column:
    st.subheader("Total Income:")
    st.subheader(f"US ${total_income:,}")

st.divider()

# Total Income by Job Title
income_by_job_title = (
    df_selection.groupby(by="job_title").sum()[["salary_in_usd"]].sort_values(by="salary_in_usd", ascending=True)
)
fig_income_by_job_title = px.bar(
    income_by_job_title,
    x="salary_in_usd",
    y=income_by_job_title.index,
    title="<b>Total Income by Job Title</b>",
    labels={"salary_in_usd": "Total Income (US $)", "index": "Job Title"},
    template="plotly_white",
    color_discrete_sequence=["#FFA07A"],
    orientation="h"
)
st.plotly_chart(fig_income_by_job_title)