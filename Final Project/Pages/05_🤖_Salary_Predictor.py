"""
pages/05_🤖_Salary_Predictor.py — Salary Predictor
Purpose: predict salary using the ML model trained in the companion notebook.
Loads: models/salary_model.pkl, models/scaler.pkl, models/encoder.pkl
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import plotly.express as px
import pandas as pd

from utils import load_data, load_model_artifacts, predict_salary
from config import PLOTLY_TEMPLATE, COLOR_SEQUENCE, SKILL_LABELS

st.header("Salary Predictor — What would this job pay")
# st.caption("Model trained in the companion notebook (best of Linear Regression / Decision Tree / "
#            "Random Forest / Gradient Boosting / XGBoost, selected by R² on a held-out test set).")
st.caption(f"Estimating what this job would pay, based on a model trained on historical postings")

df = load_data()
model, scaler, encoders = load_model_artifacts()


with st.form("predictor_form"):
    st.subheader("Job & Company Details")

    c1, c2, c3 = st.columns(3)
    with c1:
        rating = st.slider("Company Rating", 1.0, 5.0, 3.8, 0.1)
        size = st.selectbox("Company Size", sorted(df["Size"].unique()))
        ownership = st.selectbox("Type of Ownership", sorted(df["Type of ownership"].unique()))
    with c2:
        industry = st.selectbox("Industry", sorted(df["Industry"].unique()))
        sector = st.selectbox("Sector", sorted(df["Sector"].unique()))
        revenue = st.selectbox("Revenue", sorted(df["Revenue"].unique()))
    with c3:
        job_state = st.selectbox("Job State", sorted(df["job_state"].unique()))
        job_simp = st.selectbox("Job Title Type", sorted(df["job_simp"].unique()))
        seniority = st.selectbox("Seniority", sorted(df["seniority"].unique()))

    age = st.slider("Company Age (Years)", 0, 200, 15)
    same_state = st.checkbox("Job located in same state as HQ", value=True)

    st.subheader("Required Technical Skills")
    s1, s2, s3, s4, s5, s6, s7 = st.columns(7)
    python = s1.checkbox("Python", value=True)
    sql = s2.checkbox("SQL")
    aws = s3.checkbox("AWS")
    spark = s4.checkbox("Spark")
    excel = s5.checkbox("Excel")
    tableau = s6.checkbox("Tableau")
    powerbi = s7.checkbox("Power BI")

    submitted = st.form_submit_button(" Predict Salary", use_container_width=True)

if submitted:
    prediction = predict_salary(
        rating=rating, size=size, ownership=ownership, industry=industry, sector=sector,
        revenue=revenue, job_state=job_state, same_state=int(same_state), age=age,
        python=int(python), sql=int(sql), aws=int(aws), spark=int(spark),
        excel=int(excel), tableau=int(tableau), powerbi=int(powerbi),
        job_simp=job_simp, seniority_level=seniority,
    )

    margin = max(round(prediction * 0.12, 1), 5)  # display a rough +/- range around the point estimate

    st.success("Prediction complete!")
    m1, m2, m3 = st.columns(3)
    m1.metric("Predicted Salary", f"${prediction}K")
    m2.metric("Estimated Range", f"${round(prediction - margin, 1)}K – ${round(prediction + margin, 1)}K")

    if hasattr(model, "score"):
        m3.metric("Model Type", type(model).__name__)

    # ── Feature importance (if the chosen model supports it) ──────────
    if hasattr(model, "feature_importances_"):
        from config import MODEL_FEATURE_COLS
        importance_df = pd.DataFrame({
            "Feature": MODEL_FEATURE_COLS,
            "Importance": model.feature_importances_,
        }).sort_values("Importance", ascending=True)
        fig = px.bar(
            importance_df, x="Importance", y="Feature", orientation="h",
            title="What drives this prediction? (Model Feature Importance)",
            template=PLOTLY_TEMPLATE, color_discrete_sequence=COLOR_SEQUENCE,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Where this prediction sits in the overall distribution ────────
    fig = px.histogram(
        df, x="avg_salary", nbins=40, template=PLOTLY_TEMPLATE,
        title="Your Prediction vs. Overall Salary Distribution",
        labels={"avg_salary": "Average Salary ($K)"},
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.add_vline(x=prediction, line_width=3, line_dash="dash", line_color="red",
                  annotation_text="Your Prediction", annotation_position="top")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Fill in the job details above and click **Predict Salary** to get an estimate.")
