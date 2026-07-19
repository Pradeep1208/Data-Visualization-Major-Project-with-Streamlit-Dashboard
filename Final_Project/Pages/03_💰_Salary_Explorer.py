"""
pages/03_💰_Salary_Explorer.py — Salary Explorer
Purpose: analyze salary trends by industry, state, job title, and company size.
Filters: State, Industry, Job Title
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import plotly.express as px

from utils import load_data
from config import PLOTLY_TEMPLATE, COLOR_SEQUENCE

st.header(" Salary Explorer — How do salaries break down across the market")

df = load_data()

with st.sidebar:
    st.subheader("Filters")
    states = st.multiselect("State", sorted(df["job_state"].unique()))
    industries = st.multiselect("Industry", sorted(df["Industry"].unique()))
    titles = st.multiselect("Job Title", sorted(df["job_simp"].unique()))

f_df = df.copy()
if states:
    f_df = f_df[f_df["job_state"].isin(states)]
if industries:
    f_df = f_df[f_df["Industry"].isin(industries)]
if titles:
    f_df = f_df[f_df["job_simp"].isin(titles)]

# st.caption(f"Showing **{len(f_df):,}** of {len(df):,} job postings after filters")
st.caption(f"Breaking down **{len(f_df):,}** job postings by industry, state, title, and company size")

col1, col2 = st.columns(2)

with col1:
    ind_df = f_df.groupby("Industry", as_index=False)["avg_salary"].mean().sort_values(
        "avg_salary", ascending=False
    ).head(12)
    fig = px.bar(
        ind_df, x="avg_salary", y="Industry", orientation="h",
        title="Salary by Industry",
        labels={"avg_salary": "Average Salary ($K)"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    state_df = f_df.groupby("job_state", as_index=False)["avg_salary"].mean().sort_values(
        "avg_salary", ascending=False
    ).head(12)
    fig = px.bar(
        state_df, x="avg_salary", y="job_state", orientation="h",
        title="Salary by State",
        labels={"avg_salary": "Average Salary ($K)", "job_state": "State"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Salary by Job Title")
title_df = f_df.groupby("job_simp", as_index=False)["avg_salary"].mean().sort_values(
    "avg_salary", ascending=False
)
fig = px.bar(
    title_df, x="job_simp", y="avg_salary",
    title="Average Salary by Job Title",
    labels={"avg_salary": "Average Salary ($K)", "job_simp": "Job Title"},
    template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
)
st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig = px.histogram(
        f_df, x="avg_salary", nbins=40,
        title="Salary Distribution",
        labels={"avg_salary": "Average Salary ($K)"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
    )
    st.plotly_chart(fig, use_container_width=True)

with col4:
    fig = px.box(
        f_df, x="Size", y="avg_salary",
        title="Salary by Company Size",
        labels={"avg_salary": "Average Salary ($K)", "Size": "Company Size"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_layout(xaxis_tickangle=-20)
    st.plotly_chart(fig, use_container_width=True)
