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

# CSS for styling
css = """
<style>
.user-select-none.svg-container {
    border: 2px solid #1c87c9;
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0 0 5px #1c87c9, 0 0 15px #1c87c9, 0 0 20px #1c87c9;
    margin-bottom: 20px;
}

.footer {
    width: 100%;
    background-color: #f1f1f1;
    color: #333;
    text-align: center;
    padding: 10px;
    border-top: 1px solid #e5e5e5;
    box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
    font-family: 'Arial', sans-serif;
    font-size: 16px;
    position: relative;
    bottom: 0;
    margin-top: 20px; /* Add some space between the content and the footer */
}

.footer a {
    color: #1c87c9;
    text-decoration: none;
    margin: 0 10px;
}

.footer a:hover {
    text-decoration: underline;
}

.footer .icon {
    width: 24px;
    height: 24px;
    vertical-align: middle;
    margin-right: 5px;
}
</style>
"""

# HTML for the footer
footer_html = """
<div class="footer">
    <p>Developed by Anubhav Yadav</p>
    <p>
        <a href="https://www.linkedin.com/in/anubhav-yadav-data-science" target="_blank">
            <img src="" class="icon" />LinkedIn
        </a>
        |
        <a href="https://github.com/AnubhavYadavBCA25" target="_blank">
            <img src="" class="icon" />GitHub
        </a>
    </p>
</div>
"""
# Inject CSS for styling
st.markdown(css, unsafe_allow_html=True)

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
avg_income = int(df_selection["salary_in_usd"].mean())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader('Total Records:')
    st.subheader(f"{total_records:,}")
with middle_column:
    st.subheader("Total Income:")
    st.subheader(f"US ${total_income:,}")
with right_column:
    st.subheader("Average Income:")
    st.subheader(f"US ${avg_income:,}")

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
    title_x=0.2
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
    title_x=0.2
)

left_column, right_column = st.columns(2)
with left_column:
    st.plotly_chart(fig_income_by_job_title)

with right_column:
    st.plotly_chart(fig_avg_salary_by_exp_level)

# Total Earned by Year and Job Title
total_earned_by_year_job_title = (
    df_selection.groupby(by=["work_year", "job_title"]).sum()[["salary_in_usd"]].sort_values(by="salary_in_usd", ascending=True)
)
fig_total_earned_by_year_job_title = px.line(
    total_earned_by_year_job_title,
    x=total_earned_by_year_job_title.index.get_level_values(0),
    y="salary_in_usd",
    title="<b>Total Earned by Year and Job Title</b>",
    template="plotly_white",
    color=total_earned_by_year_job_title.index.get_level_values(1),
    markers=True,
    line_shape="spline"
)
fig_total_earned_by_year_job_title.update_layout(
    legend_title_text="Job Title",
    xaxis_title="Work Year",
    yaxis_title="Total Earned (US $)",
    title_x=0.4
)
st.plotly_chart(fig_total_earned_by_year_job_title)

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

# Top 5 Company Locations with Highest Average Salary
top_5_locations_avg_salary = (
    df_selection.groupby(by="company_location")[["salary_in_usd"]].mean().sort_values(by="salary_in_usd", ascending=False).head(5)
)
fig_top_5_locations_avg_salary = px.bar(
    top_5_locations_avg_salary,
    x=top_5_locations_avg_salary.index,
    y="salary_in_usd",
    title="<b>Top 5 Company Locations with Highest Average Salary</b>",
    template="plotly_white",
    color=top_5_locations_avg_salary.index
)
fig_top_5_locations_avg_salary.update_layout(
    legend_title_text="Location",
    showlegend=False,
    xaxis_title="Company Location",
    yaxis_title="Average Salary (US $)",
    title_x=0.2
)

# Total Count of Experience Level
exp_level_count = df_selection["experience_level"].value_counts().sort_values(ascending=False)
fig_exp_level_count = px.bar(
    exp_level_count,
    y=exp_level_count.index,
    x=exp_level_count.values,
    title="<b>Total Count of Experience Level</b>",
    template="plotly_white",
    color=exp_level_count.index,
    orientation="h"
)
fig_exp_level_count.update_layout(
    legend_title_text="Experience Level",
    showlegend=False,
    xaxis_title="Total Count",
    yaxis_title="Experience Level",
    title_x=0.2
)

left_column, right_column = st.columns(2)
with left_column:
    st.plotly_chart(fig_top_5_locations_avg_salary)
with right_column:
    st.plotly_chart(fig_exp_level_count)

#---------------------------------Footer---------------------------------
st.markdown(footer_html, unsafe_allow_html=True)