"""
pages/02_🏢_Company_Analysis.py — Company Analysis
Purpose: analyze company characteristics (rating, revenue, size, age) vs. salary.
Filters: Company, Revenue, Company Size, Industry
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import plotly.express as px

from utils import load_data
from config import PLOTLY_TEMPLATE, COLOR_SEQUENCE

st.header(" Company Analysis — Which companies and company traits pay the most")

df = load_data()

with st.sidebar:
    st.subheader("Filters")
    companies = st.multiselect("Company", sorted(df["company_txt"].unique()))
    revenues = st.multiselect("Revenue", sorted(df["Revenue"].unique()))
    sizes = st.multiselect("Company Size", sorted(df["Size"].unique()))
    industries = st.multiselect("Industry", sorted(df["Industry"].unique()))

f_df = df.copy()
if companies:
    f_df = f_df[f_df["company_txt"].isin(companies)]
if revenues:
    f_df = f_df[f_df["Revenue"].isin(revenues)]
if sizes:
    f_df = f_df[f_df["Size"].isin(sizes)]
if industries:
    f_df = f_df[f_df["Industry"].isin(industries)]

# st.caption(f"Showing **{len(f_df):,}** of {len(df):,} job postings after filters")
st.caption(f"Comparing **{f_df['company_txt'].nunique():,}** companies across **{len(f_df):,}** postings to see which pay the most")

st.subheader("Top Paying Companies")
top_companies = (
    f_df.groupby("company_txt", as_index=False)["avg_salary"].mean()
    .sort_values("avg_salary", ascending=False).head(15)
)
fig = px.bar(
    top_companies, x="avg_salary", y="company_txt", orientation="h",
    title="Top 15 Companies by Average Salary",
    labels={"avg_salary": "Average Salary ($K)", "company_txt": "Company"},
    template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
)
fig.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    fig = px.scatter(
        f_df[f_df["Rating"] > 0], x="Rating", y="avg_salary", color="Industry",
        trendline="ols", opacity=0.6,
        title="Salary vs. Company Rating",
        labels={"avg_salary": "Average Salary ($K)"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    rev_df = f_df.groupby("Revenue", as_index=False)["avg_salary"].mean()
    fig = px.bar(
        rev_df, x="Revenue", y="avg_salary",
        title="Revenue vs. Average Salary",
        labels={"avg_salary": "Average Salary ($K)"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    size_df = f_df.groupby("Size", as_index=False)["avg_salary"].mean()
    fig = px.bar(
        size_df, x="Size", y="avg_salary",
        title="Company Size vs. Average Salary",
        labels={"avg_salary": "Average Salary ($K)"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_layout(xaxis_tickangle=-20)
    st.plotly_chart(fig, use_container_width=True)

with col4:
    age_df = f_df[(f_df["age"] > 0) & (f_df["age"] < 200)]
    fig = px.scatter(
        age_df, x="age", y="avg_salary", trendline="ols", opacity=0.6,
        title="Company Age vs. Average Salary",
        labels={"age": "Company Age (Years)", "avg_salary": "Average Salary ($K)"},
        template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
    )
    st.plotly_chart(fig, use_container_width=True)
