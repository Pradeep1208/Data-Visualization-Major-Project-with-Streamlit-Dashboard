"""
pages/01_📊_Dashboard.py — Dashboard Overview
Purpose: provide an overall summary of the Glassdoor dataset.
Filters: Industry, State, Company Size
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import plotly.express as px

from utils import load_data
from config import PLOTLY_TEMPLATE, COLOR_SEQUENCE

st.header("Dashboard Overview — What does the job market look like overall")

df = load_data()

# ── Filters ────────────────────────────────────────────────────────────
with st.sidebar:
    st.subheader("Filters")
    industries = st.multiselect("Industry", sorted(df["Industry"].unique()))
    states = st.multiselect("State", sorted(df["job_state"].unique()))
    sizes = st.multiselect("Company Size", sorted(df["Size"].unique()))

f_df = df.copy()
if industries:
    f_df = f_df[f_df["Industry"].isin(industries)]
if states:
    f_df = f_df[f_df["job_state"].isin(states)]
if sizes:
    f_df = f_df[f_df["Size"].isin(sizes)]

st.caption(f"Showing **{len(f_df):,}** of {len(df):,} job postings after filters")

col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(
        f_df, x="avg_salary", nbins=40,
        title="Salary Distribution",
        labels={"avg_salary": "Average Salary ($K)"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    rating_df = f_df[f_df["Rating"] > 0]
    fig = px.histogram(
        rating_df, x="Rating", nbins=20,
        title="Company Rating Distribution",
        template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
    )
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    ind_salary = f_df.groupby("Industry", as_index=False)["avg_salary"].mean().sort_values(
        "avg_salary", ascending=False
    ).head(10)
    fig = px.bar(
        ind_salary, x="avg_salary", y="Industry", orientation="h",
        title="Top 10 Industries by Average Salary",
        labels={"avg_salary": "Average Salary ($K)"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

with col4:
    state_salary = f_df.groupby("job_state", as_index=False)["avg_salary"].mean().sort_values(
        "avg_salary", ascending=False
    ).head(10)
    fig = px.bar(
        state_salary, x="job_state", y="avg_salary",
        title="Top 10 States by Average Salary",
        labels={"avg_salary": "Average Salary ($K)", "job_state": "State"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Top Hiring Industries")
hiring = f_df["Industry"].value_counts().head(10).reset_index()
hiring.columns = ["Industry", "Job Postings"]
fig = px.bar(
    hiring, x="Job Postings", y="Industry", orientation="h",
    template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
)
fig.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig, use_container_width=True)
