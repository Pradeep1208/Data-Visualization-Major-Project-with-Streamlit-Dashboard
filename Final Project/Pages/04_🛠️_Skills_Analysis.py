"""
pages/04_🛠️_Skills_Analysis.py — Skills Analysis
Purpose: analyze technical skill demand and its impact on salary.
Skills: Python, SQL, AWS, Spark, Excel, Tableau, Power BI
Filters: Industry, State, Skill
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff

from utils import load_data
from config import PLOTLY_TEMPLATE, COLOR_SEQUENCE, SKILL_COLS, SKILL_LABELS

st.header(" Skills Analysis — Which technical skills are worth learning")

df = load_data()

with st.sidebar:
    st.subheader("Filters")
    industries = st.multiselect("Industry", sorted(df["Industry"].unique()))
    states = st.multiselect("State", sorted(df["job_state"].unique()))
    skill_choice = st.selectbox("Focus Skill", ["All"] + [SKILL_LABELS[c] for c in SKILL_COLS])

f_df = df.copy()
if industries:
    f_df = f_df[f_df["Industry"].isin(industries)]
if states:
    f_df = f_df[f_df["job_state"].isin(states)]

# st.caption(f"Showing **{len(f_df):,}** of {len(df):,} job postings after filters")
st.caption(f"Ranking which technical skills pay off, based on **{len(f_df):,}** job postings")

# ── Skill demand ──────────────────────────────────────────────────────
demand = f_df[SKILL_COLS].sum().reset_index()
demand.columns = ["skill", "count"]
demand["skill"] = demand["skill"].map(SKILL_LABELS)
demand = demand.sort_values("count", ascending=False)

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        demand, x="skill", y="count",
        title="Skill Demand ( Job Postings Mentioning Skill)",
        labels={"count": " Postings", "skill": "Skill"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    skill_salary = []
    for c in SKILL_COLS:
        avg_yes = f_df.loc[f_df[c] == 1, "avg_salary"].mean()
        avg_no = f_df.loc[f_df[c] == 0, "avg_salary"].mean()
        skill_salary.append({"skill": SKILL_LABELS[c], "Requires Skill": avg_yes, "No Skill": avg_no})
    skill_salary_df = pd.DataFrame(skill_salary).melt(id_vars="skill", var_name="group", value_name="avg_salary")
    fig = px.bar(
        skill_salary_df, x="skill", y="avg_salary", color="group", barmode="group",
        title="Average Salary: With vs. Without Each Skill",
        labels={"avg_salary": "Average Salary ($K)", "skill": "Skill"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Skill Demand Across Industries")
top_industries = f_df["Industry"].value_counts().head(8).index
ind_skill_df = f_df[f_df["Industry"].isin(top_industries)]
skill_by_industry = ind_skill_df.groupby("Industry")[SKILL_COLS].sum().reset_index()
melted = skill_by_industry.melt(id_vars="Industry", var_name="skill", value_name="mentions")
melted["skill"] = melted["skill"].map(SKILL_LABELS)
fig = px.bar(
    melted, x="Industry", y="mentions", color="skill",
    title="Skill Demand by Industry (Stacked)",
    labels={"mentions": " Postings"},
    template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
)
fig.update_layout(xaxis_tickangle=-35, barmode="stack")
st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Skill Correlation Heatmap")
    corr = f_df[SKILL_COLS].corr()
    labels_clean = [SKILL_LABELS[c] for c in SKILL_COLS]
    fig = ff.create_annotated_heatmap(
        z=np.round(corr.values, 2), x=labels_clean, y=labels_clean,
        colorscale="Viridis", showscale=True,
    )
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("Top Skill Combinations")
    f_df = f_df.copy()
    f_df["skill_combo"] = f_df[SKILL_COLS].apply(
        lambda row: ", ".join([SKILL_LABELS[c] for c in SKILL_COLS if row[c] == 1]) or "None", axis=1
    )
    combo_df = f_df["skill_combo"].value_counts().head(10).reset_index()
    combo_df.columns = ["Combination", "Count"]
    fig = px.bar(
        combo_df, x="Count", y="Combination", orientation="h",
        title="Top 10 Skill Combinations",
        template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)
