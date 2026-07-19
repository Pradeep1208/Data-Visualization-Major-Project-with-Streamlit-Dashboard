"""
utils.py — shared, cached data & model loading.
Every page imports from here so the CSV / model are only ever loaded once per session.
"""

import pandas as pd
import joblib
import streamlit as st

from config import DATA_PATH, MODEL_PATH, SCALER_PATH, ENCODER_PATH, MODEL_FEATURE_COLS


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load the cleaned & feature-engineered Glassdoor dataset."""
    df = pd.read_csv(DATA_PATH)
    return df


@st.cache_resource
def load_model_artifacts():
    """Load the trained model, scaler, and label encoders saved by the notebook."""
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    encoders = joblib.load(ENCODER_PATH)
    return model, scaler, encoders


def predict_salary(rating, size, ownership, industry, sector, revenue, job_state,
                    same_state, age, python, sql, aws, spark, excel, tableau, powerbi,
                    job_simp, seniority_level, hourly=0, employer_provided=0):
    """Predict average salary ($K) for a new job posting.
    Mirrors the exact encoding/scaling pipeline used during training in the notebook.
    """
    model, scaler, encoders = load_model_artifacts()

    def safe_encode(col_name, value):
        le = encoders[col_name]
        if value in le.classes_:
            return le.transform([value])[0]
        return le.transform([le.classes_[0]])[0]  # unseen category -> fallback

    row = pd.DataFrame([{
        "Rating": rating,
        "Size": safe_encode("Size", size),
        "Type of ownership": safe_encode("Type of ownership", ownership),
        "Industry": safe_encode("Industry", industry),
        "Sector": safe_encode("Sector", sector),
        "Revenue": safe_encode("Revenue", revenue),
        "job_state": safe_encode("job_state", job_state),
        "same_state": same_state,
        "age": age,
        "python_yn": python, "sql_yn": sql, "aws_yn": aws, "spark_yn": spark,
        "excel_yn": excel, "tableau_yn": tableau, "powerbi_yn": powerbi,
        "job_simp": safe_encode("job_simp", job_simp),
        "seniority": safe_encode("seniority", seniority_level),
        "hourly": hourly,
        "employer_provided": employer_provided,
    }])[MODEL_FEATURE_COLS]

    row_scaled = scaler.transform(row)
    prediction = model.predict(row_scaled)[0]
    return round(float(prediction), 1)


def kpi_dict(df: pd.DataFrame) -> dict:
    """Compute the KPI cards shown on the Home page."""
    return {
        "Total Jobs": len(df),
        "Total Companies": df["company_txt"].nunique(),
        "Total Industries": df["Industry"].nunique(),
        "Average Salary ($K)": round(df["avg_salary"].mean(), 1),
        "Highest Salary ($K)": int(df["max_salary"].max()),
        "Lowest Salary ($K)": int(df["min_salary"].min()),
    }
