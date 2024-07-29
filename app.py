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
st.header("📊Data Professionals Salary Dashboard",divider="rainbow")
st.markdown("###")

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
    df_selection.groupby(by="job_title").sum()[["salary_in_usd"]].sort_values(by="salary_in_usd", ascending=False)
)
fig_income_by_job_title = px.bar(
    income_by_job_title,
    x="salary_in_usd",
    y=income_by_job_title.index,
    title="<b>Total Income by Job Title</b>",
    template="plotly_white",
    color=income_by_job_title.index,
    orientation="h"
)
fig_income_by_job_title.update_layout(
    legend_title_text="Job Title",
    showlegend=False,
    xaxis_title="Total Income (US $)",
    yaxis_title="Job Title",
    title_x=0.5
)

# Average Salary by Experience Level
avg_salary_by_exp_level = (
    df_selection.groupby(by="experience_level")[["salary_in_usd"]].mean().sort_values(by="salary_in_usd", ascending=False)
)
fig_avg_salary_by_exp_level = px.bar(
    avg_salary_by_exp_level,
    x=avg_salary_by_exp_level.index,
    y="salary_in_usd",
    title="<b>Average Salary by Experience Level</b>",
    template="plotly_white",
    color=avg_salary_by_exp_level.index
)
fig_avg_salary_by_exp_level.update_layout(
    legend_title_text="Experience Level",
    showlegend=False,
    xaxis_title="Experience Level",
    yaxis_title="Average Salary (US $)",
    title_x=0.5
)

left_column, right_column = st.columns(2)
with left_column:
    st.plotly_chart(fig_income_by_job_title)

with right_column:
    st.plotly_chart(fig_avg_salary_by_exp_level)

# Distribution proportion of Remote Ratio
remote_ratio_distribution = (
    df_selection["remote_ratio"].value_counts(normalize=True) * 100
).sort_values(ascending=False)

fig_remote_ratio_distribution = px.pie(
    remote_ratio_distribution,
    values=remote_ratio_distribution.values,
    names=remote_ratio_distribution.index,
    title="<b>Remote Ratio Distribution</b>",
    template="plotly_white",
    color=remote_ratio_distribution.index,
    hole=0.3,
)
fig_remote_ratio_distribution.update_traces(
    textposition="outside",
    textinfo="percent+label"
)
fig_remote_ratio_distribution.update_layout(title_x=0.3)

# Distribution proportion of Company Size
company_size_distribution = (
    df_selection["company_size"].value_counts(normalize=True) * 100
).sort_values(ascending=False)

fig_company_size_distribution = px.pie(
    company_size_distribution,
    values=company_size_distribution.values,
    names=company_size_distribution.index,
    title="<b>Company Size Distribution</b>",
    template="plotly_white",
    color=company_size_distribution.index,
    hole=0.3,
)
fig_company_size_distribution.update_traces(
    textposition="outside",
    textinfo="percent+label"
)
fig_company_size_distribution.update_layout(title_x=0.3)

left_column, right_column = st.columns(2)
with left_column:
    st.plotly_chart(fig_remote_ratio_distribution)

with right_column:
    st.plotly_chart(fig_company_size_distribution)