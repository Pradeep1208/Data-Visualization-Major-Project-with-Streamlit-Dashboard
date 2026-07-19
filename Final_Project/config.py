"""
config.py — central configuration for the Glassdoor Salary Analytics Dashboard.
Import constants from here instead of hard-coding paths/columns in every page.
"""

import os

# ── Paths ─────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "salary_data_cleaned.csv")

MODEL_PATH = os.path.join(BASE_DIR, "models", "salary_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "encoder.pkl")

# ── Feature columns (must match the notebook that trained the model) ───────
SKILL_COLS = ["python_yn", "sql_yn", "aws_yn", "spark_yn", "excel_yn", "tableau_yn", "powerbi_yn"]
SKILL_LABELS = {
    "python_yn": "Python", "sql_yn": "SQL", "aws_yn": "AWS", "spark_yn": "Spark",
    "excel_yn": "Excel", "tableau_yn": "Tableau", "powerbi_yn": "Power BI",
}

CATEGORICAL_COLS = ["Size", "Type of ownership", "Industry", "Sector", "Revenue",
                     "job_state", "job_simp", "seniority"]

MODEL_FEATURE_COLS = [
    "Rating", "Size", "Type of ownership", "Industry", "Sector", "Revenue",
    "job_state", "same_state", "age",
    "python_yn", "sql_yn", "aws_yn", "spark_yn", "excel_yn", "tableau_yn", "powerbi_yn",
    "job_simp", "seniority", "hourly", "employer_provided",
]

# ── Theme ────────────────────────────────────────────────────────────────
PRIMARY_COLOR = "#6C63FF"
PLOTLY_TEMPLATE = "plotly_white"
COLOR_SEQUENCE = ["#6C63FF", "#00C2A8", "#FF6B6B", "#FFC145", "#4D96FF", "#B983FF", "#2EC4B6"]

APP_TITLE = "Glassdoor Jobs & Salary Analytics"
APP_ICON = "💼"
